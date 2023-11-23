from django.contrib import admin
from django.utils.html import format_html
from .models import UserImage
from .signature import make_signature

# Register your models here.


@admin.register(UserImage)
class UserImageAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "created_at",
        "status",
    )

    fieldsets = (
        (
            "기본정보",
            {
                "fields": ["user", "url", "index"],
            },
        ),
        (
            "평가",
            {
                "fields": [
                    "status",
                ],
            },
        ),
    )

    # readonly_fields = (
    #     "user",
    #     "url",
    #     "index",
    #     "image_tag",
    # )

    # def image_tag(self, obj):
    #     if obj.url:
    #         return format_html(
    #             '<img src="{}" width="250"/">'.format(make_signature(obj.url))
    #         )
    #     return None

    # image_tag.short_description = "Image"
