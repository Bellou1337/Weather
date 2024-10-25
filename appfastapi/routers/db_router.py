from fastapi import HTTPException,APIRouter,Depends,status
from schemas.schemas import RegUser,ChangePswrd,ChangeImg,ChangeEmail
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import get_async_session
from sqlalchemy import insert,select,update
from models.models import request, user

router = APIRouter(
    prefix="/db",
    tags=["DataBase"]
)

@router.post("/create_user")
async def add_user(new_user: RegUser, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(user).values(**new_user.dict())
    result = await session.execute(stmt)
    await session.commit()
    
    if result.rowcount == 0:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "Failed to create user"
        )
    
    return {"status": "success"}

@router.get("/user_info")
async def get_user(user_id: int, session: AsyncSession = Depends(get_async_session)):
    querry = select(user.c.login,user.c.hashed_password,user.c.email,user.c.is_active).where(user.c.id == user_id)
    result = await session.execute(querry)
    user_data = result.fetchone()
    
    if user_data:
        return dict(user_data._mapping)
    
    return {"error": "not found"}

@router.get("/user_info_all")
async def get_user_all(user_id: int, session: AsyncSession = Depends(get_async_session)):
    querry = select(user.c.email,user.c.login,user.c.hashed_password,
    user.c.registered_at,user.c.date_knockout,user.c.profile_img,
    user.c.is_active,user.c.is_superuser,user.c.is_verified).where(user.c.id == user_id)
    
    result = await session.execute(querry)
    user_data = result.fetchone()
    
    if user_data:
        return dict(user_data._mapping)
    
    return {"error" : "not found"}


@router.get("/user_img")
async def get_img(user_id: int, session: AsyncSession = Depends(get_async_session)):
    querry = select(user.c.profile_img,user.c.login).where(user.c.id == user_id)
    result = await session.execute(querry)
    user_data = result.fetchone()
    
    if user_data:
        return dict(user_data._mapping)
    
    return {"error" : "not found"}


@router.get("/user_request")
async def get_requests(user_id : int, session: AsyncSession = Depends(get_async_session)):
    querry = select(request.c.city_name,request.c.date_request,request.c.responce).where(request.c.id == user_id)
    result = await session.execute(querry)
    user_data = result.fetchall()
    
    if user_data:
        return [dict(row._mapping) for row in user_data]
    
    return {"error" : "not found"}



@router.post("/change_password")
async def set_new_pswrd(user_data: ChangePswrd, session: AsyncSession = Depends(get_async_session)):
    querry = update(user).where(user.c.id == user_data.user_id).values(hashed_password = user_data.new_password)
    result = await session.execute(querry)
    await session.commit()
    
    if result.rowcount == 0:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail = "User not found"
        )
    
    return {"status": "password update"}


@router.post("/change_img")
async def set_new_img(user_data: ChangeImg, session: AsyncSession = Depends(get_async_session)):
    querry = update(user).where(user.c.id == user_data.user_id).values(profile_img = user_data.new_img_path)
    result = await session.execute(querry)
    await session.commit()
    
    if result.rowcount == 0:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "User not found"
        )
    
    return {"status": "image update"}

@router.post("/change_email")
async def set_new_email(user_data: ChangeEmail, session: AsyncSession = Depends(get_async_session)):
    querry = update(user).where(user.c.id == user_data.user_id).values(email = user_data.new_email)
    result = await session.execute(querry)
    await session.commit()
    
    if result.rowcount == 0:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "User not found"
        )
        
    return {"status": "email update"}  