"""The House's statistical-arbitrage book (Part 33): pairs, residuals, Ornstein-Uhlenbeck spreads and the optimal band.

* Pairs by distance (Gatev, Goetzmann and Rouwenhorst 2006): normalised prices, the smallest sum of squared
  differences, open at two formation standard deviations, close at the crossing.
* Ornstein-Uhlenbeck fits by AR(1): kappa, theta, the equilibrium sd and the half-life; s-scores (Avellaneda and Lee
  2010) of factor residuals.
* A Kalman-filter hedge ratio (a random-walk beta).
* The Lo-MacKinlay (1990) decomposition of contrarian profits into own autocovariance, cross-autocovariance (lead-lag)
  and the dispersion of means.
* The band rule for an OU spread (research chapter): expected first-passage times from the scale and speed densities,
  the renewal-reward profit rate R(m) = (m - c) / (E_{-m}[T_0] + E_0[tau_m]), and its optimal band, which in units of
  the equilibrium sd and of 1/kappa depends only on the cost.
"""

from __future__ import annotations

import math

import numpy as np
from scipy.special import erf

# ---------------------------------------------------------------------------
# Ornstein-Uhlenbeck fits
# ---------------------------------------------------------------------------


def ou_fit(x, dt: float = 1.0) -> dict:
    """Fit x_{t+1} = a + b x_t + e by least squares and map it to dX = kappa(theta - X)dt + sigma dW: kappa = -ln b/dt,
    theta = a/(1-b), the equilibrium sd s_eq = sd(e)/sqrt(1-b^2), sigma = s_eq sqrt(2 kappa), half-life ln2/kappa."""
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    X = np.column_stack([np.ones(len(x) - 1), x[:-1]])
    (a, b), *_ = np.linalg.lstsq(X, x[1:], rcond=None)
    e = x[1:] - a - b * x[:-1]
    if not 0 < b < 1:
        return {"a": float(a), "b": float(b), "kappa": float("nan"), "theta": float("nan"), "s_eq": float("nan"),
                "sigma": float("nan"), "half_life": float("inf")}
    kappa = -math.log(b) / dt
    s_eq = float(np.std(e, ddof=2) / math.sqrt(1 - b * b))
    return {"a": float(a), "b": float(b), "kappa": kappa, "theta": float(a / (1 - b)), "s_eq": s_eq,
            "sigma": s_eq * math.sqrt(2 * kappa), "half_life": math.log(2) / kappa}


def s_score(x, window: int = 60):
    """Avellaneda-Lee s-score at each t: fit an OU to the last ``window`` values of x (a cumulative residual) and
    return (x_t - theta)/s_eq, NaN when the fit is not mean-reverting. Also returns the fitted kappa."""
    x = np.asarray(x, float)
    s = np.full(len(x), np.nan)
    k = np.full(len(x), np.nan)
    for t in range(window - 1, len(x)):
        f = ou_fit(x[t - window + 1:t + 1])
        if np.isfinite(f["kappa"]) and f["s_eq"] > 0:
            s[t] = (x[t] - f["theta"]) / f["s_eq"]
            k[t] = f["kappa"]
    return s, k


# ---------------------------------------------------------------------------
# Kalman hedge ratio
# ---------------------------------------------------------------------------


def kalman_beta(y, x, q: float = 1e-5, r: float = 1e-3):
    """y_t = alpha_t + beta_t x_t + e_t (var r), (alpha, beta) a random walk with covariance q I: the filtered state
    after each observation. Returns (alpha, beta) arrays."""
    y, x = np.asarray(y, float), np.asarray(x, float)
    m = np.zeros(2)
    P = np.eye(2)
    Q = q * np.eye(2)
    A, B = np.full(len(y), np.nan), np.full(len(y), np.nan)
    for t in range(len(y)):
        P = P + Q
        if np.isfinite(y[t]) and np.isfinite(x[t]):
            H = np.array([1.0, x[t]])
            S = H @ P @ H + r
            K = P @ H / S
            m = m + K * (y[t] - H @ m)
            P = P - np.outer(K, H) @ P
        A[t], B[t] = m
    return A, B


# ---------------------------------------------------------------------------
# Pairs by distance
# ---------------------------------------------------------------------------


def norm_prices(R):
    """Cumulative total-return index of each column, starting at one (NaN returns treated as zero)."""
    return np.cumprod(1 + np.nan_to_num(np.asarray(R, float)), axis=0)


def distance_pairs(P, top: int = 20):
    """The ``top`` pairs (i, j) with the smallest sum of squared differences of normalised prices over a formation
    window P (T x N), and the formation sd of each pair's spread."""
    P = np.asarray(P, float) / np.asarray(P, float)[0]
    N = P.shape[1]
    ssd = []
    for i in range(N):
        d = P[:, i + 1:] - P[:, [i]]
        s = np.sum(d * d, 0)
        for k, v in enumerate(s):
            ssd.append((v, i, i + 1 + k))
    ssd.sort()
    out = []
    for v, i, j in ssd[:top]:
        out.append((i, j, float(np.std(P[:, i] - P[:, j]))))
    return out


def trade_pair(Ri, Rj, sd, open_k: float = 2.0):
    """Trade one pair over a trading window: normalised prices from the window start; when the spread p_i - p_j
    exceeds open_k x sd, short i and long j (and the reverse), one dollar each side; close when it crosses zero.
    Returns the daily return on the two dollars committed (zero while flat) and the number of round trips."""
    pi, pj = norm_prices(Ri[:, None])[:, 0], norm_prices(Rj[:, None])[:, 0]
    pos = 0
    ret = np.zeros(len(Ri))
    trips = 0
    for t in range(len(Ri)):
        if t > 0 and pos != 0:
            ret[t] = 0.5 * pos * (np.nan_to_num(Rj[t]) - np.nan_to_num(Ri[t]))
        s = pi[t] - pj[t]
        if pos == 0 and abs(s) > open_k * sd:
            pos = 1 if s > 0 else -1          # +1: long j, short i
            trips += 1
        elif pos != 0 and (s * pos) <= 0:
            pos = 0
    return ret, trips


# ---------------------------------------------------------------------------
# Lo-MacKinlay
# ---------------------------------------------------------------------------


def lo_mackinlay(R, k: int = 1) -> dict:
    """Decompose the expected profit of the contrarian w_{i,t} = -(1/N)(r_{i,t-k} - rbar_{t-k}):
    E pi = C - O - D with own-autocovariance part O = (N-1)/N^2 tr(Gamma_k), cross part
    C = (iota' Gamma_k iota - tr Gamma_k)/N^2 and D the cross-sectional variance of mean returns; here reported as
    profit = -O_term + C_term - D (O_term = (N-1)/N^2 tr), and the realised mean profit for comparison."""
    R = np.asarray(R, float)
    R = R[np.isfinite(R).all(1)]
    T, N = R.shape
    mu = R.mean(0)
    X = R - mu
    G = X[k:].T @ X[:-k] / (T - k)            # G[i, j] = Cov(r_{i,t}, r_{j,t-k})
    tr = float(np.trace(G))
    own = -(N - 1) / N ** 2 * tr
    cross = float((G.sum() - tr) / N ** 2)
    disp = -float(np.mean(mu ** 2) - np.mean(mu) ** 2)
    w = -(R[:-k] - R[:-k].mean(1, keepdims=True)) / N
    pi = np.sum(w * R[k:], 1)
    return {"own": own, "cross": cross, "disp": disp, "total": own + cross + disp, "realised": float(pi.mean())}


# ---------------------------------------------------------------------------
# The band rule (research chapter)
# ---------------------------------------------------------------------------


def _inner(y, kappa, sigma):
    """int_{-inf}^{y} exp(-kappa z^2 / sigma^2) dz."""
    c = math.sqrt(kappa) / sigma
    return (math.sqrt(math.pi) / (2 * c)) * (1 + erf(c * y))


def _inner0(y, kappa, sigma):
    """int_{0}^{y} exp(-kappa z^2 / sigma^2) dz."""
    c = math.sqrt(kappa) / sigma
    return (math.sqrt(math.pi) / (2 * c)) * erf(c * y)


def _simpson(f, a, b, n=2000):
    xs = np.linspace(a, b, 2 * n + 1)
    ys = np.array([f(x) for x in xs])
    h = (b - a) / (2 * n)
    return float(h / 3 * (ys[0] + ys[-1] + 4 * ys[1:-1:2].sum() + 2 * ys[2:-1:2].sum()))


def ou_time_to_mean(m: float, kappa: float, sigma: float) -> float:
    """E_{-m}[T_0] for dX = -kappa X dt + sigma dW: (2/sigma^2) int_{-m}^{0} e^{kappa y^2/sigma^2} int_{-inf}^{y}
    e^{-kappa z^2/sigma^2} dz dy (Dynkin: the solution of (sigma^2/2) f'' - kappa x f' = -1 with f(0) = 0 and f'
    bounded at -infinity)."""
    k2 = kappa / sigma ** 2
    return (2 / sigma ** 2) * _simpson(lambda y: math.exp(k2 * y * y) * _inner(y, kappa, sigma), -m, 0.0)


def ou_time_to_band(m: float, kappa: float, sigma: float) -> float:
    """E_0[tau], tau the first time |X| = m, for the same OU started at its mean: (2/sigma^2) int_0^m
    e^{kappa y^2/sigma^2} int_0^y e^{-kappa z^2/sigma^2} dz dy (f(+-m) = 0, f'(0) = 0 by symmetry)."""
    k2 = kappa / sigma ** 2
    return (2 / sigma ** 2) * _simpson(lambda y: math.exp(k2 * y * y) * _inner0(y, kappa, sigma), 0.0, m)


def band_rate(m: float, kappa: float, sigma: float, c: float) -> float:
    """The long-run profit per unit time of the band rule (flat at the mean; enter one unit against the deviation
    when |X| reaches m; exit at the mean), by the renewal-reward theorem: (m - c) / (E_{-m}[T_0] + E_0[tau_m]),
    with c the round-trip cost in units of the spread."""
    return (m - c) / (ou_time_to_mean(m, kappa, sigma) + ou_time_to_band(m, kappa, sigma))


def optimal_band(kappa: float, sigma: float, c: float, grid=None) -> tuple[float, float]:
    """The band m* maximising band_rate, by a grid search refined once: returns (m*, R(m*))."""
    s_eq = sigma / math.sqrt(2 * kappa)
    g = np.linspace(max(c * 1.0001, 0.02 * s_eq), 3.0 * s_eq, 120) if grid is None else grid
    r = np.array([band_rate(m, kappa, sigma, c) for m in g])
    i = int(np.argmax(r))
    lo, hi = g[max(i - 1, 0)], g[min(i + 1, len(g) - 1)]
    g2 = np.linspace(lo, hi, 41)
    r2 = np.array([band_rate(m, kappa, sigma, c) for m in g2])
    j = int(np.argmax(r2))
    return float(g2[j]), float(r2[j])


def simulate_band(m: float, kappa: float, sigma: float, c: float, T: float, dt: float = 0.01, seed: int = 0,
                  book_at_bands: bool = True) -> dict:
    """Simulate the OU exactly on a grid of step dt for time T, run the band rule, and report the realised profit
    per unit time and the number of trades. With ``book_at_bands`` each trade is booked at the band and the mean
    (m - c), as under continuous monitoring, so only the timing is simulated; otherwise at the grid prices, which adds
    the overshoot of discrete monitoring."""
    rng = np.random.default_rng(seed)
    n = int(T / dt)
    b = math.exp(-kappa * dt)
    sd = sigma * math.sqrt((1 - b * b) / (2 * kappa))
    x, pos, entry, pnl, trades = 0.0, 0, 0.0, 0.0, 0
    z = rng.standard_normal(n)
    for t in range(n):
        x = b * x + sd * z[t]
        if pos == 0 and abs(x) >= m:
            pos, entry = (-1 if x > 0 else 1), x
        elif pos != 0 and x * pos >= 0:
            pnl += (m - c) if book_at_bands else pos * (x - entry) - c
            trades += 1
            pos = 0
    return {"rate": pnl / T, "trades": trades}


def band_curve(cs) -> np.ndarray:
    """The universal optimal band: m*/s_eq as a function of c/s_eq (kappa drops out by scaling), on the costs ``cs``."""
    k, sig = 1.0, math.sqrt(2.0)
    return np.array([optimal_band(k, sig, max(float(c), 1e-4))[0] for c in cs])


__all__ = ["ou_fit", "s_score", "kalman_beta", "norm_prices", "distance_pairs", "trade_pair", "lo_mackinlay",
           "ou_time_to_mean", "ou_time_to_band", "band_rate", "optimal_band", "simulate_band", "band_curve"]
