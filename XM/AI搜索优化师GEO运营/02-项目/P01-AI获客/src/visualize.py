# -*- coding: utf-8 -*-
"""可视化：把 P01 六段产物渲染成自包含 HTML 看板

零外部依赖（内联 CSS/SVG），生成一个 .html 双击即可在浏览器打开。
"""
import json
import os
from collections import Counter
from config import SCORED_FILE, OUTREACH_FILE, FUNNEL_FILE, RAW_FILE, CLEAN_FILE

def load(p):
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)

def hbar(items, total, color):
    """横向条形图（SVG）"""
    if not items:
        return "<div class='empty'>暂无数据</div>"
    rows = []
    for name, cnt in items:
        pct = (cnt / total * 100) if total else 0
        rows.append(
            f"<div class='bar-row'><span class='bar-label'>{name}</span>"
            f"<div class='bar-track'><div class='bar-fill' style='width:{pct:.1f}%;background:{color}'></div></div>"
            f"<span class='bar-val'>{cnt}（{pct:.1f}%）</span></div>"
        )
    return "".join(rows)

def funnel_svg(stages):
    """漏斗图（SVG 梯形）"""
    labels = list(stages.keys())
    vals = list(stages.values())
    maxv = max(vals) if vals else 1
    n = len(stages)
    w, h_total, top, bot = 620, 0, 50, 340
    step = (bot - top) / n
    parts = []
    colors = ["#4f8cff", "#5aa9e6", "#7fc8f8", "#a5e0c0", "#c9e79d"]
    for i, (lb, v) in enumerate(stages.items()):
        y1 = top + i * step
        y2 = y1 + step * 0.78
        ratio = v / maxv
        x1 = (w - w * ratio) / 2
        x2 = w - x1
        c = colors[i % len(colors)]
        parts.append(f'<polygon points="{x1},{y1} {x2},{y1} {x2 - 12},{y2} {x1 + 12},{y2}" fill="{c}" opacity="0.9"/>')
        parts.append(f'<text x="{w/2}" y="{y1 + (y2-y1)/2 + 4}" text-anchor="middle" font-size="14" fill="#1a1a2e" font-weight="600">{lb}：{v}</text>')
    svg = f'<svg viewBox="0 0 {w} {top + n*step + 20}" width="100%" height="420">{ "".join(parts) }</svg>'
    return svg

def kpi(label, value, color):
    return f'<div class="kpi" style="border-top:4px solid {color}"><div class="kpi-v">{value}</div><div class="kpi-l">{label}</div></div>'

def render():
    scored = load(SCORED_FILE)
    outreach = load(OUTREACH_FILE)
    funnel = load(FUNNEL_FILE)["funnel"]
    raw = load(RAW_FILE)
    clean = load(CLEAN_FILE)

    n_raw = len(raw); n_clean = len(clean); n_scored = len(scored); n_out = len(outreach)

    # 等级分布
    grade_dist = Counter(l["grade"] for l in scored)
    grade_items = sorted(grade_dist.items())
    # 行业分布
    ind_dist = Counter(l["industry"] for l in scored)
    ind_items = ind_dist.most_common(8)
    # 规模分布
    scale_dist = Counter(l["scale"] for l in scored)
    scale_items = sorted(scale_dist.items(), key=lambda x: ["大型","中型","小型","微型"].index(x[0]) if x[0] in ["大型","中型","小型","微型"] else 99)

    # 触达样例
    sample = outreach[0] if outreach else None

    grades_color = "#4f8cff"; ind_color = "#f5a623"; scale_color = "#7fc8f8"

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI 获客全流程 · 数据看板</title>
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ font-family:'Segoe UI','Microsoft YaHei',sans-serif; background:#0f1220; color:#e8eaf0; padding:28px; }}
  .wrap {{ max-width:1000px; margin:0 auto; }}
  h1 {{ font-size:26px; margin-bottom:4px; }}
  .sub {{ color:#8a91a8; font-size:14px; margin-bottom:24px; }}
  .kpis {{ display:grid; grid-template-columns:repeat(5,1fr); gap:14px; margin-bottom:28px; }}
  .kpi {{ background:#1a1e30; border-radius:12px; padding:18px 14px; text-align:center; }}
  .kpi-v {{ font-size:30px; font-weight:700; }}
  .kpi-l {{ font-size:13px; color:#8a91a8; margin-top:6px; }}
  .grid {{ display:grid; grid-template-columns:1fr 1fr; gap:18px; margin-bottom:28px; }}
  .card {{ background:#1a1e30; border-radius:12px; padding:20px; }}
  .card h2 {{ font-size:16px; margin-bottom:14px; color:#c8cde0; }}
  .full {{ grid-column:1 / -1; }}
  .bar-row {{ display:flex; align-items:center; margin-bottom:10px; }}
  .bar-label {{ width:80px; font-size:13px; color:#b6bdd2; flex-shrink:0; }}
  .bar-track {{ flex:1; height:18px; background:#252a40; border-radius:9px; overflow:hidden; }}
  .bar-fill {{ height:100%; border-radius:9px; }}
  .bar-val {{ width:90px; text-align:right; font-size:12px; color:#8a91a8; }}
  .empty {{ color:#6b7190; font-size:13px; }}
  .msg {{ background:#1a1e30; border-radius:12px; padding:20px; margin-bottom:28px; border-left:4px solid #4f8cff; }}
  .msg p {{ font-size:14px; line-height:1.7; color:#d5d9e8; }}
  .foot {{ text-align:center; color:#5d6480; font-size:12px; margin-top:20px; }}
</style>
</head>
<body>
<div class="wrap">
  <h1>🤖 AI 获客全流程 · 数据看板</h1>
  <div class="sub">P01 练手项目 · 六段 Pipeline（数据源→采集→清洗→分级→触达→追踪）· 模拟数据 · mock 触达</div>

  <div class="kpis">
    {kpi("原始企业", n_raw, "#4f8cff")}
    {kpi("清洗后线索", n_clean, "#5aa9e6")}
    {kpi("可触达(A/B)", n_out, "#7fc8f8")}
    {kpi("有意向", funnel.get("有意向", 0), "#a5e0c0")}
    {kpi("成交", funnel.get("成交", 0), "#c9e79d")}
  </div>

  <div class="grid">
    <div class="card full">
      <h2>转化漏斗（120 → 成交）</h2>
      {funnel_svg(funnel)}
    </div>
    <div class="card">
      <h2>线索等级分布</h2>
      {hbar(grade_items, n_scored, grades_color)}
    </div>
    <div class="card">
      <h2>行业分布 Top8</h2>
      {hbar(ind_items, n_scored, ind_color)}
    </div>
    <div class="card full">
      <h2>企业规模分布</h2>
      {hbar(scale_items, n_scored, scale_color)}
    </div>
  </div>

  <div class="msg">
    <h2 style="margin-bottom:8px">📨 个性化触达样例（mock，未真发）</h2>
    <p>{sample['message'] if sample else '暂无触达记录'}</p>
  </div>

  <div class="foot">由 XiaoY 生成 · 数据可复现（固定随机种子 20261014）· 零外部依赖</div>
</div>
</body>
</html>"""

    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dashboard.html")
    out_path = os.path.abspath(out_path)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    return out_path

if __name__ == "__main__":
    p = render()
    print("HTML 看板已生成:", p)
