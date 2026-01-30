"""
用户视图模块
"""

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models import Count
from django.http import JsonResponse
import json

from .serializers import (
    UserCreateSerializer,
    UserSerializer,
    LoginSerializer,
    PasswordChangeSerializer,
    PreferencesSerializer,
)

User = get_user_model()


class RegisterView(APIView):
    """
    用户注册视图

    POST /api/auth/register/
    """

    permission_classes = [AllowAny]
    serializer_class = UserCreateSerializer

    def post(self, request):
        """
        处理用户注册
        """
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            # 收集所有错误信息
            error_messages = []
            errors_dict = dict(serializer.errors)
            for field, errors in errors_dict.items():
                for error in errors:
                    if field == "email":
                        error_messages.append("邮箱已被注册")
                    elif field == "username":
                        error_messages.append("用户名已被使用")
                    elif field == "password":
                        # 收集原始错误信息
                        for error in errors:
                            error_messages.append(str(error))
                        # 附加密码格式要求说明
                        error_messages.append(
                            "密码要求：至少8个字符，包含大写字母、小写字母、数字和特殊字符"
                        )
                    else:
                        error_messages.append(str(error))

            # 如果有密码不一致的错误，优先显示
            if "password_confirm" in errors_dict:
                error_messages.insert(0, "两次输入的密码不一致")

            error_msg = (
                " ".join(error_messages)
                if error_messages
                else "注册信息有误，请检查后重试"
            )

            return Response(
                {"code": 400, "message": error_msg},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = serializer.save()

        # 生成 Token
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "code": 201,
                "message": "注册成功",
                "data": {
                    "user": UserSerializer(user).data,
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                },
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    """
    用户登录视图

    POST /api/auth/login/
    """

    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        """
        处理用户登录
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"code": 401, "message": "邮箱或密码不正确"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not user.check_password(password):
            return Response(
                {"code": 401, "message": "邮箱或密码不正确"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # 生成 Token
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "code": 200,
                "message": "登录成功",
                "data": {
                    "user": UserSerializer(user).data,
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                },
            },
            status=status.HTTP_200_OK,
        )


class LogoutView(APIView):
    """
    用户登出视图

    POST /api/auth/logout/
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        处理用户登出
        """
        try:
            refresh_token = request.data.get("refresh")
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            return Response(
                {"code": 200, "message": "登出成功"},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"code": 400, "message": "登出失败"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class RefreshTokenView(APIView):
    """
    Token 刷新视图

    POST /api/auth/refresh/
    """

    permission_classes = [AllowAny]

    def post(self, request):
        """
        刷新 Access Token
        """
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response(
                {"code": 400, "message": "缺少 refresh token"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            token = RefreshToken(refresh_token)
            access_token = str(token.access_token)
            return Response(
                {
                    "code": 200,
                    "message": "刷新成功",
                    "data": {"access": access_token},
                },
                status=status.HTTP_200_OK,
            )
        except Exception:
            return Response(
                {"code": 401, "message": "无效的 refresh token"},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class ProfileView(APIView):
    """
    用户信息视图

    GET /api/auth/profile/ - 获取用户信息
    PUT /api/auth/profile/ - 更新用户信息
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        获取当前用户信息
        """
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(
            {
                "code": 200,
                "message": "获取成功",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def put(self, request):
        """
        更新当前用户信息
        """
        # 处理头像上传
        if 'avatar' in request.FILES:
            request.user.avatar.delete(save=False)  # 删除旧头像
            request.user.avatar = request.FILES['avatar']
            request.user.save(update_fields=['avatar', 'updated_at'])

            # 返回更新后的用户信息
            serializer = UserSerializer(request.user, context={'request': request})
            return Response(
                {
                    "code": 200,
                    "message": "头像上传成功",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )

        # 处理其他字段更新
        serializer = UserSerializer(
            request.user, data=request.data, partial=True, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "code": 200,
                "message": "更新成功",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class ChangePasswordView(APIView):
    """
    密码修改视图

    POST /api/auth/password/change/
    """

    permission_classes = [IsAuthenticated]
    serializer_class = PasswordChangeSerializer

    def post(self, request):
        """
        修改用户密码
        """
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        # 设置新密码
        request.user.set_password(serializer.validated_data["new_password"])
        request.user.save()

        return Response(
            {"code": 200, "message": "密码修改成功"},
            status=status.HTTP_200_OK,
        )


class UserDetailView(APIView):
    """
    用户详情视图（根据ID获取）

    GET /api/auth/users/{id}/
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        """
        获取指定用户信息
        """
        try:
            user = User.objects.get(id=user_id)
            serializer = UserSerializer(user)
            return Response(
                {
                    "code": 200,
                    "message": "获取成功",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except User.DoesNotExist:
            return Response(
                {"code": 404, "message": "用户不存在"},
                status=status.HTTP_404_NOT_FOUND,
            )


class PreferencesView(APIView):
    """
    偏好设置视图

    GET /api/auth/preferences/ - 获取偏好设置
    PUT /api/auth/preferences/ - 更新偏好设置
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """获取用户偏好设置"""
        try:
            profile = getattr(request.user, 'profile', None)
        except Exception:
            profile = None

        if not profile:
            # 创建默认偏好设置
            from .models import Profile
            profile = Profile.objects.create(user=request.user)

        serializer = PreferencesSerializer(profile)
        return Response(
            {
                "code": 200,
                "message": "获取成功",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def put(self, request):
        """更新用户偏好设置"""
        try:
            profile = getattr(request.user, 'profile', None)
        except Exception:
            profile = None

        if not profile:
            from .models import Profile
            profile = Profile.objects.create(user=request.user)

        serializer = PreferencesSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "code": 200,
                "message": "更新成功",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class SessionsView(APIView):
    """
    登录设备视图

    GET /api/auth/sessions/ - 获取所有登录设备
    DELETE /api/auth/sessions/{id}/ - 退出指定设备
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """获取用户的登录设备列表"""
        # 返回当前 token 对应的设备信息
        # 在实际应用中，这里应该查询数据库中的 Session 表
        import uuid

        current_token = request.auth
        sessions = []

        # 获取当前设备信息
        user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')
        ip_address = self.get_client_ip(request)

        sessions.append({
            "id": str(current_token) if current_token else "current",
            "device": self.parse_user_agent(user_agent),
            "location": f"{ip_address}",
            "last_active": timezone.now().isoformat(),
            "current": True,
        })

        return Response(
            {
                "code": 200,
                "message": "获取成功",
                "data": {"sessions": sessions},
            },
            status=status.HTTP_200_OK,
        )

    def delete(self, request, session_id=None):
        """退出指定设备"""
        if session_id == "current" or not session_id:
            return Response(
                {"code": 400, "message": "无法退出当前设备"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 在实际应用中，这里应该从数据库中删除对应的 Session
        # 并将对应的 JWT Token 加入黑名单

        return Response(
            {"code": 200, "message": "设备已退出登录"},
            status=status.HTTP_200_OK,
        )

    def get_client_ip(self, request):
        """获取客户端 IP 地址"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR', 'Unknown')
        return ip

    def parse_user_agent(self, user_agent):
        """解析 User-Agent 字符串"""
        if not user_agent:
            return "Unknown Device"

        if 'Windows' in user_agent:
            return "Windows PC"
        elif 'Macintosh' in user_agent:
            return "Mac"
        elif 'Linux' in user_agent:
            return "Linux PC"
        elif 'Android' in user_agent:
            # 提取 Android 版本
            import re
            match = re.search(r'Android (\d+)', user_agent)
            if match:
                return f"Android {match.group(1)}"
            return "Android Device"
        elif 'iPhone' in user_agent:
            return "iPhone"
        elif 'iPad' in user_agent:
            return "iPad"
        else:
            return "Unknown Device"


class StorageView(APIView):
    """
    存储统计视图

    GET /api/auth/storage/ - 获取存储使用统计
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """获取用户存储使用统计"""
        from .models import Profile
        from apps.notes.models import Note
        from apps.attachments.models import Attachment

        # 获取用户统计数据
        try:
            profile = Profile.objects.get(user=request.user)
            notes_count = profile.notes_count
        except Profile.DoesNotExist:
            notes_count = Note.objects.filter(user=request.user).count()

        # 统计附件大小
        attachments = Attachment.objects.filter(user=request.user)
        attachments_size = attachments.aggregate(
            total_size=Count('file')
        )['total_size'] or 0

        # 统计笔记中的图片（简化处理）
        notes_with_images = Note.objects.filter(
            user=request.user,
            content__contains='<img'
        ).count()

        return Response(
            {
                "code": 200,
                "message": "获取成功",
                "data": {
                    "notes_count": notes_count,
                    "notes_size": notes_count * 2,  # 估算：每条笔记约 2KB
                    "attachments_count": attachments.count(),
                    "attachments_size": attachments_size,
                    "images_count": notes_with_images,
                    "images_size": notes_with_images * 100,  # 估算
                    "total_size": (notes_count * 2) + attachments_size + (notes_with_images * 100),
                },
            },
            status=status.HTTP_200_OK,
        )


class ExportView(APIView):
    """
    数据导出视图

    GET /api/auth/export/ - 导出用户数据
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """导出用户的所有数据"""
        from .models import Profile
        from apps.notes.models import Note
        from apps.categories.models import Category
        from apps.tags.models import Tag

        user = request.user

        # 收集用户数据
        data = {
            "exported_at": timezone.now().isoformat(),
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "bio": user.bio,
                "avatar": str(user.avatar) if user.avatar else None,
                "created_at": user.created_at.isoformat() if user.created_at else None,
            },
            "preferences": None,
            "notes": [],
            "categories": [],
            "tags": [],
        }

        # 获取偏好设置
        try:
            profile = getattr(user, 'profile', None)
            if profile:
                data["preferences"] = {
                    "theme": profile.theme,
                    "language": profile.language,
                    "timezone": profile.timezone,
                }
        except Exception:
            pass

        # 获取笔记
        notes = Note.objects.filter(user=user).values(
            'id', 'title', 'content', 'is_archived', 'is_pinned',
            'category_id', 'created_at', 'updated_at'
        )
        data["notes"] = list(notes)

        # 获取分类
        categories = Category.objects.filter(user=user).values(
            'id', 'name', 'description', 'parent_id', 'tree_id', 'level',
            'created_at', 'updated_at'
        )
        data["categories"] = list(categories)

        # 获取标签
        tags = Tag.objects.filter(user=user).values(
            'id', 'name', 'color', 'created_at'
        )
        data["tags"] = list(tags)

        # 计算笔记中引用的标签（需要反查关联表）
        from apps.notes.models import NoteTags
        note_tags = NoteTags.objects.filter(
            note_id__in=[n['id'] for n in notes]
        ).values('note_id', 'tag_id')

        data["note_tags"] = list(note_tags)

        return Response(
            {
                "code": 200,
                "message": "导出成功",
                "data": data,
            },
            status=status.HTTP_200_OK,
        )


class DeleteAccountView(APIView):
    """
    账户删除视图

    DELETE /api/auth/account/ - 删除账户
    """

    permission_classes = [IsAuthenticated]

    def delete(self, request):
        """删除用户账户"""
        password = request.data.get('password')

        if not password:
            return Response(
                {"code": 400, "message": "请提供当前密码"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 验证密码
        if not request.user.check_password(password):
            return Response(
                {"code": 400, "message": "密码不正确"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = request.user
        user_id = user.id

        # 退出登录（使 token 失效）
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
        except Exception:
            pass

        # 删除用户数据（级联删除由模型定义处理）
        user.delete()

        return Response(
            {"code": 200, "message": "账户已成功删除"},
            status=status.HTTP_200_OK,
        )
