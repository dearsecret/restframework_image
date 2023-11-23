from rest_framework import serializers
from .models import Payment
from users.serializers import GenderSerializer


class PaymentSerializer(serializers.ModelSerializer):
    user = GenderSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = (
            "pk",
            "user",
            "created",
        )
