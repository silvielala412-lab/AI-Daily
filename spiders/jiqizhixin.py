# -*- coding: utf-8 -*-
"""
机器之心爬虫
- 列表: 使用官方 JSON API (https://www.jiqizhixin.com/api/article_library/articles.json)
- 正文: 使用 requests 直接抓取文章页面，解析 .detail__info-body
  (放弃已被拦截的单篇 JSON API 和 Playwright persistent context)
"""

import re
import time
import requests
import parsel
from config.settings import HEADERS_JIQIZHIXIN, REQUEST_TIMEOUT
from spiders.base import BaseSpider
from core.network import request_url


class JiqizhixinSpider(BaseSpider):
    def __init__(self):
        self.name = "机器之心"
        self.list_url = "https://www.jiqizhixin.com/api/article_library/articles.json?page=1&per=20"

    def _clean_html_to_text(self, html_content):
        """从 HTML 中提取纯文本"""
        if not html_content:
            return ""
        text = re.sub(r"<[^>]+>", " ", html_content)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def _parse_detail_page(self, slug, cover_fallback=""):
        """
        直接 requests 抓取文章页面，解析正文区域。
        单篇 JSON API 已被服务器拦截（返回 HTML），因此完全跳过。
        """
        page_url = f"https://www.jiqizhixin.com/articles/{slug}"
        try:
            resp = requests.get(page_url, headers=HEADERS_JIQIZHIXIN, timeout=REQUEST_TIMEOUT)
            resp.raise_for_status()
            html = resp.text
        except Exception as e:
            print(f"  [机器之心] 页面抓取失败 {slug}: {e}")
            return None

        selector = parsel.Selector(html)

        # 正文 HTML：优先 .detail__info-body，备选常见容器
        body_html = (
            selector.css(".detail__info-body").get()
            or selector.css("article.article").get()
            or selector.css(".article-content").get()
            or ""
        )

        # 封面图：优先 og:image，备选 .detail__cover
        cover_img = (
            selector.css('meta[property="og:image"]::attr(content)').get()
            or selector.css(".detail__cover img::attr(src)").get()
            or cover_fallback
        )

        return {
            "cover": cover_img,
            "html": body_html,
            "text": self._clean_html_to_text(body_html)
        }

    def run(self):
        # 1. 列表 API（验证可用）
        data = request_url(self.list_url, headers=HEADERS_JIQIZHIXIN, is_json=True)
        if not data or not data.get("success"):
            return []

        results = []
        articles = data.get("articles", [])

        for art in articles:
            # 仅抓取机器之心原创/首发
            if art.get("source") != "机器之心":
                continue

            title = art.get("title", "")
            slug = art.get("slug")
            if not slug:
                continue

            # 时间格式 "2026/05/06 17:03" → "2026-05-06"
            raw_date = art.get("publishedAt", "")
            try:
                date = raw_date.split(" ")[0].replace("/", "-")
            except Exception:
                date = time.strftime("%Y-%m-%d")

            # 列表 API 中的封面图和摘要（作为降级用）
            cover_fallback = art.get("coverImageUrl", "") or art.get("cover_image_url", "") or ""
            snippet = art.get("content", "")
            link = f"https://www.jiqizhixin.com/articles/{slug}"

            # 2. 抓取详情页
            details = self._parse_detail_page(slug, cover_fallback=cover_fallback)
            if details and details["text"]:
                results.append({
                    "source": self.name,
                    "title": title,
                    "publish_date": date,
                    "cover_image": details["cover"] or cover_fallback,
                    "content_text": details["text"],
                    "content_html": details["html"],
                    "original_link": link
                })
            else:
                # 降级：使用列表中的摘要
                results.append({
                    "source": self.name,
                    "title": title,
                    "publish_date": date,
                    "cover_image": cover_fallback,
                    "content_text": snippet,
                    "content_html": f"<p>{snippet}</p>",
                    "original_link": link
                })

            time.sleep(0.5)  # 礼貌延迟

        return results
