from django.urls import path
from . import views

urlpatterns = [
    path("daily", views.TodayCards.as_view()),
    path("history", views.HistoryCards.as_view()),
]
