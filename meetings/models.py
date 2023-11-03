from django.db import models

# Create your models here.


class Meeting(models.Model):
    title = models.CharField(max_length=88)
    content = models.CharField(max_length=1000)
    invisible = models.BooleanField(default=False)
    photo = models.URLField()
    descriptions = models.ManyToManyField("users.User", related_name="descriptions")
    user = models.ForeignKey(
        "users.User",
        related_name="meetings",
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(auto_now_add=True)
