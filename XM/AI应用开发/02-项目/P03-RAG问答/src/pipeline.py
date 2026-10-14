# -*- coding: utf-8 -*-
"""P03 RAG 问答：文档切分→向量化→检索→生成，全链路纯 Python 实现

零外部 LLM API 依赖（无 key 降级为检索拼接），向量用 numpy 余弦相似度。
"""
import os, re, json, math, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np

KNOWLEDGE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "knowledge.txt")

# ---------- M1 文档加载 + 切分 ----------
def load_doc(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def split_chunks(text, chunk_size=120, overlap=30):
    """按句切分，再合并到 chunk_size 附近，带 overlap"""
    # 按段落/句号切
    sentences = re.split(r"[。\n]+", text)
    sentences = [s.strip() for s in sentences if s.strip()]
    chunks, cur = [], ""
    for s in sentences:
        if len(cur) + len(s) > chunk_size and cur:
            chunks.append(cur)
            # overlap：保留末尾 overlap 字
            cur = cur[-overlap:] if overlap else ""
        cur += s + "。"
    if cur:
        chunks.append(cur)
    return chunks

# ---------- M2 向量化 + 检索 ----------
def tokenize(text):
    """简单分词：中文按字 + 英文按词，去停用词"""
    tokens = re.findall(r"[\u4e00-\u9fa5]|[a-zA-Z0-9]+", text.lower())
    stop = {"的", "了", "是", "和", "与", "在", "有", "为", "对", "等", "the", "a", "an", "to", "of", "and", "in"}
    return [t for t in tokens if t not in stop]

def build_vocab(chunks):
    """构建词表 + 文档频率（用于 IDF）"""
    vocab = {}
    for c in chunks:
        for t in set(tokenize(c)):  # 文档频率：每个词在一个块里只算一次
            vocab[t] = vocab.get(t, 0) + 1
    return vocab

def vectorize(text, vocab, idf):
    """TF-IDF 加权向量：高频词降权、稀有词升权，避免被通用词稀释"""
    tokens = tokenize(text)
    tf = {}
    for t in tokens:
        tf[t] = tf.get(t, 0) + 1
    vec = np.zeros(len(vocab))
    for t, cnt in tf.items():
        if t in vocab:
            vec[vocab[t]] = cnt * idf[t]
    return vec

def cosine_sim(a, b):
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    return float(np.dot(a, b) / (na * nb)) if na > 0 and nb > 0 else 0.0

def retrieve(query, chunks, chunk_vecs, top_k=3):
    qv = vectorize(query, VOCAB, IDF)
    sims = [cosine_sim(qv, cv) for cv in chunk_vecs]
    ranked = sorted(range(len(chunks)), key=lambda i: -sims[i])[:top_k]
    return [(chunks[i], sims[i]) for i in ranked]

# ---------- M3 生成（LLM 调用 or 降级拼接）----------
def generate(query, top_chunks):
    """有 API key 时调 LLM，否则降级为检索拼接"""
    api_key = os.environ.get("LLM_API_KEY", "")
    if api_key:
        # 预留 OpenAI 兼容接口（有 key 时启用）
        return _call_llm(api_key, query, top_chunks)
    # 降级：拼接检索到的相关片段作为回答
    context = "\n".join(f"[来源{i+1}] {c}" for i, (c, s) in enumerate(top_chunks))
    return f"（离线检索模式，未接 LLM）根据知识库，与你问题最相关的片段：\n\n{context}"

def _call_llm(api_key, query, top_chunks):
    """OpenAI 兼容接口桩：演示调用逻辑，需 urllib + key"""
    import urllib.request
    context = "\n".join(c for c, _ in top_chunks)
    payload = json.dumps({
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "你是 AI 应用开发助教，基于给定上下文回答。"},
            {"role": "user", "content": f"上下文：\n{context}\n\n问题：{query}"},
        ],
    }).encode("utf-8")
    req = urllib.request.Request("https://api.deepseek.com/chat/completions",
        data=payload, headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())["choices"][0]["message"]["content"]

# ---------- M4 评估（检索命中自检）----------
def evaluate(chunks, chunk_vecs):
    """已知问题应命中对应块：自检检索质量"""
    test_cases = [
        ("RAG 是什么", ["RAG", "检索增强"]),
        ("向量化用什么 embedding", ["embedding", "向量化"]),
        ("AI 应用开发要什么技能", ["Coding Agent", "验证"]),
        ("API 调用什么格式", ["OpenAI", "messages"]),
    ]
    results = []
    for q, keywords in test_cases:
        top = retrieve(q, chunks, chunk_vecs, top_k=3)
        top_text = " ".join(c for c, _ in top)
        hit = any(k.lower() in top_text.lower() for k in keywords)
        results.append((q, hit))
    return results

# ---------- 主流程 ----------
def main():
    print("=" * 56)
    print("P03 RAG 问答系统")
    print("=" * 56)

    text = load_doc(KNOWLEDGE)
    chunks = split_chunks(text)
    print(f"[M1 文档切分] {len(chunks)} 个块")

    global VOCAB, IDF
    VOCAB = build_vocab(chunks)
    N = len(chunks)
    # IDF = log(N / (文档频率))，+1 平滑
    IDF = {w: math.log((N + 1) / (df + 1)) + 1 for w, df in VOCAB.items()}
    chunk_vecs = [vectorize(c, VOCAB, IDF) for c in chunks]
    print(f"[M2 向量化] 词表大小 {len(VOCAB)}，TF-IDF 加权")

    # 演示问答
    questions = ["RAG 是什么？", "AI 应用开发工程师需要什么技能？", "大模型 API 怎么调用？"]
    print()
    for q in questions:
        top = retrieve(q, chunks, chunk_vecs)
        print(f"❓ {q}")
        print(f"   命中 {len(top)} 块，最高相似度 {top[0][1]:.3f}")
        ans = generate(q, top)
        print(f"   回答（节选）: {ans[:120]}...")
        print()

    # 评估
    evals = evaluate(chunks, chunk_vecs)
    passed = sum(1 for _, h in evals if h)
    print(f"[M4 评估] 检索命中自检 {passed}/{len(evals)} 通过")
    for q, h in evals:
        print(f"   {'✅' if h else '❌'} {q}")

    print("=" * 56)
    print("P03 完成 [OK]" if passed == len(evals) else "P03 有未命中，需检查")

if __name__ == "__main__":
    main()
