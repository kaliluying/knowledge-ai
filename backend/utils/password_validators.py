"""
自定义密码验证器
"""

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class StrongPasswordValidator:
    """
    强密码验证器

    要求密码必须包含：
    - 至少8个字符
    - 至少一个大写字母
    - 至少一个小写字母
    - 至少一个数字
    - 至少一个特殊字符
    """

    def __init__(self, min_length=8):
        self.min_length = min_length

    def validate(self, password, user=None):
        errors = []

        # 检查长度
        if len(password) < self.min_length:
            errors.append(
                ValidationError(
                    _("密码长度至少 %(min_length)d 个字符"),
                    code="password_too_short",
                    params={"min_length": self.min_length},
                )
            )

        # 检查大写字母
        if not any(c.isupper() for c in password):
            errors.append(
                ValidationError(
                    _("密码必须包含至少一个大写字母"),
                    code="password_no_upper",
                )
            )

        # 检查小写字母
        if not any(c.islower() for c in password):
            errors.append(
                ValidationError(
                    _("密码必须包含至少一个小写字母"),
                    code="password_no_lower",
                )
            )

        # 检查数字
        if not any(c.isdigit() for c in password):
            errors.append(
                ValidationError(
                    _("密码必须包含至少一个数字"),
                    code="password_no_digit",
                )
            )

        # 检查特殊字符
        if not any(not c.isalnum() for c in password):
            errors.append(
                ValidationError(
                    _("密码必须包含至少一个特殊字符"),
                    code="password_no_special",
                )
            )

        if errors:
            raise ValidationError(errors)

    def get_help_text(self):
        return _(
            "密码必须包含至少 %(min_length)d 个字符，"
            "一个大写字母，一个小写字母，一个数字和一个特殊字符"
        ) % {"min_length": self.min_length}
