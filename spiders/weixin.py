# -*- coding: utf-8 -*-
"""
微信公众号爬虫
支持批量抓取多个公众号的文章列表和详情
"""

import time
import random
import hashlib
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

from spiders.base import BaseSpider
from core.network import request_url
from core.logger import log
from config.settings import (
    WEIXIN_CONFIG, 
    HEADERS_WEIXIN_LIST, 
    HEADERS_WEIXIN_DETAIL
)
from utils.format_html_elements import clean_html_keep_content_and_img


class WeixinSpider(BaseSpider):
    def __init__(self):
        self.name = "微信公众号"
        self.biz_accounts = WEIXIN_CONFIG.get('BIZ_ACCOUNTS', {})
        self.token_id = WEIXIN_CONFIG.get('TOKEN_ID', '')
        self.max_articles = WEIXIN_CONFIG.get('MAX_ARTICLES_PER_ACCOUNT', 10)
        self.time_range_hours = WEIXIN_CONFIG.get('TIME_RANGE_HOURS', 72)

    def _get_md5(self, data):
        """生成MD5哈希值"""
        if isinstance(data, str):
            data = data.encode("utf-8")
        md = hashlib.md5()
        md.update(data)
        return md.hexdigest()

    def _is_within_time_range(self, timestamp):
        """检查文章是否在时间范围内"""
        if not timestamp:
            return False
        article_time = datetime.fromtimestamp(timestamp)
        return datetime.now() - article_time <= timedelta(hours=self.time_range_hours)

    def _clean_wechat_url(self, url):
        """清理微信URL，移除多余参数"""
        if not url or url.strip() == '':
            return ''
        import re
        cleaned_url = url.replace('http://', 'https://')
        cleaned_url = re.sub(r'#wechat_redirect.*?$', '', cleaned_url)
        cleaned_url = re.sub(r'&scene=\d+', '', cleaned_url)
        cleaned_url = cleaned_url.replace('&amp;', '&')
        return cleaned_url.strip()

    def _parse_article_list(self, biz, nickname):
        """
        解析单个公众号的文章列表
        :param biz: 公众号的BIZ ID
        :param nickname: 公众号昵称
        :return: 文章字典列表
        """
        valid_articles = []
        page = 0
        wx_appmsg_url = "https://mp.weixin.qq.com/cgi-bin/appmsg"

        log.info(f"开始采集 {nickname} 文章列表...")

        while len(valid_articles) < self.max_articles:
            index = page * 5
            try:
                params = {
                    'action': 'list_ex',
                    'begin': str(index),
                    'count': '5',
                    'fakeid': biz,
                    'type': '9',
                    'token': str(self.token_id),
                    'lang': 'zh_CN',
                    'f': 'json',
                    'ajax': '1',
                }
                
                response_text = request_url(
                    wx_appmsg_url,
                    headers=HEADERS_WEIXIN_LIST,
                    params=params,
                    return_json=True
                )
                
                if not response_text:
                    log.warning(f"{nickname} 获取列表失败，终止")
                    break

                import json
                try:
                    data = json.loads(response_text) if isinstance(response_text, str) else response_text
                except:
                    log.error(f"{nickname} JSON解析失败")
                    break

                if not data.get('app_msg_list'):
                    log.info(f"{nickname} 无更多文章")
                    break

                page_has_valid = False
                for article in data['app_msg_list']:
                    ts = article.get('update_time', 0)
                    if not self._is_within_time_range(ts):
                        continue
                    
                    page_has_valid = True
                    raw_url = article.get('link', '')
                    
                    article_dict = {
                        'title': article.get('title', ''),
                        'content_url': self._clean_wechat_url(raw_url),
                        'id': self._get_md5(raw_url),
                        'digest': article.get('digest', ''),
                        'author': nickname,
                        'p_date': datetime.fromtimestamp(ts),
                        'content_text': '',
                        'content_html': ''
                    }
                    valid_articles.append(article_dict)
                    
                    if len(valid_articles) >= self.max_articles:
                        break

                if not page_has_valid:
                    log.info(f"{nickname} 超出时间范围，停止翻页")
                    break

                time.sleep(random.uniform(2, 4))
                page += 1

            except Exception as e:
                log.error(f"{nickname} 列表采集失败: {e}")
                break

        return valid_articles

    def _parse_article_detail(self, url):
        """
        获取文章详情
        :param url: 文章URL
        :return: (content_text, content_html) 元组
        """
        if not url:
            return "[错误]URL为空", ""

        for attempt in range(3):
            try:
                clean_url = url.split('#')[0]
                html = request_url(clean_url, headers=HEADERS_WEIXIN_DETAIL)
                
                if html:
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # 定位正文容器
                    content_div = soup.find('div', id='js_content')
                    if not content_div:
                        content_div = soup.find('div', class_='rich_media_content')
                    
                    if content_div:
                        # 备份HTML用于存储（清理脚本和样式）
                        html_copy = BeautifulSoup(str(content_div), 'html.parser')
                        for tag in html_copy(['script', 'style', 'iframe', 'video']):
                            tag.decompose()
                        html_element = clean_html_keep_content_and_img(str(html_copy))
                        
                        # 提取纯文本
                        for tag in content_div(['script', 'style', 'iframe']):
                            tag.decompose()
                        
                        text_content = content_div.get_text(separator='\n')
                        text_content = text_content.replace('\xa0', ' ')
                        lines = [line.strip() for line in text_content.split('\n') if line.strip()]
                        text_content = '\n'.join(lines)
                        
                        return text_content, html_element
                    else:
                        log.warning(f"未找到内容容器: {url}")
                        return "[错误]未找到内容容器", ""
                
                time.sleep(random.uniform(1, 2))
                
            except Exception as e:
                log.warning(f"详情采集尝试 {attempt + 1} 失败: {e}")
                time.sleep(2)

        return "[错误]多次请求失败", ""

    def run(self):
        """
        执行微信公众号爬虫主逻辑
        :return: 文章列表
        """
        all_results = []

        for name, biz in self.biz_accounts.items():
            try:
                log.info(f"{'='*30} 开始处理: {name} {'='*30}")
                
                # 1. 获取文章列表
                articles = self._parse_article_list(biz, name)
                
                if not articles:
                    log.warning(f"{name} 未获取到有效文章")
                    continue

                # 2. 获取每篇文章详情
                for idx, article in enumerate(articles):
                    log.info(f"正在获取 {name} 第 {idx+1}/{len(articles)} 篇文章详情...")
                    
                    text, html = self._parse_article_detail(article['content_url'])
                    
                    # 转换为项目标准格式
                    result = {
                        'source': article['author'],
                        'title': article['title'],
                        'publish_date': article['p_date'].strftime('%Y-%m-%d %H:%M:%S'),
                        'cover_image': '',  # 微信列表不提供封面
                        'content_text': text,
                        'content_html': html,
                        'original_link': article['content_url']
                    }
                    all_results.append(result)
                    
                    time.sleep(random.uniform(1.5, 3))

                time.sleep(random.uniform(3, 6))
                
            except Exception as e:
                log.error(f"{name} 处理失败: {e}")
                continue

        log.info(f"微信公众号爬虫完成，共获取 {len(all_results)} 篇文章")
        return all_results
