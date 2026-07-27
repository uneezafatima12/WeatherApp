from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

from .database import Base


class WeatherHistory(Base):
    __tablename__ = "weather_history"

    id = Column(Integer, primary_key=True, index=True)

    city = Column(String(100), nullable=False)
    country = Column(String(10), nullable=False)

    temperature = Column(Float, nullable=False)
    humidity = Column(Integer, nullable=False)
    wind_speed = Column(Float, nullable=False)

    description = Column(String(200), nullable=False)

    searched_at = Column(DateTime, default=datetime.utcnow)