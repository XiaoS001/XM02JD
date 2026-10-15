# -*- coding: utf-8 -*-
"""共享主题模块 v2 —— 视觉对标「面试帝」，代码组织学「Magic UI」

融合策略（2026-10-15）：
  视觉层 ← 面试帝（暖色系、大圆角 22px、clamp 大字、宋体标题、克制动效）
  架构层 ← Magic UI（模块化、组件函数、按需组合、类型化参数）

关键视觉参数（提取自面试帝实际 CSS）：
  - 标题：clamp(58px, 6vw, 82px)，letter-spacing -2px，line-height 1.08
  - 章节标题：clamp(36px, 4vw, 52px)，line-height 1.25
  - 卡片：border-radius 22px，padding 42px，hover translateY(-6px)
  - 网格背景：48px 方格，rgba(36,35,31,0.024)
  - 缓动：cubic-bezier(.2,.8,.2,1)
  - 间距：section 100px，容器 1200px
"""
import os

# ============ 设计 Token（面试帝体系）============
TOKENS = {
    "bg": "#f7f5f0", "surface": "#fff", "surface_alt": "#f8f6f1",
    "ink": "#171815", "ink_soft": "#24251f", "muted": "#707169",
    "line": "#dedbd3", "red": "#c63a32", "red_dark": "#9f2b25",
    "soft_red": "#f5e7e4", "gold": "#b89858", "dark": "#1d1e1b",
    "serif": '"Songti SC","STSong","Noto Serif CJK SC",serif',
    "sans": '"PingFang SC","Microsoft YaHei",sans-serif',
}

def _light_css():
    """亮色主题 —— 视觉完全对标面试帝"""
    return """
:root{
  --bg:#f7f5f0;--surface:#fff;--surface-alt:#f8f6f1;
  --ink:#171815;--ink-soft:#24251f;--muted:#707169;--line:#dedbd3;
  --red:#c63a32;--red-dark:#9f2b25;--soft-red:#f5e7e4;--gold:#b89858;--dark:#1d1e1b;
  --serif:"Songti SC","STSong","Noto Serif CJK SC",serif;
  --sans:"PingFang SC","Microsoft YaHei",sans-serif;
  --ease:cubic-bezier(.2,.8,.2,1);
  --radius:22px;
}
*{margin:0;padding:0;box-sizing:border-box}
body{background:var(--bg);color:var(--ink);font-family:var(--sans);line-height:1.75;font-size:15px}

/* 进度条 —— scaleX（学自面试帝）*/
.progress{position:fixed;top:0;left:0;height:3px;width:100%;transform:scaleX(0);
  transform-origin:0 50%;background:linear-gradient(90deg,var(--red),var(--gold));z-index:100}

/* 滚动渐显 —— cubic-bezier(.2,.8,.2,1) 快出慢入 */
.reveal{opacity:0;transform:translateY(22px);
  transition:opacity .65s var(--ease),transform .65s var(--ease);transition-delay:var(--d,0s)}
.reveal.is-visible{opacity:1;transform:none}

.wrap{max-width:1200px;margin:0 auto;padding:0 32px}

/* 标题 —— 面试帝大字（clamp 到 82px）*/
h1{font-family:var(--serif);font-size:clamp(46px,6vw,82px);line-height:1.08;
  letter-spacing:-2px;margin:24px 0;font-weight:750}
h1 em{color:var(--red);font-style:normal}
h2{font-family:var(--serif);font-size:clamp(30px,4vw,52px);line-height:1.25;
  letter-spacing:normal;margin:12px 0 11px;color:var(--ink-soft);text-wrap:balance}
h2 em{color:var(--red);font-style:normal}
.sub{color:var(--muted);font-size:15px;margin-bottom:38px;max-width:680px}

/* Hero —— 网格背景（面试帝 48px 方格）*/
.hero{padding:110px 0 70px;position:relative;overflow:hidden;
  background-image:linear-gradient(rgba(36,35,31,.024) 1px,transparent 1px),
                   linear-gradient(90deg,rgba(36,35,31,.024) 1px,transparent 1px);
  background-size:48px 48px}
.hero-inner{max-width:1200px;margin:0 auto;padding:0 32px;position:relative}
.hero p.lead{color:var(--muted);font-size:16px;max-width:640px;line-height:1.9;margin-top:8px}

/* 声波（面试帝组件）*/
.wave{display:flex;gap:5px;align-items:center;height:32px;margin-bottom:22px}
.wave i{width:3px;height:100%;background:var(--red);border-radius:2px;
  animation:wave 1.2s ease-in-out infinite;animation-delay:calc(var(--i)*.1s)}
@keyframes wave{0%,100%{transform:scaleY(.3)}50%{transform:scaleY(1)}}

/* KPI 卡片 —— 大圆角 + 大内边距 */
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:20px;margin-bottom:52px}
.kpi{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);
  padding:32px 24px;text-align:center;position:relative;overflow:hidden;
  transition:transform .3s var(--ease),box-shadow .3s,border-color .3s}
.kpi:hover{transform:translateY(-6px);box-shadow:0 14px 40px rgba(27,28,25,.07);border-color:var(--red)}
.kpi-v{font-family:var(--serif);font-size:clamp(34px,4vw,46px);font-weight:750;
  color:var(--red);line-height:1.1;letter-spacing:-1px}
.kpi-l{font-size:13px;color:var(--muted);margin-top:10px}

/* 卡片 —— 22px 圆角 + 42px 内边距（面试帝参数）*/
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:22px}
.grid-2{grid-template-columns:repeat(auto-fit,minmax(360px,1fr))}
.card{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);
  padding:42px;position:relative;overflow:hidden;
  transition:transform .3s var(--ease),border-color .3s,box-shadow .3s}
.card:hover{transform:translateY(-6px);border-color:var(--red);box-shadow:0 16px 44px rgba(27,28,25,.08)}
.card h3{font-family:var(--serif);font-size:22px;margin:10px 0 12px;color:var(--ink-soft);font-weight:700}
.card p{font-size:14.5px;color:var(--muted);line-height:1.85}

section{padding:100px 0}
section.tight{padding:64px 0}

/* 条形图 */
.bar-row{display:flex;align-items:center;margin-bottom:14px}
.bar-label{width:120px;font-size:14px;color:var(--muted);flex-shrink:0}
.bar-track{flex:1;height:22px;background:#edeae4;border-radius:11px;overflow:hidden}
.bar-fill{height:100%;border-radius:11px;transition:width 1s var(--ease)}
.bar-val{width:90px;text-align:right;font-size:13px;color:var(--muted)}

/* 表格 —— 大圆角 + 宽松间距 */
table{width:100%;border-collapse:collapse;font-size:14px;background:var(--surface);
  border-radius:var(--radius);overflow:hidden;border:1px solid var(--line)}
th{text-align:left;padding:16px 22px;background:var(--surface-alt);color:#4a4a45;
  font-weight:600;border-bottom:1px solid var(--line);font-size:13.5px}
td{padding:15px 22px;border-bottom:1px solid #f0ede7;color:#3a3a35}
tr:last-child td{border-bottom:none}
tr:hover td{background:#faf9f6}
.up{color:#3f8f52;font-weight:600} .down{color:#c63a32;font-weight:600}

/* 深色区块 */
.dark{background:var(--dark);color:#f7f5f0;padding:90px 0;margin:20px 0}
.dark h2{color:#f7f5f0}
.dark .sub{color:#9a9b93}
.dark-kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:32px;text-align:center}
.dark-v{font-family:var(--serif);font-size:clamp(34px,4vw,50px);color:var(--red);
  font-weight:750;letter-spacing:-1px}
.dark-l{font-size:13px;color:#9a9b93;margin-top:8px}

/* 漏斗 */
.funnel-row{display:flex;justify-content:space-between;align-items:center;
  padding:15px 22px;border-bottom:1px solid #f0ede7;font-size:14.5px}
.funnel-row:last-child{border-bottom:none}
.funnel-rate{color:var(--red);font-weight:600;font-size:13.5px}

/* 提示块 */
.note{background:var(--surface);border-left:4px solid var(--gold);border-radius:var(--radius);
  padding:28px 34px;font-size:14.5px;line-height:1.9;border:1px solid var(--line);border-left-width:4px}
.note code{background:var(--soft-red);color:var(--red-dark);padding:3px 9px;border-radius:6px;
  font-family:monospace;font-size:13px}
.note b{color:var(--red-dark)}

/* 标签 */
.tag{display:inline-block;font-size:12px;padding:4px 13px;border-radius:999px;
  font-weight:600;letter-spacing:.4px}
.t-red{background:var(--soft-red);color:var(--red-dark)}
.t-gold{background:#f7f1e4;color:#8a6d38}
.t-green{background:#eaf4ec;color:#3f8f52}
.t-blue{background:#e8f0f8;color:#3a6b99}
.t-gray{background:#f0ede7;color:#6b6b64}

/* 数字标签 */
.nums{margin-top:18px;display:flex;flex-wrap:wrap;gap:8px}
.num{background:var(--surface-alt);border:1px solid var(--line);border-radius:10px;
  padding:7px 13px;font-size:12.5px;color:#4a4a45}

/* 链接卡片 */
a.card{text-decoration:none;color:inherit;display:block}
a.card:hover h3{color:var(--red)}

footer{padding:60px 0;text-align:center;color:#8b8b83;font-size:13px;
  border-top:1px solid var(--line);margin-top:60px}

/* 无障碍 */
@media (prefers-reduced-motion:reduce){
  .reveal{opacity:1;transform:none;transition:none}
  .wave i{animation:none}
  .bar-fill{transition:none}
  .kpi,.card{transition:none}
}
@media (max-width:980px){
  .card{padding:32px}
  section{padding:72px 0}
}
@media (max-width:620px){
  .wrap,.hero-inner{padding:0 20px}
  .card{padding:26px}
  .kpis{gap:14px}
}
"""

# ============ 共享 JS ============
BASE_JS = """
(function(){
  var reduced=window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // 滚动渐显（面试帝：threshold .16 + 触发后 unobserve）
  var io=new IntersectionObserver(function(es){
    es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('is-visible');io.unobserve(e.target)}})
  },{threshold:0.16});
  document.querySelectorAll('.reveal').forEach(function(el){io.observe(el)});

  // 进度条
  var pb=document.querySelector('[data-progress]');
  var onScroll=function(){
    if(!pb)return;
    var el=document.documentElement,total=el.scrollHeight-el.clientHeight;
    pb.style.transform='scaleX('+(total>0?window.scrollY/total:0)+')';
  };
  window.addEventListener('scroll',onScroll,{passive:true});onScroll();

  // 数字滚动（easeOutCubic；HTML 初始值为终值，JS 失效也能看）
  var animate=function(el){
    var target=Number(el.dataset.count||0);
    if(reduced||!target){el.textContent=String(target);return}
    el.textContent='0';
    var t0=performance.now();
    var tick=function(now){
      var p=Math.min(1,(now-t0)/1100);
      el.textContent=String(Math.round(target*(1-Math.pow(1-p,3))));
      if(p<1)requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  };
  var cio=new IntersectionObserver(function(es){
    es.forEach(function(e){if(e.isIntersecting){animate(e.target);cio.unobserve(e.target)}})
  },{threshold:0.6});
  document.querySelectorAll('[data-count]').forEach(function(el){cio.observe(el)});

  // 条形图进场
  if(!reduced){
    document.querySelectorAll('.bar-fill[data-w]').forEach(function(el){
      var w=el.dataset.w;el.style.width='0%';
      var bio=new IntersectionObserver(function(es){
        es.forEach(function(e){if(e.isIntersecting){
          setTimeout(function(){el.style.width=w+'%'},120);bio.unobserve(e.target)}})
      },{threshold:0.3});
      bio.observe(el);
    });
  }
})();
"""

# ============ 组件函数（Magic UI 式模块化）============
def kpi(value, label, delay=0.0, counted=False):
    d = f' style="--d:{delay}s"' if delay else ""
    inner = f'<div class="kpi-v" data-count="{value}">{value}</div>' if counted else f'<div class="kpi-v">{value}</div>'
    return f'<div class="kpi reveal"{d}>{inner}<div class="kpi-l">{label}</div></div>'

def dark_kpi(value, label):
    return f'<div><div class="dark-v" data-count="{value}">{value}</div><div class="dark-l">{label}</div></div>'

def hbar(items, color=None, delay_step=0.06):
    if not items:
        return '<p class="sub">暂无数据</p>'
    total = max((v for _, v in items), default=1) or 1
    c = color or "var(--red)"
    rows = []
    for i, (name, val) in enumerate(items):
        pct = val / total * 100
        rows.append(
            f'<div class="bar-row reveal" style="--d:{i*delay_step:.2f}s">'
            f'<span class="bar-label">{name}</span>'
            f'<div class="bar-track"><div class="bar-fill" data-w="{pct:.1f}" '
            f'style="width:{pct:.1f}%;background:{c}"></div></div>'
            f'<span class="bar-val">{val}</span></div>')
    return "".join(rows)

def funnel_svg(stages, width=720):
    if not stages:
        return ""
    vals = list(stages.values()); maxv = max(vals) or 1; n = len(stages)
    top, bot = 50, 360; step = (bot - top) / n
    colors = ["#c63a32", "#d96a5f", "#e89a8f", "#f0c4bb", "#f5e7e4"]
    parts = []
    for i, (lb, v) in enumerate(stages.items()):
        y1, y2 = top + i * step, top + i * step + step * 0.76
        ratio = v / maxv
        x1 = (width - width * ratio) / 2; x2 = width - x1
        parts.append(f'<polygon points="{x1},{y1} {x2},{y1} {x2-14},{y2} {x1+14},{y2}" '
                     f'fill="{colors[i%len(colors)]}" opacity="0.92"/>')
        parts.append(f'<text x="{width/2}" y="{y1+(y2-y1)/2+6}" text-anchor="middle" '
                     f'font-size="15" fill="#fff" font-weight="600">{lb} · {v}</text>')
    return (f'<svg viewBox="0 0 {width} {bot+30}" width="100%" height="400" role="img" '
            f'aria-label="转化漏斗">{"".join(parts)}</svg>')

def card(title, body, delay=0.0, tag=None, tag_class="t-red"):
    d = f' style="--d:{delay}s"' if delay else ""
    tag_html = f'<span class="tag {tag_class}">{tag}</span>' if tag else ""
    return f'<div class="card reveal"{d}>{tag_html}<h3>{title}</h3><p>{body}</p></div>'

def link_card(title, body, nums, href, tag, tag_class="t-red", delay=0.0):
    d = f' style="--d:{delay}s"' if delay else ""
    nums_html = "".join(f'<span class="num">{n}</span>' for n in nums)
    return (f'<a class="card reveal" href="{href}"{d}>'
            f'<span class="tag {tag_class}">{tag}</span>'
            f'<h3>{title}</h3><p>{body}</p>'
            f'<div class="nums">{nums_html}</div></a>')

def table(headers, rows, delay=0.0):
    d = f' style="--d:{delay}s"' if delay else ""
    th = "".join(f"<th>{h}</th>" for h in headers)
    trs = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<table class="reveal"{d}><tr>{th}</tr>{trs}</table>'

def note(content, delay=0.12):
    return f'<div class="note reveal" style="--d:{delay}s">{content}</div>'

def wave(n=5):
    return f'<div class="wave" aria-hidden="true">{"".join(f"<i style=--i:{i}></i>" for i in range(n))}</div>'

def hero(title_html, lead, tagline=None, wave_bars=True, delay_step=0.12):
    """首屏（面试帝式：声波 + 大字 + 网格背景）"""
    w = wave() if wave_bars else ""
    tag = f'<p class="tag t-red" style="margin-bottom:18px">{tagline}</p>' if tagline else ""
    return f'''<header class="hero">
  <div class="hero-inner">
    {w}{tag}
    <h1 class="reveal">{title_html}</h1>
    <p class="lead reveal" style="--d:{delay_step}s">{lead}</p>
  </div>
</header>'''

def section(title_html, sub, content, delay=0.08, tight=False):
    cls = "tight" if tight else ""
    return f'''<section class="wrap {cls}" style="padding-left:32px;padding-right:32px;max-width:1200px;margin:0 auto">
  <h2 class="reveal">{title_html}</h2>
  <p class="sub reveal" style="--d:{delay}s">{sub}</p>
  {content}
</section>'''

def dark_block(title_html, sub, kpis_html):
    return f'''<div class="dark"><div style="max-width:1200px;margin:0 auto;padding:0 32px">
  <h2 class="reveal">{title_html}</h2>
  <p class="sub reveal" style="--d:.08s">{sub}</p>
  <div class="dark-kpis">{kpis_html}</div>
</div></div>'''

def page(title, hero_html, body_html, footer_text, out_path=None):
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>{_light_css()}</style>
<noscript><style>.reveal{{opacity:1!important;transform:none!important}}.bar-fill{{width:auto!important}}</style></noscript>
</head>
<body>
<div class="progress" data-progress></div>
{hero_html}
{body_html}
<footer>{footer_text}</footer>
<script>{BASE_JS}</script>
</body>
</html>'''
    if out_path:
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
    return html
