from pydantic import BaseModel
from typing import Optional, List
from pydantic.networks import EmailStr
from fastapi_users import schemas
from datetime import datetime


class ChangePswrd(BaseModel):
    new_password: str


class ChangeImg(BaseModel):
    new_img_path: str


class ChangeEmail(BaseModel):
    new_email: str


class UserRead(schemas.BaseUser[int]):
    id: int
    login: str
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class UserReadAll(UserRead):
    hashed_password: str
    registered_at: datetime
    date_knockout: datetime
    profile_img: str | None


class UserImg(BaseModel):
    profile_img: str | None
    login: str


class UserRequests(BaseModel):
    responses: List[int] | None


class UserCreate(schemas.BaseUserCreate):
    email: EmailStr
    login: str
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserUpdate(schemas.BaseUserUpdate):
    pass
