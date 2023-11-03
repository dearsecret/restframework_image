from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError, NotFound
from rest_framework.response import Response
from .serializers import (
    ChatSerializer,
    ChatListSerializer,
    PostChatSerializer,
    CommentSerializer,
)
from .models import Chat
from config.firebase import send_to_database
from django.db.models import Q
from rest_framework.status import HTTP_208_ALREADY_REPORTED

# Create your views here.


class WriteChat(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PostChatSerializer(data=request.data)
        if serializer.is_valid():
            chat = serializer.save(writer=request.user)
            send_to_database("posts/add", ChatListSerializer(chat).data)
            return Response({"status": "ok"})
        raise ParseError()


class WriteComment(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Chat.objects.get(pk=pk)
        except Chat.DoesNotExist:
            raise NotFound

    def post(self, request, pk):
        chat = self.get_object(pk)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            comment = serializer.save(comment_post=chat, author=request.user)
            # TODO: send_to_database
            return Response(
                CommentSerializer(comment, context={"request": request}).data
            )
        return Response()


class ChatDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Chat.objects.get(pk=pk)
        except Chat.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        chat = self.get_object(pk)
        serializer = ChatSerializer(
            chat,
            context={"request": request},
        )
        return Response(serializer.data)


class ChatSearch(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        page_size = 10
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1

        start = page * page_size
        # start = (page - 1) * page_size
        end = start + page_size
        serailizer = ChatListSerializer(
            Chat.objects.order_by("-created_at").all()[start:end], many=True
        )
        return Response(serailizer.data)


class ChatList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, start):
        if not start:
            start = 0
        size = 10
        end = start + size
        serailizer = ChatListSerializer(
            Chat.objects.order_by("-created_at").all()[start:end], many=True
        )
        return Response(serailizer.data)


class Vote(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Chat.objects.get(pk=pk)
        except Chat.DoesNotExist:
            raise NotFound

    def post(self, request, pk):
        chat = self.get_object(pk)
        vote = request.data.get("vote")
        if not (
            chat.likes.filter(pk=request.user.pk)
            or chat.dislikes.filter(pk=request.user.pk)
        ):
            if vote:
                chat.likes.add(request.user.pk)
            else:
                chat.dislikes.add(request.user.pk)
            return Response(
                {
                    "prefer": bool(vote),
                    "count_likes": chat.likes.count(),
                    "count_dislikes": chat.dislikes.count(),
                }
            )
        return Response({}, status=HTTP_208_ALREADY_REPORTED)
