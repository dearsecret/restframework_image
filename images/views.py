import requests
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, NotAuthenticated
from .models import UserImage
from config import settings
from .signature import make_signature
from .serializers import PhotoSerializer

# Create your views here.


class ImageUpload(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # upload image link 생성
        url = f"https://api.cloudflare.com/client/v4/accounts/{settings.CF_ID}/images/v1/direct_upload"
        res = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {settings.CF_TOKEN}",
                "Content-Type": "application/json",
            },
            # 1 Private mode
            json={"requireSignedURLs": "true"},
        )
        if res.status_code == 200:
            url = res.json().get("result").get("uploadURL")
            return Response({"uploadUrl": f"{url}"})
        else:
            return Response({"error": "잠시 후 다시 시도해주세요"})

    def put(self, request):
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            # photo = serializer.save()
            photo = serializer.save(user=request.user)
            serializer = PhotoSerializer(photo)
            return Response(serializer.data)
        return Response({"error": "잠시 후 다시 시도해주세요."})

        # http.post().then(res => {
        # http.post(res.uploadUrl, headers: {"content":"multipart/form-data", body: ~~~})})


class ImageTest(APIView):
    def post(self, request):
        # upload image link 생성
        url = f"https://api.cloudflare.com/client/v4/accounts/{settings.CF_ID}/images/v1/direct_upload"
        res = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {settings.CF_TOKEN}",
                "Content-Type": "application/json",
            },
            # 1 Private mode
            json={"requireSignedURLs": "true"},
        )
        if res.status_code == 200:
            url = res.json().get("result").get("uploadURL")
        print(url)

        res = requests.post(
            url,
            files={
                "url": "https://th-thumbnailer.cdn-si-edu.com/5V-xOO-B6H14VTVruDbqnMvmmE0=/fit-in/1072x0/filters:focal(342x433:343x434)/https://tf-cmsv2-smithsonianmag-media.s3.amazonaws.com/filer/e4/af/e4afdbe6-59c0-4a6b-8112-8b30e274d9a0/2009-49519-h-floresiensis-jgurche_web.jpg"
                # "file": open("mine.jpeg", "rb")
            },
            # 2 Private mode
            data={
                "requireSignedURLs": "true",
            },
        ).json()
        url = res["result"].get("variants")
        print(url)
        try:
            from .models import UserImage

            UserImage.objects.create(url=url[0], user=request.user)
            UserImage.objects.create(url=url[1], user=request.user)
            return Response({"success": "good"})
        except Exception as e:
            return Response({"error": "잠시 후 다시 시도해주세요."})
