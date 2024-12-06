from fastapi import FastAPI
from app.routers import weather

app = FastAPI(title="Weather Data API")

# Include router
app.include_router(weather.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Weather Data API"}
