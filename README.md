# AI 新闻聚合爬虫系统 (Enterprise AI News Crawler)

这是一个企业级的全网AI新闻爬取、分析与聚合平台。支持多数据源、DeepSeek 智能分析、自动邮件告警以及定时任务调度。

## 📁 目录结构

```text
AI_News_Crawler/
├── config/
│   ├── settings.py       # 全局配置文件 (AK、邮箱、开关)
├── core/
│   ├── logger.py         # 日志模块
│   ├── network.py        # 网络请求 (自动重试、反爬)
│   ├── notifier.py       # 邮件通知
│   ├── ai_analyzer.py    # DeepSeek AI 分析
├── spiders/
│   ├── base.py           # 爬虫基类
│   ├── xinzhiyuan.py     # 新智元
│   ├── jiqizhixin.py     # 机器之心
│   ├── aibase.py         # AI Base
├── data/                 # 结果数据 (Excel)
├── logs/                 # 运行日志
├── main.py               # 主程序 (任务调度)
└── requirements.txt      # 依赖包
```

## 🚀 快速开始

### 1. 安装依赖

确保 Python 版本 >= 3.8

```bash
pip install -r requirements.txt
```

### 2. 配置参数

打开 `config/settings.py`，重点修改以下内容：

- **DEEPSEEK_API_KEY**: 填入你的 DeepSeek API Key。
- **SMTP_CONFIG**: 填入你的发件邮箱服务器、账号和密码 (用于接收日报和告警)。
- **ENABLE_AI_ANALYSIS**: `True` 为开启AI打分，`False` 仅抓取。

### 3. 运行爬虫

**测试运行 (执行一次):**
打开 `main.py`，确保最后一行是 `job_crawl_mission()`，然后运行：

```bash
python main.py
```

**正式部署 (定时任务):**
打开 `main.py`，注释掉 `job_crawl_mission()`，解开 `main()` 中的 `scheduler.start()`，然后运行：

```bash
python main.py
```
程序将会在每天早上 8:00 自动执行抓取。

## 🛠️ 二次开发

### 添加新数据源

1. 在 `spiders/` 目录下新建 `mysource.py`。
2. 继承 `BaseSpider` 类，实现 `run()` 方法。
3. 在 `spiders/__init__.py` 中导入并添加到 `ALL_SPIDERS` 列表中。

### 开启邮件告警

在 `config/settings.py` 中设置 `ENABLE_EMAIL_ALERT = True`，并正确配置 SMTP 信息。当爬虫遇到严重错误或完成每日任务时，会自动发送邮件。

## 📊 日志查看

所有运行日志会自动保存在 `logs/` 目录下，每天轮转一个文件，方便追溯。
