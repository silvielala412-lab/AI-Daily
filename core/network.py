# -*- coding: utf-8 -*-
"""
网络请求模块
封装 requests，集成自动重试、随机User-Agent、随机延时等功能。
"""

import requests
import random
import time
import re
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from core.logger import log
from config.settings import REQUEST_RETRIES, REQUEST_TIMEOUT, REQUEST_DELAY_MIN, REQUEST_DELAY_MAX

# 禁用SSL警告 (微信请求需要)
requests.packages.urllib3.disable_warnings()

class NetworkManager:
    
    @staticmethod
    def clean_url(url):
        """清洗URL (处理Markdown格式等)"""
        url = str(url).strip()
        if "](" in url:
            match = re.search(r'\((https?://.*?)\)', url)
            if match:
                url = match.group(1)
        return url.strip()

    @staticmethod
    @retry(
        stop=stop_after_attempt(REQUEST_RETRIES),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(requests.exceptions.RequestException)
    )
    def request(url, method="get", headers=None, params=None, data=None, is_json=False, return_json=False):
        """
        通用请求方法 (带重试机制)
        :param url: 请求地址
        :param method: get/post
        :param headers: 请求头
        :param params: URL参数 (dict)
        :param data: POST数据 (dict)
        :param is_json: 是否返回JSON (已废弃，请使用return_json)
        :param return_json: 是否返回JSON
        :return: text 或 dict，失败抛出异常
        """
        url = NetworkManager.clean_url(url)
        
        # 兼容旧参数名
        if is_json:
            return_json = True
        
        # 随机延时防风控
        time.sleep(random.uniform(REQUEST_DELAY_MIN, REQUEST_DELAY_MAX))

        try:
            if method.lower() == "post":
                response = requests.post(url, headers=headers, params=params, json=data, timeout=REQUEST_TIMEOUT, verify=False)
            else:
                response = requests.get(url, headers=headers, params=params, timeout=REQUEST_TIMEOUT, verify=False)
            
            response.raise_for_status()
            
            if return_json:
                return response.json()
            else:
                response.encoding = 'utf-8' # 强制utf-8
                return response.text

        except requests.exceptions.HTTPError as e:
            # 404 不重试
            if e.response.status_code == 404:
                log.warning(f"页面未找到 (404): {url}")
                return None
            log.warning(f"请求异常 (重试中): {url} | {e}")
            raise e
        except Exception as e:
            log.warning(f"网络连接错误 (重试中): {url} | {e}")
            raise e

# 方便调用的快捷方式
request_url = NetworkManager.request
