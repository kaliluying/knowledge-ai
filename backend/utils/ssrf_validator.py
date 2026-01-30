"""
SSRF 防护模块

提供 URL 白名单验证和内部网络地址检测功能，防止 SSRF 攻击
"""

import os
from typing import List, Optional
from urllib.parse import urlparse
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.utils.translation import gettext_lazy as _


# 默认允许的域名列表
DEFAULT_ALLOWED_DOMAINS = [
    "wikipedia.org",
    "github.com",
    "medium.com",
    "stackoverflow.com",
    "dev.to",
    "blog.bitsrc.io",
    "css-tricks.com",
    "smashingmagazine.com",
    "web.dev",
    "developer.mozilla.org",
]


def get_allowed_domains() -> List[str]:
    """
    获取允许的域名列表

    从环境变量 ALLOWED_SCRAPE_DOMAINS 读取自定义域名列表
    如果未设置，则返回默认域名列表

    Returns:
        允许的域名列表
    """
    env_domains = os.getenv("ALLOWED_SCRAPE_DOMAINS", "")
    if env_domains:
        return [d.strip() for d in env_domains.split(",") if d.strip()]
    return DEFAULT_ALLOWED_DOMAINS


# 私有 IP 地址模式
PRIVATE_IP_PATTERNS = [
    # IPv4 私有地址
    r"^127\.\d{1,3}\.\d{1,3}\.\d{1,3}$",  # 127.0.0.0/8 (localhost)
    r"^192\.168\.\d{1,3}\.\d{1,3}$",  # 192.168.0.0/16
    r"^10\.\d{1,3}\.\d{1,3}\.\d{1,3}$",  # 10.0.0.0/8
    r"^172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}$",  # 172.16.0.0/12
    # IPv6 私有地址
    r"^::1$",  # IPv6 localhost
    r"^fe80:",  # IPv6 link-local
    r"^fc00:",  # IPv6 unique local
]


def is_private_ip(hostname: str) -> bool:
    """
    检查主机名是否为私有 IP 地址

    Args:
        hostname: 主机名或 IP 地址

    Returns:
        如果是私有 IP 返回 True，否则返回 False
    """
    import re

    # 检查是否为回环地址
    if hostname in ("localhost", "127.0.0.1", "::1"):
        return True

    # 检查 IPv4 私有地址模式
    for pattern in PRIVATE_IP_PATTERNS:
        if re.match(pattern, hostname):
            return True

    return False


def is_internal_network(hostname: str) -> bool:
    """
    检查是否为企业内部网络地址

    Args:
        hostname: 主机名

    Returns:
        如果是内部网络地址返回 True，否则返回 False
    """
    # 常见的内部网络域名
    internal_patterns = [
        ".internal",
        ".local",
        ".lan",
        ".intranet",
        ".corp",
        ".localdomain",
    ]

    hostname_lower = hostname.lower()
    for pattern in internal_patterns:
        if hostname_lower.endswith(pattern):
            return True

    return False


class SSRFValidator:
    """
    SSRF 攻击防护验证器

    提供 URL 白名单验证和内部网络检测功能
    """

    def __init__(self, allowed_domains: Optional[List[str]] = None):
        """
        初始化验证器

        Args:
            allowed_domains: 允许的域名列表，None 表示使用默认列表
        """
        self.allowed_domains = allowed_domains or get_allowed_domains()
        self.url_validator = URLValidator()

    def validate(self, url: str) -> None:
        """
        验证 URL 是否安全

        Args:
            url: 要验证的 URL

        Raises:
            ValidationError: URL 不安全时抛出
        """
        # 1. 基本 URL 格式验证
        try:
            self.url_validator(url)
        except ValidationError as e:
            raise ValidationError(
                _("URL 格式无效：%(error)s"),
                params={"error": str(e)},
            )

        # 2. 解析 URL
        parsed = urlparse(url)

        # 3. 检查协议
        if parsed.scheme not in ("http", "https"):
            raise ValidationError(
                _("只允许 HTTP 和 HTTPS 协议"),
            )

        hostname = parsed.hostname
        if not hostname:
            raise ValidationError(
                _("无法解析 URL 主机名"),
            )

        # 4. 检查私有 IP 地址
        if is_private_ip(hostname):
            raise ValidationError(
                _("不允许访问内部 IP 地址"),
            )

        # 5. 检查内部网络
        if is_internal_network(hostname):
            raise ValidationError(
                _("不允许访问内部网络地址"),
            )

        # 6. 检查域名白名单
        if not self._is_domain_allowed(hostname):
            raise ValidationError(
                _("域名 %(domain)s 不在允许列表中"),
                params={"domain": hostname},
            )

    def _is_domain_allowed(self, hostname: str) -> bool:
        """
        检查域名是否在允许列表中

        Args:
            hostname: 主机名

        Returns:
            如果域名允许返回 True，否则返回 False
        """
        hostname_lower = hostname.lower()

        # 检查是否以允许的域名结尾
        for allowed_domain in self.allowed_domains:
            allowed_lower = allowed_domain.lower()
            if hostname_lower == allowed_lower:
                return True
            if hostname_lower.endswith("." + allowed_lower):
                return True

        return False

    def is_safe(self, url: str) -> bool:
        """
        检查 URL 是否安全（不抛出异常）

        Args:
            url: 要检查的 URL

        Returns:
            如果 URL 安全返回 True，否则返回 False
        """
        try:
            self.validate(url)
            return True
        except ValidationError:
            return False


# 创建默认验证器实例
default_validator = SSRFValidator()


def validate_url(url: str) -> None:
    """
    便捷的 URL 验证函数

    Args:
        url: 要验证的 URL

    Raises:
        ValidationError: URL 不安全时抛出
    """
    default_validator.validate(url)


def is_url_safe(url: str) -> bool:
    """
    检查 URL 是否安全的便捷函数

    Args:
        url: 要检查的:
        如果 URL 安全返回 True，否则返回 False
    URL

    Returns"""
    return default_validator.is_safe(url)
