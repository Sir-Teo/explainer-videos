"""The House's text features (Part 28).

**Counting.**  :func:`tokenize` (lower-case words; numbers and punctuation dropped), :func:`dtm` (a document-term
matrix over a fixed vocabulary), :func:`zipf` (the rank-frequency law and its fitted exponent), :func:`tfidf`.

**Dictionaries.**  :func:`tone` counts a document's words in the Loughran-McDonald lists (Loughran and McDonald 2011):
the shares of negative, positive and uncertainty words, and net tone (positive minus negative, over all words).

**Supervised text.**  SESTM (Ke, Kelly and Xiu 2019): :func:`sestm_screen` keeps the words whose appearances side with
positive outcomes more (or less) often than chance; :func:`sestm_topics` estimates the positive and negative topics
O+ and O- by regressing the screened words' frequencies on the documents' outcome ranks; :func:`sestm_score` scores a
new document by penalized maximum likelihood, p = argmax sum_j d_j log(p O+_j + (1 - p) O-_j) + lam log(p(1 - p)).

**Meaning.**  :func:`ppmi_svd` builds word vectors from co-occurrence (positive pointwise mutual information, then a
truncated SVD: Levy and Goldberg's (2014) reading of word2vec); :func:`neighbours`; :func:`nmf_topics` factorises the
tf-idf matrix into topics (non-negative matrix factorisation, a stand-in for LDA with the same output: topics as
word weights, documents as topic shares).

**Form.**  :func:`fog` (Gunning's fog index), :func:`word_diff` (what changed between two statements, word by word).

**Time.**  :func:`point_in_time_vocab` keeps only words seen before a date: the first defence against look-ahead.
"""

from __future__ import annotations

import difflib
import math
import re
from collections import Counter

import numpy as np

_WORD = re.compile(r"[a-z][a-z'\-]*[a-z]|[a-z]")


def tokenize(text: str) -> list[str]:
    """Lower-case word tokens: letters with inner hyphens and apostrophes; numbers and punctuation dropped."""
    return _WORD.findall(text.lower().replace("’", "'"))


def vocabulary(token_lists, min_df: int = 2, max_df: float = 1.0, stop=()) -> list[str]:
    """Words in at least ``min_df`` documents and at most a share ``max_df`` of them, sorted."""
    df = Counter()
    for toks in token_lists:
        df.update(set(toks))
    n = len(token_lists)
    stop = set(stop)
    return sorted(w for w, c in df.items() if c >= min_df and c <= max_df * n and w not in stop)


def dtm(token_lists, vocab) -> np.ndarray:
    """Counts: documents x vocabulary (int32)."""
    ix = {w: i for i, w in enumerate(vocab)}
    D = np.zeros((len(token_lists), len(vocab)), np.int32)
    for r, toks in enumerate(token_lists):
        for w in toks:
            j = ix.get(w)
            if j is not None:
                D[r, j] += 1
    return D


def tfidf(D) -> np.ndarray:
    """Term frequency times inverse document frequency, rows scaled to unit length."""
    D = np.asarray(D, float)
    tf = D / np.maximum(D.sum(1, keepdims=True), 1)
    idf = np.log((1 + len(D)) / (1 + (D > 0).sum(0))) + 1
    X = tf * idf
    return X / np.maximum(np.linalg.norm(X, axis=1, keepdims=True), 1e-12)


def zipf(tokens) -> dict:
    """Rank-frequency of a corpus and the slope of log frequency on log rank (ranks 10 to 1,000)."""
    c = np.array(sorted(Counter(tokens).values(), reverse=True), float)
    r = np.arange(1, len(c) + 1)
    m = (r >= 10) & (r <= min(1000, len(c)))
    slope, icpt = np.polyfit(np.log(r[m]), np.log(c[m]), 1)
    return {"rank": r, "freq": c, "slope": float(slope), "intercept": float(icpt), "n_types": int(len(c)),
            "n_tokens": int(c.sum())}


# ---------------------------------------------------------------------------
# Dictionaries
# ---------------------------------------------------------------------------
def tone(tokens, lm: dict) -> dict:
    """Shares of a document's words in the Loughran-McDonald lists (their lists are upper case)."""
    n = max(len(tokens), 1)
    up = [t.upper() for t in tokens]
    out = {}
    for cat in ("Negative", "Positive", "Uncertainty"):
        s = lm[f"_{cat}_set"] if f"_{cat}_set" in lm else set(lm[cat])
        out[cat.lower()] = sum(1 for t in up if t in s) / n
    out["net"] = out["positive"] - out["negative"]
    return out


def lm_sets(lm: dict) -> dict:
    """The dictionary with its lists as sets, for fast repeated :func:`tone` calls."""
    out = dict(lm)
    for cat in ("Negative", "Positive", "Uncertainty", "Litigious", "Constraining"):
        out[f"_{cat}_set"] = set(lm[cat])
    return out


# ---------------------------------------------------------------------------
# SESTM
# ---------------------------------------------------------------------------
def sestm_screen(D, y, alpha: float = 0.05, kappa: int = 5, z: float | None = None) -> dict:
    """Ke, Kelly and Xiu's screening step.  For each word, f_j = the share of the documents containing it whose
    outcome is positive; keep words in at least ``kappa`` documents with f_j >= pi + alpha (positive) or
    f_j <= pi - alpha (negative), where pi is the share of positive outcomes overall.  With ``z``, the threshold is
    word by word, alpha_j = z sqrt(pi (1 - pi) / k_j): a z-test of each word's share against pi."""
    D = np.asarray(D)
    has = D > 0
    k = has.sum(0)
    pos = (np.asarray(y) > 0)
    pi = float(pos.mean())
    f = np.where(k > 0, (has & pos[:, None]).sum(0) / np.maximum(k, 1), pi)
    if z is not None:
        alpha = z * np.sqrt(pi * (1 - pi) / np.maximum(k, 1))
    keep_pos = (k >= kappa) & (f >= pi + alpha)
    keep_neg = (k >= kappa) & (f <= pi - alpha)
    return {"f": f, "k": k, "pi": pi, "pos": np.flatnonzero(keep_pos), "neg": np.flatnonzero(keep_neg),
            "S": np.flatnonzero(keep_pos | keep_neg)}


def sestm_topics(D_S, y) -> dict:
    """The positive and negative topics on the screened words: regress each document's word frequencies (over the
    screened words) on [p_i, 1 - p_i], p_i the rank of its outcome scaled to (0, 1); clip at zero and normalise."""
    D_S = np.asarray(D_S, float)
    rs = D_S.sum(1)
    use = rs > 0
    h = D_S[use] / rs[use, None]
    y = np.asarray(y, float)[use]
    p = (np.argsort(np.argsort(y)) + 1) / (len(y) + 1)
    W = np.c_[p, 1 - p]
    O = np.linalg.lstsq(W, h, rcond=None)[0].T          # words x 2
    O = np.maximum(O, 0)
    O = O / np.maximum(O.sum(0, keepdims=True), 1e-12)
    return {"O_pos": O[:, 0], "O_neg": O[:, 1], "p_train": p}


def sestm_score(d_S, O_pos, O_neg, lam: float = 1.0, grid: int = 999) -> float:
    """A document's sentiment p in (0, 1): penalized maximum likelihood on the screened words' counts."""
    d = np.asarray(d_S, float)
    if d.sum() == 0:
        return 0.5
    ps = np.linspace(0.5 / grid, 1 - 0.5 / grid, grid)
    mix = np.outer(ps, O_pos) + np.outer(1 - ps, O_neg)
    ll = (np.log(np.maximum(mix, 1e-12)) * d).sum(1) / d.sum() + lam * np.log(ps * (1 - ps)) / max(d.sum(), 1)
    return float(ps[int(np.argmax(ll))])


# ---------------------------------------------------------------------------
# Meaning: embeddings and topics
# ---------------------------------------------------------------------------
def cooccurrence(token_lists, vocab, window: int = 5) -> np.ndarray:
    """Symmetric co-occurrence counts within ``window`` words, weighted 1/distance."""
    ix = {w: i for i, w in enumerate(vocab)}
    V = len(vocab)
    C = np.zeros((V, V), np.float32)
    for toks in token_lists:
        ids = [ix.get(w, -1) for w in toks]
        for a, i in enumerate(ids):
            if i < 0:
                continue
            for b in range(a + 1, min(a + 1 + window, len(ids))):
                j = ids[b]
                if j >= 0:
                    w = 1.0 / (b - a)
                    C[i, j] += w
                    C[j, i] += w
    return C


def ppmi_svd(C, dim: int = 50, alpha: float = 0.75) -> np.ndarray:
    """Word vectors: positive PMI with context smoothing (alpha), then the top ``dim`` singular vectors scaled by the
    square root of their singular values; rows unit length."""
    C = np.asarray(C, float)
    tot = C.sum()
    pw = C.sum(1) / tot
    pc = C.sum(0) ** alpha
    pc = pc / pc.sum()
    with np.errstate(divide="ignore"):
        pmi = np.log(np.maximum(C / tot, 1e-300)) - np.log(np.maximum(pw[:, None], 1e-300)) - np.log(np.maximum(pc[None, :], 1e-300))
    P = np.where(C > 0, np.maximum(pmi, 0), 0)
    U, s, _ = np.linalg.svd(P, full_matrices=False)
    E = U[:, :dim] * np.sqrt(s[:dim])
    return E / np.maximum(np.linalg.norm(E, axis=1, keepdims=True), 1e-12)


def neighbours(E, vocab, word: str, k: int = 8) -> list:
    """The ``k`` words with the largest cosine similarity to ``word``."""
    i = vocab.index(word)
    sim = E @ E[i]
    order = [j for j in np.argsort(-sim) if j != i][:k]
    return [(vocab[j], float(sim[j])) for j in order]


def nmf_topics(X, k: int = 8, iters: int = 400, seed: int = 0) -> dict:
    """X ~ W H, all non-negative (Lee and Seung's multiplicative updates on the squared error): W are the documents'
    topic weights (rows normalised to shares), H the topics' word weights."""
    X = np.asarray(X, float)
    rng = np.random.default_rng(seed)
    n, V = X.shape
    W = rng.random((n, k)) + 0.1
    H = rng.random((k, V)) + 0.1
    err = []
    for it in range(iters):
        H *= (W.T @ X) / np.maximum(W.T @ W @ H, 1e-12)
        W *= (X @ H.T) / np.maximum(W @ H @ H.T, 1e-12)
        if it % 20 == 0 or it == iters - 1:
            err.append(float(np.linalg.norm(X - W @ H) / np.linalg.norm(X)))
    share = W / np.maximum(W.sum(1, keepdims=True), 1e-12)
    return {"W": W, "H": H, "share": share, "err": err}


# ---------------------------------------------------------------------------
# Form and time
# ---------------------------------------------------------------------------
def _syllables(w: str) -> int:
    w = w.lower()
    n = len(re.findall(r"[aeiouy]+", w))
    if w.endswith("e") and not w.endswith(("le", "ee")) and n > 1:
        n -= 1
    return max(n, 1)


def fog(text: str) -> dict:
    """Gunning's fog index: 0.4 (words per sentence + 100 x share of words with three or more syllables)."""
    sents = [s for s in re.split(r"(?<=[.!?])\s+", text.strip()) if tokenize(s)]
    words = tokenize(text)
    if not sents or not words:
        return {"fog": 0.0, "words_per_sentence": 0.0, "complex": 0.0, "words": 0}
    wps = len(words) / len(sents)
    cx = sum(1 for w in words if _syllables(w) >= 3) / len(words)
    return {"fog": 0.4 * (wps + 100 * cx), "words_per_sentence": wps, "complex": cx, "words": len(words)}


def word_diff(a: str, b: str) -> list:
    """What changed from text ``a`` to text ``b``: [(op, words)], op in {"=", "-", "+"}, words as strings."""
    ta, tb = a.split(), b.split()
    out = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(a=ta, b=tb, autojunk=False).get_opcodes():
        if op == "equal":
            out.append(("=", " ".join(ta[i1:i2])))
        else:
            if i2 > i1:
                out.append(("-", " ".join(ta[i1:i2])))
            if j2 > j1:
                out.append(("+", " ".join(tb[j1:j2])))
    return out


def point_in_time_vocab(dated_token_lists, date: int, min_df: int = 2) -> list[str]:
    """The vocabulary a model trained before ``date`` could know: words in at least ``min_df`` earlier documents."""
    return vocabulary([t for d, t in dated_token_lists if d < date], min_df=min_df)


def first_use(dated_token_lists, words) -> dict:
    """The date each word first appears in the dated corpus."""
    out = {}
    for d, toks in sorted(dated_token_lists, key=lambda x: x[0]):
        s = set(toks)
        for w in words:
            if w not in out and w in s:
                out[w] = d
    return out


def chebyshev_gap(g, q, weights=None) -> float:
    """E[g q] - E[g] E[q] for two sequences (the covariance at the heart of SESTM's screening theorem)."""
    g, q = np.asarray(g, float), np.asarray(q, float)
    w = np.ones_like(g) / len(g) if weights is None else np.asarray(weights, float) / np.sum(weights)
    return float(np.sum(w * g * q) - np.sum(w * g) * np.sum(w * q))


def entropy_bits(p) -> float:
    p = np.asarray(p, float)
    p = p[p > 0]
    return float(-(p * np.log2(p)).sum())


__all__ = ["tokenize", "vocabulary", "dtm", "tfidf", "zipf", "tone", "lm_sets", "sestm_screen", "sestm_topics",
           "sestm_score", "cooccurrence", "ppmi_svd", "neighbours", "nmf_topics", "fog", "word_diff",
           "point_in_time_vocab", "first_use", "chebyshev_gap", "entropy_bits"]
