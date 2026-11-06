"""statkit.robust: estimators that survive bad data (Part 30 of *Statistics, Built*).

Location (trimmed and winsorized means, Hodges--Lehmann with its exact interval, Huber and Tukey-biweight
M-estimates by IRLS), scale (MAD, Rousseeuw & Croux's Qn and Sn), influence (sensitivity curves, theoretical
influence functions, empirical breakdown), efficiency (Pitman ARE of the Wilcoxon test, the Hodges--Lehmann 0.864
bound, asymptotic variances of M-estimators, Huber's minimax k), regression (LMS, FAST-LTS, the S/MM-estimator),
multivariate (FAST-MCD and robust distances), and heavy-tailed means (median of means, Catoni's estimator).  Checked
in ``tests/test_stats_kit_robust.py``.
"""

from __future__ import annotations

import math
from itertools import combinations

import numpy as np
from scipy import integrate, optimize, stats

# ------------------------------------------------------------------------------------------------- location


def trimmed_mean(x, alpha: float) -> float:
    """The alpha-trimmed mean: drop floor(alpha n) points from each end."""
    x = np.sort(np.asarray(x, float))
    g = int(math.floor(alpha * len(x)))
    return float(x[g:len(x) - g].mean())


def winsorized_mean(x, alpha: float) -> float:
    x = np.sort(np.asarray(x, float))
    g = int(math.floor(alpha * len(x)))
    y = x.copy()
    if g:
        y[:g] = x[g]
        y[-g:] = x[-g - 1]
    return float(y.mean())


def walsh_averages(x) -> np.ndarray:
    x = np.asarray(x, float)
    i, j = np.triu_indices(len(x))
    return (x[i] + x[j]) / 2


def hodges_lehmann(x) -> float:
    """The one-sample Hodges--Lehmann estimate: the median of the n(n+1)/2 Walsh averages (x_i + x_j)/2, i <= j."""
    return float(np.median(walsh_averages(x)))


def signed_rank_null(n: int) -> np.ndarray:
    """The exact null distribution of the Wilcoxon signed-rank statistic W+ (counts over 2^n sign patterns)."""
    c = np.zeros(n * (n + 1) // 2 + 1)
    c[0] = 1
    for k in range(1, n + 1):
        c[k:] = c[k:] + c[:-k].copy()
    return c / 2 ** n


def hodges_lehmann_ci(x, level: float = 0.95) -> tuple:
    """The exact distribution-free interval inverting the signed-rank test: the Walsh averages of ranks k and N - k + 1,
    k from the W+ null (normal approximation for n > 60)."""
    x = np.asarray(x, float)
    n = len(x)
    w = np.sort(walsh_averages(x))
    N = len(w)
    a = (1 - level) / 2
    if n <= 60:
        cdf = np.cumsum(signed_rank_null(n))
        k = int(np.searchsorted(cdf, a, side="right"))  # P(W+ <= k - 1) <= a < P(W+ <= k)
        k = max(k, 1)
    else:
        mu, sd = n * (n + 1) / 4, math.sqrt(n * (n + 1) * (2 * n + 1) / 24)
        k = max(int(math.floor(mu - stats.norm.ppf(1 - a) * sd)), 1)
    return float(w[k - 1]), float(w[N - k])


def psi_huber(u, k: float = 1.345):
    return np.clip(u, -k, k)


def psi_biweight(u, c: float = 4.685):
    return np.where(np.abs(u) < c, u * (1 - (u / c) ** 2) ** 2, 0.0)


def psi_hampel(u, a: float = 2.0, b: float = 4.0, c: float = 8.0):
    au = np.abs(u)
    s = np.sign(u)
    return np.where(au <= a, u, np.where(au <= b, a * s, np.where(au <= c, a * s * (c - au) / (c - b), 0.0)))


def mad(x, center=None, normalize: bool = True) -> float:
    x = np.asarray(x, float)
    m = np.median(x) if center is None else center
    return float(np.median(np.abs(x - m)) * (1.482602218505602 if normalize else 1.0))


def m_location(x, psi: str = "huber", k: float | None = None, scale: float | None = None, tol: float = 1e-10,
               max_iter: int = 500) -> dict:
    """An M-estimate of location by IRLS: solve sum psi((x_i - mu)/s) = 0 with s the MAD (fixed), starting at the
    median.  Huber's k = 1.345 and the biweight's c = 4.685 give 95% efficiency at the normal."""
    x = np.asarray(x, float)
    s = mad(x) if scale is None else scale
    if s <= 0:
        return {"mu": float(np.median(x)), "scale": 0.0, "weights": np.ones(len(x)), "iterations": 0}
    f = {"huber": psi_huber, "biweight": psi_biweight, "hampel": psi_hampel}[psi]
    kk = {"huber": 1.345, "biweight": 4.685, "hampel": None}[psi] if k is None else k
    mu = float(np.median(x))
    for it in range(max_iter):
        u = (x - mu) / s
        with np.errstate(invalid="ignore", divide="ignore"):
            w = np.where(np.abs(u) > 1e-12, (f(u, kk) if kk is not None else f(u)) / u, 1.0)
        if w.sum() <= 0:
            break
        new = float(np.sum(w * x) / np.sum(w))
        if abs(new - mu) < tol * s:
            mu = new
            break
        mu = new
    u = (x - mu) / s
    with np.errstate(invalid="ignore", divide="ignore"):
        w = np.where(np.abs(u) > 1e-12, (f(u, kk) if kk is not None else f(u)) / u, 1.0)
    return {"mu": mu, "scale": s, "weights": w, "iterations": it + 1}


# --------------------------------------------------------------------------------------------------- scale


def qn_scale(x, finite_sample: bool = True) -> float:
    """Rousseeuw & Croux's (1993) Qn: 2.2219 times the k-th order statistic of the n(n-1)/2 pairwise distances,
    k = C(h, 2), h = floor(n/2) + 1, with their small-sample correction factors."""
    x = np.asarray(x, float)
    n = len(x)
    i, j = np.triu_indices(n, 1)
    d = np.sort(np.abs(x[i] - x[j]))
    h = n // 2 + 1
    k = h * (h - 1) // 2
    q = 2.2219 * d[k - 1]
    if not finite_sample:
        return float(q)
    if n <= 9:
        dn = [0.399, 0.994, 0.512, 0.844, 0.611, 0.857, 0.669, 0.872][n - 2]
    elif n % 2:
        dn = n / (n + 1.4)
    else:
        dn = n / (n + 3.8)
    return float(q * dn)


def sn_scale(x) -> float:
    """Rousseeuw & Croux's Sn: 1.1926 times med_i med_j |x_i - x_j| (low medians as in the paper, simplified)."""
    x = np.asarray(x, float)
    n = len(x)
    inner = np.array([np.median(np.abs(x[i] - x)) for i in range(n)])
    c = n / (n - 0.9) if n % 2 else 1.0
    return float(1.1926 * c * np.median(inner))


# --------------------------------------------------------------------------------------- influence and breakdown


def sensitivity_curve(est, x, grid) -> np.ndarray:
    """Tukey's sensitivity curve SC(z) = (n + 1)(T(x, z) - T(x)): the scaled effect of adding one point at z."""
    x = np.asarray(x, float)
    t0 = est(x)
    return np.array([(len(x) + 1) * (est(np.append(x, z)) - t0) for z in grid])


def influence_mean(z, mu=0.0):
    return np.asarray(z, float) - mu


def influence_median(z, f0: float = 1 / math.sqrt(2 * math.pi)):
    return np.sign(z) / (2 * f0)


def influence_huber(z, k: float = 1.345):
    """IF of Huber's M at the standard normal (known scale): psi_k(z) / E psi_k'(Z) = psi_k(z) / (2 Phi(k) - 1)."""
    return psi_huber(z, k) / (2 * stats.norm.cdf(k) - 1)


def influence_trimmed(z, alpha: float):
    """IF of the alpha-trimmed mean at the standard normal: the winsorized z, over 1 - 2 alpha."""
    q = stats.norm.ppf(1 - alpha)
    return np.clip(z, -q, q) / (1 - 2 * alpha)


def empirical_breakdown(est, x, big: float = 1e6) -> float:
    """The smallest share m/n of points that, replaced by a value B, carry the estimate beyond any bound: the estimate
    still moves when B grows from ``big`` to 10 ``big`` (by more than 1e-4 big)."""
    x = np.sort(np.asarray(x, float))
    n = len(x)
    for m in range(1, n + 1):
        y1, y2 = x.copy(), x.copy()
        y1[-m:] = big
        y2[-m:] = 10 * big
        if abs(est(y2) - est(y1)) > 1e-4 * big:
            return m / n
    return 1.0


# ------------------------------------------------------------------------------------------------- efficiency


def wilcoxon_are(pdf, var: float, lim: float = 50.0) -> float:
    """Pitman ARE of the Wilcoxon signed-rank (or rank-sum) test to the t-test for a symmetric density f with
    variance var: 12 var (int f^2)^2 (Hodges & Lehmann 1956)."""
    i2 = integrate.quad(lambda t: pdf(t) ** 2, -lim, lim, limit=400)[0]
    return float(12 * var * i2 ** 2)


def m_asymptotic_variance(psi, pdf, lim: float = 50.0) -> float:
    """V(psi, F) = E psi^2 / (E psi')^2 for a symmetric F with unit scale; E psi' by integration by parts as
    -int psi f'... computed here as int psi(x) (-f'(x)) dx via numerical differentiation of f."""
    num = integrate.quad(lambda t: psi(t) ** 2 * pdf(t), -lim, lim, limit=400)[0]
    h = 1e-5
    den = integrate.quad(lambda t: psi(t) * -(pdf(t + h) - pdf(t - h)) / (2 * h), -lim, lim, limit=400)[0]
    return float(num / den ** 2)


def huber_k(eps: float) -> float:
    """Huber's (1964) minimax k for the eps-contaminated normal: 2 phi(k)/k - 2 Phi(-k) = eps / (1 - eps)."""
    if eps <= 0:
        return math.inf
    f = lambda k: 2 * stats.norm.pdf(k) / k - 2 * stats.norm.cdf(-k) - eps / (1 - eps)
    return float(optimize.brentq(f, 1e-6, 20))


def huber_minimax_variance(eps: float) -> float:
    """The asymptotic variance of Huber's estimate at the least favourable distribution: 1 / I(F_0)."""
    k = huber_k(eps)
    # the least favourable density: (1 - eps) phi(x) in the middle, exponential tails; its Fisher information
    i = (1 - eps) * (2 * stats.norm.cdf(k) - 1)
    return float(1 / i)


def contaminated_variance(est_psi, eps: float, scale_out: float, lim: float = 60.0) -> float:
    """V(psi, F) at F = (1 - eps) N(0, 1) + eps N(0, scale_out^2)."""
    pdf = lambda t: (1 - eps) * stats.norm.pdf(t) + eps * stats.norm.pdf(t, 0, scale_out)
    return m_asymptotic_variance(est_psi, pdf, lim)


# --------------------------------------------------------------------------------------------------- regression


def _ols(X, y):
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    return b


def lms(X, y, n_sub: int = 3000, rng: np.random.Generator | None = None) -> dict:
    """Rousseeuw's (1984) least median of squares, by elemental subsets: fit exactly through p points, keep the fit
    with the smallest median squared residual."""
    rng = rng or np.random.default_rng(0)
    X, y = np.asarray(X, float), np.asarray(y, float)
    n, p = X.shape
    best = (np.inf, None)
    for _ in range(n_sub):
        idx = rng.choice(n, p, replace=False)
        try:
            b = np.linalg.solve(X[idx], y[idx])
        except np.linalg.LinAlgError:
            continue
        m = np.median((y - X @ b) ** 2)
        if m < best[0]:
            best = (m, b)
    return {"coef": best[1], "crit": float(best[0])}


def lts(X, y, h: int | None = None, n_starts: int = 500, rng: np.random.Generator | None = None) -> dict:
    """FAST-LTS (Rousseeuw & Van Driessen 2006): least trimmed squares, the fit minimizing the sum of the h smallest
    squared residuals, h = floor((n + p + 1)/2) by default.  Random elemental starts, each improved by C-steps (refit
    on the h best points, which never increases the criterion), and the best of the converged fits kept.  Returns the
    coefficients, the h-subset, a consistency-corrected scale and standardized residuals."""
    rng = rng or np.random.default_rng(0)
    X, y = np.asarray(X, float), np.asarray(y, float)
    n, p = X.shape
    h = h or (n + p + 1) // 2

    def csteps(b, k):
        for _ in range(k):
            r2 = (y - X @ b) ** 2
            H = np.argsort(r2)[:h]
            nb = _ols(X[H], y[H])
            if np.allclose(nb, b, atol=1e-12):
                break
            b = nb
        r2 = np.sort((y - X @ b) ** 2)
        return b, float(r2[:h].sum())

    cands = []
    for _ in range(n_starts):
        idx = rng.choice(n, p, replace=False)
        try:
            b = np.linalg.solve(X[idx], y[idx])
        except np.linalg.LinAlgError:
            continue
        cands.append(csteps(b, 2))
    cands.sort(key=lambda t: t[1])
    best = min((csteps(b, 100) for b, _ in cands[:10]), key=lambda t: t[1])
    b, crit = best
    r = y - X @ b
    q = h / n
    # consistency factor for the trimmed variance at the normal
    cq = stats.norm.ppf((1 + q) / 2)
    cons = q / (q - 2 * cq * stats.norm.pdf(cq))
    s = math.sqrt(cons * crit / h)
    # one reweighting step's scale estimate, as is customary
    keep = np.abs(r / s) <= 2.5
    b_rw = _ols(X[keep], y[keep])
    r_rw = y - X @ b_rw
    s_rw = math.sqrt(np.sum(r_rw[keep] ** 2) / (keep.sum() - p))
    return {"coef": b, "crit": crit, "h": h, "subset": np.argsort(r ** 2)[:h], "scale": s, "std_resid": r / s,
            "outliers": np.where(np.abs(r / s) > 2.5)[0], "coef_rw": b_rw, "scale_rw": s_rw,
            "outliers_rw": np.where(np.abs(r_rw / s_rw) > 2.5)[0]}


def _rho_biweight(u, c):
    u = np.minimum(np.abs(u) / c, 1.0)
    return 1 - (1 - u * u) ** 3  # normalized to a maximum of 1


def m_scale(r, c: float = 1.547, b: float = 0.5, tol: float = 1e-10) -> float:
    """The M-scale solving mean rho(r/s) = b with the biweight rho (c = 1.547, b = 1/2: 50% breakdown, consistent at
    the normal)."""
    r = np.asarray(r, float)
    s = np.median(np.abs(r)) / 0.6745
    if s <= 0:
        return 0.0
    for _ in range(200):
        new = s * math.sqrt(np.mean(_rho_biweight(r / s, c)) / b)
        if abs(new - s) < tol * s:
            return float(new)
        s = new
    return float(s)


def mm_regression(X, y, rng: np.random.Generator | None = None, c: float = 4.685) -> dict:
    """Yohai's (1987) MM-estimator: a high-breakdown start (here FAST-LTS), its M-scale (biweight, 50% breakdown),
    then biweight M-regression with that scale held fixed, by IRLS (95% efficiency at the normal for c = 4.685)."""
    X, y = np.asarray(X, float), np.asarray(y, float)
    start = lts(X, y, rng=rng)
    s = m_scale(y - X @ start["coef"])
    b = start["coef"].copy()
    for it in range(500):
        u = (y - X @ b) / s
        w = np.where(np.abs(u) < c, (1 - (u / c) ** 2) ** 2, 0.0)
        W = np.sqrt(w)
        nb = _ols(X * W[:, None], y * W)
        if np.max(np.abs(nb - b)) < 1e-10:
            b = nb
            break
        b = nb
    u = (y - X @ b) / s
    w = np.where(np.abs(u) < c, (1 - (u / c) ** 2) ** 2, 0.0)
    return {"coef": b, "scale": s, "weights": w, "start": start["coef"], "iterations": it + 1}


def irls_huber_regression(X, y, k: float = 1.345, max_iter: int = 200) -> dict:
    """Huber M-regression with a MAD scale of the residuals, re-estimated each step (as in rlm's default)."""
    X, y = np.asarray(X, float), np.asarray(y, float)
    b = _ols(X, y)
    for _ in range(max_iter):
        r = y - X @ b
        s = mad(r, 0.0) or 1.0
        u = r / s
        w = np.where(np.abs(u) <= k, 1.0, k / np.abs(u))
        W = np.sqrt(w)
        nb = _ols(X * W[:, None], y * W)
        if np.max(np.abs(nb - b)) < 1e-10:
            b = nb
            break
        b = nb
    return {"coef": b, "scale": s, "weights": w}


# ------------------------------------------------------------------------------------------------- multivariate


def mahalanobis(X, mu, S) -> np.ndarray:
    D = np.asarray(X, float) - mu
    return np.sqrt(np.einsum("ij,ij->i", D @ np.linalg.inv(S), D))


def mcd(X, h: int | None = None, n_starts: int = 500, rng: np.random.Generator | None = None, reweight: bool = True) -> dict:
    """FAST-MCD (Rousseeuw & Van Driessen 1999): the h-subset whose covariance has the smallest determinant, by
    C-steps from random (p + 1)-subsets, then consistency-corrected and (optionally) reweighted by the 97.5% chi^2
    cutoff.  Returns location, scatter, robust distances, and the flagged points."""
    rng = rng or np.random.default_rng(0)
    X = np.asarray(X, float)
    n, p = X.shape
    h = h or (n + p + 1) // 2

    def csteps(H, k):
        for _ in range(k):
            mu = X[H].mean(0)
            S = np.cov(X[H].T, bias=False)
            d = mahalanobis(X, mu, S)
            newH = np.sort(np.argsort(d)[:h])
            if np.array_equal(newH, H):
                break
            H = newH
        mu = X[H].mean(0)
        S = np.cov(X[H].T)
        return H, mu, S, float(np.linalg.det(S))

    cands = []
    for _ in range(n_starts):
        J = rng.choice(n, p + 1, replace=False)
        S = np.cov(X[J].T)
        if np.linalg.matrix_rank(S) < p:
            continue
        d = mahalanobis(X, X[J].mean(0), S)
        H = np.sort(np.argsort(d)[:h])
        cands.append(csteps(H, 2))
    cands.sort(key=lambda t: t[3])
    H, mu, S, det = min((csteps(c[0], 100) for c in cands[:10]), key=lambda t: t[3])
    d2 = mahalanobis(X, mu, S) ** 2
    S = S * np.median(d2) / stats.chi2.ppf(0.5, p)  # consistency at the normal
    out = {"h": h, "subset": H, "raw_location": mu, "raw_scatter": S}
    if reweight:
        d = mahalanobis(X, mu, S)
        keep = d <= math.sqrt(stats.chi2.ppf(0.975, p))
        mu, S = X[keep].mean(0), np.cov(X[keep].T)
    d = mahalanobis(X, mu, S)
    cut = math.sqrt(stats.chi2.ppf(0.975, p))
    out.update({"location": mu, "scatter": S, "distances": d, "cutoff": cut, "outliers": np.where(d > cut)[0],
                "classical": mahalanobis(X, X.mean(0), np.cov(X.T))})
    return out


# --------------------------------------------------------------------------------------- heavy-tailed means


def median_of_means(x, k: int, rng: np.random.Generator | None = None) -> float:
    """Split the sample at random into k blocks, average each, and take the median of the k averages (Nemirovski &
    Yudin 1983; Jerrum, Valiant & Vazirani 1986; Alon, Matias & Szegedy 1996)."""
    x = np.asarray(x, float)
    if rng is not None:
        x = x[rng.permutation(len(x))]
    blocks = np.array_split(x, k)
    return float(np.median([b.mean() for b in blocks]))


def catoni(x, delta: float, var: float | None = None) -> float:
    """Catoni's (2012) M-estimator: solve sum psi(alpha (x_i - theta)) = 0 with psi(u) = sign(u) log(1 + |u| + u^2/2)
    and alpha = sqrt(2 log(1/delta) / (n v)), v a variance bound (default: the sample variance)."""
    x = np.asarray(x, float)
    n = len(x)
    v = float(np.var(x, ddof=1)) if var is None else var
    a = math.sqrt(2 * math.log(1 / delta) / (n * v))

    def g(t):
        u = a * (x - t)
        return np.sum(np.sign(u) * np.log1p(np.abs(u) + u * u / 2))

    lo, hi = x.min() - 1, x.max() + 1
    return float(optimize.brentq(g, lo, hi))
