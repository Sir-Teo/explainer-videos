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
    conv = np.zeros(s.shape, dtype=bool)  # converged entries are frozen while the others iterate
    for _ in range(max_iter):
        f = norm_price(s) - target
        lo = np.where(f < 0, s, lo)
        hi = np.where(f > 0, s, hi)
        v = norm_vega(s)
        with np.errstate(divide="ignore", invalid="ignore"):
            step = s - f / v
        ok = np.isfinite(step) & (step > lo) & (step < hi)
        s_new = np.where(ok, step, 0.5 * (lo + hi))
        # a Newton correction below tolerance means converged, even where the step lands on the bracket's edge
        settled = conv | (f == 0) | (np.isfinite(step) & (np.abs(step - s) < tol * np.maximum(1.0, s)))
        s_new = np.where(settled, np.where(conv, s, np.where(np.isfinite(step), step, s)), s_new)
        conv = settled | (np.abs(s_new - s) < tol * np.maximum(1.0, s))
        s = s_new
        iters.append(s.copy())
        if np.all(conv | bad):
            break
    sigma = np.where(bad, np.nan, s / np.sqrt(np.where(T > 0, T, 1.0)))
    if return_iterations:
        return sigma, [it / np.sqrt(np.where(T > 0, T, 1.0)) for it in iters]
    return sigma


# ---------------------------------------------------------------------------
# The PDE solved by the heat kernel; Leland's volatility; Barone-Adesi–Whaley (Part 10)
# ---------------------------------------------------------------------------
def heat_price(payoff, S, T, sigma, r=0.0, q=0.0, kinks=(), n=64, width=12.0):
    """Any European payoff priced the way the Black–Scholes PDE is solved: change to y = ln S + (r - q - sigma^2/2) T,
    where the equation is the heat equation with diffusivity sigma^2/2, and convolve the payoff with the heat kernel,

        V = e^{-rT} int phi(z; y, sigma^2 T) payoff(e^z) dz.

    The integral is taken by Gauss–Legendre (``n`` nodes) on the pieces between the payoff's ``kinks`` (strikes,
    where it bends or jumps), over y +/- ``width`` standard deviations: exact to rounding for piecewise-smooth
    payoffs.  ``payoff`` takes an array of terminal prices; S and T are numbers."""
    S, T, sigma, r, q = (float(v) for v in (S, T, sigma, r, q))
    if T <= 0 or sigma <= 0:
        return float(np.exp(-r * max(T, 0.0)) * payoff(np.array([S * np.exp((r - q) * max(T, 0.0))]))[0])
    sd = sigma * np.sqrt(T)
    y = np.log(S) + (r - q - 0.5 * sigma ** 2) * T
    lo, hi = y - width * sd, y + width * sd
    cuts = sorted({lo, hi, *[np.log(k) for k in kinks if lo < np.log(k) < hi]})
    u, w = np.polynomial.legendre.leggauss(n)
    total = 0.0
    for a, b in zip(cuts, cuts[1:]):
        z = 0.5 * (b - a) * u + 0.5 * (a + b)
        kern = np.exp(-0.5 * ((z - y) / sd) ** 2) / (sd * SQRT_2PI)
        total += 0.5 * (b - a) * float(np.sum(w * kern * payoff(np.exp(z))))
    return float(np.exp(-r * T) * total)


def leland_vol(sigma, k, dt):
    """Leland (1985): with a proportional round-trip cost ``k`` (a fraction of the value traded) and rebalancing every
    ``dt`` years, price and hedge at sigma_L^2 = sigma^2 (1 + sqrt(2/pi) k / (sigma sqrt(dt)))."""
    sigma, k, dt = _arr(sigma, k, dt)
    return sigma * np.sqrt(1.0 + np.sqrt(2.0 / np.pi) * k / (sigma * np.sqrt(dt)))


def baw(S, K, T, sigma, r, q=0.0, cp=-1) -> dict:
    """Barone-Adesi and Whaley (1987): the American option as the European plus an early-exercise term that solves
    the Black–Scholes PDE with the time derivative of that term dropped, A (S / S*)^{q_i}, fitted at the critical
    price S* by value matching and smooth pasting (one equation in S*).  Returns ``price``, ``critical`` (S*; inf or
    0 when early exercise is never optimal) and ``european``.  S may be an array; the other inputs are numbers."""
    from scipy.optimize import brentq

    S = np.asarray(S, float)
    eu = price(S, K, T, sigma, r, q, cp)
    never = (cp > 0 and q <= 0) or (cp < 0 and r <= 0)
    if never or T <= 0:
        return {"price": eu, "critical": np.inf if cp > 0 else 0.0, "european": eu}
    M, N_ = 2 * r / sigma ** 2, 2 * (r - q) / sigma ** 2
    Kk = 1 - np.exp(-r * T)
    root = np.sqrt((N_ - 1) ** 2 + 4 * M / Kk)
    qi = (-(N_ - 1) + cp * root) / 2  # q2 > 1 for calls, q1 < 0 for puts

    def edge(s):  # 1 - e^{-qT} N(cp d1): the slope the early-exercise term must supply
        return 1 - np.exp(-q * T) * ndtr(cp * d1_d2(s, K, T, sigma, r, q)[0])

    def f(s):
        return cp * (s - K) - (price(s, K, T, sigma, r, q, cp) + cp * edge(s) * s / qi)

    if cp > 0:
        crit = brentq(f, K * (1 + 1e-9), K * 200)
    else:
        crit = brentq(f, K * 1e-6, K * (1 - 1e-9))
    A = cp * (crit / qi) * edge(crit)
    alive = (S < crit) if cp > 0 else (S > crit)
    am = np.where(alive, eu + A * (S / crit) ** qi, cp * (S - K))
    return {"price": am, "critical": float(crit), "european": eu}
