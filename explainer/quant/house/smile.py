"""The House's smile tools: a smooth, arbitrage-aware curve through one expiry's implied volatilities, and what option
prices say about the future under Q (Part 1 uses them; Part 12 derives SVI and adds SSVI and the surface).

* :func:`svi_total_variance` / :func:`fit_svi`: Gatheral's raw SVI, w(k) = a + b (rho (k - m) + sqrt((k - m)^2 +
  s^2)), total implied variance against log-moneyness k = ln K/F, fitted by weighted least squares;
* :func:`risk_neutral_density`: Breeden and Litzenberger (1978): the density of S_T under the forward measure is the
  second strike derivative of the undiscounted call price, q(K) = d^2 C / dK^2;
* :func:`svix2`: Martin's (2017) risk-neutral variance of the return, var^Q(S_T / F) = (2 / F^2) times the integral of
  out-of-the-money undiscounted option prices over strikes; with his negative-correlation condition it bounds the
  expected excess return from below: E[R_T] - R_f >= R_f var^Q(S_T / F).
"""

from __future__ import annotations

import numpy as np
from scipy import optimize

from explainer.quant.house import bs


def svi_total_variance(k, a, b, rho, m, s):
    k = np.asarray(k, float)
    return a + b * (rho * (k - m) + np.sqrt((k - m) ** 2 + s ** 2))


def fit_svi(k, w, weights=None) -> dict:
    """Raw SVI through total variances ``w`` = iv^2 T at log-moneyness ``k``; parameters kept in the region where
    w >= 0 and the wings are not steeper than Lee's moment bound (b (1 + |rho|) <= 2)."""
    k, w = np.asarray(k, float), np.asarray(w, float)
    wt = np.ones_like(w) if weights is None else np.asarray(weights, float)

    def resid(p):
        a, b, rho, m, s = p
        return np.sqrt(wt) * (svi_total_variance(k, a, b, rho, m, s) - w)

    best = None
    for m0 in (-0.1, 0.0, 0.1):
        for s0 in (0.05, 0.2):
            p0 = [max(w.min() * 0.5, 1e-4), 0.1, -0.2, m0, s0]
            lo = [-w.max(), 1e-6, -0.999, -1.0, 1e-3]
            hi = [w.max() * 2, 2.0 / (1 + 0.999), 0.999, 1.0, 2.0]
            r = optimize.least_squares(resid, p0, bounds=(lo, hi), max_nfev=4000)
            if best is None or r.cost < best.cost:
                best = r
    a, b, rho, m, s = best.x
    return {"a": a, "b": b, "rho": rho, "m": m, "s": s,
            "rmse": float(np.sqrt(np.mean((svi_total_variance(k, a, b, rho, m, s) - w) ** 2)))}


def svi_iv(p: dict, k, T: float):
    return np.sqrt(np.maximum(svi_total_variance(k, p["a"], p["b"], p["rho"], p["m"], p["s"]), 1e-12) / T)


def call_prices(p: dict, F: float, T: float, K):
    """Undiscounted Black-76 call prices on the SVI smile (the forward measure's expectation of (S_T - K)+)."""
    K = np.asarray(K, float)
    iv = svi_iv(p, np.log(K / F), T)
    return bs.price(F, K, T, iv, 0.0, 0.0, 1)


def risk_neutral_density(p: dict, F: float, T: float, K) -> np.ndarray:
    """q(K) = d^2 C / dK^2 on a uniform strike grid ``K`` (central differences), clipped at zero."""
    K = np.asarray(K, float)
    C = call_prices(p, F, T, K)
    h = K[1] - K[0]
    q = np.empty_like(C)
    q[1:-1] = (C[2:] - 2 * C[1:-1] + C[:-2]) / h ** 2
    q[0], q[-1] = q[1], q[-2]
    return np.maximum(q, 0.0)


def svix2(p: dict, F: float, T: float, n: int = 20001, span: float = 8.0) -> float:
    """Martin's risk-neutral variance of the gross return over the horizon, var^Q(S_T / F), from the smile's
    out-of-the-money prices integrated over strikes F e^-span ... F e^span."""
    K = F * np.exp(np.linspace(-span, span, n))
    iv = svi_iv(p, np.log(K / F), T)
    otm = np.where(K < F, bs.price(F, K, T, iv, 0.0, 0.0, -1), bs.price(F, K, T, iv, 0.0, 0.0, 1))
    return float(2.0 / F ** 2 * np.trapezoid(otm, K))
