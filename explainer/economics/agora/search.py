"""Agora's labour market with frictions (Part 24 of *Economics, Built*): looking for work, and for workers.

* :func:`mccall`: McCall's (1970) searcher: wage offers drawn one at a time, a benefit while searching; the reservation
  wage and the expected duration of search.
* :func:`dmp_steady`: the Diamond-Mortensen-Pissarides model in steady state: a Cobb-Douglas matching function, free
  entry of vacancies (the job-creation curve), Nash bargaining (the wage curve); tightness, the wage, unemployment and
  vacancies.  :func:`dmp_curves` gives both curves for plotting.
* :func:`beveridge`: steady states as productivity moves (a movement along the Beveridge curve) and as matching
  efficiency moves (a shift).
* :func:`dmp_path`: unemployment's path after a permanent change in productivity: tightness jumps, unemployment follows
  at the rate ``s + f``.
* :func:`hosios`: steady-state net output against the worker's bargaining share; the maximum at the matching elasticity
  (Hosios 1990).
* :func:`elasticity`: the response of tightness to productivity, ``d ln theta / d ln p``, for any calibration: the
  volatility puzzle (Shimer 2005) and the small-surplus answer (Hagedorn and Manovskii 2008).
* :func:`flows`, :func:`ins_outs`: Shimer's (2012) job-finding and separation rates from unemployment by duration,
  with the time-aggregation correction, and the share of unemployment's movements due to each.
* :func:`burdett_mortensen`: the Burdett-Mortensen (1998) job ladder: the equilibrium offer and earnings distributions.

numpy only.
"""

from __future__ import annotations

import numpy as np


def mccall(b: float = 0.4, beta: float = 0.99, wages=None, probs=None, sep: float = 0.0, tol: float = 1e-10) -> dict:
    """An unemployed worker gets one offer a period from ``wages`` with ``probs``; accepting w gives w each period
    until a separation (probability ``sep``), searching gives b now and another draw next period.  Returns the
    reservation wage, the chance an offer is accepted, and the expected duration of search in periods."""
    if wages is None:
        wages = np.linspace(0.2, 1.8, 161)
    wages = np.asarray(wages, float)
    probs = np.ones_like(wages) / len(wages) if probs is None else np.asarray(probs, float) / np.sum(probs)
    U = b / (1 - beta)
    for _ in range(100000):
        W = (wages + beta * sep * U) / (1 - beta * (1 - sep))
        U_new = b + beta * np.sum(probs * np.maximum(W, U))
        if abs(U_new - U) < tol:
            U = U_new
            break
        U = U_new
    # the reservation wage solves W(w*) = U
    w_star = U * (1 - beta * (1 - sep)) - beta * sep * U
    accept = float(np.sum(probs[wages >= w_star]))
    return {"reservation": float(w_star), "accept": accept, "duration": 1 / accept if accept > 0 else np.inf,
            "U": float(U), "mean_offer": float(np.sum(probs * wages)),
            "mean_accepted": float(np.sum(probs * wages * (wages >= w_star)) / max(accept, 1e-12))}


def _f(theta, A, eta):
    return A * theta ** (1 - eta)


def _q(theta, A, eta):
    return A * theta ** (-eta)


def dmp_steady(p: float = 1.0, b: float = 0.4, beta: float = 0.5, eta: float = 0.5, A: float = 0.6, s: float = 0.03,
               r: float = 0.004, c: float = 0.3) -> dict:
    """Monthly DMP: job finding ``f = A theta^(1-eta)``, vacancy filling ``q = A theta^(-eta)``.  Free entry:
    ``c / q = (p - w)/(r + s)``.  Nash wage: ``w = (1 - beta) b + beta (p + c theta)``.  Together:
    ``(r + s) c / q(theta) + beta c theta = (1 - beta)(p - b)``; steady unemployment ``u = s/(s + f)``."""
    lo, hi = 1e-8, 1e4

    def gap(th):
        return (r + s) * c / _q(th, A, eta) + beta * c * th - (1 - beta) * (p - b)
    if gap(lo) > 0:
        return {"theta": 0.0, "w": b, "u": 1.0, "v": 0.0, "f": 0.0, "q": np.inf}
    for _ in range(200):
        mid = np.sqrt(lo * hi)
        if gap(mid) > 0:
            hi = mid
        else:
            lo = mid
    th = np.sqrt(lo * hi)
    f = _f(th, A, eta)
    u = s / (s + f)
    w = (1 - beta) * b + beta * (p + c * th)
    return {"theta": float(th), "w": float(w), "u": float(u), "v": float(th * u), "f": float(f),
            "q": float(_q(th, A, eta)), "p": p, "b": b, "beta": beta, "eta": eta, "A": A, "s": s, "r": r, "c": c}


def dmp_curves(thetas, **kw) -> dict:
    """The job-creation curve ``w = p - (r + s) c / q(theta)`` and the wage curve ``w = (1-beta) b + beta(p + c
    theta)`` over ``thetas``."""
    d = {"p": 1.0, "b": 0.4, "beta": 0.5, "eta": 0.5, "A": 0.6, "s": 0.03, "r": 0.004, "c": 0.3}
    d.update(kw)
    th = np.asarray(thetas, float)
    jc = d["p"] - (d["r"] + d["s"]) * d["c"] / _q(th, d["A"], d["eta"])
    wc = (1 - d["beta"]) * d["b"] + d["beta"] * (d["p"] + d["c"] * th)
    return {"theta": th.tolist(), "jc": jc.tolist(), "wc": wc.tolist()}


def beveridge(ps=None, As=None, **kw) -> dict:
    """Steady-state (u, v) as productivity varies (along one Beveridge curve) and the curve for each matching
    efficiency in ``As`` (shifts)."""
    ps = np.linspace(0.9, 1.1, 21) if ps is None else np.asarray(ps, float)
    As = (0.6,) if As is None else As
    curves = []
    for A in As:
        pts = [dmp_steady(p=float(p), A=float(A), **kw) for p in ps]
        curves.append({"A": float(A), "u": [x["u"] for x in pts], "v": [x["v"] for x in pts], "p": ps.tolist()})
    return {"curves": curves}


def dmp_path(p0: float = 1.0, p1: float = 0.97, months: int = 36, **kw) -> dict:
    """Unemployment after a permanent change in productivity at month 0: tightness (a jump variable) moves at once to
    its new steady state, and unemployment follows ``u' = u + s (1 - u) - f u``."""
    a = dmp_steady(p=p0, **kw)
    z = dmp_steady(p=p1, **kw)
    u = [a["u"]]
    for _ in range(months):
        u.append(u[-1] + z["s"] * (1 - u[-1]) - z["f"] * u[-1])
    return {"u": u, "u_old": a["u"], "u_new": z["u"], "theta_old": a["theta"], "theta_new": z["theta"],
            "half_life": float(np.log(2) / (z["s"] + z["f"]))}


def hosios(betas=None, **kw) -> dict:
    """Steady-state flow of net output, ``(1 - u) p + u b - c v``, against the bargaining share (with r near zero, the
    planner's objective in a steady state); it peaks where beta equals the matching elasticity eta."""
    betas = np.linspace(0.05, 0.95, 91) if betas is None else np.asarray(betas, float)
    kw = {**kw, "r": kw.get("r", 1e-6)}
    out = []
    for bt in betas:
        d = dmp_steady(beta=float(bt), **kw)
        out.append((1 - d["u"]) * d["p"] + d["u"] * d["b"] - d["c"] * d["v"])
    k = int(np.argmax(out))
    return {"beta": betas.tolist(), "net": out, "best": float(betas[k])}


def elasticity(p: float = 1.0, dp: float = 0.01, **kw) -> dict:
    """``d ln theta / d ln p`` and ``d ln u / d ln p`` by central differences."""
    up = dmp_steady(p=p * (1 + dp), **kw)
    dn = dmp_steady(p=p * (1 - dp), **kw)
    mid = dmp_steady(p=p, **kw)
    e_th = (np.log(up["theta"]) - np.log(dn["theta"])) / (np.log(1 + dp) - np.log(1 - dp))
    e_u = (np.log(up["u"]) - np.log(dn["u"])) / (np.log(1 + dp) - np.log(1 - dp))
    return {"theta": float(e_th), "u": float(e_u), "steady": mid}


def flows(u, us, lf, correction=None) -> dict:
    """Shimer's (2012) monthly rates from unemployment ``u``, short-term unemployment ``us`` (under five weeks) and
    the labour force ``lf``: the job-finding probability ``F = 1 - (u' - us')/u``, the hazard ``f = -ln(1 - F)``, and
    the separation hazard ``s`` solving ``u' = (1 - e^{-(f+s)}) s/(f+s) lf + e^{-(f+s)} u`` (time aggregation).
    ``correction`` multiplies short-term unemployment (a list of factors, one per month: Shimer raised it about 10%
    after the 1994 survey redesign).  Returns f, s and the steady state ``s/(s+f)``, monthly."""
    u, us, lf = (np.asarray(x, float) for x in (u, us, lf))
    if correction is not None:
        us = us * np.asarray(correction, float)
    F = 1 - (u[1:] - us[1:]) / u[:-1]
    F = np.clip(F, 1e-6, 1 - 1e-6)
    f = -np.log(1 - F)
    s = np.empty_like(f)
    for k in range(len(f)):
        lo, hi = 1e-8, 1.0
        for _ in range(80):
            mid = (lo + hi) / 2
            x = f[k] + mid
            pred = (1 - np.exp(-x)) * mid / x * lf[k] + np.exp(-x) * u[k]
            if pred > u[k + 1]:
                hi = mid
            else:
                lo = mid
        s[k] = (lo + hi) / 2
    ss = s / (s + f)
    return {"f": f.tolist(), "s": s.tolist(), "steady": ss.tolist(), "F": F.tolist()}


def hp_filter(y, lam: float = 1e5) -> np.ndarray:
    """The Hodrick-Prescott trend of ``y`` (dense solve; fine for a few hundred points)."""
    y = np.asarray(y, float)
    n = len(y)
    D = np.zeros((n - 2, n))
    for i in range(n - 2):
        D[i, i:i + 3] = [1.0, -2.0, 1.0]
    return np.linalg.solve(np.eye(n) + lam * D.T @ D, y)


def ins_outs(f, s, lam: float = 1e5) -> dict:
    """Shimer's decomposition: with quarterly rates f and s, the steady state ``s/(s+f)`` and its two counterfactuals
    (f moving with s at its mean, and s moving with f at its mean), each in logs and HP-detrended; the share of the
    steady state's variance due to each is its covariance with the actual over the actual's variance."""
    f, s = np.asarray(f, float), np.asarray(s, float)
    act = np.log(s / (s + f))
    cf = np.log(s.mean() / (s.mean() + f))
    cs = np.log(s / (s + f.mean()))
    a, b, c = (x - hp_filter(x, lam) for x in (act, cf, cs))
    return {"share_f": float(np.cov(a, b)[0, 1] / np.var(a, ddof=1)),
            "share_s": float(np.cov(a, c)[0, 1] / np.var(a, ddof=1)),
            "steady": np.exp(act).tolist(), "only_f": np.exp(cf).tolist(), "only_s": np.exp(cs).tolist()}


def burdett_mortensen(p: float = 1.0, b: float = 0.4, lam: float = 0.1, delta: float = 0.02, n: int = 200) -> dict:
    """Burdett and Mortensen's (1998) job ladder, with offers arriving at rate ``lam`` to the employed and the
    unemployed alike (so the reservation wage is b), separations at ``delta``, and identical firms with productivity
    p.  The equilibrium offer distribution is ``F(w) = (1 + k)/k [1 - sqrt((p - w)/(p - b))]``, ``k = lam/delta``, on
    ``[b, p - (p - b)/(1 + k)^2]``; the earnings distribution of the employed is ``G = F / (1 + k (1 - F))``.
    Workers climb the ladder, so G sits to the right of F, and identical workers earn different wages."""
    k = lam / delta
    w_hi = p - (p - b) / (1 + k) ** 2
    ws = np.linspace(b, w_hi, n)
    F = np.clip((1 + k) / k * (1 - np.sqrt(np.clip((p - ws) / (p - b), 0, 1))), 0, 1)
    G = F / (1 + k * (1 - F))
    fdens = np.gradient(F, ws)
    gdens = np.gradient(G, ws)
    return {"w": ws.tolist(), "F": F.tolist(), "G": G.tolist(), "f": fdens.tolist(), "g": gdens.tolist(),
            "w_lo": float(b), "w_hi": float(w_hi), "mean_offer": float(np.trapezoid(ws * fdens, ws)),
            "mean_earned": float(np.trapezoid(ws * gdens, ws)), "u": delta / (delta + lam), "k": k}
