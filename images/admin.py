from django.contrib import admin
from .models import UserImage

# Register your models here.


@admin.register(UserImage)
class UserImageAdmin(admin.ModelAdmin):
    pass
