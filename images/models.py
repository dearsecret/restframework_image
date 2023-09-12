from django.db import models
from common.models import CommonModel
from django.utils.html import format_html

# Create your models here.


class UserImage(CommonModel):
    # TEST 용 null =True
    user = models.ForeignKey(
        "users.User", related_name="photos", on_delete=models.CASCADE, null=True
    )
    url = models.URLField()
