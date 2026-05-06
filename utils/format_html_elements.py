import os
from readability import Document
from bs4 import BeautifulSoup


def clean_html_keep_content_and_img(html_content):
    """
    清理本地HTML文件，只保留正文+图片，去除所有无关内容，修复格式错乱
    html_content:获取核心内容html片段
    final_html:去除无关内容,构建完整html片段
    """


    # 核心：用readability智能提取纯净正文+图片，自动过滤广告/导航/侧边栏等
    doc = Document(html_content)
    clean_html = doc.summary()  # 只保留正文+图片的核心内容

    #二次优化：清理冗余标签，保证本地打开样式整洁
    soup = BeautifulSoup(clean_html, 'html.parser')
    # 删除所有script脚本（无用，会导致本地报错）
    for script in soup.find_all('script'):
        script.decompose()
    # 删除所有style内联样式的冗余内容
    for style in soup.find_all('style'):
        style.decompose()
    # 修复图片标签的格式问题，保证图片正常显示
    for img in soup.find_all('img'):
        if img.get('src') and not img.get('alt'):
            img['alt'] = "正文图片"

    #生成最终的纯净HTML完整结构（带基础样式，保证本地打开排版不乱）
    final_html = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>{doc.title()}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- 基础样式：保证正文排版工整，图片自适应屏幕，无错乱 -->
    <style>
        body {{ max-width: 800px; margin: 0 auto; padding: 20px; font-size: 16px; line-height: 1.8; color: #333; }}
        img {{ max-width: 100%; height: auto; display: block; margin: 20px auto; border-radius: 4px; }}
        p {{ margin: 12px 0; }}
        h1,h2,h3 {{ margin: 20px 0 10px; color: #222; }}
        a {{ color: #0078d7; text-decoration: none; }}
        * {{ box-sizing: border-box; }}
    </style>
</head>
<body>
    {soup.prettify()}
</body>
</html>
    """
    return  final_html
