from httpx import AsyncClient, HTTPStatusError
from appfastapi.config import config
from fastapi import HTTPException, status
from appfastapi.schemas.schemas import WeatherRequest
from datetime import datetime
from appfastapi.database.redis import RedisTools

token = config['OpenWeatherMap']['token']


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


async def weather_the_future(data: WeatherRequest):
    try:
        dt_search = datetime.strftime(
            data.date_time, "%Y.%m.%d") + f"-{data.date_time.hour}"
        key_search = f"weather:{data.city_name}-{dt_search}"
        print(key_search)
        cached_data = RedisTools.get_request(key_search)

        if cached_data:
            return key_search

        forecast_data = await get_weather_the_future(data.city_name)

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

        for object in filtered_data:
            date_part, time_part = object['date_time'].split(" ")
            hour = str(int(time_part.split(":")[0]))
            set_dt = f"{date_part.replace('-', '.')}-{hour}"
            set_key = f"weather:{data.city_name}-{set_dt}"
            RedisTools.set_request(set_key, object)

        cached_data = RedisTools.get_request(key_search)
        if cached_data:
            return key_search

        raise Exception(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requested data not found in cache or API response"
        )

    except HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail="City not found or error in API request"
        )
    except HTTPException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requested data not found in cache or API response"
        )
