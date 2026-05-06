# -*- coding: utf-8 -*-
"""
新智元爬虫
"""

import time
from bs4 import BeautifulSoup
from spiders.base import BaseSpider
from core.network import request_url
from config.settings import HEADERS_GENERAL

class XinzhiyuanSpider(BaseSpider):
    def __init__(self):
        self.name = "新智元"
        self.list_url = "https://aiera.com.cn/"

    def _parse_detail(self, url):
        html = request_url(url, headers=HEADERS_GENERAL)
        if not html: return None
        soup = BeautifulSoup(html, 'html.parser')

        cover_img = ""
        meta_img = soup.find('meta', property='og:image')
        if meta_img: cover_img = meta_img.get('content')

        # 移除干扰元素
        for tag in soup(['script', 'style', 'div.related-posts']): 
            tag.decompose()
        
        article = soup.find('article') or soup.select_one('.entry-content')

        if article:
            return {
                "cover": cover_img,
                "html": str(article),
                "text": article.get_text('\n', strip=True)
            }
        return None

    def run(self):
        html = request_url(self.list_url, headers=HEADERS_GENERAL)
        if not html: return []

        soup = BeautifulSoup(html, 'html.parser')
        entries = soup.find_all('h2', class_='entry-title')
        if not entries: entries = soup.find_all('article')
        
        results = []
        for entry in entries:
            a = entry.find('a')
            if not a: continue
            
            title = a.get_text(strip=True)
            link = a['href']
            date = time.strftime("%Y-%m-%d") # 列表页无日期，取当天

            # 获取详情
            details = self._parse_detail(link)
            if details:
                results.append({
                    "source": self.name,
                    "title": title,
                    "publish_date": date,
                    "cover_image": details['cover'],
                    "content_text": details['text'],
                    "content_html": details['html'],
                    "original_link": link
                })
        
        return results
