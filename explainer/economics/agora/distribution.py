"""Agora's distribution (Part 40): who gets what, and whether children escape where they started.

* **Measures** (:func:`lorenz`, :func:`gini`, :func:`atkinson`, :func:`theil`, :func:`mld`, :func:`top_share`,
  :func:`measures`): the usual indices, with weights, and standard errors by the bootstrap; :func:`ede` is
  Atkinson's equally distributed equivalent income.
* **Pareto tails** (:func:`pareto_alpha`, :func:`inverted_b`, :func:`hill`, :func:`ccdf`): the exponent from two
  top shares, from the inverted coefficient, or from a sample.
* **Random growth** (:func:`zeta`, :func:`simulate_growth`, :class:`KFE`): log income follows a random walk with
  drift ``nu`` and volatility ``sigma``; careers end at rate ``delta`` and newcomers start at ``x0``.  The stationary
  distribution has a Pareto tail with exponent ``zeta = (-nu + sqrt(nu^2 + 2 sigma^2 delta)) / sigma^2``
  (Champernowne 1953; Gabaix 2009); :class:`KFE` solves the Kolmogorov forward equation for the whole density, its
  stationary state and its transitions, with one or two types (Gabaix, Lasry, Lions and Moll 2016).
* **Wealth** (:func:`wealth_zeta`): the same law with ``nu = r - g - c``: the tail fattens as r - g rises.
* **Kuznets** (:func:`kuznets`): a dual economy whose modern sector grows; inequality first rises, then falls.
* **Generations** (:func:`generations`, :func:`ige`, :func:`rank_slope`, :func:`gatsby`): an intergenerational
  model with transitory income, so that one year of parents' income attenuates the elasticity (Solon 1992), and a
  family of economies in which a higher return to skill raises both inequality and the elasticity (the Great
  Gatsby curve's mechanism).
* **The world** (:func:`between_gini`): the population-weighted Gini of countries' mean incomes.
* **Policy** (:func:`incidence`): a distributional table, decile by decile.

numpy and scipy only.
"""

from __future__ import annotations

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import splu, spsolve

# ---------------------------------------------------------------------------------------------------------------
# measures


def _sorted(x, w=None):
    x = np.asarray(x, float)
    w = np.ones_like(x) if w is None else np.asarray(w, float)
    o = np.argsort(x, kind="stable")
    return x[o], w[o]


def lorenz(x, w=None):
    """The Lorenz curve: cumulative population shares ``p`` and income shares ``L``, both starting at 0."""
    xs, ws = _sorted(x, w)
    p = np.concatenate([[0.0], np.cumsum(ws) / ws.sum()])
    L = np.concatenate([[0.0], np.cumsum(ws * xs) / (ws * xs).sum()])
    return p, L


def gini(x, w=None) -> float:
    """The Gini index: one minus twice the area under the Lorenz curve (trapezoids, so exact for grouped data)."""
    p, L = lorenz(x, w)
    return float(1.0 - np.sum((p[1:] - p[:-1]) * (L[1:] + L[:-1])))


def atkinson(x, eps: float, w=None) -> float:
    """Atkinson's index with inequality aversion ``eps``: one minus the equally distributed equivalent over the
    mean."""
    return 1.0 - ede(x, eps, w) / np.average(np.asarray(x, float), weights=w)


def ede(x, eps: float, w=None) -> float:
    """The equally distributed equivalent income: the income that, given to everyone, is as good as the actual
    distribution under the social welfare function sum of x^(1-eps)/(1-eps) (log x when eps = 1)."""
    x = np.asarray(x, float)
    if eps == 0:
        return float(np.average(x, weights=w))
    if eps == 1:
        return float(np.exp(np.average(np.log(x), weights=w)))
    return float(np.average(x ** (1 - eps), weights=w) ** (1 / (1 - eps)))


def theil(x, w=None) -> float:
    """Theil's T index: the mean of (x/mu) log(x/mu)."""
    x = np.asarray(x, float)
    mu = np.average(x, weights=w)
    return float(np.average(x / mu * np.log(x / mu), weights=w))


def mld(x, w=None) -> float:
    """The mean log deviation (Theil's L): the mean of log(mu/x)."""
    x = np.asarray(x, float)
    mu = np.average(x, weights=w)
    return float(np.average(np.log(mu / x), weights=w))


def top_share(x, q: float, w=None) -> float:
    """The share of total income received by the richest fraction ``q`` of the population (interpolating within a
    person's weight)."""
    p, L = lorenz(x, w)
    return float(1.0 - np.interp(1.0 - q, p, L))


def measures(x, B: int = 400, seed: int = 0, w=None) -> dict:
    """The Gini, Atkinson (0.5, 1, 2), Theil, the mean log deviation and the top 10% and 1% shares, each with a
    bootstrap standard error from ``B`` resamples."""
    x = np.asarray(x, float)
    fns = {"gini": gini, "atk05": lambda v: atkinson(v, 0.5), "atk1": lambda v: atkinson(v, 1.0),
           "atk2": lambda v: atkinson(v, 2.0), "theil": theil, "mld": mld,
           "top10": lambda v: top_share(v, 0.10), "top1": lambda v: top_share(v, 0.01)}
    point = {k: f(x) for k, f in fns.items()}
    rng = np.random.default_rng(seed)
    draws = {k: [] for k in fns}
    n = len(x)
    for _ in range(B):
        v = x[rng.integers(0, n, n)]
        for k, f in fns.items():
            draws[k].append(f(v))
    return {k: {"value": point[k], "se": float(np.std(draws[k], ddof=1))} for k in fns}


# ---------------------------------------------------------------------------------------------------------------
# Pareto tails


def pareto_alpha(s_p: float, s_q: float, p: float, q: float) -> float:
    """The Pareto exponent implied by two top shares: under a Pareto tail the share of the richest fraction ``p``
    is proportional to p^(1 - 1/alpha), so s_q / s_p = (q / p)^(1 - 1/alpha)."""
    k = np.log(s_q / s_p) / np.log(q / p)
    return float(1.0 / (1.0 - k))


def inverted_b(alpha: float) -> float:
    """The inverted Pareto coefficient: the mean income above any threshold in the tail over the threshold."""
    return alpha / (alpha - 1.0)


def hill(x, k: int) -> float:
    """Hill's estimator of the tail exponent from the ``k`` largest observations."""
    xs = np.sort(np.asarray(x, float))[::-1]
    return float(1.0 / np.mean(np.log(xs[:k] / xs[k])))


def ccdf(x, points: int = 200):
    """The complementary distribution function P(X > x) at ``points`` values spaced evenly in log x, from the median
    to the largest observation but one."""
    xs = np.sort(np.asarray(x, float))
    n = len(xs)
    grid = np.exp(np.linspace(np.log(np.median(xs)), np.log(xs[-2]), points))
    surv = 1.0 - np.searchsorted(xs, grid, side="right") / n
    return grid, surv


# ---------------------------------------------------------------------------------------------------------------
# random growth


def zeta(nu: float, sigma: float, delta: float) -> float:
    """The Pareto exponent of the stationary distribution of x = exp(y), where y drifts at ``nu`` with volatility
    ``sigma``, careers end at rate ``delta`` and newcomers start below the tail: the positive root of
    (sigma^2/2) z^2 + nu z - delta = 0."""
    return float((-nu + np.sqrt(nu * nu + 2 * sigma * sigma * delta)) / (sigma * sigma))


def simulate_growth(n: int, years: int, nu: float, sigma: float, delta: float, x0: float = 1.0, seed: int = 0,
                    steps: int = 4, init=None):
    """``n`` careers simulated for ``years`` years in ``steps`` steps a year: log income gains nu dt + sigma dW, and
    with probability delta dt a career ends and a newcomer starts at log x0.  Returns the incomes at the end."""
    rng = np.random.default_rng(seed)
    dt = 1.0 / steps
    y = np.full(n, np.log(x0)) if init is None else np.log(np.asarray(init, float)).copy()
    for _ in range(years * steps):
        y += nu * dt + sigma * np.sqrt(dt) * rng.standard_normal(n)
        end = rng.random(n) < delta * dt
        y[end] = np.log(x0)
    return np.exp(y)


class KFE:
    """The Kolmogorov forward equation of random growth on a grid of log incomes, solved as a continuous-time Markov
    chain (so that probability is conserved and stays positive).

    One type: dy = nu dt + sigma dW, with careers ending at rate ``delta`` and restarting at ``y0``.  Two types
    (``nu_h``, ``psi``, ``q_h`` given): a fraction ``q_h`` of newcomers are high-growth types who drift at ``nu_h``
    and become ordinary at rate ``psi`` (Gabaix, Lasry, Lions and Moll's type dependence)."""

    def __init__(self, nu: float, sigma: float, delta: float, y0: float = 0.0, y_lo: float = -3.0,
                 y_hi: float = 16.0, n: int = 1000, nu_h: float | None = None, psi: float = 0.0, q_h: float = 0.0,
                 sigma_h: float | None = None):
        self.y = np.linspace(y_lo, y_hi, n)
        self.h = self.y[1] - self.y[0]
        self.n = n
        self.i0 = int(np.argmin(np.abs(self.y - y0)))
        self.two = nu_h is not None
        self.Q = self._generator(nu, sigma, delta, nu_h, psi, q_h, sigma_h)

    def _walk(self, nu, sigma):
        h, n = self.h, self.n
        up = np.full(n, sigma * sigma / (2 * h * h) + max(nu, 0.0) / h)
        dn = np.full(n, sigma * sigma / (2 * h * h) + max(-nu, 0.0) / h)
        up[-1] = 0.0
        dn[0] = 0.0
        rows = np.concatenate([np.arange(n - 1), np.arange(1, n)])
        cols = np.concatenate([np.arange(1, n), np.arange(n - 1)])
        vals = np.concatenate([up[:-1], dn[1:]])
        return sparse.coo_matrix((vals, (rows, cols)), shape=(n, n)).tocsr()

    def _generator(self, nu, sigma, delta, nu_h, psi, q_h, sigma_h):
        n, i0 = self.n, self.i0
        if not self.two:
            J = self._walk(nu, sigma)
            restart = sparse.coo_matrix((np.full(n, delta), (np.arange(n), np.full(n, i0))), shape=(n, n))
            Q = J + restart
        else:
            JL = self._walk(nu, sigma)
            JH = self._walk(nu_h, sigma if sigma_h is None else sigma_h)
            idx = np.arange(n)
            # ordinary careers restart as ordinary (1 - q_h) or high (q_h); high careers likewise, or turn ordinary
            rL = sparse.coo_matrix((np.concatenate([np.full(n, delta * (1 - q_h)), np.full(n, delta * q_h)]),
                                    (np.concatenate([idx, idx]), np.concatenate([np.full(n, i0),
                                                                                 np.full(n, n + i0)]))),
                                   shape=(n, 2 * n))
            rH = sparse.coo_matrix((np.concatenate([np.full(n, delta * (1 - q_h)), np.full(n, delta * q_h),
                                                    np.full(n, psi)]),
                                    (np.concatenate([idx, idx, idx]), np.concatenate([np.full(n, i0),
                                                                                      np.full(n, n + i0),
                                                                                      idx]))),
                                   shape=(n, 2 * n))
            Q = sparse.vstack([sparse.hstack([JL, sparse.csr_matrix((n, n))]) + rL,
                               sparse.hstack([sparse.csr_matrix((n, n)), JH]) + rH]).tocsr()
        Q = Q.tolil()
        Q.setdiag(0.0)
        Q = Q.tocsr()
        Q = Q - sparse.diags(np.asarray(Q.sum(axis=1)).ravel())
        return Q.tocsr()

    def stationary(self) -> np.ndarray:
        """The stationary probabilities on the grid (stacked ordinary then high, with two types)."""
        A = self.Q.T.tolil()
        m = A.shape[0]
        A[m - 1, :] = np.ones(m)
        b = np.zeros(m)
        b[-1] = 1.0
        p = spsolve(A.tocsr(), b)
        p = np.clip(p, 0.0, None)
        return p / p.sum()

    def step(self, p: np.ndarray, dt: float) -> np.ndarray:
        """One implicit Euler step of length ``dt`` (years)."""
        lu = getattr(self, "_lu", {}).get(dt)
        if lu is None:
            m = self.Q.shape[0]
            lu = splu((sparse.identity(m) - dt * self.Q.T).tocsc())
            self._lu = {**getattr(self, "_lu", {}), dt: lu}
        q = np.clip(lu.solve(p), 0.0, None)
        return q / q.sum()

    def marginal(self, p: np.ndarray) -> np.ndarray:
        """Probabilities over the grid of log incomes, summing the two types."""
        return p[: self.n] + p[self.n:] if self.two else p

    def top_share(self, p: np.ndarray, q: float) -> float:
        """The share of income of the richest fraction ``q`` under probabilities ``p``."""
        pm = self.marginal(p)
        x = np.exp(self.y)
        return top_share(x, q, w=pm)

    def path(self, p0: np.ndarray, years: float, dt: float = 0.25, qs=(0.01,)) -> dict:
        """The top shares year by year as ``p0`` evolves under this economy."""
        out = {"t": [0.0], **{q: [self.top_share(p0, q)] for q in qs}}
        p = p0
        steps = int(round(1.0 / dt))
        for t in range(1, int(years) + 1):
            for _ in range(steps):
                p = self.step(p, dt)
            out["t"].append(float(t))
            for q in qs:
                out[q].append(self.top_share(p, q))
        out["p"] = p
        return out


def half_life(t, v, end: float | None = None) -> float:
    """The time at which a path has closed half the gap between its first value and ``end`` (its new stationary
    value; by default the path's last value), interpolated."""
    t, v = np.asarray(t, float), np.asarray(v, float)
    e = v[-1] if end is None else end
    gap = (v - e) / (v[0] - e)
    k = int(np.argmax(gap <= 0.5))
    if k == 0:
        return float("nan")
    return float(t[k - 1] + (gap[k - 1] - 0.5) / (gap[k - 1] - gap[k]) * (t[k] - t[k - 1]))


def wealth_zeta(r_minus_g: float, c: float, sigma: float, delta: float) -> float:
    """The Pareto exponent of wealth when a dynasty's wealth relative to the economy grows at r - g - c with
    volatility ``sigma`` and dynasties end (or are split) at rate ``delta``."""
    return zeta(r_minus_g - c, sigma, delta)


# ---------------------------------------------------------------------------------------------------------------
# Kuznets's dual economy


def kuznets(shares, mean_gap: float = 1.0, sd_a: float = 0.4, sd_m: float = 0.7, n: int = 40000,
            seed: int = 0) -> dict:
    """A population moving from a traditional sector (log incomes normal, sd ``sd_a``) to a modern one whose log
    incomes are ``mean_gap`` higher on average and more dispersed (``sd_m``).  For each modern share: the variance
    of log income (exactly s sd_m^2 + (1 - s) sd_a^2 + s (1 - s) gap^2) and the Gini (from a fixed draw)."""
    rng = np.random.default_rng(seed)
    za, zm = rng.standard_normal(n), rng.standard_normal(n)
    var, gin, mean = [], [], []
    for s in shares:
        k = int(round(s * n))
        y = np.concatenate([sd_a * za[: n - k], mean_gap + sd_m * zm[:k]])
        x = np.exp(y)
        var.append(float(s * sd_m ** 2 + (1 - s) * sd_a ** 2 + s * (1 - s) * mean_gap ** 2))
        gin.append(gini(x))
        mean.append(float(x.mean()))
    return {"share": [float(s) for s in shares], "var_log": var, "gini": gin, "mean": mean}


# ---------------------------------------------------------------------------------------------------------------
# generations


def generations(n: int, beta: float, sd_perm: float = 0.6, sd_trans: float = 0.5, years: int = 15,
                seed: int = 0) -> dict:
    """Parents' permanent log incomes, normal with sd ``sd_perm``; children's permanent log incomes beta times their
    parents' plus luck, scaled so that their spread is the same; each year's log income is permanent income plus an
    independent transitory shock (sd ``sd_trans``).  Returns parents' and children's permanent incomes and parents'
    yearly incomes (n x years)."""
    rng = np.random.default_rng(seed)
    yp = sd_perm * rng.standard_normal(n)
    yc = beta * yp + np.sqrt(1 - beta * beta) * sd_perm * rng.standard_normal(n)
    yearly = yp[:, None] + sd_trans * rng.standard_normal((n, years))
    child_year = yc + sd_trans * rng.standard_normal(n)
    return {"parent": yp, "child": yc, "parent_years": yearly, "child_year": child_year}


def ige(child_log, parent_log) -> tuple[float, float]:
    """The intergenerational elasticity, the least-squares slope of children's log income on parents', with its
    standard error."""
    x, y = np.asarray(parent_log, float), np.asarray(child_log, float)
    xc = x - x.mean()
    b = float(np.sum(xc * (y - y.mean())) / np.sum(xc * xc))
    e = y - y.mean() - b * xc
    se = float(np.sqrt(np.sum(e * e) / (len(x) - 2) / np.sum(xc * xc)))
    return b, se


def _ranks(v):
    v = np.asarray(v, float)
    r = np.empty(len(v))
    r[np.argsort(v, kind="stable")] = (np.arange(len(v)) + 0.5) / len(v)
    return r


def rank_slope(child, parent) -> float:
    """The rank-rank slope: children's percentile rank on parents' (Chetty et al. 2014)."""
    return ige(_ranks(child), _ranks(parent))[0]


def attenuation(T: int, sd_perm: float, sd_trans: float) -> float:
    """The factor by which averaging parents' income over ``T`` years (independent shocks) shrinks the estimated
    elasticity: var(perm) / (var(perm) + var(trans) / T)."""
    return sd_perm ** 2 / (sd_perm ** 2 + sd_trans ** 2 / T)


def gatsby(returns, lam: float = 0.5, sd_h: float = 1.0, sd_u: float = 0.5, n: int = 20000, seed: int = 0) -> dict:
    """A family of economies that differ only in the return to skill ``p``: log income p h + u, where skill h is
    inherited (h_child = lam h_parent + e, stationary spread ``sd_h``) and u is uninherited luck.  For each: the Gini
    of income and the intergenerational elasticity, exactly p^2 lam sd_h^2 / (p^2 sd_h^2 + sd_u^2), and as
    estimated on a simulated population."""
    rng = np.random.default_rng(seed)
    hp = sd_h * rng.standard_normal(n)
    hc = lam * hp + np.sqrt(1 - lam * lam) * sd_h * rng.standard_normal(n)
    up, uc = sd_u * rng.standard_normal(n), sd_u * rng.standard_normal(n)
    out = {"p": [], "gini": [], "ige": [], "ige_theory": []}
    for p in returns:
        yp, yc = p * hp + up, p * hc + uc
        out["p"].append(float(p))
        out["gini"].append(gini(np.exp(yp)))
        out["ige"].append(ige(yc, yp)[0])
        out["ige_theory"].append(float(p * p * lam * sd_h ** 2 / (p * p * sd_h ** 2 + sd_u ** 2)))
    return out


# ---------------------------------------------------------------------------------------------------------------
# the world and policy


def between_gini(means, pops) -> float:
    """The population-weighted Gini of countries' mean incomes: inequality between countries, as if everyone in a
    country had its mean."""
    return gini(np.asarray(means, float), np.asarray(pops, float))


def incidence(x, tax_rate: float, transfer: float | None = None) -> dict:
    """A flat tax at ``tax_rate`` on every income, its revenue paid back as an equal transfer (or ``transfer`` per
    person): the net gain by decile of pre-tax income, in money and as a share of pre-tax income, and the Gini
    before and after."""
    x = np.asarray(x, float)
    t = tax_rate * x.mean() if transfer is None else transfer
    after = x * (1 - tax_rate) + t
    o = np.argsort(x, kind="stable")
    dec = np.array_split(o, 10)
    gain = [float(np.mean(after[d] - x[d])) for d in dec]
    rel = [float(np.mean(after[d] - x[d]) / np.mean(x[d])) for d in dec]
    return {"gain": gain, "rel": rel, "mean_pre": [float(np.mean(x[d])) for d in dec], "gini_pre": gini(x),
            "gini_post": gini(after), "transfer": float(t)}
