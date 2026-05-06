# -*- coding: utf-8 -*-
"""
爬虫基类
定义所有爬虫必须实现的接口。
"""

from abc import ABC, abstractmethod
from core.logger import log

class BaseSpider(ABC):
    def __init__(self):
        self.name = "Unknown"

    @abstractmethod
    def run(self):
        """
        执行爬虫的主逻辑
        :return: list of dict, 每个元素是一篇解析好的文章数据
        """
        pass

    def safe_run(self):
        """
        安全执行包装器，捕获所有异常，防止单个爬虫挂掉影响整体
        """
        try:
            log.info(f"启动爬虫: {self.name}")
            results = self.run()
            log.info(f"爬虫 {self.name} 完成，获取 {len(results)} 条数据")
            return results
        except Exception as e:
            log.error(f"爬虫 {self.name} 执行失败: {e}")
            return []
