import jwt
from config import settings
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from .models import User
from .serializers import VerifySerializer
from tasks.models import Number, VerifyNumber
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

# from tasks.models import VerifyNumber

# Create your views here.


class Test(APIView):
    def post(self, request):
        username = request.data["username"]
        password = request.data["password"]
        number = request.data["number"]
        if not username or not password or not number:
            raise ParseError({"error": "올바르지 못한 입력값입니다."})
        serializer = VerifySerializer(data=request.data)
        if serializer.is_valid():
            # get_or_create 는 1개만 반영해야함.
            # number, created = Number.objects.get_or_create(number=number)
            number = Number.objects.filter(number=number)[0]
            VerifyNumber.objects.create(number=number)
            return Response({"success": "인증번호가 발송되었습니다."})
        return Response({"error": "validation"})


class RegisterUser(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        number = request.data.get("number")

        if not username or not password:
            raise ParseError()
        if User.objects.get(username=username):
            raise ParseError()
        if User.objects.get(number=number):
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
            return Response({"token": token}, status=HTTP_200_OK)
        else:
            return Response({"error": "check password"}, status=HTTP_400_BAD_REQUEST)
