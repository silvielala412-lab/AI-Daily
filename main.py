# -*- coding: utf-8 -*-
"""
主程序入口
负责任务调度、爬虫执行、数据清洗、AI分析、结果导出及邮件通知。
"""

import os
import time
import pandas as pd
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

from config.settings import (
    DATA_DIR, ENABLE_AI_ANALYSIS, ENABLE_FILTER_TOP_N, FILTER_TOP_NUMBER,
    ENABLE_DEDUPLICATION
)
from core.logger import log
from core.notifier import notifier
from core.ai_analyzer import analyzer
from spiders import ALL_SPIDERS
from utils.deduplicator import Deduplicator

# 确保数据目录存在
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

def job_crawl_mission():
    """
    全流程爬取任务
    """
    start_time = time.time()
    log.info("=== 开始全网爬取任务 ===")

    all_data = []
    
    # 1. 执行所有爬虫
    for SpiderClass in ALL_SPIDERS:
        spider = SpiderClass()
        data_list = spider.safe_run()
        all_data.extend(data_list)

    if not all_data:
        log.warning("本次未抓取到任何数据，任务结束。")
        return

    log.info(f"爬取阶段结束，共汇总 {len(all_data)} 篇文章。开始处理...")

    # 2. 先进行语义去重（与过去N天的文章对比）
    if ENABLE_DEDUPLICATION:
        log.info("开始语义去重（使用标题+正文）...")
        dedup = Deduplicator()
        all_data = dedup.filter_duplicates(all_data)
        log.info(f"去重后剩余 {len(all_data)} 篇文章")
    else:
        # 即使不去重，也添加相似度字段
        for item in all_data:
            item['similarity_score'] = 0

    # 3. 对去重后的数据进行 AI 分析（包含话题分类）
    processed_count = 0
    for item in all_data:
        # 如果开启了AI，则逐条分析（使用新的analyze_with_topic方法）
        if ENABLE_AI_ANALYSIS:
            ai_res = analyzer.analyze_with_topic(item['title'], item['content_text'])
            item['ai_score'] = ai_res.get('score', 0)
            item['ai_summary'] = ai_res.get('summary', '')
            item['ai_reason'] = ai_res.get('reason', '')
            item['topic'] = ai_res.get('topic', '未分类')  # AI返回的话题分类
            processed_count += 1
            if processed_count % 5 == 0:
                log.info(f"已分析 {processed_count}/{len(all_data)} 篇")
        else:
            item['ai_score'] = 0
            item['ai_summary'] = "-"
            item['ai_reason'] = "-"
            # 如果没有开启AI，检查是否已有topic字段（向后兼容）
            if 'topic' not in item:
                item['topic'] = "未分类"

    # 4. 结果保存与筛选
    df = pd.DataFrame(all_data)
    
    # 调整列顺序：topic在第一列，similarity_score在第二列
    desired_columns = ['topic', 'similarity_score', 'title', 'ai_score', 'ai_summary', 'ai_reason', 
                       'content_text', 'publish_date', 'url', 'source']
    # 保留实际存在的列，并按desired_columns顺序排列，其他列追加在后面
    existing_columns = [col for col in desired_columns if col in df.columns]
    other_columns = [col for col in df.columns if col not in desired_columns]
    df = df[existing_columns + other_columns]
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"AI_News_Full_{timestamp}.xlsx"
    
    # 筛选逻辑
    final_df = df
    if ENABLE_AI_ANALYSIS and ENABLE_FILTER_TOP_N:
        log.info(f"正在根据AI打分筛选 TOP {FILTER_TOP_NUMBER} ...")
        # 确保分数列是数字
        df['ai_score'] = pd.to_numeric(df['ai_score'], errors='coerce').fillna(0)
        final_df = df.sort_values(by="ai_score", ascending=False).head(FILTER_TOP_NUMBER)
        filename = f"AI_News_Top{FILTER_TOP_NUMBER}_{timestamp}.xlsx"

    save_path = os.path.join(DATA_DIR, filename)
    try:
        final_df.to_excel(save_path, index=False)
        log.info(f"文件保存成功: {save_path}")
        
        # 5. 发送邮件
        summary_text = f"本次抓取 {len(all_data)} 条，保留 {len(final_df)} 条。\n耗时: {int(time.time() - start_time)}秒。"
        notifier.send_report(summary_text, save_path)
        
    except Exception as e:
        err_msg = f"数据保存或发送邮件失败: {e}"
        log.error(err_msg)
        notifier.send_alert(err_msg)

    log.info("=== 任务全部完成 ===")

def main():
    """
    程序启动入口
    """
    log.info("程序启动，等待调度器执行...")
    
    # 初始化调度器
    scheduler = BlockingScheduler()
    
    # 立即执行一次 (方便测试)
    # job_crawl_mission() 
    
    # 添加定时任务: 每天早上 8:00 执行
    scheduler.add_job(job_crawl_mission, 'cron', hour=8, minute=0)
    
    # 或者每隔 4 小时执行一次
    # scheduler.add_job(job_crawl_mission, 'interval', hours=4)
    
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        log.info("程序停止")

if __name__ == "__main__":
    # 为了演示直接运行一次任务，如果需要定时请注释下面这行，解开 scheduler.start()
    # job_crawl_mission()
    main()
