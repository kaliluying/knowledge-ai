"""
知识图谱模型模块

包含图谱节点和链接的数据库模型。
"""

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class GraphNode(models.Model):
    """
    图谱节点模型

    表示知识图谱中的一个节点，可以是笔记、分类、标签等。
    """

    NODE_TYPE_CHOICES = [
        ("note", "笔记"),
        ("category", "分类"),
        ("tag", "标签"),
        ("collection", "收藏"),
    ]

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="graph_nodes",
        verbose_name="所属用户",
    )
    node_type = models.CharField(
        max_length=20,
        choices=NODE_TYPE_CHOICES,
        verbose_name="节点类型",
    )
    title = models.CharField(
        max_length=200,
        verbose_name="标题",
    )
    label = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="显示标签",
    )
    data = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="附加数据",
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
        verbose_name = "图谱节点"
        verbose_name_plural = "图谱节点"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.node_type}: {self.title}"

    def save(self, *args, **kwargs):
        """保存时自动生成 label"""
        if not self.label:
            self.label = self.title[:50]
        super().save(*args, **kwargs)


class GraphLink(models.Model):
    """
    图谱链接模型

    表示知识图谱中两个节点之间的关系。
    """

    LINK_TYPE_CHOICES = [
        ("related", "相关"),
        ("parent", "父子/分类"),
        ("tagged", "标签"),
        ("similar", "相似"),
        ("reference", "引用"),
    ]

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="graph_links",
        verbose_name="所属用户",
    )
    source = models.ForeignKey(
        GraphNode,
        on_delete=models.CASCADE,
        related_name="outgoing_links",
        verbose_name="源节点",
    )
    target = models.ForeignKey(
        GraphNode,
        on_delete=models.CASCADE,
        related_name="incoming_links",
        verbose_name="目标节点",
    )
    link_type = models.CharField(
        max_length=20,
        choices=LINK_TYPE_CHOICES,
        default="related",
        verbose_name="链接类型",
    )
    description = models.TextField(
        max_length=500,
        blank=True,
        verbose_name="描述",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="创建时间",
    )

    class Meta:
        verbose_name = "图谱链接"
        verbose_name_plural = "图谱链接"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["source", "target"],
                name="unique_link_per_nodes",
            )
        ]

    def __str__(self):
        return f"{self.source} -> {self.target} ({self.link_type})"
