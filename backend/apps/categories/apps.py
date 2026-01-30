"""
Categories app configuration.
"""

from django.apps import AppConfig


class CategoriesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.categories"
    verbose_name = "分类"

    def ready(self) -> None:
        from . import signals  # noqa: F401
