from rest_framework.serializers import ModelSerializer
from .models import UserImage
from users.serializers import PrivateUserSerializer


class MineSerializer(ModelSerializer):
    user = PrivateUserSerializer()

    class Meta:
        model = UserImage
        fields = (
            "user",
            "url",
        )
