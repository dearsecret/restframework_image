from django.urls.conf import path
from . import views

urlpatterns = [
    path("post", views.WriteChat.as_view()),
    path("chat/<int:pk>", views.ChatDetail.as_view()),
    path("chat/<int:pk>/comment", views.WriteComment.as_view()),
    path("prefer/<int:pk>", views.Vote.as_view()),
    path("<int:start>", views.ChatList.as_view()),
    path("search", views.ChatSearch.as_view()),
]
