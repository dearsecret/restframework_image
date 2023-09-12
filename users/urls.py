from django.urls import path
from . import views

urlpatterns = [
    path("register", views.RegisterUser.as_view()),
    path("jwt-login", views.JWTLogin.as_view()),
    path("test", views.Test.as_view()),
    path("profile", views.Profile.as_view()),
    path("detail", views.Thumbnail.as_view()),
]
