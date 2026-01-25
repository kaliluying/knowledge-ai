"""
统一 API 响应格式模块
"""


class ResponseModel:
    """
    统一 API 响应模型

    响应格式:
    {
        "code": 200,
        "message": "success",
        "data": {...}
    }
    """

    def __init__(self, code=200, message="success", data=None, errors=None):
        self.code = code
        self.message = message
        self.data = data
        self.errors = errors

    def to_dict(self):
        """转换为字典格式"""
        response = {
            "code": self.code,
            "message": self.message,
        }
        if self.data is not None:
            response["data"] = self.data
        if self.errors is not None:
            response["errors"] = self.errors
        return response

    @classmethod
    def success(cls, data=None, message="success"):
        """成功响应"""
        return cls(code=200, message=message, data=data)

    @classmethod
    def created(cls, data=None, message="created"):
        """创建成功响应"""
        return cls(code=201, message=message, data=data)

    @classmethod
    def error(cls, message="error", code=400, errors=None):
        """错误响应"""
        return cls(code=code, message=message, errors=errors)

    @classmethod
    def not_found(cls, message="resource not found"):
        """资源不存在"""
        return cls(code=404, message=message)

    @classmethod
    def validation_error(cls, message="validation error", errors=None):
        """验证错误"""
        return cls(code=422, message=message, errors=errors)

    @classmethod
    def unauthorized(cls, message="unauthorized"):
        """未授权"""
        return cls(code=401, message=message)

    @classmethod
    def forbidden(cls, message="forbidden"):
        """禁止访问"""
        return cls(code=403, message=message)

    @classmethod
    def server_error(cls, message="internal server error"):
        """服务器错误"""
        return cls(code=500, message=message)


def success_response(data=None, message="success"):
    """
    快捷成功响应

    Args:
        data: 响应数据
        message: 响应消息

    Returns:
        ResponseModel 实例
    """
    return ResponseModel.success(data=data, message=message)


def error_response(message="error", code=400, errors=None):
    """
    快捷错误响应

    Args:
        message: 错误消息
        code: 状态码
        errors: 详细错误信息

    Returns:
        ResponseModel 实例
    """
    return ResponseModel.error(message=message, code=code, errors=errors)
