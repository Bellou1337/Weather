from pydantic import BaseModel
from typing import Optional, List
from pydantic.networks import EmailStr
from fastapi_users import schemas
from datetime import datetime


class ChangePswrd(BaseModel):
    new_password: str


class ChangePswrdData(BaseModel):
    detail: str


class ChangeImg(BaseModel):
    new_img_path: str


class ChangeImgData(BaseModel):
    detail: str


class ChangeEmail(BaseModel):
    new_email: str


class ChangeEmailData(BaseModel):
    detail: str


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
    responses: List[str] | None


class WeatherRequest(BaseModel):
    city_name: str
    date_time: datetime


class UserCreate(schemas.BaseUserCreate):
    email: EmailStr
    login: str
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class WeatherInfoData(BaseModel):
    date_time: str
    temperature: float
    temp_min: float
    temp_max: float
    pressure: int
    humidity: int
    weather: str
    wind_speed: float


class WeatherInfo(BaseModel):
    detail: WeatherInfoData


class GetRequests(BaseModel):
    detail: List[WeatherInfoData]


class UserUpdate(schemas.BaseUserUpdate):
    pass


class NewEmail(BaseModel):
    pass
