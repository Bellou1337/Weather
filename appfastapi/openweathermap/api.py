from httpx import AsyncClient, HTTPStatusError
from appfastapi.config import config
from fastapi import HTTPException, status
from appfastapi.schemas.schemas import UserRequest
from datetime import datetime


token = config['OpenWeatherMap']['token']


async def get_weather_data_now(city_name: str):

    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city_name,
        "appid": token,
        "units": "metric",
    }

    async with AsyncClient() as client:
        response = await client.get(base_url, params=params)
        response.raise_for_status()
        return response.json()


async def weather_now(user_data: UserRequest):
    try:
        weather_data = await get_weather_data_now(user_data.city_name)
        filtered_data = {
            "temperature": weather_data["main"]["temp"],
            "temp_min": weather_data["main"]["temp_min"],
            "temp_max": weather_data["main"]["temp_max"],
            "pressure": weather_data["main"]["pressure"],
            "humidity": weather_data["main"]["humidity"],
            "weather": weather_data["weather"][0]["description"],
            "wind_speed": weather_data["wind"]["speed"]
        }

        user_data.responce = filtered_data
        user_data.date_request = datetime.utcnow()
        return user_data
    except HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail="City not found or error in API request"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )


async def get_weather_the_future(city_name: str):
    base_url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        "q": city_name,
        "units": "metric",
        "appid": token,
    }

    async with AsyncClient() as client:
        response = await client.get(base_url, params=params)
        response.raise_for_status()
        return response.json()


async def weather_the_future(city_name: str):
    try:

        forecast_data = await get_weather_the_future(city_name)

        filtered_data = [
            {
                "date_time": item["dt_txt"],
                "temperature": item["main"]["temp"],
                "temp_min": item["main"]["temp_min"],
                "temp_max": item["main"]["temp_max"],
                "pressure": item["main"]["pressure"],
                "humidity": item["main"]["humidity"],
                "weather": item["weather"][0]["description"],
                "wind_speed": item["wind"]["speed"]
            }
            for item in forecast_data.get("list", [])
        ]

        return {"forecast": filtered_data}

    except HTTPStatusError as e:
        print(f"HTTPStatusError: {e.response.text}")
        raise HTTPException(
            status_code=e.response.status_code,
            detail="City not found or error in API request"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )
