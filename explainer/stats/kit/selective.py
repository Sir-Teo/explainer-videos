"""statkit.selective: inference after selection (Part 56 of *Statistics, Built*).

    truncated-normal pivots and their inversion          (the workhorse of conditional inference)
    the polyhedral lemma                                  (Lee, Sun, Sun & Taylor 2016)
    the lasso's selection event at a fixed lambda         (Lee et al. 2016)
    inference on winners: conditional and hybrid          (Andrews, Kitagawa & McCloskey 2024)
    the PoSI constant over all submodels                  (Berk, Brown, Buja, Zhang & Zhao 2013)
    randomized selection (carving) for a threshold rule   (Tian & Taylor 2018)
    data fission and Poisson thinning                     (Leiner, Duan, Wasserman & Ramdas 2023; Neufeld et al. 2024)
    conformal selection with BH                           (Jin & Candes 2023)
    post-clustering inference in one dimension            (Gao, Bien & Witten 2024; Chen & Witten 2023)
"""

from __future__ import annotations

import math

import numpy as np
from scipy import optimize, special, stats

# --------------------------------------------------------------------------------------- truncated normals


def _log_mass(a: float, b: float) -> float:
    """log(Phi(b) - Phi(a)) for a < b, stable in both tails."""
    if a > 0:  # use the upper tail
        return _log_mass(-b, -a)
    lb, la = special.log_ndtr(b), special.log_ndtr(a)
    return float(lb + np.log1p(-np.exp(min(la - lb, 0.0))))


def truncnorm_sf(y: float, mu: float, sigma: float, a: float, b: float) -> float:
    """P(Y > y) for Y ~ N(mu, sigma^2) truncated to [a, b]: the selective pivot (1 minus the CDF)."""
    za, zb, zy = (a - mu) / sigma, (b - mu) / sigma, (y - mu) / sigma
    zy = min(max(zy, za), zb)
    if zy >= zb:
        return 0.0
    if zy <= za:
        return 1.0
    return float(np.exp(_log_mass(zy, zb) - _log_mass(za, zb)))


def _solve_increasing(f, centre: float, scale: float, limit: float = 1e5):
    """The root of an increasing function f, searching outward from centre in doubling steps up to limit * scale;
    -inf or inf if f has one sign on the whole range (a conditional interval can be unbounded)."""
    w = scale
    lo, hi = centre - w, centre + w
    while f(lo) > 0 and w < limit * scale:
        w *= 2
        lo = centre - w
    if f(lo) > 0:
        return -np.inf
    w = scale
    while f(hi) < 0 and w < limit * scale:
        w *= 2
        hi = centre + w
    if f(hi) < 0:
        return np.inf
    return optimize.brentq(f, lo, hi, xtol=1e-9 * scale)


def truncnorm_interval(y: float, sigma: float, a: float, b: float, alpha: float = 0.05) -> tuple:
    """Invert the pivot: the set of mu with alpha/2 <= P_mu(Y > y | Y in [a, b]) <= 1 - alpha/2.  The survival
    function is increasing in mu, so the endpoints solve sf = alpha/2 and sf = 1 - alpha/2.  When y is close to a
    truncation point the interval is very long on that side (Kivaranovic & Leeb 2021)."""

    def root(level):
        return _solve_increasing(lambda m: truncnorm_sf(y, m, sigma, a, b) - level, y, sigma)

    return root(alpha / 2), root(1 - alpha / 2)


def truncnorm_pvalue(y: float, mu0: float, sigma: float, a: float, b: float, two_sided: bool = True) -> float:
    s = truncnorm_sf(y, mu0, sigma, a, b)
    return float(min(1.0, 2 * min(s, 1 - s))) if two_sided else s


# ------------------------------------------------------------------------------------- the polyhedral lemma


def polyhedral_limits(A, b, y, eta, Sigma=None) -> dict:
    """For Y ~ N(mu, Sigma) and the event {A Y <= b}: with c = Sigma eta / (eta' Sigma eta) and z = y - c eta'y, the
    event equals {V- <= eta'Y <= V+} with (V-, V+) functions of z only, so eta'Y given the event and z is a normal
    truncated to [V-, V+] (Lee et al. 2016, Lemma 5.1)."""
    A, b, y, eta = (np.asarray(v, float) for v in (A, b, y, eta))
    n = len(y)
    Sigma = np.eye(n) if Sigma is None else np.asarray(Sigma, float)
    s2 = float(eta @ Sigma @ eta)
    c = Sigma @ eta / s2
    t = float(eta @ y)
    z = y - c * t
    Ac, Az = A @ c, A @ z
    neg, pos = Ac < -1e-12, Ac > 1e-12
    vm = float(np.max((b[neg] - Az[neg]) / Ac[neg])) if neg.any() else -np.inf
    vp = float(np.min((b[pos] - Az[pos]) / Ac[pos])) if pos.any() else np.inf
    return {"stat": t, "sd": math.sqrt(s2), "lo": vm, "hi": vp}


# ------------------------------------------------------------------------------------------------ the lasso


def lasso(X, y, lam: float, iters: int = 2000, tol: float = 1e-10) -> np.ndarray:
    """(1/2)||y - X b||^2 + lam ||b||_1 (Lee et al.'s scaling) by coordinate descent."""
    X, y = np.asarray(X, float), np.asarray(y, float)
    p = X.shape[1]
    b = np.zeros(p)
    r = y.copy()
    cn = (X ** 2).sum(axis=0)
    for _ in range(iters):
        mx = 0.0
        for j in range(p):
            old = b[j]
            z = X[:, j] @ r + cn[j] * old
            new = np.sign(z) * max(abs(z) - lam, 0.0) / cn[j]
            if new != old:
                r -= X[:, j] * (new - old)
                b[j] = new
                mx = max(mx, abs(new - old))
        if mx < tol:
            break
    return b


def lasso_event(X, y, lam: float) -> dict:
    """The lasso's active set E and signs s at lam, with the polyhedron {A y <= b} of all y giving the same (E, s)
    (Lee et al. 2016, Proposition 4.2)."""
    X = np.asarray(X, float)
    bhat = lasso(X, y, lam)
    E = np.flatnonzero(np.abs(bhat) > 1e-10)
    s = np.sign(bhat[E])
    n, p = X.shape
    N = np.setdiff1d(np.arange(p), E)
    XE, XN = X[:, E], X[:, N]
    G = np.linalg.inv(XE.T @ XE)
    P = XE @ G @ XE.T
    pinvT = XE @ G  # (X_E^+)^T
    A0 = np.vstack([XN.T @ (np.eye(n) - P), -XN.T @ (np.eye(n) - P)]) / lam
    b0 = np.concatenate([1 - XN.T @ pinvT @ s, 1 + XN.T @ pinvT @ s])
    A1 = -np.diag(s) @ G @ XE.T
    b1 = -lam * np.diag(s) @ G @ s
    return {"beta": bhat, "E": E, "signs": s, "A": np.vstack([A0, A1]), "b": np.concatenate([b0, b1]), "pinv": G @ XE.T}


def lasso_selective_intervals(X, y, lam: float, sigma: float = 1.0, alpha: float = 0.05) -> dict:
    """Selective intervals for the partial regression coefficients of the selected model, eta_j = (X_E^+)' e_j,
    conditional on the event (E, s): a truncated normal pivot for each.  Also the naive OLS intervals on E."""
    ev = lasso_event(X, y, lam)
    out = []
    for k, j in enumerate(ev["E"]):
        eta = ev["pinv"][k]
        lim = polyhedral_limits(ev["A"], ev["b"], y, eta, sigma ** 2 * np.eye(len(y)))
        lo, hi = truncnorm_interval(lim["stat"], lim["sd"], lim["lo"], lim["hi"], alpha)
        z = stats.norm.ppf(1 - alpha / 2)
        out.append({"j": int(j), "est": lim["stat"], "sd": lim["sd"], "lo": lo, "hi": hi, "naive": (lim["stat"] - z * lim["sd"], lim["stat"] + z * lim["sd"]),
                    "trunc": (lim["lo"], lim["hi"])})
    return {"E": ev["E"], "signs": ev["signs"], "intervals": out}


# ---------------------------------------------------------------------------------------- inference on winners


def winner_conditional(y, sigma: float = 1.0, alpha: float = 0.05) -> dict:
    """Independent Y_k ~ N(mu_k, sigma^2); the winner j = argmax Y_k.  Given the losers, Y_j is N(mu_j, sigma^2)
    truncated to [max_{k != j} Y_k, inf): the conditional interval and median-unbiased estimate (Andrews, Kitagawa &
    McCloskey 2024, in the independent equal-variance case)."""
    y = np.asarray(y, float)
    j = int(np.argmax(y))
    lo_t = float(np.max(np.delete(y, j)))
    lo, hi = truncnorm_interval(y[j], sigma, lo_t, np.inf, alpha)
    med = _solve_increasing(lambda m: truncnorm_sf(y[j], m, sigma, lo_t, np.inf) - 0.5, y[j], sigma)
    z = stats.norm.ppf(1 - alpha / 2)
    return {"j": j, "y": float(y[j]), "second": lo_t, "lo": lo, "hi": hi, "median_unbiased": med,
            "naive": (float(y[j] - z * sigma), float(y[j] + z * sigma))}


def max_z_quantile(K: int, level: float) -> float:
    """The level quantile of max_k |Z_k| over K independent normals (the projection / simultaneous constant)."""
    return float(stats.norm.ppf(0.5 + 0.5 * level ** (1.0 / K)))


def winner_hybrid(y, sigma: float = 1.0, alpha: float = 0.05, beta: float = 0.005) -> dict:
    """The hybrid interval: condition on the winner and also on |Y_j - mu_j| <= c_beta sigma (c_beta the 1 - beta
    simultaneous constant), at level (alpha - beta)/(1 - beta); then intersect with the projection interval.  It is never
    longer than the projection interval and close to the conditional one when the win is clear."""
    y = np.asarray(y, float)
    K = len(y)
    j = int(np.argmax(y))
    lo_t = float(np.max(np.delete(y, j)))
    c = max_z_quantile(K, 1 - beta)
    a2 = (alpha - beta) / (1 - beta)
    proj = (float(y[j] - c * sigma), float(y[j] + c * sigma))

    def sf(m):
        return truncnorm_sf(y[j], m, sigma, max(lo_t, m - c * sigma), m + c * sigma)

    def root(level):
        g = lambda m: sf(m) - level  # noqa: E731
        lo, hi = proj
        if g(lo) > 0:
            return lo
        if g(hi) < 0:
            return hi
        return optimize.brentq(g, lo, hi, xtol=1e-9)

    return {"lo": root(a2 / 2), "hi": root(1 - a2 / 2), "projection": proj}


# ------------------------------------------------------------------------------------------------ PoSI


def _contrasts(X):
    from itertools import combinations

    X = np.asarray(X, float)
    p = X.shape[1]
    L = []
    for k in range(1, p + 1):
        for M in combinations(range(p), k):
            XM = X[:, M]
            B = np.linalg.solve(XM.T @ XM, XM.T)  # rows: the contrasts l_{j.M}' y = beta_hat_{j.M}
            for r in B:
                L.append(r / np.linalg.norm(r))
    return np.asarray(L)


def posi_constant(X, rng: np.random.Generator, alpha: float = 0.05, reps: int = 20000) -> dict:
    """The PoSI constant K: P(max over submodels M and j in M of |t_{j.M}| <= K) = 1 - alpha with sigma known, by
    simulation (Berk et al. 2013), with the Bonferroni and Scheffe constants for comparison."""
    L = _contrasts(X)
    n = L.shape[1]
    Z = rng.standard_normal((reps, n))
    m = np.max(np.abs(Z @ L.T), axis=1)
    p = np.asarray(X).shape[1]
    nc = L.shape[0]
    return {"K": float(np.quantile(m, 1 - alpha)), "n_contrasts": nc, "z": float(stats.norm.ppf(1 - alpha / 2)),
            "bonferroni": float(stats.norm.ppf(1 - alpha / (2 * nc))), "scheffe": float(math.sqrt(stats.chi2.ppf(1 - alpha, p)))}


# -------------------------------------------------------------------------------- randomization: carving


def threshold_selective(y: float, c: float, sigma: float = 1.0, gamma: float = 0.0, alpha: float = 0.05,
                        grid: int = 4001) -> dict:
    """Report Y ~ N(mu, sigma^2) only if selected.  Hard selection (gamma = 0): Y > c, so the law given selection is
    N(mu, sigma^2) truncated to (c, inf).  Randomized selection (gamma > 0): Y + W > c with W ~ N(0, gamma^2) independent
    noise, so the selective density is proportional to phi((y - mu)/sigma) Phi((y - c)/gamma).  Returns the selective
    interval by inverting the pivot on a grid of mu."""
    if gamma <= 0:
        lo, hi = truncnorm_interval(y, sigma, c, np.inf, alpha)
        return {"lo": lo, "hi": hi}
    t = np.linspace(min(y, c) - 12 * sigma, max(y, c) + 12 * sigma, grid)
    logw = special.log_ndtr((t - c) / gamma)

    def sf(mu):
        lp = stats.norm.logpdf(t, mu, sigma) + logw
        w = np.exp(lp - lp.max())
        cdf = np.cumsum(w)
        cdf /= cdf[-1]
        return 1 - float(np.interp(y, t, cdf))

    mus = np.linspace(y - 10 * sigma, y + 6 * sigma, 1601)
    s = np.array([sf(m) for m in mus])
    lo = float(np.interp(alpha / 2, s, mus))
    hi = float(np.interp(1 - alpha / 2, s, mus))
    return {"lo": lo, "hi": hi}


# ------------------------------------------------------------------------------------- fission and thinning


def fission_normal(x, sigma: float, tau: float, rng: np.random.Generator) -> tuple:
    """Data fission for X ~ N(mu, sigma^2): with Z ~ N(0, sigma^2), f = X + tau Z and g = X - Z/tau are independent,
    f ~ N(mu, (1 + tau^2) sigma^2) and g ~ N(mu, (1 + 1/tau^2) sigma^2) (Leiner et al. 2023)."""
    x = np.asarray(x, float)
    z = sigma * rng.standard_normal(x.shape)
    return x + tau * z, x - z / tau


def thin_poisson(x, eps: float, rng: np.random.Generator) -> tuple:
    """Poisson thinning: X ~ Poisson(lam) split into X1 ~ Bin(X, eps) and X2 = X - X1, independent Poisson(eps lam) and
    Poisson((1 - eps) lam) (Neufeld, Dharamshi, Gao & Witten 2024)."""
    x = np.asarray(x)
    x1 = rng.binomial(x, eps)
    return x1, x - x1


# ------------------------------------------------------------------------------------ conformal selection


def conformal_selection(cal_scores, cal_labels, test_scores, c: float, q: float = 0.1) -> dict:
    """Jin & Candes (2023): select test units whose unobserved outcome is likely to exceed c, with FDR <= q.
    Conformal p-values p_j = (1 + #{i: Y_i <= c, V_i >= V_j}) / (n + 1), with V = the predicted score (higher means
    more promising; calibration units with Y_i > c are not counted), then Benjamini-Hochberg."""
    from explainer.stats.kit.multiple import bh

    cs, cy, ts = (np.asarray(v, float) for v in (cal_scores, cal_labels, test_scores))
    n = len(cs)
    null_scores = np.sort(cs[cy <= c])
    # count of calibration nulls with score >= V_j
    ge = len(null_scores) - np.searchsorted(null_scores, ts, side="left")
    p = (1 + ge) / (n + 1)
    r = bh(p, q)
    return {"p": p, "selected": np.asarray(r["reject"], bool)}


# -------------------------------------------------------------------------------- post-clustering inference


def two_means_1d(x) -> np.ndarray:
    """Two-means clustering in one dimension, exactly: the split of the sorted data minimizing within-cluster sum of
    squares.  Returns labels (0 = left, 1 = right) in the input order."""
    x = np.asarray(x, float)
    o = np.argsort(x)
    xs = x[o]
    n = len(x)
    cs, cs2 = np.cumsum(xs), np.cumsum(xs ** 2)
    k = np.arange(1, n)
    left = cs2[:-1] - cs[:-1] ** 2 / k
    right = (cs2[-1] - cs2[:-1]) - (cs[-1] - cs[:-1]) ** 2 / (n - k)
    k_best = int(k[np.argmin(left + right)])
    lab = np.zeros(n, int)
    lab[o[k_best:]] = 1
    return lab


def clustering_pvalues(x, sigma: float = 1.0, grid: int = 4001) -> dict:
    """Test equal means of the two clusters found by 1-D two-means.  Naive: the z-test of the difference.  Selective
    (Gao, Bien & Witten 2024, in one dimension): with nu the contrast and d = nu'x > 0 (the right cluster minus the left),
    perturb the data along nu, x'(phi) = x + (phi - d) nu / ||nu||^2, keep S = {phi >= 0: the clustering of x'(phi) is
    the clustering of x}, and compute P(phi >= d | phi in S) for phi ~ sigma ||nu|| chi_1, by a grid over phi."""
    x = np.asarray(x, float)
    lab = two_means_1d(x)
    n1, n2 = int(np.sum(lab == 0)), int(np.sum(lab == 1))
    nu = np.where(lab == 1, 1.0 / n2, -1.0 / n1)
    d = float(nu @ x)
    nn = float(nu @ nu)
    sd = sigma * math.sqrt(nn)
    naive = float(2 * stats.norm.sf(abs(d) / sd))
    phis = np.linspace(0.0, d + 10 * sd, grid)
    keep = np.zeros(grid, bool)
    for k, ph in enumerate(phis):
        keep[k] = np.array_equal(two_means_1d(x + (ph - d) * nu / nn), lab)
    dens = stats.norm.pdf(phis, 0, sd) * keep
    tot = dens.sum()
    sel = float(dens[phis >= d].sum() / tot) if tot > 0 else 1.0
    return {"labels": lab, "d": d, "sd": sd, "naive": naive, "selective": min(1.0, sel), "n": (n1, n2)}
