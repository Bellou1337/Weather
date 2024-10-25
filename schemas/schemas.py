from pydantic import BaseModel

class RegUser(BaseModel):
    login: str
    email: str
    hashed_password: str


class ChangePswrd(BaseModel):
    user_id : int
    new_password : str

class ChangeImg(BaseModel):
    user_id : int
    new_img_path: str
    
class ChangeEmail(BaseModel):
    user_id : int
    new_email : str
     