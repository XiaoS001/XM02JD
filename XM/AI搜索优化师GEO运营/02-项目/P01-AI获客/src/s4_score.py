# -*- coding: utf-8 -*-
"""S4 分类打分：按行业/规模/邮箱有效性给线索分级

规则可解释（面试可讲）：
- 目标行业（TARGET_INDUSTRIES 之外判低）
- 规模：大型/中型 加分
- 邮箱有效 才可能进 A/B 级（没邮箱的没法触达）
最终等级：A(高意向) / B(中意向) / C(低意向/不可触达)
"""
import json
import os
from config import TARGET_INDUSTRIES

def score(lead):
    s = 0
    if lead["industry"] in TARGET_INDUSTRIES:
        s += 2
    if lead["scale"] in ("大型", "中型"):
        s += 2
    elif lead["scale"] == "小型":
        s += 1
    # 邮箱无效/缺失 -> 无法触达，直接 C
    if lead["email_status"] != "valid":
        lead["grade"] = "C"
        lead["score"] = s
        lead["reason"] = "邮箱不可触达"
        return lead

    if s >= 4:
        lead["grade"] = "A"
    elif s >= 2:
        lead["grade"] = "B"
    else:
        lead["grade"] = "C"
    lead["score"] = s
    lead["reason"] = f"行业{'是' if lead['industry'] in TARGET_INDUSTRIES else '非'}目标/规模{lead['scale']}"
    return lead

def run(in_path, out_path):
    with open(in_path, "r", encoding="utf-8") as f:
        leads = json.load(f)
    scored = [score(l) for l in leads]
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(scored, f, ensure_ascii=False, indent=2)

    from collections import Counter
    dist = Counter(l["grade"] for l in scored)
    return len(scored), dict(dist)

if __name__ == "__main__":
    from config import CLEAN_FILE, SCORED_FILE
    n, dist = run(CLEAN_FILE, SCORED_FILE)
    print(f"S4 完成：{n} 条线索分级 -> {SCORED_FILE}")
    print("   等级分布:", dict(sorted(dist.items())))
