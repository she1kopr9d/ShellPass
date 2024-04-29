from django.urls import path
from user.views import loginView, registerView, CookieTokenRefreshView, logoutView, user, check

app_name = "user"

urlpatterns = [
    path('login', loginView),
    path('register', registerView),
    path('refresh-token', CookieTokenRefreshView.as_view()),
    path('logout', logoutView),
    path("user", user),
    path("check", check)
]
