from django.db import models
from common.models import CommonModel
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class UserImage(CommonModel):
    user = models.ForeignKey(
        "users.User", related_name="photos", on_delete=models.CASCADE, null=True
    )
    index = models.IntegerField(
        null=True, validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    status = models.BooleanField(default=False)
    url = models.URLField()
