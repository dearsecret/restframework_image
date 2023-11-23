from rest_framework import serializers
from users.models import User
from .models import Card


class MiniProfileSerializer(serializers.ModelSerializer):
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "name",
            "thumbnail",
        )

    def get_thumbnail(self, obj):
        return obj.photos.get(index=0).url


class DailyCardSerializer(serializers.ModelSerializer):
    selected = MiniProfileSerializer(read_only=True)

    class Meta:
        model = Card
        fields = (
            "selected",
            "evaluate",
            "created",
        )

    # def get_thumbnail(self, obj):
    #   request = self.context["request"]
    #   if request.user == obj.user:
    #       return obj.selected.photos.get(index=0).url
    #   else :
    #       return obj.user.photos.get(index=0).url
    #

    # def get_photos(self, obj):
    #     url =model.selected.photos.get(index=0).url
    #     return make_signature(url, created.timestamp+ 60*60*24*7)


class ChosenCardSerializer(serializers.ModelSerializer):
    user = MiniProfileSerializer(read_only=True)

    class Meta:
        model = Card
        fields = (
            "user",
            "evaluate",
            "created",
        )

    # def get__score(self, obj):
    #     if obj.evaluated >= 3 & obj.evaluate >=3:
    #         return
    #     elif obj.evalutated >=3 :
    #         return
    #     elif obj.evaluate > 3:
    #         return
    #     return None

    # def get__target(self, obj):
    #     request = self.context["request"]
    #     if request.user:
    #         if obj.selected == request.user:
    #             return obj.user
    #         elif obj.user == request.user:
    #             #  obj.user == request.user
    #             return obj.selected
    #         else:
    #             return None
    #     else:
    #         return None
