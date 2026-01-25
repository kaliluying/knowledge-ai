"""
用户视图模块
"""

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

from .serializers import (
    UserCreateSerializer,
    UserSerializer,
    LoginSerializer,
    PasswordChangeSerializer,
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
        serializer.is_valid(raise_exception=True)
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
        except Exception as e:
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
        serializer = UserSerializer(request.user)
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
        serializer = UserSerializer(request.user, data=request.data, partial=True)
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
