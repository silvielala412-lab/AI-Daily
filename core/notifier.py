# -*- coding: utf-8 -*-
"""
邮件通知模块
负责发送 运行报告(带附件) 和 紧急告警。
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from core.logger import log
from config.settings import SMTP_CONFIG, ENABLE_EMAIL_ALERT

from email.utils import formataddr

class EmailNotifier:
    def __init__(self):
        self.config = SMTP_CONFIG
        self.enabled = ENABLE_EMAIL_ALERT

    def _send(self, subject, content, attachment_path=None):
        """内部发送逻辑"""
        if not self.enabled:
            log.warning("邮件功能未开启，跳过发送")
            return False

        try:
            message = MIMEMultipart()
            message['From'] = formataddr(["AI Assistant", self.config['user']])

            # 2. 设置收件人
            # 注意：收件人列表不能用 Header 包裹，否则多于一个收件人时会报错
            message['To'] = ",".join(self.config['receivers'])

            # 3. 设置主题 (主题包含中文，必须用 Header)
            message['Subject'] = Header(subject, 'utf-8')

            # --- 修改结束 ---

            # 正文
            message.attach(MIMEText(content, 'plain', 'utf-8'))

            # 附件
            if attachment_path:
                try:
                    with open(attachment_path, 'rb') as f:
                        att = MIMEText(f.read(), 'base64', 'utf-8')
                        att["Content-Type"] = 'application/octet-stream'
                        filename = os.path.basename(attachment_path)
                        att["Content-Disposition"] = f'attachment; filename="{filename}"'
                        message.attach(att)
                except Exception as e:
                    log.error(f"附件读取失败: {e}")

            # 连接SMTP服务器
            server = smtplib.SMTP_SSL(self.config['host'], self.config['port'])
            server.login(self.config['user'], self.config['password'])
            server.sendmail(self.config['user'], self.config['receivers'], message.as_string())
            server.quit()
            
            log.info(f"邮件发送成功: {subject}")
            return True

        except Exception as e:
            log.error(f"邮件发送失败: {e}")
            return False

    def send_alert(self, error_msg):
        """发送紧急告警"""
        subject = "【爬虫告警】任务执行异常"
        content = f"爬虫任务在执行过程中发生错误：\n\n{error_msg}\n\n请及时检查服务器日志。"
        return self._send(subject, content)

    def send_report(self, summary, attachment_path):
        """发送日报 (带附件)"""
        subject = f"【AI日报】爬虫任务完成 - {summary}"
        content = f"任务已完成。\n{summary}\n\n详细数据请查看附件。"
        return self._send(subject, content, attachment_path)

# 单例模式导出
import os
notifier = EmailNotifier()
