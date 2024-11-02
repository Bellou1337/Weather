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
        
        