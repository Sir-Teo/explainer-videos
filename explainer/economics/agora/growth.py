"""Agora's growth (Part 20 of *Economics, Built*): capital accumulation, accounting and convergence.

* :func:`solow_path`, :func:`solow_steady`, :func:`golden_rule`, :func:`convergence_speed`: the Solow model in units of
  effective labour, a year at a time, ``k' = k + s k^alpha - (n + g + delta) k`` (the continuous model's equation in
  annual steps, so the two share a steady state), its steady state, the saving rate that
  maximizes steady-state consumption (``s = alpha``), and the speed of convergence ``(1 - alpha)(n + g + delta)`` with
  the exact half-life of the simulated path.
* :func:`harrod_domar`: growth from a saving rate and a capital-output ratio, ``s / v - delta``, and the knife edge
  against labour-force growth.
* :func:`growth_accounting`: Solow's (1957) decomposition of output growth into capital, labour (with human capital)
  and the residual, from Penn World Table rows.
* :func:`development_accounting`: Hall and Jones's (1999) decomposition of income per worker into capital intensity
  ``(K/Y)^(alpha/(1-alpha))``, human capital and TFP, the share of the variance of log income that capital intensity
  and schooling explain, and Caselli's (2005) "success" ``var(log k^alpha h^(1-alpha)) / var(log y)``.
* :func:`convergence`: OLS of average growth on initial log income, with or without controls, and the implied speed.
* :func:`mpk_ratio`: Lucas's (1990) question: the ratio of marginal products of capital implied by income gaps, with and
  without human capital.
* :func:`ramsey`: the Ramsey-Cass-Koopmans model solved for its saddle path by shooting.

numpy only; the regressions report heteroskedasticity-robust (HC1) standard errors.
"""

from __future__ import annotations

import numpy as np


# ---------------------------------------------------------------------------------------------------------------
# Solow

def solow_steady(s: float, n: float = 0.01, g: float = 0.02, delta: float = 0.05, alpha: float = 1 / 3) -> dict:
    """Steady state per effective worker: ``k* = (s / (n + g + delta))^(1 / (1 - alpha))``, output, consumption and
    the capital-output ratio ``s / (n + g + delta)``."""
    k = (s / (n + g + delta)) ** (1 / (1 - alpha))
    y = k ** alpha
    return {"k": k, "y": y, "c": (1 - s) * y, "ky": k / y, "mpk": alpha * k ** (alpha - 1)}


def golden_rule(n: float = 0.01, g: float = 0.02, delta: float = 0.05, alpha: float = 1 / 3,
                grid: int = 1001) -> dict:
    """The saving rate that maximizes steady-state consumption per effective worker (it equals alpha), with the
    consumption curve over saving rates."""
    s = np.linspace(0.0, 1.0, grid)
    c = np.array([solow_steady(x, n, g, delta, alpha)["c"] if x > 0 else 0.0 for x in s])
    k = int(np.argmax(c))
    return {"s": s, "c": c, "s_gold": float(s[k]), "c_gold": float(c[k])}


def solow_path(s, years: int = 100, k0: float | None = None, n: float = 0.01, g: float = 0.02,
               delta: float = 0.05, alpha: float = 1 / 3) -> dict:
    """Annual path from ``k0`` (default: the steady state of the first saving rate) under a saving rate that may
    change: ``s`` is a number or a function of the year.  Returns k, y and c per effective worker and income per
    worker (effective output times technology growing at g)."""
    sf = s if callable(s) else (lambda t: s)
    k = solow_steady(sf(0), n, g, delta, alpha)["k"] if k0 is None else float(k0)
    ks, ys, cs, ypw = [], [], [], []
    for t in range(years + 1):
        y = k ** alpha
        ks.append(k)
        ys.append(y)
        cs.append((1 - sf(t)) * y)
        ypw.append(y * (1 + g) ** t)
        k = k + sf(t) * y - (n + g + delta) * k
    return {"t": list(range(years + 1)), "k": ks, "y": ys, "c": cs, "y_per_worker": ypw}


def convergence_speed(n: float = 0.01, g: float = 0.02, delta: float = 0.05, alpha: float = 1 / 3) -> dict:
    """The linearized speed ``lambda = (1 - alpha)(n + g + delta)`` and the half-life ``ln 2 / lambda``; and the
    half-life measured on a simulated path from half the steady-state capital."""
    lam = (1 - alpha) * (n + g + delta)
    s = 0.2
    ks = solow_steady(s, n, g, delta, alpha)["k"]
    p = solow_path(s, 300, k0=0.25 * ks, n=n, g=g, delta=delta, alpha=alpha)
    gap = np.log(ks ** alpha) - np.log(np.array(p["y"]))
    half = next(t for t, x in enumerate(gap) if x <= gap[0] / 2)
    return {"lambda": lam, "half_life": float(np.log(2) / lam), "half_life_simulated": int(half)}


def harrod_domar(s: float, v: float, delta: float = 0.05, labour: float = 0.02) -> dict:
    """Harrod-Domar growth ``g = s / v - delta`` with a fixed capital-output ratio v; the saving rate needed for a
    target; and the knife edge: unless g equals labour-force growth, unemployment or idle capital grows."""
    gr = s / v - delta
    return {"growth": gr, "needed_for_target": lambda target: v * (target + delta), "gap_to_labour": gr - labour}


# ---------------------------------------------------------------------------------------------------------------
# accounting

def growth_accounting(rows: list, first: int, last: int, alpha: float | None = None) -> dict:
    """Decompose the average growth of real GDP (``rgdpna``) between two years into capital (``rnna``), hours (emp x
    avh, or emp alone where hours are missing), human capital (``hc``) and the residual, with alpha one minus the
    average labour share (``labsh``) unless given.  Growth rates are log differences per year."""
    by = {r["year"]: r for r in rows}
    a, b = by[first], by[last]
    T = last - first

    def gr(key):
        return (np.log(b[key]) - np.log(a[key])) / T

    hours = (lambda r: r["emp"] * r["avh"]) if np.isfinite(a.get("avh", np.nan)) and np.isfinite(
        b.get("avh", np.nan)) else (lambda r: r["emp"])
    gl = (np.log(hours(b)) - np.log(hours(a))) / T
    if alpha is None:
        shares = [by[y]["labsh"] for y in range(first, last + 1) if y in by and np.isfinite(by[y]["labsh"])]
        alpha = 1 - float(np.mean(shares))
    gy, gk, gh = gr("rgdpna"), gr("rnna"), gr("hc")
    tfp = gy - alpha * gk - (1 - alpha) * (gl + gh)
    per_hour = gy - gl
    return {"alpha": alpha, "output": float(gy), "capital": float(alpha * gk), "hours": float((1 - alpha) * gl),
            "human_capital": float((1 - alpha) * gh), "tfp": float(tfp),
            "tfp_share": float(tfp / gy) if gy else float("nan"),
            "per_hour": float(per_hour), "deepening": float(alpha * (gk - gl)),
            "tfp_share_per_hour": float(tfp / per_hour) if per_hour else float("nan"), "first": first, "last": last}


def development_accounting(rows: list, alpha: float = 1 / 3, base: str = "USA") -> dict:
    """For one year's rows: income per worker y = (K/Y)^(alpha/(1-alpha)) h A, each relative to ``base``; the share of
    the variance of log y explained by the factors, ``var(log y_KH) / var(log y)``, and the 90/10 ratios."""
    ok = [r for r in rows if all(np.isfinite(r.get(k, np.nan)) and r.get(k, 0) > 0
                                 for k in ("rgdpo", "emp", "cn", "hc"))]
    y = np.array([r["rgdpo"] / r["emp"] for r in ok])
    ky = np.array([r["cn"] / r["rgdpo"] for r in ok])
    h = np.array([r["hc"] for r in ok])
    kh = ky ** (alpha / (1 - alpha)) * h
    A = y / kh
    codes = [r["countrycode"] for r in ok]
    i0 = codes.index(base)
    ly, lkh = np.log(y), np.log(kh)
    share = float(np.var(lkh) / np.var(ly))

    def ratio(v):
        hi, lo = np.percentile(v, 90), np.percentile(v, 10)
        return float(hi / lo)
    k = np.array([r["cn"] / r["emp"] for r in ok])
    ykh = k ** alpha * h ** (1 - alpha)             # Caselli's factor-only income, levels form
    success = float(np.var(np.log(ykh)) / np.var(ly))
    out = {"codes": codes, "y_rel": (y / y[i0]).tolist(), "ky_rel": ((ky / ky[i0]) ** (alpha / (1 - alpha))).tolist(),
           "h_rel": (h / h[i0]).tolist(), "A_rel": (A / A[i0]).tolist(), "share_factors": share,
           "success": success, "ratio_y": ratio(y), "ratio_kh": ratio(kh), "ratio_A": ratio(A), "n": len(ok),
           "alpha": alpha}
    return out


# ---------------------------------------------------------------------------------------------------------------
# convergence

def _ols(X, y):
    n, k = X.shape
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    u = y - X @ b
    XtXi = np.linalg.inv(X.T @ X)
    meat = (X * u[:, None]).T @ (X * u[:, None])
    V = XtXi @ meat @ XtXi * n / (n - k)
    r2 = 1 - float(u @ u) / float(((y - y.mean()) ** 2).sum())
    return b, np.sqrt(np.diag(V)), r2


def convergence(y0, y1, years: int, controls=None) -> dict:
    """Average annual log growth ``(ln y1 - ln y0) / years`` on ``ln y0`` (and controls); the slope b, its HC1 s.e.,
    and the implied speed ``lambda = -ln(1 + b T) / T``."""
    y0, y1 = np.asarray(y0, float), np.asarray(y1, float)
    gr = (np.log(y1) - np.log(y0)) / years
    cols = [np.ones(len(y0)), np.log(y0)]
    if controls is not None:
        for c in np.atleast_2d(controls):
            cols.append(np.asarray(c, float))
    X = np.column_stack(cols)
    b, se, r2 = _ols(X, gr)
    slope = float(b[1])
    lam = float(-np.log(1 + slope * years) / years) if 1 + slope * years > 0 else float("nan")
    return {"slope": slope, "se": float(se[1]), "r2": r2, "lambda": lam, "n": len(y0), "coef": b.tolist(),
            "se_all": se.tolist()}


def mpk_ratio(y_poor: float, y_rich: float, alpha: float = 0.4, h_poor: float = 1.0, h_rich: float = 1.0) -> dict:
    """Lucas (1990): with y = A k^alpha and the same A, MPK is proportional to y^((alpha - 1) / alpha), so the poor
    country's MPK is ``(y_rich / y_poor)^((1 - alpha) / alpha)`` times the rich one's.  Measuring labour in
    efficiency units (output per unit of human capital) shrinks the gap."""
    raw = (y_rich / y_poor) ** ((1 - alpha) / alpha)
    adj = ((y_rich / h_rich) / (y_poor / h_poor)) ** ((1 - alpha) / alpha)
    return {"raw": float(raw), "with_human_capital": float(adj)}


# ---------------------------------------------------------------------------------------------------------------
# Ramsey-Cass-Koopmans

def ramsey(alpha: float = 1 / 3, delta: float = 0.05, rho: float = 0.03, theta: float = 2.0, n: float = 0.01,
           g: float = 0.02, k0_share: float = 0.5, T: int = 200, dt: float = 0.05) -> dict:
    """The Ramsey model per effective worker, ``k_dot = k^alpha - c - (n + g + delta) k`` and ``c_dot / c = (alpha
    k^(alpha - 1) - delta - rho - theta g) / theta``, solved for the saddle path from ``k0 = k0_share * k*`` by
    shooting on c0 (bisection: too high a c0 runs capital out, too low overaccumulates).  Returns the path, the steady
    state, the saddle path's c0, and two missed shots for the picture."""
    kss = (alpha / (delta + rho + theta * g)) ** (1 / (1 - alpha))
    css = kss ** alpha - (n + g + delta) * kss
    k0 = k0_share * kss
    steps = int(T / dt)

    def shoot(c0):
        k, c = k0, c0
        ks, cs = [k], [c]
        for _ in range(steps):
            kd = k ** alpha - c - (n + g + delta) * k
            cd = c * (alpha * k ** (alpha - 1) - delta - rho - theta * g) / theta
            k, c = k + dt * kd, c + dt * cd
            if k <= 1e-6 or c <= 0:
                return ks, cs, "crash"
            if k > 1.5 * kss and c < css:
                return ks, cs, "overaccumulate"
            ks.append(k)
            cs.append(c)
            if abs(k - kss) / kss < 1e-4 and abs(c - css) / css < 1e-4:
                break
        return ks, cs, "converge" if abs(k - kss) / kss < 0.01 else ("crash" if k < kss else "overaccumulate")

    lo, hi = 1e-6, k0 ** alpha
    for _ in range(80):
        mid = (lo + hi) / 2
        _, _, how = shoot(mid)
        if how == "crash":
            hi = mid
        else:
            lo = mid
    c0 = (lo + hi) / 2
    kp, cp, _ = shoot(c0)
    # forward integration leaves the saddle path eventually; keep the path up to its closest approach
    dist = [abs(k - kss) / kss + abs(c - css) / css for k, c in zip(kp, cp)]
    stop = int(np.argmin(dist)) + 1
    kp, cp = kp[:stop], cp[:stop]
    hi_k, hi_c, _ = shoot(c0 * 1.06)
    lo_k, lo_c, _ = shoot(c0 * 0.94)
    kgrid = np.linspace(0.05 * kss, 2.2 * kss, 200)
    return {"k_ss": kss, "c_ss": css, "k0": k0, "c0": c0, "path_k": kp, "path_c": cp, "dt": dt,
            "high_k": hi_k, "high_c": hi_c, "low_k": lo_k, "low_c": lo_c,
            "kdot0_k": kgrid.tolist(), "kdot0_c": (kgrid ** alpha - (n + g + delta) * kgrid).tolist(),
            "params": {"alpha": alpha, "delta": delta, "rho": rho, "theta": theta, "n": n, "g": g}}
