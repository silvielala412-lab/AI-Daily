# -*- coding: utf-8 -*-
"""
AI_BASE 爬虫
"""

import time
import parsel
from config.settings import HEADERS_AIBASE
from spiders.base import BaseSpider
from core.network import request_url
from utils.format_html_elements import clean_html_keep_content_and_img
from utils.format_title import format_AiBasetitle

class AIBaseSpider(BaseSpider):
    def __init__(self):
        self.name = "AI_BASE"
        # 抓取中文日报列表页
        self.list_url = "https://www.aibase.com/zh/daily"

    def _parse_detail(self, url):
        """解析单篇文章详情，支持 /news/ 和 /daily/ 两种 URL"""
        html = request_url(url, headers=HEADERS_AIBASE)
        if not html: return None
        
        selector = parsel.Selector(html)
        
        # 封面图：优先取 post-content 内图，其次取 og:image
        cover_img = (
            selector.css("div.post-content img::attr(src)").get()
            or selector.css('meta[property="og:image"]::attr(content)').get()
            or ""
        )
        
        # 正文段落
        content_p_list = selector.css("div.post-content p")
        content = ""
        for p in content_p_list:
            p_text = p.xpath("string(.)").get().strip()
            if p_text:
                content += p_text + "\n\n"
        content = content.replace("\n\n\n", "\n\n").strip() if content else "暂无正文"

        # 提取 post-content 的 HTML 片段（而非整页）
        content_html = selector.css("div.post-content").get() or html

        return {
            "cover": cover_img,
            "html": content_html,
            "text": content
        }

    def run(self):
        html = request_url(self.list_url, headers=HEADERS_AIBASE)
        if not html: return []
        
        selector = parsel.Selector(html)
        # 列表页抓取日报中的新闻条目链接（选择器已验证有效）
        news_list = selector.css("div.grid a.line-clamp-1")
        
        results = []
        seen_urls = set()

        for a in news_list:
            # 去掉标题前的编号前缀（如 "1、"）
            title = a.xpath("string(.)").get().strip()
            href = a.css("::attr(href)").get()
            if not href: continue
            
            # href 格式为 /news/xxxxx 或 /daily/xxxxx，加 /zh 前缀访问中文版
            detail_url = "https://www.aibase.com/zh" + href
            
            if detail_url in seen_urls: continue
            seen_urls.add(detail_url)
            
            date = time.strftime("%Y-%m-%d")

            details = self._parse_detail(detail_url)
            if details:
                results.append({
                    "source": self.name,
                    "title": format_AiBasetitle(title),
                    "publish_date": date,
                    "cover_image": details['cover'],
                    "content_text": details['text'],
                    "content_html": clean_html_keep_content_and_img(details['html']),
                    "original_link": detail_url
                })
        
        return results
