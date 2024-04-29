import core.settings as settings
#from user.models import User
import pickle
import socket
import json
import requests
import redis

from django.http import HttpRequest, HttpResponse
from core.settings import REDIS_HOST, REDIS_PORT
from core.auth_api import shellcore_request
from core.exception import CoreUserIsNull

def get_user(request: HttpRequest):
    try:
        data = json.loads(shellcore_request("api/auth/user", request, "GET").text)
        data["id"]
        return data
    except:
        raise CoreUserIsNull()
    
def AuthorizeRequest():
    def wrap(function):
        def called(*args, **kwargs):
            request = args[0]
            try:
                user = get_user(request=request)
                return function(*args, user, **kwargs)
            except CoreUserIsNull:
                return HttpResponse(content="Token is not valid")
        return called
    return wrap
    # ip = socket.gethostbyname(REDIS_HOST)
    # cache = redis.StrictRedis(host=ip, port=REDIS_PORT, db=0)
    
    # print("get user data")
    # data = cache.get(user_id)
    # if data != None:
    #     return pickle.loads(data)
    # try:
    #     #user = User.objects.get(id=user_id)
    #     cache.set(user_id, pickle.dumps(user))
    #     return get_user(user_id)
    # except User.DoesNotExist:
    #     raise User.DoesNotExist()
    