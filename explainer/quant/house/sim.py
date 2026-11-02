"""The House's simulation library (Part 5, *Stochastic Calculus*), used by every pricing part.

* :func:`brownian`: increments and paths of Brownian motion, shared by the schemes so errors can be compared path by
  path;
* :func:`euler_maruyama`, :func:`milstein`: the two basic schemes for dX = a(t, X) dt + b(t, X) dW;
* :func:`scheme_orders`: strong and weak errors against GBM's exact solution, and their slopes;
* :func:`ou_exact`, :func:`cir_exact`: exact transitions of Ornstein–Uhlenbeck (Gaussian) and Cox–Ingersoll–Ross
  (scaled non-central chi-square);
* :func:`merton_jumps`: a jump-diffusion (Merton 1976) on a grid;
* :func:`hawkes_thinning`, :func:`hawkes_fit`: a self-exciting point process (Hawkes 1971) by Ogata's thinning
  (1981), and its exponential-kernel maximum likelihood;
* :func:`fbm`: fractional Brownian motion by the Davies–Harte circulant embedding;
* :func:`hurst_from_increments`: the Hurst exponent from the scaling of q-th moments of increments (Gatheral, Jaisson
  and Rosenbaum 2018);
* :func:`signature2`: a path's signature to level 2 (Chen 1957; Lyons 1998), with the Lévy area.
"""

from __future__ import annotations

import numpy as np
from scipy import optimize


def brownian(T: float, n: int, n_paths: int, seed=0) -> tuple[np.ndarray, np.ndarray]:
    """Increments dW (n_paths x n) and paths W (n_paths x (n + 1), W_0 = 0) on a uniform grid of [0, T]."""
    rng = np.random.default_rng(seed)
    dW = rng.standard_normal((n_paths, n)) * np.sqrt(T / n)
    W = np.concatenate([np.zeros((n_paths, 1)), np.cumsum(dW, axis=1)], axis=1)
    return dW, W


def euler_maruyama(a, b, x0, T: float, dW: np.ndarray) -> np.ndarray:
    """X_{k+1} = X_k + a(t_k, X_k) dt + b(t_k, X_k) dW_k.  ``a``, ``b`` take (t, x arrays)."""
    n_paths, n = dW.shape
    dt = T / n
    X = np.empty((n_paths, n + 1))
    X[:, 0] = x0
    for k in range(n):
        t = k * dt
        X[:, k + 1] = X[:, k] + a(t, X[:, k]) * dt + b(t, X[:, k]) * dW[:, k]
    return X


def milstein(a, b, db, x0, T: float, dW: np.ndarray) -> np.ndarray:
    """Euler plus the Itô correction 1/2 b b' (dW^2 - dt); ``db`` is d b / dx."""
    n_paths, n = dW.shape
    dt = T / n
    X = np.empty((n_paths, n + 1))
    X[:, 0] = x0
    for k in range(n):
        t, x = k * dt, X[:, k]
        X[:, k + 1] = x + a(t, x) * dt + b(t, x) * dW[:, k] + 0.5 * b(t, x) * db(t, x) * (dW[:, k] ** 2 - dt)
    return X


def scheme_orders(mu=0.05, sigma=0.4, S0=1.0, T=1.0, ns=(8, 16, 32, 64, 128, 256), n_paths=20000, seed=0) -> dict:
    """Strong error E|X_T - S_T| and weak error |E X_T - E S_T| of Euler and Milstein on GBM, against the exact
    solution driven by the same Brownian path, for each number of steps.  Returns the errors and log-log slopes."""
    nmax = max(ns)
    dW_f, W_f = brownian(T, nmax, n_paths, seed)
    exact = S0 * np.exp((mu - 0.5 * sigma ** 2) * T + sigma * W_f[:, -1])
    a = lambda t, x: mu * x  # noqa: E731
    b = lambda t, x: sigma * x  # noqa: E731
    db = lambda t, x: sigma + 0 * x  # noqa: E731
    out = {"n": list(ns), "dt": [T / n for n in ns], "strong_euler": [], "strong_milstein": [], "weak_euler": [],
           "weak_milstein": []}
    for n in ns:
        dW = dW_f.reshape(n_paths, n, nmax // n).sum(axis=2)
        Xe = euler_maruyama(a, b, S0, T, dW)[:, -1]
        Xm = milstein(a, b, db, S0, T, dW)[:, -1]
        out["strong_euler"].append(float(np.mean(np.abs(Xe - exact))))
        out["strong_milstein"].append(float(np.mean(np.abs(Xm - exact))))
        true_mean = S0 * np.exp(mu * T)
        out["weak_euler"].append(float(abs(Xe.mean() - true_mean)))
        out["weak_milstein"].append(float(abs(Xm.mean() - true_mean)))
    ldt = np.log(out["dt"])
    for k in ("strong_euler", "strong_milstein", "weak_euler", "weak_milstein"):
        out["slope_" + k] = float(np.polyfit(ldt, np.log(out[k]), 1)[0])
    return out


def ou_exact(x0, kappa, theta, sigma, T, n, n_paths, seed=0) -> np.ndarray:
    """dX = kappa (theta - X) dt + sigma dW, sampled exactly on a grid."""
    rng = np.random.default_rng(seed)
    dt = T / n
    e = np.exp(-kappa * dt)
    sd = sigma * np.sqrt((1 - e ** 2) / (2 * kappa))
    X = np.empty((n_paths, n + 1))
    X[:, 0] = x0
    for k in range(n):
        X[:, k + 1] = theta + (X[:, k] - theta) * e + sd * rng.standard_normal(n_paths)
    return X


def cir_exact(x0, kappa, theta, sigma, T, n, n_paths, seed=0) -> np.ndarray:
    """dX = kappa (theta - X) dt + sigma sqrt(X) dW, sampled exactly: X_{t+dt} = c * noncentral chi-square(d, lambda)."""
    rng = np.random.default_rng(seed)
    dt = T / n
    c = sigma ** 2 * (1 - np.exp(-kappa * dt)) / (4 * kappa)
    d = 4 * kappa * theta / sigma ** 2
    X = np.empty((n_paths, n + 1))
    X[:, 0] = x0
    for k in range(n):
        lam = X[:, k] * np.exp(-kappa * dt) / c
        X[:, k + 1] = c * rng.noncentral_chisquare(d, lam)
    return X


def merton_jumps(S0, mu, sigma, lam, mj, sj, T, n, n_paths, seed=0) -> np.ndarray:
    """Merton's jump-diffusion: GBM plus Poisson(lam) jumps whose log sizes are N(mj, sj^2); drift compensated so that
    E[S_T] = S0 e^{mu T}."""
    rng = np.random.default_rng(seed)
    dt = T / n
    kbar = np.exp(mj + 0.5 * sj ** 2) - 1
    z = rng.standard_normal((n_paths, n))
    N = rng.poisson(lam * dt, (n_paths, n))
    J = mj * N + sj * np.sqrt(N) * rng.standard_normal((n_paths, n))
    dlog = (mu - lam * kbar - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * z + J
    return S0 * np.exp(np.concatenate([np.zeros((n_paths, 1)), np.cumsum(dlog, axis=1)], axis=1))


def hawkes_thinning(mu: float, alpha: float, beta: float, T: float, seed=0) -> np.ndarray:
    """Event times of a Hawkes process with intensity mu + sum alpha e^{-beta (t - t_i)} on [0, T], by Ogata's thinning.
    The branching ratio alpha / beta must be below one for stationarity."""
    rng = np.random.default_rng(seed)
    t, events, excite = 0.0, [], 0.0  # excite = sum alpha e^{-beta (t - t_i)} at time t
    while True:
        lam_bar = mu + excite
        w = rng.exponential(1 / lam_bar)
        t_new = t + w
        if t_new > T:
            break
        excite *= np.exp(-beta * w)
        t = t_new
        if rng.random() <= (mu + excite) / lam_bar:
            events.append(t)
            excite += alpha
    return np.array(events)


def hawkes_intensity(events, mu, alpha, beta, grid) -> np.ndarray:
    ev = np.asarray(events)
    out = np.full(len(grid), mu, float)
    for i, g in enumerate(grid):
        past = ev[ev < g]
        out[i] += alpha * np.exp(-beta * (g - past)).sum()
    return out


def hawkes_loglik(params, events, T) -> float:
    mu, alpha, beta = params
    if mu <= 0 or alpha < 0 or beta <= 0:
        return -np.inf
    ev = np.asarray(events)
    A = np.zeros(len(ev))
    for i in range(1, len(ev)):
        A[i] = np.exp(-beta * (ev[i] - ev[i - 1])) * (1 + A[i - 1])
    ll = np.sum(np.log(mu + alpha * A)) - mu * T - (alpha / beta) * np.sum(1 - np.exp(-beta * (T - ev)))
    return float(ll)


def hawkes_fit(events, T, x0=None) -> dict:
    """Maximum likelihood for an exponential-kernel Hawkes process (Ozaki 1979's recursion).  Returns mu, alpha, beta,
    the branching ratio alpha / beta and the log-likelihood (and that of a Poisson process, for comparison)."""
    ev = np.asarray(events, float)
    n = len(ev)
    x0 = x0 or [n / T * 0.5, 1.0, 2.0]
    res = optimize.minimize(lambda p: -hawkes_loglik(np.exp(p), ev, T), np.log(x0), method="Nelder-Mead",
                            options={"maxiter": 4000, "xatol": 1e-6, "fatol": 1e-8})
    mu, alpha, beta = np.exp(res.x)
    ll_pois = n * np.log(n / T) - n
    return {"mu": float(mu), "alpha": float(alpha), "beta": float(beta), "branching": float(alpha / beta),
            "loglik": float(-res.fun), "loglik_poisson": float(ll_pois), "n": int(n)}


def fbm(H: float, n: int, T: float = 1.0, n_paths: int = 1, seed=0) -> np.ndarray:
    """Fractional Brownian motion on n steps of [0, T] by Davies–Harte (exact for any 0 < H < 1)."""
    rng = np.random.default_rng(seed)
    k = np.arange(n + 1)
    gamma = 0.5 * (np.abs(k - 1) ** (2 * H) - 2 * np.abs(k) ** (2 * H) + np.abs(k + 1) ** (2 * H))
    row = np.concatenate([gamma, gamma[-2:0:-1]])
    lam = np.fft.fft(row).real
    lam = np.clip(lam, 0, None)
    m = len(row)
    out = np.empty((n_paths, n + 1))
    for p in range(n_paths):
        z = rng.standard_normal(m) + 1j * rng.standard_normal(m)
        y = np.fft.fft(np.sqrt(lam / m) * z)[:n].real
        out[p] = np.concatenate([[0.0], np.cumsum(y)]) * (T / n) ** H
    return out


def hurst_from_increments(x, lags=(1, 2, 3, 4, 5, 7, 10, 15, 20, 30, 50), qs=(0.5, 1.0, 1.5, 2.0, 3.0)) -> dict:
    """Gatheral, Jaisson and Rosenbaum (2018): m(q, lag) = mean |x_{t+lag} - x_t|^q ~ lag^{zeta_q}; for a fractional
    Brownian motion zeta_q = q H.  Returns zeta_q, the H estimates zeta_q / q, and their mean."""
    x = np.asarray(x, float)
    lags = np.asarray(lags)
    zeta = []
    for q in qs:
        m = [np.mean(np.abs(x[l:] - x[:-l]) ** q) for l in lags]
        zeta.append(float(np.polyfit(np.log(lags), np.log(m), 1)[0]))
    hs = [z / q for z, q in zip(zeta, qs)]
    return {"qs": list(qs), "zeta": zeta, "H_each": hs, "H": float(np.mean(hs))}


def signature2(path) -> dict:
    """The signature of a piecewise-linear path in R^d to level 2: S1 (the increments, d) and S2 (d x d, iterated
    integrals int dX^i dX^j), with the Lévy area (S2 - S2^T)/2.  Exact for piecewise-linear paths (Chen's identity
    applied segment by segment)."""
    X = np.asarray(path, float)
    d = X.shape[1]
    S1 = np.zeros(d)
    S2 = np.zeros((d, d))
    for k in range(1, len(X)):
        dx = X[k] - X[k - 1]
        # Chen: S(a * b) = S(a) (x) S(b); a straight segment has S1 = dx, S2 = dx dx^T / 2
        S2 = S2 + np.outer(S1, dx) + np.outer(dx, dx) / 2
        S1 = S1 + dx
    return {"S1": S1, "S2": S2, "levy_area": (S2 - S2.T) / 2}
