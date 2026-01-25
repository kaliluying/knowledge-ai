"""
用户管理后台配置
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    用户管理后台
    """

    list_display = [
        "id",
        "email",
        "username",
        "is_staff",
        "is_superuser",
        "created_at",
    ]
    list_filter = [
        "is_staff",
        "is_superuser",
        "is_active",
        "created_at",
    ]
    search_fields = ["email", "username"]
    ordering = ["-created_at"]

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("个人信息", {"fields": ("username", "avatar", "bio")}),
        (
            "权限",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("时间信息", {"fields": ("created_at", "updated_at")}),
    )
    readonly_fields = ["created_at", "updated_at"]

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )
