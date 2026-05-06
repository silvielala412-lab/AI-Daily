# -*- coding: utf-8 -*-
"""
测试AI话题分类和语义去重功能
"""

import sys
sys.path.insert(0, 'd:\\data\\zx\\xyxyanti\\xyanti\\AI_News_Crawler')

from core.ai_analyzer import AIAnalyzer

print("=" * 60)
print("测试1: AI话题分类功能")
print("=" * 60)

# 测试样本1: AI技术文章
test_article_1 = {
    'title': 'OpenAI发布全新GPT-5模型，性能提升100%',
    'content': 'OpenAI今日宣布推出最新的大语言模型GPT-5，该模型在多项基准测试中表现优异，相比GPT-4性能提升了100%。新模型支持更长的上下文窗口...'
}

# 测试样本2: 保险科技文章
test_article_2 = {
    'title': '平安保险推出AI核保系统，理赔效率提升50%',
    'content': '平安保险今日发布了基于人工智能的智能核保系统，该系统可以自动审核保单，大幅提高理赔效率。据统计，使用该系统后理赔时间从3天缩短至1天...'
}

# 测试样本3: 数字营销文章
test_article_3 = {
    'title': '抖音发布2024年度营销报告，短视频营销成主流',
    'content': '抖音官方发布了2024年度营销趋势报告，数据显示短视频营销已成为品牌推广的主要方式。报告指出，通过精准的算法推荐，品牌可以更有效地触达目标用户...'
}

print("\n正在测试AI话题分类（需开启AI功能）...")
print("提示: 请确保 settings.py 中 ENABLE_AI_ANALYSIS = True\n")

# 测试文章1
print(f"文章1: {test_article_1['title']}")
result1 = AIAnalyzer.analyze_with_topic(test_article_1['title'], test_article_1['content'])
print(f"  话题分类: {result1.get('topic', 'N/A')}")
print(f"  AI评分: {result1.get('score', 0)}")
print(f"  摘要: {result1.get('summary', 'N/A')[:80]}...")
print()

# 测试文章2
print(f"文章2: {test_article_2['title']}")
result2 = AIAnalyzer.analyze_with_topic(test_article_2['title'], test_article_2['content'])
print(f"  话题分类: {result2.get('topic', 'N/A')}")
print(f"  AI评分: {result2.get('score', 0)}")
print(f"  摘要: {result2.get('summary', 'N/A')[:80]}...")
print()

# 测试文章3
print(f"文章3: {test_article_3['title']}")
result3 = AIAnalyzer.analyze_with_topic(test_article_3['title'], test_article_3['content'])
print(f"  话题分类: {result3.get('topic', 'N/A')}")
print(f"  AI评分: {result3.get('score', 0)}")
print(f"  摘要: {result3.get('summary', 'N/A')[:80]}...")
print()

print("=" * 60)
print("测试2: 语义相似度检测")
print("=" * 60)

# 测试相似文本
similar_text1 = "OpenAI发布了新的GPT-5大语言模型，性能大幅提升"
similar_text2 = "OpenAI推出最新GPT-5模型，各项指标均有显著提高"

# 测试不相似文本
different_text1 = "OpenAI发布了新的GPT-5大语言模型"
different_text2 = "平安保险推出智能核保系统提高理赔效率"

print(f"\n相似文本测试:")
print(f"  文本1: {similar_text1}")
print(f"  文本2: {similar_text2}")
similarity1 = AIAnalyzer.check_semantic_similarity(similar_text1, similar_text2)
print(f"  相似度: {similarity1}%")
print(f"  判定: {'重复' if similarity1 >= 80 else '不重复'}")
print()

print(f"不同文本测试:")
print(f"  文本1: {different_text1}")
print(f"  文本2: {different_text2}")
similarity2 = AIAnalyzer.check_semantic_similarity(different_text1, different_text2)
print(f"  相似度: {similarity2}%")
print(f"  判定: {'重复' if similarity2 >= 80 else '不重复'}")
print()

print("=" * 60)
print("测试完成！")
print("=" * 60)
print("\n注意事项:")
print("1. 确保已设置 ENABLE_AI_ANALYSIS = True")
print("2. 确保DeepSeek API Key配置正确")
print("3. 六大话题分类: AI前沿, 研发技术与数字化前沿, 保险相关, 数字化营销, 大健康, 销售")
print("4. 相似度阈值默认为80%，可在settings.py中调整SIMILARITY_THRESHOLD")
