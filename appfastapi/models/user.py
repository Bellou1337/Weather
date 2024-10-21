from pydantic import BaseModel
import datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class User(BaseModel):
    login: str
    email: str | None = None
    profile_igm: str | None = None
    disabled: bool | None = None

class UserResponses(User):
    responses: list[int]

class UserInDB(User):
    id: int
    date_knockout: datetime.datetime
    registration_date: datetime.datetime
    hashed_password: str