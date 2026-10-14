# -*- coding: utf-8 -*-
"""M3 AI 平台引用监测：模拟 5 大平台对品牌词的引用情况

对应 JD 职责 3（多平台内容植入）、5（跟踪收录/召回/引用变化）
输出：平台 x 关键词 的引用矩阵 + 本期/上期对比（环比）
"""
import json, os, random, hashlib
from config import AI_PLATFORMS, KW_FILE, CITATION_FILE, BRAND

random.seed(20261015)

# 平台基础引用倾向（模拟各平台生态差异）
PLATFORM_BASE = {"豆包": 1.0, "元宝": 0.85, "DeepSeek": 1.15, "千问": 0.9, "文心一言": 0.8}

def platform_citations(platform, keywords, period_shift=0):
    """生成某平台对各关键词的引用记录"""
    base = PLATFORM_BASE[platform]
    rows = []
    for kw in keywords:
        h = int(hashlib.md5((platform + kw["keyword"] + str(period_shift)).encode()).hexdigest(), 16)
        # 引用次数受关键词优先级、竞争度、平台倾向影响
        weight = kw["priority"] / 10 + (10 - kw["competition"]) / 5
        cites = max(0, int(weight * base * 2.2) + (h % 7) - 3 + period_shift)
        indexed = cites > 0
        rows.append({
            "platform": platform,
            "keyword": kw["keyword"],
            "category": kw["category"],
            "citations": cites,
            "indexed": indexed,
        })
    return rows

def run(kw_file, out_path):
    with open(kw_file, "r", encoding="utf-8") as f:
        keywords = json.load(f)

    # 本期 + 上期（用于环比）
    current, previous = [], []
    for p in AI_PLATFORMS:
        current.extend(platform_citations(p, keywords, 0))
        previous.extend(platform_citations(p, keywords, -1))

    # 汇总
    def agg(rows):
        by_plat = {}
        for r in rows:
            d = by_plat.setdefault(r["platform"], {"citations": 0, "indexed": 0, "keywords": 0})
            d["citations"] += r["citations"]
            d["keywords"] += 1
            if r["indexed"]: d["indexed"] += 1
        return by_plat

    cur_agg, prev_agg = agg(current), agg(previous)
    trend = {}
    for p in AI_PLATFORMS:
        c, pr = cur_agg[p]["citations"], prev_agg[p]["citations"]
        trend[p] = {
            "current": c, "previous": pr,
            "change": c - pr,
            "change_pct": round((c - pr) / pr * 100, 1) if pr else 0,
            "index_rate": round(cur_agg[p]["indexed"] / cur_agg[p]["keywords"] * 100, 1),
        }

    result = {"detail": current, "summary": trend,
              "total_current": sum(v["current"] for v in trend.values()),
              "total_previous": sum(v["previous"] for v in trend.values())}
    result["total_change_pct"] = round(
        (result["total_current"] - result["total_previous"]) / result["total_previous"] * 100, 1)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    return result

if __name__ == "__main__":
    from config import CITATION_FILE
    r = run(KW_FILE, CITATION_FILE)
    print(f"M3 完成：5 平台引用监测 -> {CITATION_FILE}")
    print(f"   总引用 {r['total_current']} 次（上期 {r['total_previous']}，环比 {r['total_change_pct']:+}%）")
    for p, v in r["summary"].items():
        print(f"   {p}: {v['current']} 次 ({v['change_pct']:+}%) 收录率 {v['index_rate']}%")
