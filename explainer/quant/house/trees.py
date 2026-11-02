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


def derman_kani(S0, T, N, iv_fn, r=0.0) -> dict:
    """Derman and Kani's (1994) implied binomial tree: an N-step recombining tree whose nodes are placed, level by
    level, so that it reprices a call (above the centre) or a put (below) struck at every node of the previous level,
    with the smile ``iv_fn(K, t)`` (Black implied vol at strike K and expiry t, forward S0 e^{rt}). Odd levels are
    centred on the forward; a node that would break the ordering S_i < F_i < S_{i+1} is replaced by the previous
    level's log spacing (counted in ``fixes``). Returns the levels' ``nodes``, Arrow-Debreu prices ``ad``, up
    probabilities ``p`` and node local volatilities ``local_vol`` (sqrt(p (1-p)) ln(S_up/S_down) / sqrt(dt))."""
    from explainer.quant.house import bs

    dt = T / N
    g = np.exp(r * dt)
    nodes, ad, probs, lvs = [np.array([float(S0)])], [np.array([1.0])], [], []
    fixes = 0

    def price(K, t, cp):
        F = S0 * np.exp(r * t)
        return float(np.exp(-r * t) * bs.price(F, K, t, float(iv_fn(K, t)), 0.0, 0.0, cp))

    for n in range(N):
        s, lam = nodes[-1], ad[-1]
        t1 = (n + 1) * dt
        Fi = s * g
        S = np.full(n + 2, np.nan)
        if (n + 2) % 2 == 1:  # odd number of new nodes: the centre sits at the forward
            jc = (n + 1) // 2
            S[jc] = S0 * np.exp(r * t1)
            up_from, down_from = jc, jc - 1
        else:
            ic = n // 2
            C = price(s[ic], t1, 1)
            sig = float(np.sum(lam[ic + 1:] * (Fi[ic + 1:] - s[ic])))
            S[ic + 1] = s[ic] * (g * C + lam[ic] * s[ic] - sig) / (lam[ic] * Fi[ic] - g * C + sig)
            S[ic] = s[ic] ** 2 / S[ic + 1]
            if not (S[ic] < Fi[ic] < S[ic + 1]):
                h = np.exp(np.sqrt(dt) * float(iv_fn(s[ic], t1)))
                S[ic], S[ic + 1] = s[ic] / h, s[ic] * h
                fixes += 1
            up_from, down_from = ic + 1, ic - 1
        tiny = 1e-9 * S0
        for i in range(up_from, n + 1):  # upper nodes, from calls struck at s_i: F_i < S_{i+1} < F_{i+1}
            C = price(s[i], t1, 1)
            sig = float(np.sum(lam[i + 1:] * (Fi[i + 1:] - s[i])))
            num = S[i] * (g * C - sig) - lam[i] * s[i] * (Fi[i] - S[i])
            den = g * C - sig - lam[i] * (Fi[i] - S[i])
            x = num / den if (den != 0 and C > tiny) else np.nan

            def ok(x, i=i):
                return np.isfinite(x) and x > Fi[i] and (i == n or x < Fi[i + 1])
            if not ok(x):
                fixes += 1
                x = S[i] * (s[i + 1] / s[i] if i < n else s[i] / s[i - 1])
                if not ok(x):
                    x = 0.5 * (Fi[i] + Fi[i + 1]) if i < n else 2 * Fi[i] - S[i]
            S[i + 1] = x
        for i in range(down_from, -1, -1):  # lower nodes, from puts struck at s_i: F_{i-1} < S_i < F_i
            P = price(s[i], t1, -1)
            sig = float(np.sum(lam[:i] * (s[i] - Fi[:i])))
            num = S[i + 1] * (g * P - sig) + lam[i] * s[i] * (Fi[i] - S[i + 1])
            den = g * P - sig + lam[i] * (Fi[i] - S[i + 1])
            x = num / den if (den != 0 and P > tiny) else np.nan

            def ok(x, i=i):
                return np.isfinite(x) and 0 < x < Fi[i] and (i == 0 or x > Fi[i - 1])
            if not ok(x):
                fixes += 1
                x = S[i + 1] * s[i] / s[i + 1]
                if not ok(x):
                    x = 0.5 * (Fi[i - 1] + Fi[i]) if i > 0 else Fi[i] ** 2 / S[i + 1]
            S[i] = x
        p = (Fi - S[:-1]) / (S[1:] - S[:-1])
        lam_new = np.zeros(n + 2)
        lam_new[:-1] += lam * (1 - p) / g
        lam_new[1:] += lam * p / g
        nodes.append(S)
        ad.append(lam_new)
        probs.append(p)
        lvs.append(np.sqrt(p * (1 - p)) * np.log(S[1:] / S[:-1]) / np.sqrt(dt))
    return {"nodes": nodes, "ad": ad, "p": probs, "local_vol": lvs, "dt": dt, "fixes": fixes}


def tree_price(tree: dict, K, cp=1) -> np.ndarray:
    """European options at the tree's last level: the sum of Arrow-Debreu prices times payoffs."""
    S, lam = tree["nodes"][-1], tree["ad"][-1]
    K = np.atleast_1d(np.asarray(K, float))
    return np.array([float(np.sum(lam * np.maximum(cp * (S - k), 0.0))) for k in K])
