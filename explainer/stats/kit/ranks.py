"""statkit.ranks: tests that need no distribution (Part 16 of *Statistics, Built*).

Exact null distributions are computed by generating functions (dynamic programming over ranks), not by sampling;
everything is checked against SciPy in ``tests/test_stats_kit_ranks.py``.
"""

from __future__ import annotations

import numpy as np
from scipy import stats


def signed_rank_null(n: int) -> np.ndarray:
    """P(W+ = w), w = 0 .. n(n+1)/2: the coefficients of prod_k (1 + x^k)/2 (each rank's sign a fair coin)."""
    c = np.zeros(n * (n + 1) // 2 + 1)
    c[0] = 1.0
    for k in range(1, n + 1):
        c[k:] = c[k:] + c[:-k].copy()
    return c / 2 ** n


def wilcoxon_signed_rank(d, alternative: str = "two-sided") -> dict:
    """Wilcoxon (1945): rank |d|, sum the ranks of the positive differences; exact p from the generating function
    (no ties or zeros assumed)."""
    d = np.asarray(d, float)
    d = d[d != 0]
    n = len(d)
    r = stats.rankdata(np.abs(d))
    w = float(r[d > 0].sum())
    pmf = signed_rank_null(n)
    cdf = np.cumsum(pmf)
    wi = int(round(w))
    lo = cdf[wi]
    hi = 1 - (cdf[wi - 1] if wi > 0 else 0.0)
    p = {"greater": hi, "less": lo, "two-sided": min(1.0, 2 * min(lo, hi))}[alternative]
    return {"W": w, "n": n, "p": float(p), "pmf": pmf, "mean": n * (n + 1) / 4}


def mann_whitney_null(m: int, n: int) -> np.ndarray:
    """P(U = u), u = 0 .. mn, for samples of sizes m and n with no ties: counts of lattice paths (DP)."""
    # f[i][j][u] via the recursion f(m, n, u) = f(m - 1, n, u - n) + f(m, n - 1, u)
    table = {(0, j): np.array([1.0]) for j in range(n + 1)}
    for i in range(1, m + 1):
        table[(i, 0)] = np.array([1.0])
        for j in range(1, n + 1):
            a = np.zeros(i * j + 1)
            prev = table[(i - 1, j)]
            a[j: j + len(prev)] += prev
            b = table[(i, j - 1)]
            a[: len(b)] += b
            table[(i, j)] = a
    c = table[(m, n)]
    return c / c.sum()


def mann_whitney(x, y, alternative: str = "two-sided") -> dict:
    """U = #{(i, j): x_i > y_j} (+ half for ties); U/(mn) estimates P(X > Y), the AUC.  Exact p without ties."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    m, n = len(x), len(y)
    u = float(np.sum(x[:, None] > y[None, :]) + 0.5 * np.sum(x[:, None] == y[None, :]))
    pmf = mann_whitney_null(m, n)
    cdf = np.cumsum(pmf)
    ui = int(round(u))
    lo = cdf[ui]
    hi = 1 - (cdf[ui - 1] if ui > 0 else 0.0)
    p = {"greater": hi, "less": lo, "two-sided": min(1.0, 2 * min(lo, hi))}[alternative]
    return {"U": u, "auc": u / (m * n), "p": float(p), "pmf": pmf}


def kruskal_wallis(*groups) -> dict:
    """H = 12/(N(N+1)) sum n_k (Rbar_k - (N+1)/2)^2, chi^2_{k-1} approximately (no tie correction)."""
    allv = np.concatenate([np.asarray(g, float) for g in groups])
    r = stats.rankdata(allv)
    N = len(allv)
    h, i = 0.0, 0
    for g in groups:
        k = len(g)
        h += k * (r[i: i + k].mean() - (N + 1) / 2) ** 2
        i += k
    h *= 12 / (N * (N + 1))
    return {"H": float(h), "p": float(stats.chi2.sf(h, len(groups) - 1))}


def spearman(x, y) -> float:
    return float(np.corrcoef(stats.rankdata(x), stats.rankdata(y))[0, 1])


def kendall(x, y) -> float:
    """Kendall's tau-a: (concordant - discordant) / (n choose 2)."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    s = np.sign(x[:, None] - x[None, :]) * np.sign(y[:, None] - y[None, :])
    n = len(x)
    return float(s[np.triu_indices(n, 1)].sum() / (n * (n - 1) / 2))
