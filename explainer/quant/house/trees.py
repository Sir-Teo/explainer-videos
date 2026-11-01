"""Binomial trees (Cox–Ross–Rubinstein 1979): European and American options by backward induction, with the hedge
at every node and the early-exercise boundary.

    out = crr(S=100, K=100, T=1, sigma=0.2, r=0.05, N=500, cp=-1, american=True, boundary=True)
    out["price"], out["boundary"]        # the American put and its critical spot price at each step

The tree is u = e^{sigma sqrt(dt)}, d = 1/u, with risk-neutral probability p = (e^{(r-q)dt} - d) / (u - d).
"""

from __future__ import annotations

import numpy as np


def crr(S, K, T, sigma, r=0.0, q=0.0, N=200, cp=1, american=False, boundary=False, keep=0) -> dict:
    """Price an option on an N-step CRR tree.

    Returns ``price``, ``delta`` and ``gamma`` at the root (from the first two layers), ``p`` (the risk-neutral up
    probability), and with ``boundary`` the early-exercise boundary: for each step, the highest spot (puts) or
    lowest spot (calls) at which exercising is optimal (NaN where it never is).  With ``keep`` > 0, the first
    ``keep`` layers of spots, values and hedge ratios are returned too, for drawing the tree."""
    dt = T / N
    u = np.exp(sigma * np.sqrt(dt))
    d = 1.0 / u
    g = np.exp((r - q) * dt)
    p = (g - d) / (u - d)
    if not 0.0 < p < 1.0:
        raise ValueError(f"risk-neutral probability {p} outside (0, 1): dt too large for these r, q, sigma")
    disc = np.exp(-r * dt)
    j = np.arange(N + 1)
    spots = S * u ** (2 * j - N)  # at maturity, from the bottom node up
    values = np.maximum(cp * (spots - K), 0.0)
    bnd = np.full(N, np.nan)
    layers = {}
    v1 = v2 = None
    for n in range(N - 1, -1, -1):
        spots_n = S * u ** (2 * np.arange(n + 1) - n)
        cont = disc * (p * values[1:] + (1 - p) * values[:-1])
        if american:
            ex = np.maximum(cp * (spots_n - K), 0.0)
            exercise = ex > cont + 1e-14
            values = np.where(exercise, ex, cont)
            if boundary and exercise.any():
                bnd[n] = spots_n[exercise].max() if cp < 0 else spots_n[exercise].min()
        else:
            values = cont
        if n < keep:
            layers[n] = {"spots": spots_n.copy(), "values": values.copy()}
        if n == 2:
            v2, s2 = values.copy(), spots_n.copy()
        if n == 1:
            v1, s1 = values.copy(), spots_n.copy()
    out = {"price": float(values[0]), "p": float(p), "u": float(u), "dt": float(dt)}
    if v1 is not None:
        out["delta"] = float((v1[1] - v1[0]) / (s1[1] - s1[0]))
    if v2 is not None:
        d_up = (v2[2] - v2[1]) / (s2[2] - s2[1])
        d_dn = (v2[1] - v2[0]) / (s2[1] - s2[0])
        out["gamma"] = float((d_up - d_dn) / (0.5 * (s2[2] - s2[0])))
    if boundary:
        out["boundary"] = bnd
        out["times"] = np.arange(N) * dt
    if keep:
        hedge = {}
        for n in range(min(keep, N) - 1):
            v_next, s_next = layers[n + 1]["values"], layers[n + 1]["spots"]
            hedge[n] = (v_next[1:] - v_next[:-1]) / (s_next[1:] - s_next[:-1])
        out["layers"] = {n: {**layers[n], "delta": hedge.get(n)} for n in sorted(layers)}
    return out
