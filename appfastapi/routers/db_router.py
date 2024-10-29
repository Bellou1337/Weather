from fastapi import HTTPException, APIRouter, Depends, status
from appfastapi.schemas.schemas import ChangePswrd, ChangeImg, ChangeEmail
from sqlalchemy.ext.asyncio import AsyncSession
from appfastapi.database.database import get_async_session
from sqlalchemy import select, update
from appfastapi.models.models import request, user
from appfastapi.schemas.schemas import UserRead
from appfastapi.auth.auth import fastapi_users

router = APIRouter(
    prefix="/db",
    tags=["database"]
)

current_user = fastapi_users.current_user()


@router.get("/user_info", response_model=UserRead)
async def get_user(user_info: UserRead = Depends(current_user)):

    return user_info


@router.get("/user_info_all")
async def get_user_all(user_id: int, session: AsyncSession = Depends(get_async_session)):
    querry = select(user.c.email, user.c.login, user.c.hashed_password,
                    user.c.registered_at, user.c.date_knockout, user.c.profile_img,
                    user.c.is_active, user.c.is_superuser, user.c.is_verified).where(user.c.id == user_id)

    result = await session.execute(querry)
    user_data = result.fetchone()

    if user_data:
        return dict(user_data._mapping)

    return {"error": "user not found"}


@router.get("/user_img")
async def get_img(user_id: int, session: AsyncSession = Depends(get_async_session)):
    querry = select(user.c.profile_img, user.c.login).where(
        user.c.id == user_id)
    result = await session.execute(querry)
    user_data = result.fetchone()

    if user_data:
        return dict(user_data._mapping)

    return {"error": "user not found"}


@router.get("/user_request")
async def get_requests(user_id: int, session: AsyncSession = Depends(get_async_session)):
    querry = select(request.c.city_name, request.c.date_request,
                    request.c.responce).where(request.c.user_id == user_id)
    result = await session.execute(querry)
    user_data = result.fetchall()

    if user_data:
        return [dict(row._mapping) for row in user_data]

    return {"error": "user not found"}


@router.post("/change_password")
async def set_new_pswrd(user_data: ChangePswrd, session: AsyncSession = Depends(get_async_session)):
    querry = update(user).where(user.c.id == user_data.user_id).values(
        hashed_password=user_data.new_password)
    result = await session.execute(querry)
    await session.commit()

    if result.rowcount == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found"
        )

    return {"status": "password update"}


@router.post("/change_img")
async def set_new_img(user_data: ChangeImg, session: AsyncSession = Depends(get_async_session)):
    querry = update(user).where(user.c.id == user_data.user_id).values(
        profile_img=user_data.new_img_path)
    result = await session.execute(querry)
    await session.commit()

    if result.rowcount == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found"
        )

    return {"status": "image update"}


@router.post("/change_email")
async def set_new_email(user_data: ChangeEmail, session: AsyncSession = Depends(get_async_session)):
    querry = update(user).where(user.c.id == user_data.user_id).values(
        email=user_data.new_email)
    result = await session.execute(querry)
    await session.commit()

    if result.rowcount == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found"
        )

    return {"status": "email update"}
