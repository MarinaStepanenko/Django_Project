from django.contrib.auth.views import LoginView
from django.urls import path

from users.urls import app_name
from users.apps import UsersConfig

app_name = "users"

urlpatterns = [
    path("login", LoginView.as_view(), template_name="login.html"),
]
