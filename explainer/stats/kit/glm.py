"""statkit.glm (I): logistic and Poisson regression, and the tables they replace (Part 14 of *Statistics, Built*).

    from explainer.stats.kit.glm import logistic, poisson, profile_ci, table2x2, cmh, roc, brier

Both models are fitted by iteratively reweighted least squares, Newton's method written as a sequence of weighted
regressions (theory in Part 24).  ``Glm`` carries the coefficients, their classical and sandwich covariances, the
deviance and each IRLS step, so a scene can draw the iterations.  Everything is checked against statsmodels and SciPy
in ``tests/test_stats_kit_glm.py``.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from scipy import optimize, special, stats


@dataclass
class Glm:
    family: str
    coef: np.ndarray
    X: np.ndarray
    y: np.ndarray
    n_trials: np.ndarray
    offset: np.ndarray
    path: list = field(default_factory=list)

    @property
    def eta(self):
        return self.X @ self.coef + self.offset

    @property
    def mu(self):
        """Fitted means: probabilities (logistic, per trial) or counts (Poisson)."""
        if self.family == "binomial":
            return special.expit(self.eta)
        return np.exp(self.eta)

    def _w(self):
        m = self.mu
        return self.n_trials * m * (1 - m) if self.family == "binomial" else m

    @property
    def fisher_info(self):
        return self.X.T @ (self._w()[:, None] * self.X)

    def cov(self, kind: str = "classical", dispersion: float | None = None):
        inv = np.linalg.inv(self.fisher_info)
        if kind == "classical":
            return inv * (1.0 if dispersion is None else dispersion)
        if kind == "quasi":
            return inv * self.pearson_dispersion
        if kind == "sandwich":
            r = self.y - self._expected()
            meat = self.X.T @ ((r ** 2)[:, None] * self.X)
            return inv @ meat @ inv
        raise ValueError(kind)

    def se(self, kind: str = "classical"):
        return np.sqrt(np.diag(self.cov(kind)))

    def wald_ci(self, alpha: float = 0.05, kind: str = "classical"):
        z = stats.norm.ppf(1 - alpha / 2)
        s = self.se(kind)
        return np.column_stack([self.coef - z * s, self.coef + z * s])

    def _expected(self):
        return self.n_trials * self.mu if self.family == "binomial" else self.mu

    @property
    def loglik(self):
        if self.family == "binomial":
            m = np.clip(self.mu, 1e-300, 1 - 1e-16)
            return float(np.sum(special.gammaln(self.n_trials + 1) - special.gammaln(self.y + 1) - special.gammaln(self.n_trials - self.y + 1)
                                + self.y * np.log(m) + (self.n_trials - self.y) * np.log1p(-m)))
        m = self.mu
        return float(np.sum(self.y * np.log(m) - m - special.gammaln(self.y + 1)))

    @property
    def deviance(self):
        y, e = self.y, self._expected()
        if self.family == "binomial":
            n = self.n_trials
            t1 = np.where(y > 0, y * np.log(np.where(y > 0, y, 1) / e), 0.0)
            t2 = np.where(n - y > 0, (n - y) * np.log(np.where(n - y > 0, n - y, 1) / (n - e)), 0.0)
            return float(2 * np.sum(t1 + t2))
        t = np.where(y > 0, y * np.log(np.where(y > 0, y, 1) / e), 0.0)
        return float(2 * np.sum(t - (y - e)))

    @property
    def pearson_dispersion(self):
        e = self._expected()
        v = self.n_trials * self.mu * (1 - self.mu) if self.family == "binomial" else e
        return float(np.sum((self.y - e) ** 2 / v) / (len(self.y) - len(self.coef)))

    def predict(self, X0, offset=0.0):
        eta = np.asarray(X0) @ self.coef + offset
        return special.expit(eta) if self.family == "binomial" else np.exp(eta)

    def predict_ci(self, X0, alpha=0.05, kind="classical"):
        """Wald interval on the linear-predictor scale, mapped through the inverse link."""
        X0 = np.atleast_2d(X0)
        eta = X0 @ self.coef
        se = np.sqrt(np.einsum("ij,jk,ik->i", X0, self.cov(kind), X0))
        z = stats.norm.ppf(1 - alpha / 2)
        f = special.expit if self.family == "binomial" else np.exp
        return f(eta - z * se), f(eta), f(eta + z * se)


def _loglik(family, eta, y, n):
    """The log-likelihood up to a constant that does not depend on the coefficients."""
    if family == "binomial":
        return float(np.sum(y * eta - n * np.logaddexp(0.0, eta)))
    return float(np.sum(y * eta - np.exp(np.minimum(eta, 700))))


def _irls(X, y, family, n_trials=None, offset=None, tol=1e-10, max_iter=50, start=None):
    X = np.asarray(X, float)
    y = np.asarray(y, float)
    n = np.ones_like(y) if n_trials is None else np.asarray(n_trials, float)
    off = np.zeros_like(y) if offset is None else np.asarray(offset, float)
    beta = np.zeros(X.shape[1]) if start is None else np.asarray(start, float)
    path = [beta.copy()]
    for _ in range(max_iter):
        eta = X @ beta + off
        if family == "binomial":
            mu = special.expit(eta)
            w = np.maximum(n * mu * (1 - mu), 1e-9)  # floored, so a far-off start still gives a usable direction
            z = eta - off + (y - n * mu) / w
        else:
            mu = np.exp(eta)
            w = mu
            z = eta - off + (y - mu) / mu
        sw = np.sqrt(w)
        new = np.linalg.lstsq(sw[:, None] * X, sw * z, rcond=None)[0]
        # step-halving: a Newton step that lowers the likelihood is shortened until it does not (far from the optimum)
        ll_old = _loglik(family, X @ beta + off, y, n)
        for _ in range(40):
            if _loglik(family, X @ new + off, y, n) >= ll_old - 1e-10:
                break
            new = (new + beta) / 2
        path.append(new.copy())
        if np.max(np.abs(new - beta)) < tol * (1 + np.max(np.abs(beta))):
            beta = new
            break
        beta = new
    return Glm(family, beta, X, y, n, off, path)


def logistic(X, y, n_trials=None, **kw) -> Glm:
    """Logistic regression of successes ``y`` (out of ``n_trials``, default 1) on the design ``X``."""
    return _irls(X, y, "binomial", n_trials=n_trials, **kw)


def poisson(X, y, offset=None, **kw) -> Glm:
    """Poisson regression of counts ``y`` on ``X`` with a log-exposure ``offset``."""
    return _irls(X, y, "poisson", offset=offset, **kw)


def _constrained_loglik(fit: Glm, x0, eta0, start=None):
    """The maximum log-likelihood subject to x0' beta = eta0: write beta = eta0 x0/|x0|^2 + N gamma, with N an
    orthonormal basis of x0's complement, and fit gamma by IRLS with the constrained part as an offset."""
    x0 = np.asarray(x0, float)
    q = x0 / (x0 @ x0)
    _, _, vt = np.linalg.svd(x0[None, :])
    N = vt[1:].T
    off = fit.offset + eta0 * (fit.X @ q)
    g0 = N.T @ (fit.coef if start is None else start)
    sub = _irls(fit.X @ N, fit.y, fit.family, n_trials=fit.n_trials, offset=off, start=g0, max_iter=200)
    beta = eta0 * q + N @ sub.coef
    return Glm(fit.family, beta, fit.X, fit.y, fit.n_trials, fit.offset).loglik, beta


def profile_ci(fit: Glm, x0, alpha: float = 0.05):
    """Profile-likelihood interval for the linear predictor at ``x0`` (so for p(x0) after the inverse link): the set of
    values eta0 whose constrained maximum log-likelihood is within chi2_1(1 - alpha)/2 of the maximum.  Returns
    (lower, estimate, upper); an end is infinite if the profile never falls that far (as near separation)."""
    x0 = np.asarray(x0, float)
    crit = stats.chi2.ppf(1 - alpha, 1) / 2
    ll_max = fit.loglik
    eta_hat = float(x0 @ fit.coef)
    se = float(np.sqrt(x0 @ fit.cov() @ x0))
    warm = {"beta": fit.coef.copy()}

    def f(e):
        ll, beta = _constrained_loglik(fit, x0, e, start=warm["beta"])
        warm["beta"] = beta  # continuation: start the next constrained fit from this one
        return ll_max - ll - crit

    def edge(direction):
        warm["beta"] = fit.coef.copy()
        step = max(se, 1e-3)
        a, b = eta_hat, eta_hat + direction * step
        for _ in range(60):
            if f(b) > 0:
                return optimize.brentq(f, min(a, b), max(a, b))
            a, step = b, step * 1.6
            b = a + direction * step
        return direction * np.inf

    return edge(-1), eta_hat, edge(+1)


def profile_coef_ci(fit: Glm, j: int, alpha: float = 0.05):
    x0 = np.zeros(len(fit.coef))
    x0[j] = 1.0
    return profile_ci(fit, x0, alpha)


# ---------------------------------------------------------------------------------------------------------------
# Tables
# ---------------------------------------------------------------------------------------------------------------
def table2x2(a, b, c, d, alpha=0.05) -> dict:
    """[[a, b], [c, d]], rows exposed / unexposed, columns event / no event: odds ratio with Woolf's interval, relative
    risk with Katz's, Pearson's chi-squared (no continuity correction) and Fisher's exact test."""
    a, b, c, d = map(float, (a, b, c, d))
    z = stats.norm.ppf(1 - alpha / 2)
    orr = (a * d) / (b * c)
    se_lor = np.sqrt(1 / a + 1 / b + 1 / c + 1 / d)
    rr = (a / (a + b)) / (c / (c + d))
    se_lrr = np.sqrt(1 / a - 1 / (a + b) + 1 / c - 1 / (c + d))
    chi = stats.chi2_contingency([[a, b], [c, d]], correction=False)
    fe = stats.fisher_exact([[int(a), int(b)], [int(c), int(d)]])
    return {"or": orr, "or_ci": (orr * np.exp(-z * se_lor), orr * np.exp(z * se_lor)), "rr": rr,
            "rr_ci": (rr * np.exp(-z * se_lrr), rr * np.exp(z * se_lrr)), "chi2": float(chi.statistic), "p_chi2": float(chi.pvalue),
            "p_fisher": float(fe.pvalue), "p1": a / (a + b), "p2": c / (c + d)}


def cmh(tables) -> dict:
    """Cochran-Mantel-Haenszel for K strata of 2x2 tables [[a, b], [c, d]]: the Mantel-Haenszel common odds ratio and
    the CMH chi-squared statistic (no continuity correction)."""
    t = np.asarray(tables, float)
    a, b, c, d = t[:, 0, 0], t[:, 0, 1], t[:, 1, 0], t[:, 1, 1]
    n = a + b + c + d
    or_mh = float(np.sum(a * d / n) / np.sum(b * c / n))
    ea = (a + b) * (a + c) / n
    va = (a + b) * (c + d) * (a + c) * (b + d) / (n ** 2 * (n - 1))
    chi = float((np.sum(a - ea)) ** 2 / np.sum(va))
    return {"or_mh": or_mh, "chi2": chi, "p": float(stats.chi2.sf(chi, 1)), "strata_or": (a * d / (b * c)).tolist()}


# ---------------------------------------------------------------------------------------------------------------
# Scoring probabilistic predictions
# ---------------------------------------------------------------------------------------------------------------
def roc(scores, labels):
    """ROC curve (false-positive rate, true-positive rate) and the AUC (the Mann-Whitney probability)."""
    s = np.asarray(scores, float)
    yv = np.asarray(labels, bool)
    order = np.argsort(-s, kind="mergesort")
    s, yv = s[order], yv[order]
    tps = np.cumsum(yv)
    fps = np.cumsum(~yv)
    keep = np.r_[np.diff(s) != 0, True]
    tpr = np.r_[0, tps[keep] / yv.sum()]
    fpr = np.r_[0, fps[keep] / (~yv).sum()]
    auc = float(np.trapezoid(tpr, fpr))
    return fpr, tpr, auc


def brier(p, labels) -> float:
    return float(np.mean((np.asarray(p, float) - np.asarray(labels, float)) ** 2))


def calibration(p, labels, bins=10):
    """Mean predicted vs observed frequency in ``bins`` quantile bins of the predictions."""
    p = np.asarray(p, float)
    yv = np.asarray(labels, float)
    edges = np.quantile(p, np.linspace(0, 1, bins + 1))
    idx = np.clip(np.searchsorted(edges, p, side="right") - 1, 0, bins - 1)
    pred = np.array([p[idx == k].mean() for k in range(bins)])
    obs = np.array([yv[idx == k].mean() for k in range(bins)])
    cnt = np.array([(idx == k).sum() for k in range(bins)])
    return pred, obs, cnt
