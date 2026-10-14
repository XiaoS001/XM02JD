# -*- coding: utf-8 -*-
"""M4 询盘漏斗：曝光→点击→询盘→试听→成单，带来源归因

对应 JD 职责 6"监测AI引用数据与询盘转化"+ 要求 3"可量化实战成果"
"""
import json, os, random, hashlib
from config import KW_FILE, CITATION_FILE, FUNNEL_FILE, FUNNEL_RATES

random.seed(20261016)

def run(kw_file, cit_file, out_path):
    with open(kw_file, "r", encoding="utf-8") as f:
        keywords = json.load(f)
    with open(cit_file, "r", encoding="utf-8") as f:
        cit = json.load(f)

    # 曝光：由 AI 引用 + 自然搜索构成（引用越多曝光越高）
    total_citations = cit["total_current"]
    exposure = total_citations * 45 + 3000          # 模拟曝光基数
    clicks = int(exposure * FUNNEL_RATES["click"])
    inquiries = int(clicks * FUNNEL_RATES["inquiry"])
    trials = int(inquiries * FUNNEL_RATES["trial"])
    deals = int(trials * FUNNEL_RATES["deal"])

    funnel = {
        "曝光": exposure,
        "点击": clicks,
        "询盘": inquiries,
        "试听": trials,
        "成单": deals,
    }
    rates, prev = {}, None
    for stage, v in funnel.items():
        rates[stage] = 1.0 if prev is None else round(v / prev, 4) if prev else 0
        prev = v

    # 归因：按关键词优先级 × 引用数分配询盘
    detail = cit["detail"]
    scored = []
    for r in detail:
        if r["citations"] <= 0: continue
        kw = next((k for k in keywords if k["keyword"] == r["keyword"]), None)
        if not kw: continue
        h = int(hashlib.md5((r["keyword"] + "inq").encode()).hexdigest(), 16)
        inq = max(0, int(r["citations"] * FUNNEL_RATES["click"] * FUNNEL_RATES["inquiry"] * 10) + (h % 4) - 2)
        if inq > 0:
            scored.append({
                "keyword": r["keyword"], "platform": r["platform"],
                "category": kw["category"], "citations": r["citations"],
                "inquiries": inq,
                "cost_per_inquiry": round(round(300 + h % 200, 2) / max(1, inq), 1),  # 模拟获客成本
            })
    scored.sort(key=lambda x: -x["inquiries"])

    result = {
        "funnel": funnel, "rates": rates,
        "attribution_top10": scored[:10],
        "by_category": {},
    }
    # 按词类别汇总询盘
    from collections import defaultdict
    cat = defaultdict(int)
    for s in scored: cat[s["category"]] += s["inquiries"]
    result["by_category"] = dict(cat)
    result["total_inquiries_attribution"] = sum(cat.values())

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    return result

if __name__ == "__main__":
    from config import FUNNEL_FILE
    r = run(KW_FILE, CITATION_FILE, FUNNEL_FILE)
    print(f"M4 完成：询盘漏斗 -> {FUNNEL_FILE}")
    print("   漏斗:", r["funnel"])
    print("   转化率:", r["rates"])
    print("   询盘归因 Top5:")
    for s in r["attribution_top10"][:5]:
        print(f"     {s['keyword']} [{s['platform']}] 询盘 {s['inquiries']}，单询盘成本 ¥{s['cost_per_inquiry']}")
