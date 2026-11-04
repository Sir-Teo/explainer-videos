"""The House's systematic macro books (Part 32): trend, volatility targeting, risk parity, and the theory of why trend
following is long a straddle.

* Time-series momentum (Moskowitz, Ooi and Pedersen 2012): each asset long or short on the sign of its own past
  return, sized to a common ex-ante volatility, rebalanced monthly.
* Volatility targeting (Moreira and Muir 2017; Harvey et al. 2018): exposure scaled by an EWMA volatility forecast,
  with a leverage cap.
* Risk parity: inverse-volatility weights across asset classes, levered to a target volatility on a rolling
  covariance (the All Weather idea, in its simplest form).
* The trend identity: over a block of n returns, the linear trend rule (position = the return so far in the block)
  earns exactly half the squared block return minus half its realised variance; under i.i.d. returns its mean is the
  sum of the autocovariances and its skewness is 2^{3/2}(n - 2)/sqrt(n(n - 1)).

Arrays are (T x N) days by assets; returns are daily simple or log excess returns as stated; NaN marks a missing day.
"""

from __future__ import annotations

import math

import numpy as np


def ewma_vol(r, com: float = 60.0, ann: float = 252.0, min_obs: int = 60):
    """Exponentially weighted volatility (centre of mass ``com`` days), annualised, known at the close of each day
    (it includes that day's return). NaN until ``min_obs`` returns have been seen."""
    r = np.asarray(r, float)
    one = r.ndim == 1
    R = r[:, None] if one else r
    lam = com / (1.0 + com)
    T, N = R.shape
    v = np.full(N, np.nan)
    cnt = np.zeros(N)
    out = np.full((T, N), np.nan)
    for t in range(T):
        x = R[t]
        ok = np.isfinite(x)
        v = np.where(ok & np.isfinite(v), lam * v + (1 - lam) * x ** 2, np.where(ok & ~np.isfinite(v), x ** 2, v))
        cnt += ok
        out[t] = np.where(cnt >= min_obs, np.sqrt(v * ann), np.nan)
    return out[:, 0] if one else out


def month_ends(dates):
    """Indices of the last trading day of each month in ``dates`` (YYYYMMDD ints)."""
    d = np.asarray(dates)
    m = d // 100
    return np.flatnonzero(np.r_[m[1:] != m[:-1], True])


def tsmom_positions(R, vol, dates, lookback: int = 252, target: float = 0.40, rule: str = "sign"):
    """Time-series momentum positions, set at each month end and held until the next: ``sign`` (or, with
    rule="linear", the trailing return over its volatility, capped at +-2) of the trailing ``lookback``-day return,
    times target / ex-ante volatility. Returns (T x N) positions applied to the next day's return."""
    R = np.asarray(R, float)
    T, N = R.shape
    cs = np.vstack([np.zeros(N), np.nancumsum(np.nan_to_num(R), axis=0)])
    W = np.full((T, N), np.nan)
    ends = month_ends(dates)
    cur = np.zeros(N)
    j = 0
    for t in range(T):
        if j < len(ends) and t == ends[j]:
            j += 1
            if t >= lookback:
                past = cs[t + 1] - cs[t + 1 - lookback]
                have = np.isfinite(R[t - lookback + 1:t + 1]).sum(0) >= 0.9 * lookback
                sig = np.sign(past) if rule == "sign" else np.clip(past / (vol[t] * math.sqrt(lookback / 252)), -2, 2)
                cur = np.where(have & np.isfinite(vol[t]) & (vol[t] > 0), sig * target / vol[t], 0.0)
        W[t] = cur
    return W


def book(R, W, scale_to=None, com: float = 60.0):
    """Daily returns of holding ``W[t]`` over day t+1, averaged across the assets with a position (equal risk
    budget), optionally scaled ex ante to ``scale_to`` annual volatility with an EWMA of the book's own returns."""
    R, W = np.asarray(R, float), np.asarray(W, float)
    T, N = R.shape
    pnl = np.full(T, np.nan)
    for t in range(1, T):
        w = W[t - 1]
        ok = np.isfinite(w) & (w != 0) & np.isfinite(R[t])
        n = (np.isfinite(W[t - 1]) & (np.abs(np.nan_to_num(W[t - 1])) > 0)).sum()
        if n:
            pnl[t] = float(np.sum(w[ok] * R[t, ok])) / n
    if scale_to is None:
        return pnl
    v = ewma_vol(pnl, com=com)
    k = np.r_[np.nan, scale_to / v[:-1]]
    return pnl * np.clip(k, 0, 10)


def vol_target(r, target: float = 0.10, com: float = 60.0, cap: float = 3.0):
    """A volatility-targeted version of one return series: exposure target/sigma_hat (known the day before), capped
    at ``cap``. Returns (scaled returns, exposures)."""
    r = np.asarray(r, float)
    v = ewma_vol(r, com=com)
    x = np.r_[np.nan, np.clip(target / v[:-1], 0, cap)]
    return r * x, x


def inverse_vol_weights(vol):
    """Weights proportional to 1/sigma across the assets with a forecast, summing to one."""
    v = np.asarray(vol, float)
    w = np.where(np.isfinite(v) & (v > 0), 1 / v, 0.0)
    return w / w.sum() if w.sum() > 0 else w


def risk_parity(R, dates, groups, target: float = 0.10, window: int = 252, cap: float = 4.0):
    """Risk parity across asset classes: within each group inverse-volatility weights, across groups equal risk
    (each group's inverse-volatility sub-portfolio weighted by 1/its volatility), then the whole book levered to
    ``target`` on the trailing ``window`` days' covariance, leverage capped at ``cap``; rebalanced monthly. Returns
    (daily returns, gross leverage at each rebalance, weights (T x N))."""
    R = np.asarray(R, float)
    T, N = R.shape
    W = np.full((T, N), np.nan)
    lev = np.full(T, np.nan)
    cur = np.zeros(N)
    ends = set(month_ends(dates).tolist())
    for t in range(T):
        if t in ends and t >= window:
            X = R[t - window + 1:t + 1]
            ok = np.isfinite(X).all(0)
            sd = np.where(ok, np.nanstd(X, 0) * math.sqrt(252), np.nan)
            w = np.zeros(N)
            for g in set(groups):
                idx = np.array([i for i in range(N) if groups[i] == g and ok[i]])
                if len(idx) == 0:
                    continue
                wg = inverse_vol_weights(sd[idx])
                sg = float(np.sqrt(wg @ np.cov(X[:, idx].T).reshape(len(idx), len(idx)) @ wg) * math.sqrt(252))
                w[idx] = wg / sg
            if w.sum() > 0:
                C = np.cov(X[:, ok].T) * 252
                s = float(np.sqrt(w[ok] @ C @ w[ok]))
                k = min(target / s, cap / np.abs(w).sum()) if s > 0 else 0.0
                cur = w * k
                lev[t] = float(np.abs(cur).sum())
        W[t] = cur
    pnl = np.full(T, np.nan)
    for t in range(1, T):
        ok = np.isfinite(R[t])
        pnl[t] = float(np.sum(W[t - 1][ok] * R[t, ok]))
    return pnl, lev, W


# ---------------------------------------------------------------------------
# The trend identity (research chapter)
# ---------------------------------------------------------------------------


def linear_trend_blocks(r, n: int):
    """Split ``r`` into consecutive blocks of n returns; in each, hold a position equal to the return so far in the
    block (zero on its first day). Returns per block: (S = block return, Q = realised variance sum of squares,
    P = the rule's P&L), with P == (S^2 - Q)/2 exactly."""
    r = np.asarray(r, float)
    r = r[np.isfinite(r)]
    k = len(r) // n
    B = r[:k * n].reshape(k, n)
    pos = np.cumsum(B, 1) - B                # the return so far, before today's
    P = np.sum(pos * B, 1)
    S = B.sum(1)
    Q = np.sum(B ** 2, 1)
    return S, Q, P


def trend_skew_theory(n: int) -> float:
    """Skewness of the linear trend rule's block P&L for i.i.d. normal returns: P = sigma^2 sum_{s<t} z_s z_t, whose
    variance is n(n-1)/2 and third moment n(n-1)(n-2) (one term per triangle), so 2^{3/2}(n-2)/sqrt(n(n-1)); -> 2
    sqrt 2 as n grows."""
    return 2 ** 1.5 * (n - 2) / math.sqrt(n * (n - 1)) if n > 1 else 0.0


def trend_mean_theory(acov, n: int) -> float:
    """Expected block P&L of the linear trend rule for a stationary series with autocovariances acov[k] (k >= 1):
    E P = sum_{s<t} Cov(r_s, r_t) = sum_{k=1}^{n-1} (n - k) acov[k]. Zero for a random walk."""
    return float(sum((n - k) * acov[k] for k in range(1, n)))


def autocov(r, kmax: int):
    """Sample autocovariances gamma_0..gamma_kmax of a series (NaN dropped)."""
    r = np.asarray(r, float)
    r = r[np.isfinite(r)] - np.nanmean(r)
    T = len(r)
    return np.array([np.sum(r[k:] * r[:T - k]) / T for k in range(kmax + 1)])


# ---------------------------------------------------------------------------
# Scores
# ---------------------------------------------------------------------------


def sharpe(r, ann: float = 252.0) -> float:
    r = np.asarray(r, float)
    r = r[np.isfinite(r)]
    return float(r.mean() / r.std(ddof=1) * math.sqrt(ann)) if len(r) > 2 and r.std() > 0 else float("nan")


def max_drawdown(r) -> float:
    """Worst peak-to-trough fall of the cumulative simple-return path (as a negative fraction)."""
    r = np.nan_to_num(np.asarray(r, float))
    w = np.cumprod(1 + r)
    return float(np.min(w / np.maximum.accumulate(w) - 1))


def skewness(r) -> float:
    r = np.asarray(r, float)
    r = r[np.isfinite(r)]
    z = r - r.mean()
    return float(np.mean(z ** 3) / np.mean(z ** 2) ** 1.5)


__all__ = ["ewma_vol", "month_ends", "tsmom_positions", "book", "vol_target", "inverse_vol_weights", "risk_parity",
           "linear_trend_blocks", "trend_skew_theory", "trend_mean_theory", "autocov", "sharpe", "max_drawdown",
           "skewness"]
