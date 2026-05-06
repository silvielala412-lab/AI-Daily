import json

def format_AiBasetitle(title: str) -> str:
    """
    移除标题开头的 单数字+顿号(、)，返回格式化后的纯标题
    :param title: 原始带序号的标题字符串
    :return: 格式化后的纯标题
    """
    # 判断开头是否是【数字+顿号】结构，是则从索引2开始切片，否则返回原标题
    if len(title) >= 2 and title[0].isdigit() and title[1] == '、':
        return title[2:].strip()
    return title.strip()