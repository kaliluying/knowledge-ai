"""
用户测试模块

包含用户认证模块的单元测试和 API 测试。
"""

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


@pytest.fixture
def api_client():
    """创建 API 客户端"""
    return APIClient()


@pytest.fixture
def test_user(db):
    """创建测试用户"""
    return User.objects.create_user(
        email="test@example.com",
        username="testuser",
        password="testpass123",
    )


@pytest.fixture
def authenticated_client(api_client, test_user):
    """创建已认证的 API 客户端"""
    api_client.force_authenticate(user=test_user)
    return api_client


class TestUserModel:
    """用户模型单元测试"""

    def test_create_user_with_email(self, db):
        """测试使用邮箱创建用户"""
        email = "user@example.com"
        password = "testpass123"
        user = User.objects.create_user(
            email=email,
            username="testuser",
            password=password,
        )

        assert user.email == email
        assert user.username == "testuser"
        assert user.check_password(password)

    def test_create_user_without_email_raises_error(self, db):
        """测试无邮箱创建用户会报错"""
        with pytest.raises(ValueError):
            User.objects.create_user(
                email="",
                username="testuser",
                password="testpass123",
            )

    def test_create_user_normalizes_email(self, db):
        """测试用户邮箱会被规范化"""
        email = "Test@Example.COM"
        user = User.objects.create_user(
            email=email,
            username="testuser",
            password="testpass123",
        )
        assert user.email == email.lower()

    def test_create_superuser(self, db):
        """测试创建超级用户"""
        user = User.objects.create_superuser(
            email="admin@example.com",
            username="admin",
            password="adminpass123",
        )
        assert user.is_staff is True
        assert user.is_superuser is True


class TestUserAPI:
    """用户 API 测试"""

    def test_register_user(self, api_client):
        """测试用户注册 API"""
        url = reverse("user-register")
        data = {
            "email": "newuser@example.com",
            "username": "newuser",
            "password": "newpass123",
            "password_confirm": "newpass123",
        }
        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(email=data["email"]).exists()

    def test_register_user_invalid_data(self, api_client):
        """测试无效数据注册"""
        url = reverse("user-register")
        data = {
            "email": "invalid-email",
            "username": "",
            "password": "short",
        }
        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_login_user(self, api_client, test_user):
        """测试用户登录 API"""
        url = reverse("user-login")
        data = {
            "email": "test@example.com",
            "password": "testpass123",
        }
        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data["data"]
        assert "refresh" in response.data["data"]

    def test_login_user_invalid_credentials(self, api_client, test_user):
        """测试无效凭据登录"""
        url = reverse("user-login")
        data = {
            "email": "test@example.com",
            "password": "wrongpassword",
        }
        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_user_profile(self, api_client, authenticated_client):
        """测试获取用户资料"""
        url = reverse("user-profile")
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["data"]["email"] == "test@example.com"

    def test_update_user_profile(self, api_client, authenticated_client):
        """测试更新用户资料"""
        url = reverse("user-profile")
        data = {
            "username": "updateduser",
            "bio": "This is my bio",
        }
        response = authenticated_client.put(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["data"]["username"] == "updateduser"

    def test_change_password(self, api_client, authenticated_client, test_user):
        """测试修改密码"""
        url = reverse("user-change-password")
        data = {
            "old_password": "testpass123",
            "new_password": "newpass456",
        }
        response = authenticated_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK

        # 验证新密码可用
        test_user.refresh_from_db()
        assert test_user.check_password("newpass456")

    def test_change_password_wrong_old(self, api_client, authenticated_client):
        """测试错误旧密码修改密码"""
        url = reverse("user-change-password")
        data = {
            "old_password": "wrongpassword",
            "new_password": "newpass456",
        }
        response = authenticated_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_logout_user(self, api_client, authenticated_client):
        """测试用户登出"""
        url = reverse("user-logout")
        response = authenticated_client.post(url)

        assert response.status_code == status.HTTP_200_OK

    def test_refresh_token(self, api_client, test_user):
        """测试刷新 Token"""
        # 先登录获取 refresh token
        login_url = reverse("user-login")
        login_data = {
            "email": "test@example.com",
            "password": "testpass123",
        }
        login_response = api_client.post(login_url, login_data, format="json")
        refresh_token = login_response.data["data"]["refresh"]

        # 使用 refresh token 获取新的 access token
        refresh_url = reverse("user-refresh")
        refresh_data = {"refresh": refresh_token}
        response = api_client.post(refresh_url, refresh_data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data["data"]

    def test_unauthenticated_access_denied(self, api_client):
        """测试未认证访问被拒绝"""
        url = reverse("user-profile")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestUserEmailValidation:
    """用户邮箱验证测试"""

    def test_duplicate_email_not_allowed(self, api_client, test_user):
        """测试重复邮箱不被允许"""
        url = reverse("user-register")
        data = {
            "email": test_user.email,  # 使用已存在的邮箱
            "username": "newuser",
            "password": "newpass123",
            "password_confirm": "newpass123",
        }
        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_duplicate_username_not_allowed(self, api_client, test_user):
        """测试重复用户名不被允许"""
        url = reverse("user-register")
        data = {
            "email": "newuser@example.com",
            "username": test_user.username,  # 使用已存在的用户名
            "password": "newpass123",
            "password_confirm": "newpass123",
        }
        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
