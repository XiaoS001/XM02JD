# -*- coding: utf-8 -*-
"""P01 端到端编排：S1 → S6 一条命令跑完

用法：python pipeline.py
"""
import json
from config import RAW_FILE, LEADS_FILE, CLEAN_FILE, SCORED_FILE, OUTREACH_FILE, FUNNEL_FILE

def main():
    print("=" * 50)
    print("AI 获客全流程 Pipeline 启动")
    print("=" * 50)

    import s1_datasource, s2_collect, s3_clean, s4_score, s5_outreach, s6_track

    n1 = s1_datasource.run(RAW_FILE)
    print(f"[S1 数据源] 生成 {n1} 条模拟企业记录")

    n2 = s2_collect.run(RAW_FILE, LEADS_FILE)
    print(f"[S2 采集] 抽取 {n2} 条线索")

    n3, issues = s3_clean.run(LEADS_FILE, CLEAN_FILE)
    print(f"[S3 清洗] 清洗后 {n3} 条 | 去重 {issues['dup']} 非法邮箱 {issues['bad_email']} 缺邮箱 {issues['missing_email']} 补网站 {issues['missing_website']}")

    n4, dist = s4_score.run(CLEAN_FILE, SCORED_FILE)
    print(f"[S4 分级] {n4} 条 | 分布 {dist}")

    n5 = s5_outreach.run(SCORED_FILE, OUTREACH_FILE)
    print(f"[S5 触达] 生成 {n5} 条个性化触达(mock)")

    result = s6_track.track(SCORED_FILE, OUTREACH_FILE, FUNNEL_FILE)
    print(f"[S6 追踪] 漏斗 {result['funnel']}")
    print("   转化率:", result["rates"])

    print("=" * 50)
    print("全流程完成 [OK]")
    print("=" * 50)

if __name__ == "__main__":
    main()
