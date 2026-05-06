from .xinzhiyuan import XinzhiyuanSpider
from .jiqizhixin import JiqizhixinSpider
from .aibase import AIBaseSpider
from .weixin import WeixinSpider

# 注册所有爬虫类
ALL_SPIDERS = [
    XinzhiyuanSpider,
    JiqizhixinSpider,
    AIBaseSpider,
    WeixinSpider
]
