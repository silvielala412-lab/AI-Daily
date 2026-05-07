# -*- coding: utf-8 -*-
"""
机器之心爬虫
- 列表: 官方 JSON API（稳定可用）
- 正文: Playwright 无头模式渲染 JS 页面（纯 CSR 站点，requests 无法获取正文）
  使用普通 launch(headless=True)，无需任何本地 Chrome Profile 路径依赖
"""

import re
import time
from config.settings import HEADERS_JIQIZHIXIN
from spiders.base import BaseSpider
from core.network import request_url


class JiqizhixinSpider(BaseSpider):
    def __init__(self):
        self.name = "机器之心"
        self.list_url = "https://www.jiqizhixin.com/api/article_library/articles.json?page=1&per=20"

    def _clean_html_to_text(self, html_content):
        """从 HTML 提取纯文本"""
        if not html_content:
            return ""
        text = re.sub(r"<[^>]+>", " ", html_content)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def run(self):
        # 1. 获取文章列表（API 正常）
        data = request_url(self.list_url, headers=HEADERS_JIQIZHIXIN, is_json=True)
        if not data or not data.get("success"):
            return []

        articles = data.get("articles", [])
        # 只保留机器之心原创文章，提取需要的基本信息
        targets = []
        for art in articles:
            if art.get("source") != "机器之心":
                continue
            slug = art.get("slug")
            if not slug:
                continue
            raw_date = art.get("publishedAt", "")
            try:
                date = raw_date.split(" ")[0].replace("/", "-")
            except Exception:
                date = time.strftime("%Y-%m-%d")
            targets.append({
                "title": art.get("title", ""),
                "slug": slug,
                "date": date,
                "cover_fallback": art.get("coverImageUrl", "") or art.get("cover_image_url", "") or "",
                "snippet": art.get("content", ""),
                "link": f"https://www.jiqizhixin.com/articles/{slug}",
            })

        if not targets:
            return []

        results = []

        # 2. 用 Playwright 无头模式批量抓取正文（复用单个浏览器实例）
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            # 若 Playwright 未安装，降级为列表摘要
            for t in targets:
                results.append({
                    "source": self.name,
                    "title": t["title"],
                    "publish_date": t["date"],
                    "cover_image": t["cover_fallback"],
                    "content_text": t["snippet"],
                    "content_html": f"<p>{t['snippet']}</p>",
                    "original_link": t["link"],
                })
            return results

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                # 设置额外 headers（带上 Cookie 等）
                extra_http_headers={k: v for k, v in HEADERS_JIQIZHIXIN.items() if k.lower() != "user-agent"}
            )
            page = context.new_page()

            for t in targets:
                try:
                    page.goto(t["link"], timeout=30000, wait_until="domcontentloaded")
                    # 等待正文区域渲染
                    page.wait_for_selector(".detail__info-body", timeout=12000)

                    content_text = page.locator(".detail__info-body").text_content() or ""
                    content_html = page.locator(".detail__info-body").inner_html() or ""
                    content_text = content_text.strip()

                    # 封面图：优先 og:image
                    cover_img = page.evaluate(
                        "document.querySelector('meta[property=\"og:image\"]')?.content || ''"
                    ) or t["cover_fallback"]

                    results.append({
                        "source": self.name,
                        "title": t["title"],
                        "publish_date": t["date"],
                        "cover_image": cover_img,
                        "content_text": content_text,
                        "content_html": content_html,
                        "original_link": t["link"],
                    })

                except Exception as e:
                    print(f"  [机器之心] 抓取失败 {t['slug']}: {e}")
                    # 降级：使用列表摘要
                    results.append({
                        "source": self.name,
                        "title": t["title"],
                        "publish_date": t["date"],
                        "cover_image": t["cover_fallback"],
                        "content_text": t["snippet"],
                        "content_html": f"<p>{t['snippet']}</p>",
                        "original_link": t["link"],
                    })

                time.sleep(0.5)  # 礼貌延迟

            browser.close()

        return results
