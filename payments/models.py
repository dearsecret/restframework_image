from django.db import models

# Create your models here.


class Payment(models.Model):
    meeting = models.ForeignKey(
        "meetings.Meeting",
        related_name="payments",
        on_delete=models.SET_NULL,
        null=True,
    )
    user = models.ForeignKey(
        "users.User",
        related_name="paid",
        on_delete=models.SET_NULL,
        null=True,
    )
    created = models.DateTimeField(auto_now_add=True)
