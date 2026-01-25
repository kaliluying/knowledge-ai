"""
笔记管理后台配置
"""

from django.contrib import admin
from .models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    """
    笔记管理后台
    """

    list_display = [
        "id",
        "title",
        "owner",
        "category",
        "is_pinned",
        "is_archived",
        "view_count",
        "created_at",
    ]
    list_filter = [
        "is_pinned",
        "is_archived",
        "category",
        "created_at",
    ]
    search_fields = ["title", "plain_text", "owner__username"]
    ordering = ["-is_pinned", "-created_at"]
    raw_id_fields = ["owner", "category"]
    readonly_fields = [
        "slug",
        "plain_text",
        "view_count",
        "created_at",
        "updated_at",
        "archived_at",
    ]
    filter_horizontal = ["tags"]

    fieldsets = (
        (None, {"fields": ("title", "slug", "owner")}),
        ("内容", {"fields": ("content", "plain_text")}),
        ("分类", {"fields": ("category", "tags")}),
        ("媒体", {"fields": ("cover_image",)}),
        ("状态", {"fields": ("is_pinned", "is_archived")}),
        ("统计", {"fields": ("view_count",)}),
        ("时间", {"fields": ("created_at", "updated_at", "archived_at")}),
    )
