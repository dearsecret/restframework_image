from django.urls import path
from . import views

urlpatterns = [path("me", views.Mine.as_view())]
