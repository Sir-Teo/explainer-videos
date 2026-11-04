"""statkit.tests: the everyday significance tests, written out (Part 10 of *Statistics, Built*).

    from explainer.stats.kit.tests import t_test, welch_test, permutation_test, sign_flip_test, fisher_exact, chisq_test

Each function returns a small dict with the statistic, its null distribution's name or size, and the p-value, so a
scene can show every number.  They are checked against SciPy in ``tests/test_stats_kit_tests.py``; the point of
writing them here is that each is a few lines you can read.
"""

from __future__ import annotations

import itertools
from math import comb
from typing import Callable

import numpy as np
from scipy import stats

ALTERNATIVES = ("two-sided", "greater", "less")


def _tail(stat_obs: float, null: np.ndarray, alternative: str) -> float:
    if alternative == "greater":
        return float(np.mean(null >= stat_obs - 1e-12))
    if alternative == "less":
        return float(np.mean(null <= stat_obs + 1e-12))
    return float(np.mean(np.abs(null) >= abs(stat_obs) - 1e-12))


def _t_p(t: float, df: float, alternative: str) -> float:
    if alternative == "greater":
        return float(stats.t.sf(t, df))
    if alternative == "less":
        return float(stats.t.cdf(t, df))
    return float(2 * stats.t.sf(abs(t), df))


def z_test(x, mu0: float, sigma: float, alternative: str = "two-sided") -> dict:
    """The z-test for a mean with known sigma."""
    x = np.asarray(x, float)
    z = (x.mean() - mu0) / (sigma / np.sqrt(len(x)))
    p = {"greater": stats.norm.sf(z), "less": stats.norm.cdf(z)}.get(alternative, 2 * stats.norm.sf(abs(z)))
    return {"z": float(z), "p": float(p)}


def t_test(x, y=None, mu0: float = 0.0, paired: bool = False, alternative: str = "two-sided") -> dict:
    """Student's t: one-sample (``y`` None), paired (differences), or two-sample with a pooled variance."""
    x = np.asarray(x, float)
    if y is None or paired:
        d = x if y is None else x - np.asarray(y, float)
        n = len(d)
        se = d.std(ddof=1) / np.sqrt(n)
        t = (d.mean() - mu0) / se
        return {"t": float(t), "df": n - 1, "se": float(se), "p": _t_p(t, n - 1, alternative)}
    y = np.asarray(y, float)
    n1, n2 = len(x), len(y)
    sp2 = ((n1 - 1) * x.var(ddof=1) + (n2 - 1) * y.var(ddof=1)) / (n1 + n2 - 2)
    se = np.sqrt(sp2 * (1 / n1 + 1 / n2))
    t = (x.mean() - y.mean() - mu0) / se
    return {"t": float(t), "df": n1 + n2 - 2, "se": float(se), "p": _t_p(t, n1 + n2 - 2, alternative)}


def welch_test(x, y, alternative: str = "two-sided") -> dict:
    """Welch (1947): unpooled variances and the Welch–Satterthwaite degrees of freedom."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    a, b = x.var(ddof=1) / len(x), y.var(ddof=1) / len(y)
    se = np.sqrt(a + b)
    df = (a + b) ** 2 / (a * a / (len(x) - 1) + b * b / (len(y) - 1))
    t = (x.mean() - y.mean()) / se
    return {"t": float(t), "df": float(df), "se": float(se), "p": _t_p(t, df, alternative)}


def permutation_test(x, y, stat: Callable | None = None, reps: int | None = 10_000, seed: int = 0,
                     alternative: str = "two-sided") -> dict:
    """Shuffle the group labels.  ``reps=None`` enumerates every split (exact; only for small samples)."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    stat = stat or (lambda a, b: a.mean() - b.mean())
    pooled = np.concatenate([x, y])
    n, nx = len(pooled), len(x)
    obs = stat(x, y)
    if reps is None:
        null = []
        for idx in itertools.combinations(range(n), nx):
            mask = np.zeros(n, bool)
            mask[list(idx)] = True
            null.append(stat(pooled[mask], pooled[~mask]))
        null = np.asarray(null)
    else:
        g = np.random.Generator(np.random.PCG64(seed))
        null = np.empty(reps)
        for r in range(reps):
            p = g.permutation(pooled)
            null[r] = stat(p[:nx], p[nx:])
    return {"stat": float(obs), "null": null, "p": _tail(obs, null, alternative), "exact": reps is None}


def sign_flip_test(d, alternative: str = "two-sided") -> dict:
    """Fisher's (1935) randomization test for paired differences: every one of the 2^n sign patterns (n <= 20)."""
    d = np.asarray(d, float)
    n = len(d)
    if n > 20:
        raise ValueError("enumerating 2^n sign flips needs n <= 20")
    signs = np.array(list(itertools.product((1.0, -1.0), repeat=n)))
    null = signs @ np.abs(d)
    obs = d.sum()
    return {"stat": float(obs), "null": null, "p": _tail(obs, null, alternative),
            "count": int(np.sum(null >= obs - 1e-12)), "total": len(null)}


def sign_test(n_plus: int, n: int, alternative: str = "greater") -> dict:
    """The sign test: Arbuthnot's (1710) test, P(at least n_plus of n) under p = 1/2."""
    if alternative == "greater":
        p = sum(comb(n, k) for k in range(n_plus, n + 1)) / 2 ** n
    elif alternative == "less":
        p = sum(comb(n, k) for k in range(0, n_plus + 1)) / 2 ** n
    else:
        k = max(n_plus, n - n_plus)
        p = min(1.0, 2 * sum(comb(n, j) for j in range(k, n + 1)) / 2 ** n)
    return {"n_plus": n_plus, "n": n, "p": float(p)}


def fisher_exact(table, alternative: str = "greater") -> dict:
    """Fisher's exact test for a 2x2 table [[a, b], [c, d]]: the hypergeometric law of a given the margins.
    ``greater``: the chance of an a at least as large (the tea-tasting direction)."""
    (a, b), (c, d) = table
    r1, c1, n = a + b, a + c, a + b + c + d
    lo, hi = max(0, r1 + c1 - n), min(r1, c1)
    pmf = {k: comb(c1, k) * comb(n - c1, r1 - k) / comb(n, r1) for k in range(lo, hi + 1)}
    if alternative == "greater":
        p = sum(v for k, v in pmf.items() if k >= a)
    elif alternative == "less":
        p = sum(v for k, v in pmf.items() if k <= a)
    else:
        p = sum(v for v in pmf.values() if v <= pmf[a] * (1 + 1e-9))
    return {"a": a, "pmf": pmf, "p": float(min(1.0, p))}


def chisq_test(observed, expected=None, ddof: int = 0) -> dict:
    """Pearson's (1900) chi-squared.  1-D: goodness of fit against ``expected`` counts (or probabilities);
    2-D: independence in a contingency table.  ``ddof``: extra parameters estimated (Fisher's 1922 correction)."""
    o = np.asarray(observed, float)
    if o.ndim == 2:
        e = o.sum(1, keepdims=True) * o.sum(0, keepdims=True) / o.sum()
        df = (o.shape[0] - 1) * (o.shape[1] - 1)
    else:
        e = np.asarray(expected, float)
        if abs(e.sum() - 1) < 1e-9:
            e = e * o.sum()
        df = len(o) - 1 - ddof
    x2 = float(((o - e) ** 2 / e).sum())
    return {"chi2": x2, "df": int(df), "p": float(stats.chi2.sf(x2, df)), "expected": e}


def lrt(loglik_null: float, loglik_full: float, df: int) -> dict:
    """The likelihood ratio test with Wilks' (1938) chi-squared approximation."""
    w = 2 * (loglik_full - loglik_null)
    return {"stat": float(w), "df": df, "p": float(stats.chi2.sf(w, df))}


def bonferroni(pvalues, alpha: float = 0.05) -> np.ndarray:
    """Which hypotheses Bonferroni rejects: p <= alpha / m."""
    p = np.asarray(pvalues, float)
    return p <= alpha / len(p)


def power_z(delta: float, sigma: float, n: int, alpha: float = 0.05) -> float:
    """The power of the two-sided z-test of mu = 0 when the truth is mu = delta."""
    z = stats.norm.ppf(1 - alpha / 2)
    s = delta * np.sqrt(n) / sigma
    return float(stats.norm.sf(z - s) + stats.norm.cdf(-z - s))


def n_for_power(delta: float, sigma: float, power: float = 0.8, alpha: float = 0.05) -> int:
    """The textbook sample size: n = ((z_{1-alpha/2} + z_power) sigma / delta)^2, rounded up."""
    z = stats.norm.ppf(1 - alpha / 2) + stats.norm.ppf(power)
    return int(np.ceil((z * sigma / delta) ** 2))
