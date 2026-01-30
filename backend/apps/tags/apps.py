"""
Tags app configuration.
"""

from django.apps import AppConfig


class TagsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.tags"
    verbose_name = "标签"

    def ready(self) -> None:
        from . import signals  # noqa: F401
