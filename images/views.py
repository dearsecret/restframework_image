import requests
from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import MineSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from users.serializers import PrivateUserSerializer
from .models import UserImage
from config import settings

# Create your views here.


class Mine(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not UserImage.objects.filter(user=request.user).exists():
            raise NotFound()
        return Response()

    def post(self, request):
        # upload image link 생성하기
        url = f"https://api.cloudflare.com/client/v4/accounts/{settings.CF_ID}/images/v1/direct_upload"
        res = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {settings.CF_TOKEN}",
                "Content-Type": "application/json",
            },
        ).json()

        return Response({"result": f"{res}"})
