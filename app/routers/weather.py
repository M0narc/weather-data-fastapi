import io
from fastapi import APIRouter, HTTPException
from matplotlib import pyplot as plt
import seaborn as sns
from fastapi.responses import StreamingResponse
from app.utils.helpers import celsius_to_fahrenheit
from app.services.weather_service import OUTPUT_FILE, fetch_weather_data, process_weather_data, save_to_csv

router = APIRouter(prefix="/weather", tags=["Weather"])

@router.get("/fetch")
def fetch_weather():
    data = fetch_weather_data()
    if not data:
        raise HTTPException(status_code=404, detail="No weather data found")
    
    df = process_weather_data(data)
    save_to_csv(df, OUTPUT_FILE)

    return {"message": f"Weather data saved to {OUTPUT_FILE}"}


@router.get("/csv")
def get_csv():
    # Serve the CSV file for download
    try:
        return StreamingResponse(open(OUTPUT_FILE, "rb"), media_type="text/csv", headers={"Content-Disposition": f"attachment; filename={OUTPUT_FILE}"})
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="CSV file not found")
    

@router.get("/plot")
def plot_weather_data():
    # Fetch and process the weather data
    data = fetch_weather_data()
    if not data:
        raise HTTPException(status_code=404, detail="No weather data found")
    
    df = process_weather_data(data)

    # Generate a bar chart of temperatures
    plt.figure(figsize=(10, 6))
    sns.barplot(x="City", y="Temperature (C)", data=df, palette="coolwarm")
    plt.title("Temperatures of Cities")
    plt.xlabel("City")
    plt.ylabel("Temperature (Celsius)")

    # Save the plot to a BytesIO buffer
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()

    # Return the plot as a response
    return StreamingResponse(buf, media_type="image/png")