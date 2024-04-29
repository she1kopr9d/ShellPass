from user.logic.shellcore import request as shellcore_request

def loginView(request):
    return shellcore_request("api/auth/login", request, "POST")

def registerView(request):
    return shellcore_request("api/auth/register", request, "POST")

def logoutView(request):
    return shellcore_request("api/auth/logout", request, "POST")

def refresh_token(request):
    return shellcore_request("api/auth/refresh-token", request, "POST")

def user(request):
    return shellcore_request("api/auth/user", request, "GET")