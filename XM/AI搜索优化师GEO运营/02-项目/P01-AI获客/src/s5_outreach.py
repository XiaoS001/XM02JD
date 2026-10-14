# -*- coding: utf-8 -*-
"""S5 触达：生成个性化触达内容 + mock 落库

对 A/B 级线索生成个性化话术（不真发，只记录触达动作）。
个性化体现在：行业、城市、规模、公司名都进了话术模板。
"""
import json
import os
from datetime import datetime

def build_message(lead):
    """按线索特征生成个性化话术"""
    if lead["industry"] == "电商":
        pain = "电商订单增长"
    elif lead["industry"] == "SaaS":
        pain = "订阅客户续费"
    elif lead["industry"] == "本地服务":
        pain = "本地客流"
    else:
        pain = "业务增长"

    return (
        f"{lead['company']}（{lead['city']}）的负责人您好，"
        f"看到贵司在{lead['industry']}领域深耕，我们有一款针对{pain}的 AI 工具，"
        f"已帮助多家{lead['scale']}企业提升获客效率。"
        f"方便的话想约您 15 分钟聊聊。"
    )

def run(in_path, out_path):
    with open(in_path, "r", encoding="utf-8") as f:
        leads = json.load(f)

    outreach = []
    for l in leads:
        if l["grade"] in ("A", "B"):
            outreach.append({
                "raw_id": l["raw_id"],
                "company": l["company"],
                "grade": l["grade"],
                "channel": "email(mock)",
                "to": l["email"] if l["email_status"] == "valid" else "(不可触达)",
                "message": build_message(l),
                "sent_at": datetime.now().isoformat(timespec="seconds"),
                "status": "mock_sent",  # mock 触达，不真发
            })

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(outreach, f, ensure_ascii=False, indent=2)
    return len(outreach)

if __name__ == "__main__":
    from config import SCORED_FILE, OUTREACH_FILE
    n = run(SCORED_FILE, OUTREACH_FILE)
    print(f"S5 完成：生成 {n} 条个性化触达(mock) -> {OUTREACH_FILE}")
