"""
自定义异常模块
"""

from rest_framework.views import exception_handler
from rest_framework.exceptions import (
    AuthenticationFailed,
    NotAuthenticated,
    PermissionDenied,
    NotFound,
    ValidationError,
    ParseError,
    MethodNotAllowed,
    Throttled,
)
from django.core.exceptions import (
    ValidationError as DjangoValidationError,
    PermissionDenied as DjangoPermissionDenied,
    ObjectDoesNotExist,
)
from django.http import Http404


class APIException(Exception):
    """
    自定义 API 异常基类
    """

    status_code = 400
    default_message = "请求处理失败"
    error_code = "API_ERROR"

    def __init__(self, message=None, error_code=None, details=None):
        self.message = message or self.default_message
        self.error_code = error_code or self.error_code
        self.details = details
        super().__init__(self.message)


class BadRequestException(APIException):
    """400 - 错误请求"""

    status_code = 400
    default_message = "请求参数错误"
    error_code = "BAD_REQUEST"


class UnauthorizedException(APIException):
    """401 - 未授权"""

    status_code = 401
    default_message = "未登录或登录已过期"
    error_code = "UNAUTHORIZED"


class ForbiddenException(APIException):
    """403 - 禁止访问"""

    status_code = 403
    default_message = "没有权限访问此资源"
    error_code = "FORBIDDEN"


class NotFoundException(APIException):
    """404 - 资源不存在"""

    status_code = 404
    default_message = "请求的资源不存在"
    error_code = "NOT_FOUND"


class ConflictException(APIException):
    """409 - 资源冲突"""

    status_code = 409
    default_message = "资源冲突"
    error_code = "CONFLICT"


class UnprocessableEntityException(APIException):
    """422 - 无法处理"""

    status_code = 422
    default_message = "请求参数验证失败"
    error_code = "UNPROCESSABLE_ENTITY"


class InternalServerErrorException(APIException):
    """500 - 服务器内部错误"""

    status_code = 500
    default_message = "服务器内部错误"
    error_code = "INTERNAL_SERVER_ERROR"


def custom_exception_handler(exc, context):
    """
    自定义异常处理器

    Args:
        exc: 异常实例
        context: 上下文信息

    Returns:
        Response 对象
    """
    # 调用 DRF 默认处理器
    response = exception_handler(exc, context)

    if response is not None:
        # 统一响应格式
        error_data = {
            "code": response.status_code,
            "message": get_error_message(response),
            "errors": get_error_details(response),
        }
        response.data = error_data
        return response

    # 处理 Django 异常
    if isinstance(exc, ObjectDoesNotExist):
        return create_error_response(NotFoundException("对象不存在"))

    if isinstance(exc, Http404):
        return create_error_response(NotFoundException("资源不存在"))

    if isinstance(exc, DjangoPermissionDenied):
        return create_error_response(ForbiddenException(str(exc)))

    if isinstance(exc, DjangoValidationError):
        return create_error_response(UnprocessableEntityException(details=exc.messages))

    # 处理自定义异常
    if isinstance(exc, APIException):
        return create_error_response(exc)

    # 未处理的异常
    return create_error_response(InternalServerErrorException(details=str(exc)))


def get_error_message(response):
    """获取错误消息"""
    if hasattr(response, "data"):
        if isinstance(response.data, dict):
            return response.data.get(
                "message", get_status_message(response.status_code)
            )
        elif isinstance(response.data, list) and len(response.data) > 0:
            return str(response.data[0])
    return get_status_message(response.status_code)


def get_error_details(response):
    """获取错误详情"""
    if hasattr(response, "data"):
        if isinstance(response.data, dict):
            return response.data.get("errors", None)
        elif isinstance(response.data, list):
            return response.data
    return None


def get_status_message(status_code):
    """根据状态码获取默认消息"""
    messages = {
        400: "请求参数错误",
        401: "未登录或登录已过期",
        403: "没有权限访问此资源",
        404: "请求的资源不存在",
        405: "请求方法不允许",
        422: "请求参数验证失败",
        429: "请求过于频繁，请稍后再试",
        500: "服务器内部错误",
    }
    return messages.get(status_code, "请求处理失败")


def create_error_response(exception):
    """创建错误响应"""
    from rest_framework.response import Response

    return Response(
        {
            "code": exception.status_code,
            "message": exception.message,
            "errors": exception.details,
        },
        status=exception.status_code,
    )
