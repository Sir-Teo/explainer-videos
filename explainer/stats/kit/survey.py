"""statkit.survey: design-based estimation for Part 18 of *Statistics, Built* ("Who Did You Ask?").

Simple random sampling with the finite-population correction, stratification with proportional and Neyman
allocation, cluster samples and Kish's design effect, Hansen–Hurwitz and Horvitz–Thompson estimators, ratio and
regression estimators, post-stratification and raking, Kish's effective sample size, and Meng's (2018) identity for
the error of any sample.  Checked in ``tests/test_stats_kit_survey.py``.
"""

from __future__ import annotations

import numpy as np
from scipy import stats


# ---------------------------------------------------------------------------------------------------------------------
# Simple random sampling
# ---------------------------------------------------------------------------------------------------------------------
def srs_mean(y, N: int | None = None, level: float = 0.95) -> dict:
    """Mean of a simple random sample without replacement, with SE sqrt((1 - n/N) s^2 / n) (the fpc; N=None: none)."""
    y = np.asarray(y, float)
    n = len(y)
    fpc = 1.0 if N is None else 1 - n / N
    se = float(np.sqrt(fpc * y.var(ddof=1) / n))
    z = stats.norm.ppf(0.5 + level / 2)
    m = float(y.mean())
    return {"mean": m, "se": se, "fpc": fpc, "ci": (m - z * se, m + z * se)}


# ---------------------------------------------------------------------------------------------------------------------
# Stratification
# ---------------------------------------------------------------------------------------------------------------------
def proportional_allocation(N_h, n: int) -> np.ndarray:
    N_h = np.asarray(N_h, float)
    return n * N_h / N_h.sum()


def neyman_allocation(N_h, S_h, n: int) -> np.ndarray:
    """Neyman (1934): n_h proportional to N_h S_h, which minimizes the variance of the stratified mean for fixed n."""
    w = np.asarray(N_h, float) * np.asarray(S_h, float)
    return n * w / w.sum()


def stratified_variance(N_h, S_h, n_h) -> float:
    """Var of the stratified mean, sum_h W_h^2 (1 - n_h/N_h) S_h^2 / n_h, W_h = N_h / N."""
    N_h, S_h, n_h = (np.asarray(a, float) for a in (N_h, S_h, n_h))
    W = N_h / N_h.sum()
    return float(np.sum(W ** 2 * (1 - n_h / N_h) * S_h ** 2 / n_h))


def stratified_mean(y, stratum, N_h: dict) -> dict:
    """The stratified estimate sum_h W_h ybar_h and its SE, from a sample with stratum labels."""
    y, stratum = np.asarray(y, float), np.asarray(stratum)
    keys = sorted(N_h)
    N = sum(N_h.values())
    est = var = 0.0
    for h in keys:
        yh = y[stratum == h]
        W = N_h[h] / N
        est += W * yh.mean()
        var += W ** 2 * (1 - len(yh) / N_h[h]) * yh.var(ddof=1) / len(yh)
    return {"mean": float(est), "se": float(np.sqrt(var))}


# ---------------------------------------------------------------------------------------------------------------------
# Clusters
# ---------------------------------------------------------------------------------------------------------------------
def icc(y, cluster) -> float:
    """The intraclass correlation by one-way ANOVA (equal or unequal clusters)."""
    y, cluster = np.asarray(y, float), np.asarray(cluster)
    labs = np.unique(cluster)
    k = len(labs)
    n = len(y)
    sizes = np.array([np.sum(cluster == c) for c in labs])
    means = np.array([y[cluster == c].mean() for c in labs])
    msb = np.sum(sizes * (means - y.mean()) ** 2) / (k - 1)
    msw = np.sum([np.sum((y[cluster == c] - m) ** 2) for c, m in zip(labs, means)]) / (n - k)
    m0 = (n - np.sum(sizes ** 2) / n) / (k - 1)
    return float((msb - msw) / (msb + (m0 - 1) * msw))


def design_effect(m: float, rho: float) -> float:
    """Kish (1965): the variance of a cluster sample with m per cluster relative to an SRS, 1 + (m - 1) rho."""
    return 1 + (m - 1) * rho


def kish_neff(w) -> float:
    """Kish's effective sample size of a weighted sample: (sum w)^2 / sum w^2."""
    w = np.asarray(w, float)
    return float(w.sum() ** 2 / np.sum(w ** 2))


# ---------------------------------------------------------------------------------------------------------------------
# Unequal probabilities
# ---------------------------------------------------------------------------------------------------------------------
def hansen_hurwitz(y, p) -> dict:
    """Hansen & Hurwitz (1943): with-replacement draws with probabilities p_i; the total is the mean of y_i / p_i."""
    z = np.asarray(y, float) / np.asarray(p, float)
    n = len(z)
    return {"total": float(z.mean()), "se": float(z.std(ddof=1) / np.sqrt(n))}


def horvitz_thompson(y, pi) -> float:
    """Horvitz & Thompson (1952): the total sum y_i / pi_i, unbiased for any design with inclusion probabilities pi_i."""
    return float(np.sum(np.asarray(y, float) / np.asarray(pi, float)))


def poisson_sample(pi, rng: np.random.Generator) -> np.ndarray:
    """Poisson sampling: include unit i independently with probability pi_i."""
    return np.flatnonzero(rng.random(len(pi)) < np.asarray(pi, float))


# ---------------------------------------------------------------------------------------------------------------------
# Auxiliary information
# ---------------------------------------------------------------------------------------------------------------------
def ratio_mean(y, x, xbar_pop: float, N: int | None = None) -> dict:
    """The ratio estimator (ybar / xbar) * Xbar, with its linearized SE."""
    y, x = np.asarray(y, float), np.asarray(x, float)
    n = len(y)
    R = y.mean() / x.mean()
    e = y - R * x
    fpc = 1.0 if N is None else 1 - n / N
    return {"mean": float(R * xbar_pop), "ratio": float(R), "se": float(np.sqrt(fpc * e.var(ddof=1) / n) * xbar_pop / x.mean())}


def regression_mean(y, x, xbar_pop: float, N: int | None = None) -> dict:
    """The regression estimator ybar + b (Xbar - xbar), b the sample slope, with its residual-based SE."""
    y, x = np.asarray(y, float), np.asarray(x, float)
    n = len(y)
    b = np.cov(x, y, ddof=1)[0, 1] / x.var(ddof=1)
    e = y - y.mean() - b * (x - x.mean())
    fpc = 1.0 if N is None else 1 - n / N
    return {"mean": float(y.mean() + b * (xbar_pop - x.mean())), "slope": float(b),
            "se": float(np.sqrt(fpc * np.sum(e ** 2) / (n - 2) / n))}


# ---------------------------------------------------------------------------------------------------------------------
# Weighting
# ---------------------------------------------------------------------------------------------------------------------
def poststratify(groups, pop_share: dict) -> np.ndarray:
    """Weights making each group's weighted share in the sample equal its population share."""
    groups = np.asarray(groups)
    n = len(groups)
    w = np.empty(n)
    for g, share in pop_share.items():
        k = groups == g
        w[k] = share * n / k.sum()
    return w


def rake(margins: list, targets: list, w0=None, iters: int = 50, tol: float = 1e-10) -> tuple[np.ndarray, list]:
    """Raking (Deming & Stephan 1940): iterative proportional fitting of weights to several marginal shares.
    ``margins``: arrays of category labels, one per variable; ``targets``: dicts label -> population share.
    Returns the weights (mean 1) and the history of the largest marginal discrepancy after each pass."""
    n = len(margins[0])
    w = np.ones(n) if w0 is None else np.asarray(w0, float).copy()
    hist = []
    for _ in range(iters):
        for lab, tgt in zip(margins, targets):
            lab = np.asarray(lab)
            tot = w.sum()
            for c, share in tgt.items():
                k = lab == c
                w[k] *= share * tot / w[k].sum()
        tot = w.sum()
        gap = max(abs(w[np.asarray(lab) == c].sum() / tot - share) for lab, tgt in zip(margins, targets)
                  for c, share in tgt.items())
        hist.append(float(gap))
        if gap < tol:
            break
    return w / w.mean(), hist


def weighted_mean(y, w) -> float:
    y, w = np.asarray(y, float), np.asarray(w, float)
    return float(np.sum(w * y) / np.sum(w))


# ---------------------------------------------------------------------------------------------------------------------
# Meng's identity
# ---------------------------------------------------------------------------------------------------------------------
def meng(y_pop, R) -> dict:
    """Meng (2018): for any subset R of a finite population, ybar_R - ybar_N = rho(R, Y) * sqrt((1 - f)/f) * sigma_Y,
    with f = n/N, rho the population correlation of the inclusion indicator with Y, and sigma_Y the population SD
    (divisor N).  Also the effective SRS size n_eff = f/(1 - f) / rho^2 (about f / rho^2 for small f): the m at which
    sigma^2/m equals this one subset's realized squared error.  It uses the realized rho, not Meng's E[rho^2] over
    the inclusion mechanism, and ignores the SRS's fpc, so it is infinite when rho = 0 (no error) and a random sample
    of size n gives a value scattered around n, not n itself."""
    y = np.asarray(y_pop, float)
    R = np.asarray(R, bool)
    N, n = len(y), int(R.sum())
    f = n / N
    sig = y.std()
    rho = float(np.corrcoef(R.astype(float), y)[0, 1])
    err = float(y[R].mean() - y.mean())
    pred = rho * np.sqrt((1 - f) / f) * sig
    neff = f / (1 - f) / rho ** 2 if rho != 0 else np.inf
    return {"error": err, "identity": float(pred), "rho": rho, "f": f, "sigma": float(sig), "n": n, "N": N,
            "n_eff": float(neff)}


# ---------------------------------------------------------------------------------------------------------------------
# Complex designs: Taylor linearization and the PSU bootstrap (Part 20)
# ---------------------------------------------------------------------------------------------------------------------
def _psu_totals_var(z, strata, psu) -> np.ndarray:
    """With-replacement variance of the total of the rows of ``z`` (n x k), PSUs nested in strata:
    sum_h n_h/(n_h - 1) sum_i (z_hi - zbar_h)(z_hi - zbar_h)', z_hi the PSU totals.  Strata with a single PSU are
    skipped (they contribute nothing estimable)."""
    z = np.atleast_2d(np.asarray(z, float).T).T
    strata, psu = np.asarray(strata), np.asarray(psu)
    k = z.shape[1]
    V = np.zeros((k, k))
    for h in np.unique(strata):
        m = strata == h
        ids = np.unique(psu[m])
        if len(ids) < 2:
            continue
        tot = np.array([z[m & (psu == i)].sum(0) for i in ids])
        d = tot - tot.mean(0)
        V += len(ids) / (len(ids) - 1) * d.T @ d
    return V


def svy_mean(y, w, strata, psu) -> dict:
    """The weighted (Hajek) mean with its linearized design-based SE; ``deff`` against an SRS of the same size."""
    y, w = np.asarray(y, float), np.asarray(w, float)
    W = w.sum()
    m = float(np.sum(w * y) / W)
    v = float(_psu_totals_var(w * (y - m) / W, strata, psu)[0, 0])
    srs = float(np.sum(w * (y - m) ** 2) / W / len(y))
    return {"mean": m, "se": float(np.sqrt(v)), "deff": v / srs if srs > 0 else np.nan}


def svy_ols(X, y, w, strata, psu) -> dict:
    """Weighted least squares with three SEs: ``se_model`` (WLS as if the weights were precisions), ``se_hc`` (HC0
    sandwich, independent units) and ``se_design`` (Taylor linearization over strata and PSUs, as in R's survey or
    SUDAAN).  ``X`` should include the intercept column."""
    X, y, w = np.asarray(X, float), np.asarray(y, float), np.asarray(w, float)
    XtWX = X.T @ (w[:, None] * X)
    A = np.linalg.inv(XtWX)
    b = A @ (X.T @ (w * y))
    e = y - X @ b
    n, p = X.shape
    wn = w / w.mean()  # weights rescaled to mean 1, read as precisions
    s2 = float(np.sum(wn * e ** 2) / (n - p))
    v_model = s2 * np.linalg.inv(X.T @ (wn[:, None] * X))
    U = X * (w * e)[:, None]  # score contributions
    v_hc = A @ (U.T @ U) @ A
    v_des = A @ _psu_totals_var(U, strata, psu) @ A
    return {"b": b, "resid": e, "se_model": np.sqrt(np.diag(v_model)), "se_hc": np.sqrt(np.diag(v_hc)),
            "se_design": np.sqrt(np.diag(v_des)), "cov_design": v_des}


def psu_bootstrap_weights(w, strata, psu, B: int, rng: np.random.Generator) -> np.ndarray:
    """Rao & Wu's (1988) rescaling bootstrap: in each stratum with n_h PSUs, draw n_h - 1 PSUs with replacement and
    multiply each unit's weight by n_h/(n_h - 1) times its PSU's count.  Returns B x n replicate weights; the SD of
    any estimate across them is its bootstrap SE."""
    w, strata, psu = np.asarray(w, float), np.asarray(strata), np.asarray(psu)
    out = np.empty((B, len(w)))
    groups = []
    for h in np.unique(strata):
        m = strata == h
        ids = np.unique(psu[m])
        groups.append((ids, [np.flatnonzero(m & (psu == i)) for i in ids]))
    for b in range(B):
        f = np.ones(len(w))
        for ids, members in groups:
            nh = len(ids)
            if nh < 2:
                continue
            cnt = np.bincount(rng.integers(0, nh, nh - 1), minlength=nh)
            for c, idx in zip(cnt, members):
                f[idx] = nh / (nh - 1) * c
        out[b] = w * f
    return out
