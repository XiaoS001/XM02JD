# -*- coding: utf-8 -*-
"""P01 看板 —— 视觉对标面试帝，代码组织学 Magic UI"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "_共享模板"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from theme import page, hero, section, kpi, dark_kpi, hbar, funnel_svg, card, note, dark_block
from config import RAW_FILE, CLEAN_FILE, SCORED_FILE, OUTREACH_FILE, FUNNEL_FILE

def load(p):
    with open(p, "r", encoding="utf-8") as f: return json.load(f)

def build():
    raw = load(RAW_FILE); clean = load(CLEAN_FILE); scored = load(SCORED_FILE)
    outreach = load(OUTREACH_FILE); funnel = load(FUNNEL_FILE)["funnel"]
    from collections import Counter
    grade_dist = Counter(l["grade"] for l in scored)
    ind_dist = Counter(l["industry"] for l in scored).most_common(8)
    scale_dist = Counter(l["scale"] for l in scored)
    order = ["大型","中型","小型","微型"]
    scale_items = sorted(scale_dist.items(), key=lambda x: order.index(x[0]) if x[0] in order else 99)
    n_raw, n_clean, n_out = len(raw), len(clean), len(outreach)
    sample = outreach[0]["message"] if outreach else "暂无"

    hero_html = hero(
        'AI 获客<br><em>全流程 Pipeline</em>',
        "六段流水线：数据源 → 采集 → 清洗 → 分级 → 触达 → 追踪。每个数字都由固定随机种子生成，可复现。",
        tagline="P01 · 练手项目"
    )

    body = section("看板总览", "从 122 条模拟企业到 9 个成交的完整链路",
        f'<div class="kpis">'
        + kpi(n_raw, "原始企业", 0, True) + kpi(n_clean, "清洗后线索", .06, True)
        + kpi(n_out, "可触达(A/B)", .12, True) + kpi(funnel.get("有意向",0), "有意向", .18, True)
        + kpi(funnel.get("成交",0), "成交", .24, True) + '</div>')

    body += section("转化漏斗", "逐级流失发生在哪里",
        f'<div class="card reveal">{funnel_svg(funnel)}</div>')

    body += dark_block("六段流水线", "一条命令跑完，exit 0",
        dark_kpi(6, "Pipeline 阶段") + dark_kpi(n_raw, "模拟企业")
        + dark_kpi(n_clean, "清洗后") + dark_kpi(n_out, "触达"))

    body += section("线索分级与分布", "分级规则可解释：目标行业 + 企业规模 + 邮箱有效性",
        f'''<div class="grid grid-2">
  <div class="card reveal"><h3>等级分布</h3>{hbar(sorted(grade_dist.items()))}</div>
  <div class="card reveal" style="--d:.08s"><h3>企业规模分布</h3>{hbar(scale_items, "var(--gold)")}</div>
</div>
<div class="grid" style="margin-top:22px">
  <div class="card reveal" style="--d:.16s"><h3>行业分布 Top8</h3>{hbar(ind_dist, "#8a6d38")}</div>
</div>''')

    body += section("个性化触达样例", "mock 触达（未真发），体现个性化逻辑",
        note(sample))

    body += section("面试要点", "这个项目能证明什么",
        f'''<div class="grid">
  {card("流程能力", "AI 获客是一条六段流水线，不是单一技能 —— 我完整跑通过。", 0, "核心", "t-red")}
  {card("工程规范", "固定随机种子、可复现；去重、邮箱校验、边界处理齐全。", .08, "规范", "t-blue")}
  {card("数据口径", "分级规则可解释，漏斗每级转化率可追溯。", .16, "口径", "t-green")}
</div>''', tight=True)

    return page("P01 · AI 获客全流程看板", hero_html, body,
        "P01 AI获客全流程 · XiaoY · 数据可复现（种子 20261014）· 视觉对标面试帝 / 组织学 Magic UI")

def render():
    out = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dashboard.html"))
    with open(out, "w", encoding="utf-8") as f: f.write(build())
    return out

if __name__ == "__main__":
    print("看板已生成:", render())
