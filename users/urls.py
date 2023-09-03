from django.urls import path
from . import views

urlpatterns = [
    path("register", views.RegisterUser.as_view()),
    path("jwt-login", views.JWTLogin.as_view()),
]
