from django.urls import path
from .views import FavoriteList, ToggleFavorite

urlpatterns = [
    path("me", FavoriteList.as_view()),
    path("<int:pk>", ToggleFavorite.as_view()),
]
