from rest_framework.serializers import ModelSerializer
from .models import User


class PrivateUserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = [
            "first_name",
            "last_name",
            "is_superuser",
            "is_staff",
            "groups",
            "user_permissions",
        ]
