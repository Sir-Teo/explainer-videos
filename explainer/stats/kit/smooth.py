"""statkit.smooth: estimating curves (Part 29 of *Statistics, Built*).

Histograms and kernel density estimates with exact MISE for normal-mixture truths (Marron & Wand 1992); kernels and
their constants; bandwidth selectors (normal reference, Silverman, least-squares CV, Sheather--Jones's two-stage
plug-in); Silverman's (1981) critical-bandwidth test for the number of modes; Silverman's table for the curse of
dimensionality; local polynomial regression and LOESS; cubic smoothing splines in Reinsch form, with their smoother
matrix, Demmler--Reinsch eigenbasis, GCV and REML (GML) choices of lambda; kernel ridge regression; Haar and
Daubechies wavelets with VisuShrink and SureShrink; additive models by backfitting; robust bias-corrected intervals for
a density at a point (Calonico, Cattaneo & Farrell 2018); the Grenander estimator.  Everything is plain NumPy and
checked in ``tests/test_stats_kit_smooth.py``.
"""

from __future__ import annotations

import math

import numpy as np
from scipy import stats

SQ2PI = math.sqrt(2 * math.pi)

# ----------------------------------------------------------------------------------------------------- kernels


def _gauss(u):
    return np.exp(-0.5 * u * u) / SQ2PI


def _epan(u):
    return np.where(np.abs(u) <= 1, 0.75 * (1 - u * u), 0.0)


def _unif(u):
    return np.where(np.abs(u) <= 1, 0.5, 0.0)


def _tri(u):
    return np.where(np.abs(u) <= 1, 1 - np.abs(u), 0.0)


def _biw(u):
    return np.where(np.abs(u) <= 1, 15 / 16 * (1 - u * u) ** 2, 0.0)


def _tricube(u):
    return np.where(np.abs(u) < 1, 70 / 81 * (1 - np.abs(u) ** 3) ** 3, 0.0)


# name: (density, R(K) = int K^2, mu2(K) = int u^2 K)
KERNELS = {
    "gaussian": (_gauss, 1 / (2 * math.sqrt(math.pi)), 1.0),
    "epanechnikov": (_epan, 3 / 5, 1 / 5),
    "uniform": (_unif, 1 / 2, 1 / 3),
    "triangular": (_tri, 2 / 3, 1 / 6),
    "biweight": (_biw, 5 / 7, 1 / 7),
    "tricube": (_tricube, 175 / 247, 35 / 243),
}


def kernel(name: str):
    return KERNELS[name][0]


def kernel_efficiency(name: str) -> float:
    """Efficiency relative to Epanechnikov's optimal kernel: [C(Epan)/C(K)]^{5/4}, with C(K) = (sqrt(mu2) R(K))^{4/5}
    the kernel's factor in the minimal AMISE."""
    def c(k):
        _, R, m2 = KERNELS[k]
        return (math.sqrt(m2) * R) ** 0.8
    return float((c("epanechnikov") / c(name)) ** 1.25)


# ------------------------------------------------------------------------------------------------- histograms


def histogram_density(x, edges) -> np.ndarray:
    x = np.asarray(x, float)
    cnt = np.histogram(x, edges)[0]
    return cnt / (len(x) * np.diff(edges))


def histogram_mise(cdf, edges, n: int, Rf: float) -> float:
    """Exact MISE of the histogram with these bins: 1/(nh)-type terms summed bin by bin,
    MISE = sum_j [p_j (1 - p_j) / (n h_j) - p_j^2 / h_j] + R(f), with p_j the bin probabilities and R(f) = int f^2.
    (Mass outside the bins counts as estimated zero, contributing its share of R(f).)"""
    edges = np.asarray(edges, float)
    p = np.diff(cdf(edges))
    h = np.diff(edges)
    return float(np.sum(p * (1 - p) / (n * h) - p * p / h) + Rf)


def histogram_amise_h(n: int, R_fprime: float) -> float:
    """The AMISE-optimal bin width (6 / (n R(f')))^{1/3}; for a normal, 3.49 sigma n^{-1/3} (Scott 1979)."""
    return float((6 / (n * R_fprime)) ** (1 / 3))


def scott_binwidth(x) -> float:
    x = np.asarray(x, float)
    return float(3.49 * x.std(ddof=1) * len(x) ** (-1 / 3))


def freedman_diaconis(x) -> float:
    x = np.asarray(x, float)
    return float(2 * stats.iqr(x) * len(x) ** (-1 / 3))


# ------------------------------------------------------------------------------------- kernel density estimates


def kde(x, grid, h: float, kernel_name: str = "gaussian") -> np.ndarray:
    x, g = np.asarray(x, float), np.asarray(grid, float)
    K = kernel(kernel_name)
    out = np.empty(len(g))
    for i in range(0, len(g), 512):
        out[i:i + 512] = K((g[i:i + 512, None] - x[None, :]) / h).sum(1)
    return out / (len(x) * h)


class NormalMixture:
    """f = sum_l w_l N(mu_l, sigma_l^2): density, derivatives, sampling, and the exact functionals needed for MISE."""

    def __init__(self, w, mu, sigma):
        self.w = np.asarray(w, float) / np.sum(w)
        self.mu = np.asarray(mu, float)
        self.sigma = np.asarray(sigma, float)

    def pdf(self, x):
        x = np.asarray(x, float)[..., None]
        return np.sum(self.w * stats.norm.pdf(x, self.mu, self.sigma), -1)

    def cdf(self, x):
        x = np.asarray(x, float)[..., None]
        return np.sum(self.w * stats.norm.cdf(x, self.mu, self.sigma), -1)

    def d2(self, x):
        """f''(x)."""
        x = np.asarray(x, float)[..., None]
        z = (x - self.mu) / self.sigma
        return np.sum(self.w * stats.norm.pdf(z) * (z * z - 1) / self.sigma ** 3, -1)

    def rvs(self, n: int, rng: np.random.Generator) -> np.ndarray:
        k = rng.choice(len(self.w), size=n, p=self.w)
        return rng.normal(self.mu[k], self.sigma[k])

    def _omega(self, a: float, h: float) -> np.ndarray:
        s = np.sqrt(a * h * h + self.sigma[:, None] ** 2 + self.sigma[None, :] ** 2)
        return stats.norm.pdf(self.mu[:, None] - self.mu[None, :], 0, s)

    def R(self, r: int = 0) -> float:
        """int (f^{(r)})^2 for r = 0, 1, 2, exactly (products of normals integrate to normals)."""
        s2 = self.sigma[:, None] ** 2 + self.sigma[None, :] ** 2
        d = self.mu[:, None] - self.mu[None, :]
        # int phi_s1^{(r)}(x - m1) phi_s2^{(r)}(x - m2) dx = (-1)^r phi_s^{(2r)}(d), with s^2 = s1^2 + s2^2
        s = np.sqrt(s2)
        z = d / s
        he = {0: 1.0, 2: z * z - 1, 4: z ** 4 - 6 * z * z + 3}[2 * r]
        val = (-1) ** r * ((-1) ** (2 * r)) * he * stats.norm.pdf(z) / s ** (2 * r + 1)
        return float(self.w @ val @ self.w)

    def kde_mise(self, h: float, n: int) -> float:
        """The exact MISE of the Gaussian-kernel KDE (Marron & Wand 1992)."""
        w = self.w
        t = w @ ((1 - 1 / n) * self._omega(2, h) - 2 * self._omega(1, h) + self._omega(0, h)) @ w
        return float(1 / (2 * math.sqrt(math.pi) * n * h) + t)

    def kde_amise_h(self, n: int, kernel_name: str = "gaussian") -> float:
        _, RK, m2 = KERNELS[kernel_name]
        return float((RK / (m2 * m2 * self.R(2) * n)) ** 0.2)


def amise_h(n: int, R_f2: float, kernel_name: str = "gaussian") -> float:
    """(R(K) / (mu2^2 R(f'') n))^{1/5}."""
    _, RK, m2 = KERNELS[kernel_name]
    return float((RK / (m2 * m2 * R_f2 * n)) ** 0.2)


def normal_reference_h(x) -> float:
    x = np.asarray(x, float)
    return float(1.059 * x.std(ddof=1) * len(x) ** -0.2)


def silverman_h(x) -> float:
    x = np.asarray(x, float)
    return float(0.9 * min(x.std(ddof=1), stats.iqr(x) / 1.349) * len(x) ** -0.2)


def lscv(x, h: float) -> float:
    """Least-squares (unbiased) cross-validation for the Gaussian KDE: int fhat^2 - (2/n) sum_i fhat_{-i}(x_i)
    (Rudemo 1982; Bowman 1984), in closed form."""
    x = np.asarray(x, float)
    n = len(x)
    d = x[:, None] - x[None, :]
    a = stats.norm.pdf(d, 0, h * math.sqrt(2)).sum() / n ** 2
    b = (stats.norm.pdf(d, 0, h).sum() - n * stats.norm.pdf(0, 0, h)) / (n * (n - 1))
    return float(a - 2 * b)


def lscv_h(x, hs) -> float:
    v = [lscv(x, h) for h in hs]
    return float(hs[int(np.argmin(v))])


def _hermite(r: int, z):
    """Probabilists' Hermite polynomial He_r."""
    h0, h1 = np.ones_like(z), z
    if r == 0:
        return h0
    for k in range(1, r):
        h0, h1 = h1, z * h1 - k * h0
    return h1


def psi(x, r: int, g: float) -> float:
    """The density-functional estimate psi_r = n^{-2} sum_i sum_j phi_g^{(r)}(x_i - x_j), estimating int f^{(r)} f
    (= (-1)^{r/2} R(f^{(r/2)}) for even r)."""
    x = np.asarray(x, float)
    n = len(x)
    tot = 0.0
    for i in range(0, n, 1024):
        z = (x[i:i + 1024, None] - x[None, :]) / g
        tot += float(np.sum(_hermite(r, z) * np.exp(-0.5 * z * z)))
    return tot / (SQ2PI * n * n * g ** (r + 1))


def sheather_jones_h(x) -> float:
    """Sheather & Jones's (1991) two-stage direct plug-in bandwidth for the Gaussian KDE (Wand & Jones 1995, 3.6):
    a normal reference for psi_8, kernel estimates of psi_6 then psi_4, each at its own AMSE-optimal pilot bandwidth."""
    x = np.asarray(x, float)
    n = len(x)
    s = min(x.std(ddof=1), stats.iqr(x) / 1.349)
    psi8 = 105 / (32 * math.sqrt(math.pi) * s ** 9)
    g1 = (30 / (SQ2PI * psi8 * n)) ** (1 / 9)  # -2 phi^(6)(0) = 30/sqrt(2 pi)
    psi6 = psi(x, 6, g1)
    g2 = (-6 / (SQ2PI * psi6 * n)) ** (1 / 7)  # -2 phi^(4)(0) = -6/sqrt(2 pi)
    psi4 = psi(x, 4, g2)
    return float((1 / (2 * math.sqrt(math.pi) * psi4 * n)) ** 0.2)


# --------------------------------------------------------------------------------------------- modes and Silverman


def count_modes(f) -> int:
    f = np.asarray(f, float)
    d = np.diff(f)
    s = np.sign(d[np.abs(d) > 1e-14 * max(f.max(), 1e-300)])
    return int(np.sum((s[:-1] > 0) & (s[1:] < 0)))


def modes_at(x, h: float, grid) -> int:
    return count_modes(kde(x, grid, h))


def critical_bandwidth(x, k: int, grid=None, lo: float = 1e-3, hi: float | None = None, tol: float = 1e-4) -> float:
    """Silverman's h_k: the smallest bandwidth at which the Gaussian KDE has at most k modes (the number of modes of a
    Gaussian KDE is non-increasing in h, so bisection finds it)."""
    x = np.asarray(x, float)
    if grid is None:
        r = x.max() - x.min()
        grid = np.linspace(x.min() - 0.3 * r, x.max() + 0.3 * r, 801)
    hi = hi or 2 * x.std()
    while modes_at(x, hi, grid) > k:
        hi *= 2
    while hi - lo > tol * hi:
        m = 0.5 * (lo + hi)
        if modes_at(x, m, grid) <= k:
            hi = m
        else:
            lo = m
    return float(hi)


def silverman_test(x, k: int, B: int, rng: np.random.Generator, grid=None) -> dict:
    """Silverman's (1981) test of H0: at most k modes.  Smoothed bootstrap from fhat at h_k, rescaled to the sample
    variance; the p-value is the share of bootstrap samples needing a bandwidth above h_k, i.e. with more than k modes
    at h_k."""
    x = np.asarray(x, float)
    n = len(x)
    if grid is None:
        r = x.max() - x.min()
        grid = np.linspace(x.min() - 0.3 * r, x.max() + 0.3 * r, 801)
    hk = critical_bandwidth(x, k, grid)
    m, s2 = x.mean(), x.var()
    more = 0
    for _ in range(B):
        y = x[rng.integers(0, n, n)] + hk * rng.standard_normal(n)
        y = m + (y - m) / math.sqrt(1 + hk * hk / s2)
        more += modes_at(y, hk, grid) > k
    return {"h": hk, "p": more / B, "B": B}


def silverman_table(d: int, target: float = 0.1) -> int:
    """Silverman's (1986, Table 4.2): the sample size at which the Gaussian-kernel estimate of a d-variate standard
    normal density at 0, at its MSE-optimal bandwidth, first has relative MSE below ``target`` (exact finite-n MSE)."""
    def rel_mse(n, h):
        f0 = (2 * math.pi) ** (-d / 2)
        mean = (2 * math.pi * (1 + h * h)) ** (-d / 2)
        ek2 = (1 / (2 * math.sqrt(math.pi) * h) / math.sqrt(2 * math.pi * (1 + h * h / 2))) ** d
        var = (ek2 - mean * mean) / n
        return (var + (mean - f0) ** 2) / f0 ** 2

    def best(n):
        hs = np.geomspace(0.05, 3, 400)
        return min(rel_mse(n, h) for h in hs)

    lo, hi = 1, 2
    while best(hi) >= target:
        lo, hi = hi, hi * 2
    while hi - lo > 1:
        m = (lo + hi) // 2
        if best(m) < target:
            hi = m
        else:
            lo = m
    return int(hi)


# ------------------------------------------------------------------------------------------ local polynomials


def local_poly(x, y, x0, h: float, degree: int = 1, kernel_name: str = "gaussian") -> dict:
    """Local polynomial regression at the points x0 (Fan & Gijbels 1996).  Returns the fit and the equivalent-kernel
    weights l(x0) with fit = l(x0) @ y; degree 0 is Nadaraya--Watson."""
    x, y, x0 = np.asarray(x, float), np.asarray(y, float), np.atleast_1d(np.asarray(x0, float))
    K = kernel(kernel_name)
    L = np.zeros((len(x0), len(x)))
    for i, t in enumerate(x0):
        w = K((x - t) / h)
        X = np.vander(x - t, degree + 1, increasing=True)
        XtW = X.T * w
        A = XtW @ X
        L[i] = np.linalg.solve(A + 1e-12 * np.eye(degree + 1) * max(np.trace(A), 1e-300), XtW)[0]
    return {"fit": L @ y, "weights": L}


def loess(x, y, x0, span: float = 0.75, degree: int = 1, iterations: int = 0) -> np.ndarray:
    """Cleveland's (1979) LOESS: tricube weights over the nearest span*n points, local degree 1 or 2, and
    ``iterations`` robustness passes with bisquare weights on the residuals."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    x0 = np.atleast_1d(np.asarray(x0, float))
    n = len(x)
    q = max(int(math.ceil(span * n)), degree + 1)
    rob = np.ones(n)

    def fit_at(pts):
        out = np.empty(len(pts))
        for i, t in enumerate(pts):
            d = np.abs(x - t)
            hmax = np.partition(d, q - 1)[q - 1] * max(1.0, span) + 1e-12
            w = np.clip(1 - (d / hmax) ** 3, 0, None) ** 3 * rob
            X = np.vander(x - t, degree + 1, increasing=True)
            XtW = X.T * w
            out[i] = np.linalg.lstsq(XtW @ X, XtW @ y, rcond=None)[0][0]
        return out

    for _ in range(iterations):
        r = y - fit_at(x)
        s = np.median(np.abs(r))
        u = r / (6 * s + 1e-300)
        rob = np.clip(1 - u * u, 0, None) ** 2
    return fit_at(x0)


# -------------------------------------------------------------------------------------------- smoothing splines


def _QR(t):
    """Green & Silverman's (1994) band matrices for knots t: Q (n x n-2) and R (n-2 x n-2), with the roughness
    int g''^2 = g' Q R^{-1} Q' g for the natural cubic spline interpolating g at t."""
    t = np.asarray(t, float)
    n = len(t)
    h = np.diff(t)
    Q = np.zeros((n, n - 2))
    R = np.zeros((n - 2, n - 2))
    for j in range(1, n - 1):
        c = j - 1
        Q[j - 1, c] = 1 / h[j - 1]
        Q[j, c] = -1 / h[j - 1] - 1 / h[j]
        Q[j + 1, c] = 1 / h[j]
        R[c, c] = (h[j - 1] + h[j]) / 3
        if c + 1 < n - 2:
            R[c, c + 1] = R[c + 1, c] = h[j] / 6
    return Q, R


class SmoothingSpline:
    """The cubic smoothing spline: minimize sum_i w_i (y_i - g(t_i))^2 + lam int g''^2 over all functions.  By the
    Reinsch--Schoenberg theorem the minimizer is a natural cubic spline with knots at the distinct x; here it is
    computed in Reinsch form, ghat = (W + lam K)^{-1} W ybar with K = Q R^{-1} Q'.  Ties are pooled with weights."""

    def __init__(self, x, y, w=None):
        x, y = np.asarray(x, float), np.asarray(y, float)
        w = np.ones(len(x)) if w is None else np.asarray(w, float)
        t, inv = np.unique(x, return_inverse=True)
        W = np.bincount(inv, weights=w)
        yb = np.bincount(inv, weights=w * y) / W
        self.t, self.inv, self.W, self.ybar = t, inv, W, yb
        self.x, self.y, self.w = x, y, w
        Q, R = _QR(t)
        self.Q, self.R = Q, R
        self.K = Q @ np.linalg.solve(R, Q.T)
        self.K = 0.5 * (self.K + self.K.T)

    def smoother(self, lam: float) -> np.ndarray:
        """S on the distinct knots: ghat = S ybar (with the tie weights inside)."""
        W = np.diag(self.W)
        return np.linalg.solve(W + lam * self.K, W)

    def fit(self, lam: float) -> np.ndarray:
        """Fitted values at the distinct knots."""
        return self.smoother(lam) @ self.ybar

    def df(self, lam: float) -> float:
        """Effective degrees of freedom tr(S) on the observations (= trace of the knot smoother)."""
        return float(np.trace(self.smoother(lam)))

    def gcv(self, lam: float) -> float:
        g = self.fit(lam)
        r = self.y - g[self.inv]
        n = len(self.y)
        return float(np.sum(self.w * r * r) / n / (1 - self.df(lam) / n) ** 2)

    def lam_for_df(self, df: float) -> float:
        lo, hi = -12.0, 12.0
        for _ in range(80):
            m = 0.5 * (lo + hi)
            if self.df(10 ** m) > df:
                lo = m
            else:
                hi = m
        return float(10 ** (0.5 * (lo + hi)))

    def eigen(self):
        """The Demmler--Reinsch basis (unit weights): K = U diag(d) U', the eigenvalues ascending; S = U diag(1/(1 +
        lam d)) U'."""
        d, U = np.linalg.eigh(self.K)
        d[:2] = 0.0  # the null space: constants and lines
        return d, U

    def reml(self, lam: float) -> float:
        """The REML (generalized maximum likelihood, Wahba 1985) criterion for unit weights and distinct x: the spline
        as a mixed model, y = linear + random with precision (lam / sigma^2) K.  Returns minus the restricted log
        likelihood, with sigma^2 profiled out."""
        d, U = self.eigen()
        z = U.T @ self.ybar
        dk, zk = d[2:], z[2:]
        v = 1 + 1 / (lam * dk)
        m = len(dk)
        s2 = np.sum(zk * zk / v) / m
        return float(0.5 * (np.sum(np.log(v)) + m * np.log(s2) + m))

    def choose(self, criterion: str = "gcv", grid=None) -> float:
        grid = np.geomspace(1e-8, 1e4, 241) if grid is None else grid
        f = self.gcv if criterion == "gcv" else self.reml
        v = [f(l) for l in grid]
        return float(grid[int(np.argmin(v))])

    def predict(self, lam: float, x0) -> np.ndarray:
        """Evaluate the natural cubic spline through the fitted values (second derivatives gamma = R^{-1} Q' g, zero at
        the ends); linear beyond the boundary knots."""
        g = self.fit(lam)
        return natural_spline_eval(self.t, g, np.linalg.solve(self.R, self.Q.T @ g), x0)


def natural_spline_eval(t, g, gamma_inner, x0) -> np.ndarray:
    t = np.asarray(t, float)
    gam = np.concatenate([[0.0], np.asarray(gamma_inner, float), [0.0]])
    x0 = np.asarray(x0, float)
    out = np.empty(len(x0))
    h = np.diff(t)
    for k, u in enumerate(x0):
        if u <= t[0]:
            d = (g[1] - g[0]) / h[0] - h[0] / 6 * gam[1]
            out[k] = g[0] + (u - t[0]) * d
        elif u >= t[-1]:
            d = (g[-1] - g[-2]) / h[-1] + h[-1] / 6 * gam[-2]
            out[k] = g[-1] + (u - t[-1]) * d
        else:
            i = min(int(np.searchsorted(t, u, side="right") - 1), len(t) - 2)
            a, b, hi = u - t[i], t[i + 1] - u, h[i]
            out[k] = (a * g[i + 1] + b * g[i]) / hi - a * b / 6 * ((1 + a / hi) * gam[i + 1] + (1 + b / hi) * gam[i])
    return out


# ------------------------------------------------------------------------------------------------ kernel ridge


def gaussian_kernel_matrix(a, b, ell: float) -> np.ndarray:
    a, b = np.atleast_2d(np.asarray(a, float).T).T, np.atleast_2d(np.asarray(b, float).T).T
    d2 = ((a[:, None, :] - b[None, :, :]) ** 2).sum(-1)
    return np.exp(-0.5 * d2 / ell ** 2)


def kernel_ridge(x, y, lam: float, ell: float, x0=None) -> dict:
    """Kernel ridge regression: by the representer theorem (Kimeldorf & Wahba 1970) the minimizer of
    sum (y_i - f(x_i))^2 + lam ||f||_H^2 is f = sum alpha_i k(x_i, .), alpha = (K + lam I)^{-1} y."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    K = gaussian_kernel_matrix(x, x, ell)
    alpha = np.linalg.solve(K + lam * np.eye(len(y)), y)
    out = {"alpha": alpha, "fit": K @ alpha, "df": float(np.trace(K @ np.linalg.inv(K + lam * np.eye(len(y)))))}
    if x0 is not None:
        out["pred"] = gaussian_kernel_matrix(x0, x, ell) @ alpha
    return out


# ---------------------------------------------------------------------------------------------------- wavelets

D4 = np.array([1 + math.sqrt(3), 3 + math.sqrt(3), 3 - math.sqrt(3), 1 - math.sqrt(3)]) / (4 * math.sqrt(2))
HAAR = np.array([1.0, 1.0]) / math.sqrt(2)


def _qmf(h):
    g = h[::-1].copy()
    g[1::2] *= -1
    return g


def dwt(x, h=D4, levels: int | None = None) -> list:
    """The periodic orthonormal discrete wavelet transform (Mallat's pyramid).  Returns [s_J, d_J, ..., d_1]: the
    coarsest smooth coefficients, then detail coefficients from coarse to fine."""
    x = np.asarray(x, float)
    n = len(x)
    J = int(round(math.log2(n)))
    assert 2 ** J == n
    levels = J if levels is None else levels
    g = _qmf(h)
    L = len(h)
    s, details = x, []
    for _ in range(levels):
        m = len(s)
        idx = (2 * np.arange(m // 2)[:, None] + np.arange(L)[None, :]) % m
        a, d = s[idx] @ h, s[idx] @ g
        details.append(d)
        s = a
    return [s] + details[::-1]


def idwt(coefs, h=D4) -> np.ndarray:
    g = _qmf(h)
    L = len(h)
    s = np.asarray(coefs[0], float)
    for d in coefs[1:]:
        m = 2 * len(s)
        out = np.zeros(m)
        idx = (2 * np.arange(m // 2)[:, None] + np.arange(L)[None, :]) % m
        np.add.at(out, idx, s[:, None] * h[None, :] + np.asarray(d)[:, None] * g[None, :])
        s = out
    return s


def mad_sigma(finest) -> float:
    """Donoho & Johnstone's noise estimate: the median absolute finest-scale coefficient over 0.6745."""
    return float(np.median(np.abs(finest)) / 0.6745)


def soft(x, t):
    return np.sign(x) * np.maximum(np.abs(x) - t, 0.0)


def hard(x, t):
    return np.where(np.abs(x) > t, x, 0.0)


def sure_threshold(d, sigma: float) -> float:
    """The threshold minimizing Stein's unbiased risk estimate for soft thresholding,
    SURE(t) = n - 2 #{|x_i| <= t} + sum min(|x_i|, t)^2 (on the sigma = 1 scale), with Donoho & Johnstone's (1995)
    hybrid: the universal threshold when the coefficients look sparse."""
    x = np.abs(np.asarray(d, float)) / sigma
    n = len(x)
    univ = math.sqrt(2 * math.log(n))
    if n < 2:
        return univ * sigma
    if np.sum(x * x - 1) / n <= math.log2(n) ** 1.5 / math.sqrt(n):  # sparse: use the universal threshold
        return univ * sigma
    xs = np.sort(x)
    cs = np.cumsum(xs * xs)
    k = np.arange(1, n + 1)
    risk = n - 2 * k + cs + (n - k) * xs * xs
    t = xs[int(np.argmin(risk))]
    return float(min(t, univ) * sigma)


def wavelet_denoise(y, rule: str = "visu", h=D4, coarse: int = 3) -> dict:
    """VisuShrink (soft at sigma sqrt(2 log n)) or SureShrink (level-by-level SURE), keeping the 2^coarse smooth
    coefficients."""
    y = np.asarray(y, float)
    n = len(y)
    J = int(round(math.log2(n)))
    c = dwt(y, h, J - coarse)
    sigma = mad_sigma(c[-1])
    out = [c[0]]
    th = []
    for d in c[1:]:
        t = sigma * math.sqrt(2 * math.log(n)) if rule == "visu" else sure_threshold(d, sigma)
        th.append(t)
        out.append(soft(d, t))
    return {"fit": idwt(out, h), "sigma": sigma, "thresholds": th, "coefs": c, "kept": int(sum(np.sum(o != 0) for o in out[1:]))}


def dj_function(name: str, n: int) -> np.ndarray:
    """Donoho & Johnstone's (1994) test signals on t = i/n: blocks, bumps, heavisine, doppler (scaled to SD 7, as in
    their simulations)."""
    t = np.arange(n) / n
    if name == "heavisine":
        f = 4 * np.sin(4 * np.pi * t) - np.sign(t - 0.3) - np.sign(0.72 - t)
    elif name == "doppler":
        e = 0.05
        f = np.sqrt(t * (1 - t)) * np.sin(2 * np.pi * (1 + e) / (t + e))
    elif name == "blocks":
        pos = np.array([.1, .13, .15, .23, .25, .40, .44, .65, .76, .78, .81])
        hgt = np.array([4, -5, 3, -4, 5, -4.2, 2.1, 4.3, -3.1, 2.1, -4.2])
        f = np.sum(hgt[None, :] * (1 + np.sign(t[:, None] - pos[None, :])) / 2, 1)
    elif name == "bumps":
        pos = np.array([.1, .13, .15, .23, .25, .40, .44, .65, .76, .78, .81])
        hgt = np.array([4, 5, 3, 4, 5, 4.2, 2.1, 4.3, 3.1, 5.1, 4.2])
        wid = np.array([.005, .005, .006, .01, .01, .03, .01, .01, .005, .008, .005])
        f = np.sum(hgt[None, :] / (1 + np.abs((t[:, None] - pos[None, :]) / wid[None, :])) ** 4, 1)
    else:
        raise ValueError(name)
    return 7 * f / f.std()


# ------------------------------------------------------------------------------------------- additive models


def backfit(X, y, lams, iters: int = 50, tol: float = 1e-8) -> dict:
    """An additive model y = alpha + sum_j f_j(x_j) + e by backfitting (Buja, Hastie & Tibshirani 1989), each f_j a
    cubic smoothing spline with penalty lams[j], centred to mean zero."""
    X, y = np.asarray(X, float), np.asarray(y, float)
    n, p = X.shape
    alpha = y.mean()
    f = np.zeros((n, p))
    sps = [SmoothingSpline(X[:, j], np.zeros(n)) for j in range(p)]
    S = [sp.smoother(l) for sp, l in zip(sps, lams)]
    for it in range(iters):
        old = f.copy()
        for j in range(p):
            r = y - alpha - f.sum(1) + f[:, j]
            sp = sps[j]
            rb = np.bincount(sp.inv, weights=r) / sp.W
            fj = (S[j] @ rb)[sp.inv]
            f[:, j] = fj - fj.mean()
        if np.max(np.abs(f - old)) < tol:
            break
    return {"alpha": float(alpha), "f": f, "fit": alpha + f.sum(1), "iterations": it + 1}


# ------------------------------------------------------------------------------------- inference for a density


def kde_ci(x, x0: float, h: float, level: float = 0.95, robust: bool = False) -> tuple:
    """A pointwise interval for f(x0) with the Gaussian kernel.  Conventional: fhat_h(x0) +- z SE.  Robust
    bias-corrected (Calonico, Cattaneo & Farrell 2018) with pilot b = h: subtract the estimated leading bias
    (h^2/2) fhat''_h(x0), i.e. use the kernel M(u) = K(u) - K''(u)/2, and take the SE of that estimator, so the
    interval accounts for the bias correction's own variability."""
    x = np.asarray(x, float)
    n = len(x)
    u = (x0 - x) / h
    K = np.exp(-0.5 * u * u) / SQ2PI
    terms = (K - 0.5 * (u * u - 1) * K) / h if robust else K / h
    est = terms.mean()
    se = terms.std(ddof=1) / math.sqrt(n)
    z = stats.norm.ppf(0.5 + level / 2)
    return float(est - z * se), float(est + z * se), float(est)


def pointwise_mse_h(f0: float, f2: float, n: int) -> float:
    """The pointwise MSE-optimal Gaussian-kernel bandwidth at x0: (f(x0) R(K) / (f''(x0)^2 n))^{1/5}."""
    return float((f0 / (2 * math.sqrt(math.pi)) / (f2 * f2 * n)) ** 0.2)


# ------------------------------------------------------------------------------------------- shape constraints


def grenander(x) -> dict:
    """The Grenander estimator of a non-increasing density on [0, inf): the left derivative of the least concave
    majorant of the empirical CDF.  Returns the knots and the density on each interval between them."""
    x = np.sort(np.asarray(x, float))
    n = len(x)
    px = np.concatenate([[0.0], x])
    py = np.arange(n + 1) / n
    hull = [0]
    for i in range(1, n + 1):
        hull.append(i)
        while len(hull) >= 3:
            a, b, c = hull[-3], hull[-2], hull[-1]
            # remove b if it lies on or below the chord a-c (concavity)
            if (py[b] - py[a]) * (px[c] - px[a]) <= (py[c] - py[a]) * (px[b] - px[a]):
                hull.pop(-2)
            else:
                break
    k = np.array(hull)
    slopes = np.diff(py[k]) / np.diff(px[k])
    return {"knots": px[k], "density": slopes}


def grenander_at(g: dict, t) -> np.ndarray:
    t = np.atleast_1d(np.asarray(t, float))
    i = np.clip(np.searchsorted(g["knots"], t, side="left") - 1, 0, len(g["density"]) - 1)
    out = g["density"][i]
    return np.where((t < 0) | (t > g["knots"][-1]), 0.0, out)
