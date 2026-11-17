"""Measurement: what a number attached to a mind means, how much of it is error, and whether it measures what its
name says (*Psychology, Built*, Part 3; videos/psychology/SYLLABUS.md).

Three groups of tools, all plain numpy:

* **Scale types** (Stevens 1946).  :data:`SCALES` lists, for each type, the transformations that leave the
  scale's information unchanged and the statistics that keep their meaning under them.  :func:`recode` draws a
  permissible transformation; :func:`order_can_flip` says whether two groups' mean ratings can be put in either
  order by an increasing recoding of the rating scale (they can exactly when neither group dominates the other).
* **Classical test theory** (Spearman 1904, 1910; Cronbach 1951).  An observed score is a true score plus an
  error, ``X = T + E``.  :func:`reliability` is the variance ratio when the truth is known (as it is in the Pool);
  :func:`spearman_brown`, :func:`cronbach_alpha`, :func:`split_half`, :func:`disattenuate`, :func:`sem`,
  :func:`icc`, and :func:`cohen_kappa` are the estimators used when it is not.
* **Validity.**  :func:`mtmm` builds the multitrait-multimethod matrix of Campbell and Fiske (1959) and its three
  summaries.  :func:`one_factor` fits one common factor to a correlation matrix, and :func:`mutualism` gives the
  correlations of variables that cause one another directly, to show that the two pictures can imply the same
  matrix.  :func:`double_cancellation` is the test, on an ordering alone, that an additive scale exists (Luce and
  Tukey 1964).

Nothing here imports manim.
"""

from __future__ import annotations

import itertools
import math

import numpy as np

__all__ = ["SCALES", "recode", "order_can_flip", "flip_share", "reliability", "spearman_brown", "length_for",
           "cronbach_alpha", "split_half", "disattenuate", "sem", "icc", "cohen_kappa", "agreement", "mtmm",
           "one_factor", "mutualism", "independence", "double_cancellation"]

# scale type -> (what the numbers record, the transformations that change nothing, statistics that keep their
# meaning).  Each type also keeps the statistics of the types above it.
SCALES = {
    "nominal": ("which class", "any one-to-one relabelling", ("count", "mode")),
    "ordinal": ("which is more", "any increasing function", ("median", "percentiles")),
    "interval": ("how much more", "x' = ax + b, a > 0", ("mean", "standard deviation", "correlation")),
    "ratio": ("how many times more", "x' = ax, a > 0", ("ratio of two values", "coefficient of variation")),
}


def recode(kind: str, values, rng) -> np.ndarray:
    """A random permissible transformation of the scale values ``values`` (the distinct values a scale can
    take, in increasing order) for a scale of type ``kind``: the new value of each."""
    v = np.asarray(values, dtype=float)
    if kind == "nominal":
        return rng.permutation(v)
    if kind == "ordinal":  # any increasing spacing: random positive gaps
        return v[0] + np.concatenate([[0.0], np.cumsum(rng.exponential(1.0, len(v) - 1))])
    if kind == "interval":
        return rng.uniform(0.2, 5.0) * v + rng.uniform(-10, 10)
    if kind == "ratio":
        return rng.uniform(0.2, 5.0) * v
    raise ValueError(f"unknown scale type {kind!r}")


def order_can_flip(pa, pb) -> bool:
    """``pa`` and ``pb`` are two groups' shares of answers in each category of a rating scale, lowest category
    first.  True when some increasing recoding of the categories puts the two means in the opposite order from
    some other: that is, when the cumulative shares cross, so neither group answers higher throughout."""
    d = np.cumsum(np.asarray(pa, dtype=float) - np.asarray(pb, dtype=float))[:-1]
    return bool((d > 1e-12).any() and (d < -1e-12).any())


def flip_share(pa, pb, n: int = 5000, rng=None) -> float:
    """The share of ``n`` random increasing recodings (:func:`recode`) under which the difference between the two
    groups' means has the opposite sign from the one it has with equally spaced categories."""
    rng = rng or np.random.default_rng(0)
    pa, pb = np.asarray(pa, dtype=float), np.asarray(pb, dtype=float)
    v = np.arange(1, len(pa) + 1, dtype=float)
    base = np.sign((pa - pb) @ v)
    flips = sum(np.sign((pa - pb) @ recode("ordinal", v, rng)) == -base for _ in range(n))
    return float(flips) / n


# ---------------------------------------------------------------------------
# classical test theory
# ---------------------------------------------------------------------------
def reliability(true, observed) -> float:
    """var(T) / var(X): the share of the observed scores' variance that is true-score variance.  ``true`` must
    be on the scale of ``observed`` only up to a linear change, so the squared correlation is used."""
    return float(np.corrcoef(true, observed)[0, 1] ** 2)


def spearman_brown(r: float, k: float) -> float:
    """The reliability of a test made ``k`` times as long as one of reliability ``r`` (Spearman 1910; Brown
    1910)."""
    return k * r / (1 + (k - 1) * r)


def length_for(r: float, target: float) -> float:
    """How many times longer a test of reliability ``r`` must be made to reach ``target``."""
    return target * (1 - r) / (r * (1 - target))


def cronbach_alpha(items) -> float:
    """Coefficient alpha of an (n people) x (k items) array (Cronbach 1951): k/(k-1) (1 - sum of the item
    variances / variance of the total)."""
    x = np.asarray(items, dtype=float)
    k = x.shape[1]
    return float(k / (k - 1) * (1 - x.var(axis=0, ddof=1).sum() / x.sum(axis=1).var(ddof=1)))


def split_half(items, rng=None) -> float:
    """Split the items into two random halves, correlate the half scores, and step the correlation up to full
    length with Spearman-Brown."""
    x = np.asarray(items, dtype=float)
    order = (rng or np.random.default_rng(0)).permutation(x.shape[1])
    half = x.shape[1] // 2
    r = np.corrcoef(x[:, order[:half]].sum(axis=1), x[:, order[half:]].sum(axis=1))[0, 1]
    return float(spearman_brown(r, 2))


def disattenuate(rxy: float, rxx: float, ryy: float = 1.0) -> float:
    """Spearman's correction for attenuation (1904): the correlation between the true scores, from the observed
    correlation and the two reliabilities."""
    return rxy / math.sqrt(rxx * ryy)


def sem(sd: float, rel: float) -> float:
    """The standard error of measurement: the spread of one person's observed scores around their true score."""
    return sd * math.sqrt(1 - rel)


def icc(x1, x2) -> float:
    """The intraclass correlation of two sessions for absolute agreement, ICC(2,1) of Shrout and Fleiss (1979):
    between-person variance over between-person plus session plus error variance."""
    x = np.column_stack([x1, x2]).astype(float)
    n, k = x.shape
    grand = x.mean()
    msr = k * ((x.mean(axis=1) - grand) ** 2).sum() / (n - 1)
    msc = n * ((x.mean(axis=0) - grand) ** 2).sum() / (k - 1)
    mse = ((x - x.mean(axis=1, keepdims=True) - x.mean(axis=0, keepdims=True) + grand) ** 2).sum() / ((n - 1) * (k - 1))
    return float((msr - mse) / (msr + (k - 1) * mse + k * (msc - mse) / n))


def agreement(a, b) -> float:
    """The share of cases two raters put in the same category."""
    return float(np.mean(np.asarray(a) == np.asarray(b)))


def cohen_kappa(a, b) -> float:
    """Agreement beyond what the two raters' base rates would give by chance (Cohen 1960):
    (p_observed - p_chance) / (1 - p_chance)."""
    a, b = np.asarray(a), np.asarray(b)
    po = np.mean(a == b)
    pe = sum(np.mean(a == c) * np.mean(b == c) for c in np.union1d(a, b))
    return float((po - pe) / (1 - pe))


# ---------------------------------------------------------------------------
# validity
# ---------------------------------------------------------------------------
def mtmm(scores: dict) -> dict:
    """The multitrait-multimethod matrix (Campbell and Fiske 1959).  ``scores`` maps ``(trait, method)`` to one
    score per person.  Returns the labels, the correlation matrix ordered method by method, and the mean
    correlation of each kind: ``convergent`` (same trait, different methods: the validity diagonals),
    ``same_method`` (different traits, same method) and ``neither`` (different traits, different methods)."""
    methods = list(dict.fromkeys(m for _, m in scores))
    traits = list(dict.fromkeys(t for t, _ in scores))
    labels = [(t, m) for m in methods for t in traits]
    r = np.corrcoef([scores[key] for key in labels])
    kinds: dict = {"convergent": [], "same_method": [], "neither": []}
    for i, j in itertools.combinations(range(len(labels)), 2):
        (ti, mi), (tj, mj) = labels[i], labels[j]
        if ti == tj:
            kinds["convergent"].append(r[i, j])
        elif mi == mj:
            kinds["same_method"].append(r[i, j])
        else:
            kinds["neither"].append(r[i, j])
    out = {k: float(np.mean(np.abs(v))) for k, v in kinds.items()}
    out.update(labels=labels, traits=traits, methods=methods, r=r)
    return out


def one_factor(r, iterations: int = 200) -> dict:
    """Fit one common factor to the correlation matrix ``r`` by iterated principal axes.  Returns the loadings
    and the root-mean-square of the off-diagonal residuals (0 when one factor reproduces the matrix)."""
    r = np.asarray(r, dtype=float)
    p = r.shape[0]
    h = np.full(p, 0.5)
    for _ in range(iterations):
        reduced = r.copy()
        np.fill_diagonal(reduced, h)
        w, v = np.linalg.eigh(reduced)
        lam = v[:, -1] * math.sqrt(max(w[-1], 0.0))
        h = np.clip(lam ** 2, 0.0, 0.999)
    lam = lam * np.sign(lam.sum())
    resid = (r - np.outer(lam, lam))[~np.eye(p, dtype=bool)]
    return {"loadings": lam, "rms": float(np.sqrt(np.mean(resid ** 2)))}


def mutualism(p: int, b: float) -> np.ndarray:
    """The correlation matrix of ``p`` variables with no common cause, each of which is pushed by every other
    with weight ``b`` and by its own independent input: ``x = B x + e``, so ``cov(x) = (I - B)^-1 (I - B)^-T``."""
    if not 0 <= b * (p - 1) < 1:
        raise ValueError("the weights must leave the system stable: 0 <= b (p - 1) < 1")
    a = np.linalg.inv(np.eye(p) - b * (np.ones((p, p)) - np.eye(p)))
    cov = a @ a.T
    d = np.sqrt(np.diag(cov))
    return cov / np.outer(d, d)


def independence(table) -> bool:
    """Single cancellation: in a two-way table of an ordered outcome, the order of the rows is the same in every
    column and the order of the columns the same in every row."""
    t = np.asarray(table, dtype=float)
    rows = all((np.argsort(np.argsort(t[:, j])) == np.argsort(np.argsort(t[:, 0]))).all() for j in range(t.shape[1]))
    cols = all((np.argsort(np.argsort(t[i])) == np.argsort(np.argsort(t[0]))).all() for i in range(t.shape[0]))
    return bool(rows and cols)


def double_cancellation(table) -> bool:
    """Double cancellation (Luce and Tukey 1964) on every 3 x 3 part of the table: if cell (a2, b1) >= (a1, b2)
    and (a3, b2) >= (a2, b3) then (a3, b1) >= (a1, b3).  Together with :func:`independence` it is what an
    ordering must satisfy for the rows and columns to have values that add."""
    t = np.asarray(table, dtype=float)
    for rows in itertools.permutations(range(t.shape[0]), 3):
        for cols in itertools.permutations(range(t.shape[1]), 3):
            (a1, a2, a3), (b1, b2, b3) = rows, cols
            if t[a2, b1] >= t[a1, b2] and t[a3, b2] >= t[a2, b3] and not t[a3, b1] >= t[a1, b3]:
                return False
    return True
