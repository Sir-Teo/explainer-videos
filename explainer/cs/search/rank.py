"""Ranking (Part 47): tf-idf with cosine normalization and BM25 (Robertson et al.), evaluated by precision, MAP and
nDCG on a small query set with rule-based judgments; and WAND (Broder et al. 2003), which skips documents whose score
upper bound cannot reach the current top k, counting how many it fully scores."""

from __future__ import annotations

import heapq
import math
from collections import defaultdict

from explainer.cs.search import text as T


def idf_bm25(N, df):
    return math.log(1 + (N - df + 0.5) / (df + 0.5))


def bm25_scores(post, lengths, query, k1=1.2, b=0.75):
    N = len(lengths)
    if not N:
        return {}
    avg = sum(lengths) / N
    sc = defaultdict(float)
    for q in query:
        ps = post.get(q, [])
        if not ps:
            continue
        idf = idf_bm25(N, len(ps))
        for d, pos in ps:
            tf = len(pos)
            sc[d] += idf * tf * (k1 + 1) / (tf + k1 * (1 - b + b * lengths[d] / avg))
    return sc


def tfidf_scores(post, lengths, query):
    """lnc.ltc-style: (1 + log tf) * log(N/df), documents normalized by length (a cheap stand-in for the vector
    norm)."""
    N = len(lengths)
    sc = defaultdict(float)
    for q in query:
        ps = post.get(q, [])
        if not ps:
            continue
        idf = math.log(N / len(ps))
        for d, pos in ps:
            sc[d] += (1 + math.log(len(pos))) * idf / math.sqrt(lengths[d])
    return sc


def top(sc, k=10):
    """Highest score first, with ties broken by increasing document ID."""
    return [d for d, _ in heapq.nlargest(k, sc.items(), key=lambda x: (x[1], -x[0]))]


def saturation(k1s=(0.5, 1.2, 2.0, 5.0), tfs=range(0, 21)):
    """BM25's term-frequency factor tf (k1 + 1) / (tf + k1) for several k1 (b = 0): it saturates at k1 + 1."""
    return {k1: [(tf, tf * (k1 + 1) / (tf + k1)) for tf in tfs] for k1 in k1s}


# ---------------------------------------------------------------- evaluation

def ndcg(ranked, grades, k=10):
    dcg = sum((2 ** grades.get(d, 0) - 1) / math.log2(i + 2) for i, d in enumerate(ranked[:k]))
    ideal = sorted(grades.values(), reverse=True)[:k]
    idcg = sum((2 ** g - 1) / math.log2(i + 2) for i, g in enumerate(ideal))
    return dcg / idcg if idcg else 0.0


def avg_precision(ranked, rel, k=10):
    if k <= 0:
        return 0.0
    hits, s = 0, 0.0
    for i, d in enumerate(ranked[:k]):
        if d in rel:
            hits += 1
            s += hits / (i + 1)
    return s / min(len(rel), k) if rel else 0.0


QUERIES = [
    ("white whale", "Moby Dick", ["white", "whale"]),
    ("captain ahab", "Moby Dick", ["captain", "ahab"]),
    ("elizabeth darcy pride", "Pride and Prejudice", ["elizabeth", "darcy"]),
    ("emma knightley", "Emma", ["emma", "knightley"]),
    ("sherlock holmes", "The Adventures of Sherlock Holmes", ["holmes"]),
    ("long john silver", "Treasure Island", ["silver", "john"]),
    ("heathcliff catherine", "Wuthering Heights", ["heathcliff", "catherine"]),
    ("monster creator", "Frankenstein", ["monster", "creator"]),
    ("vampire count", "Dracula", ["count", "vampire"]),
]


def judge(docs, book_hint, must):
    """Rule-based grades (illustrative, not human judgments): 2 if a passage of the intended book contains every
    'must' word, 1 if it contains one of them, else 0."""
    g = {}
    for did, title, txt in docs:
        if book_hint.lower().replace("'", "") not in title.lower().replace("'", "").replace("-", " "):
            continue
        toks = set(T.tokens(txt))
        n = sum(1 for m in must if m in toks)
        if n == len(must):
            g[did] = 2
        elif n:
            g[did] = 1
    return g


def evaluate(docs, post, lengths, queries=QUERIES):
    rows = []
    for q, book, must in queries:
        terms = [T.porter(w) for w in T.tokens(q)]
        grades = judge(docs, book, must)
        rel = {d for d, g in grades.items() if g == 2}
        r1 = top(bm25_scores(post, lengths, terms))
        r2 = top(tfidf_scores(post, lengths, terms))
        rows.append({"query": q, "book": book, "judged": len(grades), "relevant": len(rel),
                     "bm25": {"ndcg": ndcg(r1, grades), "ap": avg_precision(r1, rel),
                              "p10": sum(1 for d in r1 if d in rel) / 10},
                     "tfidf": {"ndcg": ndcg(r2, grades), "ap": avg_precision(r2, rel),
                               "p10": sum(1 for d in r2 if d in rel) / 10}})
    mean = {m: {k: sum(r[m][k] for r in rows) / len(rows) for k in ("ndcg", "ap", "p10")} for m in ("bm25", "tfidf")}
    return {"rows": rows, "mean": mean}


# ---------------------------------------------------------------- WAND

def wand(post, lengths, query, k=10, k1=1.2, b=0.75):
    """Document-at-a-time with WAND: each term's cursor has an upper bound on its score contribution; sort cursors by
    current doc, find the pivot where the sum of upper bounds first exceeds the threshold (the k-th best score), and
    skip every cursor before it to the pivot document.  Returns the top k and how many documents were scored."""
    N = len(lengths)
    if k <= 0 or not N:
        return {"top": [], "scored": 0, "candidates": len({d for q in query for d, _ in post.get(q, [])})}
    avg = sum(lengths) / N
    lists, ub = [], []
    for q in query:
        ps = post.get(q, [])
        if not ps:
            continue
        idf = idf_bm25(N, len(ps))
        sc = [(d, idf * len(p) * (k1 + 1) / (len(p) + k1 * (1 - b + b * lengths[d] / avg))) for d, p in ps]
        lists.append(sc)
        ub.append(max(s for _, s in sc))
    cur = [0] * len(lists)
    heap, scored, theta = [], 0, 0.0
    while True:
        live = [i for i in range(len(lists)) if cur[i] < len(lists[i])]
        if not live:
            break
        live.sort(key=lambda i: lists[i][cur[i]][0])
        acc, pivot = 0.0, None
        for i in live:
            acc += ub[i]
            if acc >= theta:
                pivot = i
                break
        if pivot is None:
            break
        pd = lists[pivot][cur[pivot]][0]
        first = lists[live[0]][cur[live[0]]][0]
        if first == pd:
            s = 0.0
            for i in live:
                if cur[i] < len(lists[i]) and lists[i][cur[i]][0] == pd:
                    s += lists[i][cur[i]][1]
                    cur[i] += 1
            scored += 1
            if len(heap) < k:
                heapq.heappush(heap, (s, -pd))
            elif (s, -pd) > heap[0]:
                heapq.heapreplace(heap, (s, -pd))
            if len(heap) == k:
                theta = heap[0][0]
        else:
            for i in live:
                if lists[i][cur[i]][0] >= pd:
                    break
                L = lists[i]
                while cur[i] < len(L) and L[cur[i]][0] < pd:
                    cur[i] += 1
    exhaustive = len({d for L in lists for d, _ in L})
    return {"top": [-d for _, d in sorted(heap, reverse=True)], "scored": scored, "candidates": exhaustive}
