"""statkit.ols: least squares written out (Part 12 of *Statistics, Built*).

    from explainer.stats.kit.ols import fit, design
    r = fit(X, y)                       # X includes the intercept column (see ``design``)
    r.coef, r.se(), r.se("HC3"), r.t(), r.pvalue(), r.r2, r.leverage, r.cooks, r.ci(), r.band(X0)

Everything is computed from a QR decomposition (Part 4: never invert X'X).  Checked against statsmodels in
``tests/test_stats_kit_ols.py``.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from scipy import stats


def design(*columns, intercept: bool = True) -> np.ndarray:
    cols = [np.asarray(c, float) for c in columns]
    if intercept:
        cols = [np.ones(len(cols[0]))] + cols
    return np.column_stack(cols)


@dataclass
class Fit:
    X: np.ndarray
    y: np.ndarray
    coef: np.ndarray
    resid: np.ndarray
    fitted: np.ndarray
    XtX_inv: np.ndarray
    n: int
    p: int
    leverage: np.ndarray = field(repr=False, default=None)

    @property
    def df(self) -> int:
        return self.n - self.p

    @property
    def sigma2(self) -> float:
        return float(self.resid @ self.resid / self.df)

    @property
    def rss(self) -> float:
        return float(self.resid @ self.resid)

    @property
    def r2(self) -> float:
        tss = float(((self.y - self.y.mean()) ** 2).sum())
        return 1 - self.rss / tss

    @property
    def adj_r2(self) -> float:
        return 1 - (1 - self.r2) * (self.n - 1) / self.df

    def cov(self, kind: str = "classical") -> np.ndarray:
        """Classical sigma^2 (X'X)^-1, or White's sandwich HC0 (1980) and MacKinnon & White's (1985) HC1-HC3."""
        if kind == "classical":
            return self.sigma2 * self.XtX_inv
        e2 = self.resid ** 2
        if kind == "HC0":
            w = e2
        elif kind == "HC1":
            w = e2 * self.n / self.df
        elif kind == "HC2":
            w = e2 / (1 - self.leverage)
        elif kind == "HC3":
            w = e2 / (1 - self.leverage) ** 2
        else:
            raise ValueError(kind)
        meat = (self.X * w[:, None]).T @ self.X
        return self.XtX_inv @ meat @ self.XtX_inv

    def se(self, kind: str = "classical") -> np.ndarray:
        return np.sqrt(np.diag(self.cov(kind)))

    def t(self, kind: str = "classical") -> np.ndarray:
        return self.coef / self.se(kind)

    def pvalue(self, kind: str = "classical") -> np.ndarray:
        return 2 * stats.t.sf(np.abs(self.t(kind)), self.df)

    def ci(self, alpha=0.05, kind: str = "classical") -> np.ndarray:
        h = stats.t.ppf(1 - alpha / 2, self.df) * self.se(kind)
        return np.column_stack([self.coef - h, self.coef + h])

    def predict(self, X0) -> np.ndarray:
        return np.asarray(X0, float) @ self.coef

    def band(self, X0, alpha=0.05, prediction=False, simultaneous=False):
        """Pointwise (or Working-Hotelling simultaneous) confidence band for the mean, or a prediction band."""
        X0 = np.atleast_2d(np.asarray(X0, float))
        m = X0 @ self.coef
        v = np.einsum("ij,jk,ik->i", X0, self.XtX_inv, X0) * self.sigma2
        if prediction:
            v = v + self.sigma2
        q = np.sqrt(self.p * stats.f.ppf(1 - alpha, self.p, self.df)) if simultaneous else stats.t.ppf(1 - alpha / 2, self.df)
        h = q * np.sqrt(v)
        return m - h, m + h

    @property
    def student(self) -> np.ndarray:
        """Internally studentized residuals e_i / (s sqrt(1 - h_ii))."""
        return self.resid / np.sqrt(self.sigma2 * (1 - self.leverage))

    @property
    def cooks(self) -> np.ndarray:
        """Cook's distance (1977): D_i = r_i^2 h_ii / (p (1 - h_ii))."""
        return self.student ** 2 * self.leverage / (self.p * (1 - self.leverage))

    def f_test(self, other: "Fit") -> dict:
        """Nested F-test: ``other`` is the smaller model (fewer columns, same y)."""
        q = self.p - other.p
        f = ((other.rss - self.rss) / q) / (self.rss / self.df)
        return {"F": float(f), "df1": q, "df2": self.df, "p": float(stats.f.sf(f, q, self.df))}


def fit(X, y) -> Fit:
    X = np.asarray(X, float)
    y = np.asarray(y, float)
    n, p = X.shape
    Q, R = np.linalg.qr(X)
    coef = np.linalg.solve(R, Q.T @ y)
    fitted = X @ coef
    Rinv = np.linalg.inv(R)
    XtX_inv = Rinv @ Rinv.T
    lev = (Q ** 2).sum(1)
    return Fit(X=X, y=y, coef=coef, resid=y - fitted, fitted=fitted, XtX_inv=XtX_inv, n=n, p=p, leverage=lev)


def vif(X) -> np.ndarray:
    """Variance inflation factors 1/(1 - R_j^2) for each non-intercept column (X has the intercept first)."""
    X = np.asarray(X, float)
    out = []
    for j in range(1, X.shape[1]):
        others = np.delete(X, j, axis=1)
        out.append(1 / (1 - fit(others, X[:, j]).r2))
    return np.asarray(out)


def lad(x, y, iters: int = 200):
    """Least absolute deviations line (Boscovich 1757, Laplace) by iteratively reweighted least squares."""
    X = design(x)
    b = fit(X, y).coef
    for _ in range(iters):
        w = 1 / np.maximum(np.abs(y - X @ b), 1e-8)
        Xw = X * w[:, None]
        b_new = np.linalg.solve(X.T @ Xw, Xw.T @ y)
        if np.max(np.abs(b_new - b)) < 1e-10:
            break
        b = b_new
    return b


# ----------------------------------------------------------------------------------------------------------------
# Part 23: the linear model in depth
# ----------------------------------------------------------------------------------------------------------------

def normal_equations(X, y, dtype=np.float64) -> dict:
    """Solve X'X b = X'y in the given precision: Cholesky if X'X looks positive definite in that precision, else
    Gaussian elimination (what many 1960s programs did).  Returns the coefficients and which route was taken."""
    X, y = np.asarray(X, dtype), np.asarray(y, dtype)
    A, c = X.T @ X, X.T @ y
    try:
        L = np.linalg.cholesky(A)
        b = np.linalg.solve(L.T, np.linalg.solve(L, c))
        route = "cholesky"
    except np.linalg.LinAlgError:
        b = np.linalg.solve(A, c)
        route = "elimination"
    return {"coef": np.asarray(b, np.float64), "route": route}


def qr_solve(X, y, dtype=np.float64) -> np.ndarray:
    """Least squares by Householder QR in the given precision."""
    X, y = np.asarray(X, dtype), np.asarray(y, dtype)
    Q, R = np.linalg.qr(X)
    return np.asarray(np.linalg.solve(R, Q.T @ y), np.float64)


def correct_digits(estimate, truth) -> np.ndarray:
    """The number of correct significant digits, -log10 |relative error| (capped at 15), as in NIST's StRD."""
    est, tru = np.asarray(estimate, float), np.asarray(truth, float)
    rel = np.abs(est - tru) / np.abs(tru)
    return np.clip(-np.log10(np.maximum(rel, 1e-15)), 0, 15)


def householder(X) -> dict:
    """Householder QR written out: the reflections that zero each column below the diagonal, one at a time.
    Returns R, the reflection vectors and the matrix after each step (for drawing)."""
    A = np.asarray(X, float).copy()
    n, p = A.shape
    vs, steps = [], [A.copy()]
    for k in range(p):
        x = A[k:, k]
        alpha = -np.copysign(np.linalg.norm(x), x[0] if x[0] != 0 else 1.0)
        v = x.copy()
        v[0] -= alpha
        v /= np.linalg.norm(v)
        A[k:, k:] -= 2 * np.outer(v, v @ A[k:, k:])
        vs.append(v)
        steps.append(A.copy())
    return {"R": np.triu(A[:p]), "v": vs, "steps": steps}


def glh(f: Fit, C, d=None) -> dict:
    """The general linear hypothesis C b = d: F = (Cb - d)'[C (X'X)^-1 C']^-1 (Cb - d) / (q s^2) on (q, n - p) df."""
    C = np.atleast_2d(np.asarray(C, float))
    d = np.zeros(C.shape[0]) if d is None else np.asarray(d, float)
    r = C @ f.coef - d
    q = C.shape[0]
    F = float(r @ np.linalg.solve(C @ f.XtX_inv @ C.T, r) / (q * f.sigma2))
    return {"F": F, "df1": q, "df2": f.df, "p": float(stats.f.sf(F, q, f.df)), "diff": r}


def gls(X, y, Omega) -> Fit:
    """Aitken's (1935) generalized least squares: whiten by the Cholesky factor of Omega (Var e = sigma^2 Omega) and
    run OLS.  The returned fit is on the whitened scale (its coef and XtX_inv are the GLS ones)."""
    L = np.linalg.cholesky(np.asarray(Omega, float))
    return fit(np.linalg.solve(L, X), np.linalg.solve(L, y))


def ar1_omega(n: int, rho: float) -> np.ndarray:
    i = np.arange(n)
    return rho ** np.abs(i[:, None] - i[None, :]) / (1 - rho ** 2)


def prais_winsten(X, y, iters: int = 20) -> dict:
    """Feasible GLS for AR(1) errors: estimate rho from the OLS (then GLS) residuals and refit, keeping the first
    observation scaled by sqrt(1 - rho^2) (Prais & Winsten 1954)."""
    X, y = np.asarray(X, float), np.asarray(y, float)
    b = fit(X, y).coef
    rho = 0.0
    for _ in range(iters):
        e = y - X @ b
        rho_new = float(np.sum(e[1:] * e[:-1]) / np.sum(e[:-1] ** 2))
        s = np.sqrt(1 - rho_new ** 2)
        Xs = np.vstack([s * X[:1], X[1:] - rho_new * X[:-1]])
        ys = np.concatenate([s * y[:1], y[1:] - rho_new * y[:-1]])
        f = fit(Xs, ys)
        b = f.coef
        if abs(rho_new - rho) < 1e-10:
            break
        rho = rho_new
    return {"fit": f, "rho": rho_new, "coef": b}


def hac_cov(f: Fit, lags: int) -> np.ndarray:
    """Newey-West (1987) covariance with Bartlett weights."""
    U = f.X * f.resid[:, None]
    S = U.T @ U
    for L in range(1, lags + 1):
        w = 1 - L / (lags + 1)
        G = U[L:].T @ U[:-L]
        S += w * (G + G.T)
    return f.XtX_inv @ S @ f.XtX_inv


def cluster_cov(f: Fit, groups, kind: str = "CR1") -> np.ndarray:
    """Cluster-robust covariance (Liang & Zeger 1986; Arellano 1987): sum the scores within each cluster first.
    CR1 applies the small-sample factor G/(G-1) (n-1)/(n-p); CR0 none."""
    groups = np.asarray(groups)
    labels, idx = np.unique(groups, return_inverse=True)
    G = len(labels)
    U = np.zeros((G, f.p))
    np.add.at(U, idx, f.X * f.resid[:, None])
    V = f.XtX_inv @ (U.T @ U) @ f.XtX_inv
    if kind == "CR1":
        V = V * G / (G - 1) * (f.n - 1) / (f.n - f.p)
    elif kind != "CR0":
        raise ValueError(kind)
    return V


def moulton(m_bar: float, rho_x: float, rho_e: float) -> float:
    """Moulton's (1986) variance inflation of the iid OLS variance: 1 + (m - 1) rho_x rho_e."""
    return 1 + (m_bar - 1) * rho_x * rho_e


def icc(y, groups) -> float:
    """One-way ANOVA estimate of the intraclass correlation (unequal sizes, the usual n0 adjustment)."""
    y, groups = np.asarray(y, float), np.asarray(groups)
    labels, idx = np.unique(groups, return_inverse=True)
    G = len(labels)
    m = np.bincount(idx).astype(float)
    means = np.bincount(idx, y) / m
    N = len(y)
    msb = np.sum(m * (means - y.mean()) ** 2) / (G - 1)
    msw = np.sum((y - means[idx]) ** 2) / (N - G)
    n0 = (N - np.sum(m ** 2) / N) / (G - 1)
    s2b = max((msb - msw) / n0, 0.0)
    return float(s2b / (s2b + msw))


WEBB = np.array([-np.sqrt(1.5), -1.0, -np.sqrt(0.5), np.sqrt(0.5), 1.0, np.sqrt(1.5)])


def wild_cluster_boot(X, y, groups, j: int, b0: float = 0.0, R: int = 999, weights: str = "webb", g=None) -> dict:
    """The restricted wild cluster bootstrap-t (Cameron, Gelbach & Miller 2008) for H0: beta_j = b0.  Fit under the
    null, flip each cluster's residuals by one weight (Rademacher or Webb's six-point), refit, and compare the
    CR1 t-statistics.  Returns the observed t and the symmetric bootstrap p-value."""
    X, y = np.asarray(X, float), np.asarray(y, float)
    groups = np.asarray(groups)
    g = np.random.default_rng(0) if g is None else g
    labels, idx = np.unique(groups, return_inverse=True)
    G = len(labels)
    f = fit(X, y)
    t_obs = (f.coef[j] - b0) / np.sqrt(cluster_cov(f, groups)[j, j])
    Xr = np.delete(X, j, axis=1)
    yr = y - b0 * X[:, j]
    fr = fit(Xr, yr)
    base, er = y - fr.resid, fr.resid  # the restricted fitted values (including b0 x_j) and residuals
    Q, Rm = np.linalg.qr(X)
    Rinv = np.linalg.inv(Rm)
    XtX_inv = Rinv @ Rinv.T
    ts = np.empty(R)
    for r in range(R):
        w = (g.choice(WEBB, G) if weights == "webb" else g.choice([-1.0, 1.0], G))[idx]
        ys = base + w * er
        b = np.linalg.solve(Rm, Q.T @ ys)
        e = ys - X @ b
        U = np.zeros((G, X.shape[1]))
        np.add.at(U, idx, X * e[:, None])
        V = XtX_inv @ (U.T @ U) @ XtX_inv * G / (G - 1) * (len(y) - 1) / (len(y) - X.shape[1])
        ts[r] = (b[j] - b0) / np.sqrt(V[j, j])
    p = float(np.mean(np.abs(ts) >= abs(t_obs)))
    return {"t": float(t_obs), "p": p, "t_boot": ts}


def deming(x, y, delta: float = 1.0) -> dict:
    """Deming regression (orthogonal when delta = 1): delta = Var(errors in y) / Var(errors in x)."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    sxx, syy = np.var(x), np.var(y)
    sxy = np.mean((x - x.mean()) * (y - y.mean()))
    b = (syy - delta * sxx + np.sqrt((syy - delta * sxx) ** 2 + 4 * delta * sxy ** 2)) / (2 * sxy)
    return {"slope": float(b), "intercept": float(y.mean() - b * x.mean())}


def tls(X, y) -> np.ndarray:
    """Total least squares by the SVD of [X y]: the smallest right singular vector."""
    Z = np.column_stack([np.asarray(X, float), np.asarray(y, float)])
    v = np.linalg.svd(Z, full_matrices=False)[2][-1]
    return -v[:-1] / v[-1]


def dfbetas(f: Fit) -> np.ndarray:
    """DFBETAS (Belsley, Kuh & Welsch 1980): the change in each coefficient when observation i is deleted, in units
    of its deleted-data SE.  n x p."""
    h = f.leverage
    e = f.resid
    s_del = np.sqrt((f.rss - e ** 2 / (1 - h)) / (f.df - 1))
    delta = (f.XtX_inv @ f.X.T).T * (e / (1 - h))[:, None]  # b - b_(i)
    return delta / (s_del[:, None] * np.sqrt(np.diag(f.XtX_inv))[None, :])


def jackknife_coefs(X, y) -> np.ndarray:
    """Leave-one-out coefficients by the deletion formula (no refits): b_(i) = b - (X'X)^-1 x_i e_i / (1 - h_i)."""
    f = fit(X, y)
    return f.coef[None, :] - (f.XtX_inv @ f.X.T).T * (f.resid / (1 - f.leverage))[:, None]


def truncated_power(x, knots, degree: int = 3) -> np.ndarray:
    """The truncated power basis 1, x, ..., x^d, (x - k)_+^d."""
    x = np.asarray(x, float)
    cols = [x ** j for j in range(degree + 1)] + [np.clip(x - k, 0, None) ** degree for k in knots]
    return np.column_stack(cols)


def bspline_basis(x, knots, degree: int = 3, lo=None, hi=None) -> np.ndarray:
    """B-splines by de Boor's recursion on interior ``knots`` with boundary knots repeated degree + 1 times.
    Columns sum to one: a partition of unity.  len(knots) + degree + 1 columns."""
    x = np.asarray(x, float)
    lo = x.min() if lo is None else lo
    hi = x.max() if hi is None else hi
    t = np.concatenate([[lo] * (degree + 1), np.asarray(knots, float), [hi] * (degree + 1)])
    xx = np.clip(x, lo, hi - 1e-12 * (hi - lo))
    B = np.array([(t[i] <= xx) & (xx < t[i + 1]) for i in range(len(t) - 1)], float).T
    for d in range(1, degree + 1):
        nb = len(t) - d - 1
        new = np.zeros((len(x), nb))
        for i in range(nb):
            a = (xx - t[i]) / (t[i + d] - t[i]) if t[i + d] > t[i] else 0.0
            b = (t[i + d + 1] - xx) / (t[i + d + 1] - t[i + 1]) if t[i + d + 1] > t[i + 1] else 0.0
            new[:, i] = a * B[:, i] + b * B[:, i + 1]
        B = new
    return B


def qreg_se(X, y, tau: float, coef, bandwidth=None) -> np.ndarray:
    """Asymptotic SEs for quantile regression (Koenker & Bassett 1978; Powell's kernel sandwich):
    tau(1 - tau) D^-1 X'X D^-1, with D = sum_i f_i(0) x_i x_i' estimated by a uniform kernel on the residuals."""
    X, y = np.asarray(X, float), np.asarray(y, float)
    n = len(y)
    r = y - X @ np.asarray(coef, float)
    if bandwidth is None:  # Hall & Sheather (1988)
        z = stats.norm.ppf(0.975)
        q = stats.norm.ppf(tau)
        hs = n ** (-1 / 3) * z ** (2 / 3) * (1.5 * stats.norm.pdf(q) ** 2 / (2 * q ** 2 + 1)) ** (1 / 3)
        bandwidth = (stats.norm.ppf(min(tau + hs, 0.999)) - stats.norm.ppf(max(tau - hs, 0.001))) * \
            min(np.std(r), stats.iqr(r) / 1.34)
    k = (np.abs(r) <= bandwidth) / (2 * bandwidth)
    D = (X * k[:, None]).T @ X
    Di = np.linalg.inv(D)
    return np.sqrt(np.diag(tau * (1 - tau) * Di @ (X.T @ X) @ Di))
