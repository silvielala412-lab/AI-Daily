# -*- coding: utf-8 -*-
"""
语义去重模块
用于对比当天文章与历史文章的语义相似度，过滤重复内容
"""

import os
import glob
import pandas as pd
from datetime import datetime, timedelta
from core.logger import log
from core.ai_analyzer import AIAnalyzer
from config.settings import DATA_DIR, DEDUPLICATION_DAYS, SIMILARITY_THRESHOLD, ENABLE_DEDUPLICATION


class Deduplicator:
    """语义去重器"""
    
    def __init__(self):
        self.historical_articles = []
        self.merged_summary = ""  # 合并后的历史摘要
        self.load_historical_data()
    
    def load_historical_data(self):
        """加载过去N天的历史数据并合并摘要"""
        if not ENABLE_DEDUPLICATION:
            log.info("语义去重功能未开启")
            return
        
        log.info(f"正在加载过去 {DEDUPLICATION_DAYS} 天的历史文章...")
        
        # 计算日期范围
        cutoff_date = datetime.now() - timedelta(days=DEDUPLICATION_DAYS)
        
        # 查找所有Excel文件
        excel_files = glob.glob(os.path.join(DATA_DIR, "AI_News_*.xlsx"))
        
        summaries = []  # 收集所有摘要
        
        for file_path in excel_files:
            try:
                # 从文件名解析日期 (格式: AI_News_Full_20260121_170045.xlsx)
                filename = os.path.basename(file_path)
                date_str = filename.split('_')[3]  # 提取日期部分 "20260121"
                file_date = datetime.strptime(date_str, "%Y%m%d")
                
                # 只加载指定天数内的文件
                if file_date >= cutoff_date:
                    df = pd.read_excel(file_path)
                    
                    # 提取需要的字段
                    for _, row in df.iterrows():
                        article = {
                            'title': row.get('title', ''),
                            'summary': row.get('ai_summary', row.get('content_text', ''))[:500],  # 使用AI摘要或截取正文
                            'date': file_date
                        }
                        self.historical_articles.append(article)
                        
                        # 收集摘要用于合并
                        if article['summary'] and article['summary'] not in ['AI未开启', 'AI分析失败', '-']:
                            summaries.append(article['summary'])
                    
                    log.info(f"已加载历史文件: {filename} ({len(df)} 篇)")
                    
            except Exception as e:
                log.warning(f"加载历史文件失败 {file_path}: {e}")
                continue
        
        # 合并所有历史文章的摘要
        if summaries:
            # 用换行符分隔各篇摘要，方便AI理解
            self.merged_summary = "\n---\n".join(summaries)
            log.info(f"历史数据加载完成，共 {len(self.historical_articles)} 篇文章")
            log.info(f"已合并历史摘要，总长度: {len(self.merged_summary)} 字符")
        else:
            log.info("未找到有效的历史摘要")
    
    def get_similarity_score(self, article_summary):
        """
        获取文章与历史文章的相似度分数
        :param article_summary: 当前文章摘要
        :return: int 0-100 的相似度分数
        """
        if not ENABLE_DEDUPLICATION or not self.merged_summary:
            return 0
        
        # 与合并后的历史摘要比较（只调用一次AI）
        similarity = AIAnalyzer.check_semantic_similarity(
            article_summary, 
            self.merged_summary
        )
        
        return similarity
    
    def filter_duplicates(self, articles):
        """
        过滤重复文章，并为每篇文章添加相似度分数
        :param articles: 文章列表（此时还未进行AI分析，使用标题+正文进行去重）
        :return: 过滤后的文章列表
        """
        if not ENABLE_DEDUPLICATION:
            log.info("语义去重功能未开启，跳过去重")
            # 即使不去重，也添加相似度字段，值为0
            for article in articles:
                article['similarity_score'] = 0
            return articles
        
        log.info(f"开始进行语义去重，当前有 {len(articles)} 篇文章...")
        
        filtered = []
        duplicates_count = 0
        
        for idx, article in enumerate(articles):
            log.info(f"检查第 {idx + 1}/{len(articles)} 篇: {article.get('title', '')[:30]}...")
            
            # 使用标题+部分正文进行去重（因为此时还未进行AI分析）
            summary = f"{article.get('title', '')} {article.get('content_text', '')[:500]}"
            
            # 获取相似度分数
            similarity = self.get_similarity_score(summary)
            article['similarity_score'] = similarity
            
            if similarity >= SIMILARITY_THRESHOLD:
                reason = f"与过去{DEDUPLICATION_DAYS}天内的文章相似度 {similarity}%"
                duplicates_count += 1
                log.info(f"  ✗ 重复: {reason}")
            else:
                filtered.append(article)
                log.info(f"  ✓ 保留 (相似度: {similarity}%)")
        
        log.info(f"语义去重完成: 过滤 {duplicates_count} 篇，保留 {len(filtered)} 篇")
        return filtered


# 导出实例
deduplicator = Deduplicator
