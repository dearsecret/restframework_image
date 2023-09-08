from django.contrib import admin
from django.utils.html import format_html
from .models import UserImage

# Register your models here.


@admin.register(UserImage)
class UserImageAdmin(admin.ModelAdmin):
    list_display = (
        "image_tag",
        "user",
        "url",
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
        return format_html('<img src="{}" width=200 height=80/>'.format(obj.url))

    image_tag.short_description = "Image"
