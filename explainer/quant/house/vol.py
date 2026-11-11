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
    """Gaussian (quasi-) maximum likelihood.  ``r`` should be demeaned.  The fit runs on returns scaled to unit variance
    (well conditioned whatever the units) and the parameters are mapped back.  Returns params, log-likelihood,
    persistence and the fitted variances."""
    r = np.asarray(r, float)
    v = float(np.var(r))
    z = r / np.sqrt(v)
    if kind == "garch":
        x0, bounds = [0.05, 0.08, 0.9], [(1e-8, 10.0), (1e-6, 0.5), (0.0, 0.9999)]
        cons = [{"type": "ineq", "fun": lambda p: 0.9999 - p[1] - p[2]}]
    elif kind == "gjr":
        x0, bounds = [0.05, 0.03, 0.08, 0.9], [(1e-8, 10.0), (0.0, 0.5), (0.0, 0.5), (0.0, 0.9999)]
        cons = [{"type": "ineq", "fun": lambda p: 0.9999 - p[1] - p[2] / 2 - p[3]}]
    else:
        x0, bounds = [0.0, 0.15, -0.08, 0.97], [(-5, 5), (-1, 1), (-1, 1), (-0.9999, 0.9999)]
        cons = []
    best = None
    for start in (x0, [x0[0]] + [0.5 * xx for xx in x0[1:-1]] + [min(0.95, x0[-1])]):
        res = optimize.minimize(_nll, start, args=(z, kind), method="SLSQP", bounds=bounds, constraints=cons,
                                options={"maxiter": 1000, "ftol": 1e-12})
        if best is None or res.fun < best.fun:
            best = res
    p = np.array(best.x, float)
    hz = garch_filter(p, z, kind)
    if kind in ("garch", "gjr"):
        p[0] *= v
    else:
        p[0] += (1 - p[3]) * np.log(v)
    h = hz * v
    loglik = -float(best.fun) - 0.5 * len(r) * np.log(v)
    if kind == "garch":
        pers = p[1] + p[2]
    elif kind == "gjr":
        pers = p[1] + p[2] / 2 + p[3]
    else:
        pers = p[3]
    return {"params": p, "loglik": loglik, "persistence": float(pers), "h": h, "kind": kind,
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


def clark_west(y, f_small, f_big, lags: int = 0) -> dict:
    """Clark and West's (2007) test of a small model nested in a big one: the big model's squared error is adjusted
    by (f_small - f_big)^2, the noise its extra, estimated parameters add under the null, and the mean of
    e_small^2 - (e_big^2 - (f_small - f_big)^2) is tested one-sided with a Newey-West variance.  Positive t: the big
    model is better.  Also returns the unadjusted Diebold-Mariano t in the same direction."""
    y, a, b = (np.asarray(v, float) for v in (y, f_small, f_big))
    ok = np.isfinite(y) & np.isfinite(a) & np.isfinite(b)
    y, a, b = y[ok], a[ok], b[ok]
    e1, e2 = y - a, y - b
    out = {}
    for key, d in (("cw", e1 ** 2 - (e2 ** 2 - (a - b) ** 2)), ("dm", e1 ** 2 - e2 ** 2)):
        n = len(d)
        dc = d - d.mean()
        v = dc @ dc / n
        for k in range(1, lags + 1):
            v += 2 * (1 - k / (lags + 1)) * (dc[k:] @ dc[:-k]) / n
        out[key] = float(d.mean() / np.sqrt(v / n))
    from scipy.stats import norm
    return {"t_cw": out["cw"], "t_dm": out["dm"], "p_cw": float(norm.sf(out["cw"])), "p_dm": float(norm.sf(out["dm"])),
            "n": int(len(y))}


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


# ---------------------------------------------------------------------------
# Part 7, extended: identification, unit roots, cointegration, hidden states, the GARCH zoo, jumps, scoring, industry
# (statsmodels and arch are not dependencies: each tool is a few lines of numpy, tested against simulations)
def ljung_box(x, m: int = 10) -> dict:
    """Ljung and Box (1978): Q = T(T+2) sum_{k<=m} rho_k^2 / (T-k), chi-squared with m degrees of freedom under white
    noise."""
    from scipy.stats import chi2
    x = np.asarray(x, float)
    T = len(x)
    rho = acf(x, m)[1:]
    Q = float(T * (T + 2) * np.sum(rho ** 2 / (T - np.arange(1, m + 1))))
    return {"Q": Q, "p": float(chi2.sf(Q, m)), "m": int(m)}


def _arma_resid(params, x, p, q):
    c, ph, th = params[0], params[1:1 + p], params[1 + p:1 + p + q]
    e = np.zeros(len(x))
    for t in range(len(x)):
        v = x[t] - c
        for i in range(p):
            if t - i - 1 >= 0:
                v -= ph[i] * x[t - i - 1]
        for j in range(q):
            if t - j - 1 >= 0:
                v -= th[j] * e[t - j - 1]
        e[t] = v
    return e


def arma_fit(x, p: int = 1, q: int = 0) -> dict:
    """ARMA(p, q) with a constant by conditional sum of squares (Box and Jenkins 1970): minimise the sum of squared
    one-step errors e_t = x_t - c - sum phi_i x_{t-i} - sum theta_j e_{t-j}.  Gaussian log-likelihood and AIC."""
    x = np.asarray(x, float)
    start = list(ar_fit(x, p)["beta"]) + [0.0] * q if p else [float(np.mean(x))] + [0.1] * q
    res = optimize.minimize(lambda b: np.sum(_arma_resid(b, x, p, q)[p:] ** 2), start, method="Nelder-Mead",
                            options={"maxiter": 4000, "xatol": 1e-7, "fatol": 1e-9})
    e = _arma_resid(res.x, x, p, q)[p:]
    n = len(e)
    s2 = float(e @ e / n)
    ll = float(-0.5 * n * (np.log(2 * np.pi * s2) + 1))
    k = p + q + 2
    return {"const": float(res.x[0]), "phi": res.x[1:1 + p], "theta": res.x[1 + p:], "sigma2": s2, "loglik": ll,
            "aic": float(-2 * ll + 2 * k), "resid": e}


def df_simulate(T: int = 500, n: int = 20000, seed: int = 0, chunk: int = 2000) -> np.ndarray:
    """The Dickey-Fuller t-statistic (constant, no lags) on ``n`` simulated random walks of length ``T``: its
    distribution under the unit root, which is not N(0, 1)."""
    rng = np.random.default_rng(seed)
    out = []
    for i in range(0, n, chunk):
        m = min(chunk, n - i)
        x = np.cumsum(rng.standard_normal((m, T + 1)), axis=1)
        y, z = np.diff(x, axis=1), x[:, :-1]
        yc = y - y.mean(1, keepdims=True)
        zc = z - z.mean(1, keepdims=True)
        g = np.sum(yc * zc, 1) / np.sum(zc * zc, 1)
        u = yc - g[:, None] * zc
        s2 = np.sum(u * u, 1) / (T - 2)
        out.append(g / np.sqrt(s2 / np.sum(zc * zc, 1)))
    return np.concatenate(out)


# 5% (and 10%, 1%) trace critical values with an unrestricted constant (Osterwald-Lenum 1992; the values statsmodels
# tabulates for det_order=0), indexed by n - r, the number of common trends tested for.
JOHANSEN_TRACE = {1: (2.7055, 3.8415, 6.6349), 2: (13.4294, 15.4943, 19.9349), 3: (27.0669, 29.7961, 35.4628),
                  4: (44.4929, 47.8545, 54.6815)}


def johansen(X, k: int = 1) -> dict:
    """Johansen (1991): the VECM dX_t = Pi X_{t-1} + sum_{i<k} G_i dX_{t-i} + c + e, Pi = alpha beta'.  Reduced-rank
    regression: the squared canonical correlations lambda_i of dX_t and X_{t-1} (both purged of the lagged differences
    and the constant), and the trace statistics -T sum_{i>r} ln(1 - lambda_i) for r = 0, 1, ...  ``beta`` columns are
    the cointegrating vectors, strongest first; ``rank`` is the 5% trace test's verdict."""
    X = np.asarray(X, float)
    dX = np.diff(X, axis=0)
    n = X.shape[1]
    Z0 = dX[k - 1:]
    Z1 = X[k - 1:-1]
    W = [np.ones((len(Z0), 1))] + [dX[k - 1 - i:len(dX) - i] for i in range(1, k)]
    W = np.column_stack(W)

    def purge(A):
        b, *_ = np.linalg.lstsq(W, A, rcond=None)
        return A - W @ b

    R0, R1 = purge(Z0), purge(Z1)
    T = len(R0)
    S00, S11, S01 = R0.T @ R0 / T, R1.T @ R1 / T, R0.T @ R1 / T
    M = np.linalg.solve(S11, S01.T @ np.linalg.solve(S00, S01))
    lam, V = np.linalg.eig(M)
    lam, V = lam.real, V.real
    o = np.argsort(lam)[::-1]
    lam, V = lam[o], V[:, o]
    V = V / np.sqrt(np.einsum("ij,jk,ki->i", V.T, S11, V))[None, :]
    trace = np.array([-T * np.sum(np.log(1 - lam[r:])) for r in range(n)])
    crit = np.array([JOHANSEN_TRACE[n - r][1] for r in range(n)])
    rank = int(np.argmax(trace < crit)) if np.any(trace < crit) else n
    alpha = S01 @ V
    return {"eig": lam, "trace": trace, "crit5": crit, "rank": rank, "beta": V, "alpha": alpha, "T": T}


def ecm_fit(y, x) -> dict:
    """Engle-Granger's second step: the error-correction model for both legs, dy_t = a_y u_{t-1} + e and
    dx_t = a_x u_{t-1} + e, with u the first step's residual.  The leg with the larger |a| does the correcting."""
    from explainer.quant.house import econ
    eg = engle_granger(y, x)
    u = eg["resid"]
    fy = econ.ols(np.diff(y), u[:-1])
    fx = econ.ols(np.diff(x), u[:-1])
    return {"alpha_y": float(fy["beta"][1]), "t_y": float(fy["t"][1]), "alpha_x": float(fx["beta"][1]),
            "t_x": float(fx["t"][1]), "beta": eg["beta"], "u": u}


def hamilton_filter(x, mu, sd, P, pi0=None) -> dict:
    """The Hamilton (1989) filter for given parameters: predicted and filtered regime probabilities, each step Bayes
    (multiply by the densities, renormalise) then a Markov prediction xi_{t+1|t} = P' xi_{t|t}."""
    x = np.asarray(x, float)
    mu, sd, P = np.asarray(mu, float), np.asarray(sd, float), np.asarray(P, float)
    k = len(mu)
    p = np.full(k, 1 / k) if pi0 is None else np.asarray(pi0, float)
    pred, filt, dens = np.empty((len(x), k)), np.empty((len(x), k)), np.empty((len(x), k))
    ll = 0.0
    for t, v in enumerate(x):
        pred[t] = p
        dens[t] = np.exp(-0.5 * ((v - mu) / sd) ** 2) / (np.sqrt(2 * np.pi) * sd)
        f = p * dens[t]
        s = f.sum()
        ll += np.log(s)
        filt[t] = f / s
        p = filt[t] @ P
    return {"pred": pred, "filt": filt, "dens": dens, "loglik": float(ll)}


def kalman_states(y, q: float, r: float, m0=None, P0=None) -> dict:
    """The local-level filter step by step: prior variance P- = P + q, gain K = P- / (P- + r), mean m + K (y - m),
    posterior variance (1 - K) P-.  Every intermediate is returned (for drawing the belief)."""
    y = np.asarray(y, float)
    n = len(y)
    m = y[0] if m0 is None else m0
    P = np.var(y) if P0 is None else P0
    out = {k: np.empty(n) for k in ("m_prior", "P_prior", "K", "m", "P")}
    for t in range(n):
        Pm = P + q
        K = Pm / (Pm + r)
        out["m_prior"][t], out["P_prior"][t], out["K"][t] = m, Pm, K
        m = m + K * (y[t] - m)
        P = (1 - K) * Pm
        out["m"][t], out["P"][t] = m, P
    return out


def steady_gain(q_over_r) -> np.ndarray:
    """The local level's steady-state Kalman gain from the signal-to-noise ratio q/r: p = (q + sqrt(q^2 + 4q)) / 2
    (prior variance in units of r), K = p / (1 + p)."""
    q = np.asarray(q_over_r, float)
    p = (q + np.sqrt(q * q + 4 * q)) / 2
    return p / (1 + p)


LOG_CHI2_MEAN = -1.2703628454614782  # E ln chi2_1 = psi(1/2) + ln 2
LOG_CHI2_VAR = np.pi ** 2 / 2  # Var ln chi2_1


def sv_qml(r, c: float = 1e-10) -> dict:
    """Stochastic volatility by quasi-maximum likelihood (Harvey, Ruiz and Shephard 1994): y_t = ln(r_t^2 + c) =
    h_t + ln z_t^2, h_t = mu + phi (h_{t-1} - mu) + eta_t.  ln z^2 is treated as Gaussian with its true mean -1.27 and
    variance pi^2/2, and the Kalman filter gives the likelihood.  Returns phi, sigma_eta, mu, the filtered and the
    smoothed log variance."""
    y = np.log(np.asarray(r, float) ** 2 + c) - LOG_CHI2_MEAN
    R = LOG_CHI2_VAR

    def run(th, keep=False):
        phi, s2, mu = np.tanh(th[0]), np.exp(th[1]), th[2]
        a, P = mu, s2 / max(1 - phi ** 2, 1e-6)
        ll = 0.0
        if keep:
            A, PP, Ap, Pp = (np.empty(len(y)) for _ in range(4))
        for t, v in enumerate(y):
            S = P + R
            e = v - a
            ll += -0.5 * (np.log(2 * np.pi * S) + e * e / S)
            K = P / S
            af, Pf = a + K * e, P * (1 - K)
            if keep:
                Ap[t], Pp[t], A[t], PP[t] = a, P, af, Pf
            a = mu + phi * (af - mu)
            P = phi * phi * Pf + s2
        return (ll, A, PP, Ap, Pp) if keep else ll

    res = optimize.minimize(lambda th: -run(th), [np.arctanh(0.97), np.log(0.05), float(np.mean(y))],
                            method="Nelder-Mead", options={"maxiter": 3000, "xatol": 1e-6, "fatol": 1e-6})
    ll, A, PP, Ap, Pp = run(res.x, keep=True)
    phi, s2, mu = np.tanh(res.x[0]), np.exp(res.x[1]), res.x[2]
    sm = A.copy()
    for t in range(len(y) - 2, -1, -1):  # Rauch-Tung-Striebel smoother
        J = PP[t] * phi / Pp[t + 1]
        sm[t] = A[t] + J * (sm[t + 1] - Ap[t + 1])
    return {"phi": float(phi), "sigma_eta": float(np.sqrt(s2)), "mu": float(mu), "loglik": float(ll), "filtered": A,
            "smoothed": sm}


def _nll_t(params, z):
    w, a, b, nu = params
    if nu <= 2.05 or w <= 0 or a < 0 or b < 0 or a + b >= 0.9999:
        return 1e18
    from scipy.special import gammaln
    h = garch_filter((w, a, b), z, "garch")
    c = gammaln((nu + 1) / 2) - gammaln(nu / 2) - 0.5 * np.log(np.pi * (nu - 2))
    return float(-np.sum(c - 0.5 * np.log(h) - (nu + 1) / 2 * np.log1p(z ** 2 / (h * (nu - 2)))))


def garch_t_fit(r) -> dict:
    """GARCH(1,1) with standardized Student-t innovations (Bollerslev 1987) by maximum likelihood: the degrees of
    freedom nu measure how fat the tails of z_t = r_t / sigma_t are."""
    r = np.asarray(r, float)
    v = float(np.var(r))
    z = r / np.sqrt(v)
    res = optimize.minimize(_nll_t, [0.01, 0.08, 0.9, 8.0], args=(z,), method="Nelder-Mead",
                            options={"maxiter": 4000, "xatol": 1e-7, "fatol": 1e-7})
    w, a, b, nu = res.x
    return {"params": np.array([w * v, a, b]), "nu": float(nu), "loglik": -float(res.fun) - 0.5 * len(r) * np.log(v),
            "h": garch_filter((w, a, b), z, "garch") * v}


def news_impact(params, kind: str, r, h: float) -> np.ndarray:
    """Engle and Ng's (1993) news-impact curve: tomorrow's variance as a function of today's return r, with today's
    variance held at h."""
    r = np.asarray(r, float)
    if kind == "garch":
        w, a, b = params
        return w + a * r ** 2 + b * h
    if kind == "gjr":
        w, a, g, b = params
        return w + (a + g * (r < 0)) * r ** 2 + b * h
    w, a, g, b = params
    z = r / np.sqrt(h)
    return np.exp(w + a * (np.abs(z) - np.sqrt(2 / np.pi)) + g * z + b * np.log(h))


def nelson_elog(alpha, beta, n: int = 80) -> np.ndarray:
    """E ln(alpha z^2 + beta) for z ~ N(0, 1), by Gauss-Hermite quadrature: GARCH(1,1) is strictly stationary iff this
    is negative (Nelson 1990), which allows alpha + beta >= 1."""
    x, w = np.polynomial.hermite_e.hermegauss(n)
    w = w / w.sum()
    a, b = np.broadcast_arrays(np.asarray(alpha, float), np.asarray(beta, float))
    return np.sum(w * np.log(a[..., None] * x ** 2 + b[..., None]), axis=-1)


def signature_plot(logp, steps=(1, 2, 3, 5, 10, 15, 20, 30, 60)) -> np.ndarray:
    """Realized variance of one day's log prices sampled every k observations (averaged over the k offsets), for
    each k in ``steps``: RV against the sampling interval (Andersen, Bollerslev, Diebold and Labys 2000)."""
    x = np.asarray(logp, float)
    return np.array([np.mean([np.sum(np.diff(x[o::k]) ** 2) for o in range(k)]) for k in steps])


def bns_jump_z(r) -> float:
    """Barndorff-Nielsen and Shephard's (2006) ratio jump test for one day's intraday returns:
    z = ((RV - BV)/RV) / sqrt((pi^2/4 + pi - 5) max(1, TQ/BV^2) / n), N(0, 1) without jumps; TQ is tripower quarticity."""
    from scipy.special import gamma
    r = np.abs(np.asarray(r, float))
    n = len(r)
    rv = np.sum(r ** 2)
    bv = np.pi / 2 * np.sum(r[1:] * r[:-1])
    mu43 = 2 ** (2 / 3) * gamma(7 / 6) / gamma(1 / 2)
    tq = n * mu43 ** -3 * np.sum((r[2:] * r[1:-1] * r[:-2]) ** (4 / 3))
    return float(((rv - bv) / rv) / np.sqrt((np.pi ** 2 / 4 + np.pi - 5) * max(1.0, tq / bv ** 2) / n))


def har_cj(rv, bv, jump, rq=None) -> dict:
    """HAR-CJ (Andersen, Bollerslev and Diebold 2007): the HAR averages of the continuous part C = RV - J and the
    jump part J (``jump``: J_t, zero on days without a significant jump) as separate regressors."""
    rv, J = np.asarray(rv, float), np.asarray(jump, float)
    C = rv - J
    Xc, y = _har_design(C)
    Xj, _ = _har_design(J)
    y = rv[22:]
    X = np.column_stack([np.ones(len(y)), Xc, Xj[:, 0]])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    return {"beta": beta, "fitted": X @ beta}


def mincer_zarnowitz(forecast, realized, lags: int = 5) -> dict:
    """Mincer and Zarnowitz (1969): regress the realized value on the forecast; an unbiased, efficient forecast has
    a = 0, b = 1.  Newey-West t-statistics for b = 1 and a = 0."""
    from explainer.quant.house import econ
    f = econ.ols(np.asarray(realized, float), np.asarray(forecast, float), se="nw", lags=lags)
    a, b = f["beta"]
    se = f["beta"] / f["t"]
    return {"a": float(a), "b": float(b), "t_b1": float((b - 1) / se[1]), "t_a0": float(f["t"][0]), "r2": float(f["r2"])}


def model_confidence_set(losses, names, alpha: float = 0.10, B: int = 2000, block: int = 10, seed: int = 0) -> dict:
    """Hansen, Lunde and Nason's (2011) model confidence set with the T_max statistic and a stationary bootstrap:
    eliminate the worst model while equal predictive ability is rejected at ``alpha``.  ``losses`` is T x M."""
    L = np.asarray(losses, float)
    T, M = L.shape
    rng = np.random.default_rng(seed)
    idx = np.empty((B, T), int)
    jump = rng.random((B, T)) < 1 / block  # stationary bootstrap (Politis and Romano 1994), mean block ``block``
    jump[:, 0] = True
    fresh = rng.integers(T, size=(B, T))
    for t in range(T):
        idx[:, t] = np.where(jump[:, t], fresh[:, t], (idx[:, t - 1] + 1) % T if t else 0)
    alive = list(range(M))
    order, pvals = [], []
    pmax = 0.0
    while len(alive) > 1:
        Ls = L[:, alive]
        dbar = Ls.mean(0) - Ls.mean()
        boot = Ls[idx].mean(1)
        bd = boot - boot.mean(1, keepdims=True)
        var = np.mean((bd - dbar) ** 2, 0)
        t = dbar / np.sqrt(var)
        tb = np.max((bd - dbar) / np.sqrt(var), 1)
        p = float(np.mean(tb >= t.max()))
        pmax = max(pmax, p)
        if pmax >= alpha:
            break
        worst = alive[int(np.argmax(t))]
        order.append(names[worst])
        pvals.append(pmax)
        alive.remove(worst)
    return {"survivors": [names[i] for i in alive], "eliminated": order, "p": pvals}


def vol_target(r, target: float = 0.10, com: float = 60.0, lag: int = 2, ann: float = 252.0, cap: float = 10.0) -> dict:
    """Volatility targeting (Harvey et al. 2018; Moreira and Muir 2017): scale r_t by target / sigma_{t-lag}, with
    sigma an exponentially weighted volatility of daily returns of centre of mass ``com`` days (Moskowitz, Ooi and
    Pedersen 2012 use 60), annualised.  Returns the weights and the scaled returns."""
    r = np.asarray(r, float)
    d = com / (1 + com)
    s2 = np.empty(len(r))
    s2[0] = np.var(r[:60])
    for t in range(1, len(r)):
        s2[t] = d * s2[t - 1] + (1 - d) * r[t - 1] ** 2
    sig = np.sqrt(s2 * ann)
    w = np.full(len(r), np.nan)
    w[lag:] = np.minimum(target / sig[:-lag], cap)
    return {"weight": w, "scaled": w * r, "sigma": sig}


def vra(f, sigma, halflife: float = 42.0) -> np.ndarray:
    """A volatility-regime adjustment in the spirit of Barra's (a replica, not MSCI's published formula): the
    cross-sectional bias statistic B_t^2 = mean_k (f_kt / sigma_kt)^2 of K assets' returns over their forecast vols,
    smoothed by an EWMA of half-life ``halflife`` days; lambda_t = sqrt(EWMA) multiplies every forecast."""
    z2 = np.nanmean((np.asarray(f, float) / np.asarray(sigma, float)) ** 2, axis=1)
    d = 0.5 ** (1 / halflife)
    out = np.empty(len(z2))
    acc = 1.0
    for t, v in enumerate(z2):
        out[t] = np.sqrt(acc)  # known before day t
        if np.isfinite(v):
            acc = d * acc + (1 - d) * v
    return out


def forecast(rv, horizon: int = 22) -> dict:
    """The House's volatility forecast from daily realized variances: log-HAR for tomorrow (with the log-normal
    mean), iterated forward for the term structure; returns the daily variance path and the average over ``horizon``
    days, annualised as volatility (365 days, for a market that never closes)."""
    lrv = np.log(np.asarray(rv, float))
    fit = har_fit(lrv)
    _, y = _har_design(lrv)
    s2 = float(np.var(y - fit["fitted"]))
    path = list(lrv)
    out = []
    for _ in range(horizon):
        nxt = har_predict(fit["beta"], np.array(path))[-1]
        path.append(nxt)
        out.append(np.exp(nxt + 0.5 * s2))
    out = np.array(out)
    return {"daily": out, "next_vol": float(np.sqrt(out[0] * 365)), "avg_vol": float(np.sqrt(out.mean() * 365)),
            "beta": fit["beta"]}
