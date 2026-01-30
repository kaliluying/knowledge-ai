"""
附件模型模块
"""

import os
import uuid
from django.db import models
from django.utils.text import slugify


def attachment_file_path(instance, filename):
    """
    生成附件文件路径

    上传文件存储到: media/attachments/{user_id}/{year}/{month}/{uuid}_{filename}
    """
    # 获取文件扩展名
    ext = os.path.splitext(filename)[1].lower()

    # 生成唯一文件名
    unique_id = uuid.uuid4().hex[:12]
    base_name = slugify(filename[:50]) if filename else "file"

    # 构建路径
    user_id = instance.owner.id if instance.owner else "unknown"
    return f"attachments/{user_id}/{unique_id}{ext}"


class Attachment(models.Model):
    """
    附件模型

    用于存储用户上传的文件，支持图片、文档等
    """

    FILE_TYPE_CHOICES = [
        ("image", "图片"),
        ("document", "文档"),
        ("video", "视频"),
        ("audio", "音频"),
        ("other", "其他"),
    ]

    name = models.CharField(
        max_length=255,
        verbose_name="文件名",
    )
    file = models.FileField(
        upload_to=attachment_file_path,
        verbose_name="文件",
    )
    file_type = models.CharField(
        max_length=20,
        choices=FILE_TYPE_CHOICES,
        default="other",
        verbose_name="文件类型",
    )
    mime_type = models.CharField(
        max_length=100,
        blank=True,
        default="",
        verbose_name="MIME类型",
    )
    size = models.PositiveIntegerField(
        default=0,
        verbose_name="文件大小（字节）",
    )
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="attachments",
        verbose_name="所属用户",
    )
    note = models.ForeignKey(
        "notes.Note",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="attachments",
        verbose_name="所属笔记",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="创建时间",
        db_index=True,
    )

    class Meta:
        verbose_name = "附件"
        verbose_name_plural = "附件"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["owner", "created_at"]),
            models.Index(fields=["note", "created_at"]),
        ]

    def __str__(self):
        return self.name[:50]

    def save(self, *args, **kwargs):
        """保存时设置文件信息"""
        # 如果没有设置文件名，从文件名提取
        if not self.name:
            self.name = os.path.splitext(self.file.name)[0][:255]

        # 设置文件大小
        if self.file and self.size == 0:
            self.size = self.file.size

        # 推断文件类型
        if self.file:
            mime = self.file.content_type if self.file.content_type else ""

            if not self.mime_type:
                self.mime_type = mime

            # 根据 MIME 类型推断文件类型
            if mime.startswith("image/"):
                self.file_type = "image"
            elif mime.startswith("video/"):
                self.file_type = "video"
            elif mime.startswith("audio/"):
                self.file_type = "audio"
            elif mime in [
                "application/pdf",
                "application/msword",
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                "application/vnd.ms-excel",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                "application/vnd.ms-powerpoint",
                "application/vnd.openxmlformats-officedocument.presentationml.presentation",
                "text/plain",
                "text/markdown",
                "text/html",
            ]:
                self.file_type = "document"
            else:
                self.file_type = "other"

        super().save(*args, **kwargs)

    @property
    def size_formatted(self):
        """获取格式化后的文件大小"""
        for unit in ["B", "KB", "MB", "GB"]:
            if self.size < 1024:
                return f"{self.size:.1f} {unit}"
            self.size /= 1024
        return f"{self.size:.1f} TB"

    @property
    def extension(self):
        """获取文件扩展名"""
        if self.file:
            return os.path.splitext(self.file.name)[1].lower()
        return ""
