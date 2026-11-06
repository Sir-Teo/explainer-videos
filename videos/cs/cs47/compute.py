"""Precompute everything numerical in Part 47 of *Computer Science, Built* ("Search Engines").

    python -m videos.cs.cs47.compute              # everything missing
    python -m videos.cs.cs47.compute --force bm25

Results are cached in ``.cache/cs47/<name>.json``; scenes call ``load(name)``.  The instruments are
``explainer/cs/search/`` (text, index, rank, links); tests in tests/test_cs47_search.py.  The corpus is the thirty
novels cut into passages of 400 words (11,261 documents).

Items:
    porter      Porter's stemmer against the published examples; stems of sample words
    zipf        Zipf's law (rank against frequency) and Heaps' law (vocabulary against tokens) fitted on the novels
    index       the inverted index: terms, postings, the postings of a few terms
    intersect   comparisons for merge, skip pointers and galloping on five queries
    phrase      a phrase query over positions
    codes       postings compressed as gaps: bits per posting for 32-bit, vbyte, gamma, delta, Rice; sample codes
    bm25        BM25's saturation curves; BM25 against tf-idf on nine queries with rule-based judgments
    wand        WAND: documents fully scored against all candidates, with identical top tens
    pagerank    PageRank and HITS on a synthetic web with a link farm
    simhash     SimHash bit differences against edits; unrelated passages
    pq          product quantization: bytes per vector, distortion and recall of the top ten
    hnsw        HNSW: recall against distance computations
    spell       noisy-channel spelling correction with a BK-tree; autocompletion
    bound       the information-theoretic minimum bits per posting, log2 C(N, f) summed over terms
    engine      our engine answering queries over the novels with snippets
"""

from __future__ import annotations

from explainer.ai.cache import Cache

CACHE = Cache("cs47")
load = CACHE.load
_STATE = {}


def _index():
    if "post" not in _STATE:
        from explainer.cs.search import index as I, text as T
        docs = T.corpus()
        post, lengths = I.build(docs)
        _STATE.update(docs=docs, post=post, lengths=lengths)
    return _STATE["docs"], _STATE["post"], _STATE["lengths"]


def _vectors():
    if "X" not in _STATE:
        from explainer.cs.search import links as K
        _STATE["X"] = K.passage_vectors(_index()[0])
    return _STATE["X"]


def compute_porter() -> dict:
    from explainer.cs.search import text as T
    words = ["whaling", "whales", "harpooned", "connection", "connected", "connecting", "generalizations",
             "happiness", "relational", "running", "ran"]
    return {"published": T.check_porter(), "samples": {w: T.porter(w) for w in words}}


def compute_zipf() -> dict:
    from explainer.cs.search import text as T
    docs, _, _ = _index()
    ws = [w for _, _, t in docs for w in T.tokens(t)]
    return T.zipf_heaps(ws)


def compute_index() -> dict:
    docs, post, lengths = _index()
    sample = {t: [d for d, _ in post[t][:12]] for t in ("whale", "ahab", "darci", "holm") if t in post}
    return {"docs": len(docs), "terms": len(post), "postings": sum(len(v) for v in post.values()),
            "tokens": sum(lengths), "df": {t: len(post[t]) for t in sample}, "sample": sample}


def compute_intersect() -> dict:
    from explainer.cs.search import index as I
    _, post, _ = _index()
    return {"rows": I.intersect_experiment(post, [("whale", "sea"), ("captain", "ahab"), ("love", "marriag"),
                                                  ("the", "whale"), ("elizabeth", "darci")])}


def compute_phrase() -> dict:
    from explainer.cs.search import index as I
    docs, post, _ = _index()
    out = {}
    for ph in (["white", "whale"], ["mr", "darcy"], ["call", "me", "ishmael"], ["sherlock", "holmes"]):
        hits = I.phrase(post, ph)
        both = set(I.docs_of(post, __import__("explainer.cs.search.text", fromlist=["porter"]).porter(ph[0])))
        for w in ph[1:]:
            both &= set(I.docs_of(post, __import__("explainer.cs.search.text", fromlist=["porter"]).porter(w)))
        out[" ".join(ph)] = {"phrase_docs": len(hits), "all_words_docs": len(both),
                             "first": [(d, docs[d][1]) for d, _ in hits[:3]]}
    return out


def compute_codes() -> dict:
    from explainer.cs.search import index as I
    docs, post, _ = _index()
    c = I.compress(post, len(docs))
    samples = {g: {"gamma": I.gamma_code(g), "delta": I.delta_code(g), "rice2": I.rice_code(g, 2)}
               for g in (1, 2, 3, 4, 5, 9, 17, 100)}
    return {**c, "samples": samples}


def compute_bm25() -> dict:
    from explainer.cs.search import rank as R
    docs, post, lengths = _index()
    sat = R.saturation()
    return {"saturation": {str(k): v for k, v in sat.items()}, **R.evaluate(docs, post, lengths)}


def compute_wand() -> dict:
    from explainer.cs.search import rank as R, text as T
    _, post, lengths = _index()
    rows = []
    for q in ("white whale", "captain ahab ship", "the sea", "love marriage money", "pride prejudice"):
        terms = [T.porter(w) for w in T.tokens(q)]
        w = R.wand(post, lengths, terms)
        sc = R.bm25_scores(post, lengths, terms)
        ex = R.top(sc)
        same = [round(sc[d], 9) for d in w["top"]] == [round(sc[d], 9) for d in ex]   # equal up to ties
        rows.append({"query": q, "scored": w["scored"], "candidates": w["candidates"], "same_top10": same})
    return {"rows": rows}


def compute_pagerank() -> dict:
    from explainer.cs.search import links as K
    return K.link_experiment()


def compute_simhash() -> dict:
    from explainer.cs.search import links as K
    return K.simhash_experiment(_index()[0])


def compute_pq() -> dict:
    from explainer.cs.search import links as K
    return {"rows": K.pq_experiment(_vectors(), queries=100), "dim": 64}


def compute_hnsw() -> dict:
    from explainer.cs.search import links as K
    r = K.hnsw_experiment(_vectors())
    r["levels"] = {str(k): v for k, v in r["levels"].items()}
    return r


def compute_spell() -> dict:
    from explainer.cs.search import links as K, text as T
    docs, _, _ = _index()
    ws = [w for _, _, t in docs for w in T.tokens(t)]
    return {**K.spell_experiment(ws), "complete": K.complete(ws)}


def compute_bound() -> dict:
    """The fewest bits any code can spend on a list of f document ids out of N (without exploiting clustering):
    log2 C(N, f).  Summed over the vocabulary, per posting, against the codes."""
    import math
    docs, post, _ = _index()
    N = len(docs)
    tot = sum((math.lgamma(N + 1) - math.lgamma(len(v) + 1) - math.lgamma(N - len(v) + 1)) / math.log(2)
              for v in post.values())
    n = sum(len(v) for v in post.values())
    return {"docs": N, "postings": n, "bound_bits_per_posting": tot / n}


def compute_engine() -> dict:
    """Three queries answered end to end: BM25 over the index, phrase boost, and a snippet around the best window."""
    from explainer.cs.search import rank as R, text as T
    docs, post, lengths = _index()
    out = []
    for q in ("white whale", "call me ishmael", "pride and prejudice", "the hound on the moor"):
        terms = [T.porter(w) for w in T.tokens(q) if w not in T.STOP]
        sc = R.bm25_scores(post, lengths, terms)
        best = R.top(sc, 5)
        res = []
        for d in best:
            toks = docs[d][2].split()
            stems = [T.porter(w.lower().strip(".,;:!?\"'()")) for w in toks]
            pos = next((i for i, s in enumerate(stems) if s in terms), 0)
            snip = " ".join(toks[max(0, pos - 8):pos + 12])
            res.append({"doc": d, "book": docs[d][1], "score": sc[d], "snippet": snip})
        out.append({"query": q, "terms": terms, "results": res})
    return {"queries": out}


ITEMS = {k[8:]: v for k, v in globals().items() if k.startswith("compute_")}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
