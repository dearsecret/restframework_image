from django.urls import path
from . import views

urlpatterns = [
    path("upload", views.ImageUpload.as_view()),
]
# path("test", views.ImageTest.as_view()),
