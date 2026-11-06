"""statkit.survival -- time to event (Part 40 of *Statistics, Built*).

Lifetimes we have not finished watching.  Everything works from ``time`` (the time of the event or of censoring),
``event`` (1 if the event was seen, 0 if censored) and, where it matters, ``entry`` (delayed entry / start-stop
rows) and integer ``status`` codes for competing causes.

* **Estimators of S and H:** Kaplan--Meier with Greenwood's variance and plain, log and log-log intervals; Efron's
  redistribute-to-the-right; Nelson--Aalen with its variance; restricted mean survival time.
* **Tests:** the log-rank test and its weighted family (Gehan--Breslow, Fleming--Harrington).
* **Cox:** partial likelihood with Breslow or Efron ties, start-stop data (time-varying covariates), case weights,
  Breslow's baseline hazard; Schoenfeld residuals and Grambsch--Therneau's test of proportional hazards.
* **Parametric:** exponential, Weibull, log-normal and log-logistic accelerated failure time models by ML.
* **Competing risks:** Aalen--Johansen cumulative incidence; Fine--Gray's subdistribution hazard with IPCW weights.
* **Frailty:** the shared gamma frailty Weibull model by marginal likelihood.
* **Prediction:** Harrell's concordance; the IPCW Brier score; a small random survival forest; conformal lower
  prediction bounds under censoring (Candes, Lei & Ren 2023).

Checked against statsmodels (``SurvfuncRight``, ``survdiff``, ``PHReg``) in ``tests/test_stats_kit_survival.py``.
"""

from __future__ import annotations

import math

import numpy as np
from scipy import optimize, special, stats


# ---------------------------------------------------------------------------------------------------------------
# Kaplan--Meier, Greenwood, Nelson--Aalen
# ---------------------------------------------------------------------------------------------------------------
def risk_table(time, event, entry=None, weights=None) -> dict:
    """At each distinct event time: the number at risk (``n``), events (``d``) and censorings in (t_k, t_{k+1})."""
    time, event = np.asarray(time, float), np.asarray(event, int)
    w = np.ones(len(time)) if weights is None else np.asarray(weights, float)
    entry = np.full(len(time), -np.inf) if entry is None else np.asarray(entry, float)
    ts = np.unique(time[event == 1])
    n = np.array([w[(entry < t) & (time >= t)].sum() for t in ts])
    d = np.array([w[(time == t) & (event == 1)].sum() for t in ts])
    return {"t": ts, "n": n, "d": d}


def kaplan_meier(time, event, entry=None, weights=None, level: float = 0.95) -> dict:
    """Kaplan & Meier (1958): S(t) = prod (1 - d_k / n_k) over event times t_k <= t.  Greenwood's (1926) variance
    S^2 sum d / (n (n - d)), with plain, log and log-log ("exponential Greenwood") pointwise intervals."""
    r = risk_table(time, event, entry, weights)
    n, d = r["n"], r["d"]
    s = np.cumprod(1 - d / n)
    with np.errstate(divide="ignore", invalid="ignore"):
        gw = np.cumsum(np.where(n > d, d / (n * (n - d)), np.inf))
    with np.errstate(invalid="ignore"):
        var = np.where(s > 0, s ** 2 * gw, 0.0)
    z = stats.norm.ppf(0.5 + level / 2)
    se = np.sqrt(var)
    plain = (np.clip(s - z * se, 0, 1), np.clip(s + z * se, 0, 1))
    with np.errstate(divide="ignore", invalid="ignore"):
        lg = np.log(s)
        sl = np.sqrt(gw) / np.abs(lg)  # SE of log(-log S)
        ll = (s ** np.exp(z * sl), s ** np.exp(-z * sl))
        lgci = (np.clip(s * np.exp(-z * np.sqrt(gw)), 0, 1), np.clip(s * np.exp(z * np.sqrt(gw)), 0, 1))
    return {"t": r["t"], "n": n, "d": d, "surv": s, "var": var, "se": se, "greenwood": gw, "plain": plain,
            "loglog": ll, "log": lgci, "level": level}


def step_at(t_grid, t_knots, values, left: float = 1.0) -> np.ndarray:
    """A right-continuous step function (value ``values[k]`` from ``t_knots[k]`` on) evaluated at ``t_grid``."""
    idx = np.searchsorted(np.asarray(t_knots, float), np.asarray(t_grid, float), side="right") - 1
    v = np.asarray(values, float)
    return np.where(idx < 0, left, v[np.clip(idx, 0, len(v) - 1)])


def km_at(km: dict, t) -> np.ndarray:
    return step_at(t, km["t"], km["surv"], 1.0)


def km_median(km: dict) -> float:
    """The smallest t with S(t) <= 1/2 (NaN if the curve never gets there)."""
    k = np.flatnonzero(km["surv"] <= 0.5)
    return float(km["t"][k[0]]) if len(k) else float("nan")


def km_quantile_ci(km: dict, p: float = 0.5) -> tuple:
    """Brookmeyer & Crowley (1982): the times whose log-log interval contains 1 - p."""
    lo, hi = km["loglog"]
    q = 1 - p
    a = np.flatnonzero(hi <= q)
    b = np.flatnonzero(lo <= q)
    return (float(km["t"][b[0]]) if len(b) else float("nan"), float(km["t"][a[0]]) if len(a) else float("nan"))


def redistribute_right(time, event) -> dict:
    """Efron's (1967) redistribute-to-the-right: each censored observation's mass is shared equally among everyone
    to its right.  Returns the mass at each event time; 1 - cumsum(mass) is the Kaplan--Meier curve."""
    time, event = np.asarray(time, float), np.asarray(event, int)
    o = np.lexsort((1 - event, time))  # events before censorings at ties
    t, e = time[o], event[o]
    m = np.full(len(t), 1.0 / len(t))
    steps = []
    for i in range(len(t)):
        if e[i] == 0 and i < len(t) - 1:
            m[i + 1:] += m[i] / (len(t) - i - 1)
            m[i] = 0.0
        steps.append(m.copy())
    keep = e == 1
    ts = np.unique(t[keep])
    mass = np.array([m[(t == u) & keep].sum() for u in ts])
    return {"t": ts, "mass": mass, "surv": 1 - np.cumsum(mass), "order": o, "history": np.array(steps)}


def nelson_aalen(time, event, entry=None, weights=None) -> dict:
    """Nelson (1969) and Aalen (1978): H(t) = sum d_k / n_k, variance sum d_k / n_k^2."""
    r = risk_table(time, event, entry, weights)
    H = np.cumsum(r["d"] / r["n"])
    return {"t": r["t"], "H": H, "var": np.cumsum(r["d"] / r["n"] ** 2), "n": r["n"], "d": r["d"]}


def rmst(km: dict, tau: float) -> dict:
    """The restricted mean survival time int_0^tau S(t) dt from a KM curve, with its variance
    sum_k A_k^2 d_k / (n_k (n_k - d_k)), A_k the area under S from t_k to tau."""
    t, s = km["t"], km["surv"]
    k = t <= tau
    tt = np.concatenate([[0.0], t[k], [tau]])
    ss = np.concatenate([[1.0], s[k]])
    area = float(np.sum(np.diff(tt) * ss))
    seg = np.diff(tt) * ss  # area of each step; step j runs from tt[j] to tt[j+1]
    A = np.array([seg[j + 1:].sum() for j in range(int(k.sum()))])
    n, d = km["n"][k], km["d"][k]
    with np.errstate(divide="ignore", invalid="ignore"):
        v = float(np.sum(np.where(n > d, A ** 2 * d / (n * (n - d)), 0.0)))
    return {"rmst": area, "var": v, "se": math.sqrt(v)}


# ---------------------------------------------------------------------------------------------------------------
# The log-rank family
# ---------------------------------------------------------------------------------------------------------------
def logrank(time, event, group, weight: str = "logrank", rho: float = 0.0, gamma: float = 0.0) -> dict:
    """The two-sample log-rank test (Mantel 1966; Peto & Peto 1972): at each event time, observed minus expected
    events in group 1 given the risk sets, with the hypergeometric variance.  ``weight``: "logrank", "gehan"
    (Gehan 1965 / Breslow: weight n_k) or "fh" (Fleming--Harrington S(t-)^rho (1 - S(t-))^gamma, pooled KM)."""
    time, event, group = np.asarray(time, float), np.asarray(event, int), np.asarray(group)
    g1 = group == np.unique(group)[-1]
    ts = np.unique(time[event == 1])
    pooled = kaplan_meier(time, event)
    s_minus = np.concatenate([[1.0], pooled["surv"][:-1]])
    O = E = V = 0.0
    O1 = E1 = 0.0
    rows = []
    for k, t in enumerate(ts):
        at = time >= t
        n, n1 = at.sum(), (at & g1).sum()
        dk = ((time == t) & (event == 1)).sum()
        d1 = ((time == t) & (event == 1) & g1).sum()
        e1 = dk * n1 / n
        v = dk * (n1 / n) * (1 - n1 / n) * (n - dk) / (n - 1) if n > 1 else 0.0
        w = 1.0 if weight == "logrank" else (float(n) if weight == "gehan" else s_minus[k] ** rho * (1 - s_minus[k]) ** gamma)
        O += w * d1
        E += w * e1
        V += w * w * v
        O1 += d1
        E1 += e1
        rows.append((t, n, n1, dk, d1, e1, v))
    chi2 = (O - E) ** 2 / V
    return {"O": O1, "E": E1, "O_minus_E": O - E, "V": V, "chi2": float(chi2), "p": float(stats.chi2.sf(chi2, 1)),
            "z": float((O - E) / math.sqrt(V)), "rows": np.array(rows)}


# ---------------------------------------------------------------------------------------------------------------
# Cox's proportional hazards model
# ---------------------------------------------------------------------------------------------------------------
def _cox_terms(beta, time, event, X, entry, w, ties, ts):
    eta = X @ beta
    r = w * np.exp(eta - eta.max())
    scale = math.exp(eta.max())
    ll, U, I = 0.0, np.zeros(X.shape[1]), np.zeros((X.shape[1], X.shape[1]))
    for t in ts:
        R = (entry < t) & (time >= t)
        D = (time == t) & (event == 1)
        rr, XR = r[R], X[R]
        s0, s1, s2 = rr.sum(), rr @ XR, (XR * rr[:, None]).T @ XR
        wd = w[D]
        dsum = wd.sum()
        ll += float(wd @ eta[D])
        U += wd @ X[D]
        if ties == "breslow" or D.sum() == 1:
            ll -= dsum * (math.log(s0) + math.log(scale))
            xb = s1 / s0
            U -= dsum * xb
            I += dsum * (s2 / s0 - np.outer(xb, xb))
        else:  # Efron (1977)
            rd, XD = r[D], X[D]
            d0, d1, d2 = rd.sum(), rd @ XD, (XD * rd[:, None]).T @ XD
            m = int(D.sum())
            wbar = dsum / m
            for l in range(m):
                f = l / m
                a0, a1, a2 = s0 - f * d0, s1 - f * d1, s2 - f * d2
                ll -= wbar * (math.log(a0) + math.log(scale))
                xb = a1 / a0
                U -= wbar * xb
                I += wbar * (a2 / a0 - np.outer(xb, xb))
    return ll, U, I


def cox_fit(time, event, X, entry=None, weights=None, ties: str = "efron", max_iter: int = 60, tol: float = 1e-10) -> dict:
    """Cox (1972) by Newton--Raphson on the partial likelihood.  ``entry`` gives start-stop (counting process) rows,
    so a covariate can change over time (Andersen & Gill 1982); ``ties`` "efron" (Efron 1977) or "breslow".  Returns
    beta, its covariance (inverse information), the log partial likelihood at beta and at 0, Wald, score and LR
    statistics, and Breslow's baseline cumulative hazard at the event times (at X = 0)."""
    time, event = np.asarray(time, float), np.asarray(event, int)
    X = np.asarray(X, float)
    X = X[:, None] if X.ndim == 1 else X
    n, p = X.shape
    w = np.ones(n) if weights is None else np.asarray(weights, float)
    entry = np.full(n, -np.inf) if entry is None else np.asarray(entry, float)
    ts = np.unique(time[event == 1])
    beta = np.zeros(p)
    ll0, U0, I0 = _cox_terms(beta, time, event, X, entry, w, ties, ts)
    ll = ll0
    for _ in range(max_iter):
        l_, U, I = _cox_terms(beta, time, event, X, entry, w, ties, ts)
        step = np.linalg.solve(I, U)
        lam = 1.0
        while True:
            nb = beta + lam * step
            l_new = _cox_terms(nb, time, event, X, entry, w, ties, ts)[0]
            if l_new >= l_ - 1e-12 or lam < 1e-6:
                break
            lam /= 2
        beta = nb
        if abs(l_new - l_) < tol and np.max(np.abs(lam * step)) < 1e-8:
            ll = l_new
            break
        ll = l_new
    _, U, I = _cox_terms(beta, time, event, X, entry, w, ties, ts)
    cov = np.linalg.inv(I)
    eta = X @ beta
    H0 = np.cumsum([w[(time == t) & (event == 1)].sum() / (w[(entry < t) & (time >= t)] @ np.exp(eta[(entry < t) & (time >= t)]))
                    for t in ts])
    score = float(U0 @ np.linalg.solve(I0, U0))
    return {"beta": beta, "cov": cov, "se": np.sqrt(np.diag(cov)), "loglik": ll, "loglik0": ll0, "lr": 2 * (ll - ll0),
            "score": score, "wald": float(beta @ np.linalg.solve(cov, beta)), "t": ts, "H0": H0, "n_events": int(event.sum())}


def cox_survival(fit: dict, x, t_grid) -> np.ndarray:
    """S(t | x) = exp(-H0(t) exp(x' beta)) on ``t_grid`` (rows: individuals)."""
    x = np.atleast_2d(np.asarray(x, float))
    H = step_at(t_grid, fit["t"], fit["H0"], 0.0)
    return np.exp(-np.outer(np.exp(x @ fit["beta"]), H))


def schoenfeld(time, event, X, fit: dict, entry=None) -> dict:
    """Schoenfeld (1982) residuals x_i - xbar(t_i) at each event (Breslow form), their scaled version
    beta + D V r (Grambsch & Therneau 1994), and the GT test of zero slope against g(t) = the KM transform."""
    time, event = np.asarray(time, float), np.asarray(event, int)
    X = np.asarray(X, float)
    X = X[:, None] if X.ndim == 1 else X
    entry = np.full(len(time), -np.inf) if entry is None else np.asarray(entry, float)
    r = np.exp(X @ fit["beta"])
    idx = np.flatnonzero(event == 1)
    idx = idx[np.argsort(time[idx], kind="stable")]
    res = []
    for i in idx:
        R = (entry < time[i]) & (time >= time[i])
        res.append(X[i] - (r[R] @ X[R]) / r[R].sum())
    res = np.array(res)
    D = len(idx)
    scaled = fit["beta"] + D * res @ fit["cov"]
    km = kaplan_meier(time, event)
    g = 1 - step_at(time[idx] - 1e-9, km["t"], km["surv"], 1.0)
    gc = g - g.mean()
    V = fit["cov"]
    # per-covariate statistic: (sum gc * scaled_j)^2 / (D V_jj sum gc^2)
    sc = scaled - fit["beta"]
    test = np.array([(gc @ sc[:, j]) ** 2 / (D * V[j, j] * (gc @ gc)) for j in range(X.shape[1])])
    return {"t": time[idx], "resid": res, "scaled": scaled, "g": g, "chi2": test, "p": stats.chi2.sf(test, 1)}


# ---------------------------------------------------------------------------------------------------------------
# Parametric (AFT) models
# ---------------------------------------------------------------------------------------------------------------
def aft_fit(time, event, X=None, dist: str = "weibull") -> dict:
    """log T = x' gamma + sigma W, W standard extreme-value ("weibull", "exponential" with sigma = 1), normal
    ("lognormal") or logistic ("loglogistic"), fitted by maximum likelihood with right censoring.  For the Weibull,
    the hazard ratio of a covariate is exp(-gamma / sigma)."""
    time, event = np.asarray(time, float), np.asarray(event, int)
    n = len(time)
    Z = np.ones((n, 1)) if X is None else np.column_stack([np.ones(n), np.asarray(X, float)])
    y = np.log(time)

    def logf_logS(u):
        if dist in ("weibull", "exponential"):
            return u - np.exp(u), -np.exp(u)
        if dist == "lognormal":
            return stats.norm.logpdf(u), stats.norm.logsf(u)
        if dist == "loglogistic":
            return u - 2 * np.log1p(np.exp(u)), -np.log1p(np.exp(u))
        raise ValueError(dist)

    def nll(par):
        g = par[:Z.shape[1]]
        ls = 0.0 if dist == "exponential" else par[-1]
        s = math.exp(ls)
        u = (y - Z @ g) / s
        lf, lS = logf_logS(u)
        return -float(np.sum(event * (lf - ls - y) + (1 - event) * lS))

    g0 = np.linalg.lstsq(Z, y, rcond=None)[0]
    x0 = g0 if dist == "exponential" else np.concatenate([g0, [0.0]])
    res = optimize.minimize(nll, x0, method="BFGS", options={"gtol": 1e-8, "maxiter": 2000})
    H = _num_hessian(nll, res.x)
    cov = np.linalg.inv(H)
    k = Z.shape[1]
    sigma = 1.0 if dist == "exponential" else math.exp(res.x[-1])
    return {"coef": res.x[:k], "sigma": sigma, "log_sigma": None if dist == "exponential" else res.x[-1], "cov": cov,
            "se": np.sqrt(np.diag(cov)), "loglik": -res.fun, "dist": dist, "aic": 2 * res.fun + 2 * len(res.x)}


def aft_survival(fit: dict, x, t) -> np.ndarray:
    z = np.concatenate([[1.0], np.atleast_1d(np.asarray(x, float))]) if np.ndim(x) <= 1 else None
    mu = float(z[: len(fit["coef"])] @ fit["coef"])
    u = (np.log(np.asarray(t, float)) - mu) / fit["sigma"]
    d = fit["dist"]
    if d in ("weibull", "exponential"):
        return np.exp(-np.exp(u))
    if d == "lognormal":
        return stats.norm.sf(u)
    return 1 / (1 + np.exp(u))


def _num_hessian(f, x, h: float = 1e-4) -> np.ndarray:
    x = np.asarray(x, float)
    k = len(x)
    H = np.zeros((k, k))
    for i in range(k):
        for j in range(i, k):
            ei, ej = np.zeros(k), np.zeros(k)
            ei[i], ej[j] = h, h
            H[i, j] = H[j, i] = (f(x + ei + ej) - f(x + ei - ej) - f(x - ei + ej) + f(x - ei - ej)) / (4 * h * h)
    return H


# ---------------------------------------------------------------------------------------------------------------
# Competing risks
# ---------------------------------------------------------------------------------------------------------------
def aalen_johansen(time, status, causes=(1, 2)) -> dict:
    """Cumulative incidence F_k(t) = sum_{s <= t} S(s-) d_k(s) / n(s), with S the all-cause KM; ``status`` 0 is
    censoring.  Also returns the naive 1 - KM that treats the other causes as censoring, which overstates F_k."""
    time, status = np.asarray(time, float), np.asarray(status, int)
    ts = np.unique(time[status > 0])
    n = np.array([(time >= t).sum() for t in ts])
    dall = np.array([((time == t) & (status > 0)).sum() for t in ts])
    S = np.cumprod(1 - dall / n)
    Sm = np.concatenate([[1.0], S[:-1]])
    out = {"t": ts, "surv": S}
    for c in causes:
        dk = np.array([((time == t) & (status == c)).sum() for t in ts])
        out[f"cif{c}"] = np.cumsum(Sm * dk / n)
        out[f"naive{c}"] = 1 - np.cumprod(1 - dk / n)
    return out


def fine_gray(time, status, X, cause: int = 1, max_iter: int = 50) -> dict:
    """Fine & Gray (1999): proportional hazards for the subdistribution of ``cause``.  Those who failed of another
    cause stay in the risk set with inverse-probability-of-censoring weight G(t-) / G(T_i-) (G the censoring KM);
    Breslow ties.  exp(beta) is a subdistribution hazard ratio: it moves the cumulative incidence."""
    time, status = np.asarray(time, float), np.asarray(status, int)
    X = np.asarray(X, float)
    X = X[:, None] if X.ndim == 1 else X
    n, p = X.shape
    Gk = kaplan_meier(time, (status == 0).astype(int))
    G = lambda t: step_at(np.asarray(t) - 1e-10, Gk["t"], Gk["surv"], 1.0)  # noqa: E731
    ts = np.unique(time[status == cause])
    other = (status > 0) & (status != cause)
    Gi = G(time)
    beta = np.zeros(p)

    def terms(b):
        eta = X @ b
        r = np.exp(eta - eta.max())
        ll, U, I = 0.0, np.zeros(p), np.zeros((p, p))
        for t in ts:
            w = np.where(time >= t, 1.0, np.where(other & (time < t), G(t) / np.maximum(Gi, 1e-12), 0.0))
            rr = w * r
            s0, s1, s2 = rr.sum(), rr @ X, (X * rr[:, None]).T @ X
            D = (time == t) & (status == cause)
            d = D.sum()
            ll += eta[D].sum() - d * (math.log(s0) + eta.max())
            xb = s1 / s0
            U += X[D].sum(0) - d * xb
            I += d * (s2 / s0 - np.outer(xb, xb))
        return ll, U, I

    ll = terms(beta)[0]
    for _ in range(max_iter):
        l_, U, I = terms(beta)
        step = np.linalg.solve(I, U)
        beta = beta + step
        if np.max(np.abs(step)) < 1e-9:
            break
    ll, U, I = terms(beta)
    cov = np.linalg.inv(I)  # model-based; Fine & Gray's sandwich is close for these sample sizes
    return {"beta": beta, "cov": cov, "se": np.sqrt(np.diag(cov)), "loglik": ll}


# ---------------------------------------------------------------------------------------------------------------
# Frailty
# ---------------------------------------------------------------------------------------------------------------
def gamma_frailty_weibull(time, event, cluster, X=None) -> dict:
    """The shared gamma frailty model: h_ij(t) = Z_i h0(t) exp(x' beta), Z_i ~ Gamma(mean 1, variance theta), with a
    Weibull baseline h0(t) = k t^{k-1} / lam^k.  The frailty integrates out in closed form (the Laplace transform):
    L_i = prod h_ij^{delta_ij} theta^{d_i} Gamma(1/theta + d_i) / Gamma(1/theta) (1 + theta sum H_ij)^{-(1/theta + d_i)}."""
    time, event = np.asarray(time, float), np.asarray(event, int)
    cl = np.unique(cluster, return_inverse=True)[1]
    Xm = np.zeros((len(time), 0)) if X is None else np.asarray(X, float).reshape(len(time), -1)
    p = Xm.shape[1]

    def nll(par):
        lk, llam, lth = par[0], par[1], par[2]
        b = par[3:]
        k, lam, th = math.exp(lk), math.exp(llam), math.exp(lth)
        eta = Xm @ b if p else np.zeros(len(time))
        H = (time / lam) ** k * np.exp(eta)
        logh = lk - k * llam + (k - 1) * np.log(time) + eta
        di = np.bincount(cl, weights=event)
        Hi = np.bincount(cl, weights=H)
        ll = float(event @ logh)
        ll += float(np.sum(di * lth + special.gammaln(1 / th + di) - special.gammaln(1 / th) - (1 / th + di) * np.log1p(th * Hi)))
        return -ll

    x0 = np.concatenate([[0.0, math.log(np.mean(time)), math.log(0.5)], np.zeros(p)])
    res = optimize.minimize(nll, x0, method="Nelder-Mead", options={"maxiter": 20000, "xatol": 1e-8, "fatol": 1e-10})
    res = optimize.minimize(nll, res.x, method="BFGS")
    cov = np.linalg.inv(_num_hessian(nll, res.x))
    return {"k": math.exp(res.x[0]), "lam": math.exp(res.x[1]), "theta": math.exp(res.x[2]), "beta": res.x[3:],
            "cov": cov, "loglik": -res.fun, "se_log_theta": math.sqrt(cov[2, 2])}


# ---------------------------------------------------------------------------------------------------------------
# Prediction
# ---------------------------------------------------------------------------------------------------------------
def concordance(time, event, risk) -> float:
    """Harrell's C: among usable pairs (the shorter time is an event), the share where the shorter-lived has the
    higher risk score (ties in risk count one half)."""
    time, event, risk = np.asarray(time, float), np.asarray(event, int), np.asarray(risk, float)
    T1, T2 = time[:, None], time[None, :]
    usable = (T1 < T2) & (event[:, None] == 1)
    conc = (risk[:, None] > risk[None, :]) + 0.5 * (risk[:, None] == risk[None, :])
    return float((conc * usable).sum() / usable.sum())


def brier_ipcw(time, event, surv_at_t, t: float) -> float:
    """Graf et al. (1999): the Brier score at time t with inverse-probability-of-censoring weights."""
    time, event, S = np.asarray(time, float), np.asarray(event, int), np.asarray(surv_at_t, float)
    Gk = kaplan_meier(time, 1 - event)
    G = lambda u: np.maximum(step_at(np.asarray(u) - 1e-10, Gk["t"], Gk["surv"], 1.0), 1e-8)  # noqa: E731
    died = (time <= t) & (event == 1)
    alive = time > t
    return float(np.mean(died * S ** 2 / G(time) + alive * (1 - S) ** 2 / G(t)))


def _logrank_stat(time, event, left):
    """The two-sample log-rank z^2 for a split (fast, unweighted)."""
    ts = np.unique(time[event == 1])
    if len(ts) == 0:
        return 0.0
    at = time[None, :] >= ts[:, None]
    dk = ((time[None, :] == ts[:, None]) & (event[None, :] == 1))
    n = at.sum(1)
    n1 = (at & left[None, :]).sum(1)
    d = dk.sum(1)
    d1 = (dk & left[None, :]).sum(1)
    e1 = d * n1 / n
    with np.errstate(invalid="ignore", divide="ignore"):
        v = np.where(n > 1, d * (n1 / n) * (1 - n1 / n) * (n - d) / (n - 1), 0.0)
    V = v.sum()
    return float((d1.sum() - e1.sum()) ** 2 / V) if V > 0 else 0.0


def survival_forest(time, event, X, n_trees: int = 100, mtry: int | None = None, min_leaf: int = 15, max_depth: int = 6,
                    n_cuts: int = 8, rng: np.random.Generator | None = None) -> dict:
    """A small random survival forest (Ishwaran et al. 2008): bootstrap samples, trees split by the log-rank
    statistic over ``mtry`` random covariates and a few quantile cut points, Nelson--Aalen hazards in the leaves.
    Returns the trees and their out-of-bag rows; predict with ``forest_chf``."""
    rng = rng or np.random.default_rng(0)
    time, event, X = np.asarray(time, float), np.asarray(event, int), np.asarray(X, float)
    n, p = X.shape
    mtry = mtry or max(1, int(math.sqrt(p)))
    trees, oob = [], []

    def grow(idx, depth):
        if depth >= max_depth or len(idx) < 2 * min_leaf or event[idx].sum() < 2:
            return ("leaf", idx)
        best = (0.0, None, None)
        for j in rng.choice(p, mtry, replace=False):
            xs = X[idx, j]
            cuts = np.unique(np.quantile(xs, np.linspace(0.1, 0.9, n_cuts)))
            for c in cuts:
                left = xs <= c
                if left.sum() < min_leaf or (~left).sum() < min_leaf:
                    continue
                s = _logrank_stat(time[idx], event[idx], left)
                if s > best[0]:
                    best = (s, j, c)
        if best[1] is None:
            return ("leaf", idx)
        j, c = best[1], best[2]
        m = X[idx, j] <= c
        return ("node", j, c, grow(idx[m], depth + 1), grow(idx[~m], depth + 1))

    for _ in range(n_trees):
        b = rng.integers(0, n, n)
        trees.append((grow(b, 0), b))
        oob.append(np.setdiff1d(np.arange(n), b))
    return {"trees": trees, "oob": oob, "time": time, "event": event, "X": X}


def forest_chf(forest: dict, Xnew, t_grid, oob_only: bool = False) -> np.ndarray:
    """The ensemble cumulative hazard at ``t_grid`` for each row of ``Xnew`` (or, with ``oob_only``, for the
    training rows using only trees that did not see them)."""
    time, event = forest["time"], forest["event"]
    Xnew = np.asarray(Xnew, float)
    out = np.zeros((len(Xnew), len(t_grid)))
    cnt = np.zeros(len(Xnew))

    def leaf_chf(idx):
        na = nelson_aalen(time[idx], event[idx])
        return step_at(t_grid, na["t"], na["H"], 0.0) if len(na["t"]) else np.zeros(len(t_grid))

    for k, (tree, _) in enumerate(forest["trees"]):
        rows = forest["oob"][k] if oob_only else np.arange(len(Xnew))
        cache = {}
        for i in rows:
            node = tree
            while node[0] == "node":
                node = node[3] if Xnew[i, node[1]] <= node[2] else node[4]
            key = id(node)
            if key not in cache:
                cache[key] = leaf_chf(node[1])
            out[i] += cache[key]
            cnt[i] += 1
    return out / np.maximum(cnt, 1)[:, None]


def conformal_lpb(t_cal, c_cal, q_cal, q_test, c0: float, alpha: float = 0.1, w_cal=None, w_test=None) -> np.ndarray:
    """Candes, Lei & Ren (2023): a lower prediction bound for T under censoring.  Calibrate on units whose censoring
    time is at least c0 (so T ^ c0 is seen), with scores V = q(x) - (T ^ c0) and weights 1 / P(C >= c0 | x) (``w``);
    the bound is q(x) - eta, eta the weighted (1 - alpha) quantile of V.  ``q`` is any fitted lower quantile."""
    t_cal, c_cal, q_cal = (np.asarray(a, float) for a in (t_cal, c_cal, q_cal))
    keep = c_cal >= c0
    V = q_cal[keep] - np.minimum(t_cal[keep], c0)
    w = np.ones(keep.sum()) if w_cal is None else np.asarray(w_cal, float)[keep]
    q_test = np.asarray(q_test, float)
    wt = np.ones(len(q_test)) if w_test is None else np.asarray(w_test, float)
    o = np.argsort(V)
    Vs, ws = V[o], w[o]
    out = np.empty(len(q_test))
    for i in range(len(q_test)):
        tot = ws.sum() + wt[i]
        cum = np.cumsum(ws) / tot
        k = np.searchsorted(cum, 1 - alpha)
        eta = Vs[k] if k < len(Vs) else np.inf
        out[i] = min(q_test[i] - eta, c0)
    return out
