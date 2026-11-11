"""Can you beat the market? (Part 43): Sharpe's arithmetic, luck against skill, scale, and adaptive efficiency.

* :func:`beat_prob` — the chance that a zero-skill active manager with costs beats the index over T years;
* :func:`fund_population` — a population of funds with zero, negative and positive true alphas, observed with noise;
* :func:`storey_pi0`, :func:`bsw` — Storey's estimator of the share of true nulls, and Barras, Scaillet and Wermers'
  estimates of the skilled and unskilled shares, from p-values;
* :func:`berk_green` — Berk and Green's market for skill: flows chase estimated skill until net alpha is zero, with
  decreasing returns to scale;
* :func:`rolling_autocorr`, :func:`variance_ratio` — Lo's adaptive markets, measured: how efficiency moves over time.
"""

from __future__ import annotations

import math

import numpy as np
from scipy import stats


def beat_prob(cost: float, te: float, years: float) -> float:
    """P(active beats the index over ``years``) for a manager with zero skill, annual cost ``cost`` and tracking
    error ``te``: the active return over T years is N(-cost T, te^2 T), so the chance is Phi(-cost sqrt(T) / te)."""
    return float(stats.norm.cdf(-cost * math.sqrt(years) / te))


def fund_population(m: int = 2000, shares=(0.75, 0.24, 0.01), alphas=(0.0, -0.032, 0.038), te: float = 0.05,
                    months: int = 240, seed: int = 0) -> dict:
    """``m`` funds; a share ``shares[0]`` with alpha 0, ``shares[1]`` with alpha ``alphas[1]`` and ``shares[2]`` with
    ``alphas[2]`` (annual). Each fund's monthly alpha is observed with residual volatility ``te`` (annual) for
    ``months`` months. Returns the true group, the estimated alphas, their t-statistics and two-sided p-values."""
    rng = np.random.default_rng(seed)
    g = rng.choice(3, size=m, p=list(shares))
    a = np.asarray(alphas)[g]
    s = te / math.sqrt(12)
    r = a[:, None] / 12 + s * rng.standard_normal((m, months))
    ah = r.mean(1)
    se = r.std(1, ddof=1) / math.sqrt(months)
    t = ah / se
    p = 2 * stats.t.sf(np.abs(t), months - 1)
    return {"group": g, "alpha": ah * 12, "t": t, "p": p, "true_alpha": a}


def storey_pi0(p, lam: float = 0.5) -> float:
    """Storey (2002): the share of true nulls, from the p-values above ``lam``, which are mostly nulls:
    pi0_hat = #{p > lam} / (m (1 - lam)). Uncapped, E[pi0_hat] >= pi0 with or without independence (linearity of
    expectation): the alternatives only add to the count. The cap at 1 is the usual practical guard."""
    p = np.asarray(p, float)
    return float(min(1.0, np.mean(p > lam) / (1 - lam)))


def bsw(p, t, gamma: float = 0.2, lam: float = 0.5) -> dict:
    """Barras, Scaillet and Wermers (2010): of the funds significant at level ``gamma`` in each tail, the expected
    number of lucky nulls is pi0 m gamma / 2; the rest are estimated to be truly skilled (right tail) or unskilled
    (left tail)."""
    p = np.asarray(p, float)
    t = np.asarray(t, float)
    pi0 = storey_pi0(p, lam)
    right = float(np.mean((p < gamma) & (t > 0)))
    left = float(np.mean((p < gamma) & (t < 0)))
    luck = pi0 * gamma / 2
    return {"pi0": pi0, "plus": max(0.0, right - luck), "minus": max(0.0, left - luck), "right": right, "left": left,
            "luck": luck}


def berk_green(skill, fee: float = 0.01, b: float = 0.002, prior_sd: float = 0.03, te: float = 0.05, years: int = 20,
               seed: int = 0) -> dict:
    """Berk and Green (2004), simulated. A manager with true gross alpha ``skill`` on the first dollar loses ``b`` per
    unit of assets (decreasing returns to scale): gross alpha a - b A. Investors know the prior N(0, prior_sd^2) on a
    and learn from realised returns by Bayes' rule; each year they move assets until the expected net alpha
    E[a] - b A - fee is zero. Returns, for each manager, the yearly assets, net alphas to investors and value added
    (gross alpha times assets)."""
    rng = np.random.default_rng(seed)
    skill = np.asarray(skill, float)
    n = len(skill)
    mean = np.zeros(n)
    var = np.full(n, prior_sd ** 2)
    A = np.zeros((years, n))
    net = np.zeros((years, n))
    va = np.zeros((years, n))
    for y in range(years):
        size = np.maximum(0.0, (mean - fee) / b)
        gross = skill - b * size
        realised = gross + te * rng.standard_normal(n)
        A[y], net[y], va[y] = size, realised - fee, gross * size
        # the investor sees realised - (- b size) = skill + noise
        obs = realised + b * size
        k = var / (var + te ** 2)
        mean = mean + k * (obs - mean)
        var = (1 - k) * var
    return {"assets": A, "net": net, "value_added": va}


def rolling_autocorr(r, window: int) -> np.ndarray:
    """First-order autocorrelation of ``r`` in trailing windows of ``window`` observations."""
    r = np.asarray(r, float)
    out = np.full(len(r), np.nan)
    for i in range(window, len(r) + 1):
        x = r[i - window:i]
        x = x - x.mean()
        out[i - 1] = float(np.dot(x[:-1], x[1:]) / np.dot(x, x))
    return out


def variance_ratio(r, q: int) -> float:
    """Lo and MacKinlay's variance ratio: Var(q-period sum) / (q Var(one period)); 1 for a random walk."""
    r = np.asarray(r, float)
    r = r - r.mean()
    s = np.convolve(r, np.ones(q), "valid")
    return float(s.var() / (q * r.var()))
