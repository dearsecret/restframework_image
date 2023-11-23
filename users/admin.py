from django.contrib import admin
from .models import User, Profile, Usage

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "username",
        "last_login",
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user",)


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
