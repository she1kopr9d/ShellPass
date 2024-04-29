import socket
import json
import requests
from django.http import HttpRequest, HttpResponse

def shellcore_request(url: str, request: HttpRequest, method: str = "GET"):
    ip = socket.gethostbyname("shellcore")
    headers = request.headers
    body = {}
    if request.body != b"":
        body = json.loads(request.body.decode('utf-8'))
    try:
        headers["Content-Type"] = "application/json"
    except:
        pass

    if method == "POST":
        func = requests.post
    elif method == "GET":
        func = requests.get
    data = func(f"http://{ip}:8000/{url}", data=json.dumps(body), cookies=request.COOKIES, headers=headers)
    return data

def shellcore_auto(url: str, request: HttpRequest, method: str = "GET"):
    data = shellcore_request(url, request, method)
    return HttpResponse(content=data.text, headers=data.headers)