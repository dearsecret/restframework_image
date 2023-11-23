from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from common.models import CommonModel
from uuid import uuid4
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class User(AbstractUser):
    id = models.UUIDField(
        primary_key=True, default=uuid4, editable=False, max_length=150
    )

    class Discrimination(models.TextChoices):
        STUDENT = ("female", "여성")
        TEACHER = ("male", "남성")

    name = models.CharField(
        max_length=10, null=True, validators=[MinLengthValidator(3)]
    )
    point = models.PositiveIntegerField(default=20)
    gender = models.BooleanField(default=False)
    location = models.CharField(max_length=120, null=True)
    age = models.DateField(null=True)
    first_name = models.CharField(editable=False, max_length=13)
    last_name = models.CharField(editable=False, max_length=13)
    discrimination = models.CharField(choices=Discrimination.choices, max_length=13)
    friend = models.ManyToManyField("self", related_name="friends", symmetrical=False)

    def __str__(self):
        return f"{self.pk}"


class Profile(CommonModel):
    # TODO: 지역 / 나이  따로 빼놓을것
    class Policy(models.IntegerChoices):
        none = (0, "무관심")
        progressive = (1, "진보")
        conservative = (2, "보수")

    class Religion(models.IntegerChoices):
        none = (0, "무관심")
        buddhism = (1, "불교")
        catholicism = (2, "천주교")
        christian = (3, "기독교")
        etc = (4, "기타")

    class Smoke(models.IntegerChoices):
        none = (0, "-")
        quit = (1, "금연")
        electronic = (2, "전자담배")
        tabacco = (3, "담배")

    class Drink(models.IntegerChoices):
        none = (0, "안마셔요")
        often = (1, "아주 가끔")
        usually = (2, "가끔")
        always = (3, "자주")

    class School(models.IntegerChoices):
        none = (0, "고등학교 졸업")
        college = (1, "전문대 졸업")
        university = (2, "대학교 졸업")
        graduate = (3, "대학원 졸업")

    class Drive(models.IntegerChoices):
        none = (0, "면허 없음")
        possible = (1, "면허 있음")
        own = (2, "차량 보유")

    class Weight(models.IntegerChoices):
        none = (0, "마른")
        slim = (1, "슬림한")
        normal = (2, "보통")
        fit = (3, "탄탄한")
        chubby = (4, "통통한")
        fat = (5, "뚱뚱한")

    phone_number = models.CharField(max_length=13, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profiles")
    height = models.IntegerField(
        validators=[MinValueValidator(145), MaxValueValidator(210)], null=True
    )
    job = models.CharField(max_length=12, null=True)
    policy = models.IntegerField(choices=Policy.choices, null=True)
    religion = models.IntegerField(choices=Religion.choices, null=True)
    smoke = models.IntegerField(choices=Smoke.choices, null=True)
    drink = models.IntegerField(choices=Drink.choices, null=True)
    school = models.IntegerField(choices=School.choices, null=True)
    drive = models.IntegerField(choices=Drive.choices, null=True)
    weight = models.IntegerField(choices=Weight.choices, null=True)

    prefer = models.TextField(max_length=1000, null=True, blank=True)
    deny = models.TextField(max_length=1000, null=True, blank=True)
    dating = models.TextField(max_length=1000, null=True, blank=True)
    hobby = models.TextField(max_length=1000, null=True, blank=True)
    more = models.TextField(max_length=1000, null=True, blank=True)
    # ideal = models.TextField(max_length=1000, null=True)
    # mbti = models.TextField(max_length=4)
    #  = models.TextField(max_length=4)


class Usage(models.Model):
    user = models.ForeignKey(User, related_name="points", on_delete=models.CASCADE)
    usage = models.IntegerField(default=10)
    timestamp = models.DateTimeField(auto_now_add=True)


# class Bio(models.Model):
#         # specialty , hobby,
#     # dating
#     # bio = models.TextField(max_length=2000)
#     updated = models.DateTimeField(auto_now=True)
