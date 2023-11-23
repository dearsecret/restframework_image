from django.urls import path
from .views import MyMeeting, Meetings, MeetingDetail, MeetingSerach

# from .views import  MeetingList

urlpatterns = [
    path("me", MyMeeting.as_view()),
    path("list", Meetings.as_view()),
    path("<int:pk>", MeetingDetail.as_view()),
    path("search", MeetingSerach.as_view()),
]
