"""The House's volatility forecaster and time-series tools (Part 7, *Time Series and Volatility*).

Plain numpy and scipy, tested against simulated processes with known parameters:

* realized measures: :func:`realized_variance`, :func:`bipower_variation`, :func:`two_scale_rv` (Zhang, Mykland and
  Ait-Sahalia 2005), :func:`realized_kernel` (Parzen; Barndorff-Nielsen, Hansen, Lunde and Shephard 2008);
* forecasters: :func:`ewma`, :func:`garch_fit` for GARCH(1,1) (Bollerslev 1986), GJR (Glosten, Jagannathan and Runkle
  1993) and EGARCH (Nelson 1991) by maximum likelihood, with :func:`garch_filter`; :func:`har_fit` for HAR-RV (Corsi
  2009) and HARQ (Bollerslev, Patton and Quaedvlieg 2016);
* evaluation: :func:`qlike`, :func:`mse`, :func:`diebold_mariano`;
* time series: :func:`acf`, :func:`ar_fit`, :func:`adf` (Dickey-Fuller with MacKinnon's 5% value), :func:`engle_granger`;
* hidden states: :func:`markov_switching` (Hamilton 1989, two Gaussian regimes, EM) and :func:`kalman_local_level`;
* correlation: :func:`dcc_fit` (Engle 2002), two assets.
"""

from __future__ import annotations

import numpy as np
from scipy import optimize


# ---------------------------------------------------------------------------
# Realized measures (inputs: intraday log prices or returns of one day)
def realized_variance(r) -> float:
    r = np.asarray(r, float)
    return float(np.sum(r ** 2))


def bipower_variation(r) -> float:
    r = np.abs(np.asarray(r, float))
    return float(np.pi / 2 * np.sum(r[1:] * r[:-1]))


def two_scale_rv(logp, K: int = 5) -> float:
    """TSRV: the average of K sparse realized variances, minus a bias correction from the dense one."""
    x = np.asarray(logp, float)
    n = len(x) - 1
    dense = np.sum(np.diff(x) ** 2)
    sparse = np.mean([np.sum(np.diff(x[k::K]) ** 2) for k in range(K)])
    nbar = (n - K + 1) / K
    return float((sparse - nbar / n * dense) / (1 - nbar / n))


def realized_kernel(r, H: int = 5) -> float:
    """Flat-top Parzen realized kernel: RV plus weighted realized autocovariances up to H."""
    r = np.asarray(r, float)

    def parzen(x):
        return 1 - 6 * x ** 2 + 6 * x ** 3 if x <= 0.5 else 2 * (1 - x) ** 3

    out = np.sum(r ** 2)
    for h in range(1, H + 1):
        g = np.sum(r[h:] * r[:-h])
        out += 2 * parzen(h / (H + 1)) * g
    return float(out)


# ---------------------------------------------------------------------------
def ewma(r, lam: float = 0.94, init=None) -> np.ndarray:
    """One-step-ahead variance forecasts: h_{t+1} = lam h_t + (1 - lam) r_t^2 (RiskMetrics).  h[t] is known at t-1."""
    r = np.asarray(r, float)
    h = np.empty(len(r))
    h[0] = np.var(r[:50]) if init is None else init
    for t in range(1, len(r)):
        h[t] = lam * h[t - 1] + (1 - lam) * r[t - 1] ** 2
    return h


def garch_filter(params, r, kind: str = "garch") -> np.ndarray:
    """Conditional variances h_t (each known at t-1) for 'garch' (omega, alpha, beta), 'gjr' (omega, alpha, gamma, beta)
    or 'egarch' (omega, alpha, gamma, beta, on log h)."""
    r = np.asarray(r, float)
    n = len(r)
    h = np.empty(n)
    h[0] = np.var(r)
    if kind == "garch":
        w, a, b = params
        for t in range(1, n):
            h[t] = w + a * r[t - 1] ** 2 + b * h[t - 1]
    elif kind == "gjr":
        w, a, g, b = params
        for t in range(1, n):
            h[t] = w + (a + g * (r[t - 1] < 0)) * r[t - 1] ** 2 + b * h[t - 1]
    elif kind == "egarch":
        w, a, g, b = params
        lh = np.log(h[0])
        Ez = np.sqrt(2 / np.pi)
        for t in range(1, n):
            z = r[t - 1] / np.sqrt(np.exp(lh))
            lh = float(np.clip(w + a * (abs(z) - Ez) + g * z + b * lh, -50, 50))
            h[t] = np.exp(lh)
    else:
        raise ValueError(kind)
    return h


def _nll(params, r, kind):
    h = garch_filter(params, r, kind)
    if not np.all(np.isfinite(h)) or np.any(h <= 0):
        return 1e18
    return float(0.5 * np.sum(np.log(2 * np.pi * h) + r ** 2 / h))


def garch_fit(r, kind: str = "garch") -> dict:
    """Gaussian (quasi-) maximum likelihood.  ``r`` should be demeaned.  Returns params, log-likelihood, persistence and
    the fitted variances."""
    r = np.asarray(r, float)
    v = np.var(r)
    if kind == "garch":
        x0, bounds = [0.05 * v, 0.08, 0.9], [(1e-12, 10 * v), (1e-6, 0.5), (0.0, 0.9999)]
        cons = [{"type": "ineq", "fun": lambda p: 0.9999 - p[1] - p[2]}]
    elif kind == "gjr":
        x0, bounds = [0.05 * v, 0.03, 0.08, 0.9], [(1e-12, 10 * v), (0.0, 0.5), (0.0, 0.5), (0.0, 0.9999)]
        cons = [{"type": "ineq", "fun": lambda p: 0.9999 - p[1] - p[2] / 2 - p[3]}]
    else:
        x0, bounds = [0.0, 0.15, -0.08, 0.97], [(-5, 5), (-1, 1), (-1, 1), (-0.9999, 0.9999)]
        cons = []
        x0[0] = (1 - x0[3]) * np.log(v)
    res = optimize.minimize(_nll, x0, args=(r, kind), method="SLSQP", bounds=bounds, constraints=cons,
                            options={"maxiter": 500, "ftol": 1e-10})
    p = res.x
    h = garch_filter(p, r, kind)
    if kind == "garch":
        pers = p[1] + p[2]
    elif kind == "gjr":
        pers = p[1] + p[2] / 2 + p[3]
    else:
        pers = p[3]
    return {"params": p, "loglik": -float(res.fun), "persistence": float(pers), "h": h, "kind": kind,
            "half_life": float(np.log(0.5) / np.log(pers)) if 0 < pers < 1 else float("inf")}


def garch_forecast(params, r_last: float, h_last: float, steps: int, kind: str = "garch") -> np.ndarray:
    """Multi-step variance forecasts for GARCH(1,1) and GJR (mean reversion to the unconditional variance)."""
    if kind == "garch":
        w, a, b = params
        pers = a + b
        nxt = w + a * r_last ** 2 + b * h_last
    else:
        w, a, g, b = params
        pers = a + g / 2 + b
        nxt = w + (a + g * (r_last < 0)) * r_last ** 2 + b * h_last
    vbar = w / (1 - pers)
    k = np.arange(steps)
    return vbar + pers ** k * (nxt - vbar)


# ---------------------------------------------------------------------------
def _har_design(rv, rq=None):
    rv = np.asarray(rv, float)
    n = len(rv)
    d = rv[21:n - 1]
    w = np.array([rv[t - 4:t + 1].mean() for t in range(21, n - 1)])
    m = np.array([rv[t - 21:t + 1].mean() for t in range(21, n - 1)])
    X = [d, w, m]
    if rq is not None:
        X.append(np.sqrt(np.asarray(rq, float)[21:n - 1]) * d)
    return np.column_stack(X), rv[22:]


def har_fit(rv, rq=None) -> dict:
    """HAR-RV: RV_{t+1} = b0 + bd RV_t + bw RV_{t-4:t} + bm RV_{t-21:t}.  With ``rq`` (realized quarticity), HARQ adds
    sqrt(RQ_t) RV_t so that the daily coefficient falls when RV is measured noisily."""
    X, y = _har_design(rv, rq)
    Xd = np.column_stack([np.ones(len(X)), X])
    beta, *_ = np.linalg.lstsq(Xd, y, rcond=None)
    return {"beta": beta, "fitted": Xd @ beta}


def har_predict(beta, rv, rq=None) -> np.ndarray:
    """One-step forecasts for every t >= 21 using the given coefficients (forecast for t+1 made at t)."""
    X, _ = _har_design(np.concatenate([rv, [np.nan]]), None if rq is None else np.concatenate([rq, [np.nan]]))
    return np.column_stack([np.ones(len(X)), X]) @ beta


# ---------------------------------------------------------------------------
def qlike(forecast, realized) -> np.ndarray:
    """Patton (2011): robust to noise in the realized proxy; minimized in expectation by the true conditional variance."""
    f, r = np.asarray(forecast, float), np.asarray(realized, float)
    return r / f - np.log(r / f) - 1


def mse(forecast, realized) -> np.ndarray:
    return (np.asarray(forecast, float) - np.asarray(realized, float)) ** 2


def diebold_mariano(loss_a, loss_b, lags: int = 5) -> dict:
    """DM test of equal predictive accuracy: d = loss_a - loss_b; t-statistic with a Newey-West variance.  Negative t
    means A is better."""
    d = np.asarray(loss_a, float) - np.asarray(loss_b, float)
    d = d[np.isfinite(d)]
    n = len(d)
    dc = d - d.mean()
    v = dc @ dc / n
    for k in range(1, lags + 1):
        v += 2 * (1 - k / (lags + 1)) * (dc[k:] @ dc[:-k]) / n
    t = d.mean() / np.sqrt(v / n)
    from scipy.stats import norm
    return {"mean_diff": float(d.mean()), "t": float(t), "p": float(2 * norm.sf(abs(t)))}


# ---------------------------------------------------------------------------
def acf(x, lags: int = 20) -> np.ndarray:
    x = np.asarray(x, float) - np.mean(x)
    v = x @ x
    return np.array([x[k:] @ x[:-k] / v if k else 1.0 for k in range(lags + 1)])


def ar_fit(x, p: int = 1) -> dict:
    x = np.asarray(x, float)
    X = np.column_stack([np.ones(len(x) - p)] + [x[p - k - 1:len(x) - k - 1] for k in range(p)])
    y = x[p:]
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    return {"beta": beta, "sigma": float(resid.std(ddof=p + 1)), "resid": resid}


ADF_5PCT = -2.86  # MacKinnon (1996), constant, no trend, large sample


def adf(x, lags: int = 1) -> dict:
    """Augmented Dickey-Fuller with a constant: dx_t = a + g x_{t-1} + sum c_k dx_{t-k} + e.  Reject a unit root when t
    is below -2.86 (5%)."""
    x = np.asarray(x, float)
    dx = np.diff(x)
    n = len(dx)
    rows = n - lags
    X = [np.ones(rows), x[lags:-1]]
    X += [dx[lags - k - 1:n - k - 1] for k in range(lags)]
    X = np.column_stack(X)
    y = dx[lags:]
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    s2 = resid @ resid / (rows - X.shape[1])
    se = np.sqrt(s2 * np.linalg.inv(X.T @ X)[1, 1])
    t = beta[1] / se
    return {"gamma": float(beta[1]), "t": float(t), "reject_5pct": bool(t < ADF_5PCT)}


EG_5PCT = -3.34  # Engle-Granger, two variables, constant (MacKinnon 1991)


def engle_granger(y, x, lags: int = 1) -> dict:
    """Regress y on x, test the residual for a unit root (critical value -3.34 at 5% for two variables)."""
    y, x = np.asarray(y, float), np.asarray(x, float)
    X = np.column_stack([np.ones(len(x)), x])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    u = y - X @ beta
    a = adf(u, lags)
    return {"beta": beta, "resid": u, "t": a["t"], "cointegrated_5pct": bool(a["t"] < EG_5PCT)}


# ---------------------------------------------------------------------------
def markov_switching(x, n_iter: int = 200, seed=0) -> dict:
    """Hamilton (1989) two-regime Gaussian mixture with Markov switching, by EM (Hamilton filter + Kim smoother).
    Regime 1 is the high-variance one.  Returns means, sds, transition matrix and smoothed regime-1 probabilities."""
    x = np.asarray(x, float)
    n = len(x)
    mu = np.array([np.mean(x), np.mean(x)])
    sd = np.array([0.7 * np.std(x), 1.8 * np.std(x)])
    P = np.array([[0.97, 0.03], [0.1, 0.9]])
    pi = np.array([0.8, 0.2])
    for _ in range(n_iter):
        dens = np.exp(-0.5 * ((x[:, None] - mu) / sd) ** 2) / (np.sqrt(2 * np.pi) * sd)
        filt = np.empty((n, 2))
        pred = np.empty((n, 2))
        p = pi
        ll = 0.0
        for t in range(n):
            pred[t] = p
            f = p * dens[t]
            s = f.sum()
            ll += np.log(s)
            filt[t] = f / s
            p = filt[t] @ P
        sm = np.empty((n, 2))
        sm[-1] = filt[-1]
        for t in range(n - 2, -1, -1):
            ratio = sm[t + 1] / np.maximum(pred[t + 1], 1e-300)
            sm[t] = filt[t] * (P @ ratio)
        # transitions
        xi = np.zeros((2, 2))
        for t in range(n - 1):
            m = (filt[t][:, None] * P) * (sm[t + 1] / np.maximum(pred[t + 1], 1e-300))[None, :]
            xi += m
        P = xi / xi.sum(axis=1, keepdims=True)
        w = sm
        mu = (w * x[:, None]).sum(axis=0) / w.sum(axis=0)
        sd = np.sqrt((w * (x[:, None] - mu) ** 2).sum(axis=0) / w.sum(axis=0))
        pi = sm[0]
    order = np.argsort(sd)
    return {"mu": mu[order], "sd": sd[order], "P": P[np.ix_(order, order)], "prob_high": sm[:, order[1]],
            "loglik": float(ll), "duration": 1 / (1 - np.diag(P[np.ix_(order, order)]))}


def kalman_local_level(y, q=None, r=None) -> dict:
    """y_t = m_t + e (var r), m_t = m_{t-1} + w (var q).  If q, r are None they are fitted by maximum likelihood."""
    y = np.asarray(y, float)

    def run(q_, r_):
        m, P = y[0], np.var(y)
        ms, ll = np.empty(len(y)), 0.0
        for t, obs in enumerate(y):
            P = P + q_
            S = P + r_
            k = P / S
            v = obs - m
            ll += -0.5 * (np.log(2 * np.pi * S) + v * v / S)
            m = m + k * v
            P = (1 - k) * P
            ms[t] = m
        return ms, ll

    if q is None or r is None:
        v = np.var(np.diff(y))
        res = optimize.minimize(lambda p: -run(np.exp(p[0]), np.exp(p[1]))[1], [np.log(v / 10), np.log(v / 2)],
                                method="Nelder-Mead")
        q, r = np.exp(res.x)
    ms, ll = run(q, r)
    return {"level": ms, "q": float(q), "r": float(r), "loglik": float(ll), "signal_to_noise": float(q / r)}


# ---------------------------------------------------------------------------
def dcc_fit(r1, r2) -> dict:
    """Engle (2002), two assets, two steps: GARCH(1,1) on each, then DCC(1,1) on the standardized residuals."""
    g1, g2 = garch_fit(r1), garch_fit(r2)
    z = np.column_stack([np.asarray(r1) / np.sqrt(g1["h"]), np.asarray(r2) / np.sqrt(g2["h"])])
    Qbar = np.cov(z.T)

    def corr_path(a, b):
        Q = Qbar.copy()
        rho = np.empty(len(z))
        for t in range(len(z)):
            d = np.sqrt(np.diag(Q))
            rho[t] = Q[0, 1] / (d[0] * d[1])
            Q = (1 - a - b) * Qbar + a * np.outer(z[t], z[t]) + b * Q
        return rho

    def nll(p):
        a, b = p
        if a < 0 or b < 0 or a + b >= 0.999:
            return 1e18
        rho = corr_path(a, b)
        rho = np.clip(rho, -0.999, 0.999)
        q = (z[:, 0] ** 2 + z[:, 1] ** 2 - 2 * rho * z[:, 0] * z[:, 1]) / (1 - rho ** 2)
        return float(0.5 * np.sum(np.log(1 - rho ** 2) + q))

    res = optimize.minimize(nll, [0.03, 0.95], method="Nelder-Mead")
    a, b = res.x
    return {"a": float(a), "b": float(b), "rho": corr_path(a, b), "garch1": g1["params"], "garch2": g2["params"]}
