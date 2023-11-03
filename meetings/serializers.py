from .models import Meeting
from rest_framework import serializers
from users.models import User
from users.serializers import GenderSerializer, PublicUserSerializer


class MeetingDetailSerializer(serializers.ModelSerializer):
    user = PublicUserSerializer(read_only=True)
    descriptions = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Meeting
        fields = (
            "photo",
            "title",
            "content",
            "descriptions",
            "created",
            "user",
        )
        lookup_field = ("photo",)
        extra_kwargs = {"url": {"lookup_field": "photo"}}

    def get_descriptions(self, model):
        request = self.context["request"]
        if request and model.user == request.user:
            return PublicUserSerializer(
                model.descriptions.all(), many=True, context={"request": request}
            ).data
        else:
            return None


class MeetingListSerializer(serializers.ModelSerializer):
    user = GenderSerializer(read_only=True)

    class Meta:
        model = Meeting
        fields = (
            "pk",
            "photo",
            "title",
            "created",
            "user",
        )
        lookup_field = ("photo",)
        extra_kwargs = {"url": {"lookup_field": "photo"}}
