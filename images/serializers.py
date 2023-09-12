from rest_framework.serializers import ModelSerializer
from .models import UserImage


class PhotoSerializer(ModelSerializer):
    class Meta:
        model = UserImage
        fields = ("url",)
