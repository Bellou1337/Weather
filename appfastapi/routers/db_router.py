from fastapi import HTTPException, APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError
from sqlalchemy import insert, update, func, select
from appfastapi.database import get_async_session
from appfastapi.models import request, user
from appfastapi.schemas import UserRead, UserReadAll, UserImg, UserRequests, ChangePswrd, ChangeImg, ChangeEmail, UserRequest
from appfastapi.dependencies import current_user


router = APIRouter(
    prefix="/db",
    tags=["database"]
)


@router.get("/user_info", response_model=UserRead)
async def get_user(user_data: UserRead = Depends(current_user)):
    try:
        return user_data
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"detail": "User not found"}
        )


@router.get("/user_info_all", response_model=UserReadAll)
async def get_user_all(user_data: UserReadAll = Depends(current_user)):
    try:
        return user_data
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"detail": "User not found"}
        )


@router.get("/user_image", response_model=UserImg)
async def get_img(user_data: UserImg = Depends(current_user)):
    try:
        return user_data
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"detail": "User not found"}
        )


@router.get("/user_requests", response_model=UserRequests)
async def get_requests(user_data: UserRequests = Depends(current_user)):
    try:
        return user_data
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"detail": "User not found"}
        )


@router.post("/change_password")
async def set_new_pswrd(user_data: ChangePswrd, user_info=Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    try:
        if len(user_data.new_password) < 6:
            return {"detail": "Password length is invalid"}

        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        hash_pswrd = pwd_context.hash(user_data.new_password)
        stmt = update(user).where(user.c.id == user_info.id).values(
            hashed_password=hash_pswrd)
        await session.execute(stmt)
        await session.commit()

        return {"detail": "Password update"}
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"detail": "User not found"}
        )


@router.post("/change_image")
async def set_new_img(user_data: ChangeImg, user_info=Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = update(user).where(user.c.id == user_info.id).values(
            profile_img=user_data.new_img_path)
        await session.execute(stmt)
        await session.commit()

        return {"detail": "Image update"}
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"detail": "User not found"}
        )


@router.post("/change_email")
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
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"detail": "User not found"}
        )


@router.post("/add_request")
async def add_new_request(user_data: UserRequest, user_info=Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    try:
        user_data.date_request = user_data.date_request.replace(tzinfo=None)
        request_stmt = insert(request).values(user_data.dict())
        result = await session.execute(request_stmt)
        await session.commit()

        request_id = result.inserted_primary_key[0]

        current_responses_query = select(
            user.c.responses).where(user.c.id == user_info.id)
        current_responses_result = await session.execute(current_responses_query)
        result_data = current_responses_result.fetchone()
        result_data = dict(result_data._mapping)
        result_array = result_data['responses']

        if len(result_array) == 10:
            result_array = result_array[1:]

        result_array = [request_id] + result_array

        user_stmt = update(user).where(user.c.id == user_info.id).values(
            responses=result_array)
        await session.execute(user_stmt)
        await session.commit()

        return {"detail": "Request successfully added"}
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "detail": "Failed to add request due to invalid data or server error"}
        )
