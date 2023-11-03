from rest_framework.views import APIView
from .serializers import MeetingDetailSerializer, MeetingListSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.exceptions import NotFound, PermissionDenied
from .models import Meeting
from config.firebase import send_to_database


class Meetings(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        meetings = Meeting.objects.filter(invisible=False).order_by("-created")[:12]
        serializer = MeetingListSerializer(meetings, many=True)
        return Response(serializer.data)


class MeetingDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Meeting.objects.get(pk=pk)
        except Meeting.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        meeting = self.get_object(pk)
        serializer = MeetingDetailSerializer(meeting, context={"request": request})
        return Response(serializer.data)

    def post(self, request, pk):
        meeting = self.get_object(pk)
        if meeting.user != request.user:
            print("PLEASE MAKE MODEL")
            return Response()
        raise PermissionDenied

    def delete(self, request, pk):
        meeting = self.get_object(pk)
        if request.user == meeting.user:
            meeting.invisible = True
            meeting.save()
            send_to_database("meetings/remove", {"pk": meeting.pk})
            return Response(status=HTTP_200_OK)
        return Response(status=HTTP_400_BAD_REQUEST)


class MeetingPost(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = MeetingDetailSerializer(data=request.data)
        if serializer.is_valid():
            meeting = serializer.save(user=request.user)
            send_to_database("meetings/add", MeetingListSerializer(meeting).data)
            return Response(status=HTTP_200_OK)
        return Response(status=HTTP_400_BAD_REQUEST)
