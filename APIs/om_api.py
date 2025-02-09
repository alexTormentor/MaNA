from fastapi import FastAPI, APIRouter
import requests
from datetime import date

app = FastAPI(
    title="Weather API", openapi_url="/openapi.json"
)

api_router = APIRouter()


@api_router.get("/weather/current/{latitude}/{longitude}", status_code=200)
def get_current_weather(latitude: float, longitude: float):
    """
    Get current weather for a given latitude and longitude
    """
    weather_info = {}
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
        response = requests.get(url)

        if response.status_code == 200 and 'json' in response.headers['content-type']:
            weather_info = response.json().get("current_weather", {})
    except:
        weather_info = {"error": "Could not fetch weather data"}

    return weather_info


@api_router.get("/weather/history/{latitude}/{longitude}", status_code=200)
def get_historical_weather(latitude: float, longitude: float, start_date: date, end_date: date):
    """
    Get historical weather data for a given latitude, longitude, and date range
    """
    weather_history = {}
    try:
        url = f"https://archive-api.open-meteo.com/v1/era5?latitude={latitude}&longitude={longitude}&start_date={start_date}&end_date={end_date}&daily=temperature_2m_max,temperature_2m_min&timezone=UTC"
        response = requests.get(url)

        if response.status_code == 200 and 'json' in response.headers['content-type']:
            weather_history = response.json().get("daily", {})
    except Exception as e:
        weather_history = {"error": f"Could not fetch historical weather data: {str(e)}"}

    return weather_history


@api_router.get("/weather/forecast/{latitude}/{longitude}", status_code=200)
def get_weather_forecast(latitude: float, longitude: float):
    """
    Get weather forecast for a given latitude and longitude in a simplified format
    """
    forecast_info = []
    try:
        # Запрос к Open-Meteo API для прогноза погоды, осадков и скорости ветра
        url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,precipitation,windspeed_10m"
        response = requests.get(url)

        if response.status_code == 200 and 'json' in response.headers['content-type']:
            hourly_data = response.json().get("hourly", {})
            temperatures = hourly_data.get("temperature_2m", [])
            precipitations = hourly_data.get("precipitation", [])
            wind_speeds = hourly_data.get("windspeed_10m", [])
            timestamps = hourly_data.get("time", [])
            
            for i in range(0, len(timestamps), 3):  # Берём данные через каждые 3 часа
                forecast_info.append({
                    "time": timestamps[i],
                    "temperature": temperatures[i],
                    "precipitation": precipitations[i],
                    "wind_speed": wind_speeds[i]
                })
    except:
        forecast_info = {"error": "Could not fetch weather forecast data"}

    return forecast_info


app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")



'''GET http://0.0.0.0:8001/weather/forecast/48.8566/2.3522
http://localhost:8001/weather/history/48.8566/2.3522?start_date=2024-10-01&end_date=2024-10-05
GET http://0.0.0.0:8001/weather/current/48.8566/2.3522'''