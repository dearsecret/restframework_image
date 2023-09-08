import re
from rest_framework import serializers
from .models import User


class VerifySerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    number = serializers.CharField()

    def validate_number(self, value):
        reg = re.compile(r"^(01[0|1|6|7|8|9])\d{7,8}$")
        if not reg.match(value):
            raise serializers.ValidationError("지원되지 않는 형식입니다. 전화번호를 확인해주세요.")
        return value

    def validate_password(self, value):
        reg = re.compile(
            r"(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[^A-Za-z0-9])(?=.{8,})"
        )
        if not reg.match(value):
            raise serializers.ValidationError("지원되지 않는 형식입니다.")
        return value

    def validate_username(self, value):
        reg = re.compile(
            r"^[a-zA-Z0-9.a-zA-Z0-9.!#$%&'*+-/=?^_`{|}~]+@[a-zA-Z0-9]+\.[a-zA-Z]+"
        )
        if not reg.match(value):
            raise serializers.ValidationError("지원되지 않는 형식입니다.")
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("이미 존재하는 아이디 입니다.")
        return value
