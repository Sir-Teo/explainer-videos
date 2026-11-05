"""statkit.mixed: linear and generalized linear mixed models (Part 25 of *Statistics, Built*).

    from explainer.stats.kit.mixed import lmm, satterthwaite, glmm_logit

``lmm`` fits y_g = X_g beta + Z_g b_g + e_g, b_g ~ N(0, G), e ~ N(0, sigma^2 I), with Z_g built from an intercept and
optional slope columns of X (Laird & Ware 1982), by ML or REML with sigma^2 profiled out; per-group Woodbury algebra
keeps it O(n q^2).  BLUPs come from Henderson's equations.  ``satterthwaite`` gives approximate degrees of freedom for
a contrast.  ``glmm_logit`` fits a random-intercept logistic model by Laplace (nagq = 1) or adaptive Gauss-Hermite
quadrature.  Checked against statsmodels in ``tests/test_stats_kit_mixed.py``.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from scipy import optimize, special, stats


def _chol_from_theta(theta, q):
    L = np.zeros((q, q))
    idx = np.tril_indices(q)
    L[idx] = theta
    d = np.diag_indices(q)
    L[d] = np.exp(L[d])
    return L


@dataclass
class LMM:
    beta: np.ndarray
    cov_beta: np.ndarray
    G: np.ndarray
    sigma2: float
    blup: np.ndarray
    loglik: float
    method: str
    theta: np.ndarray
    groups: np.ndarray = field(repr=False)
    q: int = 1
    extra: dict = field(default_factory=dict)

    @property
    def se(self):
        return np.sqrt(np.diag(self.cov_beta))

    @property
    def icc(self) -> float:
        return float(self.G[0, 0] / (self.G[0, 0] + self.sigma2))


def _prep(y, X, groups, slopes):
    y, X = np.asarray(y, float), np.asarray(X, float)
    groups = np.asarray(groups)
    labels, idx = np.unique(groups, return_inverse=True)
    members = [np.flatnonzero(idx == g) for g in range(len(labels))]
    Zcols = [np.ones(len(y))] + [X[:, j] for j in (slopes or [])]
    Z = np.column_stack(Zcols)
    return y, X, Z, members, labels


def _profiled(theta, y, X, Z, members, reml):
    """-2 log likelihood (profiled over beta and sigma^2) and the pieces needed afterwards."""
    n, p = X.shape
    q = Z.shape[1]
    L = _chol_from_theta(theta, q)
    Gs = L @ L.T  # G / sigma^2
    XtVX = np.zeros((p, p))
    XtVy = np.zeros(p)
    logdet = 0.0
    store = []
    for m in members:
        Zg, Xg, yg = Z[m], X[m], y[m]
        # V_g / sigma^2 = I + Zg Gs Zg'; Woodbury: V^-1 = I - Zg (Gs^-1 + Zg'Zg)^-1 Zg'  (Gs may be singular: use L)
        M = np.eye(q) + L.T @ (Zg.T @ Zg) @ L
        Mi = np.linalg.inv(M)
        A = Zg @ L
        def vinv(v, A=A, Mi=Mi):
            return v - A @ (Mi @ (A.T @ v))
        XtVX += Xg.T @ vinv(Xg)
        XtVy += Xg.T @ vinv(yg)
        logdet += np.linalg.slogdet(M)[1]
        store.append((A, Mi))
    beta = np.linalg.solve(XtVX, XtVy)
    rss = 0.0
    for m, (A, Mi) in zip(members, store):
        r = y[m] - X[m] @ beta
        rss += float(r @ (r - A @ (Mi @ (A.T @ r))))
    df = n - p if reml else n
    s2 = rss / df
    dev = logdet + df * (1 + np.log(2 * np.pi * s2))
    if reml:
        dev += np.linalg.slogdet(XtVX)[1]
    return dev, beta, s2, XtVX, Gs, store


def lmm(y, X, groups, slopes=None, method: str = "REML") -> LMM:
    """Fit the linear mixed model; ``slopes`` lists columns of X that also get random slopes."""
    y, X, Z, members, labels = _prep(y, X, groups, slopes)
    q = Z.shape[1]
    reml = method.upper() == "REML"
    theta0 = np.zeros(q * (q + 1) // 2)
    f = lambda th: _profiled(th, y, X, Z, members, reml)[0]  # noqa: E731
    r = optimize.minimize(f, theta0, method="Nelder-Mead" if q > 1 else "BFGS",
                          options={"xatol": 1e-9, "fatol": 1e-10, "maxiter": 20000} if q > 1 else {"gtol": 1e-8})
    # a variance at zero: also try the boundary
    th = r.x
    if q == 1:
        r2 = optimize.minimize_scalar(lambda t: f(np.array([t])), bounds=(-15, 6), method="bounded", options={"xatol": 1e-10})
        if r2.fun < f(th):
            th = np.array([r2.x])
    dev, beta, s2, XtVX, Gs, store = _profiled(th, y, X, Z, members, reml)
    cov = s2 * np.linalg.inv(XtVX)
    G = s2 * Gs
    # BLUPs: b_g = G Zg' V_g^-1 (y_g - X_g beta)
    L = _chol_from_theta(th, q)
    blup = np.zeros((len(members), q))
    for k, (m, (A, Mi)) in enumerate(zip(members, store)):
        r_ = y[m] - X[m] @ beta
        vr = r_ - A @ (Mi @ (A.T @ r_))
        blup[k] = (L @ L.T) @ (Z[m].T @ vr)
    return LMM(beta, cov, G, s2, blup, -dev / 2, "REML" if reml else "ML", th, labels, q,
               {"y": y, "X": X, "Z": Z, "members": members, "reml": reml})


def satterthwaite(fit: LMM, c) -> dict:
    """Satterthwaite's degrees of freedom for c'beta: 2 V^2 / (g' A g), V = c' Cov(beta) c as a function of the
    variance parameters (log sigma^2 and theta), g its gradient, A the inverse Hessian of the (RE)ML deviance / 2."""
    c = np.asarray(c, float)
    e = fit.extra
    q = fit.q

    def pieces(par):
        ls2, th = par[0], par[1:]
        _, beta, _, XtVX, Gs, _ = _profiled(th, e["y"], e["X"], e["Z"], e["members"], e["reml"])
        return np.exp(ls2) * c @ np.linalg.solve(XtVX, c)

    def dev_full(par):  # the unprofiled -2 log likelihood in (log sigma^2, theta)
        ls2, th = par[0], par[1:]
        d, beta, s2, XtVX, Gs, store = _profiled(th, e["y"], e["X"], e["Z"], e["members"], e["reml"])
        n, p = e["X"].shape
        df = n - p if e["reml"] else n
        # replace the profiled sigma^2 by exp(ls2): d = logdet + df log(2 pi s2_hat) + df; general form:
        return d - df * (1 + np.log(s2)) + df * ls2 + df * s2 / np.exp(ls2)

    n, p_ = e["X"].shape
    if q == 1 and fit.G[0, 0] < 1e-8 * fit.sigma2:  # the variance estimate is on the boundary: an OLS fit, n - p df
        V0 = float(c @ fit.cov_beta @ c)
        return {"V": V0, "se": float(np.sqrt(V0)), "df": float(n - p_), "boundary": True}
    par = np.concatenate([[np.log(fit.sigma2)], fit.theta])
    h = 1e-4
    k = len(par)
    g = np.array([(pieces(par + h * np.eye(k)[i]) - pieces(par - h * np.eye(k)[i])) / (2 * h) for i in range(k)])
    H = np.zeros((k, k))
    for i in range(k):
        for j in range(k):
            ei, ej = h * np.eye(k)[i], h * np.eye(k)[j]
            H[i, j] = (dev_full(par + ei + ej) - dev_full(par + ei - ej) - dev_full(par - ei + ej) + dev_full(par - ei - ej)) / (4 * h * h)
    A = np.linalg.pinv(H / 2)
    V = pieces(par)
    df = float(np.clip(2 * V ** 2 / max(g @ A @ g, 1e-300), 1.0, n - p_))
    return {"V": float(V), "se": float(np.sqrt(V)), "df": df, "boundary": False}


def glmm_logit(y, X, groups, nagq: int = 1) -> dict:
    """Random-intercept logistic regression: logit P(y = 1 | u_g) = x'beta + u_g, u_g ~ N(0, s^2).  The marginal
    likelihood integrates each group's u by the Laplace approximation (nagq = 1) or adaptive Gauss-Hermite quadrature
    centred at the conditional mode with the mode's curvature (Pinheiro & Bates 1995)."""
    y, X = np.asarray(y, float), np.asarray(X, float)
    groups = np.asarray(groups)
    labels, idx = np.unique(groups, return_inverse=True)
    members = [np.flatnonzero(idx == g) for g in range(len(labels))]
    gh_x, gh_w = np.polynomial.hermite.hermgauss(nagq)

    def group_ll(eta0, yg, s):
        def h(u):  # log integrand
            e = eta0 + u
            return np.sum(yg * e - np.logaddexp(0, e)) - 0.5 * u * u / s ** 2 - 0.5 * np.log(2 * np.pi * s ** 2)
        u = 0.0
        for _ in range(50):  # Newton for the mode
            p = special.expit(eta0 + u)
            g1 = np.sum(yg - p) - u / s ** 2
            g2 = -np.sum(p * (1 - p)) - 1 / s ** 2
            step = g1 / g2
            u -= step
            if abs(step) < 1e-12:
                break
        p = special.expit(eta0 + u)
        curv = np.sum(p * (1 - p)) + 1 / s ** 2
        sd = 1 / np.sqrt(curv)
        if nagq == 1:
            return h(u) + 0.5 * np.log(2 * np.pi) + np.log(sd), u
        nodes = u + np.sqrt(2) * sd * gh_x
        vals = np.array([h(t) for t in nodes]) + gh_x ** 2
        mx = vals.max()
        return float(np.log(np.sum(gh_w * np.exp(vals - mx))) + mx + np.log(np.sqrt(2) * sd)), u

    def nll(par):
        b, ls = par[:-1], par[-1]
        s = np.exp(ls)
        tot = 0.0
        for m in members:
            ll, _ = group_ll(X[m] @ b, y[m], s)
            tot += ll
        return -tot

    from explainer.stats.kit.glm import family, glm_fit
    b0 = glm_fit(X, y, family("binomial")).coef
    r = optimize.minimize(nll, np.concatenate([b0, [np.log(0.5)]]), method="BFGS", options={"gtol": 1e-7})
    par = r.x
    from explainer.stats.kit.mle import numerical_hessian
    H = numerical_hessian(lambda t: -nll(t), par, h=1e-4)
    cov = np.linalg.inv(-H)
    modes = np.array([group_ll(X[m] @ par[:-1], y[m], np.exp(par[-1]))[1] for m in members])
    return {"beta": par[:-1], "sigma": float(np.exp(par[-1])), "se": np.sqrt(np.diag(cov))[:-1], "loglik": -float(r.fun),
            "modes": modes, "nagq": nagq}


def vc_lmm(y, X, factors: dict, method: str = "REML") -> dict:
    """Random intercepts for several grouping factors, crossed or nested: V = sigma^2 (I + sum_k gamma_k Z_k Z_k'),
    tau_k^2 = gamma_k sigma^2, fitted by ML or REML with sigma^2 profiled out and gamma_k >= 0 (dense algebra, so for
    a few thousand rows).  Returns beta, its covariance, the variances by factor, sigma^2, BLUPs by factor (Henderson:
    b_k = tau_k^2 Z_k' V^-1 (y - X beta)) and the log likelihood."""
    y, X = np.asarray(y, float), np.asarray(X, float)
    n, p = X.shape
    names = list(factors)
    Zs, labs = [], []
    for k in names:
        lab, idx = np.unique(np.asarray(factors[k]), return_inverse=True)
        Z = np.zeros((n, len(lab)))
        Z[np.arange(n), idx] = 1.0
        Zs.append(Z)
        labs.append(lab)
    ZZ = [Z @ Z.T for Z in Zs]
    reml = method.upper() == "REML"

    def parts(gam):
        H = np.eye(n) + sum(g_ * M for g_, M in zip(gam, ZZ))
        L = np.linalg.cholesky(H)
        Li = np.linalg.solve(L, np.eye(n))
        Hi = Li.T @ Li
        XtHX = X.T @ Hi @ X
        beta = np.linalg.solve(XtHX, X.T @ Hi @ y)
        r = y - X @ beta
        q = float(r @ Hi @ r)
        ldH = 2 * np.sum(np.log(np.diag(L)))
        return H, Hi, XtHX, beta, r, q, ldH

    def dev(gam):
        _, _, XtHX, _, _, q, ldH = parts(gam)
        if reml:
            m = n - p
            return ldH + np.linalg.slogdet(XtHX)[1] + m * (1 + np.log(2 * np.pi * q / m))
        return ldH + n * (1 + np.log(2 * np.pi * q / n))

    best = None
    for start in (0.1, 1.0):
        r_ = optimize.minimize(dev, np.full(len(Zs), start), method="L-BFGS-B", bounds=[(0, None)] * len(Zs))
        if best is None or r_.fun < best.fun:
            best = r_
    gam = best.x
    H, Hi, XtHX, beta, r, q, _ = parts(gam)
    s2 = q / (n - p if reml else n)
    blups = {k: (gam[i] * Zs[i].T @ Hi @ r) for i, k in enumerate(names)}
    return {"beta": beta, "cov_beta": s2 * np.linalg.inv(XtHX), "var": {k: float(gam[i] * s2) for i, k in enumerate(names)},
            "sigma2": float(s2), "blup": blups, "labels": {k: labs[i] for i, k in enumerate(names)},
            "loglik": -0.5 * float(best.fun), "method": "REML" if reml else "ML"}
