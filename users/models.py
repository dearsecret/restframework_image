from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from common.models import CommonModel
from uuid import uuid4

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
    first_name = models.CharField(editable=False, max_length=13)
    last_name = models.CharField(editable=False, max_length=13)
    discrimination = models.CharField(choices=Discrimination.choices, max_length=13)

    def __str__(self):
        return f"{self.username}"

    def point(self):
        return self.points.all().aggregate(total=Sum("usage"))["total"]


class Profile(CommonModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=13, null=True)
    avatar = models.URLField()
    bio = models.TextField(max_length=2000)


class Usage(models.Model):
    user = models.ForeignKey(User, related_name="points", on_delete=models.CASCADE)
    usage = models.IntegerField(default=10)
    timestamp = models.DateTimeField(auto_now_add=True)
