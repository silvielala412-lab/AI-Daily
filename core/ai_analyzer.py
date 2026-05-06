# # -*- coding: utf-8 -*-
# """
# AI 分析模块
# 对接 DeepSeek API，对新闻进行摘要和打分。
# """
#
# import json
# import re
# from core.network import request_url
# from core.logger import log
# from config.settings import ENABLE_AI_ANALYSIS, DEEPSEEK_API_KEY, DEEPSEEK_API_URL
#
# class AIAnalyzer:
#
#     @staticmethod
#     def clean_json(text):
#         """清洗AI返回的代码块格式，提取纯JSON"""
#         if not text:
#             return "{}"
#         text = re.sub(r'^```(json)?\s*', '', text, flags=re.I)
#         text = re.sub(r'\s*```$', '', text)
#         return text.strip()
#
#     @staticmethod
#     def analyze(title, content):
#         """
#         调用 DeepSeek 进行分析（旧版本，保持向后兼容）
#         :return: dict {"summary": "...", "score": 80, "reason": "..."}
#         """
#         if not ENABLE_AI_ANALYSIS:
#             return {"summary": "AI未开启", "score": 0, "reason": "功能关闭"}
#
#         log.info(f"正在进行AI分析: {title[:20]}...")
#
#         # 截断内容以防超长
#         input_text = content[:3000] if content else "无内容"
#
#         prompt = f"""
#         你是一位金融公司的科技领域工作者,你关注技术的新进展以及在金融或者生活中的落地应用与价值
#         现在你需要阅读下面这篇文章,并输出严格的JSON 格式数据。
#         文章标题:{title}
#         文章内容:{input_text}
#         要求返回字段:
#         1."summary": 100-150字左右的精炼摘要。
#         2."score": 0-100分的价值打分(基于技术对生活的影响,技术带来的价值、技术的可溶地性;我们不需要某
#         个人或者公司的个人人员动态)。
#         3."reason":一句话解释打分理由。
#         请只返回 JSON字符串,不要任何多余内容。
#         """
#
#         payload = {
#             "model": "deepseek-chat",
#             "messages": [{"role": "user", "content": prompt}],
#             "temperature": 0.1,
#             "response_format": {"type": "json_object"}
#         }
#
#         headers = {
#             "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
#             "Content-Type": "application/json"
#         }
#
#         try:
#             # 复用 network 的重试机制
#             resp = request_url(DEEPSEEK_API_URL, method="post", headers=headers, data=payload, is_json=True)
#
#             if resp and 'choices' in resp:
#                 content_str = resp['choices'][0]['message']['content']
#                 return json.loads(AIAnalyzer.clean_json(content_str))
#
#         except Exception as e:
#             log.error(f"AI 分析接口调用失败: {e}")
#
#         return {"summary": "AI分析失败", "score": 0, "reason": "接口异常"}
#
#     @staticmethod
#     def analyze_with_topic(title, content):
#         """
#         调用 DeepSeek 进行分析，包含话题分类
#         :return: dict {"summary": "...", "score": 80, "reason": "...", "topic": "..."}
#         """
#         if not ENABLE_AI_ANALYSIS:
#             return {"summary": "AI未开启", "score": 0, "reason": "功能关闭", "topic": "未分类"}
#
#         log.info(f"正在进行AI分析(含话题分类): {title[:20]}...")
#
#         # 截断内容以防超长
#         input_text = content[:7000] if content else "无内容"
#
#         prompt = f"""
#         你是一位保险金融公司的科技团队成员,需要对文章进行分类和价值评分。
#
#         文章标题:{title}
#         文章内容:{input_text}
#
#         任务要求:
#         1. 首先将文章分类到以下六个类别之一,然后根据对应类别的评分标准打分。
#
#         【话题分类及评分标准】:
#
#         ▪ "AI前沿" - AI技术的最新发展、研究成果、技术突破
#           评分维度(0-100分):
#           - 技术对研发领域的影响
#           - 技术对用户带来的价值
#           - 技术的可落地性
#           - 是否对团队的技术演进带来帮助
#           ⚠️ 排除: 具体个人或公司的人员动态(对团队帮助很小)
#
#         ▪ "研发技术与数字化前沿" - 软件开发、云计算、大数据、区块链等技术
#           评分维度(0-100分):
#           - 技术对研发领域的影响
#           - 技术对用户带来的价值
#           - 技术的可落地性
#           - 是否对团队的技术演进带来帮助
#           ⚠️ 排除: 具体个人或公司的人员动态(对团队帮助很小)
#
#         ▪ "保险相关" - 保险行业动态、保险科技、保险产品
#           评分维度(0-100分):
#           - 是否对用户有投资回报性/保障性/体验提升
#           - 是否对公司的运转和效率带来提升
#           - 是否与技术具有相关性
#           - 是否对团队的业务经营思路带来帮助
#           ⚠️ 排除: 具体个人或公司的人员动态、营收动态(对团队帮助很小)
#
#         ▪ "数字化营销" - 营销技术、广告科技、用户增长、品牌营销
#           评分维度(0-100分):
#           - 营销思路与方案的创新性
#           - 营销技术的创新性
#           - 营销方案在保险行业的可复制性
#           - 是否对团队的业务经营思路及技术支持方案带来帮助
#           ⚠️ 排除: 具体个人或公司的人员动态、营收动态(对团队帮助很小)
#
#         ▪ "大健康" - 医疗健康、生物科技、健康管理
#           评分维度(0-100分):
#           - 健康类应用的新体验
#           - 互联网健康的新发展趋势
#           - 健康领域的技术关联性
#           - 是否对团队的技术演进以及技术与健康领域的融合带来帮助
#           ⚠️ 排除: 具体的健康知识、具体公司或个人的人员动态(对团队帮助很小)
#
#         ▪ "销售" - 销售模式、销售流程、客户关系管理
#           评分维度(0-100分):
#           - 销售模式与流程的创新
#           - 销售体验的创新
#           - 保险类APP或互联网保险APP在销售方面的创新
#           - 是否对团队的技术演进以及技术与保险销售的融合带来帮助
#           ⚠️ 排除: 具体公司或个人的人员动态(对团队帮助很小)
#
#         返回JSON格式(必须包含以下4个字段):
#         {{
#           "topic": "从上述六个类别中选择一个",
#           "score": 0-100的整数分数,
#           "summary": "100-150字的精炼摘要",
#           "reason": "一句话解释打分理由,说明符合哪些评分维度"
#         }}
#
#         请只返回JSON,不要任何多余内容。
#         """
#
#         payload = {
#             "model": "deepseek-chat",
#             "messages": [{"role": "user", "content": prompt}],
#             "temperature": 0.1,
#             "response_format": {"type": "json_object"}
#         }
#
#         headers = {
#             "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
#             "Content-Type": "application/json"
#         }
#
#         try:
#             # 复用 network 的重试机制
#             resp = request_url(DEEPSEEK_API_URL, method="post", headers=headers, data=payload, is_json=True)
#
#             if resp and 'choices' in resp:
#                 content_str = resp['choices'][0]['message']['content']
#                 result = json.loads(AIAnalyzer.clean_json(content_str))
#
#                 # 验证topic字段，确保是六大类之一
#                 valid_topics = ["AI前沿", "研发技术与数字化前沿", "保险相关", "数字化营销", "大健康", "销售"]
#                 if 'topic' not in result or result['topic'] not in valid_topics:
#                     log.warning(f"AI返回的topic无效: {result.get('topic', 'None')}, 默认设为'AI前沿'")
#                     result['topic'] = "AI前沿"
#
#                 return result
#
#         except Exception as e:
#             log.error(f"AI 分析接口调用失败: {e}")
#
#         return {"summary": "AI分析失败", "score": 0, "reason": "接口异常", "topic": "未分类"}
#
#     @staticmethod
#     def check_semantic_similarity(summary1, summary2):
#         """
#         检查两篇文章摘要的语义相似度
#         :param summary1: 第一篇文章摘要
#         :param summary2: 第二篇文章摘要
#         :return: int 0-100 的相似度分数
#         """
#         if not ENABLE_AI_ANALYSIS:
#             return 0
#
#         log.info(f"检查语义相似度...")
#
#         prompt = f"""
#         你是一个语义分析专家。请判断文本1（一篇新文章的摘要）是否与文本2（多篇历史文章的合并摘要）中的任何一篇相似。
#
#         文本1（新文章）: {summary1[:1500]}
#
#         文本2（历史文章合并摘要，用---分隔）: {summary2[:7000]}
#
#         请返回一个JSON对象，包含以下字段:
#         1. "similarity": 0-100的相似度分数。如果新文章与历史文章集合中的任何一篇相似，就返回高分。
#         2. "reason": 简短说明相似或不相似的原因。
#
#         评分标准:
#         - 80-100分: 新文章与历史文章集合中的某一篇描述的是同一件事，只是表述不同
#         - 60-79分: 新文章与历史文章集合中的某一篇主题相似，但具体内容有明显差异
#         - 40-59分: 新文章与历史文章集合中的某一篇有一些相关性，但是不同的事件或话题
#         - 0-39分: 新文章与历史文章集合中的所有文章都完全不相关或主题完全不同
#
#         请只返回 JSON字符串。
#         """
#
#         payload = {
#             "model": "deepseek-chat",
#             "messages": [{"role": "user", "content": prompt}],
#             "temperature": 0.1,
#             "response_format": {"type": "json_object"}
#         }
#
#         headers = {
#             "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
#             "Content-Type": "application/json"
#         }
#
#         try:
#             resp = request_url(DEEPSEEK_API_URL, method="post", headers=headers, data=payload, is_json=True)
#
#             if resp and 'choices' in resp:
#                 content_str = resp['choices'][0]['message']['content']
#                 result = json.loads(AIAnalyzer.clean_json(content_str))
#                 return result.get('similarity', 0)
#
#         except Exception as e:
#             log.error(f"语义相似度检查失败: {e}")
#
#         return 0
#
# # 导出实例或类
# analyzer = AIAnalyzer


# -*- coding: utf-8 -*-
"""
AI 分析模块
对接 DeepSeek API，对新闻进行摘要和打分。
"""

import json
import re
from core.network import request_url
from core.logger import log
from config.settings import ENABLE_AI_ANALYSIS, DEEPSEEK_API_KEY, DEEPSEEK_API_URL


class AIAnalyzer:

    @staticmethod
    def clean_json(text):
        """清洗AI返回的代码块格式，提取纯JSON"""
        if not text:
            return "{}"
        text = re.sub(r'^```(json)?\s*', '', text, flags=re.I)
        text = re.sub(r'\s*```$', '', text)
        return text.strip()

    @staticmethod
    def analyze(title, content):
        """
        调用 DeepSeek 进行分析（旧版本，保持向后兼容）
        :return: dict {"summary": "...", "score": 80, "reason": "..."}
        """
        if not ENABLE_AI_ANALYSIS:
            return {"summary": "AI未开启", "score": 0, "reason": "功能关闭"}

        log.info(f"正在进行AI分析: {title[:20]}...")

        # 截断内容以防超长
        input_text = content[:3000] if content else "无内容"

        prompt = f"""
        你是一位金融公司的科技领域工作者,你关注技术的新进展以及在金融或者生活中的落地应用与价值
        现在你需要阅读下面这篇文章,并输出严格的JSON 格式数据。
        文章标题:{title}
        文章内容:{input_text}
        要求返回字段:
        1."summary": 100-150字左右的精炼摘要。
        2."score": 0-100分的价值打分(基于技术对生活的影响,技术带来的价值、技术的可溶地性;我们不需要某
        个人或者公司的个人人员动态)。
        3."reason":一句话解释打分理由。
        请只返回 JSON字符串,不要任何多余内容。
        """

        payload = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.1,
            "response_format": {"type": "json_object"}
        }

        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }

        try:
            # 复用 network 的重试机制
            resp = request_url(DEEPSEEK_API_URL, method="post", headers=headers, data=payload, is_json=True)

            if resp and 'choices' in resp:
                content_str = resp['choices'][0]['message']['content']
                return json.loads(AIAnalyzer.clean_json(content_str))

        except Exception as e:
            log.error(f"AI 分析接口调用失败: {e}")

        return {"summary": "AI分析失败", "score": 0, "reason": "接口异常"}

    @staticmethod
    def analyze_with_topic(title, content):
        """
        调用 DeepSeek 进行分析，包含话题分类
        :return: dict {"summary": "...", "score": 80, "reason": "...", "topic": "..."}
        """
        if not ENABLE_AI_ANALYSIS:
            return {"summary": "AI未开启", "score": 0, "reason": "功能关闭", "topic": "未分类"}

        log.info(f"正在进行AI分析(含话题分类): {title[:20]}...")

        # 截断内容以防超长
        input_text = content[:7000] if content else "无内容"

        prompt = f"""你是一个金融公司的科技领域工作者,
        关注技术的新进展以及在金融或者生活中的落地应用与价值,从而能给团队更好的进行技术演进或者给用户提供更好的服务带来正面的启发
        
        文章标题:{title}
        文章内容:{input_text}
任务要求:
1. 首先将文章分类到以下六个类别之一,然后根据对应类别的评分标准打分。

【话题分类及评分标准】:
分数说明:
0分: 完全不符合评分维度要求
1分: 很少符合评分维度要求
2分: 部分符合评分维度要求
3分: 大部分符合评分维度要求
4分: 基本符合评分维度要求
5分: 完全符合评分维度要求

▪ "AI前沿" - AI技术的最新发展、研究成果、技术突破
  评分维度(0-5分):
  - 技术对研发领域的影响
  - 技术对用户带来的价值
  - 技术的可落地性
  - 是否对团队的技术演进带来帮助
  ⚠ 排除: 具体个人或公司的人员动态(对团队帮助很小)

▪ "研发技术与数字化前沿" - 软件开发、云计算、大数据、区块链等技术
  评分维度(0-5分):
  - 技术对研发领域的影响
  - 技术对用户带来的价值
  - 技术的可落地性
  - 是否对团队的技术演进带来帮助
  ⚠ 排除: 具体个人或公司的人员动态(对团队帮助很小)

▪ "保险相关" - 保险行业动态、保险科技、保险产品
  评分维度(0-5分):
- 是否揭示行业重大趋势或商业模式创新，能否帮助公司识别新机会或应对关键挑战。
- 是否成熟、能解决实际业务痛点，并具备与公司现有系统整合的潜力。
- 是否存在落地可能性，能否在短期内进行试点或应用。
- 能否直接启发一个试点项目、流程优化或策略调整，并明确后续分析或跟进的步骤。
⚠ 排除: 具体个人或公司的人员动态、营收动态(对团队帮助很小)

▪ "数字化营销" - 营销技术、广告科技、用户增长、品牌营销
  评分维度(0-5分):
  - 营销思路与方案的创新性
  - 营销技术的创新性
  - 营销方案在保险行业的可复制性
  - 是否对团队的业务经营思路及技术支持方案带来帮助
  ⚠ 排除: 具体个人或公司的人员动态、营收动态(对团队帮助很小)

▪ "大健康" - 医疗健康、生物科技、健康管理
  评分维度(0-5分):
  - 健康类应用的新体验
  - 互联网健康的新发展趋势
  - 健康领域的技术关联性
  - 是否对团队的技术演进以及技术与健康领域的融合带来帮助
  ⚠ 排除: 具体的健康知识、具体公司或个人的人员动态(对团队帮助很小)

▪ "销售" - 销售模式、销售流程、客户关系管理
  评分维度(0-5分):
  - 销售模式与流程的创新
  - 销售体验的创新
  - 保险类APP或互联网保险APP在销售方面的创新
  - 是否对团队的技术演进以及技术与保险销售的融合带来帮助
  ⚠ 排除: 具体公司或个人的人员动态(对团队帮助很小)

返回JSON格式(必须包含以下4个字段):
{{
  "topic": "从上述六个类别中选择一个",
  "score": 0-5的整数分数,
  "summary": "100-150字的精炼摘要",
  "reason": "一句话解释打分理由,说明符合哪些评分维度"
}}

请只返回JSON,不要任何多余内容。"""

        payload = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.1,
            "response_format": {"type": "json_object"}
        }

        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }

        try:
            # 复用 network 的重试机制
            resp = request_url(DEEPSEEK_API_URL, method="post", headers=headers, data=payload, is_json=True)

            if resp and 'choices' in resp:
                content_str = resp['choices'][0]['message']['content']
                result = json.loads(AIAnalyzer.clean_json(content_str))

                # 验证topic字段，确保是六大类之一
                valid_topics = ["AI前沿", "研发技术与数字化前沿", "保险相关", "数字化营销", "大健康", "销售"]
                if 'topic' not in result or result['topic'] not in valid_topics:
                    log.warning(f"AI返回的topic无效: {result.get('topic', 'None')}, 默认设为'AI前沿'")
                    result['topic'] = "AI前沿"

                return result

        except Exception as e:
            log.error(f"AI 分析接口调用失败: {e}")

        return {"summary": "AI分析失败", "score": 0, "reason": "接口异常", "topic": "未分类"}

    @staticmethod
    def check_semantic_similarity(summary1, summary2):
        """
        检查两篇文章摘要的语义相似度
        :param summary1: 第一篇文章摘要
        :param summary2: 第二篇文章摘要
        :return: int 0-100 的相似度分数
        """
        if not ENABLE_AI_ANALYSIS:
            return 0

        log.info(f"检查语义相似度...")

        prompt = f"""
        你是一个语义分析专家。请判断文本1（一篇新文章的摘要）是否与文本2（多篇历史文章的合并摘要）中的任何一篇相似。

        文本1（新文章）: {summary1[:1500]}

        文本2（历史文章合并摘要，用---分隔）: {summary2[:7000]}

        请返回一个JSON对象，包含以下字段:
        1. "similarity": 0-100的相似度分数。如果新文章与历史文章集合中的任何一篇相似，就返回高分。
        2. "reason": 简短说明相似或不相似的原因。

        评分标准:
        - 80-100分: 新文章与历史文章集合中的某一篇描述的是同一件事，只是表述不同
        - 60-79分: 新文章与历史文章集合中的某一篇主题相似，但具体内容有明显差异
        - 40-59分: 新文章与历史文章集合中的某一篇有一些相关性，但是不同的事件或话题
        - 0-39分: 新文章与历史文章集合中的所有文章都完全不相关或主题完全不同

        请只返回 JSON字符串。
        """

        payload = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.1,
            "response_format": {"type": "json_object"}
        }

        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }

        try:
            resp = request_url(DEEPSEEK_API_URL, method="post", headers=headers, data=payload, is_json=True)

            if resp and 'choices' in resp:
                content_str = resp['choices'][0]['message']['content']
                result = json.loads(AIAnalyzer.clean_json(content_str))
                return result.get('similarity', 0)

        except Exception as e:
            log.error(f"语义相似度检查失败: {e}")

        return 0


# 导出实例或类
analyzer = AIAnalyzer
