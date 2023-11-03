from django.urls import path
from .views import MeetingPost, Meetings, MeetingDetail

# from .views import  MeetingList

urlpatterns = [
    path("init", MeetingPost.as_view()),
    path("list", Meetings.as_view()),
    path("<int:pk>", MeetingDetail.as_view()),
]
