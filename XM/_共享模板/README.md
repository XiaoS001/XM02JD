# 共享主题模块 v2

> 建立：2026-10-15　**视觉对标「面试帝」，代码组织学「Magic UI」**
> 融合流程见 [效果页面融合流程.md](<效果页面融合流程.md>)

## 融合策略

| 层 | 来源 | 学到的 |
|---|---|---|
| **视觉层** | 面试帝 | 暖色系、中文宋体大字（clamp 82px）、22px 大圆角、快出慢入缓动 |
| **架构层** | Magic UI | 模块化组件函数、设计 token、按需引用 |

## 文件

| 文件 | 用途 |
|---|---|
| `theme.py` | **核心**：设计 token + CSS + 组件函数 |
| `build_showcase.py` | 岗位展示首页生成器 |
| `效果页面融合流程.md` | ★ **以后看到新效果，按它走** |
| `render/` | 渲染验证截图 |
| `v2-test-results.json` | 测试结果（16/16 通过） |

## 组件函数 API

```python
from theme import page, hero, section, kpi, dark_kpi, hbar, funnel_svg, card, link_card, table, note, wave, dark_block

hero(title_html, lead, tagline=None)       # 首屏（声波 + 大字 + 网格背景）
section(title, sub, content, delay, tight)  # 章节
kpi(value, label, delay, counted)           # KPI（counted=True 数字滚动）
dark_kpi(value, label)                      # 深色区数字
hbar(items, color)                          # 条形图（带进场）
funnel_svg(stages)                          # 漏斗图
card(title, body, delay, tag, tag_class)    # 卡片
link_card(title, body, nums, href, tag)     # 链接卡片（带数字标签）
table(headers, rows, delay)                 # 表格
note(content, delay)                        # 提示块
dark_block(title, sub, kpis_html)           # 深色区块
page(title, hero, body, footer, out_path)   # 组装整页
```

## 关键视觉参数（提取自面试帝）

| 参数 | 值 | 说明 |
|---|---|---|
| 标题字号 | `clamp(46px,6vw,82px)` | 比 v1 大 58% |
| 标题字距 | `-2px` | 大字要收紧 |
| 卡片圆角 | `22px` | 高级感来源 |
| 卡片内边距 | `42px` | 呼吸感来源 |
| 缓动 | `cubic-bezier(.2,.8,.2,1)` | 快出慢入 |
| 网格背景 | `48px` 方格 | 细节质感 |
| section 间距 | `100px` | 版式节奏 |

## 重构成果

| 项目 | 重构前 | 重构后 | 变化 |
|---|---|---|---|
| P01 visualize.py | 5.8KB | 3.6KB | -38% |
| P02 visualize.py | 5.2KB | 3.6KB | -31% |
| P03 visualize.py | 4.4KB | 3.4KB | -23% |

## 测试结果：16/16 通过

- 视觉规范 7 项（大字/圆角/缓动/网格/宋体/内边距/间距）✅
- 功能 5 项（渐显/数字滚动/进度条/错峰/条形图）✅
- 无障碍 2 项（reduced-motion / noscript）✅
- 数字一致性 1 项 ✅
- 渲染验证 1 项（5 张截图）✅

## 用法

```python
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "...", "_共享模板"))
from theme import page, hero, section, kpi

html = page(
    "标题",
    hero('大标题<br><em>强调</em>', "副标题", tagline="标签"),
    section("章节", "副标题", f'<div class="kpis">{kpi(100, "指标", 0, True)}</div>'),
    "底部文字",
    out_path="dashboard.html"
)
```
