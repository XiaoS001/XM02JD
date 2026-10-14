# -*- coding: utf-8 -*-
"""P03 可视化看板：RAG 问答系统（自包含 HTML，零依赖）

展示：RAG 四步流程、三个演示问答的检索结果、相似度、命中块内容、评估结果。
"""
import os, sys, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import pipeline

def render():
    text = pipeline.load_doc(pipeline.KNOWLEDGE)
    chunks = pipeline.split_chunks(text)
    pipeline.VOCAB = pipeline.build_vocab(chunks)
    N = len(chunks)
    pipeline.IDF = {w: math.log((N + 1) / (df + 1)) + 1 for w, df in pipeline.VOCAB.items()}
    cvecs = [pipeline.vectorize(c, pipeline.VOCAB, pipeline.IDF) for c in chunks]

    questions = ["RAG 是什么？", "AI 应用开发工程师需要什么技能？", "大模型 API 怎么调用？"]
    qa_rows = []
    for q in questions:
        top = pipeline.retrieve(q, chunks, cvecs, top_k=3)
        best_sim = top[0][1]
        # 命中块前 60 字
        snippets = "".join(
            f"<div class='hit'><span class='sim'>{s:.2f}</span>{c[:70]}…</div>"
            for c, s in top
        )
        qa_rows.append(f"""
        <div class="qa">
          <div class="q">❓ {q}</div>
          <div class="sim-badge">最高相似度 {best_sim:.3f}</div>
          <div class="hits">{snippets}</div>
        </div>""")

    # 评估
    evals = pipeline.evaluate(chunks, cvecs)
    eval_rows = "".join(
        f"<tr><td>{q}</td><td class='{'ok' if h else 'bad'}'>{'✅ 命中' if h else '❌ 未命中'}</td></tr>"
        for q, h in evals
    )

    # 四步流程条
    steps = [
        ("M1 文档切分", f"{len(chunks)} 个块", "#4f8cff"),
        ("M2 向量化", f"TF-IDF · {len(pipeline.VOCAB)} 维", "#5aa9e6"),
        ("M3 检索", "余弦相似度 Top3", "#7fc8f8"),
        ("M4 生成", "检索拼接 / LLM", "#a5e0c0"),
    ]
    step_html = "".join(
        f"<div class='step' style='border-top:4px solid {c}'><div class='step-n'>{i+1}</div><div class='step-t'>{n}</div><div class='step-d'>{d}</div></div>"
        for i, (n, d, c) in enumerate(steps)
    )

    html = f"""<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8">
<title>P03 RAG 问答系统 · 看板</title><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Segoe UI','Microsoft YaHei';background:#0d1117;color:#e6edf3;padding:28px}}
.wrap{{max-width:960px;margin:0 auto}}
h1{{font-size:24px}} .sub{{color:#8b949e;font-size:13px;margin-bottom:22px}}
.steps{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:26px}}
.step{{background:#161b22;border-radius:10px;padding:16px 12px;text-align:center}}
.step-n{{font-size:20px;font-weight:700;color:#58a6ff}}
.step-t{{font-size:14px;font-weight:600;margin:4px 0}}
.step-d{{font-size:12px;color:#8b949e}}
.qa{{background:#161b22;border-radius:10px;padding:18px;margin-bottom:16px}}
.q{{font-size:15px;font-weight:600;margin-bottom:10px}}
.sim-badge{{display:inline-block;background:#1f6feb33;color:#58a6ff;border-radius:20px;padding:3px 12px;font-size:13px;margin-bottom:10px}}
.hits{{display:flex;flex-direction:column;gap:6px}}
.hit{{background:#21262d;border-radius:8px;padding:8px 12px;font-size:13px;color:#c9d1d9}}
.sim{{color:#58a6ff;font-weight:700;margin-right:10px}}
.card{{background:#161b22;border-radius:10px;padding:18px;margin-bottom:16px}}
.card h2{{font-size:15px;margin-bottom:12px;color:#c9d1d9}}
table{{width:100%;border-collapse:collapse;font-size:13px}}
th{{color:#8b949e;text-align:left;padding:6px 10px;border-bottom:1px solid #30363d}}
td{{padding:6px 10px;border-bottom:1px solid #21262d}}
.ok{{color:#3fb950}} .bad{{color:#f85149}}
.note{{background:#161b22;border-left:4px solid #f5a623;border-radius:10px;padding:16px;font-size:13px;color:#c9d1d9;line-height:1.7}}
.foot{{text-align:center;color:#5d6480;font-size:11px;margin-top:18px}}
</style></head><body><div class="wrap">
<h1>🔍 P03 · RAG 问答系统看板</h1>
<div class="sub">检索增强生成 · 纯 Python 实现（切分→向量化→检索→生成）· 离线可跑</div>

<div class="steps">{step_html}</div>

<h2 style="font-size:16px;margin-bottom:12px;color:#c9d1d9">演示问答（检索结果 + 相似度）</h2>
{''.join(qa_rows)}

<div class="card">
  <h2>检索命中自检</h2>
  <table><tr><th>问题</th><th>结果</th></tr>{eval_rows}</table>
</div>

<div class="note"><b>面试要点：</b>
① RAG = 先从知识库检索相关片段，再让 LLM 基于片段生成，解决幻觉问题；
② 我踩过并修掉"词袋被高频词稀释"的坑（改用 TF-IDF，相似度 0.865→1.000）；
③ 词袋不做语义理解，真实生产要用 embedding 模型——这是本项目的已知局限，也是下一步升级点。</div>

<div class="foot">XiaoY 生成 · 零外部依赖 · 数据可复现</div>
</div></body></html>"""

    out = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dashboard.html"))
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    return out

if __name__ == "__main__":
    print("看板已生成:", render())
