"""
分类视图模块
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Prefetch

from .models import Category
from .serializers import (
    CategorySerializer,
    CategoryListSerializer,
    CategoryTreeSerializer,
    CategoryCreateSerializer,
    CategoryUpdateSerializer,
)
from utils.permissions import IsOwnerOrReadOnly


class CategoryViewSet(viewsets.ModelViewSet):
    """
    分类视图集

    提供 CRUD 操作:
    - GET /api/categories/ - 分类列表
    - POST /api/categories/ - 创建分类
    - GET /api/categories/{id}/ - 分类详情
    - PUT /api/categories/{id}/ - 更新分类
    - DELETE /api/categories/{id}/ - 删除分类
    - GET /api/categories/tree/ - 分类树
    - GET /api/categories/{id}/children/ - 子分类列表
    """

    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = "id"

    def get_queryset(self):
        """获取当前用户的分类"""
        user = self.request.user
        return (
            Category.objects.filter(owner=user)
            .select_related("parent")
            .prefetch_related(
                Prefetch(
                    "children",
                    queryset=Category.objects.filter(is_active=True),
                )
            )
        )

    def get_serializer_class(self):
        """根据操作返回不同的序列化器"""
        if self.action == "list":
            return CategoryListSerializer
        if self.action == "tree":
            return CategoryTreeSerializer
        if self.action == "create":
            return CategoryCreateSerializer
        if self.action in ["update", "partial_update"]:
            return CategoryUpdateSerializer
        return CategorySerializer

    def perform_create(self, serializer):
        """创建时设置所有者"""
        serializer.save(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        """创建分类并返回包装的响应"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        category = Category.objects.get(id=serializer.instance.id)
        response_serializer = CategorySerializer(category)

        return Response(
            {
                "code": 201,
                "message": "创建成功",
                "data": response_serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )

    def retrieve(self, request, *args, **kwargs):
        """获取分类详情并返回包装的响应"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
            {
                "code": 200,
                "message": "获取成功",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def update(self, request, *args, **kwargs):
        """更新分类并返回包装的响应"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        category = Category.objects.get(id=instance.id)
        response_serializer = CategorySerializer(category)

        return Response(
            {
                "code": 200,
                "message": "更新成功",
                "data": response_serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["get"])
    def tree(self, request):
        """
        获取分类树

        GET /api/categories/tree/
        """
        # 获取所有一级分类（root）
        root_categories = self.get_queryset().filter(parent__isnull=True)

        serializer = CategoryTreeSerializer(root_categories, many=True)
        return Response(
            {
                "code": 200,
                "message": "获取成功",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["get"])
    def children(self, request, id=None):
        """
        获取子分类

        GET /api/categories/{id}/children/
        """
        category = self.get_object()
        children = category.get_children().filter(is_active=True)

        serializer = CategoryListSerializer(children, many=True)
        return Response(
            {
                "code": 200,
                "message": "获取成功",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["get"])
    def root(self, request):
        """
        获取一级分类

        GET /api/categories/root/
        """
        root_categories = self.get_queryset().filter(parent__isnull=True)

        serializer = CategoryListSerializer(root_categories, many=True)
        return Response(
            {
                "code": 200,
                "message": "获取成功",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["get"])
    def all(self, request):
        """
        获取所有分类（扁平结构）

        GET /api/categories/all/
        """
        categories = self.get_queryset().filter(is_active=True)

        serializer = CategoryListSerializer(categories, many=True)
        return Response(
            {
                "code": 200,
                "message": "获取成功",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, *args, **kwargs):
        """
        删除分类

        删除时将子分类的父分类设为祖父分类
        """
        category = self.get_object()

        # 获取所有子分类
        children = category.get_children()

        if children.exists():
            # 将子分类的父分类设为祖父分类
            grandparent = category.parent
            children.update(parent=grandparent)

        # 删除分类
        category.delete()

        return Response(
            {"code": 200, "message": "删除成功"},
            status=status.HTTP_200_OK,
        )
