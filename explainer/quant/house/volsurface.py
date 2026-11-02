"""The surface builder (Part 12, the volatility desk): arbitrage-free parametrizations of implied total variance,
the butterfly and calendar checks in total-variance form, Dupire's local volatility, the variance-swap strike, and
the VIX formula.  Tested in ``tests/test_quant_house.py``.

* ``ssvi_w``, ``fit_ssvi``: Gatheral and Jacquier's (2014) surface SVI, w(k, theta) = theta/2 (1 + rho phi k +
  sqrt((phi k + rho)^2 + 1 - rho^2)) with the power-law phi(theta) = eta / (theta^g (1 + theta)^(1 - g)); free of
  calendar arbitrage when theta rises with T, and of butterfly arbitrage when eta (1 + |rho|) <= 2;
* ``g_function``: Gatheral's density condition on a smile w(k): g >= 0 everywhere, or a butterfly is negative;
* ``dupire_local_var``: local variance from total variance and its derivatives (Gatheral 2006, eq. 1.10);
* ``var_swap_strike``: the fair variance from a strip of out-of-the-money options weighted 1/K^2 (Carr and Madan
  1998; Demeterfi, Derman, Kamal and Zou 1999);
* ``vix``: the CBOE's discretization of the same integral, with its forward correction.
"""

from __future__ import annotations

import numpy as np
from scipy import optimize


def phi_power(theta, eta, gam):
    theta = np.asarray(theta, float)
    return eta / (theta ** gam * (1 + theta) ** (1 - gam))


def ssvi_w(k, theta, rho, eta, gam):
    k, theta = np.asarray(k, float), np.asarray(theta, float)
    p = phi_power(theta, eta, gam)
    return 0.5 * theta * (1 + rho * p * k + np.sqrt((p * k + rho) ** 2 + 1 - rho ** 2))


def fit_ssvi(k, T, w, weights=None, theta_atm=None) -> dict:
    """Fit (rho, eta, gamma) and one ATM total variance theta per maturity to quotes (k, T, w = iv^2 T).  ``theta``
    is kept non-decreasing in T (no calendar arbitrage) and eta (1 + |rho|) <= 2 (no butterfly arbitrage)."""
    k, T, w = (np.asarray(a, float) for a in (k, T, w))
    wt = np.ones_like(w) if weights is None else np.asarray(weights, float)
    Ts = np.unique(T)
    if theta_atm is None:
        theta0 = np.array([max(np.interp(0.0, np.sort(k[T == t]), w[T == t][np.argsort(k[T == t])]), 1e-4) for t in Ts])
    else:
        theta0 = np.asarray(theta_atm, float)
    theta0 = np.maximum.accumulate(theta0)
    inc0 = np.diff(np.concatenate([[0.0], theta0]))

    def unpack(x):
        rho, eta, gam = np.tanh(x[0]), np.exp(x[1]), 1 / (1 + np.exp(-x[2]))
        eta = min(eta, 2 / (1 + abs(rho)))
        theta = np.cumsum(np.exp(x[3:]))
        return rho, eta, gam, theta

    def resid(x):
        rho, eta, gam, theta = unpack(x)
        th = theta[np.searchsorted(Ts, T)]
        return np.sqrt(wt) * (ssvi_w(k, th, rho, eta, gam) - w)

    x0 = np.concatenate([[np.arctanh(-0.3), np.log(1.0), 0.0], np.log(np.maximum(inc0, 1e-6))])
    r = optimize.least_squares(resid, x0, max_nfev=5000)
    rho, eta, gam, theta = unpack(r.x)
    return {"rho": float(rho), "eta": float(eta), "gamma": float(gam), "theta": theta, "T": Ts,
            "rmse": float(np.sqrt(np.mean((resid(r.x) / np.sqrt(wt)) ** 2)))}


def theta_at(fit: dict, T):
    """The ATM total variance of an SSVI fit at any maturity: linear between the fitted expiries, from zero at T = 0
    (so the short end keeps its forward variance), and extended past the last expiry at the last forward variance.
    Clamping instead would make the forward variance zero outside the quoted range, and Dupire's local volatility
    with it."""
    Tn = np.concatenate([[0.0], np.asarray(fit["T"], float)])
    th = np.concatenate([[0.0], np.asarray(fit["theta"], float)])
    T = np.asarray(T, float)
    slope = (th[-1] - th[-2]) / (Tn[-1] - Tn[-2])
    return np.where(T > Tn[-1], th[-1] + slope * (T - Tn[-1]), np.interp(T, Tn, th))


def ssvi_surface_w(fit: dict, k, T):
    """Total variance w(k, T) of an SSVI fit at any (k, T)."""
    return ssvi_w(k, theta_at(fit, T), fit["rho"], fit["eta"], fit["gamma"])


def local_vol_fn(fit: dict):
    """Dupire's local volatility sigma(k, t) of an SSVI fit, by finite differences (k = log S/F, zero rates)."""
    f = lambda k, T: ssvi_surface_w(fit, k, T)  # noqa: E731

    def lv(k, t):
        t = max(t, 0.25 / 365)
        w, dw, d2w, dT = numeric_derivs(f, k, t, h=2e-3, hT=min(2e-3, 0.5 * t))
        return np.sqrt(np.clip(dupire_local_var(k, w, dw, d2w, dT), 1e-4, 25.0))
    return lv


def local_vol_paths(fit: dict, days: int, n_paths: int, seed=0, substeps=4) -> np.ndarray:
    """Daily log(S_t/S_0) under Dupire's local volatility of an SSVI fit (log-Euler, ``substeps`` per day: the short
    end is steep, and a daily step underprices by about a vol point). Returns (days + 1, n_paths)."""
    lv = local_vol_fn(fit)
    g = np.random.default_rng(seed)
    h = 1 / 365 / substeps
    X = np.zeros((days + 1, n_paths))
    x = np.zeros(n_paths)
    for i in range(days):
        for j in range(substeps):
            s = lv(np.clip(x, -1.2, 1.2), (i * substeps + j + 1) * h)
            x = x - 0.5 * s * s * h + s * np.sqrt(h) * g.standard_normal(n_paths)
        X[i + 1] = x
    return X


# ---------------------------------------------------------------------------
def g_function(k, w, dw, d2w):
    """Gatheral's g(k) = (1 - k w'/(2w))^2 - (w'^2/4)(1/w + 1/4) + w''/2; the implied density is proportional to g
    times a positive factor, so g < 0 anywhere is a butterfly arbitrage."""
    k, w, dw, d2w = (np.asarray(a, float) for a in (k, w, dw, d2w))
    return (1 - k * dw / (2 * w)) ** 2 - dw ** 2 / 4 * (1 / w + 0.25) + d2w / 2


def dupire_local_var(k, w, dw, d2w, dwdT):
    """Local variance at log-moneyness k from total implied variance w(k, T): dw/dT divided by g(k)."""
    return np.asarray(dwdT, float) / g_function(k, w, dw, d2w)


def numeric_derivs(f, k, T, h=1e-3, hT=1e-4):
    """w, dw/dk, d2w/dk2 and dw/dT of a total-variance function f(k, T) by central differences."""
    w = f(k, T)
    dw = (f(k + h, T) - f(k - h, T)) / (2 * h)
    d2w = (f(k + h, T) - 2 * w + f(k - h, T)) / h ** 2
    dT = (f(k, T + hT) - f(k, T - hT)) / (2 * hT)
    return w, dw, d2w, dT


# ---------------------------------------------------------------------------
def var_swap_strike(K, otm_prices, F, T, df=1.0) -> float:
    """Fair variance (annualized) of a variance swap: (2 / (T df)) * integral of OTM option prices / K^2 dK, by the
    trapezoid rule, on the given strikes (puts below F, calls above)."""
    K, P = np.asarray(K, float), np.asarray(otm_prices, float)
    return float(2.0 / (T * df) * np.trapezoid(P / K ** 2, K))


def vix(K, calls, puts, F, T, r=0.0) -> float:
    """The CBOE VIX formula on one expiry: sigma^2 = (2/T) sum dK_i / K_i^2 e^{rT} Q(K_i) - (1/T)(F/K0 - 1)^2, with
    K0 the first strike at or below F, Q the put below K0, the call above, and their average at K0.  Returns the
    volatility (not x 100)."""
    K, C, P = (np.asarray(a, float) for a in (K, calls, puts))
    o = np.argsort(K)
    K, C, P = K[o], C[o], P[o]
    i0 = int(np.searchsorted(K, F, side="right") - 1)
    K0 = K[i0]
    Q = np.where(K < K0, P, C)
    Q[i0] = 0.5 * (P[i0] + C[i0])
    dK = np.empty_like(K)
    dK[1:-1] = (K[2:] - K[:-2]) / 2
    dK[0], dK[-1] = K[1] - K[0], K[-1] - K[-2]
    s2 = 2 / T * np.sum(dK / K ** 2 * np.exp(r * T) * Q) - (F / K0 - 1) ** 2 / T
    return float(np.sqrt(max(s2, 0.0)))
