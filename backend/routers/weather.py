from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from dotenv import load_dotenv

import httpx
import os
import csv
import io


from ..database import SessionLocal
from ..models import WeatherHistory


# Load environment variables
load_dotenv("backend/.env")

API_KEY = os.getenv("OPENWEATHER_API_KEY")


router = APIRouter(
    prefix="/weather",
    tags=["Weather"]
)


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# ============================================================
# GET CURRENT WEATHER
# ============================================================

@router.get("/{city}")
async def get_weather(
    city: str,
    db: Session = Depends(get_db)
):

    city = city.strip()

    if not city:
        raise HTTPException(
            status_code=400,
            detail="City name cannot be empty"
        )

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={API_KEY}&units=metric"
    )

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    if response.status_code != 200:
        raise HTTPException(
            status_code=404,
            detail="City not found"
        )

    data = response.json()

    weather_data = {
        "city": data["name"],
        "country": data["sys"]["country"],
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"],
        "description": data["weather"][0]["description"]
    }

    # Save search to database
    history = WeatherHistory(
        city=weather_data["city"],
        country=weather_data["country"],
        temperature=weather_data["temperature"],
        humidity=weather_data["humidity"],
        wind_speed=weather_data["wind_speed"],
        description=weather_data["description"]
    )

    db.add(history)
    db.commit()
    db.refresh(history)

    return weather_data



# ============================================================
# GET 5-DAY WEATHER FORECAST
# ============================================================

@router.get("/forecast/{city}")
async def get_forecast(city: str):

    city = city.strip()

    if not city:
        raise HTTPException(
            status_code=400,
            detail="City name cannot be empty"
        )

    url = (
        f"https://api.openweathermap.org/data/2.5/forecast"
        f"?q={city}&appid={API_KEY}&units=metric"
    )

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    if response.status_code != 200:
        raise HTTPException(
            status_code=404,
            detail="City not found"
        )

    data = response.json()

    forecast = []

    # OpenWeather provides forecasts every 3 hours.
    # Select one forecast around midday for each day.
    days_seen = set()

    for item in data["list"]:

        date_value = item["dt_txt"].split(" ")[0]
        time = item["dt_txt"].split(" ")[1]

        # Prefer 12:00 forecast
        if (
            time == "12:00:00"
            and date_value not in days_seen
        ):

            forecast.append({
                "date": date_value,
                "temperature": item["main"]["temp"],
                "humidity": item["main"]["humidity"],
                "wind_speed": item["wind"]["speed"],
                "description": item["weather"][0]["description"]
            })

            days_seen.add(date_value)

        if len(forecast) == 5:
            break

    return {
        "city": data["city"]["name"],
        "country": data["city"]["country"],
        "forecast": forecast
    }


# ============================================================
# GOOGLE MAPS LOCATION
# ============================================================

@router.get("/maps/{city}")
def get_map_location(city: str):

    city = city.strip()

    if not city:
        raise HTTPException(
            status_code=400,
            detail="City name cannot be empty"
        )

    maps_url = (
        "https://www.google.com/maps/search/"
        + city.replace(" ", "+")
    )

    return {
        "city": city,
        "maps_url": maps_url
    }


# ============================================================
# READ WEATHER HISTORY
# ============================================================

@router.get("/history/all")
def get_history(
    db: Session = Depends(get_db)
):

    history = (
        db.query(WeatherHistory)
        .order_by(
            WeatherHistory.searched_at.desc()
        )
        .all()
    )

    return history


# ============================================================
# UPDATE WEATHER HISTORY
# ============================================================

@router.put("/history/{history_id}")
def update_history(
    history_id: int,
    city: str | None = None,
    temperature: float |None = None,
    humidity: int | None = None,
    wind_speed: float | None = None,
    description: str | None = None,
    db: Session = Depends(get_db)
):

    history = (
        db.query(WeatherHistory)
        .filter(
            WeatherHistory.id == history_id
        )
        .first()
    )

    if not history:
        raise HTTPException(
            status_code=404,
            detail="Weather history record not found"
        )

    # Validate city
    if city is not None:

        city = city.strip()

        if not city:
            raise HTTPException(
                status_code=400,
                detail="City cannot be empty"
            )

        history.city = city

    

    # Validate humidity
    if humidity is not None:

        if humidity < 0 or humidity > 100:
            raise HTTPException(
                status_code=400,
                detail="Humidity must be between 0 and 100"
            )

        history.humidity = humidity

    # Validate wind speed
    if wind_speed is not None:

        if wind_speed < 0:
            raise HTTPException(
                status_code=400,
                detail="Wind speed cannot be negative"
            )

        history.wind_speed = wind_speed

    # Temperature
    if temperature is not None:
        history.temperature = temperature

    # Description
    if description is not None:
        history.description = description.strip()

    db.commit()
    db.refresh(history)

    return {
        "message": "Weather history updated successfully",
        "record": history
    }


# ============================================================
# DELETE ALL WEATHER HISTORY
# ============================================================

@router.delete("/history/clear")
def clear_history(
    db: Session = Depends(get_db)
):

    db.query(WeatherHistory).delete()

    db.commit()

    return {
        "message": "Weather history cleared successfully"
    }


# ============================================================
# DELETE ONE WEATHER HISTORY RECORD
# ============================================================

@router.delete("/history/{history_id}")
def delete_history(
    history_id: int,
    db: Session = Depends(get_db)
):

    history = (
        db.query(WeatherHistory)
        .filter(
            WeatherHistory.id == history_id
        )
        .first()
    )

    if not history:
        raise HTTPException(
            status_code=404,
            detail="Weather history record not found"
        )

    db.delete(history)
    db.commit()

    return {
        "message": "Weather history record deleted successfully"
    }


# ============================================================
# EXPORT WEATHER HISTORY AS CSV
# ============================================================

@router.get("/history/export/csv")
def export_history_csv(
    db: Session = Depends(get_db)
):

    history = (
        db.query(WeatherHistory)
        .order_by(
            WeatherHistory.searched_at.desc()
        )
        .all()
    )

    output = io.StringIO()

    writer = csv.writer(output)

    # CSV header
    writer.writerow([
    "ID",
    "City",
    "Country",
    "Temperature",
    "Humidity",
    "Wind Speed",
    "Description",
    "Searched At"
])

    # CSV data
    for item in history:

        writer.writerow([
        item.id,
        item.city,
        item.country,
        item.temperature,
        item.humidity,
        item.wind_speed,
        item.description,
        item.searched_at
])

    output.seek(0)

    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition":
                "attachment; filename=weather_history.csv"
        }
    )