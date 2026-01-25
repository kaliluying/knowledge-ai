"""
分类模型模块

使用 django-mptt 实现树形结构
"""

from django.db import models
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    """
    分类模型

    支持层级结构，最大深度为 3 级
    - 一级分类: 笔记、工作、生活
    - 二级分类: 笔记 -> 技术、学习
    - 三级分类: 技术 -> Python、Django
    """

    name = models.CharField(
        max_length=100,
        verbose_name="分类名称",
    )
    slug = models.SlugField(
        max_length=120,
        unique=True,
        verbose_name="URL别名",
    )
    description = models.TextField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="分类描述",
    )
    color = models.CharField(
        max_length=7,
        default="#1890ff",
        verbose_name="颜色",
        help_text="十六进制颜色值，如 #1890ff",
    )
    icon = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="图标",
        help_text="图标类名或 emoji",
    )
    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
        verbose_name="父分类",
    )
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="categories",
        verbose_name="所属用户",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="是否启用",
    )
    sort_order = models.PositiveIntegerField(
        default=0,
        verbose_name="排序顺序",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="创建时间",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="更新时间",
    )

    class MPTTMeta:
        """MPTT 元数据"""

        order_insertion_by = ["sort_order", "name"]
        parent_attr = "parent"

    class Meta:
        """模型元数据"""

        verbose_name = "分类"
        verbose_name_plural = "分类"
        ordering = ["sort_order", "name"]
        constraints = [
            models.UniqueConstraint(
                fields=["slug", "owner"],
                name="unique_category_slug_per_user",
            )
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """保存时自动生成 slug"""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def level(self):
        """获取分类层级 (从 0 开始)"""
        return self.get_level()

    @property
    def ancestors(self):
        """获取所有祖先"""
        return self.get_ancestors(include_self=False)

    @property
    def descendants(self):
        """获取所有后代"""
        return self.get_descendants(include_self=False)

    @property
    def path(self):
        """获取分类路径，如 '笔记/技术/Django'"""
        if self.parent:
            return f"{self.parent.path}/{self.name}"
        return self.name

    def get_full_path(self):
        """获取完整的分类路径"""
        ancestors = self.get_ancestors(include_self=False)
        path_parts = [ancestor.name for ancestor in ancestors]
        path_parts.append(self.name)
        return "/".join(path_parts)
