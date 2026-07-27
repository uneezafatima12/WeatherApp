from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .database import engine, Base
from . import models

from .routers import weather
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Weather App API",
    version="1.0.0"
)

# Weather API routes
app.include_router(weather.router)

# Serve frontend
app.mount(
    "/",
    StaticFiles(directory="frontend", html=True),
    name="frontend"
)