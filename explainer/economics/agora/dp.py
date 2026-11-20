"""Agora's dynamic programming (Part 29): the cake-eating problem by value function iteration, the contraction's
convergence, policy iteration, discretized AR(1) processes (Tauchen; Rouwenhorst), and the trend filters used to
define a business cycle (Hodrick-Prescott; Hamilton's regression filter).  numpy and scipy only."""

from __future__ import annotations

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve
from scipy.stats import norm


# --- the cake ------------------------------------------------------------------------------------------------------
def cake(beta: float = 0.9, w_max: float = 1.0, n: int = 301, iters: int = 200, keep: tuple = (0, 1, 2, 5, 10, 30),
         tol: float = 1e-10) -> dict:
    """Eat a cake of size ``w`` over infinitely many days, ``V(w) = max_{c <= w} log c + beta V(w - c)``, by value
    function iteration on a grid, starting from ``V = 0``.  Returns the grid, the iterates kept, the converged value and
    policy, the sup-norm distance between successive iterates (which falls at rate ``beta``), and the closed form
    ``c = (1 - beta) w``."""
    w = np.linspace(w_max / n, w_max, n)
    V = np.zeros(n)
    kept, gaps = {}, []
    # consumption c = w_i - w_j for next-period cake w_j < w_i; some cake is always kept (with log utility, a day
    # with nothing to eat is worth minus infinity), so the smallest cake on the grid can only be carried, not eaten
    C = w[:, None] - w[None, :]
    U = np.where(C > 0, np.log(np.maximum(C, 1e-300)), -1e10)
    U[0, 0] = np.log(w[0])
    pol = np.zeros(n, int)
    for it in range(iters):
        if it in keep:
            kept[str(it)] = V.tolist()
        cand = U + beta * V[None, :]
        Vn = cand.max(axis=1)
        pol = cand.argmax(axis=1)
        gap = float(np.max(np.abs(Vn - V)))
        gaps.append(gap)
        V = Vn
        if gap < tol:
            break
    nxt = w[pol]
    c = np.where(np.arange(n) == 0, w[0], w - nxt)
    exact_V = np.log(1 - beta) / (1 - beta) + beta * np.log(beta) / (1 - beta) ** 2 + np.log(w) / (1 - beta)
    return {"w": w.tolist(), "kept": kept, "V": V.tolist(), "c": c.tolist(), "c_exact": ((1 - beta) * w).tolist(),
            "gaps": gaps, "iterations": len(gaps), "beta": beta, "V_exact": exact_V.tolist()}


# --- Markov chains for shocks --------------------------------------------------------------------------------------
def tauchen(n: int, rho: float, sigma: float, m: float = 3.0) -> dict:
    """Tauchen (1986): an n-state chain approximating ``z' = rho z + e``, ``e ~ N(0, sigma^2)``, on a grid spanning
    ``m`` unconditional standard deviations."""
    sd = sigma / np.sqrt(1 - rho ** 2)
    z = np.linspace(-m * sd, m * sd, n)
    step = z[1] - z[0]
    P = np.empty((n, n))
    for i in range(n):
        mu = rho * z[i]
        cdf_hi = norm.cdf((z - mu + step / 2) / sigma)
        cdf_lo = norm.cdf((z - mu - step / 2) / sigma)
        P[i] = cdf_hi - cdf_lo
        P[i, 0] = cdf_hi[0]
        P[i, -1] = 1 - cdf_lo[-1]
    return {"z": z.tolist(), "P": P.tolist()}


def rouwenhorst(n: int, rho: float, sigma: float) -> dict:
    """Rouwenhorst's chain, exact in its first two moments for any persistence (Kopecky and Suen 2010)."""
    p = (1 + rho) / 2
    P = np.array([[p, 1 - p], [1 - p, p]])
    for k in range(3, n + 1):
        Z = np.zeros((k, k))
        Z[:-1, :-1] += p * P
        Z[:-1, 1:] += (1 - p) * P
        Z[1:, :-1] += (1 - p) * P
        Z[1:, 1:] += p * P
        Z[1:-1] /= 2
        P = Z
    sd = sigma / np.sqrt(1 - rho ** 2)
    psi = sd * np.sqrt(n - 1)
    return {"z": np.linspace(-psi, psi, n).tolist(), "P": P.tolist()}


def chain_moments(z, P) -> dict:
    """The stationary distribution, standard deviation and first-order autocorrelation of a Markov chain."""
    z, P = np.asarray(z, float), np.asarray(P, float)
    w, v = np.linalg.eig(P.T)
    pi = np.real(v[:, np.argmin(np.abs(w - 1))])
    pi = pi / pi.sum()
    m = pi @ z
    var = pi @ (z - m) ** 2
    cov = (pi * (z - m)) @ (P @ (z - m))
    return {"pi": pi.tolist(), "sd": float(np.sqrt(var)), "rho": float(cov / var)}


# --- trends and cycles ---------------------------------------------------------------------------------------------
def hp_filter(y, lam: float = 1600.0) -> dict:
    """Hodrick and Prescott (1997): the trend ``tau`` minimizing ``sum (y - tau)^2 + lam sum (Delta^2 tau)^2``;
    returns trend and cycle."""
    y = np.asarray(y, float)
    T = len(y)
    D = sparse.diags([np.ones(T - 2), -2 * np.ones(T - 2), np.ones(T - 2)], [0, 1, 2], shape=(T - 2, T))
    A = sparse.eye(T) + lam * (D.T @ D)
    tau = spsolve(A.tocsc(), y)
    return {"trend": tau.tolist(), "cycle": (y - tau).tolist()}


def hamilton_filter(y, h: int = 8, p: int = 4) -> dict:
    """Hamilton (2018): the cycle is the error in forecasting ``y_{t+h}`` by a regression on ``y_t, ..., y_{t-p+1}``;
    returns the cycle aligned with the dates ``t + h`` (the first ``h + p - 1`` dates are lost)."""
    y = np.asarray(y, float)
    rows = range(p - 1, len(y) - h)
    X = np.column_stack([np.ones(len(rows))] + [[y[t - j] for t in rows] for j in range(p)])
    Y = np.array([y[t + h] for t in rows])
    b, *_ = np.linalg.lstsq(X, Y, rcond=None)
    return {"cycle": (Y - X @ b).tolist(), "start": p - 1 + h}
