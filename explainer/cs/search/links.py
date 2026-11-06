"""Links, duplicates, vectors and spelling (Part 47): PageRank by power iteration and HITS on a synthetic web with a
link farm; SimHash fingerprints that find near-duplicate passages (Charikar 2002); product quantization (Jégou et
al. 2011) and a small HNSW graph (Malkov and Yashunin) over passage vectors; noisy-channel spelling correction with a
BK-tree; and top-k autocompletion."""

from __future__ import annotations

import hashlib
import heapq
import math
import random
from collections import Counter, defaultdict

import numpy as np


# ---------------------------------------------------------------- link analysis

def synthetic_web(n=400, m=4, farm=20, seed=0):
    """Preferential attachment (a few hubs, many small pages) plus a link farm: farm pages that all link to one
    target and to each other."""
    rng = random.Random(seed)
    out = defaultdict(set)
    deg = [1] * n
    for v in range(1, n):
        for _ in range(min(m, v)):
            u = rng.choices(range(v), weights=deg[:v])[0]
            out[v].add(u)
            deg[u] += 1
            if rng.random() < 0.3:
                out[u].add(v)
    target = n - 1
    farm_nodes = list(range(n, n + farm))
    for f in farm_nodes:
        out[f].add(target)
        for g in farm_nodes:
            if g != f:
                out[f].add(g)
    return {v: sorted(s) for v, s in out.items()}, n + farm, target, farm_nodes


def pagerank(out, N, d=0.85, iters=100, tol=1e-12):
    r = np.full(N, 1 / N)
    hist = []
    for it in range(iters):
        nr = np.full(N, (1 - d) / N)
        dangling = 0.0
        for v in range(N):
            vs = out.get(v, [])
            if vs:
                share = d * r[v] / len(vs)
                for u in vs:
                    nr[u] += share
            else:
                dangling += d * r[v]
        nr += dangling / N
        diff = float(np.abs(nr - r).sum())
        hist.append(diff)
        r = nr
        if diff < tol:
            break
    return r, hist


def hits(out, N, iters=50):
    a = np.ones(N)
    h = np.ones(N)
    for _ in range(iters):
        a = np.zeros(N)
        for v, vs in out.items():
            for u in vs:
                a[u] += h[v]
        a /= np.linalg.norm(a)
        h = np.array([sum(a[u] for u in out.get(v, [])) for v in range(N)])
        h /= np.linalg.norm(h)
    return a, h


def link_experiment():
    out, N, target, farm = synthetic_web()
    r, hist = pagerank(out, N)
    rank = np.argsort(-r)
    pos = int(np.where(rank == target)[0][0]) + 1
    out_nf = {v: [u for u in vs] for v, vs in out.items() if v < N - len(farm)}
    r2, _ = pagerank(out_nf, N - len(farm))
    rank2 = np.argsort(-r2)
    pos2 = int(np.where(rank2 == target)[0][0]) + 1
    a, h = hits(out, N)
    return {"pages": N, "target": target, "rank_with_farm": pos, "rank_without_farm": pos2,
            "iterations": len(hist), "convergence": hist[:40], "top": [(int(i), float(r[i])) for i in rank[:10]],
            "hits_top_authority": int(np.argmax(a)), "hits_top_hub": int(np.argmax(h)),
            "farm_in_top_hubs": int(sum(1 for i in np.argsort(-h)[:20] if i in farm))}


# ---------------------------------------------------------------- SimHash

def _h64(s):
    return int.from_bytes(hashlib.blake2b(s.encode(), digest_size=8).digest(), "big")


def simhash(tokens, shingle=3):
    v = [0] * 64
    grams = [" ".join(tokens[i:i + shingle]) for i in range(max(1, len(tokens) - shingle + 1))]
    for g in grams:
        h = _h64(g)
        for b in range(64):
            v[b] += 1 if h >> b & 1 else -1
    return sum(1 << b for b in range(64) if v[b] > 0)


def hamming(a, b):
    return bin(a ^ b).count("1")


def simhash_experiment(docs, n=600, edits=(0, 1, 5, 20, 80), seed=1):
    """Fingerprint passages and lightly edited copies (k random words replaced): bit differences grow with edits,
    unrelated passages differ in about 32 bits."""
    from explainer.cs.search import text as T
    rng = random.Random(seed)
    sample = rng.sample(docs, n)
    rows = []
    for k in edits:
        ds = []
        for _, _, txt in sample[:200]:
            toks = T.tokens(txt)
            t2 = list(toks)
            for _ in range(k):
                t2[rng.randrange(len(t2))] = rng.choice(["foo", "bar", "baz", "qux"])
            ds.append(hamming(simhash(toks), simhash(t2)))
        rows.append({"edits": k, "mean_bits": sum(ds) / len(ds), "max_bits": max(ds)})
    un = [hamming(simhash(T.tokens(sample[i][2])), simhash(T.tokens(sample[i + 1][2]))) for i in range(0, 400, 2)]
    return {"rows": rows, "unrelated_mean": sum(un) / len(un), "unrelated_min": min(un)}


# ---------------------------------------------------------------- dense vectors

def passage_vectors(docs, dim=64, vocab=4000, seed=2):
    """A cheap embedding: tf-idf over the most common terms, projected to dim dimensions by a random Gaussian
    matrix (Johnson–Lindenstrauss) and normalized."""
    from explainer.cs.search import text as T
    rng = np.random.default_rng(seed)
    toks = [[t for t in T.tokens(txt) if t not in T.STOP] for _, _, txt in docs]
    df = Counter(t for ts in toks for t in set(ts))
    terms = [t for t, _ in df.most_common(vocab)]
    idx = {t: i for i, t in enumerate(terms)}
    N = len(docs)
    P = rng.normal(0, 1 / math.sqrt(dim), (len(terms), dim))
    X = np.zeros((N, dim), dtype=np.float32)
    for i, ts in enumerate(toks):
        c = Counter(t for t in ts if t in idx)
        for t, f in c.items():
            X[i] += (1 + math.log(f)) * math.log(N / df[t]) * P[idx[t]]
        nrm = np.linalg.norm(X[i])
        if nrm:
            X[i] /= nrm
    return X


def kmeans(X, k, iters=15, seed=0):
    rng = np.random.default_rng(seed)
    C = X[rng.choice(len(X), k, replace=False)].copy()
    for _ in range(iters):
        d = ((X[:, None, :] - C[None, :, :]) ** 2).sum(-1)
        a = d.argmin(1)
        for j in range(k):
            pts = X[a == j]
            if len(pts):
                C[j] = pts.mean(0)
    return C, a


def pq(X, m=8, k=256, seed=0):
    """Split each vector into m sub-vectors, quantize each to one of k centroids: m bytes per vector instead of
    4 * dim.  Returns the codebooks, codes and reconstruction error."""
    n, dim = X.shape
    s = dim // m
    books, codes = [], np.zeros((n, m), dtype=np.int32)
    recon = np.zeros_like(X)
    for j in range(m):
        C, a = kmeans(X[:, j * s:(j + 1) * s], k, seed=seed + j)
        books.append(C)
        codes[:, j] = a
        recon[:, j * s:(j + 1) * s] = C[a]
    err = float(((X - recon) ** 2).sum(1).mean())
    return books, codes, err


def pq_experiment(X, queries=200, ms=(2, 4, 8, 16), seed=3):
    rng = np.random.default_rng(seed)
    qi = rng.choice(len(X), queries, replace=False)
    exact = [set(np.argsort(-(X @ X[q]))[1:11]) for q in qi]
    rows = []
    for m in ms:
        books, codes, err = pq(X, m=m, k=256)
        s = X.shape[1] // m
        rec = 0.0
        for q, ex in zip(qi, exact):
            # asymmetric distance: query exact, database quantized
            tables = [((books[j] - X[q, j * s:(j + 1) * s]) ** 2).sum(1) for j in range(m)]
            d = sum(tables[j][codes[:, j]] for j in range(m))
            d[q] = np.inf
            got = set(np.argsort(d)[:10])
            rec += len(got & ex) / 10
        rows.append({"m": m, "bytes": m, "float_bytes": 4 * X.shape[1], "mse": err, "recall10": rec / queries})
    return rows


class HNSW:
    """A compact HNSW: each point gets a level from a geometric distribution; greedy search descends from the top
    level; on each level a beam search of width ef finds neighbours, keeping M links per node."""

    def __init__(self, X, M=8, ef=32, seed=4):
        self.X, self.M, self.ef = X, M, ef
        self.rng = random.Random(seed)
        self.levels, self.links, self.entry, self.top = [], [], None, -1
        self.dist_calls = 0
        for i in range(len(X)):
            self.insert(i)

    def d(self, a, q):
        self.dist_calls += 1
        return 1 - float(self.X[a] @ q)

    def search_layer(self, q, eps, ef, lev):
        seen = set(eps)
        cand = [(self.d(e, q), e) for e in eps]
        heapq.heapify(cand)
        best = [(-dd, e) for dd, e in cand]
        heapq.heapify(best)
        while cand:
            dd, c = heapq.heappop(cand)
            if dd > -best[0][0] and len(best) >= ef:
                break
            for nb in self.links[c].get(lev, []):
                if nb in seen:
                    continue
                seen.add(nb)
                dn = self.d(nb, q)
                if len(best) < ef or dn < -best[0][0]:
                    heapq.heappush(cand, (dn, nb))
                    heapq.heappush(best, (-dn, nb))
                    if len(best) > ef:
                        heapq.heappop(best)
        return sorted((-dd, e) for dd, e in best)

    def insert(self, i):
        lev = int(-math.log(1 - self.rng.random()) / math.log(self.M))
        self.levels.append(lev)
        self.links.append({})
        if self.entry is None:
            self.entry, self.top = i, lev
            return
        q = self.X[i]
        ep = [self.entry]
        for L in range(self.top, lev, -1):
            ep = [self.search_layer(q, ep, 1, L)[0][1]]
        for L in range(min(lev, self.top), -1, -1):
            res = self.search_layer(q, ep, self.ef, L)
            nbs = [e for _, e in res[:self.M]]
            self.links[i][L] = nbs
            for nb in nbs:
                lst = self.links[nb].setdefault(L, [])
                lst.append(i)
                if len(lst) > 2 * self.M:
                    lst.sort(key=lambda x: 1 - float(self.X[x] @ self.X[nb]))
                    del lst[2 * self.M:]
            ep = [e for _, e in res]
        if lev > self.top:
            self.entry, self.top = i, lev

    def query(self, q, k=10, ef=None):
        ep = [self.entry]
        for L in range(self.top, 0, -1):
            ep = [self.search_layer(q, ep, 1, L)[0][1]]
        return [e for _, e in self.search_layer(q, ep, ef or self.ef, 0)[:k]]


def hnsw_experiment(X, n=3000, queries=200, efs=(10, 20, 40, 80, 160), seed=5):
    rng = np.random.default_rng(seed)
    Xs = X[:n]
    g = HNSW(Xs)
    build_calls = g.dist_calls
    qi = rng.choice(n, queries, replace=False)
    rows = []
    for ef in efs:
        rec, calls = 0.0, 0
        for q in qi:
            exact = set(np.argsort(-(Xs @ Xs[q]))[:10])
            g.dist_calls = 0
            got = set(g.query(Xs[q], 10, ef))
            calls += g.dist_calls
            rec += len(got & exact) / 10
        rows.append({"ef": ef, "recall10": rec / queries, "distance_calls": calls / queries, "brute_force": n})
    return {"n": n, "levels": Counter(g.levels), "build_distance_calls": build_calls, "rows": rows}


# ---------------------------------------------------------------- spelling and completion

def edit_distance(a, b):
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


class BKTree:
    def __init__(self, words):
        it = iter(words)
        self.root = (next(it), {})
        self.calls = 0
        for w in it:
            self.add(w)

    def add(self, w):
        node = self.root
        while True:
            d = edit_distance(w, node[0])
            if d == 0:
                return
            if d in node[1]:
                node = node[1][d]
            else:
                node[1][d] = (w, {})
                return

    def near(self, w, tol):
        out, stack = [], [self.root]
        while stack:
            word, ch = stack.pop()
            self.calls += 1
            d = edit_distance(w, word)
            if d <= tol:
                out.append((d, word))
            for k, c in ch.items():
                if d - tol <= k <= d + tol:
                    stack.append(c)
        return sorted(out)


def spell_experiment(words, typos=("whale", "captian", "elizabth", "recieve", "seperate", "monstr", "londn")):
    """Noisy-channel correction: candidates within edit distance 2 from a BK-tree, ranked by P(word) (counts in the
    novels) with a penalty per edit; and how many distance computations the tree needs against the whole
    vocabulary."""
    c = Counter(words)
    vocab = [w for w, f in c.items() if f >= 3]
    tree = BKTree(vocab)
    rows = []
    for t in typos:
        tree.calls = 0
        cands = tree.near(t, 2)
        best = max(cands, key=lambda dw: math.log(c[dw[1]]) - 4 * dw[0])[1] if cands else None
        rows.append({"typed": t, "candidates": len(cands), "correction": best, "distance_calls": tree.calls})
    return {"vocab": len(vocab), "rows": rows}


def complete(words, prefixes=("wh", "ca", "eliz", "mon", "lo"), k=5):
    c = Counter(words)
    return {p: [w for w, _ in sorted(((w, f) for w, f in c.items() if w.startswith(p)), key=lambda x: -x[1])[:k]]
            for p in prefixes}
