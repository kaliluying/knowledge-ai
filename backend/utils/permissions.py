"""
自定义权限类模块
"""

from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    自定义权限：只有资源所有者才能修改，其他用户只能读取

    用于笔记、分类、标签等用户私有资源的权限控制
    """

    def has_object_permission(self, request, view, obj):
        """检查对象权限"""
        # 读取权限：允许任何认证用户
        if request.method in permissions.SAFE_METHODS:
            return True

        # 写入权限：只有所有者可以
        return obj.owner == request.user


class IsOwner(permissions.BasePermission):
    """
    自定义权限：只有资源所有者才能访问

    用于严格的权限控制场景
    """

    def has_object_permission(self, request, view, obj):
        """检查对象权限"""
        return obj.owner == request.user


class IsAuthenticated(permissions.BasePermission):
    """
    自定义权限：用户必须认证

    继承自 DRF 默认实现，添加中文错误消息
    """

    message = "用户未认证，请先登录"

    def has_permission(self, request, view):
        """检查用户是否认证"""
        return request.user and request.user.is_authenticated


class IsAdminUser(permissions.BasePermission):
    """
    自定义权限：只有管理员才能访问

    用于管理后台等场景
    """

    message = "权限不足，需要管理员权限"

    def has_permission(self, request, view):
        """检查用户是否为管理员"""
        return request.user and request.user.is_staff


class IsSuperUser(permissions.BasePermission):
    """
    自定义权限：只有超级管理员才能访问

    用于系统级管理操作
    """

    message = "权限不足，需要超级管理员权限"

    def has_permission(self, request, view):
        """检查用户是否为超级管理员"""
        return request.user and request.user.is_superuser


class AllowAny(permissions.BasePermission):
    """
    自定义权限：允许任何人访问

    用于公开资源，如登录、注册等接口
    """

    def has_permission(self, request, view):
        """始终返回 True"""
        return True
