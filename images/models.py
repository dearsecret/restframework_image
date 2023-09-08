from django.db import models
from common.models import CommonModel
from django.utils.html import format_html

# Create your models here.


class UserImage(CommonModel):
    user = models.ForeignKey(
        "users.User", related_name="images", on_delete=models.CASCADE
    )
    url = models.URLField()
