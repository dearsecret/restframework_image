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

    def post(self, request):
        try:
            cnt = request.data.get("cnt")
            assert type(cnt) is int, "type validate"
        except Exception as e:
            raise ParseError({"error": "올바르지 않은 입력값"})

        if cnt > 0:
            url_links = get_links(cnt)
            return Response({"uploadUrl": url_links}, status=HTTP_200_OK)
        else:
            return Response({"error": "type error"}, status=HTTP_400_BAD_REQUEST)

    def put(self, request):
        data = request.data.get("data")
        if not data:
            raise ParseError()

        try:
            with atomic():
                for key in data:
                    if not str(data[key]).startswith(
                        "https://imagedelivery.net/J9h5bfi5i6mCYIcaebsRcw/"
                    ):
                        raise ParseError()

                    UserImage.objects.create(
                        index=key, url=data[key], user=request.user
                    )
            return Response({"success": "confirm frontend"})
        except Exception as e:
            return Response({"error": "needs to confirm your data"})
