from django.db import models
from common.models import CommonModel

# Create your models here.


class Chat(CommonModel):
    title = models.CharField(max_length=88)
    content = models.CharField(max_length=2000)
    writer = models.ForeignKey(
        "users.User",
        related_name="chats",
        null=True,
        on_delete=models.SET_NULL,
    )
    image = models.URLField(blank=True, null=True)
    views = models.PositiveIntegerField(default=0)
    is_sensitive = models.BooleanField(default=False)

    likes = models.ManyToManyField(
        "users.User",
        related_name="likes",
    )
    dislikes = models.ManyToManyField(
        "users.user",
        related_name="dislikes",
    )

    def count_comment(chat):
        return chat.comments.count()

    def count_likes(chat):
        return chat.likes.count()

    def count_dislikes(chat):
        return chat.dislikes.count()


class Comment(CommonModel):
    comment_post = models.ForeignKey(
        Chat, on_delete=models.CASCADE, related_name="comments"
    )
    author = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="comments"
    )
    content = models.TextField()
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies"
    )

    # def __str__(self):
    #     return str(self.author) + ' comment ' + str(self.content)

    @property
    def children(self):
        return Comment.objects.filter(parent=self).reverse()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False


# class Prefer(CommonModel):
#     chat = models.OneToOneField(
#         Chat, related_name="prefers", on_delete=models.SET_NULL, null=True
#     )
#     likes = models.ManyToManyField("users.User", related_name="likes")
#     dislikes = models.ManyToManyField("users.User", related_name="dislikes")
