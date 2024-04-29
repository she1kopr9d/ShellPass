import json
import socket
import requests

from core.data_utils import get_user
from core.settings import server_ips

from django.http import HttpRequest, HttpResponse

database_url_start = f"http://{server_ips["database_server"]["local"]["ip"]}:{server_ips["database_server"]["local"]["port"]}/"

def PostInDatabase(url, request: HttpRequest, body):
    header = {
        "Content-Type" : "application/json",
        "Authorization" : request.headers["Authorization"],
        "X-CSRFToken" : request.headers["X-CSRFToken"]
    }
    ip = socket.gethostbyname(server_ips["database_server"]["local"]["ip"])
    port = server_ips["database_server"]["local"]["port"]
    req = requests.post(url=f"http://{ip}:{port}/{url}", json=body, headers=header, cookies=request.COOKIES)
    return req

def DataBase_ModuleRequest(url: str, request: HttpRequest, user: dict):
    user = get_user(request)
    if user == None:
        return HttpResponse(content="error")
    data = json.loads(request.body.decode('utf-8'))
    req = PostInDatabase(url=url, body=data, request=request)
    return HttpResponse(content=req.text)