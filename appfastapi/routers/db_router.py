from fastapi import APIRouter,Depends
from schemas.schemas import RegUser
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import get_async_session
from sqlalchemy import insert,select
from models.models import user

router = APIRouter(
    prefix="/db",
    tags=["DataBase"]
)

@router.post("/create_user")
async def add_user(new_user: RegUser, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(user).values(**new_user.dict())
    await session.execute(stmt)
    await session.commit()
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