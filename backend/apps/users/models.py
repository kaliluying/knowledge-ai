"""
用户模型模块
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    """
    自定义用户模型

    扩展 Django 默认的 AbstractUser，添加头像和个人简介字段
    """

    email = models.EmailField(
        unique=True,
        verbose_name="邮箱",
        help_text="用户邮箱，唯一标识",
    )
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


class Profile(models.Model):
    """
    用户详细资料模型

    存储用户的扩展信息，如偏好设置、统计信息等
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="用户",
    )

    # 偏好设置
    theme = models.CharField(
        max_length=20,
        default="light",
        choices=[("light", "亮色"), ("dark", "暗色"), ("auto", "跟随系统")],
        verbose_name="主题",
    )
    language = models.CharField(
        max_length=10,
        default="zh-CN",
        verbose_name="语言",
    )
    timezone = models.CharField(
        max_length=50,
        default="Asia/Shanghai",
        verbose_name="时区",
    )

    # 统计信息
    notes_count = models.PositiveIntegerField(
        default=0,
        verbose_name="笔记数量",
    )
    categories_count = models.PositiveIntegerField(
        default=0,
        verbose_name="分类数量",
    )
    tags_count = models.PositiveIntegerField(
        default=0,
        verbose_name="标签数量",
    )

    # 活跃度
    last_active_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="最后活跃时间",
    )
    login_count = models.PositiveIntegerField(
        default=0,
        verbose_name="登录次数",
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
        verbose_name = "用户资料"
        verbose_name_plural = "用户资料"

    def __str__(self):
        return f"{self.user.username}的资料"

    def update_stats(self, notes=0, categories=0, tags=0):
        """更新统计信息"""
        self.notes_count = notes
        self.categories_count = categories
        self.tags_count = tags
        self.save(
            update_fields=[
                "notes_count",
                "categories_count",
                "tags_count",
                "updated_at",
            ]
        )

    def record_login(self):
        """记录登录"""
        self.login_count += 1
        self.last_active_at = timezone.now()
        self.save(update_fields=["login_count", "last_active_at", "updated_at"])

    def update_theme(self, theme: str):
        """更新主题设置"""
        if theme in ["light", "dark", "auto"]:
            self.theme = theme
            self.save(update_fields=["theme", "updated_at"])
