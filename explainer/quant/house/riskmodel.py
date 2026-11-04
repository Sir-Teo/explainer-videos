"""The House's risk model, trading and attribution (Part 31).

* A Barra-style cross-sectional factor model: standardised style exposures, daily weighted cross-sectional regressions
  for factor returns, an exponentially weighted factor covariance, specific variances shrunk toward their cross-
  sectional mean (Bayesian, as the commercial models do), Vasicek's shrinkage of betas, and Barra's bias statistic.
* The fundamental law of active management (Grinold 1989), with the transfer coefficient (Clarke, de Silva and Thorley
  2002) and with a time-varying information coefficient (Qian and Hua 2004; Ding 2010).
* Trading with costs: the square-root impact law, Garleanu and Pedersen's (2013) aim portfolio and trade rate, checked
  against a brute-force Riccati solution, and capacity.
* Attribution of a portfolio's return to factors and to the specific residual.

Arrays are (T x N) days by assets unless stated; NaN marks an asset that is not in the universe that day.
"""

from __future__ import annotations

import math

import numpy as np

# ---------------------------------------------------------------------------
# Exposures and the cross-sectional model
# ---------------------------------------------------------------------------


def standardise(x, mask, weights=None):
    """Cross-sectional z-score of each row over the assets in ``mask``, winsorised at 3 (cap-weighted mean if weights
    are given, as Barra does, equal-weighted standard deviation)."""
    x = np.where(mask, x, np.nan)
    out = np.full_like(x, np.nan, dtype=float)
    for t in range(x.shape[0]):
        m = np.isfinite(x[t])
        if m.sum() < 5:
            continue
        v = x[t, m]
        mu = np.average(v, weights=weights[t, m]) if weights is not None else v.mean()
        sd = v.std()
        if sd > 0:
            out[t, m] = np.clip((v - mu) / sd, -3, 3)
    return out


def factor_returns(R, X, w=None, ridge: float = 1e-6):
    """Daily cross-sectional regressions R[t] = X[t] f[t] + u[t] (weighted least squares with weights ``w``, e.g. the
    square root of size). ``X``: (T x N x K) exposures; returns (f (T x K), residuals (T x N))."""
    T, N, K = X.shape
    f = np.full((T, K), np.nan)
    u = np.full((T, N), np.nan)
    for t in range(T):
        m = np.isfinite(R[t]) & np.isfinite(X[t]).all(1)
        if m.sum() < K + 5:
            continue
        A, y = X[t, m], R[t, m]
        wt = np.ones(m.sum()) if w is None else np.nan_to_num(w[t, m], nan=0.0) + 1e-12
        G = A.T @ (A * wt[:, None]) + ridge * np.eye(K)
        f[t] = np.linalg.solve(G, A.T @ (wt * y))
        u[t, m] = y - A @ f[t]
    return f, u


def ewma_cov(F, half_life: float):
    """Exponentially weighted covariance of the rows of F (NaN rows skipped), the latest estimate after each row."""
    lam = 0.5 ** (1 / half_life)
    K = F.shape[1]
    S = np.eye(K) * 1e-4
    out = np.full((F.shape[0], K, K), np.nan)
    started = False
    for t in range(F.shape[0]):
        if np.isfinite(F[t]).all():
            x = F[t]
            S = np.outer(x, x) if not started else lam * S + (1 - lam) * np.outer(x, x)
            started = True
        if started:
            out[t] = S
    return out


def specific_var(U, half_life: float, shrink: float = 0.3):
    """Exponentially weighted specific variance of each asset's residuals, shrunk toward the day's cross-sectional mean
    by ``shrink`` (a Bayesian adjustment: assets with short histories borrow from the others)."""
    lam = 0.5 ** (1 / half_life)
    T, N = U.shape
    v = np.full(N, np.nan)
    out = np.full((T, N), np.nan)
    for t in range(T):
        m = np.isfinite(U[t])
        u2 = U[t] ** 2
        v = np.where(m & np.isfinite(v), lam * v + (1 - lam) * u2, np.where(m, u2, v))
        live = np.isfinite(v)
        if live.sum() > 5:
            mu = np.nanmean(v[live])
            out[t, live] = (1 - shrink) * v[live] + shrink * mu
    return out


def vasicek(beta, se, prior_mean=None, prior_var=None):
    """Vasicek (1973): shrink each estimated beta toward the cross-sectional mean, weighting by precision:
    b* = (b/se^2 + m/s^2) / (1/se^2 + 1/s^2)."""
    beta, se = np.asarray(beta, float), np.asarray(se, float)
    m = np.nanmean(beta) if prior_mean is None else prior_mean
    s2 = max(np.nanvar(beta) - np.nanmean(se ** 2), 1e-8) if prior_var is None else prior_var
    w = (1 / se ** 2) / (1 / se ** 2 + 1 / s2)
    return w * beta + (1 - w) * m, w


def portfolio_risk(h, X, Fcov, svar):
    """Forecast variance of holdings h (N): h'X F X'h + sum h_i^2 s_i, split into factor and specific parts."""
    m = np.isfinite(svar) & np.isfinite(X).all(1)
    hx = h[m] @ X[m]
    fac = float(hx @ Fcov @ hx)
    spec = float(np.sum(h[m] ** 2 * svar[m]))
    return fac + spec, fac, spec


def bias_statistic(z):
    """Barra's bias statistic: the standard deviation of realised returns divided by their forecast volatility. Near one
    when the risk forecasts are right; a 95% band is about 1 +- sqrt(2/T)."""
    z = np.asarray(z, float)
    z = z[np.isfinite(z)]
    return float(z.std(ddof=1)), float(math.sqrt(2 / len(z)))


# ---------------------------------------------------------------------------
# The fundamental law
# ---------------------------------------------------------------------------


def fundamental_ir(ic: float, breadth: float, tc: float = 1.0) -> float:
    """Grinold (1989), with Clarke, de Silva and Thorley's (2002) transfer coefficient: IR = TC x IC x sqrt(BR)."""
    return tc * ic * math.sqrt(breadth)


def ir_time_varying(ic_mean: float, ic_sd: float, N: int) -> float:
    """The per-period information ratio of a strategy whose cross-sectional IC varies over time (Qian and Hua 2004;
    Ding 2010): IR = E[IC] / sqrt(sd(IC)^2 + (1 - E[IC]^2)/N); it equals IC sqrt(N) only when sd(IC) = 0 apart from
    sampling noise, and tends to E[IC]/sd(IC) as N grows."""
    return ic_mean / math.sqrt(ic_sd ** 2 + (1 - ic_mean ** 2) / N)


def simulate_ic_strategy(N: int, T: int, ic_mean: float, ic_sd: float, rng):
    """Simulate a long-short strategy with holdings proportional to standardised scores z and returns whose
    cross-sectional correlation with z on day t is IC_t ~ N(ic_mean, ic_sd^2): realised per-period IR and IC series."""
    pnl, ics = np.empty(T), np.empty(T)
    for t in range(T):
        ic_t = np.clip(ic_mean + ic_sd * rng.standard_normal(), -0.99, 0.99)
        z = rng.standard_normal(N)
        z = (z - z.mean()) / z.std()
        e = rng.standard_normal(N)
        r = ic_t * z + math.sqrt(1 - ic_t ** 2) * e
        pnl[t] = z @ r / N
        ics[t] = np.corrcoef(z, r)[0, 1]
    return pnl.mean() / pnl.std(ddof=1), ics


# ---------------------------------------------------------------------------
# Costs and dynamic trading
# ---------------------------------------------------------------------------


def sqrt_impact(q, adv, sigma, y: float = 1.0):
    """The square-root law of market impact: cost per unit traded ~ Y sigma sqrt(Q / ADV) (Torre 1997; Almgren et al.
    2005; Toth et al. 2011), as a fraction of price."""
    return y * sigma * np.sqrt(np.abs(q) / adv)


def gp_trade_rate(gamma: float, lam: float, rho: float) -> float:
    """Garleanu and Pedersen (2013), Proposition 3, for trading costs (lam/2) dx' Sigma dx and risk aversion gamma with
    discount rate rho: the fraction a/lam of the gap to the aim portfolio traded each period, where
    a = (-(gamma(1-rho) + lam rho) + sqrt((gamma(1-rho) + lam rho)^2 + 4 gamma lam (1-rho)^2)) / (2 (1-rho))."""
    b = gamma * (1 - rho) + lam * rho
    a = (-b + math.sqrt(b * b + 4 * gamma * lam * (1 - rho) ** 2)) / (2 * (1 - rho))
    return a / lam


def gp_aim_weight(gamma: float, lam: float, rho: float, phi: float) -> float:
    """The aim portfolio's loading on a signal that mean-reverts at rate phi (f_{t+1} = (1 - phi) f_t + noise), relative
    to the Markowitz loading 1/gamma: 1 / (1 + phi a / gamma). Slow signals get full weight, fast ones are discounted."""
    b = gamma * (1 - rho) + lam * rho
    a = (-b + math.sqrt(b * b + 4 * gamma * lam * (1 - rho) ** 2)) / (2 * (1 - rho))
    return 1.0 / (1.0 + phi * a / gamma)


def riccati_scalar(gamma: float, lam: float, rho: float, phi: float, sigma2: float = 1.0, beta: float = 1.0,
                   iters: int = 20000):
    """Brute-force check of the scalar Garleanu-Pedersen problem by value iteration on the quadratic value function
    V(x, f) = -1/2 Axx x^2 + Axf x f - 1/2 Aff f^2: max over x_t of (1-rho)[x beta f' - gamma/2 sigma2 x^2] -
    lam/2 sigma2 (x - x_prev)^2 + (1-rho) E V(x, f'). Returns the implied trade rate and the aim loading (per unit of
    the Markowitz position)."""
    d = 1 - rho
    Axx, Axf = 0.0, 0.0
    for _ in range(iters):
        # objective in x given (x_prev, f): quadratic; first-order condition linear in x
        # coefficient on x^2: -(d*gamma*sigma2 + lam*sigma2 + d*Axx); on x: lam*sigma2*x_prev + d*beta*(1-phi) f
        #   + d*Axf*(1-phi) f
        cxx = d * gamma * sigma2 + lam * sigma2 + d * Axx
        kx = lam * sigma2 / cxx                       # x = kx x_prev + kf f
        kf = (d * beta * (1 - phi) + d * Axf * (1 - phi)) / cxx
        # new value function coefficients (in x_prev and f)
        Axx_new = lam * sigma2 - (lam * sigma2) ** 2 / cxx
        Axf_new = lam * sigma2 * kf
        if abs(Axx_new - Axx) < 1e-14 and abs(Axf_new - Axf) < 1e-14:
            Axx, Axf = Axx_new, Axf_new
            break
        Axx, Axf = Axx_new, Axf_new
    rate = 1 - kx
    markowitz = beta * (1 - phi) / (gamma * sigma2)      # myopic position on the expected next-period return
    aim = kf / rate / markowitz if rate > 0 else float("nan")
    return rate, aim


# ---------------------------------------------------------------------------
# Attribution
# ---------------------------------------------------------------------------


def attribute(h, X, f, u):
    """Split the return of holdings h on one day into factor contributions (h'X)_k f_k and the specific part h'u."""
    m = np.isfinite(u) & np.isfinite(X).all(1)
    hx = h[m] @ X[m]
    return hx * f, float(h[m] @ u[m])


# ---------------------------------------------------------------------------
# Guards (Rule 31): what the registered rule of Part 31 lacked
# ---------------------------------------------------------------------------


def floor_variance(sig2, floor: float):
    """Forecast variances with a floor: no asset is ever forecast to be safer than ``floor`` (a daily variance set from
    the asset class, not from the asset's own recent history), so 1/sigma^2 rules cannot take unbounded positions."""
    return np.maximum(np.asarray(sig2, float), floor)


def cap_positions(x, book: float = 1.0, cap: float = 0.05, adv=None, adv_cap: float = 0.1):
    """Position limits that do not depend on the model: |x_i| <= cap x book and, if daily volumes ``adv`` (in the same
    units as x) are given, |x_i| <= adv_cap x adv_i."""
    x = np.asarray(x, float)
    lim = np.full_like(x, cap * book)
    if adv is not None:
        lim = np.minimum(lim, adv_cap * np.nan_to_num(np.asarray(adv, float), nan=0.0))
    return np.clip(x, -lim, lim)


__all__ = ["standardise", "factor_returns", "ewma_cov", "specific_var", "vasicek", "portfolio_risk", "bias_statistic",
           "fundamental_ir", "ir_time_varying", "simulate_ic_strategy", "sqrt_impact", "gp_trade_rate", "gp_aim_weight",
           "riccati_scalar", "attribute", "floor_variance", "cap_positions"]
