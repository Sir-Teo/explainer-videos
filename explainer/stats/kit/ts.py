"""statkit.ts (I): time series for Part 17 of *Statistics, Built*: the autocorrelation function, ARMA processes and
their roots, Yule–Walker and least-squares fitting, the Ljung–Box test, forecasts with intervals, exponential smoothing,
classical decomposition, MASE, and the standard error of an autocorrelated mean (Newey–West).  Checked against
statsmodels in ``tests/test_stats_kit_ts.py``.
"""

from __future__ import annotations

import numpy as np
from scipy import optimize, special, stats


# ---------------------------------------------------------------------------------------------------------------------
# Autocorrelation
# ---------------------------------------------------------------------------------------------------------------------
def acvf(x, nlags: int) -> np.ndarray:
    """Sample autocovariances gamma(0..nlags), with divisor n (so the matrix they make is positive definite)."""
    x = np.asarray(x, float)
    n = len(x)
    d = x - x.mean()
    return np.array([np.dot(d[: n - k], d[k:]) / n for k in range(nlags + 1)])


def acf(x, nlags: int) -> np.ndarray:
    g = acvf(x, nlags)
    return g / g[0]


def durbin_levinson(rho) -> tuple[np.ndarray, np.ndarray]:
    """From autocorrelations rho(0..K): the partial autocorrelations phi_kk (k = 1..K), and the AR(K) coefficients."""
    rho = np.asarray(rho, float)
    K = len(rho) - 1
    pacf = np.zeros(K)
    phi = np.zeros(0)
    for k in range(1, K + 1):
        if k == 1:
            a = rho[1]
            new = np.array([a])
        else:
            a = (rho[k] - np.dot(phi, rho[k - 1:0:-1])) / (1 - np.dot(phi, rho[1:k]))
            new = np.r_[phi - a * phi[::-1], a]
        pacf[k - 1] = a
        phi = new
    return pacf, phi


def pacf(x, nlags: int) -> np.ndarray:
    return durbin_levinson(acf(x, nlags))[0]


# ---------------------------------------------------------------------------------------------------------------------
# ARMA processes
# ---------------------------------------------------------------------------------------------------------------------
def simulate_arma(phi=(), theta=(), n: int = 200, rng: np.random.Generator | None = None, sigma: float = 1.0,
                  burn: int = 200, mu: float = 0.0) -> np.ndarray:
    """X_t - mu = sum phi_i (X_{t-i} - mu) + e_t + sum theta_j e_{t-j}, e_t ~ N(0, sigma^2), after a burn-in."""
    rng = rng or np.random.default_rng()
    phi, theta = np.asarray(phi, float), np.asarray(theta, float)
    p, q = len(phi), len(theta)
    N = n + burn
    e = rng.normal(0, sigma, N)
    x = np.zeros(N)
    for t in range(N):
        ar = sum(phi[i] * x[t - 1 - i] for i in range(p) if t - 1 - i >= 0)
        ma = sum(theta[j] * e[t - 1 - j] for j in range(q) if t - 1 - j >= 0)
        x[t] = ar + e[t] + ma
    return x[burn:] + mu


def ar_roots(phi) -> np.ndarray:
    """Roots of 1 - phi_1 z - ... - phi_p z^p.  Stationary (causal) iff all lie outside the unit circle."""
    phi = np.asarray(phi, float)
    coef = np.r_[-phi[::-1], 1.0]  # highest power first
    return np.roots(coef)


def ma_roots(theta) -> np.ndarray:
    """Roots of 1 + theta_1 z + ... + theta_q z^q.  Invertible iff all lie outside the unit circle."""
    theta = np.asarray(theta, float)
    return np.roots(np.r_[theta[::-1], 1.0])


def is_stationary(phi) -> bool:
    return bool(len(phi) == 0 or np.all(np.abs(ar_roots(phi)) > 1))


def psi_weights(phi=(), theta=(), k: int = 20) -> np.ndarray:
    """The MA(infinity) weights psi_0 .. psi_{k-1}: X_t = sum psi_j e_{t-j}."""
    phi, theta = np.asarray(phi, float), np.asarray(theta, float)
    psi = np.zeros(k)
    psi[0] = 1.0
    for j in range(1, k):
        v = theta[j - 1] if j - 1 < len(theta) else 0.0
        v += sum(phi[i] * psi[j - 1 - i] for i in range(len(phi)) if j - 1 - i >= 0)
        psi[j] = v
    return psi


def arma_acf(phi=(), theta=(), nlags: int = 20, terms: int = 2000) -> np.ndarray:
    """Theoretical autocorrelations, from the psi weights (truncated at ``terms``)."""
    psi = psi_weights(phi, theta, terms + nlags)
    g = np.array([np.dot(psi[: terms], psi[k: k + terms]) for k in range(nlags + 1)])
    return g / g[0]


def ar2_period(phi1: float, phi2: float) -> float:
    """The pseudo-period 2 pi / arccos(phi1 / (2 sqrt(-phi2))) of an AR(2) with complex roots (phi2 < 0)."""
    return float(2 * np.pi / np.arccos(phi1 / (2 * np.sqrt(-phi2))))


# ---------------------------------------------------------------------------------------------------------------------
# Fitting
# ---------------------------------------------------------------------------------------------------------------------
def yule_walker(x, p: int) -> dict:
    """Yule (1927), Walker (1931): solve Gamma phi = gamma from the sample autocovariances."""
    x = np.asarray(x, float)
    g = acvf(x, p)
    G = np.array([[g[abs(i - j)] for j in range(p)] for i in range(p)])
    phi = np.linalg.solve(G, g[1: p + 1])
    sigma2 = float(g[0] - np.dot(phi, g[1: p + 1]))
    return {"phi": phi, "sigma2": sigma2, "mu": float(x.mean())}


def ar_ols(x, p: int) -> dict:
    """Conditional least squares: regress x_t on 1, x_{t-1}, ..., x_{t-p}."""
    x = np.asarray(x, float)
    n = len(x)
    X = np.column_stack([np.ones(n - p)] + [x[p - i - 1: n - i - 1] for i in range(p)])
    y = x[p:]
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    r = y - X @ b
    sigma2 = float(r @ r / (len(y) - p - 1))
    cov = sigma2 * np.linalg.inv(X.T @ X)
    phi = b[1:]
    mu = float(b[0] / (1 - phi.sum())) if abs(1 - phi.sum()) > 1e-12 else float("nan")
    return {"phi": phi, "const": float(b[0]), "mu": mu, "sigma2": sigma2, "se": np.sqrt(np.diag(cov))[1:], "resid": r}


def ar_resid(x, phi, mu: float) -> np.ndarray:
    x = np.asarray(x, float) - mu
    p = len(phi)
    return np.array([x[t] - np.dot(phi, x[t - p: t][::-1]) for t in range(p, len(x))])


def ljung_box(resid, h: int, fitdf: int = 0) -> tuple[float, float]:
    """Ljung & Box (1978): Q = n(n+2) sum_{k<=h} r_k^2/(n-k), chi^2 on h - fitdf degrees of freedom."""
    r = acf(resid, h)[1:]
    n = len(resid)
    Q = float(n * (n + 2) * np.sum(r ** 2 / (n - np.arange(1, h + 1))))
    return Q, float(stats.chi2(h - fitdf).sf(Q))


def aic_ar(x, pmax: int) -> np.ndarray:
    """AIC of AR(p) fits by least squares on a common sample (t > pmax), p = 0..pmax."""
    x = np.asarray(x, float)
    n = len(x)
    out = []
    for p in range(pmax + 1):
        X = np.column_stack([np.ones(n - pmax)] + [x[pmax - i - 1: n - i - 1] for i in range(p)])
        y = x[pmax:]
        b, *_ = np.linalg.lstsq(X, y, rcond=None)
        s2 = np.mean((y - X @ b) ** 2)
        out.append(len(y) * np.log(s2) + 2 * (p + 1))
    return np.array(out)


# ---------------------------------------------------------------------------------------------------------------------
# Forecasting
# ---------------------------------------------------------------------------------------------------------------------
def ar_forecast(x, phi, mu: float, sigma2: float, h: int, level: float = 0.95) -> dict:
    """Best linear predictions h steps ahead from an AR(p), with normal prediction intervals from the psi weights."""
    x = list(np.asarray(x, float) - mu)
    phi = np.asarray(phi, float)
    p = len(phi)
    f = []
    for _ in range(h):
        v = float(np.dot(phi, x[-1: -p - 1: -1])) if p else 0.0
        f.append(v)
        x.append(v)
    psi = psi_weights(phi, (), h)
    se = np.sqrt(sigma2 * np.cumsum(psi ** 2))
    z = stats.norm.ppf(0.5 + level / 2)
    f = np.array(f) + mu
    return {"mean": f, "se": se, "lo": f - z * se, "hi": f + z * se}


def ses(y, alpha: float) -> np.ndarray:
    """Simple exponential smoothing: one-step forecasts yhat_{t+1} = alpha y_t + (1 - alpha) yhat_t (yhat_1 = y_1)."""
    y = np.asarray(y, float)
    f = np.empty(len(y) + 1)
    f[0] = y[0]
    for t in range(len(y)):
        f[t + 1] = alpha * y[t] + (1 - alpha) * f[t]
    return f


def holt_winters(y, m: int, alpha: float, beta: float, gamma: float, h: int = 0) -> dict:
    """Additive Holt–Winters (Holt 1957; Winters 1960): level, trend and m seasonal terms.  Returns the one-step fitted
    values and h forecasts beyond the end."""
    y = np.asarray(y, float)
    n = len(y)
    level = y[:m].mean()
    trend = (y[m: 2 * m].mean() - y[:m].mean()) / m
    season = list(y[:m] - level)
    fitted = np.empty(n)
    for t in range(n):
        s = season[t]
        fitted[t] = level + trend + s
        new_level = alpha * (y[t] - s) + (1 - alpha) * (level + trend)
        trend = beta * (new_level - level) + (1 - beta) * trend
        season.append(gamma * (y[t] - new_level) + (1 - gamma) * s)
        level = new_level
    fc = np.array([level + (k + 1) * trend + season[n + (k % m)] for k in range(h)])
    return {"fitted": fitted, "forecast": fc, "level": level, "trend": trend}


def fit_holt_winters(y, m: int, h: int = 0) -> dict:
    """Choose alpha, beta, gamma in (0, 1) by minimizing the one-step squared error (after the first season)."""
    y = np.asarray(y, float)

    def sse(p):
        a, b, g = special.expit(p)
        r = y - holt_winters(y, m, a, b, g)["fitted"]
        return float(np.sum(r[m:] ** 2))

    best = min((optimize.minimize(sse, x0, method="Nelder-Mead", options={"xatol": 1e-6, "fatol": 1e-8, "maxiter": 4000})
                for x0 in ([0, -2, -1], [1, -3, 0], [-1, -2, -2])), key=lambda r: r.fun)
    a, b, g = special.expit(best.x)
    out = holt_winters(y, m, a, b, g, h)
    out.update({"alpha": float(a), "beta": float(b), "gamma": float(g), "sse": float(best.fun)})
    return out


def moving_average(y, m: int) -> np.ndarray:
    """The centred moving average of order m (a 2 x m average when m is even); NaN at the ends."""
    y = np.asarray(y, float)
    n = len(y)
    if m % 2:
        w = np.ones(m) / m
    else:
        w = np.r_[0.5, np.ones(m - 1), 0.5] / m
    k = len(w) // 2
    out = np.full(n, np.nan)
    for t in range(k, n - k):
        out[t] = np.dot(w, y[t - k: t + k + 1])
    return out


def decompose(y, m: int) -> dict:
    """Classical additive decomposition: trend (centred MA), seasonal (mean detrended value per season, centred), and
    the remainder."""
    y = np.asarray(y, float)
    tr = moving_average(y, m)
    det = y - tr
    s = np.array([np.nanmean(det[k::m]) for k in range(m)])
    s -= s.mean()
    seasonal = np.resize(s, len(y))
    return {"trend": tr, "seasonal": seasonal, "remainder": y - tr - seasonal, "figure": s}


def mase(actual, forecast, train, m: int = 1) -> float:
    """Hyndman & Koehler (2006): mean absolute error scaled by the in-sample MAE of the seasonal naive forecast."""
    train = np.asarray(train, float)
    scale = np.mean(np.abs(train[m:] - train[:-m]))
    return float(np.mean(np.abs(np.asarray(actual, float) - np.asarray(forecast, float))) / scale)


# ---------------------------------------------------------------------------------------------------------------------
# The mean of a dependent series
# ---------------------------------------------------------------------------------------------------------------------
def ar1_neff(n: int, rho: float) -> float:
    """The effective sample size of the mean of an AR(1): about n (1 - rho)/(1 + rho)."""
    return n * (1 - rho) / (1 + rho)


def newey_west_se(x, lags: int | None = None) -> float:
    """Newey & West (1987): the SE of the mean from Bartlett-weighted autocovariances (HAC)."""
    x = np.asarray(x, float)
    n = len(x)
    L = int(np.floor(4 * (n / 100) ** (2 / 9))) if lags is None else lags
    g = acvf(x, L)
    lrv = g[0] + 2 * sum((1 - k / (L + 1)) * g[k] for k in range(1, L + 1))
    return float(np.sqrt(max(lrv, 0.0) / n))


def block_bootstrap_means(x, block: int, B: int, rng: np.random.Generator) -> np.ndarray:
    """Künsch's (1989) moving-block bootstrap: glue together randomly chosen overlapping blocks of length ``block`` to
    make series of the original length, keeping the dependence within blocks; returns the B resampled means."""
    x = np.asarray(x, float)
    n = len(x)
    k = int(np.ceil(n / block))
    starts = rng.integers(0, n - block + 1, size=(B, k))
    idx = (starts[:, :, None] + np.arange(block)[None, None, :]).reshape(B, -1)[:, :n]
    return x[idx].mean(1)


def random_walk(n: int, rng: np.random.Generator, sigma: float = 1.0) -> np.ndarray:
    return np.cumsum(rng.normal(0, sigma, n))
