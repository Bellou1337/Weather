from fastapi import HTTPException, APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import update, select
from appfastapi.database import get_async_session
from appfastapi.models import user
from appfastapi.schemas import UserImg, UserRequests, ChangeImg, ChangeEmail
from appfastapi.schemas import WeatherInfo, ChangeEmailData, ChangeImgData, GetRequests
from appfastapi.dependencies import current_user
from appfastapi.openweathermap.api import weather_the_future
from typing import Dict
from appfastapi.database.redis import RedisTools

router = APIRouter(
    prefix="/db",
    tags=["database"]
)


@router.get("/user_image", response_model=UserImg)
async def get_img(user_data: UserImg = Depends(current_user)):
    try:
        return user_data
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"detail": "User not found"}
        )


@router.get("/get_user_requests", response_model=GetRequests)
async def get_requests(user_data: UserRequests = Depends(current_user)):
    try:
        responses = user_data.responses

        all_responses = []

        for response in responses:
            data = RedisTools.get_request(response)
            all_responses.append(data)

        return {"detail": all_responses}

    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"detail": "User not found"}
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"detail": "error on the server something with requests "}
        )


@router.post("/change_image", response_model=ChangeImgData)
async def set_new_img(user_data: ChangeImg, user_info=Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = update(user).where(user.c.id == user_info.id).values(
            profile_img=user_data.new_img_path)
        await session.execute(stmt)
        await session.commit()

        return {"detail": "Image update"}
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"detail": "User not found"}
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"detail": "server error something with the data"}
        )


@router.post("/change_email", response_model=ChangeEmailData)
async def set_new_email(user_data: ChangeEmail, user_info=Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    try:

        if len(user_data.new_email) < 6 or len(user_data.new_email) > 255:
            return {"detail": "Email length is invalid"}

        stmt = update(user).where(user.c.id == user_info.id).values(
            email=user_data.new_email)
        await session.execute(stmt)
        await session.commit()

        return {"detail": "Email update"}
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"detail": "Email length is invalid"}
        )
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"detail": "User not found"}
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"detail": "server error something with the data"}
        )


@router.post("/get_weather_info", response_model=WeatherInfo)
async def add_new_request(key=Depends(weather_the_future), user_info=Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    try:

        query = select(user.c.responses).where(user.c.id == user_info.id)
        result = await session.execute(query)
        result_data = result.fetchone()
        result_dict = dict(result_data._mapping)
        result_arr = result_dict['responses']
        if result_arr == None:
            result_arr = []
        elif len(result_arr) == 10:
            result_arr = result_arr[: -1]

        result_arr = [key] + result_arr

        stmt = update(user).where(
            user.c.id == user_info.id).values(responses=result_arr)
        await session.execute(stmt)
        await session.commit()

        data = RedisTools.get_request(key)
        return {"detail": data}

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "detail": "Failed to add request due to invalid data or server error"}
        )


@router.get("/get_cities")
async def get_cities_list():
    try:
        redis_cities = RedisTools.get_city_list()
        decoded_cities = [city.decode('utf-8') for city in redis_cities]
        return {"detail": decoded_cities}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"detail": "Error while getting cities list"}
        )
