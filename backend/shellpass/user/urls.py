from django.urls import path
from user.views import loginView, registerView, refresh_token, logoutView, user

app_name = "user"

urlpatterns = [
    path('login', loginView),
    path('register', registerView),
    path('refresh-token', refresh_token),
    path('logout', logoutView),
    path("user", user),
]
