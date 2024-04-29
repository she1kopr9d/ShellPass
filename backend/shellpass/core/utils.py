import json
import socket
import requests

from core.settings import server_ips
from core.exception import CoreUserIsNull, UncorrentType, UncorrectMethod
from core.data_utils import get_user, AuthorizeRequest

from django.http import HttpRequest, HttpResponse

#input -> request: HttpRequest, user: dict, req: Response
def AuthorizePreRequest(
    url: str,
    type: str = "domen",
    method : str = "GET"):

    def wrap(
        function):
        @AuthorizeRequest()
        def called(
            *args,
            **kwargs):
            request : HttpRequest = args[0]
            data = json.loads(
                request.body.decode(
                    'utf-8'
                )
            )
            header = {
                "Content-Type" : "application/json",
                "Authorization" : request.headers["Authorization"],
                "X-CSRFToken" : request.headers["X-CSRFToken"]
            }
            if type == "domen":
                path = url
                domen = path.split(":")[1].replace("//", "")
                ip = socket.gethostbyname(domen)
                path = path.replace(domen, ip)
            elif type == "ip":
                pass
            else:
                raise UncorrentType()
            if method == "GET":
                req = requests.get(
                    url = path,
                    json = data,
                    headers = header,
                    cookies = request.COOKIES
                )
            elif method == "POST":
                req = requests.post(
                    url = path,
                    json = data,
                    headers = header,
                    cookies = request.COOKIES
                )
            else:
                raise UncorrectMethod()
            return function(
                *args,
                req,
                **kwargs
            )
        return called
    return wrap

def AuthorizePermissionRequest(
    signature: str = "0:0:0:0"):
    
    def wrap(function):

        @AuthorizeRequest()
        def called(
            *args,
            **kwargs):

            request : HttpRequest = args[0]
            data = json.loads(
                request.body.decode(
                    'utf-8'
                )
            )
            data.update(
                {
                    "signature" : signature
                }
            )
            header = {
                "Content-Type" : "application/json",
                "Authorization" : request.headers["Authorization"],
                "X-CSRFToken" : request.headers["X-CSRFToken"]
            }

            ip = socket.gethostbyname(
                server_ips["database_server"]["local"]["ip"]
            )
            req = requests.get(
                url = f"http://{ip}:{server_ips["database_server"]["local"]["port"]}/database/user/permission/check",
                json = data,
                headers = header,
                cookies = request.COOKIES
            )
            
            answer = json.loads(
                req.text
            )
            try:
                if answer["can"] == True:
                    return function(
                        *args,
                        **kwargs
                    )
                else:
                    return HttpResponse(
                        content = "You don't have permission"
                    )
            except:
                raise CoreUserIsNull
        return called
    return wrap

def AuthorizeRedirect(
    url: str,
    type: str = "domen",
    method : str = "GET"):
    def wrap(function):
        @AuthorizeRequest()
        def called(
            *args,
            **kwargs):
            request : HttpRequest = args[0]
            data = json.loads(
                request.body.decode(
                    'utf-8'
                )
            )
            header = {
                "Content-Type" : "application/json",
                "Authorization" : request.headers["Authorization"],
                "X-CSRFToken" : request.headers["X-CSRFToken"]
            }
            if type == "domen":
                path = url
                domen = path.split(":")[1].replace("//", "")
                ip = socket.gethostbyname(
                    domen
                )
                path = path.replace(
                    old = domen,
                    new = ip
                )
            elif type == "ip":
                pass
            else:
                raise UncorrentType()
            if method == "GET":
                req = requests.get(
                    url = path,
                    json = data,
                    headers = header,
                    cookies = request.COOKIES
                )
            elif method == "POST":
                req = requests.post(
                    url = path,
                    json = data,
                    headers = header,
                    cookies = request.COOKIES
                )
            else:
                raise UncorrectMethod()
            return HttpResponse(
                content = req.text
            )
        return called
    return wrap

def get_req_args(
    *args, 
    request: HttpRequest):
    data = json.loads(
        request.body.decode(
            'utf-8'
        )
    )
    vars = []
    for arg in args:
        vars.append(
            data[arg]
        )
    if len(vars) > 1:
        return tuple(vars)
    return vars[0]