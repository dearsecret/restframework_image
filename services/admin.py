from django.contrib import admin
from .models import Card

# Register your models here.


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    fields = (
        "selected",
        "user",
        "evaluate",
        "updated",
        "created",
    )

    readonly_fields = (
        "updated",
        # "created",
    )
