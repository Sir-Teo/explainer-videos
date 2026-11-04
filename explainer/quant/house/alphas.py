"""The House's alpha miners (Part 29).

**Formulas.**  An alpha is an expression tree over daily fields (``close``, ``high``, ``low``, ``volume`` (quote
volume), ``ret`` (log return), ``vwap`` (the typical price (h + l + c)/3)), built from Kakushadze's (2016) operators:
cross-sectional :func:`rank`; time-series ``ts_mean``, ``ts_std``, ``ts_rank``, ``ts_max``, ``ts_min``, ``delta``,
``delay`` over a window of 3, 5, 10 or 20 days; ``corr`` of two series over a window; and ``+ − × ÷``, ``neg``,
``abs``, ``sign``, ``slog`` (signed log).  :func:`evaluate` computes one on a (days × assets) grid; :func:`to_str`
prints it; :func:`random_tree` grows one; :func:`count_trees` counts how many exist by depth.

**Scoring.**  :func:`ic_series` is the daily cross-sectional rank correlation between an alpha and the next day's
return over the eligible assets; :func:`score` gives its mean, t-statistic and the long-short returns of its
signal (:func:`ls_returns`).

**Search.**  :func:`random_search` (the baseline), :func:`gp` (genetic programming after Koza 1992: tournament
selection, subtree crossover, point mutation, a parsimony penalty) and :class:`RLMiner` (a REINFORCE policy over
reverse-Polish tokens whose reward is the gain in the pool's combined IC: the idea of AlphaGen, Yu et al. 2023).

**Combination.**  :func:`combine` fits weights to the alphas' long-short returns (plug-in mean-variance, optionally
shrunk); :func:`sr_oos_theory` is the research chapter's formula for the out-of-sample Sharpe ratio of a combination
estimated from T observations: SR* / sqrt(1 + K / (T SR*^2)) with known covariance.
"""

from __future__ import annotations

import math

import numpy as np
from numpy.lib.stride_tricks import sliding_window_view

FIELDS = ("close", "high", "low", "volume", "ret", "vwap")
UNARY = ("neg", "abs", "sign", "slog", "rank")
TS = ("ts_mean", "ts_std", "ts_rank", "ts_max", "ts_min", "delta", "delay")
BINARY = ("add", "sub", "mul", "div")
WINDOWS = (3, 5, 10, 20)


# ---------------------------------------------------------------------------
# Operators on (days x assets) arrays, NaN-aware
# ---------------------------------------------------------------------------
def _roll(x, d):
    """Sliding windows of length d along time: (T, N, d), the first d - 1 rows NaN-padded."""
    pad = np.full((d - 1, x.shape[1]), np.nan)
    return sliding_window_view(np.vstack([pad, x]), d, axis=0)


def rank(x):
    """Each day's cross-sectional rank, scaled to [-0.5, 0.5]; NaN stays NaN."""
    out = np.full_like(x, np.nan, dtype=float)
    for t in range(x.shape[0]):
        v = x[t]
        m = np.isfinite(v)
        k = int(m.sum())
        if k > 1:
            r = np.empty(k)
            r[np.argsort(v[m], kind="stable")] = np.arange(k)
            out[t, m] = r / (k - 1) - 0.5
    return out


def _ts(op, x, d):
    with np.errstate(all="ignore"):
        if op == "delay":
            return np.vstack([np.full((d, x.shape[1]), np.nan), x[:-d]])
        if op == "delta":
            return x - np.vstack([np.full((d, x.shape[1]), np.nan), x[:-d]])
        W = _roll(x, d)
        if op == "ts_mean":
            return np.nanmean(W, axis=2)
        if op == "ts_std":
            return np.nanstd(W, axis=2)
        if op == "ts_max":
            return np.nanmax(W, axis=2)
        if op == "ts_min":
            return np.nanmin(W, axis=2)
        if op == "ts_rank":
            last = W[..., -1:]
            return (np.sum(W < last, axis=2) + 0.5 * np.sum(W == last, axis=2) - 0.5) / (d - 1) - 0.5
    raise ValueError(op)


def _corr(x, y, d):
    with np.errstate(all="ignore"):
        X, Y = _roll(x, d), _roll(y, d)
        mx, my = np.nanmean(X, axis=2, keepdims=True), np.nanmean(Y, axis=2, keepdims=True)
        cov = np.nanmean((X - mx) * (Y - my), axis=2)
        return cov / (np.nanstd(X, axis=2) * np.nanstd(Y, axis=2))


def evaluate(tree, F: dict):
    """The value of an expression tree on the fields ``F`` (each (days x assets)); infinities become NaN."""
    op = tree[0]
    with np.errstate(all="ignore"):
        if op == "field":
            out = F[tree[1]]
        elif op == "const":
            out = np.full_like(F["close"], tree[1], dtype=float)
        elif op in UNARY:
            a = evaluate(tree[1], F)
            out = {"neg": lambda v: -v, "abs": np.abs, "sign": np.sign,
                   "slog": lambda v: np.sign(v) * np.log1p(np.abs(v)), "rank": rank}[op](a)
        elif op in TS:
            out = _ts(op, evaluate(tree[1], F), tree[2])
        elif op == "corr":
            out = _corr(evaluate(tree[1], F), evaluate(tree[2], F), tree[3])
        elif op in BINARY:
            a, b = evaluate(tree[1], F), evaluate(tree[2], F)
            out = {"add": a + b, "sub": a - b, "mul": a * b, "div": a / np.where(np.abs(b) > 1e-12, b, np.nan)}[op]
        else:
            raise ValueError(op)
    out = np.asarray(out, float)
    out[~np.isfinite(out)] = np.nan
    return out


def to_str(tree) -> str:
    op = tree[0]
    if op == "field":
        return tree[1]
    if op == "const":
        return f"{tree[1]:g}"
    if op in UNARY:
        return f"{op}({to_str(tree[1])})"
    if op in TS:
        return f"{op}({to_str(tree[1])}, {tree[2]})"
    if op == "corr":
        return f"corr({to_str(tree[1])}, {to_str(tree[2])}, {tree[3]})"
    sym = {"add": "+", "sub": "-", "mul": "*", "div": "/"}[op]
    return f"({to_str(tree[1])} {sym} {to_str(tree[2])})"


def size(tree) -> int:
    return 1 + sum(size(c) for c in tree[1:] if isinstance(c, tuple))


def depth(tree) -> int:
    kids = [c for c in tree[1:] if isinstance(c, tuple)]
    return 1 + (max(depth(c) for c in kids) if kids else 0)


def random_tree(rng, max_depth: int = 4, p_leaf: float = 0.3):
    """Grow a random tree (Koza's `grow' method)."""
    if max_depth <= 1 or rng.random() < p_leaf:
        return ("field", FIELDS[rng.integers(len(FIELDS))])
    kind = rng.random()
    if kind < 0.25:
        return (UNARY[rng.integers(len(UNARY))], random_tree(rng, max_depth - 1, p_leaf))
    if kind < 0.6:
        return (TS[rng.integers(len(TS))], random_tree(rng, max_depth - 1, p_leaf), int(WINDOWS[rng.integers(4)]))
    if kind < 0.7:
        return ("corr", random_tree(rng, max_depth - 1, p_leaf), random_tree(rng, max_depth - 1, p_leaf),
                int(WINDOWS[rng.integers(4)]))
    return (BINARY[rng.integers(len(BINARY))], random_tree(rng, max_depth - 1, p_leaf),
            random_tree(rng, max_depth - 1, p_leaf))


def count_trees(max_depth: int) -> list:
    """How many distinct trees of depth at most d exist, d = 1..max_depth (exact integers)."""
    n = [0, len(FIELDS)]
    for d in range(2, max_depth + 1):
        m = n[d - 1]
        n.append(len(FIELDS) + len(UNARY) * m + len(TS) * len(WINDOWS) * m + len(WINDOWS) * m * m + len(BINARY) * m * m)
    return n[1:]


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------
def ic_series(signal, fwd, mask):
    """Daily cross-sectional Spearman correlation of ``signal`` (day t) with ``fwd`` (the return from t to t + 1),
    over the assets in ``mask`` (eligible that day); NaN when fewer than 10 assets."""
    T = signal.shape[0]
    out = np.full(T, np.nan)
    for t in range(T):
        m = mask[t] & np.isfinite(signal[t]) & np.isfinite(fwd[t])
        k = int(m.sum())
        if k < 10:
            continue
        a, b = signal[t, m], fwd[t, m]
        if np.ptp(a) == 0:
            continue
        ra = np.empty(k)
        ra[np.argsort(a, kind="stable")] = np.arange(k)
        rb = np.empty(k)
        rb[np.argsort(b, kind="stable")] = np.arange(k)
        out[t] = np.corrcoef(ra, rb)[0, 1]
    return out


def ls_returns(signal, fwd, mask):
    """The next-day return of a dollar-neutral portfolio with weights proportional to the demeaned cross-sectional rank
    of the signal, scaled to one dollar long and one short."""
    R = rank(np.where(mask, signal, np.nan))
    out = np.full(signal.shape[0], np.nan)
    for t in range(signal.shape[0]):
        m = np.isfinite(R[t]) & np.isfinite(fwd[t])
        if m.sum() < 10:
            continue
        w = R[t, m] - R[t, m].mean()
        s = np.abs(w).sum()
        if s > 0:
            out[t] = float(np.sum(w / s * 2 * fwd[t, m]))
    return out


def score(ic, idx=None) -> dict:
    """Mean IC, its t-statistic (iid days) and the number of days, over the day indices ``idx``."""
    x = ic if idx is None else ic[idx]
    x = x[np.isfinite(x)]
    if len(x) < 20:
        return {"ic": 0.0, "t": 0.0, "n": int(len(x))}
    return {"ic": float(x.mean()), "t": float(x.mean() / x.std(ddof=1) * math.sqrt(len(x))), "n": int(len(x))}


# ---------------------------------------------------------------------------
# Search
# ---------------------------------------------------------------------------
def random_search(F, fwd, mask, train, valid, n: int, rng, max_depth: int = 4):
    """Score ``n`` random trees on the train and validation days: [(train IC, valid IC, string)]."""
    out = []
    for _ in range(n):
        tr = random_tree(rng, max_depth)
        ic = ic_series(evaluate(tr, F), fwd, mask)
        out.append((score(ic, train)["ic"], score(ic, valid)["ic"], to_str(tr)))
    return out


def _subtrees(tree, path=()):
    yield path, tree
    for i, c in enumerate(tree[1:], 1):
        if isinstance(c, tuple):
            yield from _subtrees(c, path + (i,))


def _replace(tree, path, new):
    if not path:
        return new
    i = path[0]
    lst = list(tree)
    lst[i] = _replace(tree[i], path[1:], new)
    return tuple(lst)


def gp(F, fwd, mask, train, valid, rng, pop: int = 120, gens: int = 20, tourn: int = 5, p_cross: float = 0.7,
       p_mut: float = 0.2, parsimony: float = 0.0005, max_depth: int = 6, history=None):
    """Genetic programming on |train IC| - parsimony x size.  Returns per generation the best individual's train and
    validation IC, its string and size, the population's mean size, and the number of trees evaluated."""
    cache = {}

    def fit(tr):
        k = to_str(tr)
        if k not in cache:
            ic = ic_series(evaluate(tr, F), fwd, mask)
            cache[k] = (score(ic, train)["ic"], score(ic, valid)["ic"])
        a, b = cache[k]
        return abs(a) - parsimony * size(tr), a, b

    P = [random_tree(rng, 4) for _ in range(pop)]
    gens_out = []
    for g in range(gens):
        scored = [fit(t) for t in P]
        best = int(np.argmax([s[0] for s in scored]))
        gens_out.append({"gen": g, "train": scored[best][1], "valid": scored[best][2], "best": to_str(P[best]),
                         "size": size(P[best]), "mean_size": float(np.mean([size(t) for t in P])),
                         "evaluated": len(cache)})

        def pick():
            c = rng.choice(len(P), tourn, replace=False)
            return P[max(c, key=lambda i: scored[i][0])]
        nxt = [P[best]]
        while len(nxt) < pop:
            a = pick()
            r = rng.random()
            if r < p_cross:
                b = pick()
                pa, _ = list(_subtrees(a))[rng.integers(size(a))]
                _, sb = list(_subtrees(b))[rng.integers(size(b))]
                child = _replace(a, pa, sb)
            elif r < p_cross + p_mut:
                pa, _ = list(_subtrees(a))[rng.integers(size(a))]
                child = _replace(a, pa, random_tree(rng, 3))
            else:
                child = a
            nxt.append(child if depth(child) <= max_depth else a)
        P = nxt
    return gens_out


# ---------------------------------------------------------------------------
# Combination and its estimation risk
# ---------------------------------------------------------------------------
def combine(R, shrink: float = 0.0):
    """Mean-variance weights for the columns of ``R`` (T x K returns): w ∝ (Σ̂ + shrink·tr(Σ̂)/K·I)⁻¹ μ̂."""
    R = np.asarray(R, float)
    mu = np.nanmean(R, axis=0)
    S = np.cov(np.nan_to_num(R - mu), rowvar=False)
    S = np.atleast_2d(S)
    K = S.shape[0]
    S = S + shrink * np.trace(S) / K * np.eye(K)
    w = np.linalg.solve(S, mu)
    return w / np.sum(np.abs(w))


def sharpe(r, periods: int = 365) -> float:
    r = np.asarray(r, float)
    r = r[np.isfinite(r)]
    return float(r.mean() / r.std(ddof=1) * math.sqrt(periods)) if len(r) > 2 and r.std() > 0 else 0.0


def sr_oos_theory(sr_star: float, K: int, T: int) -> float:
    """The research chapter's approximation for the (per-period) out-of-sample Sharpe ratio of plug-in weights
    Σ⁻¹μ̂ estimated from T observations of K returns with known Σ: SR* / sqrt(1 + K / (T SR*²))."""
    return sr_star / math.sqrt(1.0 + K / (T * sr_star ** 2)) if sr_star > 0 else 0.0


def sr_oos_sim(theta, T: int, reps: int, rng, known_cov: bool = True) -> np.ndarray:
    """Simulated out-of-sample Sharpe ratios (per period) of plug-in weights for K independent unit-variance returns
    with means ``theta``: known covariance (w = μ̂) or estimated (w = Σ̂⁻¹μ̂)."""
    theta = np.asarray(theta, float)
    K = len(theta)
    out = np.empty(reps)
    for r in range(reps):
        X = theta + rng.standard_normal((T, K))
        mu = X.mean(0)
        w = mu if known_cov else np.linalg.solve(np.atleast_2d(np.cov(X, rowvar=False)), mu)
        out[r] = float(w @ theta / np.linalg.norm(w))
    return out


__all__ = ["FIELDS", "UNARY", "TS", "BINARY", "WINDOWS", "rank", "evaluate", "to_str", "size", "depth", "random_tree",
           "count_trees", "ic_series", "ls_returns", "score", "random_search", "gp", "combine", "sharpe",
           "sr_oos_theory", "sr_oos_sim"]
