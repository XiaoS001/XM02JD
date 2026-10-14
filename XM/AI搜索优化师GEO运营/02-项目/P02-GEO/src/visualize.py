# -*- coding: utf-8 -*-
"""P02 可视化看板：GEO 数据工作台（自包含 HTML，零依赖）"""
import json, os
from collections import Counter
from config import KW_FILE, CONTENT_FILE, CITATION_FILE, FUNNEL_FILE

def load(p):
    with open(p, "r", encoding="utf-8") as f: return json.load(f)

def hbar(items, color):
    total = max((v for _, v in items), default=1)
    rows = []
    for name, cnt in items:
        pct = cnt / total * 100
        rows.append(f"<div class='bar-row'><span class='bar-label'>{name}</span>"
                    f"<div class='bar-track'><div class='bar-fill' style='width:{pct:.0f}%;background:{color}'></div></div>"
                    f"<span class='bar-val'>{cnt}</span></div>")
    return "".join(rows)

def render():
    kws = load(KW_FILE)
    content = load(CONTENT_FILE)
    cit = load(CITATION_FILE)
    fun = load(FUNNEL_FILE)

    n_kw = len(kws)
    cat_dist = Counter(k["category"] for k in kws)
    top_kws = sorted(kws, key=lambda x: -x["priority"])[:10]
    plat = cit["summary"]

    plat_rows = "".join(
        f"<tr><td>{p}</td><td>{v['current']}</td><td class='{ 'up' if v['change_pct']>0 else 'down'}'>{v['change_pct']:+}%</td><td>{v['index_rate']}%</td></tr>"
        for p, v in plat.items())
    kw_rows = "".join(
        f"<tr><td>{k['keyword']}</td><td>{k['category']}</td><td>{k['competition']}</td><td>{k['est_volume']}</td><td>{k['priority']}</td></tr>"
        for k in top_kws)
    fun_rows = "".join(
        f"<div class='frow'><span>{s}</span><b>{v}</b><span class='rate'>{fun['rates'][s]*100:.1f}%</span></div>"
        for s, v in fun["funnel"].items())

    html = f"""<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8">
<title>P02 GEO 数据工作台</title><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Segoe UI','Microsoft YaHei';background:#0d1117;color:#e6edf3;padding:26px}}
.wrap{{max-width:1060px;margin:0 auto}}
h1{{font-size:25px}} .sub{{color:#8b949e;font-size:13px;margin-bottom:22px}}
.kpis{{display:grid;grid-template-columns:repeat(6,1fr);gap:12px;margin-bottom:24px}}
.kpi{{background:#161b22;border-radius:10px;padding:16px 10px;text-align:center;border-top:3px solid #58a6ff}}
.kpi-v{{font-size:22px;font-weight:700}} .kpi-l{{font-size:12px;color:#8b949e;margin-top:5px}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:16px}}
.card{{background:#161b22;border-radius:10px;padding:18px}}
.card h2{{font-size:15px;color:#c9d1d9;margin-bottom:12px}}
.full{{grid-column:1/-1}}
.bar-row{{display:flex;align-items:center;margin-bottom:9px}}
.bar-label{{width:110px;font-size:13px;color:#b6bdd2}}
.bar-track{{flex:1;height:16px;background:#21262d;border-radius:8px;overflow:hidden}}
.bar-fill{{height:100%;border-radius:8px}} .bar-val{{width:60px;text-align:right;font-size:12px;color:#8b949e}}
table{{width:100%;border-collapse:collapse;font-size:13px}}
th{{color:#8b949e;text-align:left;padding:6px 8px;border-bottom:1px solid #30363d}}
td{{padding:6px 8px;border-bottom:1px solid #21262d}}
.up{{color:#3fb950}} .down{{color:#f85149}}
.frow{{display:flex;justify-content:space-between;padding:8px 10px;border-bottom:1px solid #21262d;font-size:14px}}
.frow .rate{{color:#58a6ff}}
.note{{background:#161b22;border-left:4px solid #f5a623;border-radius:10px;padding:16px;margin-top:18px;font-size:13px;color:#c9d1d9;line-height:1.7}}
.foot{{text-align:center;color:#5d6480;font-size:11px;margin-top:18px}}
</style></head><body><div class="wrap">
<h1>📊 P02 · GEO 数据工作台（日语学习品牌）</h1>
<div class="sub">关键词矩阵 → 埋词检查 → AI 引用监测 → 询盘漏斗 · 模拟数据 · 固定种子可复现</div>

<div class="kpis">
  <div class="kpi"><div class="kpi-v">{n_kw}</div><div class="kpi-l">关键词总量</div></div>
  <div class="kpi"><div class="kpi-v">{content['coverage_pct']}%</div><div class="kpi-l">埋词覆盖率</div></div>
  <div class="kpi"><div class="kpi-v">{content['density_pct']}%</div><div class="kpi-l">埋词密度</div></div>
  <div class="kpi"><div class="kpi-v">{cit['total_current']}</div><div class="kpi-l">AI 引用次数</div></div>
  <div class="kpi"><div class="kpi-v">{cit['total_change_pct']:+}%</div><div class="kpi-l">引用环比</div></div>
  <div class="kpi"><div class="kpi-v">{fun['funnel']['询盘']}</div><div class="kpi-l">月询盘数</div></div>
</div>

<div class="grid">
  <div class="card"><h2>四类关键词分布</h2>{hbar(cat_dist.most_common(), '#58a6ff')}</div>
  <div class="card"><h2>询盘漏斗</h2>{fun_rows}</div>
  <div class="card full"><h2>五大 AI 平台引用监测</h2>
    <table><tr><th>平台</th><th>引用次数</th><th>环比</th><th>收录率</th></tr>{plat_rows}</table></div>
  <div class="card full"><h2>高优先级关键词 Top10</h2>
    <table><tr><th>关键词</th><th>类别</th><th>竞争度</th><th>预估月搜</th><th>优先级</th></tr>{kw_rows}</table></div>
</div>

<div class="note"><b>面试弹药（可量化成果）：</b>
① 关键词矩阵 {n_kw} 个（四类分布见上）；② 埋词覆盖率 {content['coverage_pct']}%，密度 {content['density_pct']}%；
③ 五大 AI 平台总引用 {cit['total_current']} 次；④ 环比 {cit['total_change_pct']:+}%；
⑤ 月询盘 {fun['funnel']['询盘']}，成单 {fun['funnel']['成单']}；
⑥ DeepSeek 引用 {plat['DeepSeek']['current']} 次居首，豆包环比 {plat['豆包']['change_pct']:+}% 增长最快。</div>

<div class="foot">XiaoY 生成 · 零外部依赖 · 数据可复现（种子 20261014）</div>
</div></body></html>"""

    out = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dashboard.html"))
    with open(out, "w", encoding="utf-8") as f: f.write(html)
    return out

if __name__ == "__main__":
    print("看板已生成:", render())
