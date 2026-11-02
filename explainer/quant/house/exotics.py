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


# ---------------------------------------------------------------- Part 15, expanded: touches, static hedges, the
# snowball as a linear function of its coupon, any-model autocalls, two-asset payoffs, cliquets, the hedged UVM,
# the entropic worst case, and the Greeks of a discontinuous payoff


def one_touch(S, H, T, sigma, r=0.0, q=0.0):
    """One-touch paying 1 at expiry if the barrier H is ever touched (down if H < S, up if H > S), continuous
    monitoring: the first-passage law of Brownian motion with drift mu = r - q - sigma^2/2 (reflection plus
    Girsanov). With r = q = 0 it is N(-d2) + (S/H) N(-d1) for a down touch: about twice the digital."""
    S, H = float(S), float(H)
    mu = r - q - 0.5 * sigma ** 2
    b = np.log(H / S)
    sT = sigma * np.sqrt(T)
    if b < 0:
        p = N((b - mu * T) / sT) + np.exp(2 * mu * b / sigma ** 2) * N((b + mu * T) / sT)
    else:
        p = N((-b + mu * T) / sT) + np.exp(2 * mu * b / sigma ** 2) * N((-b - mu * T) / sT)
    return float(np.exp(-r * T) * min(p, 1.0))


def static_dic_hedge(K, H, F):
    """Carr, Ellis and Gupta (1998): with put-call symmetry (r = q = 0, a smile symmetric in log(K/F)), a down-and-in
    call (H <= K) is replicated by K/H puts struck at H^2/K, held until the barrier is touched and then exchanged for
    the call at no cost. Returns (number of puts, their strike). F is unused when r = q = 0 (the forward is the spot
    at the touch, H)."""
    return K / H, H * H / K


def snowball_AB(sigma, ko=1.03, ki=0.75, lockup=3, months=24, r=0.02, q=0.0, n_paths=40000, seed=0, S=1.0,
                elapsed_days=0, knocked_in=False, days_per_month=21, disc_spread=0.0):
    """The snowball's value is affine in its coupon: V(c) = A + c B on every path, so one simulation gives both and
    the fair coupon is (1 - A) / B, with no root search. Same paths and conventions as snowball_price (which equals
    A + c B for the same seed); ``disc_spread`` discounts at r + s (the issuer's funding) while the index drifts at
    r - q."""
    total = months * days_per_month
    rem = total - elapsed_days
    dt = 1 / (12 * days_per_month)
    p = gbm_paths(S, sigma, rem * dt, rem, n_paths, r, q, seed)
    full = np.vstack([np.full((elapsed_days, p.shape[1]), np.nan), p]) if elapsed_days else p
    rd = r + disc_spread
    alive = np.ones(p.shape[1], bool)
    a = np.zeros(p.shape[1])
    b = np.zeros(p.shape[1])
    for m in range(lockup, months + 1):
        i = m * days_per_month
        if i < elapsed_days:
            continue
        hit = alive & (full[i] >= ko)
        d = np.exp(-rd * (i - elapsed_days) * dt)
        a[hit] = d
        b[hit] = m / 12 * d
        alive &= ~hit
    kin = knocked_in | (p.min(axis=0) < ki)
    d = np.exp(-rd * rem * dt)
    lost = alive & kin
    a[lost] = (1 + np.minimum(p[-1][lost] - 1, 0)) * d
    keep = alive & ~kin
    a[keep] = d
    b[keep] = months / 12 * d
    return float(a.mean()), float(b.mean())


def autocall_on_paths(S, obs, ko, ki, coupons, disc=None):
    """An autocall on paths S (steps x paths, relative to the start, daily rows) from any model: at observation row
    obs[k] the note is redeemed for 1 + coupons[k] if S >= ko; if it survives to the last observation it pays
    1 + coupons[-1] unless S ever closed below ki, in which case it pays min(S_T, 1). ``disc`` are the discount
    factors at the observation rows (default 1). Returns the present value per path."""
    S = np.asarray(S, float)
    disc = np.ones(len(obs)) if disc is None else np.asarray(disc, float)
    alive = np.ones(S.shape[1], bool)
    pv = np.zeros(S.shape[1])
    for k, i in enumerate(obs):
        hit = alive & (S[i] >= ko)
        pv[hit] = (1 + coupons[k]) * disc[k]
        alive &= ~hit
    last = obs[-1]
    kin = S[: last + 1].min(axis=0) < ki
    lost = alive & kin
    pv[lost] = np.minimum(S[last][lost], 1.0) * disc[-1]
    keep = alive & ~kin
    pv[keep] = (1 + coupons[-1]) * disc[-1]
    return pv


def two_asset_paths(sig1, sig2, rho, T, n, n_paths, r=0.0, q1=0.0, q2=0.0, seed=0):
    """Two correlated GBMs started at 1 on n steps, (n + 1, n_paths) each. The first asset uses exactly the random
    numbers of gbm_paths(seed), so with rho = 1 and equal vols both reduce to it."""
    g = np.random.default_rng(seed)
    m = n_paths // 2
    Z1 = g.standard_normal((n, m))
    Z1 = np.concatenate([Z1, -Z1], axis=1)
    W = g.standard_normal((n, m))
    W = np.concatenate([W, -W], axis=1)
    Z2 = rho * Z1 + np.sqrt(max(1 - rho ** 2, 0.0)) * W
    dt = T / n
    out = []
    for s, qq, Z in ((sig1, q1, Z1), (sig2, q2, Z2)):
        x = np.cumsum((r - qq - 0.5 * s ** 2) * dt + s * np.sqrt(dt) * Z, axis=0)
        out.append(np.exp(np.vstack([np.zeros(Z.shape[1]), x])))
    return out[0], out[1]


def worst_of_autocall_AB(sig1, sig2, rho, ko=1.03, ki=0.75, lockup=3, months=24, r=0.02, n_paths=40000, seed=0,
                         days_per_month=21):
    """A worst-of snowball on two indices: the autocall reads min(S1, S2) (each relative to its start). Returns
    (A, B) with V(c) = A + c B, so the fair coupon is (1 - A) / B."""
    n = months * days_per_month
    dt = 1 / (12 * days_per_month)
    P1, P2 = two_asset_paths(sig1, sig2, rho, n * dt, n, n_paths, r, seed=seed)
    W = np.minimum(P1, P2)
    obs = [m * days_per_month for m in range(lockup, months + 1)]
    disc = np.exp(-r * np.array(obs) * dt)
    a = autocall_on_paths(W, obs, ko, ki, np.zeros(len(obs)), disc).mean()
    b = autocall_on_paths(W, obs, ko, ki, np.array([m / 12 for m in range(lockup, months + 1)]), disc).mean() - a
    return float(a), float(b)


def margrabe(S1, S2, T, s1, s2, rho, q1=0.0, q2=0.0):
    """Margrabe (1978): the option to exchange asset 2 for asset 1, E[e^{-rT}(S1_T - S2_T)^+], by the change of
    numeraire to S2: a Black-Scholes call on S1/S2 struck at 1 with sigma^2 = s1^2 + s2^2 - 2 rho s1 s2. No r."""
    s = np.sqrt(s1 ** 2 + s2 ** 2 - 2 * rho * s1 * s2)
    sT = s * np.sqrt(T)
    d1 = (np.log(S1 / S2) + (q2 - q1 + 0.5 * s ** 2) * T) / sT
    return float(S1 * np.exp(-q1 * T) * N(d1) - S2 * np.exp(-q2 * T) * N(d1 - sT))


def cliquet_bs(sigma, n=12, cap=0.03, floor=-0.03, gfloor=0.0, n_paths=200000, seed=0, T=1.0, reverse=None):
    """A cliquet under Black-Scholes (r = q = 0): n periodic returns r_i, each clipped to [floor, cap], summed, with a
    global floor: max(sum clip(r_i), gfloor). With ``reverse`` = C, the reverse cliquet max(C + sum min(r_i, 0), 0).
    Returns (price, standard error)."""
    dt = T / n
    Z = np.random.default_rng(seed).standard_normal((n, n_paths))
    R = np.exp(-0.5 * sigma ** 2 * dt + sigma * np.sqrt(dt) * Z) - 1
    if reverse is not None:
        pay = np.maximum(reverse + np.minimum(R, 0).sum(axis=0), 0)
    else:
        pay = np.maximum(np.clip(R, floor, cap).sum(axis=0), gfloor)
    return float(pay.mean()), float(pay.std() / np.sqrt(n_paths))


def uvm_solve(values, S_grid, T, sig_lo, sig_hi, r=0.0, n_t=400, upper=True, keep_every=0):
    """The Black-Scholes-Barenblatt solver of uvm_price, vectorized, for payoff values on S_grid: the same scheme
    (volatility chosen from the sign of the discrete gamma, implicit in time). With keep_every = k it also returns
    the value and the chosen volatility every k steps (the solution marching back from expiry)."""
    S = np.asarray(S_grid, float)
    V = np.asarray(values, float).copy()
    dt = T / n_t
    h = np.diff(S)
    hm, hp = h[:-1], h[1:]
    n = len(S)
    Si = S[1:-1]
    film = []
    for k in range(n_t):
        g = 2 * (hm * V[2:] - (hm + hp) * V[1:-1] + hp * V[:-2]) / (hm * hp * (hm + hp))
        sig = np.where(g > 0, sig_hi, sig_lo) if upper else np.where(g > 0, sig_lo, sig_hi)
        if keep_every and k % keep_every == 0:
            film.append((V.copy(), np.concatenate([[sig[0]], sig, [sig[-1]]])))
        a = 0.5 * sig ** 2 * Si ** 2
        cm = 2 * a / (hm * (hm + hp)) - r * Si / (hm + hp)
        cp = 2 * a / (hp * (hm + hp)) + r * Si / (hm + hp)
        lower = np.zeros(n)
        upper_ = np.zeros(n)
        diag = np.ones(n)
        lower[1:-1] = -dt * cm
        upper_[1:-1] = -dt * cp
        diag[1:-1] = 1 + r * dt + dt * (cm + cp)
        rhs = V.copy()
        rhs[0] = 2 * V[1] - V[2]
        rhs[-1] = 2 * V[-2] - V[-3]
        V = _thomas(lower, diag, upper_, rhs)
    if keep_every:
        film.append((V.copy(), film[-1][1] if film else np.full(n, sig_hi)))
        return V, film
    return V


def uvm_lagrangian(payoff, hedges, mkt_prices, S_grid, S0, T, sig_lo, sig_hi, r=0.0, n_t=200, maxfev=80):
    """Avellaneda and Paras (1996): the seller's worst-case price when vanillas can be bought or sold at known market
    prices, min over weights l of U(g - sum l_i h_i)(S0) + sum l_i p_i, by Nelder-Mead. ``payoff`` and ``hedges`` are
    functions of S. Returns {"price", "weights", "unhedged", "iterates": [(weights, price), ...]}."""
    from scipy.optimize import minimize

    S = np.asarray(S_grid, float)
    g0 = payoff(S)
    H = [h(S) for h in hedges]
    its = []

    def obj(w):
        f = g0 - sum(wi * hi for wi, hi in zip(w, H))
        v = float(np.interp(S0, S, uvm_solve(f, S, T, sig_lo, sig_hi, r, n_t)) + np.dot(w, mkt_prices))
        its.append((list(map(float, w)), v))
        return v

    un = obj(np.zeros(len(hedges)))
    res = minimize(obj, np.zeros(len(hedges)), method="Nelder-Mead",
                   options=dict(xatol=1e-3, fatol=1e-4, maxfev=maxfev, initial_simplex=None))
    return {"price": float(min(res.fun, un)), "weights": list(map(float, res.x)), "unhedged": un, "iterates": its}


def kl_worst_case(values, eta, side=-1):
    """Glasserman and Xu (2014): the worst expectation of ``values`` (equally weighted samples under the model P)
    over every model Q within relative entropy eta of P. The optimum is an exponential tilt, dQ/dP proportional to
    exp(theta V), with theta < 0 for the lowest value (side = -1) and theta > 0 for the highest; theta is set so that
    D(Q||P) = eta. Returns (worst value, theta, weights)."""
    v = np.asarray(values, float)
    if eta <= 0:
        return float(v.mean()), 0.0, np.full(len(v), 1 / len(v))
    z = (v - v.mean()) / (v.std() + 1e-300)

    def tilt(th):
        lw = side * th * z
        lw -= lw.max()
        w = np.exp(lw)
        w /= w.sum()
        kl = float(np.sum(w * np.log(np.maximum(w * len(v), 1e-300))))
        return w, kl

    lo, hi = 0.0, 1.0
    while tilt(hi)[1] < eta and hi < 1e4:
        hi *= 2
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if tilt(mid)[1] < eta:
            lo = mid
        else:
            hi = mid
    w, _ = tilt(0.5 * (lo + hi))
    return float(np.sum(w * v)), float(side * 0.5 * (lo + hi) / (v.std() + 1e-300)), w


def digital_delta_estimators(S0, K, T, sigma, n_paths, seed=0, r=0.0, n_steps=21):
    """Three Monte Carlo estimators of a digital call's delta, d/dS0 E[e^{-rT} 1{S_T > K}], on paths of n_steps:
    pathwise (the derivative of an indicator is zero on every path: biased, it returns 0); likelihood ratio
    (differentiate the density of the first step instead: unbiased, noisy); and pathwise plus the boundary term,
    here computed by conditioning on the path before the last step, which makes the payoff smooth (unbiased, quiet).
    Returns per-path samples (pathwise, lr, boundary); their means estimate the delta."""
    g = np.random.default_rng(seed)
    dt = T / n_steps
    Z = g.standard_normal((n_steps, n_paths))
    mu = (r - 0.5 * sigma ** 2) * dt
    x = np.log(S0) + np.cumsum(mu + sigma * np.sqrt(dt) * Z, axis=0)
    ST = np.exp(x[-1])
    D = np.exp(-r * T)
    pathwise = np.zeros(n_paths)
    lr = D * (ST > K) * Z[0] / (S0 * sigma * np.sqrt(dt))
    S_prev = np.exp(x[-2]) if n_steps > 1 else np.full(n_paths, S0)
    d = (np.log(S_prev / K) + mu) / (sigma * np.sqrt(dt))
    boundary = D * norm.pdf(d) / (sigma * np.sqrt(dt)) / S0  # d/dS0 of P(S_T > K | S_prev), with dS_prev/dS0 = S_prev/S0
    return pathwise, lr, boundary
