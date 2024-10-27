from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from sqlalchemy import Integer, Column, String, TIMESTAMP, Boolean, ARRAY
from datetime import datetime
from ...config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER


DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

class Base(DeclarativeBase):
    pass


class User(SQLAlchemyBaseUserTable[int], Base):
    id = Column(Integer, nullable = False, primary_key=True)

    email = Column(String, nullable = False)
    login = Column(String, nullable = False)
    hashed_password = Column(String, nullable = False)
    registered_at = Column(TIMESTAMP, default = datetime.utcnow)
    responses = Column(ARRAY(Integer))
    date_knockout = Column(TIMESTAMP, default = datetime.utcnow)
    profile_img = Column(String, nullable = True)
    is_active = Column(Boolean, default = True, nullable = False)
    is_superuser = Column(Boolean, default = False, nullable = False)
    is_verified = Column(Boolean, default = False, nullable = False)


engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)