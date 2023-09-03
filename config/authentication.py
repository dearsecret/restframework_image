import jwt
from . import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from users.models import User


class JWTauthetication(BaseAuthentication):
    def authenticate(self, request):
        token = request.data.get("Jwt")

        if not token:
            return None
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        pk = decoded.get("pk")
        if not pk:
            raise AuthenticationFailed("No Permission")
        try:
            user = User.objects.get(pk=pk)
            return (user, None)
        except User.DoesNotExist:
            raise AuthenticationFailed("Not found")
