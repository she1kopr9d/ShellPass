import redis
from core.settings import REDIS_HOST, REDIS_PORT

redis_instance = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0)