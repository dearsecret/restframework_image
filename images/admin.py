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
    )

    fieldsets = (
        (
            "fields",
            {
                "fields": ["user", "url", "image_tag"],
            },
        ),
    )

    readonly_fields = (
        "image_tag",
        "url",
    )

    def image_tag(self, obj):
        return format_html(
            '<img src="{}" width="250"/">'.format(make_signature(obj.url))
        )

    image_tag.short_description = "Image"
