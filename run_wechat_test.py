# -*- coding: utf-8 -*-
"""
测试微信爬虫独立运行
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from spiders.weixin import WeixinSpider
from core.logger import log

if __name__ == "__main__":
    print("=" * 50)
    print("测试微信公众号爬虫")
    print("=" * 50)

    try:
        # 创建爬虫实例
        spider = WeixinSpider()
        print(f"✓ 爬虫初始化成功: {spider.name}")
        print(f"  监控账号数量: {len(spider.biz_accounts)}")
        print(f"  每账号抓取: {spider.max_articles} 篇")
        print(f"  时间范围: {spider.time_range_hours} 小时")

        # 执行爬取 (使用safe_run保证异常处理)
        print("\n开始爬取...")
        results = spider.safe_run()

        # 输出结果
        print(f"\n{'=' * 50}")
        print(f"爬取完成！共获取 {len(results)} 篇文章")

        if results:
            print("\n前3篇文章预览:")
            for i, article in enumerate(results[:3], 1):
                print(f"\n{i}. {article['title']}")
                print(f"   来源: {article['source']}")
                print(f"   时间: {article['publish_date']}")
                print(f"   内容长度: {len(article['content_text'])} 字符")

        print(f"\n{'=' * 50}")
        print("✓ 测试通过!")

    except Exception as e:
        print(f"\n✗ 测试失败: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
