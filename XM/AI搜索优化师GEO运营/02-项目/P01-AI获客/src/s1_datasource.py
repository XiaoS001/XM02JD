# -*- coding: utf-8 -*-
"""S1 数据源：生成模拟企业名录

生成逼真的企业记录，模拟"从公开名录/地图/企查查等源头"拿到的原始数据。
刻意埋入一些脏数据（重复、缺字段、非法邮箱），供 S3 清洗验证演示。
"""
import json
import random
import os

random.seed(20261014)  # 固定种子，可复现

INDUSTRIES = ["电商", "SaaS", "本地服务", "教育", "金融", "医疗", "制造业", "物流", "餐饮", "零售"]
CITIES = ["北京", "上海", "深圳", "广州", "杭州", "成都", "武汉", "南京"]
SCALES = ["微型", "小型", "中型", "大型"]  # 规模

def _email(name, i):
    """生成邮箱，埋入部分非法值"""
    if i % 23 == 0: return "not-an-email"          # 非法格式
    if i % 31 == 0: return ""                       # 缺失
    domain = random.choice(["163.com", "qq.com", "gmail.com", "company.cn", "126.com"])
    return f"contact{i}@{domain}"

def generate(n):
    companies = []
    for i in range(n):
        ind = INDUSTRIES[i % len(INDUSTRIES)]
        city = CITIES[i % len(CITIES)]
        scale = SCALES[i % len(SCALES)]
        name = f"{city}{ind}科技{i:03d}号"
        rec = {
            "id": f"RAW{i:04d}",
            "name": name,
            "industry": ind,
            "city": city,
            "scale": scale,
            "email": _email(name, i),
            "phone": f"13{random.randint(100000000, 999999999)}",
            "website": f"https://www.{name.replace(' ', '')}.com" if i % 7 != 0 else "",  # 部分缺失网站
        }
        companies.append(rec)

    # 刻意埋入重复记录（模拟数据源里的重复项）
    if n > 5:
        companies.append(dict(companies[2])); companies[-1]["id"] = "RAWdup-1"
        companies.append(dict(companies[5])); companies[-1]["id"] = "RAWdup-2"

    return companies

def run(out_path):
    data = generate(120)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return len(data)

if __name__ == "__main__":
    from config import RAW_FILE
    n = run(RAW_FILE)
    print(f"S1 完成：生成 {n} 条模拟企业记录 -> {RAW_FILE}")
