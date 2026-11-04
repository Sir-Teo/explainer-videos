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
