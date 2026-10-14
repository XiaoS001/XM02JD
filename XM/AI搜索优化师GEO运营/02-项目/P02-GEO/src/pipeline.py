# -*- coding: utf-8 -*-
"""P02 端到端编排：M1 → M4 一条命令跑完"""
from config import KW_FILE, CONTENT_FILE, CITATION_FILE, FUNNEL_FILE

def main():
    print("=" * 56)
    print("GEO 关键词矩阵 + AI 引用监测 + 询盘漏斗 启动")
    print("=" * 56)

    import m1_keywords, m2_content, m3_citation, m4_funnel
    from config import CONTENT_SAMPLE, CONTENT_FILE

    n, dist, hp = m1_keywords.run(KW_FILE)
    print(f"[M1 关键词矩阵] {n} 个词 | 分布 {dist} | 高优先级 {hp}")

    rep = m2_content.run(CONTENT_SAMPLE, KW_FILE, CONTENT_FILE)
    print(f"[M2 埋词检查] 覆盖率 {rep['coverage_pct']}% | 命中 {rep['hit_count']} 缺失 {rep['missing_count']} | 密度 {rep['density_pct']}%")

    cit = m3_citation.run(KW_FILE, CITATION_FILE)
    print(f"[M3 引用监测] 总引用 {cit['total_current']}（上期 {cit['total_previous']}，环比 {cit['total_change_pct']:+}%）")
    for p, v in cit["summary"].items():
        print(f"    {p}: {v['current']}（{v['change_pct']:+}%）收录率 {v['index_rate']}%")

    r = m4_funnel.run(KW_FILE, CITATION_FILE, FUNNEL_FILE)
    print(f"[M4 询盘漏斗] {r['funnel']}")
    print(f"    转化率: {r['rates']}")
    print(f"    询盘归因Top5:")
    for s in r["attribution_top10"][:5]:
        print(f"      {s['keyword']} [{s['platform']}] 询盘 {s['inquiries']}，成本 ¥{s['cost_per_inquiry']}")

    print("=" * 56)
    print("P02 全流程完成 [OK]")

    # 量化数字汇总（面试弹药）
    print()
    print(">>> 可量化成果汇总（面试可报数字）<<<")
    print(f"  1. 关键词矩阵总量: {n}")
    print(f"  2. 四类词分布: {dist}")
    print(f"  3. 内容埋词覆盖率: {rep['coverage_pct']}%（密度 {rep['density_pct']}%）")
    print(f"  4. AI 平台总引用: {cit['total_current']} 次")
    print(f"  5. 引用环比变化: {cit['total_change_pct']:+}%")
    print(f"  6. 询盘转化: 曝光 {r['funnel']['曝光']} → 询盘 {r['funnel']['询盘']} → 成单 {r['funnel']['成单']}")

if __name__ == "__main__":
    main()
