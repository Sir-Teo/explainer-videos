"""Lab 47: index a synthetic Zipfian corpus, intersect and compress its postings, and check WAND and PageRank against exhaustive answers."""

from videos.coursekit import labs  # noqa: I001  (must stay first: it lets explainer.cs import without manim)

import math

import numpy as np

from explainer.cs.search import index as ix
from explainer.cs.search import links as lk
from explainer.cs.search import rank as rk

TITLE = "Postings merged, compressed and pruned; PageRank as an eigenvector"
GOAL = ("Build the series' inverted index over 2,000 synthetic documents with Zipfian words, then check three "
        "claims: galloping beats the merge when list lengths differ, Rice codes come within a few percent of the "
        "bound log2 C(N, f), and WAND returns exactly the exhaustive BM25 top ten while scoring fewer documents; "
        "last, compare power-iteration PageRank with a direct linear solve.")
TASKS = [
    "Fix every Rice parameter at k = 0 (a unary code) or k = 8 in rice_total and compare the bits per posting with the per-list rule k = floor(log2(0.69 N / f)).",
    "Ask WAND for the top 1 and the top 100 instead of the top 10. How does the share of candidates it scores move, and why?",
    "Change the damping d from 0.85 to 0.5 and to 0.99 in lk.pagerank and count the iterations until the change is below 1e-10. Compare the count with log(1e-10) / log(d).",
]

N_DOCS, VOCAB, DOC_LEN = 2000, 3000, 150


def word(i):
    """A made-up word for rank i, letters only: 0 -> 'baa', 1 -> 'bab', ..."""
    s = ""
    for _ in range(3):
        s = "abcdefghijklmnopqrstuvwxyz"[i % 26] + s
        i //= 26
    return "b" + s


def corpus(rng):
    p = 1 / np.arange(1, VOCAB + 1)
    ranks = rng.choice(VOCAB, size=(N_DOCS, DOC_LEN), p=p / p.sum())
    return [(d, "synthetic", " ".join(word(int(r)) for r in row)) for d, row in enumerate(ranks)]


def rice_total(post):
    """(bits used by Rice codes with the per-list rule, the bound sum of log2 C(N, f)), over every postings list."""
    bits = bound = 0.0
    for ps in post.values():
        ids = [d for d, _ in ps]
        gaps = [ids[0] + 1] + [b - a for a, b in zip(ids, ids[1:])]
        k = max(0, int(math.log2(max(1.0, 0.69 * N_DOCS / len(gaps)))))
        bits += sum(ix.rice_bits(g, k) for g in gaps)
        bound += math.log2(math.comb(N_DOCS, len(gaps)))
    return bits, bound


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    post, lengths = ix.build(corpus(rng), stem=False)
    by_df = sorted(post, key=lambda t: -len(post[t]))
    lab.row("index", f"{N_DOCS:,} documents, {len(post):,} terms, {sum(len(v) for v in post.values()):,} postings")

    # 1. intersection: the three algorithms agree; galloping wins when the lists differ in length
    ratios, c_merge, c_gallop = [], [], []
    for _ in range(60):
        a = ix.docs_of(post, by_df[int(rng.integers(0, 40))])
        b = ix.docs_of(post, by_df[int(rng.integers(0, 1500))])
        (m, cm), (s, _), (g, cg) = ix.merge(a, b), ix.skips(a, b), ix.gallop(a, b)
        assert m == s == g == sorted(set(a) & set(b)), "three ways to intersect, one answer"
        assert cm <= len(a) + len(b), "the merge makes at most m + n comparisons"
        ratios.append(max(len(a), len(b)) / min(len(a), len(b)))
        c_merge.append(cm)
        c_gallop.append(cg)
    ratios, c_merge, c_gallop = map(np.array, (ratios, c_merge, c_gallop))
    lopsided = ratios > 30
    assert lopsided.sum() >= 5 and np.all(c_gallop[lopsided] < c_merge[lopsided]), "galloping wins on lopsided lists"
    lab.row("pairs with a length ratio above 30", f"{int(lopsided.sum())}; merge / galloping comparisons, median "
                                                  f"{np.median(c_merge[lopsided] / c_gallop[lopsided]):.1f}x")

    # 2. compression: gaps under four codes, against the bound log2 C(N, f)
    comp = ix.compress(post, N_DOCS)
    bpp = comp["bits_per_posting"]
    bits, bound = rice_total(post)
    assert abs(bits - comp["bits"]["rice"]) < 1e-6, "the same total as the library's"
    assert bound <= bits <= 1.1 * bound, "Rice with k from the mean gap is within 10% of the bound"
    assert bpp["rice"] < bpp["delta"] < bpp["vbyte"] < 32 and bpp["rice"] < bpp["gamma"]
    for g in (1, 2, 9, 1000):
        assert len(ix.gamma_code(g)) == ix.gamma_bits(g) == 2 * int(math.log2(g)) + 1
    lab.row("bits per posting", f"32-bit 32, variable byte {bpp['vbyte']:.2f}, gamma {bpp['gamma']:.2f}, delta "
                                f"{bpp['delta']:.2f}, Rice {bpp['rice']:.2f}; bound {bound / comp['postings']:.2f}")

    # 3. WAND: the exhaustive top ten, for fewer documents scored
    shares = []
    for _ in range(25):
        query = [by_df[int(i)] for i in rng.integers(5, 400, int(rng.integers(2, 4)))]
        scores = rk.bm25_scores(post, lengths, query)
        best = sorted(scores.values(), reverse=True)[:10]
        w = rk.wand(post, lengths, query, k=10)
        assert np.allclose(sorted((scores[d] for d in w["top"]), reverse=True), best, atol=1e-9), "WAND is safe"
        assert w["scored"] <= w["candidates"] == len(scores)
        shares.append(w["scored"] / w["candidates"])
    assert np.mean(shares) < 0.9, "and it skips documents"
    lab.row("WAND on 25 queries", f"top ten identical to exhaustive BM25; {np.mean(shares):.0%} of candidates scored on average")

    # 4. PageRank: power iteration against the linear system (I - d P) r = (1 - d) / N
    out, n, target, farm = lk.synthetic_web(n=300, farm=15, seed=seed)
    r, hist = lk.pagerank(out, n)
    P = np.zeros((n, n))
    for v in range(n):
        if out.get(v):
            P[out[v], v] = 1 / len(out[v])
        else:
            P[:, v] = 1 / n
    direct = np.linalg.solve(np.eye(n) - 0.85 * P, np.full(n, 0.15 / n))
    assert abs(r.sum() - 1) < 1e-9 and np.abs(r - direct).max() < 1e-9, "the stationary distribution"
    assert all(b <= 0.85 * a + 1e-15 for a, b in zip(hist, hist[1:])), "each step shrinks the change by at least d"
    no_farm = lk.pagerank({v: us for v, us in out.items() if v not in farm}, n - len(farm))[0]
    rank_with, rank_without = int((r > r[target]).sum()) + 1, int((no_farm > no_farm[target]).sum()) + 1
    assert rank_with < rank_without, "a link farm lifts its target"
    lab.row("PageRank", f"power iteration equals the linear solve to {np.abs(r - direct).max():.0e} after {len(hist)} "
                        f"steps; the farm lifts its target from rank {rank_without} to {rank_with}")
    lab.note = ("Sorted lists make a query a merge, gaps between sorted ids are small numbers that a Rice code "
                "stores near the counting bound, and score upper bounds let WAND skip most documents without "
                "changing the top ten.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    order = np.argsort(ratios)
    ax[0].loglog(ratios[order], c_merge[order], "o", ms=4, color=labs.RED, label="linear merge")
    ax[0].loglog(ratios[order], c_gallop[order], "o", ms=4, color=labs.GREEN, label="galloping search")
    ax[0].set(title="Comparisons to intersect two postings lists", xlabel="longer list / shorter list",
              ylabel="comparisons")
    ax[0].legend()
    names = ["variable byte", "gamma", "delta", "Rice"]
    vals = [bpp["vbyte"], bpp["gamma"], bpp["delta"], bpp["rice"]]
    ax[1].set_axisbelow(True)
    ax[1].bar(names, vals, color=[labs.GREY, labs.BLUE, labs.PURPLE, labs.GOLD])
    ax[1].axhline(bound / comp["postings"], color=labs.GREEN, ls="--", label="bound: log2 C(N, f) per posting")
    for i, v in enumerate(vals):
        ax[1].text(i, v + 0.15, f"{v:.2f}", ha="center")
    ax[1].set(title="Bits per posting (gaps between document ids)", ylabel="bits")
    ax[1].legend()
    lab.fig = fig
    return lab
