"""
工具函数模块
"""

import re
import uuid
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.cache import cache


def generate_uuid():
    """生成 UUID 字符串"""
    return str(uuid.uuid4())


def generate_short_uuid(length=8):
    """生成短 UUID"""
    return uuid.uuid4().hex[:length]


def slugify_text(text):
    """
    将文本转换为 URL 友好的 slug 格式

    Args:
        text: 原始文本

    Returns:
        slug 格式字符串
    """
    # 移除非字母数字字符
    text = re.sub(r"[^\w\s-]", "", text)
    # 转换为小写
    text = text.lower()
    # 替换空格为连字符
    text = re.sub(r"[\s_-]+", "-", text)
    # 移除首尾连字符
    text = text.strip("-")
    return text


def truncate_text(text, max_length, suffix="..."):
    """
    截断文本

    Args:
        text: 原始文本
        max_length: 最大长度
        suffix: 截断后缀

    Returns:
        截断后的文本
    """
    if len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)] + suffix


def format_datetime(dt, format="%Y-%m-%d %H:%M:%S"):
    """
    格式化日期时间

    Args:
        dt: 日期时间对象
        format: 格式字符串

    Returns:
        格式化后的日期时间字符串
    """
    if isinstance(dt, str):
        return dt
    return dt.strftime(format)


def time_ago(dt):
    """
    计算时间差，返回相对时间描述

    Args:
        dt: 日期时间对象

    Returns:
        相对时间描述，如 "3分钟前"、"2天前"
    """
    if isinstance(dt, str):
        dt = datetime.fromisoformat(dt.replace("Z", "+00:00"))

    now = timezone.now()
    delta = now - dt

    if delta < timedelta(minutes=1):
        return "刚刚"
    elif delta < timedelta(hours=1):
        minutes = int(delta.total_seconds() / 60)
        return f"{minutes}分钟前"
    elif delta < timedelta(days=1):
        hours = int(delta.total_seconds() / 3600)
        return f"{hours}小时前"
    elif delta < timedelta(days=7):
        days = int(delta.total_seconds() / 86400)
        return f"{days}天前"
    elif delta < timedelta(days=30):
        weeks = int(delta.total_seconds() / 604800)
        return f"{weeks}周前"
    elif delta < timedelta(days=365):
        months = int(delta.total_seconds() / 2592000)
        return f"{months}个月前"
    else:
        years = int(delta.total_seconds() / 31536000)
        return f"{years}年前"


def get_cache_key(*args):
    """
    生成缓存键

    Args:
        *args: 缓存键组成部分

    Returns:
        缓存键字符串
    """
    return ":".join(str(arg) for arg in args)


def cache_data(key, data, timeout=3600):
    """
    缓存数据

    Args:
        key: 缓存键
        data: 要缓存的数据
        timeout: 过期时间（秒）
    """
    cache.set(key, data, timeout)


def get_cached_data(key):
    """
    获取缓存数据

    Args:
        key: 缓存键

    Returns:
        缓存的数据，不存在返回 None
    """
    return cache.get(key)


def delete_cache(key):
    """
    删除缓存

    Args:
        key: 缓存键
    """
    cache.delete(key)


def clear_cache_pattern(pattern):
    """
    清除匹配模式的所有缓存

    Args:
        pattern: 缓存键模式
    """
    cache.delete_pattern(f"*{pattern}*")


class DateRange:
    """
    日期范围工具类
    """

    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date

    @classmethod
    def today(cls):
        """今天"""
        today = timezone.now().date()
        return cls(today, today)

    @classmethod
    def this_week(cls):
        """本周"""
        today = timezone.now().date()
        start = today - timedelta(days=today.weekday())
        return cls(start, today)

    @classmethod
    def this_month(cls):
        """本月"""
        today = timezone.now().date()
        start = today.replace(day=1)
        return cls(start, today)

    @classmethod
    def last_n_days(cls, n):
        """最近 n 天"""
        today = timezone.now().date()
        start = today - timedelta(days=n - 1)
        return cls(start, today)

    def to_dict(self):
        """转换为字典"""
        return {
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
        }
