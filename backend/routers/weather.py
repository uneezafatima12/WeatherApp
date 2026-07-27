from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import httpx
import os

from ..database import SessionLocal
from ..models import WeatherHistory

load_dotenv("backend/.env")

API_KEY = os.getenv("OPENWEATHER_API_KEY")

router = APIRouter(
    prefix="/weather",
    tags=["Weather"]
)


# Database connection
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# Get current weather
@router.get("/{city}")
async def get_weather(
    city: str,
    db: Session = Depends(get_db)
):

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

    # Weather information
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


# Get weather search history
@router.get("/history/all")
def get_history(db: Session = Depends(get_db)):

    history = (
        db.query(WeatherHistory)
        .order_by(WeatherHistory.searched_at.desc())
        .all()
    )

    return history

@router.delete("/history/clear")
def clear_history(db: Session = Depends(get_db)):

    db.query(WeatherHistory).delete()

    db.commit()

    return {
        "message": "Weather history cleared successfully"
    }