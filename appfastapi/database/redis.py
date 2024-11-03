import redis
from appfastapi.config import config
from json import dumps,loads

class RedisTools:
    
    __redis_connect = redis.Redis(host=config["Redis"]["host"], port=config.get("Redis", "port"))

    @classmethod
    def set_request(cls,key: str, data: dict):
        cls.__redis_connect.set(key,dumps(data))
    
    @classmethod 
    def get_request(cls, key: str):
        data = cls.__redis_connect.get(key)
        return loads(data) if data else None
    
    @classmethod
    def add_city_to_list(cls,city_name:str):
        cls.__redis_connect.lpush("cities",city_name)
    
    @classmethod
    def get_city_list(cls):
        return cls.__redis_connect.lrange("cities",0,-1)