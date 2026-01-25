"""
用户序列化器模块
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import User

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    """
    用户注册序列化器
    """

    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={"input_type": "password"},
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
    )

    class Meta:
        model = User
        fields = [
            "email",
            "username",
            "password",
            "password_confirm",
        ]

    def validate(self, attrs):
        """
        验证两次密码是否一致
        """
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError(
                {"password_confirm": "两次输入的密码不一致"}
            )
        return attrs

    def create(self, validated_data):
        """
        创建用户
        """
        validated_data.pop("password_confirm")
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    """
    用户详情序列化器
    """

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "avatar",
            "bio",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "email", "created_at", "updated_at"]


class UserListSerializer(serializers.ModelSerializer):
    """
    用户列表序列化器（精简版）
    """

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "avatar",
        ]


class LoginSerializer(serializers.Serializer):
    """
    用户登录序列化器
    """

    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={"input_type": "password"},
    )


class TokenResponseSerializer(serializers.Serializer):
    """
    Token 响应序列化器
    """

    access = serializers.CharField()
    refresh = serializers.CharField()
    user = UserSerializer()


class PasswordChangeSerializer(serializers.Serializer):
    """
    密码修改序列化器
    """

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(
        required=True,
        validators=[validate_password],
        style={"input_type": "password"},
    )

    def validate_old_password(self, value):
        """
        验证旧密码
        """
        user = self.context.get("request").user
        if not user.check_password(value):
            raise serializers.ValidationError("旧密码不正确")
        return value
