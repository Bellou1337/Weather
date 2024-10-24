from pydantic import BaseModel

class RegUser(BaseModel):
    login: str
    email: str
    hashed_password: str