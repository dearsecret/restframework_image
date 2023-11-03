from rest_framework import serializers
from .models import Favorite
from chats.serializers import ChatListSerializer


class FavoriteSerializer(serializers.ModelSerializer):
    posts = ChatListSerializer(many=True, read_only=True)

    class Meta:
        model = Favorite
        fields = (
            "posts",
            "created",
        )
