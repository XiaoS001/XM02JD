# -*- coding: utf-8 -*-
"""P01 全局配置"""

# 模拟数据规模
TARGET_COMPANIES = 120          # 生成企业总数
# 数据源文件
RAW_FILE = "data/raw_companies.json"
LEADS_FILE = "data/leads.json"
CLEAN_FILE = "data/leads_clean.json"
SCORED_FILE = "data/leads_scored.json"
OUTREACH_FILE = "data/outreach.json"
FUNNEL_FILE = "data/funnel.json"

# 邮箱校验（简单正则，不引第三方）
# 行业 → 目标客户判定
TARGET_INDUSTRIES = ["电商", "SaaS", "本地服务", "教育", "金融", "医疗", "制造业", "物流"]

# MySQL（尝试连接，失败则自动降级为本地 JSON）
DB = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "Wms@2026Root",
    "database": "leadgen",
}
