from fastapi import HTTPException, APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from appfastapi.database.database import get_async_session
from sqlalchemy import select, update
from appfastapi.models.models import request, user
from appfastapi.schemas.schemas import UserRead, UserReadAll, UserImg, UserRequests, ChangePswrd, ChangeImg, ChangeEmail
from appfastapi.auth.auth import fastapi_users
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError

router = APIRouter(
    prefix="/db",
    tags=["database"]
)

current_user = fastapi_users.current_user()


@router.get("/user_info", response_model=UserRead)
async def get_user(user_data: UserRead = Depends(current_user)):
    try:
        return user_data
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "User not found"}
        )


@router.get("/user_info_all", response_model=UserReadAll)
async def get_user_all(user_data: UserReadAll = Depends(current_user)):
    try:
        return user_data
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "User not found"}
        )


@router.get("/user_image", response_model=UserImg)
async def get_img(user_data: UserImg = Depends(current_user)):
    try:
        return user_data
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "User not found"}
        )


@router.get("/user_requests", response_model=UserRequests)
async def get_requests(user_data: UserRequests = Depends(current_user)):
    try:
        return user_data
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "User not found"}
        )


@router.post("/change_password")
async def set_new_pswrd(user_data: ChangePswrd, user_info=Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    try:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        hash_pswrd = pwd_context.hash(user_data.new_password)
        querry = update(user).where(user.c.id == user_info.id).values(
            hashed_password=hash_pswrd)
        await session.execute(querry)
        await session.commit()

        return {"status": "Password update"}
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "User not found"}
        )


@router.post("/change_image")
async def set_new_img(user_data: ChangeImg, user_info=Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    try:
        querry = update(user).where(user.c.id == user_info.id).values(
            profile_img=user_data.new_img_path)
        await session.execute(querry)
        await session.commit()

        return {"status": "Image update"}
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "User not found"}
        )


@router.post("/change_email")
async def set_new_email(user_data: ChangeEmail, user_info=Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    try:
        querry = update(user).where(user.c.id == user_info.id).values(
            email=user_data.new_email)
        await session.execute(querry)
        await session.commit()

        return {"status": "Email update"}
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Email length is invalid"}
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "User not found"}
        )
