"""
笔记模型模块

Markdown 编辑器内容存储
"""

from django.db import models
from django.utils.text import slugify


class Note(models.Model):
    """
    笔记模型

    使用 Markdown 编辑器存储文本内容
    """

    title = models.CharField(
        max_length=200,
        verbose_name="标题",
    )
    slug = models.SlugField(
        max_length=220,
        unique=True,
        verbose_name="URL别名",
    )
    content = models.TextField(
        blank=True,
        default="",
        verbose_name="Markdown 内容",
    )
    plain_text = models.TextField(
        blank=True,
        default="",
        verbose_name="纯文本内容",
        help_text="用于全文搜索",
    )
    related_notes = models.ManyToManyField(
        "self",
        symmetrical=True,
        blank=True,
        verbose_name="相关笔记",
    )
    cover_image = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="封面图",
    )
    category = models.ForeignKey(
        "categories.Category",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="notes",
        verbose_name="分类",
    )
    tags = models.ManyToManyField(
        "tags.Tag",
        related_name="notes",
        blank=True,
        verbose_name="标签",
    )
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="notes",
        verbose_name="所属用户",
    )
    is_pinned = models.BooleanField(
        default=False,
        verbose_name="是否置顶",
    )
    is_archived = models.BooleanField(
        default=False,
        verbose_name="是否归档",
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
    archived_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="归档时间",
    )

    class Meta:
        verbose_name = "笔记"
        verbose_name_plural = "笔记"
        ordering = ["-is_pinned", "-created_at"]
        indexes = [
            models.Index(fields=["owner", "created_at"]),
            models.Index(fields=["owner", "is_archived"]),
            models.Index(fields=["owner", "is_pinned"]),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """保存时自动生成 slug 和纯文本"""
        if not self.slug:
            self.slug = slugify(self.title)

        # 从 Markdown 内容生成纯文本
        if self.content:
            self.plain_text = self._extract_text_from_markdown(self.content)

        super().save(*args, **kwargs)

    def _extract_text_from_markdown(self, content):
        """从 Markdown 内容提取纯文本"""
        import re
        # 移除 Markdown 语法标记，保留纯文本
        text = content
        # 移除标题标记 (#)
        text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
        # 移除粗体标记
        text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
        text = re.sub(r'__(.+?)__', r'\1', text)
        # 移除斜体标记
        text = re.sub(r'\*(.+?)\*', r'\1', text)
        text = re.sub(r'_(.+?)_', r'\1', text)
        # 移除删除线
        text = re.sub(r'~~(.+?)~~', r'\1', text)
        # 移除行内代码标记
        text = re.sub(r'`(.+?)`', r'\1', text)
        # 移除代码块
        text = re.sub(r'```[\s\S]*?```', '', text)
        # 移除链接 [text](url)
        text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
        # 移除图片
        text = re.sub(r'!\[([^\]]*)\]\([^\)]+\)', r'\1', text)
        # 移除引用标记
        text = re.sub(r'^>\s+', '', text, flags=re.MULTILINE)
        # 移除列表标记
        text = re.sub(r'^[\s]*[-*+]\s+', '', text, flags=re.MULTILINE)
        text = re.sub(r'^[\s]*\d+\.\s+', '', text, flags=re.MULTILINE)
        # 移除水平线
        text = re.sub(r'^[-*_]{3,}$', '', text, flags=re.MULTILINE)
        # 移除 HTML 标签
        text = re.sub(r'<[^>]+>', '', text)
        # 合并空白字符
        text = re.sub(r'\s+', ' ', text).strip()

        return text

    @property
    def word_count(self):
        """获取字数"""
        return len(self.plain_text.split())

    @property
    def reading_time(self):
        """获取预计阅读时间（分钟）"""
        words_per_minute = 200
        words = len(self.plain_text.split())
        minutes = max(1, words // words_per_minute)
        return minutes

    def increment_view(self):
        """增加浏览次数"""
        self.view_count += 1
        self.save(update_fields=["view_count"])
