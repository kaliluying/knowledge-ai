"""
分类管理后台配置
"""

from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Category


@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    """
    分类管理后台

    使用 MPTTModelAdmin 支持树形结构展示
    """

    list_display = [
        "name",
        "slug",
        "owner",
        "parent",
        "is_active",
        "sort_order",
        "created_at",
    ]
    list_filter = [
        "is_active",
        "parent",
        "created_at",
    ]
    search_fields = ["name", "slug", "owner__username"]
    ordering = ["sort_order", "name"]
    raw_id_fields = ["owner", "parent"]
    readonly_fields = ["slug", "created_at", "updated_at"]

    mptt_level_indent = 20

    fieldsets = (
        (None, {"fields": ("name", "slug", "owner")}),
        ("信息", {"fields": ("description", "color", "icon")}),
        ("层级", {"fields": ("parent", "sort_order")}),
        ("状态", {"fields": ("is_active",)}),
        ("时间", {"fields": ("created_at", "updated_at")}),
    )
