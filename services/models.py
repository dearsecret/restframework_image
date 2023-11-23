from django.db import models
from django.core.validators import MaxValueValidator
from django.utils import timezone


class Card(models.Model):
    selected = models.ForeignKey(
        "users.User", related_name="chosen", on_delete=models.CASCADE, null=True
    )
    user = models.ForeignKey(
        "users.User", related_name="chose", on_delete=models.CASCADE, null=True
    )
    evaluate = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(5)],
        null=True,
        blank=True,
    )
    updated = models.DateTimeField(auto_now=True)
    # TODO : must change TEST version before Deploy
    created = models.DateTimeField(default=timezone.now)
    # created = models.DateTimeField(auto_now_add=True)
