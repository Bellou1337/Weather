from pydantic import BaseModel
from typing import Optional
from pydantic.networks import EmailStr
from fastapi_users import schemas

class ChangePswrd(BaseModel):
    user_id : int
    new_password : str

class ChangeImg(BaseModel):
    user_id : int
    new_img_path: str
    
class ChangeEmail(BaseModel):
    user_id : int
    new_email : str

class UserRead(schemas.BaseUser[int]):
    id: int
    login: str
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class UserCreate(schemas.BaseUserCreate):
    email: EmailStr
    login: str
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserUpdate(schemas.BaseUserUpdate):
    pass
