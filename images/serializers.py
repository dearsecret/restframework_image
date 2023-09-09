from rest_framework.serializers import ModelSerializer
from .models import UserImage
from users.serializers import PublicSerializer


class PhotoSerializer(ModelSerializer):
    # user = PublicSerializer(read_only=True)

    class Meta:
        model = UserImage
        fields = (
            "pk",
            "url",
        )
