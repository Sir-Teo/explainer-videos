"""Agora's central bank (Part 31): the market for reserves under a corridor and a floor, balance sheets as T-accounts,
the Island's monetary history with its true shocks known, and four ways to identify a monetary shock (a naive
regression, a recursive VAR, narrative shocks and high-frequency surprises), each scored against the truth; plus the
event-study arithmetic for asset purchases.  numpy and scipy only."""

from __future__ import annotations

import numpy as np
from scipy.stats import norm

from . import rbc


# --- the market for reserves --------------------------------------------------------------------------------------
def reserve_demand(R, floor: float = 0.0, ceiling: float = 2.0, need: float = 50.0, spread: float = 15.0):
    """The overnight rate at which banks will hold reserves ``R``: near the lending (ceiling) rate when reserves are
    scarce, falling to the deposit (floor) rate once banks have more than they need."""
    R = np.asarray(R, float)
    return floor + (ceiling - floor) * norm.sf((R - need) / spread)


def corridor_and_floor(floor: float = 1.0, ceiling: float = 3.0, need: float = 50.0, spread: float = 15.0) -> dict:
    """Two regimes on one demand curve: a corridor (reserves scarce: the rate moves when the central bank adds or
    drains a little) and a floor (reserves abundant: the rate sits at the deposit rate, whatever the quantity)."""
    R = np.linspace(0, 400, 401)
    i = reserve_demand(R, floor, ceiling, need, spread)
    target = (floor + ceiling) / 2
    r_corr = float(need + spread * norm.isf((target - floor) / (ceiling - floor)))
    slope = float((reserve_demand(r_corr + 1, floor, ceiling, need, spread) -
                   reserve_demand(r_corr - 1, floor, ceiling, need, spread)) / 2)
    return {"R": R.tolist(), "i": i.tolist(), "floor": floor, "ceiling": ceiling, "corridor_R": r_corr,
            "corridor_i": target, "slope_per_unit": slope, "floor_R": 300.0,
            "floor_i": float(reserve_demand(300.0, floor, ceiling, need, spread))}


# --- the Island's monetary history -------------------------------------------------------------------------------
DEFAULT = {"a": 0.8, "b": 0.25, "c": 0.08, "rho": 0.7, "phi_pi": 1.5, "phi_y": 0.5, "phi_ns": 1.5, "phi_nd": 1.0,
           "sd_d": 0.5, "sd_s": 0.3, "sd_v": 0.25, "sd_ns": 0.3, "sd_nd": 0.4}


def _p(**kw) -> dict:
    return {**DEFAULT, **kw}


def history(T: int = 240, seed: int = 0, burn: int = 100, **kw) -> dict:
    """A quarterly economy with recursive timing.  Output gap ``y`` and inflation ``pi`` respond to policy with a
    lag; the central bank sets ``i`` after seeing this quarter's ``y`` and ``pi`` and two pieces of private news:
    ``ns`` about next quarter's cost shock and ``nd`` about next quarter's demand shock; ``v`` is the true policy
    shock.

        y_t  = a y_{t-1} - b (i_{t-1} - pi_{t-1}) + nd_{t-1} + e_d
        pi_t = pi_{t-1} + c y_{t-1} + ns_{t-1} + e_s
        i_t  = rho i_{t-1} + (1 - rho)(phi_pi pi_t + phi_y y_t + phi_ns ns_t + phi_nd nd_t) + v_t
    """
    p = _p(**kw)
    rng = np.random.default_rng(seed)
    n = T + burn
    y, pi, i, ns, nd, v = (np.zeros(n) for _ in range(6))
    for t in range(1, n):
        y[t] = p["a"] * y[t - 1] - p["b"] * (i[t - 1] - pi[t - 1]) + nd[t - 1] + p["sd_d"] * rng.standard_normal()
        pi[t] = pi[t - 1] + p["c"] * y[t - 1] + ns[t - 1] + p["sd_s"] * rng.standard_normal()
        ns[t] = p["sd_ns"] * rng.standard_normal()
        nd[t] = p["sd_nd"] * rng.standard_normal()
        v[t] = p["sd_v"] * rng.standard_normal()
        i[t] = (p["rho"] * i[t - 1] + (1 - p["rho"]) * (p["phi_pi"] * pi[t] + p["phi_y"] * y[t] + p["phi_ns"] * ns[t]
                                                         + p["phi_nd"] * nd[t]) + v[t])
    s = slice(burn, n)
    return {k: arr[s].tolist() for k, arr in (("y", y), ("pi", pi), ("i", i), ("ns", ns), ("nd", nd), ("v", v))}


def true_irf(h: int = 20, size: float = 1.0, **kw) -> dict:
    """The true responses of output, inflation, the price level and the policy rate to a policy shock of ``size``
    points (the rule then responds to what follows)."""
    p = _p(**kw)
    y, pi, i = np.zeros(h + 1), np.zeros(h + 1), np.zeros(h + 1)
    for t in range(h + 1):
        if t > 0:
            y[t] = p["a"] * y[t - 1] - p["b"] * (i[t - 1] - pi[t - 1])
            pi[t] = pi[t - 1] + p["c"] * y[t - 1]
        prev = i[t - 1] if t > 0 else 0.0
        i[t] = p["rho"] * prev + (1 - p["rho"]) * (p["phi_pi"] * pi[t] + p["phi_y"] * y[t]) + (size if t == 0 else 0)
    return {"h": list(range(h + 1)), "y": y.tolist(), "pi": pi.tolist(), "i": i.tolist()}


# --- identification ----------------------------------------------------------------------------------------------
def naive(H: dict, h: int = 8) -> float:
    """Regress the change in output over ``h`` quarters on this quarter's change in the policy rate."""
    y, i = np.array(H["y"]), np.array(H["i"])
    di = np.diff(i)[:-h]
    dy = (y[h + 1:] - y[1:-h])
    return float(np.polyfit(di, dy, 1)[0])


def var_cholesky(H: dict, keys=("y", "pi", "i"), p: int = 4, h: int = 20) -> dict:
    """A recursive VAR with the policy rate ordered last; responses to a one-point policy shock."""
    X = np.column_stack([H[k] for k in keys])
    fit = rbc.var_ols(X, p)
    L = np.linalg.cholesky(fit["Sigma"])
    k = list(keys).index("i")
    r = np.array([P @ L[:, k] for P in rbc._ma(fit["A"], h)]) / L[k, k]
    return {"h": list(range(h + 1)), **{key: r[:, j].tolist() for j, key in enumerate(keys)}}


def local_projection(y, shock, h: int = 20, lags: int = 4, controls=()) -> list:
    """The response of ``y`` at each horizon to ``shock``, by regressions of ``y_{t+h}`` on the shock and lags of
    ``y`` (Jorda 2005)."""
    y, shock = np.asarray(y, float), np.asarray(shock, float)
    out = []
    T = len(y)
    for k in range(h + 1):
        rows = range(lags, T - k)
        X = np.column_stack([np.ones(len(rows)), [shock[t] for t in rows]] +
                            [[y[t - j] for t in rows] for j in range(1, lags + 1)] +
                            [[np.asarray(c)[t - 1] for t in rows] for c in controls])
        Y = np.array([y[t + k] for t in rows])
        b, *_ = np.linalg.lstsq(X, Y, rcond=None)
        out.append(float(b[1]))
    return out


def narrative(H: dict, h: int = 20) -> dict:
    """Romer and Romer's idea: the part of the policy rate the central bank's own information cannot explain.  The
    rate is regressed on the bank's information (this quarter's output, inflation and news, last quarter's rate); the
    residual is the shock, and local projections trace its effects."""
    y, pi, i = (np.array(H[k]) for k in ("y", "pi", "i"))
    ns, nd = np.array(H["ns"]), np.array(H["nd"])
    X = np.column_stack([np.ones(len(i) - 1), y[1:], pi[1:], ns[1:], nd[1:], i[:-1]])
    b, *_ = np.linalg.lstsq(X, i[1:], rcond=None)
    shock = np.concatenate([[0.0], i[1:] - X @ b])
    corr = float(np.corrcoef(shock[1:], np.array(H["v"])[1:])[0, 1])
    return {"h": list(range(h + 1)), "y": local_projection(y, shock, h), "pi": local_projection(pi, shock, h),
            "corr_with_truth": corr}


def high_frequency(H: dict, h: int = 20, info: float = 0.6, noise: float = 0.05, seed: int = 1) -> dict:
    """A market surprise on announcement day: the true shock, plus what the announcement reveals of the bank's demand
    news (``info``; the information effect), plus noise.  The surprise instruments the policy rate in local
    projections (first stage: the rate on the surprise)."""
    rng = np.random.default_rng(seed)
    v, nd = np.array(H["v"]), np.array(H["nd"])
    s = v + info * (1 - _p()["rho"]) * _p()["phi_nd"] * nd + noise * rng.standard_normal(len(v))
    i = np.array(H["i"])
    first = float(np.polyfit(s, i, 1)[0])
    resp = {k: [b / first for b in local_projection(np.array(H[k]), s, h)] for k in ("y", "pi")}
    return {"h": list(range(h + 1)), **resp, "first_stage": first, "surprise": s.tolist()}


def peak(path_, sign: float = -1.0) -> dict:
    """The extreme (most negative by default) value of a response and its horizon."""
    a = np.asarray(path_, float) * sign
    k = int(np.argmax(a))
    return {"h": k, "value": float(path_[k])}


# --- asset purchases ----------------------------------------------------------------------------------------------
def event_changes(dates, series: dict, window: int = 1) -> list:
    """Changes in a daily series over ``window`` trading days ending on each event date (from the close before)."""
    days = sorted(series)
    out = []
    for d in dates:
        if d not in series:
            continue
        k = days.index(d)
        out.append({"date": d, "change": float(series[days[k + window - 1]] - series[days[k - 1]])})
    return out


def qe_t_accounts(purchase: float = 100.0) -> dict:
    """Quantitative easing in T-accounts: the central bank buys bonds from banks (or their customers) and pays with
    new reserves; banks swap bonds for reserves; deposits are unchanged if banks sell, and rise if non-banks sell."""
    return {"central_bank": {"assets": {"bonds": purchase}, "liabilities": {"reserves": purchase}},
            "banks_selling": {"assets": {"bonds": -purchase, "reserves": purchase}, "liabilities": {}},
            "nonbanks_selling": {"banks": {"assets": {"reserves": purchase}, "liabilities": {"deposits": purchase}},
                                 "public": {"assets": {"bonds": -purchase, "deposits": purchase}}}}


def naive_irf(H: dict, h: int = 20) -> dict:
    """The naive reading: local projections of output and inflation on this quarter's change in the policy rate,
    with no account of why the rate moved."""
    i = np.array(H["i"])
    di = np.concatenate([[0.0], np.diff(i)])
    first = 1.0
    return {"h": list(range(h + 1)), **{k: [b / first for b in local_projection(np.array(H[k]), di, h, lags=0)]
                                        for k in ("y", "pi")}}


def identification_mc(reps: int = 200, T: int = 240, h: int = 16, seed: int = 0, info: float = 0.6,
                      proxy_noise: float = 0.15) -> dict:
    """Run every method on ``reps`` Island histories of ``T`` quarters, where the true shock is known, and report the
    mean response of output and inflation to a one-point policy shock with a 5-95% band across histories.

    Methods: the naive projection on rate changes; a recursive VAR of output, inflation and the rate (the bank's
    news left out); the same VAR with a noisy commodity-price proxy for the cost news (Sims's fix); narrative shocks
    (the residual of the rate on the bank's own information, as in Romer and Romer); high-frequency surprises with
    and without an information effect."""
    out = {m: {"y": [], "pi": []} for m in ("naive", "var", "var_news", "narrative", "hf_clean", "hf_info")}
    corr = []
    rng = np.random.default_rng(seed + 10_000)
    for r in range(reps):
        H = history(T, seed=seed + r)
        Hp = dict(H, cp=(np.array(H["ns"]) + proxy_noise * rng.standard_normal(T)).tolist())
        res = {"naive": naive_irf(H, h), "var": var_cholesky(H, ("y", "pi", "i"), 4, h),
               "var_news": var_cholesky(Hp, ("y", "pi", "cp", "i"), 4, h)}
        n = narrative(H, h)
        corr.append(n["corr_with_truth"])
        res["narrative"] = n
        res["hf_clean"] = high_frequency(H, h, info=0.0, seed=seed + r + 1)
        res["hf_info"] = high_frequency(H, h, info=info, seed=seed + r + 1)
        for m, v in res.items():
            for k in ("y", "pi"):
                out[m][k].append(v[k][:h + 1])
    tr = true_irf(h)
    summary = {}
    for m, d in out.items():
        summary[m] = {}
        for k in ("y", "pi"):
            a = np.array(d[k])
            summary[m][k] = {"mean": a.mean(0).tolist(), "lo": np.percentile(a, 5, 0).tolist(),
                             "hi": np.percentile(a, 95, 0).tolist()}
    return {"h": list(range(h + 1)), "truth": {"y": tr["y"], "pi": tr["pi"], "i": tr["i"]}, "methods": summary,
            "reps": reps, "T": T, "narrative_corr": float(np.mean(corr))}
