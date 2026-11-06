"""statkit.ts (I): time series for Part 17 of *Statistics, Built*: the autocorrelation function, ARMA processes and
their roots, Yule–Walker and least-squares fitting, the Ljung–Box test, forecasts with intervals, exponential smoothing,
classical decomposition, MASE, and the standard error of an autocorrelated mean (Newey–West).  Checked against
statsmodels in ``tests/test_stats_kit_ts.py``.

statkit.ts (II), Part 38: Hurst's R/S, the periodogram, Welch and multitaper spectra; Dickey–Fuller and KPSS with
MacKinnon's critical values; Engle–Granger and Johansen cointegration; ARCH tests and GARCH(1,1) by maximum
likelihood; fractional differencing, ARFIMA simulation and the GPH estimator; the Kalman filter and RTS smoother for
a general linear Gaussian state space, its likelihood and EM; the extended and unscented filters, a bootstrap particle
filter, Hamilton's regime-switching filter; VARs, Granger causality and impulse responses; the stationary bootstrap.
Checked in ``tests/test_stats_kit_ts2.py``.
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


# =====================================================================================================================
# statkit.ts (II): Part 38
# =====================================================================================================================
def hurst_rs(x, sizes=None) -> dict:
    """Hurst's rescaled range: for each block size m, the mean over non-overlapping blocks of R/S, where R is the range
    of the block's cumulative deviations from its mean and S its standard deviation; H is the log-log slope."""
    x = np.asarray(x, float)
    n = len(x)
    if sizes is None:
        sizes = np.unique(np.floor(np.logspace(np.log10(8), np.log10(n // 2), 12)).astype(int))
    rs = []
    for m in sizes:
        vals = []
        for b in range(n // m):
            y = x[b * m:(b + 1) * m]
            z = np.cumsum(y - y.mean())
            s = y.std()
            if s > 0:
                vals.append((z.max() - z.min()) / s)
        rs.append(np.mean(vals))
    sizes = np.asarray(sizes, float)
    H, c = np.polyfit(np.log(sizes), np.log(rs), 1)
    return {"sizes": sizes, "rs": np.asarray(rs), "H": float(H), "c": float(c)}


def periodogram(x, demean: bool = True) -> dict:
    """I(f_j) = |sum x_t e^{-2 pi i f_j t}|^2 / n at the Fourier frequencies f_j = j/n, 0 < f_j <= 1/2 (cycles per
    observation); an unbiased-but-inconsistent estimate of the spectral density s(f) = sum_h gamma(h) e^{-2 pi i f h}."""
    x = np.asarray(x, float)
    if demean:
        x = x - x.mean()
    n = len(x)
    F = np.fft.rfft(x)
    I = np.abs(F) ** 2 / n
    f = np.arange(len(F)) / n
    return {"f": f[1:], "I": I[1:]}


def welch(x, nseg: int, overlap: float = 0.5) -> dict:
    """Welch's (1967) estimate: average the periodograms of overlapping Hann-tapered segments of length nseg."""
    x = np.asarray(x, float) - np.mean(x)
    step = max(1, int(nseg * (1 - overlap)))
    w = np.hanning(nseg)
    segs = [x[s:s + nseg] for s in range(0, len(x) - nseg + 1, step)]
    P = np.mean([np.abs(np.fft.rfft(w * sg)) ** 2 / np.sum(w * w) for sg in segs], 0)
    f = np.arange(len(P)) / nseg
    return {"f": f[1:], "S": P[1:], "k": len(segs)}


def multitaper(x, NW: float = 4.0, K: int | None = None) -> dict:
    """Thomson's (1982) multitaper estimate: average the periodograms of the series multiplied by K orthogonal
    Slepian (DPSS) tapers with time-bandwidth NW (K = 2NW - 1 by default)."""
    from scipy.signal.windows import dpss

    x = np.asarray(x, float) - np.mean(x)
    n = len(x)
    K = int(2 * NW - 1) if K is None else K
    tapers = dpss(n, NW, K)
    P = np.mean([np.abs(np.fft.rfft(t * x)) ** 2 for t in tapers], 0)
    f = np.arange(len(P)) / n
    return {"f": f[1:], "S": P[1:], "K": K}


def arma_spectrum(f, phi=(), theta=(), sigma2: float = 1.0) -> np.ndarray:
    """The spectral density of an ARMA process: sigma^2 |theta(e^{-2 pi i f})|^2 / |phi(e^{-2 pi i f})|^2."""
    f = np.asarray(f, float)
    z = np.exp(-2j * np.pi * f)
    num = np.abs(1 + sum(t * z ** (k + 1) for k, t in enumerate(theta))) ** 2
    den = np.abs(1 - sum(p * z ** (k + 1) for k, p in enumerate(phi))) ** 2
    return sigma2 * num / den


# MacKinnon (2010), response surfaces tau(T) = b0 + b1/T + b2/T^2 + b3/T^3 for the 1, 5 and 10% critical values.
_MACKINNON = {
    (1, "n"): {0.01: (-2.56574, -2.2358, -3.627, 0.0), 0.05: (-1.94100, -0.2686, -3.365, 31.223),
               0.10: (-1.61682, 0.2656, -2.714, 25.364)},
    (1, "c"): {0.01: (-3.43035, -6.5393, -16.786, -79.433), 0.05: (-2.86154, -2.8903, -4.234, -40.040),
               0.10: (-2.56677, -1.5384, -2.809, 0.0)},
    (1, "ct"): {0.01: (-3.95877, -9.0531, -28.428, -134.155), 0.05: (-3.41049, -4.3904, -9.036, -45.374),
                0.10: (-3.12705, -2.5856, -3.925, -22.380)},
    (2, "c"): {0.01: (-3.89644, -10.9519, -22.527, 0.0), 0.05: (-3.33613, -6.1101, -6.823, 0.0),
               0.10: (-3.04445, -4.2412, -2.720, 0.0)},
}


def df_critical(T: int, level: float = 0.05, trend: str = "c", N: int = 1) -> float:
    """MacKinnon's (2010) finite-sample critical value of the (augmented) Dickey–Fuller t statistic (N = 1), or of the
    Engle–Granger residual test with N = 2 variables."""
    b = _MACKINNON[(N, trend)][level]
    return float(b[0] + b[1] / T + b[2] / T ** 2 + b[3] / T ** 3)


def adf(x, lags: int = 0, trend: str = "c") -> dict:
    """The augmented Dickey–Fuller regression dx_t = [a + b t] + gamma x_{t-1} + sum_j c_j dx_{t-j} + e_t; returns
    gamma's t statistic (compare with ``df_critical``, not the normal), gamma, and the effective sample size."""
    x = np.asarray(x, float)
    dx = np.diff(x)
    n = len(dx)
    rows = range(lags, n)
    y = dx[lags:]
    cols = [x[lags:-1]]
    for j in range(1, lags + 1):
        cols.append(dx[lags - j:n - j])
    if trend in ("c", "ct"):
        cols.append(np.ones(len(y)))
    if trend == "ct":
        cols.append(np.arange(len(y), dtype=float))
    X = np.column_stack(cols)
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    e = y - X @ b
    s2 = e @ e / (len(y) - X.shape[1])
    se = np.sqrt(s2 * np.linalg.inv(X.T @ X)[0, 0])
    return {"t": float(b[0] / se), "gamma": float(b[0]), "T": len(y), "crit5": df_critical(len(y), 0.05, trend)}


def kpss(x, trend: str = "c", lags: int | None = None) -> dict:
    """Kwiatkowski, Phillips, Schmidt & Shin (1992): the null is stationarity.  eta = sum S_t^2 / (T^2 lrv), with S the
    partial sums of the residuals from a constant (or trend) and lrv the Bartlett long-run variance."""
    x = np.asarray(x, float)
    T = len(x)
    t = np.arange(T, dtype=float)
    X = np.ones((T, 1)) if trend == "c" else np.column_stack([np.ones(T), t])
    e = x - X @ np.linalg.lstsq(X, x, rcond=None)[0]
    L = int(np.ceil(12 * (T / 100) ** 0.25)) if lags is None else lags
    g = np.array([e[k:] @ e[:T - k] / T for k in range(L + 1)])
    lrv = g[0] + 2 * sum((1 - k / (L + 1)) * g[k] for k in range(1, L + 1))
    S = np.cumsum(e)
    eta = float(np.sum(S * S) / (T * T * lrv))
    crit = {"c": {0.10: 0.347, 0.05: 0.463, 0.01: 0.739}, "ct": {0.10: 0.119, 0.05: 0.146, 0.01: 0.216}}[trend]
    return {"eta": eta, "crit": crit, "lags": L}


def engle_granger(y, x, lags: int = 0) -> dict:
    """Engle & Granger (1987): regress y on x (with a constant), then test the residuals for a unit root; the critical
    values are MacKinnon's for N = 2, more negative than Dickey–Fuller's because the regression already made the
    residuals look as stationary as possible."""
    y, x = np.asarray(y, float), np.asarray(x, float)
    X = np.column_stack([np.ones(len(y)), x])
    b = np.linalg.lstsq(X, y, rcond=None)[0]
    e = y - X @ b
    a = adf(e, lags, trend="n")
    return {"beta": float(b[1]), "t": a["t"], "crit5": df_critical(a["T"], 0.05, "c", 2), "resid": e}


def johansen_trace(Y, k: int = 1) -> dict:
    """Johansen's (1988) trace statistics for a VAR(k) in levels with a constant in the error-correction model: the
    squared canonical correlations between the differences and the lagged levels, each corrected for the lagged
    differences.  trace_r = -T sum_{i > r} log(1 - lambda_i)."""
    Y = np.asarray(Y, float)
    dY = np.diff(Y, axis=0)
    T = len(dY) - (k - 1)
    Z0 = dY[k - 1:]
    Z1 = Y[k - 1:-1]
    W = [np.ones((T, 1))] + [dY[k - 1 - j:len(dY) - j] for j in range(1, k)]
    W = np.hstack(W)
    R0 = Z0 - W @ np.linalg.lstsq(W, Z0, rcond=None)[0]
    R1 = Z1 - W @ np.linalg.lstsq(W, Z1, rcond=None)[0]
    S00, S11, S01 = R0.T @ R0 / T, R1.T @ R1 / T, R0.T @ R1 / T
    M = np.linalg.solve(S11, S01.T) @ np.linalg.solve(S00, S01)
    lam, vec = np.linalg.eig(M)
    order = np.argsort(-lam.real)
    lam = lam.real[order]
    p = Y.shape[1]
    trace = np.array([-T * np.sum(np.log(1 - lam[r:])) for r in range(p)])
    return {"eig": lam, "trace": trace, "beta": vec.real[:, order]}


def arch_lm(e, q: int = 5) -> dict:
    """Engle's (1982) LM test for ARCH: T R^2 from regressing e_t^2 on q of its lags, chi-square with q df."""
    e2 = np.asarray(e, float) ** 2
    y = e2[q:]
    X = np.column_stack([np.ones(len(y))] + [e2[q - j:len(e2) - j] for j in range(1, q + 1)])
    b = np.linalg.lstsq(X, y, rcond=None)[0]
    r = y - X @ b
    R2 = 1 - r @ r / np.sum((y - y.mean()) ** 2)
    LM = len(y) * R2
    return {"LM": float(LM), "p": float(stats.chi2.sf(LM, q))}


def garch_filter(r, omega: float, alpha: float, beta: float, mu: float = 0.0) -> np.ndarray:
    """The GARCH(1,1) conditional variances sigma_t^2 = omega + alpha e_{t-1}^2 + beta sigma_{t-1}^2, started at the
    sample variance."""
    e = np.asarray(r, float) - mu
    s2 = np.empty(len(e))
    s2[0] = e.var()
    for t in range(1, len(e)):
        s2[t] = omega + alpha * e[t - 1] ** 2 + beta * s2[t - 1]
    return s2


def garch11_fit(r) -> dict:
    """Bollerslev's (1986) GARCH(1,1) with a constant mean, by Gaussian maximum likelihood (Nelder–Mead on transformed
    parameters, so that omega > 0, alpha, beta > 0 and alpha + beta < 1)."""
    r = np.asarray(r, float)

    def unpack(th):
        mu, lw, a, b = th
        ea, eb = np.exp(a), np.exp(b)
        s = 1 + ea + eb
        return mu, np.exp(lw), ea / s, eb / s

    def nll(th):
        mu, w, a, b = unpack(th)
        s2 = garch_filter(r, w, a, b, mu)
        return 0.5 * np.sum(np.log(2 * np.pi * s2) + (r - mu) ** 2 / s2)

    v = r.var()
    best = None
    for a0, b0 in ((0.05, 0.9), (0.1, 0.8), (0.03, 0.95)):
        th0 = [r.mean(), np.log(v * (1 - a0 - b0)), np.log(a0 / (1 - a0 - b0)), np.log(b0 / (1 - a0 - b0))]
        o = optimize.minimize(nll, th0, method="Nelder-Mead", options={"maxiter": 8000, "xatol": 1e-8, "fatol": 1e-8})
        if best is None or o.fun < best.fun:
            best = o
    mu, w, a, b = unpack(best.x)
    return {"mu": float(mu), "omega": float(w), "alpha": float(a), "beta": float(b), "loglik": float(-best.fun),
            "s2": garch_filter(r, w, a, b, mu), "persistence": float(a + b),
            "half_life": float(np.log(0.5) / np.log(a + b))}


def frac_diff_weights(d: float, n: int) -> np.ndarray:
    """The weights pi_k of (1 - B)^d = sum_k pi_k B^k: pi_0 = 1, pi_k = pi_{k-1} (k - 1 - d)/k."""
    w = np.empty(n)
    w[0] = 1.0
    for k in range(1, n):
        w[k] = w[k - 1] * (k - 1 - d) / k
    return w


def arfima_acf(d: float, nlags: int) -> np.ndarray:
    """The ACF of ARFIMA(0, d, 0): rho_k = prod_{j=1}^k (j - 1 + d)/(j - d), decaying like k^{2d - 1}."""
    r = np.empty(nlags + 1)
    r[0] = 1.0
    for k in range(1, nlags + 1):
        r[k] = r[k - 1] * (k - 1 + d) / (k - d)
    return r


def simulate_arfima(d: float, n: int, rng: np.random.Generator, sigma: float = 1.0) -> np.ndarray:
    """Exact simulation of a Gaussian ARFIMA(0, d, 0) by circulant embedding (Davies & Harte 1987) of its
    autocovariances gamma_0 = sigma^2 Gamma(1 - 2d)/Gamma(1 - d)^2, gamma_k = gamma_0 rho_k."""
    g0 = sigma ** 2 * special.gamma(1 - 2 * d) / special.gamma(1 - d) ** 2
    g = g0 * arfima_acf(d, n)
    c = np.concatenate([g, g[-2:0:-1]])
    lam = np.fft.fft(c).real
    lam = np.clip(lam, 0, None)
    m = len(c)
    z = rng.standard_normal(m) + 1j * rng.standard_normal(m)
    y = np.fft.fft(np.sqrt(lam / m) * z)
    return y.real[:n]


def gph(x, power: float = 0.5) -> dict:
    """Geweke & Porter-Hudak (1983): regress log I(f_j) on -log(4 sin^2(pi f_j)) over the m = n^power lowest Fourier
    frequencies; the slope estimates d (H = d + 1/2), with SE pi/sqrt(24 m)."""
    p = periodogram(x)
    n = len(x)
    m = int(np.floor(n ** power))
    f, I = p["f"][:m], p["I"][:m]
    X = -np.log(4 * np.sin(np.pi * f) ** 2)
    d, c = np.polyfit(X, np.log(I), 1)
    return {"d": float(d), "se": float(np.pi / np.sqrt(24 * m)), "m": m}


def local_whittle(x, power: float = 0.65) -> dict:
    """Robinson's (1995) local Whittle estimate of d: minimize log(mean_j lambda_j^{2d} I_j) - 2d mean_j log lambda_j
    over the m = n^power lowest frequencies; SE 1/(2 sqrt m)."""
    p = periodogram(x)
    m = int(np.floor(len(x) ** power))
    lam, I = 2 * np.pi * p["f"][:m], p["I"][:m]
    R = lambda d: np.log(np.mean(lam ** (2 * d) * I)) - 2 * d * np.mean(np.log(lam))
    o = optimize.minimize_scalar(R, bounds=(-0.49, 0.99), method="bounded")
    return {"d": float(o.x), "se": float(1 / (2 * np.sqrt(m))), "m": m}


def kalman(y, F, H, Q, R, m0, P0) -> dict:
    """The Kalman (1960) filter for x_t = F x_{t-1} + w_t (w ~ N(0, Q)), y_t = H x_t + v_t (v ~ N(0, R)); y may contain
    NaN (missing: predict only).  Returns the predicted and filtered means and covariances, the innovations, their
    variances and the Gaussian log-likelihood of the prediction errors."""
    y = np.asarray(y, float)
    if y.ndim == 1:
        y = y[:, None]
    F, H, Q, R = (np.atleast_2d(np.asarray(a, float)) for a in (F, H, Q, R))
    n, k = len(y), F.shape[0]
    m, P = np.asarray(m0, float).reshape(k), np.atleast_2d(np.asarray(P0, float))
    mp, Pp, mf, Pf = np.zeros((n, k)), np.zeros((n, k, k)), np.zeros((n, k)), np.zeros((n, k, k))
    v, S = np.full((n, y.shape[1]), np.nan), np.zeros((n, y.shape[1], y.shape[1]))
    ll = 0.0
    for t in range(n):
        m = F @ m
        P = F @ P @ F.T + Q
        mp[t], Pp[t] = m, P
        ok = ~np.isnan(y[t])
        if ok.any():
            Ht = H[ok]
            St = Ht @ P @ Ht.T + R[np.ix_(ok, ok)]
            vt = y[t, ok] - Ht @ m
            K = P @ Ht.T @ np.linalg.inv(St)
            m = m + K @ vt
            P = (np.eye(k) - K @ Ht) @ P
            v[t, ok] = vt
            S[t][np.ix_(ok, ok)] = St
            ll += -0.5 * (ok.sum() * np.log(2 * np.pi) + np.log(np.linalg.det(St)) + vt @ np.linalg.solve(St, vt))
        mf[t], Pf[t] = m, P
    return {"mp": mp, "Pp": Pp, "mf": mf, "Pf": Pf, "v": v, "S": S, "loglik": float(ll), "F": F}


def rts(kf: dict) -> dict:
    """The Rauch–Tung–Striebel (1965) smoother: backward passes m_t^s = m_t + J_t (m_{t+1}^s - m_{t+1|t}),
    J_t = P_t F' P_{t+1|t}^{-1}; also returns the lag-one smoothed cross-covariances needed by EM."""
    mf, Pf, mp, Pp, F = kf["mf"], kf["Pf"], kf["mp"], kf["Pp"], kf["F"]
    n, k = mf.shape
    ms, Ps = mf.copy(), Pf.copy()
    J = np.zeros((n, k, k))
    for t in range(n - 2, -1, -1):
        J[t] = Pf[t] @ F.T @ np.linalg.inv(Pp[t + 1])
        ms[t] = mf[t] + J[t] @ (ms[t + 1] - mp[t + 1])
        Ps[t] = Pf[t] + J[t] @ (Ps[t + 1] - Pp[t + 1]) @ J[t].T
    cross = np.array([Ps[t + 1] @ J[t].T for t in range(n - 1)])  # Cov(x_{t+1}, x_t | all)
    return {"ms": ms, "Ps": Ps, "cross": cross}


def local_level_mle(y, a1: float | None = None) -> dict:
    """The local-level model x_t = x_{t-1} + w_t, y_t = x_t + v_t, by maximizing the prediction-error likelihood over
    the two log-variances (a diffuse-ish start: x_0 ~ N(y_1, 10^7))."""
    y = np.asarray(y, float)
    m0 = y[~np.isnan(y)][0] if a1 is None else a1

    def nll(th):
        q, r = np.exp(th)
        return -kalman(y, [[1.0]], [[1.0]], [[q]], [[r]], [m0], [[1e7]])["loglik"]

    v = np.nanvar(np.diff(y))
    o = optimize.minimize(nll, [np.log(v / 4), np.log(v / 2)], method="Nelder-Mead", options={"xatol": 1e-8, "fatol": 1e-8})
    q, r = np.exp(o.x)
    kf = kalman(y, [[1.0]], [[1.0]], [[q]], [[r]], [m0], [[1e7]])
    return {"q": float(q), "r": float(r), "loglik": float(-o.fun), "kf": kf, "sm": rts(kf)}


def local_level_em(y, q0: float, r0: float, iters: int = 200) -> dict:
    """Shumway & Stoffer's (1982) EM for the local-level variances: E-step by the RTS smoother, M-step in closed form;
    returns the path of (q, r, loglik), which never decreases."""
    y = np.asarray(y, float)
    q, r = q0, r0
    m0 = y[0]
    path = []
    for _ in range(iters):
        kf = kalman(y, [[1.0]], [[1.0]], [[q]], [[r]], [m0], [[1e7]])
        sm = rts(kf)
        ms, Ps, C = sm["ms"][:, 0], sm["Ps"][:, 0, 0], sm["cross"][:, 0, 0]
        path.append((q, r, kf["loglik"]))
        n = len(y)
        r = float(np.mean((y - ms) ** 2 + Ps))
        q = float(np.mean((ms[1:] - ms[:-1]) ** 2 + Ps[1:] + Ps[:-1] - 2 * C))
    return {"q": q, "r": r, "path": np.array(path)}


def ekf(y, f, fjac, h, hjac, Q: float, R: float, m0: float, P0: float) -> dict:
    """The extended Kalman filter for a scalar state: linearize f and h at the current mean. ``f(x, t)``, ``h(x)``."""
    m, P = m0, P0
    mf, Pf = [], []
    for t, yt in enumerate(y):
        Fm = fjac(m, t)
        m = f(m, t)
        P = Fm * P * Fm + Q
        Hm = hjac(m)
        S = Hm * P * Hm + R
        K = P * Hm / S
        m = m + K * (yt - h(m))
        P = (1 - K * Hm) * P
        mf.append(m), Pf.append(P)
    return {"m": np.array(mf), "P": np.array(Pf)}


def ukf(y, f, h, Q: float, R: float, m0: float, P0: float, kappa: float = 2.0) -> dict:
    """The unscented Kalman filter (Julier & Uhlmann 1997) for a scalar state: propagate the 2n + 1 = 3 sigma points
    m, m +- sqrt((1 + kappa) P) through f and h instead of linearizing."""
    m, P = m0, P0
    w = np.array([kappa, 0.5, 0.5]) / (1 + kappa)
    mf, Pf = [], []
    for t, yt in enumerate(y):
        s = np.sqrt((1 + kappa) * P)
        X = np.array([m, m + s, m - s])
        Xf = np.array([f(xx, t) for xx in X])
        m = w @ Xf
        P = w @ (Xf - m) ** 2 + Q
        s = np.sqrt((1 + kappa) * P)
        X = np.array([m, m + s, m - s])
        Yh = np.array([h(xx) for xx in X])
        yh = w @ Yh
        S = w @ (Yh - yh) ** 2 + R
        C = w @ ((X - m) * (Yh - yh))
        K = C / S
        m = m + K * (yt - yh)
        P = P - K * S * K
        mf.append(m), Pf.append(P)
    return {"m": np.array(mf), "P": np.array(Pf)}


def bootstrap_pf(y, f, h, Q: float, R: float, m0: float, P0: float, n: int, rng: np.random.Generator) -> dict:
    """Gordon, Salmond & Smith's (1993) bootstrap particle filter for a scalar state with Gaussian noise: propagate
    particles through f, weight by the likelihood of y_t, resample systematically."""
    x = m0 + np.sqrt(P0) * rng.standard_normal(n)
    mean, q05, q95, ess = [], [], [], []
    for t, yt in enumerate(y):
        x = f(x, t) + np.sqrt(Q) * rng.standard_normal(n)
        lw = -0.5 * (yt - h(x)) ** 2 / R
        w = np.exp(lw - lw.max())
        w /= w.sum()
        mean.append(w @ x)
        ess.append(1 / np.sum(w * w))
        o = np.argsort(x)
        cw = np.cumsum(w[o])
        q05.append(x[o][np.searchsorted(cw, 0.05)]), q95.append(x[o][min(np.searchsorted(cw, 0.95), n - 1)])
        u = (rng.random() + np.arange(n)) / n
        x = x[np.minimum(np.searchsorted(np.cumsum(w), u), n - 1)]
    return {"m": np.array(mean), "lo": np.array(q05), "hi": np.array(q95), "ess": np.array(ess)}


def hamilton_filter(y, mu, sigma: float, P, phi: float = 0.0) -> dict:
    """Hamilton's (1989) filter for a two-state Markov-switching mean y_t = mu_{s_t} + phi (y_{t-1} - mu_{s_{t-1}})
    + sigma e_t with transition matrix P[i, j] = P(s_t = j | s_{t-1} = i): filtered state probabilities and the
    log-likelihood (phi = 0 for a switching mean with white noise)."""
    y = np.asarray(y, float)
    mu, P = np.asarray(mu, float), np.asarray(P, float)
    pi = np.array([P[1, 0], P[0, 1]]) / (P[0, 1] + P[1, 0])  # the stationary distribution
    xi = pi.copy()
    filt, ll = [], 0.0
    for t in range(len(y)):
        pred = xi @ P
        prev = y[t - 1] if t > 0 else y[0]
        dens = np.array([stats.norm.pdf(y[t], mu[j] + phi * (prev - mu[j]), sigma) for j in range(2)])
        joint = pred * dens
        lik = joint.sum()
        ll += np.log(lik)
        xi = joint / lik
        filt.append(xi.copy())
    return {"p": np.array(filt), "loglik": float(ll)}


def hamilton_fit(y) -> dict:
    """Maximum likelihood for the two-state switching mean (state 0: low mean), by Nelder–Mead."""
    y = np.asarray(y, float)

    def unpack(th):
        m0, m1, ls, a, b = th
        return np.array([m0, m1]), np.exp(ls), np.array([[1 / (1 + np.exp(-a)), 1 - 1 / (1 + np.exp(-a))],
                                                        [1 - 1 / (1 + np.exp(-b)), 1 / (1 + np.exp(-b))]])

    def nll(th):
        mu, s, P = unpack(th)
        return -hamilton_filter(y, mu, s, P)["loglik"]

    th0 = [np.percentile(y, 10), np.percentile(y, 60), np.log(y.std() * 0.7), 1.0, 3.0]
    o = optimize.minimize(nll, th0, method="Nelder-Mead", options={"maxiter": 6000, "xatol": 1e-8, "fatol": 1e-9})
    mu, s, P = unpack(o.x)
    if mu[0] > mu[1]:
        mu, P = mu[::-1], P[::-1, ::-1]
    f = hamilton_filter(y, mu, s, P)
    return {"mu": mu, "sigma": float(s), "P": P, "p_low": f["p"][:, 0], "loglik": f["loglik"],
            "duration_low": float(1 / (1 - P[0, 0])), "duration_high": float(1 / (1 - P[1, 1]))}


def var_fit(Y, p: int) -> dict:
    """A VAR(p) with a constant by equation-by-equation least squares: Y_t = c + A_1 Y_{t-1} + ... + A_p Y_{t-p} + u_t."""
    Y = np.asarray(Y, float)
    T, k = Y.shape
    X = np.hstack([np.ones((T - p, 1))] + [Y[p - j:T - j] for j in range(1, p + 1)])
    Yt = Y[p:]
    B = np.linalg.lstsq(X, Yt, rcond=None)[0]
    U = Yt - X @ B
    Sigma = U.T @ U / (T - p - X.shape[1])
    A = [B[1 + (j - 1) * k:1 + j * k].T for j in range(1, p + 1)]
    return {"c": B[0], "A": A, "Sigma": Sigma, "U": U, "X": X, "B": B, "p": p}


def granger_test(Y, p: int, cause: int, effect: int) -> dict:
    """Granger (1969) causality in a VAR(p): the F test that the p lags of variable ``cause`` have zero coefficients in
    the equation of ``effect``."""
    Y = np.asarray(Y, float)
    T, k = Y.shape
    full = var_fit(Y, p)
    X = full["X"]
    y = Y[p:, effect]
    drop = [1 + (j - 1) * k + cause for j in range(1, p + 1)]
    keep = [i for i in range(X.shape[1]) if i not in drop]
    rss = lambda Z: np.sum((y - Z @ np.linalg.lstsq(Z, y, rcond=None)[0]) ** 2)
    r1, r0 = rss(X), rss(X[:, keep])
    df2 = len(y) - X.shape[1]
    F = ((r0 - r1) / p) / (r1 / df2)
    return {"F": float(F), "p": float(stats.f.sf(F, p, df2))}


def irf(fit: dict, h: int, orth: bool = True) -> np.ndarray:
    """Impulse responses Psi_s (h + 1, k, k): the MA weights of the VAR, times the Cholesky factor of Sigma when
    ``orth`` (Sims 1980: the ordering matters)."""
    A, k = fit["A"], fit["Sigma"].shape[0]
    p = len(A)
    Psi = [np.eye(k)]
    for s in range(1, h + 1):
        Psi.append(sum(A[j - 1] @ Psi[s - j] for j in range(1, min(p, s) + 1)))
    Psi = np.array(Psi)
    if orth:
        Psi = Psi @ np.linalg.cholesky(fit["Sigma"])
    return Psi


def stationary_bootstrap_means(x, mean_block: float, B: int, rng: np.random.Generator) -> np.ndarray:
    """Politis & Romano's (1994) stationary bootstrap: blocks of geometric length (mean ``mean_block``) from random
    starts, wrapping around the end; the resampled series are stationary.  Vectorized over the B replicates."""
    x = np.asarray(x, float)
    n = len(x)
    new = rng.random((B, n)) < 1 / mean_block
    new[:, 0] = True
    starts = rng.integers(0, n, (B, n))
    t = np.arange(n)[None, :].repeat(B, 0)
    last = np.maximum.accumulate(np.where(new, t, 0), axis=1)
    s0 = np.take_along_axis(starts, last, axis=1)
    idx = (s0 + t - last) % n
    return x[idx].mean(1)
