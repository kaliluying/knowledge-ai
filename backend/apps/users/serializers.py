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

    def validate_email(self, value):
        """
        验证邮箱是否已被注册
        """
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("该邮箱已被注册")
        return value

    def validate_username(self, value):
        """
        验证用户名是否已被使用
        """
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("该用户名已被使用")
        return value

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

    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "avatar",
            "avatar_url",
            "bio",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "email", "created_at", "updated_at"]

    def get_avatar_url(self, obj):
        """返回完整的头像URL"""
        if obj.avatar:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.avatar.url)
            return obj.avatar.url
        return obj.avatar_url or None

    def to_representation(self, instance):
        """自定义序列化输出"""
        data = super().to_representation(instance)
        # 确保 avatar 字段返回完整URL
        if instance.avatar:
            request = self.context.get('request')
            if request:
                data['avatar'] = request.build_absolute_uri(instance.avatar.url)
        return data


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


class PasswordResetSerializer(serializers.Serializer):
    """
    密码重置请求序列化器

    用于发送密码重置邮件
    """

    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        """
        验证邮箱是否已注册
        """
        from django.contrib.auth import get_user_model

        User = get_user_model()
        if not User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("该邮箱未注册")
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    密码重置确认序列化器

    用于设置新密码
    """

    token = serializers.CharField(required=True)
    new_password = serializers.CharField(
        required=True,
        validators=[validate_password],
        style={"input_type": "password"},
    )
    new_password_confirm = serializers.CharField(
        required=True,
        style={"input_type": "password"},
    )

    def validate(self, attrs):
        """
        验证两次密码是否一致
        """
        if attrs["new_password"] != attrs["new_password_confirm"]:
            raise serializers.ValidationError(
                {"new_password_confirm": "两次输入的密码不一致"}
            )
        return attrs


class PreferencesSerializer(serializers.ModelSerializer):
    """
    用户偏好设置序列化器
    """

    class Meta:
        from .models import Profile
        model = Profile
        fields = [
            "theme",
            "language",
            "timezone",
        ]
