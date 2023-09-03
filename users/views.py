import jwt
from config import settings
from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from .serializers import PrivateUserSerializer
from .models import User

# Create your views here.


class RegisterUser(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("passwrod")

        if not username or not password:
            raise ParseError()
        if User.objects.get(username=username):
            raise ParseError()

        user = User.objects.create(username=username)
        user.set_password(password)
        return Response({"ok": "success"})

        # serializer = PrivateUserSerializer(data=)


class JWTLogin(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            raise ParseError

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user:
            token = jwt.encode({"pk": user.pk}, settings.SECRET_KEY, algorithm="HS256")
            return Response({"token": token})
        else:
            return Response({"error": "check password"})
