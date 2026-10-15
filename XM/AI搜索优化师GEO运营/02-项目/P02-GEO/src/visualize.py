# -*- coding: utf-8 -*-
"""P02 看板 —— 视觉对标面试帝，代码组织学 Magic UI"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "_共享模板"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from theme import page, hero, section, kpi, dark_kpi, hbar, card, table, note, dark_block
from config import KW_FILE, CONTENT_FILE, CITATION_FILE, FUNNEL_FILE

def load(p):
    with open(p, "r", encoding="utf-8") as f: return json.load(f)

def build():
    kws = load(KW_FILE); content = load(CONTENT_FILE)
    cit = load(CITATION_FILE); fun = load(FUNNEL_FILE)
    from collections import Counter
    n_kw = len(kws)
    cat_dist = Counter(k["category"] for k in kws)
    top_kws = sorted(kws, key=lambda x: -x["priority"])[:10]
    plat = cit["summary"]
    f = fun["funnel"]

    hero_html = hero(
        'GEO 数据工作台<br><em>日语学习品牌</em>',
        "关键词矩阵 → 埋词检查 → 五大 AI 平台引用监测 → 询盘漏斗。每个数字可复现，口径经得起追问。",
        tagline="P02 · 练手项目"
    )

    body = section("GEO 数据总览", "围绕日语学习品牌的关键词与引用数据",
        f'<div class="kpis">'
        + kpi(n_kw, "关键词总量", 0, True)
        + kpi(content["coverage_pct"], "埋词覆盖率 %", .06)
        + kpi(cit["total_current"], "AI 引用次数", .12, True)
        + kpi(f["询盘"], "月询盘", .18, True)
        + kpi(f["成单"], "成交", .24, True) + '</div>')

    plat_rows = [[p, f"{v['current']}",
                  f'<span class="{"up" if v["change_pct"]>0 else "down"}">{v["change_pct"]:+}%</span>',
                  f"{v['index_rate']}%"] for p, v in plat.items()]
    body += section("五大 AI 平台引用监测", "豆包 / 元宝 / DeepSeek / 千问 / 文心一言",
        table(["平台", "引用次数", "环比", "收录率"], plat_rows))

    body += dark_block("引用规模", f"五大平台合计 · 环比 {cit['total_change_pct']:+}%",
        dark_kpi(cit["total_current"], "总引用次数") + dark_kpi(n_kw, "关键词矩阵")
        + dark_kpi(f["曝光"], "月曝光") + dark_kpi(f["成单"], "成交"))

    body += section("关键词与询盘漏斗", "四类词分布 + 逐级转化率",
        f'''<div class="grid grid-2">
  <div class="card reveal"><h3>四类关键词分布</h3>{hbar(cat_dist.most_common(), "var(--red)")}</div>
  <div class="card reveal" style="--d:.08s"><h3>询盘漏斗</h3>
    {"".join(f'<div class="funnel-row"><span>{s}</span><b>{v}</b><span class="funnel-rate">{fun["rates"][s]*100:.1f}%</span></div>' for s, v in f.items())}
  </div>
</div>''')

    kw_rows = [[k["keyword"], k["category"], k["competition"], k["est_volume"], k["priority"]] for k in top_kws]
    body += section("高优先级关键词 Top10", "排序依据：意图价值 × (10 − 竞争度)",
        table(["关键词", "类别", "竞争度", "预估月搜", "优先级"], kw_rows))

    body += section("面试弹药 · 6 个可报数字", "对应 JD 任职要求第 3 条「可量化实战成果」",
        note(f'''① 关键词矩阵 <b>{n_kw}</b> 个（四类分布）<br>
② 埋词覆盖率 <b>{content["coverage_pct"]}%</b>，密度 {content["density_pct"]}%<br>
③ 五大 AI 平台总引用 <b>{cit["total_current"]}</b> 次<br>
④ 引用环比 <b>{cit["total_change_pct"]:+}%</b>（豆包增速最快）<br>
⑤ 月询盘 <b>{f["询盘"]}</b>，成单 <b>{f["成单"]}</b><br>
⑥ DeepSeek 引用 <b>{plat["DeepSeek"]["current"]}</b> 次居首'''), tight=True)

    return page("P02 · GEO 数据工作台", hero_html, body,
        "P02 GEO数据工作台 · XiaoY · 数据可复现（种子 20261014）· 视觉对标面试帝 / 组织学 Magic UI")

def render():
    out = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dashboard.html"))
    with open(out, "w", encoding="utf-8") as fh: fh.write(build())
    return out

if __name__ == "__main__":
    print("看板已生成:", render())
