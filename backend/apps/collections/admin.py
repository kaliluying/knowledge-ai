"""
收藏管理后台配置
"""

from django.contrib import admin
from .models import Collection


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    """
    收藏管理后台
    """

    list_display = [
        "id",
        "title",
        "domain",
        "owner",
        "is_processed",
        "word_count",
        "view_count",
        "created_at",
    ]
    list_filter = [
        "is_processed",
        "domain",
        "created_at",
    ]
    search_fields = ["title", "description", "content", "owner__username", "url"]
    ordering = ["-created_at"]
    raw_id_fields = ["owner"]
    readonly_fields = [
        "domain",
        "word_count",
        "view_count",
        "created_at",
        "updated_at",
    ]
    fieldsets = (
        (None, {"fields": ("title", "url", "owner")}),
        ("来源", {"fields": ("domain", "favicon", "image")}),
        ("内容", {"fields": ("description", "content", "html_content")}),
        ("状态", {"fields": ("is_processed",)}),
        ("统计", {"fields": ("word_count", "view_count")}),
        ("时间", {"fields": ("created_at", "updated_at")}),
    )
