from sqlalchemy import MetaData,Table,Integer,Column,String,TIMESTAMP,JSON,ForeignKey,Boolean
from datetime import datetime

meta_data = MetaData()

user = Table(
    "user",
    meta_data,
    Column("id",Integer,primary_key = True),
    Column("email",String,nullable = False),
    Column("login",String,nullable = False),
    Column("hashed_password",String, nullable = False),
    Column("registered_at",TIMESTAMP, default = datetime.utcnow()),
    Column("response",Integer,ForeignKey("request.id")),
    Column("date_knockout",TIMESTAMP, default = datetime.utcnow()),
    Column("profile_img",String), 
    Column("is_active",Boolean, default = True, nullable = False),
    Column("is_superuser",Boolean, default = False, nullable = False),
    Column("is_verified",Boolean, default = False, nullable = False),
)

request = Table(
    "request",
    meta_data,
    Column("id",Integer,primary_key = True),
    Column("city_name",String, nullable = True),
    Column("date_request",TIMESTAMP,nullable = True),
    Column("responce",JSON,nullable = True),
)
