"""Exotic options and structured products (Part 15): barriers in closed form and their discrete-monitoring
correction, digitals and their call-spread hedge, Asians and lookbacks, the snowball (autocallable with a knock-in)
by Monte Carlo, worst-of options, and uncertain-volatility bounds by the Black-Scholes-Barenblatt PDE.

Conventions: continuous rate r and dividend yield q; prices per unit of the underlying's starting level unless said.
"""
from __future__ import annotations

import numpy as np
from scipy.stats import norm

from explainer.quant.house import bs

N = norm.cdf

# ---------------------------------------------------------------- barriers


def down_out_call(S, K, H, T, sigma, r=0.0, q=0.0):
    """Down-and-out call with continuous monitoring, H <= K (Merton 1973; Reiner and Rubinstein 1991): the vanilla
    minus its reflection in the barrier."""
    S, K, H = (np.asarray(x, float) for x in (S, K, H))
    lam = (r - q + 0.5 * sigma ** 2) / sigma ** 2
    y = np.log(H * H / (S * K)) / (sigma * np.sqrt(T)) + lam * sigma * np.sqrt(T)
    din = (S * np.exp(-q * T) * (H / S) ** (2 * lam) * N(y)
           - K * np.exp(-r * T) * (H / S) ** (2 * lam - 2) * N(y - sigma * np.sqrt(T)))
    out = bs.price(S, K, T, sigma, r, q, 1) - din
    return np.where(S <= H, 0.0, out)


def down_in_put(S, K, H, T, sigma, r=0.0, q=0.0):
    """Down-and-in put with continuous monitoring, H < K <= S (the reflection formula)."""
    S, K, H = (np.asarray(x, float) for x in (S, K, H))
    lam = (r - q + 0.5 * sigma ** 2) / sigma ** 2
    sT = sigma * np.sqrt(T)
    x1 = np.log(S / H) / sT + lam * sT
    y = np.log(H * H / (S * K)) / sT + lam * sT
    y1 = np.log(H / S) / sT + lam * sT
    a = -S * np.exp(-q * T) * N(-x1) + K * np.exp(-r * T) * N(-x1 + sT)
    b = (S * np.exp(-q * T) * (H / S) ** (2 * lam) * (N(y) - N(y1))
         - K * np.exp(-r * T) * (H / S) ** (2 * lam - 2) * (N(y - sT) - N(y1 - sT)))
    out = a + b
    return np.where(S <= H, bs.price(S, K, T, sigma, r, q, -1), out)


BGK_BETA = 0.5825971579390106  # -zeta(1/2)/sqrt(2 pi): Broadie, Glasserman and Kou (1997)


def bgk_barrier(H, S, sigma, dt):
    """The continuity correction: a barrier watched every dt behaves like a continuous one shifted away from the
    spot by exp(beta sigma sqrt(dt))."""
    return H * np.exp(-BGK_BETA * sigma * np.sqrt(dt)) if H < S else H * np.exp(BGK_BETA * sigma * np.sqrt(dt))


# ---------------------------------------------------------------- digitals, Asians, lookbacks


def digital_call(S, K, T, sigma, r=0.0, q=0.0):
    """Cash-or-nothing call paying 1: e^{-rT} N(d2)."""
    _, d2 = bs.d1_d2(S, K, T, sigma, r, q)
    return np.exp(-r * T) * N(d2)


def call_spread_digital(S, K, T, sigma, eps, r=0.0, q=0.0):
    """The overhedge: (C(K - eps) - C(K)) / eps >= the digital, for a seller who wants to be safe."""
    return (bs.price(S, K - eps, T, sigma, r, q, 1) - bs.price(S, K, T, sigma, r, q, 1)) / eps


def geometric_asian_call(S, K, T, sigma, n, r=0.0, q=0.0):
    """A call on the geometric average of n equally spaced fixings (Kemna and Vorst 1990): log-normal, in closed form;
    the control variate for the arithmetic Asian."""
    dt = T / n
    t = dt * np.arange(1, n + 1)
    mu = np.log(S) + (r - q - 0.5 * sigma ** 2) * t.mean()
    var = sigma ** 2 * np.sum(np.minimum.outer(t, t)) / n ** 2
    sG = np.sqrt(var)
    d1 = (mu - np.log(K) + var) / sG
    return np.exp(-r * T) * (np.exp(mu + 0.5 * var) * N(d1) - K * N(d1 - sG))


def lookback_floating_call(S, T, sigma, r=0.0, q=0.0, m=None):
    """Floating-strike lookback call paying S_T - min S, continuous monitoring (Goldman, Sosin and Gatto 1979)."""
    m = S if m is None else m
    b = r - q
    if abs(b) < 1e-7:  # the formula is continuous in b; step off zero rather than special-case it
        b = 1e-7 if b >= 0 else -1e-7
    sT = sigma * np.sqrt(T)
    a1 = (np.log(S / m) + (b + 0.5 * sigma ** 2) * T) / sT
    a2 = a1 - sT
    a3 = (np.log(S / m) + (-b + 0.5 * sigma ** 2) * T) / sT
    return (S * np.exp(-q * T) * N(a1) - m * np.exp(-r * T) * N(a2)
            + S * np.exp(-r * T) * sigma ** 2 / (2 * b) * ((S / m) ** (-2 * b / sigma ** 2) * N(-a3)
                                                           - np.exp(b * T) * N(-a1)))


def gbm_paths(S0, sigma, T, n, n_paths, r=0.0, q=0.0, seed=0, antithetic=True):
    """GBM on n equal steps; returns (n + 1, n_paths)."""
    g = np.random.default_rng(seed)
    m = n_paths // 2 if antithetic else n_paths
    Z = g.standard_normal((n, m))
    if antithetic:
        Z = np.concatenate([Z, -Z], axis=1)
    dt = T / n
    x = np.cumsum((r - q - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * Z, axis=0)
    return S0 * np.exp(np.vstack([np.zeros(Z.shape[1]), x]))


# ---------------------------------------------------------------- the snowball


def snowball_payoff(paths, days_per_month=21, coupon=0.15, ko=1.03, ki=0.75, lockup=3, months=24, r=0.02):
    """The investor's discounted payoff of a snowball (雪球) note of notional 1 on paths of S/S0, daily steps:
    observed monthly after a lock-up, the note knocks out (pays 1 + coupon x months elapsed / 12) when S >= ko; if it
    never knocks out and S has ever closed below ki, the investor bears the fall, 1 + min(S_T - 1, 0); otherwise the
    full coupon is paid at maturity. Returns (pv, knocked_out_month or 0, knocked_in flag)."""
    n_paths = paths.shape[1]
    dt = 1 / (12 * days_per_month)
    alive = np.ones(n_paths, bool)
    pv = np.zeros(n_paths)
    ko_month = np.zeros(n_paths, int)
    for m in range(lockup, months + 1):
        i = m * days_per_month
        hit = alive & (paths[i] >= ko)
        pv[hit] = (1 + coupon * m / 12) * np.exp(-r * i * dt)
        ko_month[hit] = m
        alive &= ~hit
    kin = (paths[: months * days_per_month + 1].min(axis=0) < ki)
    T = months * days_per_month * dt
    ST = paths[months * days_per_month]
    lost = alive & kin
    pv[lost] = (1 + np.minimum(ST[lost] - 1, 0)) * np.exp(-r * T)
    full = alive & ~kin
    pv[full] = (1 + coupon * months / 12) * np.exp(-r * T)
    return pv, ko_month, kin


def snowball_price(sigma, coupon=0.15, ko=1.03, ki=0.75, lockup=3, months=24, r=0.02, q=0.0, n_paths=40000, seed=0,
                   S=1.0, elapsed_days=0, knocked_in=False, days_per_month=21):
    """Value of the investor's note (notional 1, struck at 1) at spot S after ``elapsed_days``, by Monte Carlo with
    daily steps; ``knocked_in`` if the barrier was already breached. Common random numbers across calls with the
    same seed make differences (Greeks) smooth."""
    total = months * days_per_month
    rem = total - elapsed_days
    dt = 1 / (12 * days_per_month)
    p = gbm_paths(S, sigma, rem * dt, rem, n_paths, r, q, seed)
    full = np.vstack([np.full((elapsed_days, p.shape[1]), np.nan), p]) if elapsed_days else p
    # observation schedule relative to the note's start; past observations are over
    alive = np.ones(p.shape[1], bool)
    pv = np.zeros(p.shape[1])
    for m in range(lockup, months + 1):
        i = m * days_per_month
        if i < elapsed_days:
            continue
        hit = alive & (full[i] >= ko)
        pv[hit] = (1 + coupon * m / 12) * np.exp(-r * (i - elapsed_days) * dt)
        alive &= ~hit
    kin = knocked_in | (p.min(axis=0) < ki)
    ST = p[-1]
    T = rem * dt
    lost = alive & kin
    pv[lost] = (1 + np.minimum(ST[lost] - 1, 0)) * np.exp(-r * T)
    keep = alive & ~kin
    pv[keep] = (1 + coupon * months / 12) * np.exp(-r * T)
    return float(pv.mean())


def fair_coupon(sigma, lo=0.0, hi=0.6, tol=1e-4, **kw):
    """The coupon that makes the note worth its notional (1): bisection on snowball_price - 1."""
    f = lambda c: snowball_price(sigma, coupon=c, **kw) - 1.0  # noqa: E731
    flo, fhi = f(lo), f(hi)
    if flo > 0 or fhi < 0:
        return float("nan")
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        fm = f(mid)
        if fm > 0:
            hi = mid
        else:
            lo = mid
        if hi - lo < tol:
            break
    return 0.5 * (lo + hi)


# ---------------------------------------------------------------- worst-of


def worst_of_put(S0, K, T, sig1, sig2, rho, n_paths=200000, r=0.0, seed=0):
    """A put on the worse of two assets (each started at 1), struck at K: MC with correlated log-normals."""
    g = np.random.default_rng(seed)
    z1 = g.standard_normal(n_paths)
    z2 = rho * z1 + np.sqrt(1 - rho ** 2) * g.standard_normal(n_paths)
    s1 = np.exp((r - 0.5 * sig1 ** 2) * T + sig1 * np.sqrt(T) * z1)
    s2 = np.exp((r - 0.5 * sig2 ** 2) * T + sig2 * np.sqrt(T) * z2)
    return float(np.exp(-r * T) * np.mean(np.maximum(K - np.minimum(s1, s2), 0)))


# ---------------------------------------------------------------- uncertain volatility


def uvm_price(payoff, S_grid, T, sig_lo, sig_hi, r=0.0, n_t=400, upper=True):
    """Avellaneda, Levy and Paras (1995): the price of a payoff when volatility is only known to lie in
    [sig_lo, sig_hi], by the Black-Scholes-Barenblatt equation dV/dt + r S V_S + 1/2 sigma(Gamma)^2 S^2 V_SS - r V = 0,
    with sigma = sig_hi where Gamma > 0 and sig_lo where Gamma < 0 for the seller's (upper) price, the reverse for the
    lower. Explicit-in-sigma, implicit-in-time finite differences on S_grid."""
    S = np.asarray(S_grid, float)
    V = payoff(S).astype(float)
    dt = T / n_t
    h = np.diff(S)
    n = len(S)
    for _ in range(n_t):
        g = np.zeros(n)
        g[1:-1] = 2 * (h[:-1] * V[2:] - (h[:-1] + h[1:]) * V[1:-1] + h[1:] * V[:-2]) / (h[:-1] * h[1:] * (h[:-1] + h[1:]))
        sig = np.where(g > 0, sig_hi, sig_lo) if upper else np.where(g > 0, sig_lo, sig_hi)
        a = 0.5 * sig ** 2 * S ** 2
        # implicit step: (1 + r dt) V_new - dt [a V_SS + r S V_S] = V_old, tridiagonal
        lower = np.zeros(n)
        diag = np.ones(n) * (1 + r * dt)
        upper_ = np.zeros(n)
        for i in range(1, n - 1):
            hm, hp = h[i - 1], h[i]
            cm = 2 * a[i] / (hm * (hm + hp)) - r * S[i] / (hm + hp)
            cp = 2 * a[i] / (hp * (hm + hp)) + r * S[i] / (hm + hp)
            lower[i] = -dt * cm
            upper_[i] = -dt * cp
            diag[i] = 1 + r * dt + dt * (cm + cp)
        # boundaries: linear extrapolation (V_SS = 0)
        diag[0] = diag[-1] = 1.0
        rhs = V.copy()
        rhs[0] = 2 * V[1] - V[2] if n > 2 else V[0]
        rhs[-1] = 2 * V[-2] - V[-3] if n > 2 else V[-1]
        V = _thomas(lower, diag, upper_, rhs)
    return V


def _thomas(a, b, c, d):
    n = len(d)
    cp = np.zeros(n)
    dp = np.zeros(n)
    cp[0] = c[0] / b[0]
    dp[0] = d[0] / b[0]
    for i in range(1, n):
        m = b[i] - a[i] * cp[i - 1]
        cp[i] = c[i] / m if i < n - 1 else 0.0
        dp[i] = (d[i] - a[i] * dp[i - 1]) / m
    x = np.zeros(n)
    x[-1] = dp[-1]
    for i in range(n - 2, -1, -1):
        x[i] = dp[i] - cp[i] * x[i + 1]
    return x
