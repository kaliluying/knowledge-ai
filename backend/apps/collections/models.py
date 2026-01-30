"""
收藏模型模块

用于收藏和保存外部网页内容
"""

from django.db import models
from django.utils.text import slugify


class Collection(models.Model):
    """
    收藏模型

    用于保存用户收藏的网页链接，支持抓取网页标题、描述和正文内容
    """

    title = models.CharField(
        max_length=500,
        verbose_name="标题",
        help_text="收藏内容的标题",
    )
    description = models.TextField(
        blank=True,
        default="",
        verbose_name="描述",
        help_text="收藏内容的简要描述",
    )
    url = models.URLField(
        max_length=2000,
        verbose_name="原始链接",
    )
    domain = models.CharField(
        max_length=255,
        verbose_name="域名",
        help_text="来源网站域名",
    )
    favicon = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="网站图标",
    )
    image = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="封面图片",
    )
    content = models.TextField(
        blank=True,
        default="",
        verbose_name="正文内容",
        help_text="抓取的网页正文内容",
    )
    html_content = models.TextField(
        blank=True,
        default="",
        verbose_name="原始HTML",
        help_text="原始 HTML 内容，用于二次处理",
    )
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="collections",
        verbose_name="所属用户",
    )
    is_processed = models.BooleanField(
        default=False,
        verbose_name="是否已处理",
        help_text="标记内容是否已成功抓取和处理",
    )
    word_count = models.PositiveIntegerField(
        default=0,
        verbose_name="字数",
    )
    view_count = models.PositiveIntegerField(
        default=0,
        verbose_name="浏览次数",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="创建时间",
        db_index=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="更新时间",
    )

    class Meta:
        verbose_name = "收藏"
        verbose_name_plural = "收藏"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["owner", "created_at"]),
            models.Index(fields=["owner", "is_processed"]),
        ]

    def __str__(self):
        return self.title[:50]

    def save(self, *args, **kwargs):
        """保存时提取域名和统计字数"""
        if not self.domain:
            # 从 URL 提取域名
            from urllib.parse import urlparse

            parsed = urlparse(self.url)
            self.domain = parsed.netloc

        if self.content:
            self.word_count = len(self.content.split())

        super().save(*args, **kwargs)

    @property
    def reading_time(self):
        """获取预计阅读时间（分钟）"""
        words_per_minute = 200
        minutes = max(1, self.word_count // words_per_minute)
        return minutes
