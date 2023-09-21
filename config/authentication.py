import jwt
from . import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from users.models import User

# import firebase_admin
# from firebase_admin import auth as firebase_auth
# from firebase_admin import credentials
# from firebase_admin.exceptions import FirebaseError


class JWTauthetication(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get("Authorization")
        if not token:
            return None
        try:
            decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            pk = decoded.get("pk")
            if not pk:
                raise AuthenticationFailed("No Permission")
            try:
                user = User.objects.get(pk=pk)
                return (user, None)
            except User.DoesNotExist:
                raise AuthenticationFailed("Not found")
        except Exception as e:
            raise AuthenticationFailed("not found pk")


# if not firebase_admin._apps:
#     cred = credentials.Certificate("./firebase.json")
#     default_app = firebase_admin.initialize_app(cred)


# class FirebaseAuthentication(BaseAuthentication):
#     def authenticate(self, request):
#         auth_header = request.META.get("HTTP_AUTHORIZATION")
#         if not auth_header:
#             raise AuthenticationFailed("No auth token provided")

#         id_token = auth_header.split(" ").pop()
#         decoded_token = None
#         try:
#             decoded_token = firebase_auth.verify_id_token(id_token)
#         except Exception:
#             raise AuthenticationFailed("Invalid auth token")

#         if not id_token or not decoded_token:
#             return None

#         try:
#             uid = decoded_token.get("uid")
#         except Exception:
#             raise FirebaseError()

#         user, created = User.objects.get_or_create(username=uid)
#         return (user, None)
