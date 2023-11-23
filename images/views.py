from django.db.transaction import atomic
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.exceptions import ParseError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .upload import get_links
from .models import UserImage


class ImageUpload(APIView):
    permission_classes = [IsAuthenticated]

    def get_count(self ,cnt):
        try :
            return int(cnt)
        except ValueError:
            raise ParseError

    def get(self ,request, cnt):
        cnt = self.get_count(cnt)
        print(cnt)
        if cnt <=6 and cnt>0:
            links = get_links(cnt)
            print(links)
            return Response({"uploadUrl": links})
        return Response()

    def post(self, request):
        print(request.user)
        print(request.data)
        return Response({"fucker": "success"})

    # def put(self, request):
    #     data = request.data.get("data")
    #     if not data:
    #         raise ParseError()
    #     try:
    #         with atomic():
    #             for key in data:
    #                 if not str(data[key]).startswith(
    #                     "https://imagedelivery.net/J9h5bfi5i6mCYIcaebsRcw/"
    #                 ):
    #                     raise ParseError()

    #                 UserImage.objects.create(
    #                     index=key, url=data[key], user=request.user
    #                 )
    #         return Response({"success": "confirm frontend"})
    #     except Exception as e:
    #         return Response({"error": "needs to confirm your data"})
