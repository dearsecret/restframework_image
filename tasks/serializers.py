from rest_framework import serializers
from .models import VerifyNumber, Number
from .validators import validate_phone
from django.utils import timezone
import re


class NumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Number
        fields = ("number",)

    # def validate_to(self, value):
    #     num = VerifyNumber.objects.order_by("-time").filter(to=value)[0]
    #     if (
    #         num.time
    #         - timezone.localtime(timezone.now() - timezone.timedelta(minutes=3))
    #         < 0
    #     ):
    #         raise serializers.ValidationError("유효시간 초과")
    #     return value

    # def validate(self, data):
    #     data["to"]

    def validate_number(self, value):
        reg = re.compile(r"^(01[0|1|6|7|8|9])\d{7,8}$")
        if not reg.match(value):
            raise serializers.ValidationError("지원되지 않는 형식입니다.")
        return value
