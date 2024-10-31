from httpx import AsyncClient, HTTPStatusError
from appfastapi.config import config
from fastapi import HTTPException, status
from appfastapi.schemas.schemas import UserRequest
from datetime import datetime

token = config['TOKEN']['key']


async def get_weather_data(city_name: str):

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


async def get_weather(user_data: UserRequest):
    try:
        weather_data = await get_weather_data(user_data.city_name)
        weather_data.pop("coord", None)
        weather_data.pop("sys", None)
        weather_data.pop("dt", None)
        weather_data.pop("timezone", None)
        weather_data.pop("id", None)
        weather_data.pop("name", None)
        weather_data.pop("cod", None)

        user_data.responce = weather_data
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
