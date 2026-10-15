# -*- coding: utf-8 -*-
"""岗位展示首页 —— 视觉对标面试帝，代码组织学 Magic UI"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from theme import page, hero, section, card, link_card, note

def build_geo(out_path):
    hero_html = hero('AI 搜索优化师<br><em>GEO 运营</em>',
        "冲鸭教育 · 岗位三合一（需求 / 展示 / 项目）。每个数字都由项目代码生成，可复现。",
        tagline="★ 求职岗位展示")

    s1 = section("项目作品集", "点击卡片打开对应看板",
        f'''<div class="grid grid-2">
  {link_card("P02 · GEO 数据工作台",
    "关键词矩阵 → 埋词检查 → 五大 AI 平台引用监测 → 询盘漏斗，直击 JD「可量化实战成果」要求。",
    ["62 关键词", "90.3% 覆盖率", "2284 次引用 (+16.1%)", "1015 询盘 / 202 成单"],
    "../02-项目/P02-GEO/dashboard.html", "主力 · 贴合本岗位", "t-red", 0.0)}
  {link_card("P01 · AI 获客全流程",
    "六段获客流水线：数据源 → 采集 → 清洗 → 分级 → 触达 → 追踪，回应 HR「会不会 AI 获客」。",
    ["六段 pipeline", "122→120 清洗", "A43/B57/C20 分级", "漏斗 120→9"],
    "../02-项目/P01-AI获客/dashboard.html", "补充 · 证明流程能力", "t-blue", 0.08)}
</div>''')

    s2 = section("岗位需求要点", "来自 JD 原文与真实 HR 对话",
        f'''<div class="grid">
  {card("核心要求", "有可量化实战成果（关键词排名、AI 引用次数、线索增长），会看数据、能输出复盘。", 0, "JD 第 3 条", "t-red")}
  {card("真实对话", "HR 追问「数据怎么样呢」→ 对应第 3 条硬性筛选，必须用数字回答。", .08, "复盘", "t-gold")}
  {card("技能覆盖", "GEO 方法论 + 关键词矩阵 + 多平台引用监测 + 询盘漏斗，全部由 P01/P02 覆盖。", .16, "已补", "t-green")}
</div>''', tight=True)

    return page("AI搜索优化师/GEO运营 · 岗位展示", hero_html, s1 + s2,
        "岗位-AI搜索优化师GEO运营 · XiaoY · 点击卡片查看项目看板 · theme.py 统一主题", out_path=out_path)

def build_ai(out_path):
    hero_html = hero('AI 应用开发<br><em>Agent / RAG / Vibe Coding</em>',
        "从 RAG 最小应用到 LLM API 集成能力。代码全部可运行、可复现。",
        tagline="★ 求职岗位展示")

    s1 = section("项目作品集", "点击卡片打开对应看板",
        f'''<div class="grid grid-2">
  {link_card("P03 · RAG 问答系统",
    "纯 Python 从 0 实现：文档切分 → TF-IDF 向量化 → 余弦检索 → 生成，全链路可跑、可验证。",
    ["10 个文档块", "TF-IDF 226 维", "检索自检 4/4", "相似度最高 1.000"],
    "../02-项目/P03-RAG问答/dashboard.html", "P03 · 主力", "t-red", 0.0)}
</div>''')

    s2 = section("这条线还要补的能力", "对照市场 AI 应用开发岗位要求",
        f'''<div class="grid">
  {card("LLM API 真调", "接口已预留（OpenAI 兼容格式），配置 key 即可实跑。", 0, "待补", "t-gold")}
  {card("部署上线", "把 demo 部署成可访问服务，证明工程落地能力。", .08, "待补", "t-gold")}
  {card("Agent / 工具调用", "再做一个 Agent 项目，覆盖当前市场热点方向。", .16, "待补", "t-gold")}
</div>''', tight=True)

    return page("AI应用开发 · 岗位展示", hero_html, s1 + s2,
        "岗位-AI应用开发 · XiaoY · 点击卡片查看项目看板 · theme.py 统一主题", out_path=out_path)

if __name__ == "__main__":
    base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    g = build_geo(os.path.abspath(os.path.join(base, "AI搜索优化师GEO运营", "01-展示", "index.html")))
    a = build_ai(os.path.abspath(os.path.join(base, "AI应用开发", "01-展示", "index.html")))
    print("GEO 展示首页 OK")
    print("AI 展示首页 OK")
