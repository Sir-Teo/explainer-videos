"""Price paths for the House: geometric Brownian motion (exact) and Heston (Andersen's quadratic-exponential
scheme), seeded and vectorized over paths.

    t, S = gbm(S0=100, mu=0.0, sigma=0.2, T=1.0, n_steps=252, n_paths=10_000, seed=7)
    t, S, v = heston(S0=100, v0=0.04, kappa=2.0, theta=0.04, xi=0.6, rho=-0.7, T=1.0, n_steps=252,
                     n_paths=10_000, seed=7)

Arrays are (n_paths, n_steps + 1); ``t`` is (n_steps + 1,).
"""

from __future__ import annotations

import numpy as np


def rng_of(seed) -> np.random.Generator:
    return seed if isinstance(seed, np.random.Generator) else np.random.default_rng(seed)


def gbm(S0, mu, sigma, T, n_steps, n_paths, seed=0, antithetic=False):
    """Exact GBM: S_{t+dt} = S_t exp((mu - sigma^2/2) dt + sigma sqrt(dt) Z)."""
    rng = rng_of(seed)
    dt = T / n_steps
    if antithetic:
        half = rng.standard_normal(((n_paths + 1) // 2, n_steps))
        Z = np.concatenate([half, -half])[:n_paths]
    else:
        Z = rng.standard_normal((n_paths, n_steps))
    incr = (mu - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * Z
    logS = np.concatenate([np.zeros((n_paths, 1)), np.cumsum(incr, axis=1)], axis=1)
    return np.linspace(0.0, T, n_steps + 1), S0 * np.exp(logS)


def heston(S0, v0, kappa, theta, xi, rho, T, n_steps, n_paths, seed=0, mu=0.0, psi_c=1.5):
    """Heston (1993) by Andersen's (2008) QE scheme for the variance and the matching log-price step
    (gamma1 = gamma2 = 1/2).  dS/S = mu dt + sqrt(v) dW, dv = kappa (theta - v) dt + xi sqrt(v) dB, d<W,B> = rho dt.
    Returns t, S and v."""
    rng = rng_of(seed)
    dt = T / n_steps
    e = np.exp(-kappa * dt)
    g1 = g2 = 0.5
    K0 = -rho * kappa * theta / xi * dt
    K1 = g1 * dt * (kappa * rho / xi - 0.5) - rho / xi
    K2 = g2 * dt * (kappa * rho / xi - 0.5) + rho / xi
    K3 = g1 * dt * (1 - rho ** 2)
    K4 = g2 * dt * (1 - rho ** 2)
    v = np.full(n_paths, float(v0))
    x = np.full(n_paths, np.log(S0))
    V = np.empty((n_paths, n_steps + 1))
    X = np.empty((n_paths, n_steps + 1))
    V[:, 0], X[:, 0] = v, x
    for i in range(n_steps):
        m = theta + (v - theta) * e
        s2 = v * xi ** 2 * e / kappa * (1 - e) + theta * xi ** 2 / (2 * kappa) * (1 - e) ** 2
        psi = s2 / np.maximum(m * m, 1e-300)
        U = rng.random(n_paths)
        Zv = rng.standard_normal(n_paths)
        quad = psi <= psi_c
        # quadratic branch: v' = a (b + Z)^2
        with np.errstate(divide="ignore", invalid="ignore"):
            b2 = np.where(quad, 2 / psi - 1 + np.sqrt(2 / psi) * np.sqrt(np.maximum(2 / psi - 1, 0.0)), 0.0)
            a = np.where(quad, m / (1 + b2), 0.0)
            v_quad = a * (np.sqrt(b2) + Zv) ** 2
            # exponential branch: a point mass at zero plus an exponential tail
            p = np.where(~quad, (psi - 1) / (psi + 1), 0.0)
            beta = np.where(~quad, (1 - p) / m, 1.0)
            v_exp = np.where(U <= p, 0.0, np.log((1 - p) / np.maximum(1 - U, 1e-300)) / beta)
        v_new = np.where(quad, v_quad, v_exp)
        Zx = rng.standard_normal(n_paths)
        x = x + mu * dt + K0 + K1 * v + K2 * v_new + np.sqrt(np.maximum(K3 * v + K4 * v_new, 0.0)) * Zx
        v = v_new
        V[:, i + 1], X[:, i + 1] = v, x
    return np.linspace(0.0, T, n_steps + 1), np.exp(X), V


def realized_vol(S, dt, axis=-1):
    """Annualized realized volatility of log returns (no mean subtracted: the hedger's, not the statistician's)."""
    r = np.diff(np.log(S), axis=axis)
    return np.sqrt(np.sum(r * r, axis=axis) / (r.shape[axis] * dt))
