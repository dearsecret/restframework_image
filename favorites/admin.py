from django.contrib import admin
from .models import Favorite

# Register your models here.


@admin.register(Favorite)
class FovirteAdmin(admin.ModelAdmin):
    pass
