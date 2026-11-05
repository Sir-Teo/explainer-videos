"""Market microstructure (Part 35): who trades with whom, and what their trades reveal.

Theory: an inventory dealer (Garman 1976; Ho and Stoll 1981), Glosten and Milgrom's (1985) sequential-trade quotes,
Kyle's (1985) one-shot and N-auction equilibria and their continuous-time limit. Measurement: Roll's (1984) spread,
Amihud's (2002) illiquidity, Kyle's lambda from signed flow, bulk-volume VPIN (Easley, Lopez de Prado and O'Hara 2012)
and Hasbrouck's (1995) information shares."""

from __future__ import annotations

import math

import numpy as np


# ---------------------------------------------------------------------------
# Dealers
# ---------------------------------------------------------------------------
def inventory_dealer(n: int, half_spread: float, skew: float, arrival: float = 1.0, sigma: float = 0.0,
                     seed: int = 0) -> dict:
    """A dealer quoting mid -/+ half_spread, shifted by -skew * inventory (Ho-Stoll's inventory effect); buyers and
    sellers arrive with equal probability and trade one unit with probability exp(-arrival * distance) of each quote
    from the fair value, which itself moves with volatility ``sigma`` per step. Returns inventory and P&L paths."""
    rng = np.random.default_rng(seed)
    q, cash, v = 0, 0.0, 100.0
    inv, pnl = np.zeros(n), np.zeros(n)
    for t in range(n):
        v += sigma * rng.standard_normal()
        mid = v - skew * q
        ask, bid = mid + half_spread, mid - half_spread
        if rng.random() < 0.5:                       # a buyer arrives
            if rng.random() < math.exp(-arrival * max(ask - v, 0.0)):
                q -= 1
                cash += ask
        else:
            if rng.random() < math.exp(-arrival * max(v - bid, 0.0)):
                q += 1
                cash -= bid
        inv[t] = q
        pnl[t] = cash + q * v
    return {"inventory": inv, "pnl": pnl}


def gm_quotes(p: float, mu: float, v_hi: float = 1.0, v_lo: float = 0.0) -> tuple[float, float]:
    """Glosten-Milgrom zero-profit quotes when P(V = v_hi) = p and a fraction ``mu`` of traders is informed (the rest
    buy or sell with probability one half): ask = E[V | buy], bid = E[V | sell]."""
    pb_hi, pb_lo = mu + (1 - mu) / 2, (1 - mu) / 2          # P(buy | V high), P(buy | V low)
    p_buy_hi = p * pb_hi / (p * pb_hi + (1 - p) * pb_lo)
    p_sell_hi = p * (1 - pb_hi) / (p * (1 - pb_hi) + (1 - p) * (1 - pb_lo))
    return v_lo + (v_hi - v_lo) * p_buy_hi, v_lo + (v_hi - v_lo) * p_sell_hi


def gm_simulate(mu: float, n: int, v_true: float = 1.0, p0: float = 0.5, seed: int = 0) -> dict:
    """A run of the Glosten-Milgrom market: each period one trader arrives (informed with probability mu, trading
    toward v_true; otherwise buying or selling at random), the dealer quotes the zero-profit ask and bid, and the
    belief updates by Bayes' rule on the trade. Returns beliefs, asks, bids and trades."""
    rng = np.random.default_rng(seed)
    p = p0
    P, A, B, X = [], [], [], []
    for _ in range(n):
        a, b = gm_quotes(p, mu)
        if rng.random() < mu:
            buy = v_true > 0.5
        else:
            buy = rng.random() < 0.5
        P.append(p), A.append(a), B.append(b), X.append(1 if buy else -1)
        p = a if buy else b                                    # the new belief is the price just traded at
    return {"p": np.array(P), "ask": np.array(A), "bid": np.array(B), "trade": np.array(X)}


# ---------------------------------------------------------------------------
# Kyle
# ---------------------------------------------------------------------------
def kyle_one(sigma_v: float, sigma_u: float) -> dict:
    """Kyle's one-shot equilibrium: the insider trades x = beta (v - p0), the market maker sets p = p0 + lambda y on
    total flow y = x + u, with beta = sigma_u/sigma_v, lambda = sigma_v/(2 sigma_u); the insider's expected profit is
    sigma_u sigma_v / 2, and half the value's variance is revealed."""
    beta = sigma_u / sigma_v
    lam = sigma_v / (2 * sigma_u)
    return {"beta": beta, "lambda": lam, "profit": sigma_u * sigma_v / 2, "post_var": sigma_v ** 2 / 2}


def _kyle_back(sig_n: float, N: int, sigma_u2: float):
    """Kyle's backward recursion (1985, Theorem 2) from a guessed final Sigma_N: returns Sigma_0 and the paths."""
    dt = 1.0 / N
    alpha = 0.0
    lam, beta, sig = np.zeros(N), np.zeros(N), np.zeros(N + 1)
    sig[N] = sig_n
    for n in range(N, 0, -1):
        S = sig[n]
        # lambda solves -2 a su2 dt l^3 + 2 su2 dt l^2 + 2 a S l - S = 0, with 0 < a l < 1/2
        c = [-2 * alpha * sigma_u2 * dt, 2 * sigma_u2 * dt, 2 * alpha * S, -S]
        if alpha == 0.0:
            roots = np.roots(c[1:])
        else:
            roots = np.roots(c)
        roots = [r.real for r in roots if abs(r.imag) < 1e-10 and r.real > 0 and alpha * r.real < 0.5]
        L = min(roots)
        bdt = (1 - 2 * alpha * L) / (2 * L * (1 - alpha * L))
        lam[n - 1], beta[n - 1] = L, bdt / dt
        sig[n - 1] = S / (1 - bdt * L)
        alpha = 1 / (4 * L * (1 - alpha * L))
    return sig[0], lam, beta, sig


def kyle_multi(N: int, sigma_v: float = 1.0, sigma_u: float = 1.0) -> dict:
    """Kyle's N-auction equilibrium on [0, 1], noise variance sigma_u^2 per unit time, found by shooting on the final
    conditional variance so that Sigma_0 = sigma_v^2. Returns lambda_n, beta_n, Sigma_n (n = 0..N)."""
    lo, hi = 1e-12, sigma_v ** 2
    for _ in range(200):
        mid = math.sqrt(lo * hi)
        s0 = _kyle_back(mid, N, sigma_u ** 2)[0]
        if s0 > sigma_v ** 2:
            hi = mid
        else:
            lo = mid
    s0, lam, beta, sig = _kyle_back(math.sqrt(lo * hi), N, sigma_u ** 2)
    sig = sig * sigma_v ** 2 / s0
    return {"lambda": lam, "beta": beta, "Sigma": sig, "t": np.arange(N + 1) / N}


def kyle_continuous(v: float, p0: float, sigma_v: float, sigma_u: float, n: int = 1000, seed: int = 0) -> dict:
    """The continuous-time Kyle equilibrium on [0, 1] (Kyle 1985; Back 1992), discretised: lambda = sigma_v/sigma_u,
    the insider trades dx = (v - p)/(lambda (1 - t)) dt, noise du = sigma_u dW, and dp = lambda (dx + du). The price
    ends at v: a Brownian bridge in the insider's filtration."""
    rng = np.random.default_rng(seed)
    lam = sigma_v / sigma_u
    dt = 1.0 / n
    p = np.empty(n + 1)
    p[0] = p0
    x = 0.0
    for k in range(n):
        t = k * dt
        dx = (v - p[k]) / (lam * max(1 - t, dt)) * dt
        du = sigma_u * math.sqrt(dt) * rng.standard_normal()
        p[k + 1] = p[k] + lam * (dx + du)
        x += dx
    return {"t": np.arange(n + 1) * dt, "p": p, "lambda": lam, "x": x}


# ---------------------------------------------------------------------------
# Measurement
# ---------------------------------------------------------------------------
def roll_spread(p) -> float:
    """Roll's (1984) implied effective spread 2 sqrt(-Cov(dp_t, dp_{t-1})); NaN when the covariance is positive."""
    d = np.diff(np.asarray(p, float))
    d = d[np.isfinite(d)]
    c = float(np.cov(d[1:], d[:-1])[0, 1])
    return 2 * math.sqrt(-c) if c < 0 else float("nan")


def amihud(ret, dollar_volume) -> float:
    """Amihud's (2002) illiquidity: the mean of |r| / dollar volume (return per dollar traded)."""
    r = np.asarray(ret, float)
    v = np.asarray(dollar_volume, float)
    m = np.isfinite(r) & np.isfinite(v) & (v > 0)
    return float(np.mean(np.abs(r[m]) / v[m]))


def kyle_lambda(ret, flow) -> dict:
    """Price impact by least squares: r_t = a + lambda * flow_t + e, with its t-statistic and R^2."""
    r = np.asarray(ret, float)
    f = np.asarray(flow, float)
    m = np.isfinite(r) & np.isfinite(f)
    r, f = r[m], f[m]
    X = np.column_stack([np.ones(len(f)), f])
    b, *_ = np.linalg.lstsq(X, r, rcond=None)
    e = r - X @ b
    se = math.sqrt(e.var(ddof=2) / np.sum((f - f.mean()) ** 2))
    return {"lambda": float(b[1]), "t": float(b[1] / se), "r2": float(1 - e.var() / r.var()), "n": int(len(r))}


def bvc_vpin(dp, volume, bucket: float, n_buckets: int = 50) -> np.ndarray:
    """VPIN with bulk volume classification: each bar's volume is split into buys V Phi(dp/sigma_dp) and sells; bars
    fill volume buckets of size ``bucket``; VPIN is the mean |buy - sell| / bucket over the last ``n_buckets`` buckets.
    Returns one VPIN per completed bucket (NaN until enough buckets)."""
    from scipy.stats import norm

    dp = np.asarray(dp, float)
    vol = np.asarray(volume, float)
    sd = np.nanstd(dp)
    buy_frac = norm.cdf(dp / sd)
    imb, fill_b, fill_s = [], 0.0, 0.0
    room = bucket
    for v_, z in zip(vol, buy_frac):
        while v_ > 0:
            take = min(v_, room)
            fill_b += take * z
            fill_s += take * (1 - z)
            v_ -= take
            room -= take
            if room <= 1e-12:
                imb.append(abs(fill_b - fill_s) / bucket)
                fill_b = fill_s = 0.0
                room = bucket
    imb = np.asarray(imb)
    out = np.full(len(imb), np.nan)
    if len(imb) >= n_buckets:
        c = np.cumsum(np.r_[0.0, imb])
        out[n_buckets - 1:] = (c[n_buckets:] - c[:-n_buckets]) / n_buckets
    return out


def hasbrouck_is(p1, p2, lags: int = 5) -> dict:
    """Hasbrouck's (1995) information shares for two cointegrated log prices (cointegrating vector (1, -1)): fit the
    VECM dp_t = a (p1 - p2)_{t-1} + sum_k G_k dp_{t-k} + e_t, take the common-factor weights psi proportional to the
    orthogonal complement of a, and the share of the efficient price's variance from each market, with the upper and
    lower bounds from the two Cholesky orderings. Also returns Gonzalo and Granger's component shares."""
    p1, p2 = np.asarray(p1, float), np.asarray(p2, float)
    d = np.column_stack([np.diff(p1), np.diff(p2)])
    z = (p1 - p2)[:-1]
    T = len(d)
    rows = []
    for t in range(lags, T):
        rows.append(np.r_[1.0, z[t], d[t - lags:t][::-1].ravel()])
    X = np.asarray(rows)
    Y = d[lags:]
    B, *_ = np.linalg.lstsq(X, Y, rcond=None)
    E = Y - X @ B
    alpha = B[1]                                              # loadings on the error-correction term
    # the common-trend weights: psi is proportional to the orthogonal complement of alpha (the scale cancels in the
    # shares, so the short-run matrices are not needed)
    a_perp = np.array([alpha[1], -alpha[0]])
    psi = a_perp
    Om = np.cov(E.T)
    out = {"alpha": alpha.tolist(), "gg": (a_perp / a_perp.sum()).tolist()}
    shares = []
    for order in ((0, 1), (1, 0)):
        P = np.eye(2)[list(order)]
        F = np.linalg.cholesky(P @ Om @ P.T)
        F = P.T @ F @ P
        tot = float(psi @ Om @ psi)
        s = (psi @ F) ** 2 / tot
        shares.append(s)
    s = np.array(shares)
    out["is_low"] = s.min(0).tolist()
    out["is_high"] = s.max(0).tolist()
    out["is_mid"] = ((s.min(0) + s.max(0)) / 2).tolist()
    return out
