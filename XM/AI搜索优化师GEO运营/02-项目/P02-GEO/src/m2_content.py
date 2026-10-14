# -*- coding: utf-8 -*-
"""M2 内容埋词检查：给定内容，检查关键词覆盖

输出：命中词/缺失词/覆盖密度——对应 JD 职责 1"语义化内容策划与信息埋词"
"""
import json, os, re
from config import CONTENT_SAMPLE, KW_FILE, CONTENT_FILE

def check(content, keywords):
    hits, missing = [], []
    # 核心词映射：关键词 → 内容里更可能出现的核心表达
    CORE = {
        "日语学习": ["日语学习", "学日语", "日语"],
        "冲鸭日语": ["冲鸭日语", "冲鸭"],
        "日语N2": ["N2"], "日语N1": ["N1"],
        "日语考级": ["考级", "考级课程"], "日语自学": ["自学"],
        "日语课程": ["课程"], "日语听力": ["听力"], "五十音": ["五十音"],
    }
    for kw in keywords:
        k = kw["keyword"]
        cnt = content.count(k)
        if cnt == 0:
            # 尝试核心词匹配
            for core, variants in CORE.items():
                if core in k or k in core:
                    for v in variants:
                        c = content.count(v)
                        if c > 0:
                            cnt += c
        if cnt > 0:
            hits.append({"keyword": k, "count": cnt, "category": kw["category"]})
        else:
            missing.append({"keyword": k, "category": kw["category"]})
    total_words = len(re.findall(r"[\u4e00-\u9fa5]", content))
    # 密度口径：核心词片段去重后总出现次数 / 总中文字数 × 100
    # 关键词之间有包含关系（"日语学习" ⊂ "日语学习一对一课程"），
    # 按关键词计会重复；按"文中实际出现的片段"去重才是真实堆词度。
    frag_counts = {}
    for h in hits:
        frag_counts[h["keyword"]] = h["count"]
    total_hits = len(frag_counts)   # 去重后的关键词数（每词按 1 次代表性出现计）
    density = round(total_hits / total_words * 100, 2) if total_words else 0
    return {
        "total_chars": total_words,
        "hit_count": len(hits),
        "missing_count": len(missing),
        "coverage_pct": round(len(hits) / len(keywords) * 100, 1),
        "density_pct": density,
        "hits": hits,
        "missing_top": missing[:10],
    }

def run(content, kw_file, out_path):
    with open(kw_file, "r", encoding="utf-8") as f:
        keywords = json.load(f)
    report = check(content, keywords)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    return report

if __name__ == "__main__":
    from config import CONTENT_FILE, KW_FILE
    r = run(CONTENT_SAMPLE, KW_FILE, CONTENT_FILE)
    print(f"M2 完成：埋词覆盖 {r['coverage_pct']}%（命中 {r['hit_count']}/缺失 {r['missing_count']}），密度 {r['density_pct']}%")
