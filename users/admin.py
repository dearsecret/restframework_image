from django.contrib import admin
from .models import User, Profile, Usage

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "last_login",
        "get_point",
    )

    def get_point(self, obj):
        return obj.point()


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "phone_number",
    )


@admin.register(Usage)
class UsageAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "usage",
        "timestamp",
    )
    readonly_fields = (
        "user",
        "usage",
        "timestamp",
    )
