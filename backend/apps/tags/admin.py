"""
标签管理后台配置
"""

from django.contrib import admin
from .models import Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    标签管理后台
    """

    list_display = [
        "id",
        "name",
        "slug",
        "color",
        "owner",
        "usage_count",
        "created_at",
    ]
    list_filter = [
        "color",
        "created_at",
    ]
    search_fields = ["name", "slug", "owner__username"]
    ordering = ["-usage_count", "name"]
    raw_id_fields = ["owner"]
    readonly_fields = ["slug", "created_at", "updated_at"]
