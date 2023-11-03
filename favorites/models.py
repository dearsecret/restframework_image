from django.db import models


class Favorite(models.Model):
    posts = models.ManyToManyField(
        "chats.Chat",
        related_name="favorites",
    )
    user = models.OneToOneField(
        "users.User",
        related_name="favorites",
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(auto_now_add=True)
