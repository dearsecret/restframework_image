from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from common.models import CommonModel

# Create your models here.


class User(AbstractUser):
    class Discrimination(models.TextChoices):
        STUDENT = ("STUDENT", "student")
        TEACHER = ("TEACHER", "teacher")

    name = models.CharField(
        max_length=10, null=True, validators=[MinLengthValidator(3)]
    )
    first_name = models.CharField(editable=False, max_length=13)
    last_name = models.CharField(editable=False, max_length=13)
    discrimination = models.CharField(choices=Discrimination.choices, max_length=13)

    def __str__(self):
        return f"{self.name}"


class Profile(CommonModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=13, null=True)
    avatar = models.URLField()
    bio = models.TextField(max_length=2000)
