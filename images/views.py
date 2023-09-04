import requests
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import UserImage
from config import settings
from .signature import make_signautre

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
            # 1 Private mode
            json={"requireSignedURLs": "true"},
        ).json()

        # requests 사용하여 파일 보내기
        # frontend에서 사용할 component test
        url = res.get("result").get("uploadURL")
        res = requests.post(
            url,
            files={
                "url": "https://www.mantech.co.kr/wp-content/uploads/2014/01/purple-bg.jpg"
                # "file": open("mine.jpeg", "rb")
            },
            # 2 Private mode
            data={
                "requireSignedURLs": "true",
            },
        ).json()
        url = res["result"].get("variants")[0]

        # make_signautre(url , minutes)
        served_private_url = make_signautre(url, 60)
        return Response({"result": f"{served_private_url}"})
