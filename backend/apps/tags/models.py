"""
标签模型模块
"""

from django.db import models
from django.utils.text import slugify


class Tag(models.Model):
    """
    标签模型

    用于对笔记进行多维度分类
    """

    name = models.CharField(
        max_length=50,
        verbose_name="标签名称",
    )
    slug = models.SlugField(
        max_length=60,
        unique=True,
        verbose_name="URL别名",
    )
    color = models.CharField(
        max_length=7,
        default="#1890ff",
        verbose_name="颜色",
        help_text="十六进制颜色值，如 #1890ff",
    )
    description = models.TextField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="标签描述",
    )
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="tags",
        verbose_name="所属用户",
    )
    usage_count = models.PositiveIntegerField(
        default=0,
        verbose_name="使用次数",
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
        verbose_name = "标签"
        verbose_name_plural = "标签"
        ordering = ["-usage_count", "name"]
        constraints = [
            models.UniqueConstraint(
                fields=["slug", "owner"],
                name="unique_tag_slug_per_user",
            )
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """保存时自动生成 slug"""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def increment_usage(self):
        """增加使用次数"""
        self.usage_count += 1
        self.save(update_fields=["usage_count", "updated_at"])

    def decrement_usage(self):
        """减少使用次数"""
        if self.usage_count > 0:
            self.usage_count -= 1
            self.save(update_fields=["usage_count", "updated_at"])
