"""
自定义分页器模块
"""

from rest_framework.pagination import PageNumberPagination, CursorPagination


class StandardPagination(PageNumberPagination):
    """
    标准分页器

    适用于大多数列表接口，支持页码导航
    响应格式:
    {
        "count": 100,
        "next": "http://api/notes/?page=2",
        "previous": null,
        "results": [...]
    }
    """

    page_size = 20
    page_query_param = "page"
    page_size_query_param = "page_size"
    max_page_size = 100


class SmallPagination(PageNumberPagination):
    """
    小型分页器

    适用于数据量较大的列表
    """

    page_size = 10
    page_query_param = "page"
    page_size_query_param = "page_size"
    max_page_size = 50


class LargePagination(PageNumberPagination):
    """
    大型分页器

    适用于数据量较小的列表
    """

    page_size = 50
    page_query_param = "page"
    page_size_query_param = "page_size"
    max_page_size = 200


class NoteCursorPagination(CursorPagination):
    """
    笔记专用游标分页器

    适用于大数据量，性能更好
    响应格式:
    {
        "next": "http://api/notes/?cursor=abc123",
        "previous": null,
        "results": [...]
    }
    """

    page_size = 20
    ordering = "-created_at"
    cursor_query_param = "cursor"


class NotePagination(StandardPagination):
    """
    笔记专用分页器
    """

    page_size = 12
    max_page_size = 48


class CategoryPagination(StandardPagination):
    """
    分类专用分页器
    """

    page_size = 50


class TagPagination(StandardPagination):
    """
    标签专用分页器
    """

    page_size = 100
