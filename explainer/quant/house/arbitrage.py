"""The arbitrage checker (Part 9, research): the fundamental theorem in one period, super-replication, static checks
on a surface of option prices, martingale optimal transport bounds, and Ross recovery.  Used on every surface the
House prices against; tested in ``tests/test_quant_house.py``.

* ``ftap``: given payoffs D (assets x states) and prices p, either strictly positive state prices psi with D psi = p
  exist, or an arbitrage portfolio does (Farkas's lemma), found by linear programming;
* ``superhedge``: the cheapest portfolio whose payoff dominates a claim, and the richest one it dominates: the
  no-arbitrage price interval in an incomplete market;
* ``static_checks``: call prices across strikes must be decreasing, convex and within their bounds, and total implied
  variance must not fall with maturity;
* ``mot_bounds``: the range of prices of a path-dependent claim consistent with two maturities' marginals and the
  martingale property (Beiglboeck, Henry-Labordere and Penkner 2013), as a linear program;
* ``ross_recovery``: Perron-Frobenius on a state-price transition matrix (Ross 2015), and what it recovers when the
  pricing kernel has a permanent component (Borovicka, Hansen and Scheinkman 2016).
"""

from __future__ import annotations

import numpy as np
from scipy import sparse
from scipy.optimize import linprog


# ---------------------------------------------------------------------------
def parity_gap(C, P, S, K, T, r=0.0, q=0.0):
    """C - P - (S e^{-qT} - K e^{-rT}): zero without arbitrage, frictions aside."""
    return np.asarray(C) - np.asarray(P) - (np.asarray(S) * np.exp(-q * np.asarray(T)) - np.asarray(K) * np.exp(-r * np.asarray(T)))


def ftap(D, p) -> dict:
    """One period, finitely many states.  Returns ``no_arbitrage`` and either strictly positive state prices ``psi``
    with D psi = p (maximizing the smallest one) or an arbitrage portfolio ``theta`` (cost theta.p <= 0 and payoff
    D^T theta >= 0, not identically zero, normalized to total payoff 1)."""
    D, p = np.asarray(D, float), np.asarray(p, float)
    n, m = D.shape
    # maximize t subject to psi_j >= t, D psi = p, t <= 1
    c = np.zeros(m + 1)
    c[-1] = -1.0
    A_ub = np.hstack([-np.eye(m), np.ones((m, 1))])
    A_eq = np.hstack([D, np.zeros((n, 1))])
    res = linprog(c, A_ub=A_ub, b_ub=np.zeros(m), A_eq=A_eq, b_eq=p, bounds=[(0, None)] * m + [(None, 1.0)],
                  method="highs")
    if res.status == 0 and res.x[-1] > 1e-10:
        return {"no_arbitrage": True, "psi": res.x[:m], "min_psi": float(res.x[-1])}
    # an arbitrage: minimize theta.p subject to D^T theta >= 0, sum(D^T theta) = 1, |theta| <= big
    res = linprog(p, A_ub=-D.T, b_ub=np.zeros(m), A_eq=D.sum(axis=1)[None, :], b_eq=[1.0],
                  bounds=[(-1e6, 1e6)] * n, method="highs")
    theta = res.x
    return {"no_arbitrage": False, "theta": theta, "cost": float(theta @ p), "payoff": D.T @ theta}


def superhedge(D, p, X) -> dict:
    """Bounds on the price of a claim with state payoffs X: upper = min theta.p s.t. D^T theta >= X, lower =
    max theta.p s.t. D^T theta <= X.  Equal when the claim is replicable."""
    D, p, X = np.asarray(D, float), np.asarray(p, float), np.asarray(X, float)
    n = D.shape[0]
    up = linprog(p, A_ub=-D.T, b_ub=-X, bounds=[(None, None)] * n, method="highs")
    lo = linprog(-p, A_ub=D.T, b_ub=X, bounds=[(None, None)] * n, method="highs")
    return {"upper": float(up.fun), "lower": float(-lo.fun), "theta_up": up.x, "theta_lo": lo.x}


# ---------------------------------------------------------------------------
def static_checks(K, C, F, df=1.0, tol=1e-10) -> dict:
    """Call prices C(K) on one maturity (forward F, discount df): monotone decreasing (no call spread for free),
    convex (no negative butterfly), and df max(F - K, 0) <= C <= df F.  Returns the violations."""
    K, C = np.asarray(K, float), np.asarray(C, float)
    o = np.argsort(K)
    K, C = K[o], C[o]
    slope = np.diff(C) / np.diff(K)
    mono = np.where(slope > tol)[0]
    steep = np.where(slope < -df - tol)[0]
    fly = np.where(np.diff(slope) < -tol)[0]
    lo = np.where(C < df * np.maximum(F - K, 0) - tol)[0]
    hi = np.where(C > df * F + tol)[0]
    return {"monotone": mono.tolist(), "slope": steep.tolist(), "butterfly": fly.tolist(), "lower": lo.tolist(),
            "upper": hi.tolist(), "ok": not (len(mono) or len(steep) or len(fly) or len(lo) or len(hi))}


def calendar_check(k, w_short, w_long, tol=1e-10) -> list:
    """Total implied variance at the same log-moneyness must not fall with maturity (no calendar arbitrage)."""
    return np.where(np.asarray(w_long) < np.asarray(w_short) - tol)[0].tolist()


# ---------------------------------------------------------------------------
def mot_bounds(x, mu, y, nu, cost) -> dict:
    """min and max of sum pi_ij c(x_i, y_j) over couplings pi >= 0 with row sums mu, column sums nu and the martingale
    condition sum_j pi_ij (y_j - x_i) = 0 for every i.  ``mu`` and ``nu`` must have equal means and be in convex order.
    Returns both values and both optimal couplings."""
    x, mu, y, nu = (np.asarray(a, float) for a in (x, mu, y, nu))
    n, m = len(x), len(y)
    C = np.asarray([[cost(a, b) for b in y] for a in x]).ravel()
    rows, cols, vals = [], [], []
    r = 0
    for i in range(n):  # row sums
        rows += [r] * m
        cols += list(i * m + np.arange(m))
        vals += [1.0] * m
        r += 1
    for j in range(m):  # column sums
        rows += [r] * n
        cols += list(np.arange(n) * m + j)
        vals += [1.0] * n
        r += 1
    for i in range(n):  # martingale
        rows += [r] * m
        cols += list(i * m + np.arange(m))
        vals += list(y - x[i])
        r += 1
    A = sparse.csr_matrix((vals, (rows, cols)), shape=(r, n * m))
    b = np.concatenate([mu, nu, np.zeros(n)])
    out = {}
    for name, sign in (("lower", 1.0), ("upper", -1.0)):
        res = linprog(sign * C, A_eq=A, b_eq=b, bounds=(0, None), method="highs")
        if res.status != 0:
            raise ValueError(f"MOT {name} infeasible: {res.message} (are the marginals in convex order?)")
        out[name] = float(sign * res.fun)
        out[f"pi_{name}"] = res.x.reshape(n, m)
    return out


def convex_order_fix(x, mu, y, nu):
    """Discretized marginals rarely have exactly equal means; shift the later grid so the means agree."""
    return np.asarray(y) + (np.dot(x, mu) - np.dot(y, nu))


# ---------------------------------------------------------------------------
def ross_recovery(P) -> dict:
    """Ross (2015): a state-price transition matrix P (P_ij = price today, in state i, of 1 tomorrow in state j)
    factors as P = delta D^{-1} F D if the pricing kernel is a discount factor times a ratio of a function of the
    state.  The Perron root delta and its positive eigenvector z give the recovered transition probabilities
    F_ij = P_ij z_j / (delta z_i)."""
    P = np.asarray(P, float)
    w, V = np.linalg.eig(P)
    k = int(np.argmax(w.real))
    delta = float(w[k].real)
    z = np.abs(V[:, k].real)
    F = P * z[None, :] / (delta * z[:, None])
    return {"delta": delta, "z": z, "F": F}
