from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import UserImage


class PhotoSerializer(ModelSerializer):
    is_me = SerializerMethodField()

    class Meta:
        model = UserImage
        fields = ("url",)

    def get__is_me(self, context):
        request = self.context["request"]
        return request
