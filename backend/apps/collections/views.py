"""
收藏视图模块
"""

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.db import models

from .models import Collection
from .serializers import (
    CollectionSerializer,
    CollectionListSerializer,
    CollectionCreateSerializer,
)
from .services import URLScraperService


class CollectionViewSet(viewsets.ModelViewSet):
    """
    收藏视图集

    提供收藏的 CRUD 操作
    """

    serializer_class = CollectionSerializer

    def get_queryset(self):
        """获取当前用户的收藏列表"""
        return Collection.objects.filter(owner=self.request.user)

    def get_serializer_class(self):
        """根据动作返回不同的序列化器"""
        if self.action == "list":
            return CollectionListSerializer
        if self.action == "create":
            return CollectionCreateSerializer
        return CollectionSerializer

    def create(self, request, *args, **kwargs):
        """创建收藏"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 创建收藏记录
        collection = serializer.save()

        # 异步抓取网页内容（可选，这里使用同步方式）
        try:
            scraper = URLScraperService()
            result = scraper.scrape(collection.url)

            if result["success"]:
                collection.title = result["title"]
                collection.description = result.get("description", "")[:500]
                collection.content = result.get("content", "")
                collection.html_content = result.get("html_content", "")
                collection.favicon = result.get("favicon")
                collection.image = result.get("image")
                collection.is_processed = True
                collection.save()
        except Exception:
            # 抓取失败不影响收藏创建
            pass

        output_serializer = CollectionSerializer(collection)
        return Response(
            {
                "code": 201,
                "message": "收藏创建成功",
                "data": output_serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        """更新收藏"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        collection = self.get_queryset().get(id=instance.id)
        output_serializer = CollectionSerializer(collection)
        return Response(
            {
                "code": 200,
                "message": "更新成功",
                "data": output_serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def list(self, request, *args, **kwargs):
        """获取收藏列表"""
        queryset = self.get_queryset()

        # 搜索过滤
        search = request.query_params.get("search")
        if search:
            queryset = queryset.filter(
                models.Q(title__icontains=search)
                | models.Q(description__icontains=search)
                | models.Q(content__icontains=search)
            )

        # 处理状态过滤
        processed = request.query_params.get("processed")
        if processed is not None:
            queryset = queryset.filter(is_processed=processed.lower() == "true")

        # 排序
        order = request.query_params.get("order", "-created_at")
        allowed_orders = ["created_at", "-created_at", "title", "-title"]
        if order not in allowed_orders:
            order = "-created_at"
        queryset = queryset.order_by(order)

        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {
                "code": 200,
                "message": "获取成功",
                "data": serializer.data,
                "count": queryset.count(),
            }
        )

    def retrieve(self, request, *args, **kwargs):
        """获取收藏详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        # 增加浏览次数
        instance.view_count += 1
        instance.save(update_fields=["view_count"])

        return Response(
            {
                "code": 200,
                "message": "获取成功",
                "data": serializer.data,
            }
        )

    def destroy(self, request, *args, **kwargs):
        """删除收藏"""
        instance = self.get_object()
        instance.delete()
        return Response(
            {
                "code": 200,
                "message": "删除成功",
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"])
    def refresh(self, request, pk=None):
        """刷新收藏内容"""
        collection = self.get_object()

        try:
            scraper = URLScraperService()
            result = scraper.scrape(collection.url)

            if result["success"]:
                collection.title = result["title"]
                collection.description = result.get("description", "")[:500]
                collection.content = result.get("content", "")
                collection.html_content = result.get("html_content", "")
                collection.favicon = result.get("favicon") or collection.favicon
                collection.image = result.get("image") or collection.image
                collection.is_processed = True
                collection.save()

                serializer = CollectionSerializer(collection)
                return Response(
                    {
                        "code": 200,
                        "message": "刷新成功",
                        "data": serializer.data,
                    }
                )
            else:
                return Response(
                    {
                        "code": 400,
                        "message": "刷新失败：" + result.get("error", "未知错误"),
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            return Response(
                {"code": 400, "message": f"刷新失败：{str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=False, methods=["get"])
    def recent(self, request):
        """获取最近收藏"""
        limit = int(request.query_params.get("limit", 5))
        collections = self.get_queryset()[:limit]
        serializer = CollectionListSerializer(collections, many=True)
        return Response(
            {
                "code": 200,
                "message": "获取成功",
                "data": serializer.data,
            }
        )
