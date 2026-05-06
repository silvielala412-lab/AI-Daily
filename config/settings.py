# -*- coding: utf-8 -*-
"""
全局配置文件
集中管理所有参数，包括API Key、爬虫规则、邮件配置等。
所有注释均为中文，方便阅读和维护。
"""

import os

# ================= 1. 核心功能开关 (Feature Toggles) =================
# 是否开启AI智能分析 (True=开启 | False=仅抓取)
ENABLE_AI_ANALYSIS = True

# 是否开启Top-N筛选 (True=仅保留高分文章 | False=保留全部)
ENABLE_FILTER_TOP_N = True

# 筛选保留的条数 (仅在 ENABLE_FILTER_TOP_N = True 时生效)
FILTER_TOP_NUMBER = 101

# 是否开启语义去重 (True=开启 | False=关闭)
ENABLE_DEDUPLICATION = True

# 语义去重回溯天数 (与过去N天的文章对比)
DEDUPLICATION_DAYS = 3

# 相似度阈值 (0-100，超过此值视为重复)
SIMILARITY_THRESHOLD = 80


# ================= 2. DeepSeek AI 配置 (AI Config) =================
# 建议使用环境变量获取 Key，这里为了方便直接写了默认值
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "sk-2bc9833c71964631af4baf86639ac27c")
DEEPSEEK_API_URL = "https://api.deepseek.com/chat/completions"


# ================= 3. 邮件告警配置 (Email Alert Config) =================
# 用于发送爬虫运行报告和错误告警
# 请将其替换为您的SMTP服务器信息 (例如: smtp.qq.com, smtp.163.com)
SMTP_CONFIG = {
    "host": "smtp.qq.com",        # SMTP服务器地址
    "port": 465,                       # 端口 (通常SSL是465)
    "user": "582798963@qq.com",  # 发件人邮箱账号
    "password": "sfxekrikxzfjbbih",       # 发件人邮箱密码/授权码
    "receivers": ["1214148116@qq.com"]  # 接收报告的邮箱列表
}

# 邮件发送开关 (开发测试时可设为 False)
ENABLE_EMAIL_ALERT = True


# ================= 4. 爬虫通用配置 (Crawler Config) =================
# 通用请求头
HEADERS_GENERAL = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
}

# 机器之心专用 Header (Cookie可能需要定期更新)
HEADERS_JIQIZHIXIN = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Cookie": "ahoy_visitor=89c16990-f351-405b-9659-6a62e43874b0; _ga=GA1.1.1559419992.1767928514; ..."  # (此处省略长Cookie，建议定期更新)
}

# AI_BASE 专用 Header
HEADERS_AIBASE = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Cookie": "Hm_lvt_20171d7bc84390037a47470dd0e59957=1768530411; ..."
}

# ================= 微信公众号配置 (WeChat MP Config) =================
# 微信公众号平台配置
WEIXIN_CONFIG = {
    # 微信公众平台 Token (需定期更新)
    "TOKEN_ID": "1808943823",
    
    # 公众号账号映射 (昵称 -> BIZ ID)
    "BIZ_ACCOUNTS": {
        '51CTO': 'MzAwMDEzNTc1Mw==',
        'InfoQ': 'MjM5MDE0Mjc4MA==',
        'AI前线': 'MzU1NDA4NjU2MA==',
        '量子位': 'MzIzNjc1NzUzMw==',
        '慧保天下': 'MzA4NzY1NjAxNQ==',
        '深蓝保': 'MzI0Nzg2MTExMA==',
        '今日保': 'MzUzMjUwMDE0NQ==',
        '13个精算师': 'Mzg3Mzg0NTE5OA==',
        '空手': 'MzAxNzU1MTI0MQ==',
        'socialbeta': 'Mzg2Mzg5NTgwMw==',
        '数字营销市场': 'MjM5MTgxODU3MQ==',
        '首席营销官': 'MzAxMDUwNjI3MQ==',
        '蚂蚁阿福': 'Mzk5MDkwNDg1Mg==',
        '京东健康': 'MzI2MzYxMDEyMg==',
        # '丁香医生': 'MjA1ODMxMDQwMQ==',
        '蚂蚁保': 'MzkzOTEzMjkwNw==',
        '微保': 'MzIwNjc3NjI5MA==',
        '小雨伞': 'MzI0MDk0MjUzNw=='
    },
    
    # 每个账号最大抓取文章数
    "MAX_ARTICLES_PER_ACCOUNT": 10,
    
    # 时间范围过滤 (小时)
    "TIME_RANGE_HOURS": 48,
}

# 微信文章列表请求头 (用于API接口)
HEADERS_WEIXIN_LIST = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
    # 'Cookie': '_qimei_uuid42=19a0b0e0321100feae4f6672aa9a900553e9872200; _qimei_fingerprint=ec639a8ea13c99d3a3d2ed4039da668a; _qimei_q36=; _qimei_h38=21de693eae4f6672aa9a90050200000da19a0b; RK=fGm0tB+fPQ; ptcz=bc0403bd782d82a11003786b608ee095440dd67d9796f2c42f380cf3a4febad6; pac_uid=0_AATfwJjP0R7aF; omgid=0_AATfwJjP0R7aF; ua_id=mfXzRh1QWDO5fqRKAAAAABHITwAC_lXT-nr2-cmMLf4=; wxuin=62924964227315; mm_lang=zh_CN; markHashId_L=395527c2-cd23-499e-a2e7-9c312e109946; poc_sid=HKmTYGmj_n_aFQdJIQMMO1Mso2mfX-j0ErRCaF_y; bizuin=3919532824; slave_bizuin=3919532824; noticeLoginFlag=1; remember_acct=a582798963%40qq.com; rand_info=CAESIO//HMdZ91PqrElHwOfR9Ghh3S5rO9S6MGqldyZtkJdt; data_bizuin=3919532824; data_ticket=Iz5ZwVACO2D1UZJGXk+99ir/MzkwTgNRciKb7navsXoUW8ykAbRE8n9+OyxuwEHV; slave_sid=dFBza2Rra3p5T0RPd01zZXJPMjRWTEtmcU9HQTM1aXhRNXZOWHI5UjNhbmxtTUU5TkhNR0xRdzdhU01NRWg0Y1RHYmwxTm96NEUwRnJncmhmd0toenhCZndXZzRMcUZNX1IwVjZIdGNxS05KX3hzeWVUUmtvY1RQZWE2S0tFR3V3YlZ0WTlNQnN5WGpGbmp0; slave_user=gh_ad0f44a6e5af; xid=6c2e96726bde57e31ac94b3a3a8d96d4; openid2ticket_oGFOf6ZHHVIE-A0EvwCxLNsR90Zk=r8WEeFHmVUrgsmeWo7cBb2SPz38J7qpnxjEY2HvIpwg=; _clck=3919532824|1|g2v|0; _clsk=1wfk5sr|1768907474095|4|1|mp.weixin.qq.com/weheat-agent/payload/record',
    # 'Cookie': 'ua_id=djbTRSOBzk0T0ZGPAAAAALe0IOEssmMccWUeO0lAMF8=; wxuin=63485095923111; pac_uid=0_d4j6SzdciXZJE; omgid=0_d4j6SzdciXZJE; _qimei_uuid42=19c0912270b100c2e088a8e08d002b3cd12f7fc79a; _qimei_fingerprint=c77635264a41ca519315bbdaa83833fa; _qimei_q32=7b8a9b13cb105d751c2081e5185e4854; _qimei_h38=fded44b5e088a8e08d002b3c0200000ad19c09; _qimei_q36=; uuid=0ec594aa1c15fe5e57b9edea46a3e675; rand_info=CAESIOChSC5GBPPAycaIsW8NDNY95i54K897y/zwgh+Hnslh; slave_bizuin=3919532824; data_bizuin=3919532824; bizuin=3919532824; data_ticket=k+Jei0qJ/ahwGSC5kFUX8kxNacKlhS+N5nysp+iOHfWon7IglzoJuPc3YKyxg76k; slave_sid=bVhuRjZaaktZZjhlWjdWMWMzdW1LSzlNRDdkQVJRZFJSVEZCMlFGVXhIcUVnclJlcWVkQzk4T1hqT0ZMcExadnl5VGhENU9yTGJ4eDlqUVZlMGEzV3JlVlMzaEhaNXVZbndnOGIwek5XTkVrSk9YR2JZOTlRQXVWMTkwQ1I4UnJkMUJSNlJvV2RjMGFHWFdr; slave_user=gh_ad0f44a6e5af; xid=49334514fa465719c008317fab5190d9; mm_lang=zh_CN; _clck=3919532824|1|g30|0; _clsk=nw77qx|1769360351624|2|1|mp.weixin.qq.com/weheat-agent/payload/record',
    # 'Cookie':'ua_id=djbTRSOBzk0T0ZGPAAAAALe0IOEssmMccWUeO0lAMF8=; wxuin=63485095923111; pac_uid=0_d4j6SzdciXZJE; omgid=0_d4j6SzdciXZJE; _qimei_uuid42=19c0912270b100c2e088a8e08d002b3cd12f7fc79a; _qimei_fingerprint=c77635264a41ca519315bbdaa83833fa; _qimei_q32=7b8a9b13cb105d751c2081e5185e4854; _qimei_h38=fded44b5e088a8e08d002b3c0200000ad19c09; _qimei_q36=; mm_lang=zh_CN; _clck=3919532824|1|g32|0; cert=R0vULK1LCsNaFUytBBtcPx9wzpAUplQv; noticeLoginFlag=1; uuid=b550d5fdfd5ea037e5ff995188b86341; rand_info=CAESIAPpRJAoxIRXc1ZPceH3beTAnUkCdcM581fbJMWYi5JE; slave_bizuin=3919532824; data_bizuin=3919532824; bizuin=3919532824; data_ticket=+uzBEDebLr+X1vaq5nmXpGdsgAZsHmkpITApxIWBaT72PkkV1qUG/o3oYqKmRee0; slave_sid=WWE4MXN1OXV1bFZVVWlrZmduY0Z1djRxN09GdXlScU9HZTRrNUdNQWV1OUdDYmZSMW0yQmo1SlpNM0swdElVS1BySXJZUkRqWFVwNW5rdUpReXZaTWJXZ0JzWV8zOGxFbUNXUUVNNGZXNzRUdUVXS0dTejhDeDl5RDlFRng5VWMzVU5XOGtzeUJ2ajdUTWFM; slave_user=gh_ad0f44a6e5af; xid=0638dd01830419278cc9fd337b28d70f; _clsk=1i6cgmj|1769537013419|2|1|mp.weixin.qq.com/weheat-agent/payload/record',
    # 'Cookie': 'ua_id=djbTRSOBzk0T0ZGPAAAAALe0IOEssmMccWUeO0lAMF8=; wxuin=63485095923111; pac_uid=0_d4j6SzdciXZJE; omgid=0_d4j6SzdciXZJE; _qimei_uuid42=19c0912270b100c2e088a8e08d002b3cd12f7fc79a; _qimei_fingerprint=c77635264a41ca519315bbdaa83833fa; _qimei_q32=7b8a9b13cb105d751c2081e5185e4854; _qimei_h38=fded44b5e088a8e08d002b3c0200000ad19c09; _qimei_q36=; _clck=ujiaxh|1|g2y|0; uuid=0ec594aa1c15fe5e57b9edea46a3e675; rand_info=CAESIOChSC5GBPPAycaIsW8NDNY95i54K897y/zwgh+Hnslh; slave_bizuin=3919532824; data_bizuin=3919532824; bizuin=3919532824; data_ticket=k+Jei0qJ/ahwGSC5kFUX8kxNacKlhS+N5nysp+iOHfWon7IglzoJuPc3YKyxg76k; slave_sid=bVhuRjZaaktZZjhlWjdWMWMzdW1LSzlNRDdkQVJRZFJSVEZCMlFGVXhIcUVnclJlcWVkQzk4T1hqT0ZMcExadnl5VGhENU9yTGJ4eDlqUVZlMGEzV3JlVlMzaEhaNXVZbndnOGIwek5XTkVrSk9YR2JZOTlRQXVWMTkwQ1I4UnJkMUJSNlJvV2RjMGFHWFdr; slave_user=gh_ad0f44a6e5af; xid=49334514fa465719c008317fab5190d9; mm_lang=zh_CN; _clsk=1fpk4z7|1769127645317|1|1|mp.weixin.qq.com/weheat-agent/payload/record',
    'Cookie': 'appmsglist_action_3919532824=card; pgv_pvid=8293164550; fqm_pvqid=d76b92a8-206f-41de-bdd0-0e0ad8ec1590; ua_id=xVawqYeVZqYkAEmGAAAAABn9ED7qJlRhXvoB45_2b6k=; wxuin=75468010741125; mm_lang=zh_CN; _clck=3919532824|1|g5s|0; uuid=0454d6c83f532dce9644b7f4952b6fd5; rand_info=CAESIHo3Q8YJECz2hEhagj2unKnH4FEt+PSpL9LCcbUJ1V5s; slave_bizuin=3919532824; data_bizuin=3919532824; bizuin=3919532824; data_ticket=uhuIiMtQLZ1Gg60QS37jbt1NqJSbf8eliHduf5eG4T2X6eq+wegaSUUHIzZy5oFx; slave_sid=M3Y0Mk9yQ3EyUnpMdlNYMmhxa29zMG81cU1kTFRyODFMNkRKRVcyZHZ6VDliN3hzZ21jRVdMa1Z0aDBLZDJhNjJyZGJuWnZLZjRnMnJqWFphTFg3NGpMYk9CMkNJVVl4aUtmempFdTNTTjJYc2hBcXRYbTU1NEdkSEExbDhXcjQ2QnRXamY4cTd5OHJvODdZ; slave_user=gh_ad0f44a6e5af; xid=b5ecdf38a824d83374510ef5c874acc3; _clsk=gwssgv|1778007714144|1|1|mp.weixin.qq.com/weheat-agent/payload/record',
    'x-requested-with': 'XMLHttpRequest',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
    'referer': f'https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit_v2&action=edit&isNew=1&type=77&createType=0&token={WEIXIN_CONFIG["TOKEN_ID"]}&lang=zh_CN',
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
}

# 微信文章详情请求头 (用于文章页面)

HEADERS_WEIXIN_DETAIL = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    # 'Cookie': '_qimei_uuid42=19a0b0e0321100feae4f6672aa9a900553e9872200; _qimei_fingerprint=ec639a8ea13c99d3a3d2ed4039da668a; _qimei_q36=; _qimei_h38=21de693eae4f6672aa9a90050200000da19a0b; RK=fGm0tB+fPQ; ptcz=bc0403bd782d82a11003786b608ee095440dd67d9796f2c42f380cf3a4febad6; pac_uid=0_AATfwJjP0R7aF; omgid=0_AATfwJjP0R7aF; ua_id=mfXzRh1QWDO5fqRKAAAAABHITwAC_lXT-nr2-cmMLf4=; wxuin=62924964227315; mm_lang=zh_CN; markHashId_L=395527c2-cd23-499e-a2e7-9c312e109946; poc_sid=HKmTYGmj_n_aFQdJIQMMO1Mso2mfX-j0ErRCaF_y; bizuin=3919532824; slave_bizuin=3919532824; noticeLoginFlag=1; remember_acct=a582798963%40qq.com; rand_info=CAESIO//HMdZ91PqrElHwOfR9Ghh3S5rO9S6MGqldyZtkJdt; data_bizuin=3919532824; data_ticket=Iz5ZwVACO2D1UZJGXk+99ir/MzkwTgNRciKb7navsXoUW8ykAbRE8n9+OyxuwEHV; slave_sid=dFBza2Rra3p5T0RPd01zZXJPMjRWTEtmcU9HQTM1aXhRNXZOWHI5UjNhbmxtTUU5TkhNR0xRdzdhU01NRWg0Y1RHYmwxTm96NEUwRnJncmhmd0toenhCZndXZzRMcUZNX1IwVjZIdGNxS05KX3hzeWVUUmtvY1RQZWE2S0tFR3V3YlZ0WTlNQnN5WGpGbmp0; slave_user=gh_ad0f44a6e5af; xid=6c2e96726bde57e31ac94b3a3a8d96d4; openid2ticket_oGFOf6ZHHVIE-A0EvwCxLNsR90Zk=r8WEeFHmVUrgsmeWo7cBb2SPz38J7qpnxjEY2HvIpwg=; _clck=3919532824|1|g2v|0; _clsk=1wfk5sr|1768908512809|5|1|mp.weixin.qq.com/weheat-agent/payload/record; rewardsn=; wxtokenkey=777'
    # 'Cookie': 'ua_id=djbTRSOBzk0T0ZGPAAAAALe0IOEssmMccWUeO0lAMF8=; wxuin=63485095923111; pac_uid=0_d4j6SzdciXZJE; omgid=0_d4j6SzdciXZJE; _qimei_uuid42=19c0912270b100c2e088a8e08d002b3cd12f7fc79a; _qimei_fingerprint=c77635264a41ca519315bbdaa83833fa; _qimei_q32=7b8a9b13cb105d751c2081e5185e4854; _qimei_h38=fded44b5e088a8e08d002b3c0200000ad19c09; _qimei_q36=; _clck=ujiaxh|1|g2y|0; uuid=0ec594aa1c15fe5e57b9edea46a3e675; rand_info=CAESIOChSC5GBPPAycaIsW8NDNY95i54K897y/zwgh+Hnslh; slave_bizuin=3919532824; data_bizuin=3919532824; bizuin=3919532824; data_ticket=k+Jei0qJ/ahwGSC5kFUX8kxNacKlhS+N5nysp+iOHfWon7IglzoJuPc3YKyxg76k; slave_sid=bVhuRjZaaktZZjhlWjdWMWMzdW1LSzlNRDdkQVJRZFJSVEZCMlFGVXhIcUVnclJlcWVkQzk4T1hqT0ZMcExadnl5VGhENU9yTGJ4eDlqUVZlMGEzV3JlVlMzaEhaNXVZbndnOGIwek5XTkVrSk9YR2JZOTlRQXVWMTkwQ1I4UnJkMUJSNlJvV2RjMGFHWFdr; slave_user=gh_ad0f44a6e5af; xid=49334514fa465719c008317fab5190d9; mm_lang=zh_CN; _clsk=1fpk4z7|1769127645317|1|1|mp.weixin.qq.com/weheat-agent/payload/record'
    # 'Cookie': 'ua_id=djbTRSOBzk0T0ZGPAAAAALe0IOEssmMccWUeO0lAMF8=; wxuin=63485095923111; pac_uid=0_d4j6SzdciXZJE; omgid=0_d4j6SzdciXZJE; _qimei_uuid42=19c0912270b100c2e088a8e08d002b3cd12f7fc79a; _qimei_fingerprint=c77635264a41ca519315bbdaa83833fa; _qimei_q32=7b8a9b13cb105d751c2081e5185e4854; _qimei_h38=fded44b5e088a8e08d002b3c0200000ad19c09; _qimei_q36=; mm_lang=zh_CN; _clck=3919532824|1|g32|0; cert=R0vULK1LCsNaFUytBBtcPx9wzpAUplQv; noticeLoginFlag=1; uuid=b550d5fdfd5ea037e5ff995188b86341; rand_info=CAESIAPpRJAoxIRXc1ZPceH3beTAnUkCdcM581fbJMWYi5JE; slave_bizuin=3919532824; data_bizuin=3919532824; bizuin=3919532824; data_ticket=+uzBEDebLr+X1vaq5nmXpGdsgAZsHmkpITApxIWBaT72PkkV1qUG/o3oYqKmRee0; slave_sid=WWE4MXN1OXV1bFZVVWlrZmduY0Z1djRxN09GdXlScU9HZTRrNUdNQWV1OUdDYmZSMW0yQmo1SlpNM0swdElVS1BySXJZUkRqWFVwNW5rdUpReXZaTWJXZ0JzWV8zOGxFbUNXUUVNNGZXNzRUdUVXS0dTejhDeDl5RDlFRng5VWMzVU5XOGtzeUJ2ajdUTWFM; slave_user=gh_ad0f44a6e5af; xid=0638dd01830419278cc9fd337b28d70f; _clsk=1i6cgmj|1769537013419|2|1|mp.weixin.qq.com/weheat-agent/payload/record',
    # 'Cookie':'ua_id=djbTRSOBzk0T0ZGPAAAAALe0IOEssmMccWUeO0lAMF8=; wxuin=63485095923111; pac_uid=0_d4j6SzdciXZJE; omgid=0_d4j6SzdciXZJE; _qimei_uuid42=19c0912270b100c2e088a8e08d002b3cd12f7fc79a; _qimei_fingerprint=c77635264a41ca519315bbdaa83833fa; _qimei_q32=7b8a9b13cb105d751c2081e5185e4854; _qimei_h38=fded44b5e088a8e08d002b3c0200000ad19c09; _qimei_q36=; mm_lang=zh_CN; noticeLoginFlag=1; _clck=3919532824|1|g3b|0; uuid=ee59716d8326b8897f632f17922b5047; rand_info=CAESIO7gNPEwi6bwHKurE+3sdNTdE7tTfeemCBg/cDouiekC; slave_bizuin=3919532824; data_bizuin=3919532824; bizuin=3919532824; data_ticket=pf3JEEjXuLIDv3MNkpBRquRXhmwzGnEhrjcVItoSXJqYyXp8AvcdPfRD/u5W7hXY; slave_sid=aDJZMmRBZHNOSzEwQUNWRHZqVTZoM0JzakN0TUNCWmZPRFoyYnU0dGhVZm9HSlo4MVU4QTd6cktfVkc3YXRoUTdWQ25JN3lGa0RLZjhma1FrR2NCenFzUHIzYXhycDdlYUlDVXUwanBMWU5USTBRcHZ0cm9QSVlxZXNMTW84S24xN2FHbUJOVHZiWnd0cU51; slave_user=gh_ad0f44a6e5af; xid=214d7f1519b1f9cea1621b53f61d6b65; _clsk=1s7i2m9|1770318547007|2|1|mp.weixin.qq.com/weheat-agent/payload/record'
    # 'Cookie':'ua_id=djbTRSOBzk0T0ZGPAAAAALe0IOEssmMccWUeO0lAMF8=; wxuin=63485095923111; pac_uid=0_d4j6SzdciXZJE; omgid=0_d4j6SzdciXZJE; _qimei_uuid42=19c0912270b100c2e088a8e08d002b3cd12f7fc79a; _qimei_fingerprint=c77635264a41ca519315bbdaa83833fa; _qimei_q32=7b8a9b13cb105d751c2081e5185e4854; _qimei_h38=fded44b5e088a8e08d002b3c0200000ad19c09; _qimei_q36=; mm_lang=zh_CN; RK=rGj2sh+kcQ; ptcz=d76940992fa1150f1ab2eb351158a30d4eb9c5b7e685c8a13b51aa894a48d905; _clck=3919532824|1|g46|0; uuid=a912586f55dff9355b4d901182f78c64; rand_info=CAESIDiCgXR0cc0mVwk0v4i51HOoV4W9G6Ksd/7ymeThCtmi; slave_bizuin=3919532824; data_bizuin=3919532824; bizuin=3919532824; data_ticket=71ALVjT2EwbvsEZyPXlxSKgnE8yCbveSUN+KcY+/02yKSBKvSvpDhbSxZNM1SHk5; slave_sid=NFJISm1QUmNsV3hoaTF3Wk5ZT09UVmlwQXRVX1JBZlpEOEF6QjVEa3NIaG91RGlKTk8wY0NJV1E3RW9oMjVfRTV5N0QxQzJUMEJCQ2c0VWpVdkI0VVh5ZkxUdnRFRks0TkpGQk9OSnpLQXhzMFY4WHd4WEFCdjNWNjVrOFRKbTlpY2o5WFNVU093MXE1R2NS; slave_user=gh_ad0f44a6e5af; xid=3471dd1c46a9bf0e85e94b900aeb4b7b; _clsk=cp368i|1772990174160|1|1|mp.weixin.qq.com/weheat-agent/payload/record'
    'Cookie': 'appmsglist_action_3919532824=card; pgv_pvid=8293164550; fqm_pvqid=d76b92a8-206f-41de-bdd0-0e0ad8ec1590; ua_id=xVawqYeVZqYkAEmGAAAAABn9ED7qJlRhXvoB45_2b6k=; wxuin=75468010741125; mm_lang=zh_CN; _clck=3919532824|1|g5s|0; uuid=0454d6c83f532dce9644b7f4952b6fd5; rand_info=CAESIHo3Q8YJECz2hEhagj2unKnH4FEt+PSpL9LCcbUJ1V5s; slave_bizuin=3919532824; data_bizuin=3919532824; bizuin=3919532824; data_ticket=uhuIiMtQLZ1Gg60QS37jbt1NqJSbf8eliHduf5eG4T2X6eq+wegaSUUHIzZy5oFx; slave_sid=M3Y0Mk9yQ3EyUnpMdlNYMmhxa29zMG81cU1kTFRyODFMNkRKRVcyZHZ6VDliN3hzZ21jRVdMa1Z0aDBLZDJhNjJyZGJuWnZLZjRnMnJqWFphTFg3NGpMYk9CMkNJVVl4aUtmempFdTNTTjJYc2hBcXRYbTU1NEdkSEExbDhXcjQ2QnRXamY4cTd5OHJvODdZ; slave_user=gh_ad0f44a6e5af; xid=b5ecdf38a824d83374510ef5c874acc3; _clsk=gwssgv|1778007714144|1|1|mp.weixin.qq.com/weheat-agent/payload/record',
}
# 请求重试配置
REQUEST_RETRIES = 3      # 最大重试次数
REQUEST_TIMEOUT = 18     # 请求超时时间 (秒)
REQUEST_DELAY_MIN = 0.8  # 最小随机延迟 (秒)
REQUEST_DELAY_MAX = 2.0  # 最大随机延迟 (秒)


# ================= 5. 日志与存储配置 (Log & Storage) =================
# 日志文件路径
LOG_DIR = "logs"
LOG_ROTATION = "1 day"   # 日志轮转周期
LOG_RETENTION = "10 days" # 日志保留时间

# 数据存储路径
DATA_DIR = "data"

