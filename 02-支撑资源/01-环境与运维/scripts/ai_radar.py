#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 动态查证脚本（可复用）
用途：一键抓取 GitHub 新仓库 + Hacker News AI 热点，输出结构化简报。
用法：python ai_radar.py [输出目录]
作者：XiaoY　2026-10-13
"""

import io
import os
import sys
import json
import urllib.request
import urllib.parse
from datetime import datetime, timedelta, timezone

# ============ 配置 ============
GITHUB_MIRRORS = [
    "https://gh-proxy.com",
    "https://ghfast.top",
    "https://ghproxy.net",
]
HN_URL = "https://hn.algolia.com/api/v1/search_by_date"


def fetch(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 xiaoy-radar"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", errors="replace")


def github_api(path, query=""):
    """依次尝试镜像访问 GitHub API，全部失败返回 None。"""
    qs = urllib.parse.urlencode(query)
    tail = path + ("?" + qs if qs else "")
    for m in GITHUB_MIRRORS:
        try:
            url = m + "/https://api.github.com/" + tail
            return json.loads(fetch(url))
        except Exception as e:
            continue
    return None


def new_repos(days=14, topic=None, per_page=12):
    since = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%d")
    q = "created:>%s" % since
    if topic:
        q = "%s %s" % (topic, q)
    return github_api("search/repositories", {"q": q, "sort": "stars", "order": "desc", "per_page": per_page})


def hn_ai(points=100, hits=15):
    try:
        url = HN_URL + "?" + urllib.parse.urlencode({
            "query": "AI", "tags": "story",
            "numericFilters": "points>%d" % points, "hitsPerPage": hits,
        })
        return json.loads(fetch(url))
    except Exception:
        return None


def main():
    out_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    os.makedirs(out_dir, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_path = os.path.join(out_dir, "ai-radar-%s.md" % stamp)

    lines = []
    lines.append("# AI 动态雷达 %s" % datetime.now().strftime("%Y-%m-%d %H:%M"))
    lines.append("")
    lines.append("> 数据源：GitHub API（经镜像）/ Hacker News API；生成：XiaoY")
    lines.append("")

    # 1. GitHub 新仓库
    lines.append("## 一、GitHub 近 14 天新仓库（按 star）")
    lines.append("")
    repos = new_repos(14)
    if repos and repos.get("items"):
        lines.append("| 仓库 | star | 创建 | 说明 |")
        lines.append("|---|---|---|---|")
        for it in repos["items"]:
            desc = (it.get("description") or "").replace("|", "/")[:80]
            lines.append("| %s | %s | %s | %s |" % (it["full_name"], it["stargazers_count"], it["created_at"][:10], desc))
    else:
        lines.append("⚠️ GitHub API 镜像不可达，跳过。")
    lines.append("")

    # 2. HN 热点
    lines.append("## 二、Hacker News AI 高热度讨论（points>100）")
    lines.append("")
    hn = hn_ai(100)
    if hn and hn.get("hits"):
        lines.append("| 日期 | 热度 | 标题 |")
        lines.append("|---|---|---|")
        for h in hn["hits"]:
            lines.append("| %s | %s | %s |" % (h["created_at"][:10], h["points"], h["title"].replace("|", "/")))
    else:
        lines.append("⚠️ HN API 不可达，跳过。")
    lines.append("")

    with io.open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("WROTE", out_path)


if __name__ == "__main__":
    main()
