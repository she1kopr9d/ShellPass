import core.settings as settings
from user.models import User
import pickle
import socket
import redis
from core.settings import REDIS_HOST, REDIS_PORT

def get_user(user_id: int) -> User:
    ip = socket.gethostbyname(REDIS_HOST)
    cache = redis.StrictRedis(host=ip, port=REDIS_PORT, db=0)
    data = cache.get(user_id)
    if data != None:
        return pickle.loads(data)
    try:
        user = User.objects.get(id=user_id)
        cache.set(user_id, pickle.dumps(user))
        return user
    except User.DoesNotExist:
        raise User.DoesNotExist()
    