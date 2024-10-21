from sqlalchemy import MetaData,Table,Integer,Column,String,TIMESTAMP,JSON,ForeignKey
from datetime import datetime

meta_data = MetaData()


''' 
    (по поводу profile_img) короче будем хранить ссылку на локальный путь
    2 вариант есть, но он мне не нравится, потому что нужно хранить бинарник
    но потом его придётся обратно конвертировать, я не знаю насколько это хороший варик,
    потому что мб потом из-за этого фотка сожмётся и будет плохое качество
'''

user = Table(
    "user",
    meta_data,
    Column("id",Integer,primary_key = True),
    Column("email",String,nullable = False),
    Column("login",String,nullable = False),
    Column("hashed_password",String,nullable = False),
    Column("registered_at",TIMESTAMP, default = datetime.utcnow()),
    Column("response",Integer,ForeignKey("request.id")),
    Column("date_knockout",TIMESTAMP, nullable = True),
    Column("profile_img",String, nullable = True), 
    
)

request = Table(
    "request",
    meta_data,
    Column("id",Integer,primary_key = True),
    Column("city_name",String, nullable = True),
    Column("date_request",TIMESTAMP,nullable = True),
    Column("responce",JSON,nullable = True),
)
