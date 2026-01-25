"""
用户模型模块
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    自定义用户模型

    扩展 Django 默认的 AbstractUser，添加头像和个人简介字段
    """

    avatar = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="头像URL",
        help_text="用户头像的URL地址",
    )
    bio = models.TextField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="个人简介",
        help_text="用户的个人简介，最多500字符",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="创建时间",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="更新时间",
    )

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = "用户"
        ordering = ["-created_at"]

    def __str__(self):
        return self.username
