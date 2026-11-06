"""statkit.semipar: semiparametric efficiency (Part 49 of *Statistics, Built*).

Small, exact where possible, and checked in ``tests/test_stats_kit_semipar.py``:

* the geometry of a finite sample space: L2_0(p), projections, scores of submodels, pathwise derivatives, efficient
  influence functions as projections of any gradient onto the tangent space, and the efficiency bound;
* a worked restricted model: two binary variables assumed independent, whose tangent space is {a(x1) + b(x2)};
* adaptive estimation of the centre of a symmetric law (Stein 1956; Stone 1975): an estimated score by a symmetrized
  kernel density, a one-step update, and the Fisher informations it should reach;
* the ATE: plug-in, IPW, one-step (AIPW) and TMLE, with influence-function standard errors;
* the product-rate experiment: nuisances corrupted at chosen rates n^-a and n^-b, and the one-step's bias;
* a mean under MAR: complete cases, IPW, regression and AIPW, with correct or wrong working models;
* the integrated squared density: plug-in, first-order one-step and the second-order U-statistic.
"""

from __future__ import annotations

import math

import numpy as np
from scipy import integrate, stats

# -------------------------------------------------------------------------------------------- discrete geometry


def inner(p, a, b) -> float:
    p, a, b = (np.asarray(v, float) for v in (p, a, b))
    return float(np.sum(p * a * b))


def center(p, a) -> np.ndarray:
    a = np.asarray(a, float)
    return a - np.sum(np.asarray(p, float) * a)


def project(p, v, basis) -> np.ndarray:
    """L2(p) projection of v onto the span of the (centred) functions in ``basis`` (rows)."""
    p = np.asarray(p, float)
    B = np.atleast_2d(np.asarray(basis, float))
    B = np.array([center(p, b) for b in B])
    G = (B * p) @ B.T
    rhs = (B * p) @ center(p, v)
    c = np.linalg.lstsq(G, rhs, rcond=None)[0]
    return c @ B


def pathwise_derivative(psi, p, s, eps: float = 1e-6) -> float:
    """d/dt psi(p_t) at t = 0 along the submodel p_t = p (1 + t s), s a centred score."""
    p, s = np.asarray(p, float), center(p, s)
    return (psi(p * (1 + eps * s)) - psi(p * (1 - eps * s))) / (2 * eps)


def gradient_discrete(psi, p, eps: float = 1e-7) -> np.ndarray:
    """The nonparametric influence function of psi at p: d psi / d p_x, centred (psi evaluated on unnormalized p is
    renormalized first, so any differentiable functional of the law works)."""
    p = np.asarray(p, float)
    f = lambda q: psi(q / q.sum())  # noqa: E731
    g = np.empty(len(p))
    for x in range(len(p)):
        e = np.zeros(len(p))
        e[x] = eps
        g[x] = (f(p + e) - f(p - e)) / (2 * eps)
    return center(p, g)


def bound(p, phi) -> float:
    """The efficiency bound: the variance of the efficient influence function."""
    return inner(p, center(p, phi), center(p, phi))


def independence_scores(k1: int, k2: int) -> np.ndarray:
    """The tangent space of the model 'X1 independent of X2' on a k1 x k2 grid (cells ordered row-major): all
    functions a(x1) + b(x2), spanned by the indicators of the rows and of the columns."""
    rows = [np.repeat(np.eye(k1)[i], k2) for i in range(k1)]
    cols = [np.tile(np.eye(k2)[j], k1) for j in range(k2)]
    return np.array(rows + cols)


# ------------------------------------------------------------------------------------------- adaptive location


def fisher_location(name: str) -> float:
    """Fisher information for location of a standard law: normal 1, logistic 1/3, Laplace 1, t_nu (nu+1)/(nu+3)."""
    if name == "normal":
        return 1.0
    if name == "logistic":
        return 1.0 / 3.0
    if name == "laplace":
        return 1.0
    if name.startswith("t"):
        nu = float(name[1:])
        return (nu + 1) / (nu + 3)
    if name == "mixture":  # 0.5 N(-2, 1) + 0.5 N(2, 1): numerically
        f = lambda x: 0.5 * stats.norm.pdf(x, -2) + 0.5 * stats.norm.pdf(x, 2)  # noqa: E731
        fp = lambda x: 0.5 * -(x + 2) * stats.norm.pdf(x, -2) + 0.5 * -(x - 2) * stats.norm.pdf(x, 2)  # noqa: E731
        return integrate.quad(lambda x: fp(x) ** 2 / f(x), -12, 12, limit=200)[0]
    raise ValueError(name)


def draw_symmetric(name: str, rng: np.random.Generator, size) -> np.ndarray:
    if name == "normal":
        return rng.standard_normal(size)
    if name == "logistic":
        return rng.logistic(size=size)
    if name == "laplace":
        return rng.laplace(size=size)
    if name.startswith("t"):
        return rng.standard_t(float(name[1:]), size=size)
    if name == "mixture":
        return rng.standard_normal(size) + np.where(rng.random(size) < 0.5, -2.0, 2.0)
    raise ValueError(name)


def hodges_lehmann(x) -> float:
    x = np.asarray(x, float)
    i, j = np.triu_indices(len(x))
    return float(np.median((x[i] + x[j]) / 2))


def adaptive_location(x, h: float | None = None, trim: float = 1e-3) -> dict:
    """Stone's (1975) adaptive estimator of the centre of a symmetric law, as a one-step update.  Start from the
    Hodges-Lehmann estimate; symmetrize the residuals (r and -r); estimate the density by a Gaussian kernel and the
    location score psi = -f'/f where f is not tiny; then theta = theta0 + mean psi(r) / mean psi(r)^2."""
    x = np.asarray(x, float)
    n = len(x)
    t0 = hodges_lehmann(x)
    r = x - t0
    s = np.concatenate([r, -r])
    if h is None:
        sd = min(np.std(s), stats.iqr(s) / 1.349)
        h = 1.06 * sd * (2 * n) ** (-1 / 5)
    d = (r[:, None] - s[None, :]) / h
    k = np.exp(-0.5 * d ** 2) / math.sqrt(2 * math.pi)
    f = k.mean(axis=1) / h
    fp = (-d * k).mean(axis=1) / h ** 2
    ok = f > trim
    psi = np.where(ok, -fp / np.maximum(f, trim), 0.0)
    info = float(np.mean(psi ** 2))
    th = t0 + float(np.mean(psi)) / info
    return {"est": th, "start": t0, "info": info, "se": 1 / math.sqrt(n * info), "h": h}


# ---------------------------------------------------------------------------------------------------- the ATE


def ate_plugin(mu0, mu1) -> float:
    return float(np.mean(np.asarray(mu1) - np.asarray(mu0)))


def ate_eif(y, t, mu0, mu1, e, psi):
    y, t = np.asarray(y, float), np.asarray(t, float)
    return mu1 - mu0 + t * (y - mu1) / e - (1 - t) * (y - mu0) / (1 - e) - psi


def ate_one_step(y, t, mu0, mu1, e, alpha: float = 0.1) -> dict:
    """Plug-in plus the mean of the efficient influence function: the AIPW estimator (Hahn 1998)."""
    y, t = np.asarray(y, float), np.asarray(t, float)
    pl = ate_plugin(mu0, mu1)
    phi0 = ate_eif(y, t, mu0, mu1, e, pl)
    est = pl + float(np.mean(phi0))
    phi = ate_eif(y, t, mu0, mu1, e, est)
    se = float(np.std(phi) / math.sqrt(len(y)))
    q = stats.norm.ppf(1 - alpha / 2)
    return {"est": est, "se": se, "lo": est - q * se, "hi": est + q * se, "plugin": pl, "correction": float(np.mean(phi0))}


def ate_tmle(y, t, mu0, mu1, e, alpha: float = 0.1) -> dict:
    """Targeted maximum likelihood (van der Laan & Rubin 2006) for a continuous outcome with a linear fluctuation:
    regress the residual y - mu_t on the clever covariate H = t/e - (1-t)/(1-e), update mu, and plug in.  The update
    solves the efficient-influence-function equation exactly, so the estimate is a plug-in that is also efficient."""
    y, t = np.asarray(y, float), np.asarray(t, float)
    mu_t = np.where(t == 1, mu1, mu0)
    H = t / e - (1 - t) / (1 - e)
    eps = float(np.sum(H * (y - mu_t)) / np.sum(H * H))
    m1 = mu1 + eps / e
    m0 = mu0 - eps / (1 - e)
    est = ate_plugin(m0, m1)
    phi = ate_eif(y, t, m0, m1, e, est)
    se = float(np.std(phi) / math.sqrt(len(y)))
    q = stats.norm.ppf(1 - alpha / 2)
    return {"est": est, "se": se, "lo": est - q * se, "hi": est + q * se, "eps": eps,
            "eif_mean": float(np.mean(ate_eif(y, t, m0, m1, e, est)))}


def ate_ipw(y, t, e, alpha: float = 0.1) -> dict:
    y, t = np.asarray(y, float), np.asarray(t, float)
    w1, w0 = t / e, (1 - t) / (1 - e)
    est = float(np.sum(w1 * y) / np.sum(w1) - np.sum(w0 * y) / np.sum(w0))
    m1, m0 = np.sum(w1 * y) / np.sum(w1), np.sum(w0 * y) / np.sum(w0)
    phi = w1 * (y - m1) - w0 * (y - m0)
    se = float(np.std(phi) / math.sqrt(len(y)))
    q = stats.norm.ppf(1 - alpha / 2)
    return {"est": est, "se": se, "lo": est - q * se, "hi": est + q * se}


# ----------------------------------------------------------------------------------------- product-rate experiment


def rate_world(n: int, rng: np.random.Generator) -> dict:
    """X ~ U(0,1)^2; e(x) = 0.2 + 0.6 x1; mu0(x) = sin(2 pi x2) + x1, mu1 = mu0 + 1 + x2; y = mu_t + N(0, 1).  The true
    ATE is 1.5."""
    X = rng.random((n, 2))
    e = 0.2 + 0.6 * X[:, 0]
    t = (rng.random(n) < e).astype(float)
    mu0 = np.sin(2 * np.pi * X[:, 1]) + X[:, 0]
    mu1 = mu0 + 1 + X[:, 1]
    y = np.where(t == 1, mu1, mu0) + rng.standard_normal(n)
    return {"X": X, "t": t, "y": y, "e": e, "mu0": mu0, "mu1": mu1, "ate": 1.5}


def corrupt(w: dict, a: float, b: float, c: float = 1.0) -> dict:
    """Nuisance estimates with errors of size c n^-a (outcome) and c n^-b (propensity) in fixed smooth directions,
    chosen so that the errors are correlated and the one-step's bias is their product."""
    n = len(w["y"])
    X = w["X"]
    d = 1 + np.cos(np.pi * X[:, 0])  # the shared direction, in [0, 2]: errors in the same places
    da, db = c * n ** (-a), c * n ** (-b)
    mu1 = w["mu1"] + 2 * da * d
    mu0 = w["mu0"] + da * d
    e = np.clip(w["e"] - 0.1 * db * d, 0.05, 0.95)
    return {"mu0": mu0, "mu1": mu1, "e": e}


# ------------------------------------------------------------------------------------------- missing at random


def mar_mean(y, r, X, e_hat, m_hat, alpha: float = 0.1) -> dict:
    """The mean of y when y is seen only if r = 1, missing at random given X: complete cases, IPW (Hajek), regression
    imputation, and AIPW (Robins, Rotnitzky & Zhao 1994) with influence-function SEs."""
    y, r = np.asarray(y, float), np.asarray(r, float)
    yy = np.where(r == 1, y, 0.0)
    n = len(y)
    q = stats.norm.ppf(1 - alpha / 2)
    out = {}
    cc = float(np.sum(yy * r) / np.sum(r))
    out["cc"] = cc
    w = r / e_hat
    ipw = float(np.sum(w * yy) / np.sum(w))
    out["ipw"] = ipw
    out["reg"] = float(np.mean(m_hat))
    phi = m_hat + r * (yy - m_hat) / e_hat
    a = float(np.mean(phi))
    se = float(np.std(phi) / math.sqrt(n))
    out["aipw"] = a
    out["aipw_se"] = se
    out["aipw_lo"], out["aipw_hi"] = a - q * se, a + q * se
    return out


# ------------------------------------------------------------------------------------- the integrated square


def int_sq_normal() -> float:
    """int phi^2 = 1 / (2 sqrt(pi))."""
    return 1 / (2 * math.sqrt(math.pi))


def int_sq_estimates(x, h: float, rng: np.random.Generator) -> dict:
    """Three estimators of psi = int f^2 from a sample, with a Gaussian kernel of bandwidth h.
    plug-in: int f_hat^2 = mean over all pairs (i, j), including i = j, of K_{h sqrt 2}(X_i - X_j);
    one-step (sample split): 2 mean_B f_hat_A(X) - int f_hat_A^2, the first-order correction;
    U-statistic: mean over i != j of K_{h sqrt 2}(X_i - X_j), the second-order (quadratic) estimator."""
    x = np.asarray(x, float)
    n = len(x)
    s = h * math.sqrt(2)
    D = (x[:, None] - x[None, :]) / s
    K = np.exp(-0.5 * D ** 2) / (math.sqrt(2 * math.pi) * s)
    plug = float(K.mean())
    ustat = float((K.sum() - np.trace(K)) / (n * (n - 1)))
    idx = rng.permutation(n)
    A, B = x[idx[: n // 2]], x[idx[n // 2:]]
    DA = (A[:, None] - A[None, :]) / s
    intA = float((np.exp(-0.5 * DA ** 2) / (math.sqrt(2 * math.pi) * s)).mean())
    fB = (np.exp(-0.5 * ((B[:, None] - A[None, :]) / h) ** 2) / (math.sqrt(2 * math.pi) * h)).mean(axis=1)
    one = 2 * float(fB.mean()) - intA
    return {"plugin": plug, "one_step": one, "ustat": ustat}


def att_one_step(y, t, mu0, e, alpha: float = 0.1) -> dict:
    """The ATT's efficient one-step estimator (Hahn 1998): (1/n1) sum [t (y - mu0) - (1 - t) e/(1 - e) (y - mu0)],
    with its influence-function SE."""
    y, t = np.asarray(y, float), np.asarray(t, float)
    n = len(y)
    p = t.mean()
    r = y - mu0
    est = float(np.sum(t * r - (1 - t) * e / (1 - e) * r) / np.sum(t))
    phi = (t * (r - est) - (1 - t) * e / (1 - e) * r) / p
    se = float(np.std(phi) / math.sqrt(n))
    q = stats.norm.ppf(1 - alpha / 2)
    return {"est": est, "se": se, "lo": est - q * se, "hi": est + q * se}


def l2_basis(p, vectors) -> np.ndarray:
    """Gram-Schmidt in L2(p) on the centred ``vectors``: an orthonormal basis (rows) of their span."""
    p = np.asarray(p, float)
    out = []
    for v in vectors:
        w = center(p, v)
        for b in out:
            w = w - inner(p, w, b) * b
        nrm = math.sqrt(max(inner(p, w, w), 0.0))
        if nrm > 1e-10:
            out.append(w / nrm)
    return np.array(out)


def coords(p, v, basis) -> np.ndarray:
    return np.array([inner(p, center(p, v), b) for b in basis])
