"""
速率限制中间件
"""

import logging
from django.core.cache import cache
from django.http import JsonResponse

logger = logging.getLogger(__name__)


class RateLimitMiddleware:
    """
    简单的速率限制中间件

    限制：
    - 登录请求：5次/分钟
    - API请求：100次/分钟
    - 注册请求：3次/小时
    """

    LOGIN_LIMIT = 5  # 5次/分钟
    API_LIMIT = 100  # 100次/分钟
    REGISTER_LIMIT = 3  # 3次/小时

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 获取客户端IP
        ip = self.get_client_ip(request)

        # 根据路径选择限制策略
        # 注意：认证相关端点不进行速率限制，避免影响正常使用
        if "/auth/login/" in request.path:
            if self.is_rate_limited(ip, "login", self.LOGIN_LIMIT, 60):
                return JsonResponse(
                    {"code": 429, "message": "请求过于频繁，请稍后再试"}, status=429
                )
        elif "/auth/register/" in request.path:
            if self.is_rate_limited(ip, "register", self.REGISTER_LIMIT, 3600):
                return JsonResponse(
                    {"code": 429, "message": "注册过于频繁，请稍后再试"}, status=429
                )
        elif "/api/" in request.path and "/auth/" not in request.path:
            # 仅对非认证的API请求进行速率限制
            if self.is_rate_limited(ip, "api", self.API_LIMIT, 60):
                return JsonResponse(
                    {"code": 429, "message": "请求过于频繁"}, status=429
                )

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        """获取客户端IP"""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0].strip()
        else:
            ip = request.META.get("REMOTE_ADDR", "unknown")
        return ip

    def is_rate_limited(self, ip, action, limit, timeout):
        """检查是否被限制"""
        key = f"ratelimit:{action}:{ip}"
        current = cache.get(key, 0)

        if current >= limit:
            return True

        try:
            cache.set(key, current + 1, timeout)
        except Exception as e:
            # Log cache error but don't fail the request
            logger.warning(f"Rate limit cache set failed: {e}")
        return False
