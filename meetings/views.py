from rest_framework.views import APIView

from payments.models import Payment
from .serializers import (
    MeetingDetailSerializer,
    MeetingListSerializer,
    MeetingOwnerSerializer,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.exceptions import NotFound, PermissionDenied
from .models import Meeting
from config.firebase import send_to_database
from django.db.transaction import atomic
from django.db.models import Q


class Meetings(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        meetings = Meeting.objects.filter(invisible=False).order_by("-created")[:12]
        serializer = MeetingListSerializer(
            meetings, many=True, context={"request": request}
        )
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
        if request.user == meeting.user:
            serializer = MeetingOwnerSerializer(meeting, context={"request": request})
            return Response(serializer.data)

        else:
            serializer = MeetingDetailSerializer(meeting, context={"request": request})
            return Response(serializer.data)

    def post(self, request, pk):
        meeting = self.get_object(pk)
        if (
            not meeting.descriptions.filter(user=request.user).exists()
            and meeting.user != request.user
        ):
            if meeting.user.friend.filter(pk=request.user.pk).exists():
                return Response({"status": "이미 지나친 상대"})
            else:
                try:
                    with atomic():
                        request.user.point -= 20
                        payment = Payment.objects.create(
                            meeting=meeting, user=request.user
                        )
                        meeting.descriptions.add(payment)
                        # meeting.descriptions.add(request.user)
                        request.user.save()
                        return Response({"joined": True})
                except Exception:
                    return Response()
        elif request.user == meeting.user:
            print("owner")
            return Response()
        raise PermissionDenied()

    def delete(self, request, pk):
        meeting = self.get_object(pk)
        if request.user == meeting.user:
            meeting.invisible = True
            meeting.save()
            send_to_database("meetings/remove", {"pk": meeting.pk})
            return Response(status=HTTP_200_OK)
        return Response(status=HTTP_400_BAD_REQUEST)


class MyMeeting(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        meetings = Meeting.objects.filter(user=request.user)
        serializer = MeetingListSerializer(
            meetings, many=True, context={"request": request}
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = MeetingDetailSerializer(data=request.data)
        print(request.data["photo"])
        if serializer.is_valid():
            meeting = serializer.save(user=request.user)
            send_to_database(
                "meetings/add",
                MeetingListSerializer(meeting, context={"request": request}).data,
            )
            return Response(status=HTTP_200_OK)
        return Response(status=HTTP_400_BAD_REQUEST)


class MeetingSerach(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        title = request.query_params.get("title", None)

        if len(title) > 1:
            meetings = Meeting.objects.filter(
                Q(title__contains=title) | Q(content__contains=title)
            )
            serializer = MeetingListSerializer(
                meetings, many=True, context={"request": request}
            )
            return Response(serializer.data)
        return Response()
