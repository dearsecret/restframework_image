from .models import Meeting
from rest_framework import serializers
from users.serializers import PublicUserSerializer, GenderSerializer
from payments.serializers import PaymentSerializer


class MeetingOwnerSerializer(serializers.ModelSerializer):
    user = PublicUserSerializer(read_only=True)
    descriptions = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = Meeting
        fields = (
            "content",
            "descriptions",
            "created",
            "user",
        )
        lookup_field = ("photo",)
        extra_kwargs = {"url": {"lookup_field": "photo"}}


class MeetingDetailSerializer(serializers.ModelSerializer):
    user = PublicUserSerializer(read_only=True)
    joined = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Meeting
        fields = (
            "title",
            "photo",
            "joined",
            "content",
            "created",
            "user",
        )
        lookup_field = ("photo",)
        extra_kwargs = {"url": {"lookup_field": "photo"}}

    def get_joined(self, model):
        request = self.context["request"]
        if model.descriptions.filter(meeting=model, user=request.user).exists():
            return True
        else:
            return False


class MeetingListSerializer(serializers.ModelSerializer):
    user = PublicUserSerializer(read_only=True)

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
