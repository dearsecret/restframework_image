from typing import Any, Callable, Dict, Optional, Tuple, Union
from django.contrib import admin
from django.http.request import HttpRequest
from .models import Number, VerifyNumber

# Register your models here.


@admin.register(Number)
class NumberAdmin(admin.ModelAdmin):
    list_display = (
        "number",
        "user",
        "get_tried",
        "updated_at",
    )

    readonly_fields = (
        "user",
        "number",
        "updated_at",
    )

    def get_tried(self, obj):
        return f"{obj.tried()}"

    def has_change_permission(
        self, request: HttpRequest, obj: Any | None = ...
    ) -> bool:
        return False

    def has_delete_permission(
        self, request: HttpRequest, obj: Any | None = ...
    ) -> bool:
        return False

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False


@admin.register(VerifyNumber)
class VerifyNumberAdmin(admin.ModelAdmin):
    list_display = (
        "number",
        "time",
        "sended",
    )

    readonly_fields = ("number",)

    def has_change_permission(
        self, request: HttpRequest, obj: Any | None = ...
    ) -> bool:
        return False

    def has_delete_permission(
        self, request: HttpRequest, obj: Any | None = ...
    ) -> bool:
        return False

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False
