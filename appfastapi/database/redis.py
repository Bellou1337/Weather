import redis
from appfastapi.config import config

rd = redis.Redis(host=config["Redis"]["host"], port=config.get("Redis", "port"))