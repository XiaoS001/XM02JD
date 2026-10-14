# -*- coding: utf-8 -*-
"""M1 关键词矩阵：围绕种子词生成四类关键词

每词带：类别、搜索意图、竞争度(0-10)、预估月搜索量、优先级评分
"""
import json, os, random, hashlib
from config import TEMPLATES, SEED_WORD, BRAND, KW_FILE

random.seed(20261014)

INTENT = {
    "需求词": "信息型（了解怎么学）",
    "课程词": "交易型（准备报名）",
    "对比词": "比较型（正在选机构）",
    "长尾问答词": "问答型（具体疑问）",
}

def score_word(word, cat):
    """竞争度与优先级（确定性伪随机，保证可复现）"""
    h = int(hashlib.md5(word.encode()).hexdigest(), 16)
    competition = h % 11                      # 0-10
    volume = 50 + (h >> 8) % 5000             # 50-5000
    # 优先级 = 意图价值 * (10-竞争度)，交易/比较型价值更高
    intent_value = {"需求词": 2, "课程词": 5, "对比词": 5, "长尾问答词": 3}[cat]
    priority = intent_value * (10 - competition) + (volume // 500)
    return competition, volume, priority

def generate():
    words = []
    for cat, tpls in TEMPLATES.items():
        for tpl in tpls:
            w = tpl.format(seed=SEED_WORD)
            comp, vol, prio = score_word(w, cat)
            words.append({
                "keyword": w,
                "category": cat,
                "intent": INTENT[cat],
                "competition": comp,
                "est_volume": vol,
                "priority": prio,
                "brand_related": BRAND[:2] in w,
            })
    return words

def run(out_path):
    words = generate()
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(words, f, ensure_ascii=False, indent=2)
    from collections import Counter
    dist = Counter(w["category"] for w in words)
    high_p = [w for w in words if w["priority"] >= 25]
    return len(words), dict(dist), len(high_p)

if __name__ == "__main__":
    from config import KW_FILE
    n, dist, hp = run(KW_FILE)
    print(f"M1 完成：生成 {n} 个关键词 -> {KW_FILE}")
    print(f"   分布: {dist}")
    print(f"   高优先级词(>=25): {hp} 个")
