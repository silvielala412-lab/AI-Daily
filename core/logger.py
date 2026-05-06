# -*- coding: utf-8 -*-
"""
日志模块
使用 Loguru 封装，支持控制台输出和文件自动轮转。
"""

import os
import sys
from loguru import logger
from config.settings import LOG_DIR, LOG_ROTATION, LOG_RETENTION

# 确保日志目录存在
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# 移除默认的 handler
logger.remove()

# 添加控制台输出 (Log Level: INFO)
logger.add(
    sys.stderr,
    level="INFO",
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{module}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
)

# 添加文件输出 (每天轮转，保留10天)
log_file_path = os.path.join(LOG_DIR, "crawler_runtime.log")
logger.add(
    log_file_path,
    rotation=LOG_ROTATION,
    retention=LOG_RETENTION,
    level="DEBUG",
    encoding="utf-8",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {module}:{line} - {message}"
)

# 导出 logger 实例
log = logger
