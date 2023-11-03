from django.contrib import admin
from .models import Chat, Comment

# Register your models here.


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = [
        "__str__",
        "count_comment",
    ]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass
