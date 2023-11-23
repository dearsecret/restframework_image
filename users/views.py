import jwt
from config import settings
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import User, Profile
from .serializers import (
    VerifySerializer,
    PublicSerializer,
    PrivateSerializer,
    MeSerializer,
    PrivateProfileSerializer,
    ProfileDetailSerializer,
)
from tasks.models import Number, VerifyNumber
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from config.firebase import make_custom_token
import datetime

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
        user = authenticate(request, username=username, password=password)
        if user:
            token = jwt.encode(
                {"pk": f"{user.pk}"}, settings.SECRET_KEY, algorithm="HS256"
            )
            return Response(
                {"token": token, "fire_token": make_custom_token(str(user.pk))},
                status=HTTP_200_OK,
            )
        else:
            return Response({"error": "check password"}, status=HTTP_400_BAD_REQUEST)

    # def put(self, request):
    #     username = request.data.get("username")
    #     password = request.data.get("password")

    #     user, created = User.objects.get_or_create(username=username)
    #     print(user)
    #     if not created:
    #         user.set_password(password)
    #         user.save()
    #         token = jwt.encode(
    #             {"pk": f"{user.pk}"}, settings.SECRET_KEY, algorithm="HS256"
    #         )
    #         return Response({"token": token}, status=HTTP_200_OK)
    #     else:
    #         raise AuthenticationFailed()


# class Profile(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         try:
#             serializer = PublicSerializer(request.user)
#             return Response(serializer.data)
#         except Exception as e:
#             return Response("fail!", status=HTTP_400_BAD_REQUEST)


class PrivateProfile(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PrivateSerializer(request.user)
        return Response(serializer.data, status=HTTP_200_OK)


class Me(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = MeSerializer(request.user)
        return Response(serializer.data)

    # now = timezone.localtime(timezone.now())
    #     if now.hour >= 12:
    #         noon = now.replace(hour=12, minute=0, second=0, microsecond=0)
    #         # today_list= something.objects.filter(created_at__gte= noon).all()
    #         # serializer
    #         return Response()
    #     else:
    #         yesterday = timezone.localtime(
    #             timezone.now() - timezone.timedelta(days=1)
    #         ).replace(hour=12, minute=0, second=0, microsecond=0)
    #         # today_list= somthing.objects.filter(created_at__gte=yesterday).all()
    #         # serializer
    #         return Response()

    # def post(self ,request)


from .serializers import PrivateDetailSerializer


class ProfileList(APIView):
    def get(self, request):
        obj = {}
        obj["school"] = Profile.School.labels
        obj["weight"] = Profile.Weight.labels
        obj["drive"] = Profile.Drive.labels
        obj["policy"] = Profile.Policy.labels
        obj["religion"] = Profile.Religion.labels
        obj["drink"] = Profile.Drink.labels
        obj["smoke"] = Profile.Smoke.labels
        return Response(obj)


    def post(self, request):
        profile = Profile.objects.get(user=request.user)
        serializer = PrivateProfileSerializer(
            profile,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            profile = serializer.save(user=request.user)
            serializer = PrivateProfileSerializer(profile)
            print(serializer.data)
            return Response(serializer.data)
        return Response(status=HTTP_400_BAD_REQUEST)
