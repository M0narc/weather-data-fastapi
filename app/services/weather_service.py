import requests
import pandas as pd
from app.utils.helpers import celsius_to_fahrenheit, mps_to_mph
from pathlib import Path
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Sample city data
CITIES = [
    {"City": "New York", "Latitude": 40.7128, "Longitude": -74.0060},
    {"City": "Tokyo", "Latitude": 35.6895, "Longitude": 139.6917},
    {"City": "London", "Latitude": 51.5074, "Longitude": -0.1278},
    {"City": "Paris", "Latitude": 48.8566, "Longitude": 2.3522},
    {"City": "Berlin", "Latitude": 52.5200, "Longitude": 13.4050},
    {"City": "Sydney", "Latitude": -33.8688, "Longitude": 151.2093},
    {"City": "Mumbai", "Latitude": 19.0760, "Longitude": 72.8777},
    {"City": "Cape Town", "Latitude": -33.9249, "Longitude": 18.4241},
    {"City": "Moscow", "Latitude": 55.7558, "Longitude": 37.6173},
    {"City": "Rio de Janeiro", "Latitude": -22.9068, "Longitude": -43.1729}

]

BASE_URL = "https://api.open-meteo.com/v1/forecast"
OUTPUT_FILE = "output/weather_data.csv"


def fetch_weather_data():
    """Fetch weather data for the specified cities."""
    weather_data = []
    for city in CITIES:
        params = {
            "latitude": city["Latitude"],
            "longitude": city["Longitude"],
            "current_weather": True,
            "hourly": "relativehumidity_2m",
        }
        try:
            logging.info(f"Fetching data for {city['City']}...")
            response = requests.get(BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            print(data)

            # Validate response data
            if "current_weather" not in data:
                logging.warning(f"No 'current_weather' found for {city['City']}: {data}")
                continue

            current_weather = data["current_weather"]

            # Extract humidity
            humidity = None
            if "hourly" in data and "relativehumidity_2m" in data["hourly"]:
                try:
                    current_time = current_weather["time"]
                    print("current time ->", current_time)
                    print("----------")
                    t_index = data["hourly"]["time"].index(current_time)
                    print("index time", t_index)
                    print("----------")
                    humidity = data["hourly"]["relativehumidity_2m"][t_index]
                    print("humidity ->", humidity)
                    print("----------")
                except ValueError:
                    logging.warning(f"Time mismatch for {city['City']}")
                    continue

            # Convert wind speed (if exists)
            wind_speed = current_weather.get("windspeed", 0)
            wind_speed_ms = wind_speed / 3.6

            # Append data
            weather_data.append({
                "City": city["City"],
                "Temperature (C)": current_weather["temperature"],
                "Temperature (F)": celsius_to_fahrenheit(current_weather["temperature"]),
                "Humidity (%)": humidity,
                "Wind Speed (m/s)": round(wind_speed_ms, 2),
            })
            logging.info(f"Data fetched successfully for {city['City']}.")

        except requests.exceptions.RequestException as e:
            logging.error(f"Network error for {city['City']}: {e}")
        except KeyError as e:
            logging.error(f"Data parsing error for {city['City']}: {e}")

    return weather_data

def process_weather_data(data):
    df = pd.DataFrame(data)
    df["Temperature (F)"] = df["Temperature (C)"].apply(celsius_to_fahrenheit)
    df["Wind Speed (mph)"] = df["Wind Speed (m/s)"].apply(mps_to_mph)
    return df

def save_to_csv(df, filepath):
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(filepath, index=False)
