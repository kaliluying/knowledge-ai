"""
URL抓取服务模块

提供网页内容抓取功能，使用 BeautifulSoup 解析 HTML
"""

import re
from typing import Dict, Optional
from urllib.parse import urlparse, urljoin

import requests
from bs4 import BeautifulSoup
from django.core.exceptions import ValidationError

from utils.ssrf_validator import validate_url


class URLScraperService:
    """
    URL 网页内容抓取服务

    提供网页标题、描述、正文、图片等信息的提取功能
    """

    def __init__(self, timeout: int = 30):
        """
        初始化抓取服务

        Args:
            timeout: 请求超时时间（秒）
        """
        self.timeout = timeout
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,"
            "image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        }

    def scrape(self, url: str) -> Dict:
        """
        抓取网页内容

        Args:
            url: 要抓取的网页 URL

        Returns:
            包含抓取结果的字典，包含以下键：
            - success: 是否成功
            - title: 网页标题
            - description: 网页描述
            - content: 网页正文内容
            - html_content: 原始 HTML 内容
            - favicon: 网站图标 URL
            - image: Open Graph 图片 URL
            - error: 错误信息（失败时）
        """
        try:
            # SSRF 防护：验证 URL 是否安全
            validate_url(url)

            response = requests.get(
                url, headers=self.headers, timeout=self.timeout, allow_redirects=True
            )
            response.raise_for_status()

            # 设置编码
            if response.encoding == "ISO-8859-1":
                response.encoding = response.apparent_encoding

            soup = BeautifulSoup(response.text, "html.parser")

            # 提取标题
            title = self._extract_title(soup)

            # 提取描述
            description = self._extract_description(soup)

            # 提取正文内容
            content = self._extract_content(soup)

            # 提取 favicon
            favicon = self._extract_favicon(soup, url)

            # 提取 Open Graph 图片
            image = self._extract_og_image(soup)

            return {
                "success": True,
                "title": title,
                "description": description,
                "content": content,
                "html_content": response.text,
                "favicon": favicon,
                "image": image,
            }

        except requests.exceptions.Timeout:
            return {"success": False, "error": "请求超时"}
        except requests.exceptions.HTTPError as e:
            return {"success": False, "error": f"HTTP 错误：{str(e)}"}
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": f"请求失败：{str(e)}"}
        except Exception as e:
            return {"success": False, "error": f"解析失败：{str(e)}"}

    def _extract_title(self, soup: BeautifulSoup) -> str:
        """提取网页标题"""
        # 优先尝试 Open Graph 标题
        og_title = soup.find("meta", property="og:title")
        if og_title and og_title.get("content"):
            return og_title["content"].strip()

        # 其次尝试 Twitter 标题
        twitter_title = soup.find("meta", attrs={"name": "twitter:title"})
        if twitter_title and twitter_title.get("content"):
            return twitter_title["content"].strip()

        # 最后使用 HTML 标题
        title_tag = soup.find("title")
        if title_tag:
            return title_tag.get_text().strip()

        return ""

    def _extract_description(self, soup: BeautifulSoup) -> str:
        """提取网页描述"""
        # 优先尝试 Open Graph 描述
        og_desc = soup.find("meta", property="og:description")
        if og_desc and og_desc.get("content"):
            return og_desc["content"].strip()

        # 其次尝试 Meta description
        meta_desc = soup.find("meta", attrs={"name": "description"})
        if meta_desc and meta_desc.get("content"):
            return meta_desc["content"].strip()

        # 最后尝试 Twitter 描述
        twitter_desc = soup.find("meta", attrs={"name": "twitter:description"})
        if twitter_desc and twitter_desc.get("content"):
            return twitter_desc["content"].strip()

        return ""

    def _extract_content(self, soup: BeautifulSoup) -> str:
        """
        提取网页正文内容

        尝试移除脚本、样式、导航等非正文内容
        """
        # 移除不需要的元素
        for tag in soup(
            ["script", "style", "nav", "header", "footer", "aside", "noscript"]
        ):
            tag.decompose()

        # 尝试查找文章主体
        article = soup.find("article")
        if article:
            return article.get_text(separator="\n", strip=True)

        # 尝试查找 main 内容区域
        main = soup.find("main")
        if main:
            return main.get_text(separator="\n", strip=True)

        # 使用 body
        body = soup.find("body")
        if body:
            text = body.get_text(separator="\n", strip=True)

            # 清理多余空白
            lines = (line.strip() for line in text.splitlines())
            non_empty_lines = [line for line in lines if line]

            return "\n".join(non_empty_lines)

        return ""

    def _extract_favicon(self, soup: BeautifulSoup, original_url: str) -> Optional[str]:
        """
        提取网站图标

        尝试多种方法获取 favicon
        """
        base_url = urlparse(original_url)

        # 方法1：查找 rel="icon" 或 rel="shortcut icon"
        icon = soup.find("link", rel=re.compile(r"icon", re.I))
        if icon and icon.get("href"):
            href = icon["href"]
            return self._resolve_url(href, original_url)

        # 方法2：查找 rel="apple-touch-icon"
        apple_icon = soup.find("link", rel=re.compile(r"apple-touch-icon", re.I))
        if apple_icon and apple_icon.get("href"):
            href = apple_icon["href"]
            return self._resolve_url(href, original_url)

        # 方法3：默认查找 /favicon.ico
        return f"{base_url.scheme}://{base_url.netloc}/favicon.ico"

    def _extract_og_image(self, soup: BeautifulSoup) -> Optional[str]:
        """
        提取 Open Graph 图片
        """
        og_image = soup.find("meta", property="og:image")
        if og_image and og_image.get("content"):
            return og_image["content"]

        twitter_image = soup.find("meta", attrs={"name": "twitter:image"})
        if twitter_image and twitter_image.get("content"):
            return twitter_image["content"]

        return None

    def _resolve_url(self, href: str, original_url: str) -> str:
        """
        解析相对 URL 为绝对 URL

        Args:
            href: 相对或绝对 URL
            original_url: 原始 URL（用于解析相对路径）

        Returns:
            绝对 URL
        """
        if not href:
            return ""

        parsed = urlparse(original_url)

        if href.startswith("//"):
            return f"{parsed.scheme}:{href}"

        if href.startswith("/"):
            return f"{parsed.scheme}://{parsed.netloc}{href}"

        if href.startswith("http://") or href.startswith("https://"):
            return href

        # 相对路径
        return urljoin(original_url, href)
