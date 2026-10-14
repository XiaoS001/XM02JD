# -*- coding: utf-8 -*-
"""S6 转化追踪：漏斗统计 + 归因

模拟"触达后有部分线索响应→有意向→成交"的转化过程，
输出漏斗，定位流失最大的环节。
"""
import json
import os
import random
from config import SCORED_FILE, OUTREACH_FILE, FUNNEL_FILE

random.seed(20261014)

# 各阶段转化率（模拟，实际应来自 CRM 真实数据）
RATES = {"response": 0.35, "interest": 0.5, "deal": 0.3}

def track(scored_file, outreach_file, out_path):
    with open(scored_file, "r", encoding="utf-8") as f:
        scored = json.load(f)
    with open(outreach_file, "r", encoding="utf-8") as f:
        outreach = json.load(f)

    # 触达基数 = A/B 级线索
    contacted = [o for o in outreach if o["status"] == "mock_sent"]
    n_contacted = len(contacted)

    responded = [c for c in contacted if random.random() < RATES["response"]]
    interested = [c for c in responded if random.random() < RATES["interest"]]
    deals = [c for c in interested if random.random() < RATES["deal"]]

    funnel = {
        "总线索": len(scored),
        "A/B级可触达": n_contacted,
        "响应": len(responded),
        "有意向": len(interested),
        "成交": len(deals),
    }
    # 计算各环节转化率
    rates = {}
    prev = len(scored)
    for stage, cur in funnel.items():
        rates[stage] = round(cur / prev, 4) if prev else 0
        prev = cur if cur else prev

    result = {"funnel": funnel, "rates": rates}

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    return result

if __name__ == "__main__":
    r = track(SCORED_FILE, OUTREACH_FILE, FUNNEL_FILE)
    print(f"S6 完成：漏斗统计 -> {FUNNEL_FILE}")
    print("   漏斗:", r["funnel"])
    print("   转化率:", r["rates"])
