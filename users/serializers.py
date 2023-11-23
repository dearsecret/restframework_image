import re
from rest_framework import serializers
from images.signature import make_signature
from .models import User, Profile


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


class PublicSerializer(serializers.ModelSerializer):
    point = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            "pk",
            "name",
            "point",
        )

    def get_point(self, obj):
        return obj.point()


class PrivateSerializer(serializers.ModelSerializer):
    photos = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "username",
            "photos",
        )

    def get_photos(self, user):
        return [
            make_signature(photo.url, 60 * 60 * 24 * 7)
            for photo in user.photos.filter(status=True)
        ]


# TODO : SHOULD MAKE AGE SWITCH FUNCTION
class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "gender",
            "name",
            "location",
            "age",
        )


class PublicUserSerializer(serializers.ModelSerializer):
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = User

        fields = (
            "is_owner",
            "gender",
        )

    def get_is_owner(self, model):
        request = self.context["request"]
        if request and (request.user == model):
            return True
        else:
            return False


class MeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "point",
            "name",
        )


from images.models import UserImage


class UserPhotosSerializer(serializers.ModelSerializer):
    signature_url = serializers.SerializerMethodField()

    class Meta:
        model = UserImage
        fields = (
            "url",
            "signature_url",
        )

    def get_signature_url(self, obj):
        if self.parent.context["request"].user == obj.user:
            time = obj.user.last_login.timestamp()
            return make_signature(obj.url, time + 60 * 60 * 24 * 365)
        # time = obj.PARENT_FIELD.created
        # return make_signature(obj.url, time + 60 * 60 * 24 * 7)
        return None


class PrivateProfileSerializer(serializers.ModelSerializer):
    policy = serializers.ChoiceField(
        choices=Profile.Policy.choices,
        source="get_policy_display",
    )
    religion = serializers.ChoiceField(
        choices=Profile.Religion.choices,
        source="get_religion_display",
    )
    smoke = serializers.ChoiceField(
        choices=Profile.Smoke.choices,
        source="get_smoke_display",
    )
    drink = serializers.ChoiceField(
        choices=Profile.Drink.choices,
        source="get_drink_display",
    )
    school = serializers.ChoiceField(
        choices=Profile.School.choices,
        source="get_school_display",
    )
    drive = serializers.ChoiceField(
        choices=Profile.Drive.choices,
        source="get_drive_display",
    )
    weight = serializers.ChoiceField(
        choices=Profile.Weight.choices,
        source="get_weight_display",
    )

    class Meta:
        model = Profile
        fields = (
            "height",
            "job",
            "policy",
            "religion",
            "smoke",
            "drink",
            "school",
            "drive",
            "weight",
            "prefer",
            "deny",
            "dating",
            "hobby",
            "more",
        )

    def to_internal_value(self, data):
        for key in data:
            if key in self.fields:
                field = Profile._meta.get_field(key)
                if field.choices and data[key] < len(field.choices):
                    pass
            else:
                raise serializers.ValidationError()

        return data


class ProfileDetailSerializer(serializers.ModelSerializer):
    policy = serializers.ChoiceField(choices=Profile.Policy.choices)
    religion = serializers.ChoiceField(Profile.Religion.choices)
    smoke = serializers.ChoiceField(choices=Profile.Smoke.choices)
    drink = serializers.ChoiceField(choices=Profile.Drink.choices)
    school = serializers.ChoiceField(choices=Profile.School.choices)
    drive = serializers.ChoiceField(choices=Profile.Drive.choices)
    weight = serializers.ChoiceField(choices=Profile.Weight.choices)

    class Meta:
        model = Profile
        fields = (
            "height",
            "job",
            "policy",
            "religion",
            "smoke",
            "drink",
            "school",
            "drive",
            "weight",
            "prefer",
            "deny",
            "dating",
            "hobby",
            "more",
        )


class PrivateDetailSerializer(serializers.ModelSerializer):
    profiles = PrivateProfileSerializer(read_only=True)
    photos = UserPhotosSerializer(read_only=True, many=True)
    # is_me = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            "name",
            "profiles",
            "photos",
            # "is_me",
        )

    # def get_is_me(self, obj):
    #     request = self.context.get("request")
    #     return request.user == obj
