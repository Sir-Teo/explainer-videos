"""Black–Scholes–Merton, vectorized: prices, Greeks, the forward (Black-76) form, and implied volatility.

Conventions, for the whole House:

* times in years, rates and volatilities annualized and continuously compounded;
* ``cp`` is +1 for a call and -1 for a put (arrays allowed);
* ``q`` is the continuous carry yield (dividends, borrow, or the foreign rate for FX); the forward is
  F = S e^{(r - q) T};
* theta is the derivative with respect to calendar time t (so it is negative for a long vanilla), per year;
* vega is per unit of volatility (per 1.00, not per vol point).

Every function broadcasts over its arguments.  At T = 0 prices are the payoff and the Greeks their limits (delta a
step, gamma and vega zero), so a hedging loop can run to expiry without special cases.
"""

from __future__ import annotations

import numpy as np
from scipy.special import ndtr

SQRT_2PI = np.sqrt(2.0 * np.pi)


def npdf(x):
    return np.exp(-0.5 * np.square(x)) / SQRT_2PI


def _arr(*xs):
    return [np.asarray(x, dtype=float) for x in xs]


def d1_d2(S, K, T, sigma, r=0.0, q=0.0):
    S, K, T, sigma, r, q = _arr(S, K, T, sigma, r, q)
    s = sigma * np.sqrt(np.maximum(T, 0.0))
    with np.errstate(divide="ignore", invalid="ignore"):
        d1 = (np.log(S / K) + (r - q) * T) / s + 0.5 * s
    return d1, d1 - s


def price(S, K, T, sigma, r=0.0, q=0.0, cp=1):
    """The Black–Scholes–Merton price of a European call (cp = +1) or put (cp = -1)."""
    S, K, T, sigma, r, q, cp = _arr(S, K, T, sigma, r, q, cp)
    live = (T > 0) & (sigma > 0)
    d1, d2 = d1_d2(S, K, np.where(live, T, 1.0), np.where(live, sigma, 1.0), r, q)
    disc_q, disc_r = np.exp(-q * T), np.exp(-r * T)
    v = cp * (S * disc_q * ndtr(cp * d1) - K * disc_r * ndtr(cp * d2))
    payoff = np.maximum(cp * (S * disc_q - K * disc_r), 0.0)  # T = 0 or sigma = 0: the discounted intrinsic
    return np.where(live, v, payoff)


def greeks(S, K, T, sigma, r=0.0, q=0.0, cp=1) -> dict:
    """Price and Greeks: delta, gamma, theta (per year, calendar time), vega (per 1.00 of vol), rho, and the
    second-order vanna (d delta / d sigma) and volga (d vega / d sigma)."""
    S, K, T, sigma, r, q, cp = _arr(S, K, T, sigma, r, q, cp)
    live = (T > 0) & (sigma > 0)
    Tl, sl = np.where(live, T, 1.0), np.where(live, sigma, 1.0)
    d1, d2 = d1_d2(S, K, Tl, sl, r, q)
    disc_q, disc_r = np.exp(-q * Tl), np.exp(-r * Tl)
    sqT = np.sqrt(Tl)
    pdf = npdf(d1)
    out = {
        "price": price(S, K, T, sigma, r, q, cp),
        "delta": np.where(live, cp * disc_q * ndtr(cp * d1), np.where(cp * (S - K) > 0, cp, 0.0)),
        "gamma": np.where(live, disc_q * pdf / (S * sl * sqT), 0.0),
        "vega": np.where(live, S * disc_q * pdf * sqT, 0.0),
        "theta": np.where(live, -S * disc_q * pdf * sl / (2 * sqT) - cp * r * K * disc_r * ndtr(cp * d2)
                          + cp * q * S * disc_q * ndtr(cp * d1), 0.0),
        "rho": np.where(live, cp * K * Tl * disc_r * ndtr(cp * d2), 0.0),
        "vanna": np.where(live, -disc_q * pdf * d2 / sl, 0.0),
        "volga": np.where(live, S * disc_q * pdf * sqT * d1 * d2 / sl, 0.0),
    }
    return out


def black(F, K, T, sigma, df=1.0, cp=1):
    """Black-76: the price of an option on a forward F, discounted by ``df``."""
    F, K, T, sigma, df, cp = _arr(F, K, T, sigma, df, cp)
    return df * price(F, K, T, sigma, 0.0, 0.0, cp)


# ---------------------------------------------------------------------------
# Implied volatility
# ---------------------------------------------------------------------------
def implied_vol(p, S, K, T, r=0.0, q=0.0, cp=1, tol=1e-12, max_iter=200, return_iterations=False):
    """The volatility at which the Black–Scholes–Merton price equals ``p``.

    Works on the normalized forward price: with F = S e^{(r-q)T} and x = ln(F/K), the undiscounted price divided
    by sqrt(F K) depends only on x and the total volatility s = sigma sqrt(T), and is increasing in s.  Newton
    steps in s, from the Brenner–Subrahmanyam / Corrado–Miller guess, kept inside a bisection bracket that shrinks
    every iteration, so it converges from anywhere (quadratically once close).  Prices outside the no-arbitrage
    bounds give NaN.  ``return_iterations`` also returns the iterates (for drawing the solver at work)."""
    p, S, K, T, r, q, cp = np.broadcast_arrays(*_arr(p, S, K, T, r, q, cp))
    F = S * np.exp((r - q) * T)
    df = np.exp(-r * T)
    x = np.log(F / K)
    target = p / (df * np.sqrt(F * K))  # normalized price
    lo_bound = np.maximum(cp * (np.exp(x / 2) - np.exp(-x / 2)), 0.0)
    hi_bound = np.where(cp > 0, np.exp(x / 2), np.exp(-x / 2))
    bad = ~((target >= lo_bound - 1e-15) & (target < hi_bound) & (T > 0))

    def norm_price(s):
        with np.errstate(divide="ignore", invalid="ignore"):
            d1 = x / s + s / 2
        return cp * (np.exp(x / 2) * ndtr(cp * d1) - np.exp(-x / 2) * ndtr(cp * (d1 - s)))

    def norm_vega(s):
        with np.errstate(divide="ignore", invalid="ignore"):
            d1 = x / s + s / 2
        return np.exp(x / 2) * npdf(d1)

    # initial guess: Corrado–Miller in normalized units (it reduces to Brenner–Subrahmanyam's sqrt(2 pi) c at the
    # money); a put is first turned into the call with the same strike by parity
    a, b = np.exp(x / 2), np.exp(-x / 2)
    call = np.where(cp > 0, target, target + (a - b))
    m = call - (a - b) / 2
    cm = np.sqrt(2 * np.pi) / (a + b) * (m + np.sqrt(np.maximum(m * m - (a - b) ** 2 / np.pi, 0.0)))
    s = np.clip(np.where(np.isfinite(cm) & (cm > 0), cm, 0.5), 1e-4, 4.0)
    lo = np.full_like(s, 1e-12)
    hi = np.full_like(s, 12.0)
    iters = [s.copy()]
    for _ in range(max_iter):
        f = norm_price(s) - target
        lo = np.where(f < 0, s, lo)
        hi = np.where(f > 0, s, hi)
        v = norm_vega(s)
        with np.errstate(divide="ignore", invalid="ignore"):
            step = s - f / v
        ok = np.isfinite(step) & (step > lo) & (step < hi)
        s_new = np.where(ok, step, 0.5 * (lo + hi))
        done = np.abs(s_new - s) < tol * np.maximum(1.0, s)
        s = s_new
        iters.append(s.copy())
        if np.all(done | bad):
            break
    sigma = np.where(bad, np.nan, s / np.sqrt(np.where(T > 0, T, 1.0)))
    if return_iterations:
        return sigma, [it / np.sqrt(np.where(T > 0, T, 1.0)) for it in iters]
    return sigma
