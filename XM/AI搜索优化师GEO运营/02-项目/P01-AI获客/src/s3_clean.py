# -*- coding: utf-8 -*-
"""S3 清洗验证：去重、补全、邮箱格式校验

关键点（面试可讲）：
- 去重：以公司名+城市为唯一键，去掉重复线索
- 邮箱校验：正则判断格式合法性，非法/缺失的标记出来（不能假装它们不存在）
- 补全：缺失 website 的用公司名拼音兜底
"""
import json
import os
import re

EMAIL_RE = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")

def clean(leads):
    seen = set()
    cleaned = []
    issues = {"dup": 0, "bad_email": 0, "missing_email": 0, "missing_website": 0}

    for lead in leads:
        key = (lead["company"], lead["city"])
        if key in seen:
            issues["dup"] += 1
            continue
        seen.add(key)

        # 邮箱校验
        email = (lead.get("email") or "").strip()
        if not email:
            issues["missing_email"] += 1
            lead["email_status"] = "missing"
        elif not EMAIL_RE.match(email):
            issues["bad_email"] += 1
            lead["email_status"] = "invalid"
        else:
            lead["email_status"] = "valid"

        # 补全 website
        if not lead.get("website"):
            issues["missing_website"] += 1
            lead["website"] = "https://www." + lead["company"].replace(" ", "") + ".com"
            lead["website_filled"] = True

        cleaned.append(lead)

    return cleaned, issues

def run(in_path, out_path):
    with open(in_path, "r", encoding="utf-8") as f:
        leads = json.load(f)
    cleaned, issues = clean(leads)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, ensure_ascii=False, indent=2)
    return len(cleaned), issues

if __name__ == "__main__":
    from config import LEADS_FILE, CLEAN_FILE
    n, issues = run(LEADS_FILE, CLEAN_FILE)
    print(f"S3 完成：清洗后 {n} 条线索 -> {CLEAN_FILE}")
    print("   清洗统计:", issues)
