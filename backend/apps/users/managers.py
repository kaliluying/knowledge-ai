"""
用户管理器模块
"""

from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """
    自定义用户管理器

    支持使用邮箱登录，替代默认的用户名登录
    """

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        内部方法：创建用户
        """
        if not email:
            raise ValueError(_("邮箱地址不能为空"))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """
        创建普通用户
        """
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        创建超级管理员
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("超级管理员必须设置 is_staff=True"))

        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("超级管理员必须设置 is_superuser=True"))

        return self._create_user(email, password, **extra_fields)

    def create(self, email, password=None, **extra_fields):
        """
        兼容 create_user 方法
        """
        return self.create_user(email, password, **extra_fields)
