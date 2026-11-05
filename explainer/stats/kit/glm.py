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


# ===============================================================================================================
# statkit.glm (II), Part 24: the exponential dispersion family, one IRLS for all, and its extensions
# ===============================================================================================================
@dataclass
class Family:
    """A GLM family: variance function V(mu), link g with inverse and derivative dmu/deta, the unit deviance, and the
    dispersion (fixed at 1 for binomial and Poisson)."""
    name: str
    link: str

    # --- links ---
    def g(self, mu):
        mu = np.asarray(mu, float)
        return {"identity": lambda m: m, "log": np.log, "logit": special.logit, "probit": stats.norm.ppf,
                "cloglog": lambda m: np.log(-np.log1p(-m)), "inverse": lambda m: 1 / m,
                "inverse_squared": lambda m: 1 / m ** 2}[self.link](mu)

    def ginv(self, eta):
        eta = np.asarray(eta, float)
        if self.link == "identity":
            return eta
        if self.link == "log":
            return np.exp(np.minimum(eta, 700))
        if self.link == "logit":
            return special.expit(eta)
        if self.link == "probit":
            return np.clip(stats.norm.cdf(eta), 1e-15, 1 - 1e-15)
        if self.link == "cloglog":
            return np.clip(-np.expm1(-np.exp(np.minimum(eta, 700))), 1e-15, 1 - 1e-15)
        if self.link == "inverse":
            return 1 / eta
        if self.link == "inverse_squared":
            return 1 / np.sqrt(eta)
        raise ValueError(self.link)

    def dmu(self, eta):
        eta = np.asarray(eta, float)
        if self.link == "identity":
            return np.ones_like(eta)
        if self.link == "log":
            return np.exp(np.minimum(eta, 700))
        if self.link == "logit":
            m = special.expit(eta)
            return m * (1 - m)
        if self.link == "probit":
            return np.maximum(stats.norm.pdf(eta), 1e-300)
        if self.link == "cloglog":
            e = np.exp(np.minimum(eta, 700))
            return np.maximum(e * np.exp(-e), 1e-300)
        if self.link == "inverse":
            return -1 / eta ** 2
        if self.link == "inverse_squared":
            return -0.5 * eta ** -1.5
        raise ValueError(self.link)

    # --- variance and deviance ---
    def V(self, mu):
        mu = np.asarray(mu, float)
        return {"gaussian": np.ones_like(mu), "binomial": mu * (1 - mu), "poisson": mu, "gamma": mu ** 2,
                "inverse_gaussian": mu ** 3}[self.name]

    def unit_deviance(self, y, mu, n=1.0):
        y, mu = np.asarray(y, float), np.asarray(mu, float)
        if self.name == "gaussian":
            return (y - mu) ** 2
        if self.name == "poisson":
            return 2 * (np.where(y > 0, y * np.log(np.where(y > 0, y, 1) / mu), 0.0) - (y - mu))
        if self.name == "binomial":  # y is the proportion, n the trials
            a = np.where(y > 0, y * np.log(np.where(y > 0, y, 1) / mu), 0.0)
            b = np.where(y < 1, (1 - y) * np.log(np.where(y < 1, 1 - y, 1) / (1 - mu)), 0.0)
            return 2 * n * (a + b)
        if self.name == "gamma":
            return 2 * (-np.log(y / mu) + (y - mu) / mu)
        if self.name == "inverse_gaussian":
            return (y - mu) ** 2 / (mu ** 2 * y)
        raise ValueError(self.name)

    @property
    def fixed_dispersion(self) -> bool:
        return self.name in ("binomial", "poisson")


CANONICAL = {"gaussian": "identity", "binomial": "logit", "poisson": "log", "gamma": "inverse", "inverse_gaussian": "inverse_squared"}


def family(name: str, link: str | None = None) -> Family:
    return Family(name, link or CANONICAL[name])


@dataclass
class GlmFit:
    fam: Family
    coef: np.ndarray
    X: np.ndarray
    y: np.ndarray  # proportions for binomial
    n: np.ndarray  # trials (binomial) or prior weights
    offset: np.ndarray
    path: list = field(default_factory=list)
    deviance_path: list = field(default_factory=list)

    @property
    def eta(self):
        return self.X @ self.coef + self.offset

    @property
    def mu(self):
        return self.fam.ginv(self.eta)

    @property
    def weights(self):
        """IRLS working weights n (dmu/deta)^2 / V(mu): the expected information per observation (up to phi)."""
        return self.n * self.fam.dmu(self.eta) ** 2 / self.fam.V(self.mu)

    @property
    def deviance(self) -> float:
        return float(np.sum(self.fam.unit_deviance(self.y, self.mu, self.n) * (1 if self.fam.name == "binomial" else self.n)))

    @property
    def null_deviance(self) -> float:
        m0 = np.full_like(self.y, np.sum(self.n * self.y) / np.sum(self.n))
        return float(np.sum(self.fam.unit_deviance(self.y, m0, self.n) * (1 if self.fam.name == "binomial" else self.n)))

    @property
    def df_resid(self) -> int:
        return len(self.y) - len(self.coef)

    @property
    def pearson(self) -> np.ndarray:
        return (self.y - self.mu) * np.sqrt(self.n / self.fam.V(self.mu))

    @property
    def deviance_resid(self) -> np.ndarray:
        d = self.fam.unit_deviance(self.y, self.mu, self.n) * (1 if self.fam.name == "binomial" else self.n)
        return np.sign(self.y - self.mu) * np.sqrt(np.maximum(d, 0))

    @property
    def phi(self) -> float:
        """The dispersion: 1 for binomial and Poisson; otherwise Pearson's estimate."""
        if self.fam.fixed_dispersion:
            return 1.0
        return float(np.sum(self.pearson ** 2) / self.df_resid)

    @property
    def pearson_phi(self) -> float:
        return float(np.sum(self.pearson ** 2) / self.df_resid)

    def cov(self, kind: str = "model"):
        inv = np.linalg.inv(self.X.T @ (self.weights[:, None] * self.X))
        if kind == "model":
            return inv * self.phi
        if kind == "quasi":
            return inv * self.pearson_phi
        if kind == "sandwich":
            u = self.X * ((self.y - self.mu) * self.n * self.fam.dmu(self.eta) / self.fam.V(self.mu))[:, None]
            return inv @ (u.T @ u) @ inv
        raise ValueError(kind)

    def se(self, kind: str = "model"):
        return np.sqrt(np.diag(self.cov(kind)))

    @property
    def loglik_binomial(self) -> float:
        k = self.n * self.y
        m = np.clip(self.mu, 1e-300, 1 - 1e-16)
        return float(np.sum(special.gammaln(self.n + 1) - special.gammaln(k + 1) - special.gammaln(self.n - k + 1)
                            + k * np.log(m) + (self.n - k) * np.log1p(-m)))

    def quantile_resid(self, rng=None) -> np.ndarray:
        """Dunn & Smyth's (1996) randomized quantile residuals: Phi^-1 of a uniform drawn between F(y-) and F(y)
        under the fitted model (continuous families: Phi^-1 F(y)).  Exactly N(0, 1) if the model is right."""
        g = np.random.default_rng(0) if rng is None else rng
        mu = self.mu
        if self.fam.name == "poisson":
            a, b = stats.poisson.cdf(self.y - 1, mu), stats.poisson.cdf(self.y, mu)
        elif self.fam.name == "binomial":
            k = np.round(self.y * self.n)
            a, b = stats.binom.cdf(k - 1, self.n, mu), stats.binom.cdf(k, self.n, mu)
        elif self.fam.name == "gaussian":
            return (self.y - mu) / np.sqrt(self.phi)
        elif self.fam.name == "gamma":
            sh = 1 / self.phi
            return stats.norm.ppf(stats.gamma.cdf(self.y, sh, scale=mu / sh))
        else:
            raise ValueError(self.fam.name)
        u = a + g.random(len(mu)) * (b - a)
        return stats.norm.ppf(np.clip(u, 1e-12, 1 - 1e-12))


def glm_fit(X, y, fam: Family, n=None, offset=None, tol=1e-12, max_iter=100, start=None) -> GlmFit:
    """IRLS for any family and link (Nelder & Wedderburn 1972): Fisher scoring as weighted least squares on the working
    response z = eta + (y - mu) deta/dmu with weights n (dmu/deta)^2 / V(mu).  For binomial, ``y`` are proportions out of
    ``n`` trials.  Records the coefficient path and the deviance at each step; step-halving keeps the deviance falling."""
    X = np.asarray(X, float)
    y = np.asarray(y, float)
    n = np.ones_like(y) if n is None else np.asarray(n, float)
    off = np.zeros_like(y) if offset is None else np.asarray(offset, float)
    if start is None:
        mu0 = (n * y + 0.5) / (n + 1) if fam.name == "binomial" else np.maximum(y, 0.1) if fam.name != "gaussian" else y
        if fam.name == "inverse_gaussian" or fam.name == "gamma":
            mu0 = np.maximum(y, 1e-3)
        eta = fam.g(mu0)
        sw = np.sqrt(n)
        beta = np.linalg.lstsq(sw[:, None] * X, sw * (eta - off), rcond=None)[0]
    else:
        beta = np.asarray(start, float)
    fit = GlmFit(fam, beta, X, y, n, off)
    path, devs = [beta.copy()], [fit.deviance]
    for _ in range(max_iter):
        eta = X @ beta + off
        mu = fam.ginv(eta)
        d = fam.dmu(eta)
        w = np.maximum(n * d ** 2 / fam.V(mu), 1e-12)
        z = eta - off + (y - mu) / d
        sw = np.sqrt(w)
        new = np.linalg.lstsq(sw[:, None] * X, sw * z, rcond=None)[0]
        dev_old = devs[-1]
        for _ in range(40):
            cand = GlmFit(fam, new, X, y, n, off)
            dv = cand.deviance
            if np.isfinite(dv) and dv <= dev_old + 1e-9 * (1 + abs(dev_old)):
                break
            new = (new + beta) / 2
        path.append(new.copy())
        devs.append(dv)
        if np.max(np.abs(new - beta)) < tol * (1 + np.max(np.abs(beta))):
            beta = new
            break
        beta = new
    return GlmFit(fam, beta, X, y, n, off, path, devs)


def ld50(fit: GlmFit, alpha: float = 0.05, p: float = 0.5) -> dict:
    """The dose with response probability p for a fit with intercept and one dose slope: x_p = (g(p) - a) / b, with
    the delta-method SE and Fieller's interval (Part 11)."""
    a, b = fit.coef[:2]
    V = fit.cov()[:2, :2]
    gp = float(fit.fam.g(np.array([p]))[0])
    x = (gp - a) / b
    grad = np.array([-1 / b, -(gp - a) / b ** 2])
    se = float(np.sqrt(grad @ V @ grad))
    z = stats.norm.ppf(1 - alpha / 2)
    # Fieller: solve (gp - a - b x)^2 = z^2 (V_aa + 2x V_ab + x^2 V_bb)
    A = b ** 2 - z ** 2 * V[1, 1]
    B = -2 * (b * (gp - a) + z ** 2 * V[0, 1])
    C = (gp - a) ** 2 - z ** 2 * V[0, 0]
    disc = B ** 2 - 4 * A * C
    fl = tuple(sorted(((-B - np.sqrt(disc)) / (2 * A), (-B + np.sqrt(disc)) / (2 * A)))) if A > 0 and disc > 0 else (-np.inf, np.inf)
    return {"x": float(x), "se": se, "wald": (x - z * se, x + z * se), "fieller": (float(fl[0]), float(fl[1]))}


def firth_logistic(X, y, tol=1e-10, max_iter=200) -> dict:
    """Firth's (1993) penalized logistic regression: maximize l(b) + (1/2) log det I(b).  Finite even under separation.
    Newton on the modified score U* = X'(y - p + h (1/2 - p)), h the hat values of the weighted design."""
    X, y = np.asarray(X, float), np.asarray(y, float)
    b = np.zeros(X.shape[1])
    path = [b.copy()]
    for _ in range(max_iter):
        p = special.expit(X @ b)
        w = p * (1 - p)
        I = X.T @ (w[:, None] * X)
        Ii = np.linalg.inv(I)
        h = np.einsum("ij,jk,ik->i", X, Ii, X) * w
        U = X.T @ (y - p + h * (0.5 - p))
        step = Ii @ U
        b = b + step
        path.append(b.copy())
        if np.max(np.abs(step)) < tol:
            break
    p = special.expit(X @ b)
    I = X.T @ ((p * (1 - p))[:, None] * X)
    return {"coef": b, "se": np.sqrt(np.diag(np.linalg.inv(I))), "path": np.array(path)}


def logistic_path_separated(X, y, iters=30) -> dict:
    """Plain IRLS on separated data: the log likelihood keeps rising and the slope keeps growing (Albert & Anderson
    1984).  Returns the slope and log likelihood at each step (no step-halving, no convergence)."""
    X, y = np.asarray(X, float), np.asarray(y, float)
    b = np.zeros(X.shape[1])
    slopes, lls = [], []
    for _ in range(iters):
        eta = X @ b
        p = special.expit(eta)
        w = np.maximum(p * (1 - p), 1e-300)
        b = b + np.linalg.solve(X.T @ (w[:, None] * X) + 1e-300 * np.eye(len(b)), X.T @ (y - p))
        eta = X @ b
        slopes.append(float(b[-1]))
        lls.append(float(np.sum(y * eta - np.logaddexp(0, eta))))
    return {"slope": slopes, "loglik": lls}


def negbin_fit(X, y, offset=None, tol=1e-10, max_iter=100) -> dict:
    """Negative binomial regression NB2 (Var = mu + mu^2/k) by alternating IRLS for beta (fixed k) and Newton for log k
    (the profile score in k).  Returns beta, k, model SEs and the log likelihood."""
    X, y = np.asarray(X, float), np.asarray(y, float)
    off = np.zeros_like(y) if offset is None else np.asarray(offset, float)
    b = glm_fit(X, y, family("poisson"), offset=off).coef
    k = 1.0

    def ll_k(lk, mu):
        kk = np.exp(lk)
        return float(np.sum(special.gammaln(y + kk) - special.gammaln(kk) - special.gammaln(y + 1)
                            + kk * np.log(kk / (kk + mu)) + y * np.log(mu / (kk + mu))))

    for _ in range(max_iter):
        mu = np.exp(X @ b + off)
        lk = optimize.minimize_scalar(lambda t: -ll_k(t, mu), bounds=(-10, 15), method="bounded").x
        k = float(np.exp(lk))
        b_old = b
        for _ in range(50):  # IRLS for beta with Var = mu + mu^2/k, log link
            eta = X @ b + off
            mu = np.exp(eta)
            w = mu ** 2 / (mu + mu ** 2 / k)
            z = eta - off + (y - mu) / mu
            sw = np.sqrt(w)
            nb = np.linalg.lstsq(sw[:, None] * X, sw * z, rcond=None)[0]
            if np.max(np.abs(nb - b)) < tol:
                b = nb
                break
            b = nb
        if np.max(np.abs(b - b_old)) < 1e-9:
            break
    mu = np.exp(X @ b + off)
    w = mu ** 2 / (mu + mu ** 2 / k)
    cov = np.linalg.inv(X.T @ (w[:, None] * X))
    return {"coef": b, "k": k, "se": np.sqrt(np.diag(cov)), "loglik": ll_k(np.log(k), mu), "mu": mu}


def zip_em(X, y, Z=None, iters=500, tol=1e-10) -> dict:
    """Zero-inflated Poisson (Lambert 1992) by EM: a structural zero with probability pi = expit(Z gamma), else
    Poisson(exp(X beta)).  E-step: each zero's chance of being structural; M-step: a weighted logistic and a weighted
    Poisson regression.  The log likelihood never falls (Part 22)."""
    X, y = np.asarray(X, float), np.asarray(y, float)
    Z = np.ones((len(y), 1)) if Z is None else np.asarray(Z, float)
    b = glm_fit(X, y, family("poisson")).coef
    gmm = np.zeros(Z.shape[1])
    lls = []
    for _ in range(iters):
        lam = np.exp(X @ b)
        pi = special.expit(Z @ gmm)
        zero = y == 0
        r = np.where(zero, pi / (pi + (1 - pi) * np.exp(-lam)), 0.0)
        # M-step: logistic for r on Z (fractional responses), Poisson for y with weights 1 - r
        gmm = glm_fit(Z, r, family("binomial"), start=gmm).coef
        b = glm_fit(X, y, family("poisson"), n=np.maximum(1 - r, 1e-12), start=b).coef
        lam = np.exp(X @ b)
        pi = special.expit(Z @ gmm)
        ll = float(np.sum(np.where(zero, np.log(pi + (1 - pi) * np.exp(-lam)),
                                   np.log1p(-pi) + stats.poisson.logpmf(y, lam))))
        lls.append(ll)
        if len(lls) > 1 and abs(lls[-1] - lls[-2]) < tol:
            break
    return {"beta": b, "gamma": gmm, "loglik": lls[-1], "path": lls, "pi": special.expit(Z @ gmm)}


def hurdle(X, y) -> dict:
    """A Poisson hurdle model (Mullahy 1986): a logistic regression for y > 0, and a zero-truncated Poisson for the
    positive counts (fitted by Newton on its likelihood)."""
    X, y = np.asarray(X, float), np.asarray(y, float)
    pos = y > 0
    zero_part = glm_fit(X, pos.astype(float), family("binomial"))
    Xp, yp = X[pos], y[pos]

    def nll(b):
        lam = np.exp(Xp @ b)
        return -float(np.sum(yp * np.log(lam) - lam - np.log(-np.expm1(-lam)) - special.gammaln(yp + 1)))

    b = optimize.minimize(nll, glm_fit(Xp, yp, family("poisson")).coef, method="BFGS").x
    return {"zero": zero_part.coef, "count": b, "loglik": float(zero_part.loglik_binomial - nll(b))}


def multinomial_logit(X, Y, iters=100, tol=1e-10) -> dict:
    """Baseline-category logits: Y is n x K (one-hot or counts), category 0 the baseline.  Newton on the stacked
    coefficients (K - 1 columns of p each)."""
    X, Y = np.asarray(X, float), np.asarray(Y, float)
    n, p = X.shape
    K = Y.shape[1]
    B = np.zeros((p, K - 1))
    m = Y.sum(1)
    for _ in range(iters):
        E = np.column_stack([np.zeros(n), X @ B])
        P = special.softmax(E, axis=1)
        g = (X.T @ (Y[:, 1:] - m[:, None] * P[:, 1:])).ravel(order="F")
        H = np.zeros((p * (K - 1), p * (K - 1)))
        for a in range(K - 1):
            for c in range(K - 1):
                w = m * P[:, a + 1] * ((a == c) - P[:, c + 1])
                H[a * p:(a + 1) * p, c * p:(c + 1) * p] = X.T @ (w[:, None] * X)
        step = np.linalg.solve(H, g)
        B = B + step.reshape((p, K - 1), order="F")
        if np.max(np.abs(step)) < tol:
            break
    cov = np.linalg.inv(H)
    return {"coef": B, "se": np.sqrt(np.diag(cov)).reshape((p, K - 1), order="F"), "probs": P}


def proportional_odds(X, y, K: int) -> dict:
    """McCullagh's (1980) proportional-odds model: P(y <= j) = expit(theta_j - x'beta), j = 0..K-2, X without an
    intercept.  Maximum likelihood by BFGS on (theta increments, beta), then the observed information."""
    X, y = np.asarray(X, float), np.asarray(y, int)
    p = X.shape[1]

    def unpack(par):
        th = np.cumsum(np.concatenate([[par[0]], np.exp(par[1:K - 1])]))
        return th, par[K - 1:]

    def nll(par):
        th, b = unpack(par)
        e = X @ b
        cdf = np.column_stack([np.zeros(len(y)), special.expit(th[None, :] - e[:, None]), np.ones(len(y))])
        pr = cdf[np.arange(len(y)), y + 1] - cdf[np.arange(len(y)), y]
        return -float(np.sum(np.log(np.maximum(pr, 1e-300))))

    par0 = np.concatenate([[-1.0], np.zeros(K - 2), np.zeros(p)])
    r = optimize.minimize(nll, par0, method="BFGS", options={"gtol": 1e-8})
    th, b = unpack(r.x)

    def nll2(q):  # in (theta, beta) directly, for the information
        th_, b_ = q[:K - 1], q[K - 1:]
        e = X @ b_
        cdf = np.column_stack([np.zeros(len(y)), special.expit(th_[None, :] - e[:, None]), np.ones(len(y))])
        pr = cdf[np.arange(len(y)), y + 1] - cdf[np.arange(len(y)), y]
        return -float(np.sum(np.log(np.maximum(pr, 1e-300))))

    from explainer.stats.kit.mle import numerical_hessian
    q = np.concatenate([th, b])
    H = numerical_hessian(lambda t: -nll2(t), q, h=1e-4)
    se = np.sqrt(np.diag(np.linalg.inv(-H)))
    return {"theta": th, "beta": b, "se_theta": se[:K - 1], "se_beta": se[K - 1:], "loglik": -r.fun}


def gee_logistic(X, y, groups, corstr: str = "exchangeable", iters=50, tol=1e-10) -> dict:
    """Liang & Zeger's (1986) GEE for a binary outcome with a logit link: solve sum_g D_g' V_g^-1 (y_g - mu_g) = 0 with
    a working correlation (independence or exchangeable, alpha by moments), and report the model-based and the robust
    (sandwich) covariance."""
    X, y = np.asarray(X, float), np.asarray(y, float)
    groups = np.asarray(groups)
    labels, idx = np.unique(groups, return_inverse=True)
    members = [np.flatnonzero(idx == g) for g in range(len(labels))]
    b = glm_fit(X, y, family("binomial")).coef
    alpha = 0.0
    for _ in range(iters):
        mu = special.expit(X @ b)
        v = mu * (1 - mu)
        r = (y - mu) / np.sqrt(v)
        if corstr == "exchangeable":
            num = sum((r[m].sum() ** 2 - (r[m] ** 2).sum()) for m in members)
            den = sum(len(m) * (len(m) - 1) for m in members)
            phi = float(np.sum(r ** 2) / (len(y) - X.shape[1]))
            alpha = float(num / den / phi)
        A = np.zeros((X.shape[1], X.shape[1]))
        U = np.zeros(X.shape[1])
        for m in members:
            k = len(m)
            R = (1 - alpha) * np.eye(k) + alpha * np.ones((k, k))
            sv = np.sqrt(v[m])
            Vi = np.linalg.inv(sv[:, None] * R * sv[None, :])
            D = X[m] * v[m][:, None]
            A += D.T @ Vi @ D
            U += D.T @ Vi @ (y[m] - mu[m])
        step = np.linalg.solve(A, U)
        b = b + step
        if np.max(np.abs(step)) < tol:
            break
    mu = special.expit(X @ b)
    v = mu * (1 - mu)
    A = np.zeros((X.shape[1], X.shape[1]))
    M = np.zeros_like(A)
    for m in members:
        k = len(m)
        R = (1 - alpha) * np.eye(k) + alpha * np.ones((k, k))
        sv = np.sqrt(v[m])
        Vi = np.linalg.inv(sv[:, None] * R * sv[None, :])
        D = X[m] * v[m][:, None]
        A += D.T @ Vi @ D
        s = D.T @ Vi @ (y[m] - mu[m])
        M += np.outer(s, s)
    Ai = np.linalg.inv(A)
    return {"coef": b, "alpha": alpha, "se_model": np.sqrt(np.diag(Ai)), "se_robust": np.sqrt(np.diag(Ai @ M @ Ai))}


def log_score(p, y) -> float:
    """Mean negative log probability of what happened (binary): the logarithmic scoring rule (Good 1952)."""
    p, y = np.clip(np.asarray(p, float), 1e-15, 1 - 1e-15), np.asarray(y, float)
    return float(-np.mean(y * np.log(p) + (1 - y) * np.log(1 - p)))


def crps_normal(mu, sigma, y) -> np.ndarray:
    """The continuous ranked probability score of a N(mu, sigma^2) forecast for outcome y (Gneiting & Raftery 2007)."""
    z = (np.asarray(y, float) - mu) / sigma
    return sigma * (z * (2 * stats.norm.cdf(z) - 1) + 2 * stats.norm.pdf(z) - 1 / np.sqrt(np.pi))
