"""Every number in Part 8 (Decisions and Control), computed and cached in .cache/quant8/.

    python -m videos.quant.quant8.compute [items] [--force]

Research window: to December 2020.  Items (seeded; seconds to a few minutes on a CPU):

* ``coin``       Haghani and Dewey's game (2016): $25, a 60% coin at even odds, 300 flips, a $250 cap; final wealth for
                 fixed fractions of 5% to 100%, with the Kelly 20%;
* ``bellman``    Merton's problem by dynamic programming (10 years, monthly, gamma 3), with and without a floor;
                 the value surface and the optimal fraction over (time, wealth);
* ``merton_us``  the US market, monthly 1926-2020 (French): mean excess return, volatility, the Merton fraction for
                 gamma 1 to 10 and its standard error;
* ``kelly_us``   realized log growth of rebalancing to a fixed fraction of the US market (borrowing at the T-bill),
                 1926-2020; the best fraction, its block-bootstrap spread, and a split-sample test of using it;
* ``fractional`` simulated ten-year paths at a half, one and two times Kelly: median, 5th percentile, drawdowns;
* ``samuelson``  Kelly against the gamma-3 Merton fraction: the chance Kelly ends richer, and each strategy's
                 certainty equivalent for the gamma-3 investor, by horizon;
* ``ergodic``    Peters' coin (+50% / -40%): the ensemble average against the typical path;
* ``ltcm``       growth against leverage for a low-volatility convergence trade, before and after its volatility
                 triples (an illustration, labelled as one);
* ``secretary``  the 1/e rule for n = 100, simulated and exact;
* ``american``   the Snell envelope of an American put on a CRR tree: the exercise boundary;
* ``bsde``       a call spread hedged with different borrowing and lending rates: the BSDE by regression against the
                 nonlinear PDE, and the two Black-Scholes prices that bound it;
* ``ppo``        PPO on Merton's problem with log utility, against the closed form;
* ``envelope``   registers the split-sample Kelly test (trial counter).
"""

from __future__ import annotations

import inspect

import numpy as np
from scipy import stats as sst

from explainer.ai.cache import Cache
from explainer.quant import data
from explainer.quant.house import control as C
from explainer.quant.house import pit, trees

CACHE = Cache("quant8")
from explainer.quant.house import pit as _pit  # noqa: E402
load = _pit.counted(CACHE.load, 8)  # the series' trial counter as of this part

MU, R, SIG = 0.08, 0.02, 0.18  # the illustrative market of the Merton, PPO and fractional-Kelly items


def _json(x):
    if isinstance(x, dict):
        return {str(k): _json(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_json(v) for v in x]
    if isinstance(x, np.ndarray):
        return np.where(np.isfinite(x), x, np.nan).tolist() if x.dtype.kind == "f" else x.tolist()
    if isinstance(x, np.generic):
        return x.item()
    return x


def _us_monthly():
    k = data.ken_french_factors_monthly()
    d, x = pit.research(np.asarray(k["date"]) * 100 + 1, np.asarray(k["mkt_rf"]))
    _, rf = pit.research(np.asarray(k["date"]) * 100 + 1, np.asarray(k["rf"]))
    return d // 100, np.asarray(x), np.asarray(rf)


# ---------------------------------------------------------------------------
def compute_coin() -> dict:
    fr = [0.05, 0.1, 0.2, 0.3, 0.4, 0.6, 0.8, 1.0]
    sim = C.kelly_simulation(0.6, fr, n_bets=300, n_paths=20000, seed=8, w0=25.0, cap=250.0)
    out = {}
    for f, w in sim.items():
        out[f"{f:.2f}"] = {"median": float(np.median(w)), "mean": float(np.mean(w)), "p_cap": float(np.mean(w >= 250)),
                           "p_bust": float(np.mean(w < 0.01)), "p_below_25": float(np.mean(w < 25))}
    f = np.linspace(0, 0.99, 199)
    # five sample paths at Kelly and at 60%, same coin
    g = np.random.default_rng(3)
    wins = g.random((5, 300)) < 0.6
    paths = {}
    for frac in (0.2, 0.6):
        w = np.full(5, 25.0)
        rows = [w.copy()]
        for t in range(300):
            w = w + np.where(wins[:, t], 1, -1) * frac * w
            rows.append(w.copy())
        paths[f"{frac:.1f}"] = np.array(rows).T
    return _json({"fractions": fr, "by_fraction": out, "f": f, "growth": C.growth_binary(f, 0.6),
                  "kelly": C.kelly_binary(0.6), "g_kelly": float(C.growth_binary(0.2, 0.6)), "paths": paths})


def compute_bellman() -> dict:
    gamma, T, steps = 3.0, 10.0, 120
    res = {}
    for name, floor in (("merton", 0.0), ("floor", 0.6)):
        o = C.bellman_merton(MU, R, SIG, gamma, T=T, steps=steps, floor=floor, n_w=200, w_max=6.0,
                             pis=np.linspace(0, 1.5, 151))
        wgrid = np.linspace(0.65 if floor else 0.2, 3.0, 60)
        tsel = np.arange(0, steps, 4)
        V, P = [], []
        for n in tsel:
            c = wgrid - o["pv_floor"][n]
            V.append(np.interp(np.log(c), np.log(o["cushion"]), o["V"][n]))
            P.append(np.interp(np.log(c), np.log(o["cushion"]), o["pi"][n]))
        res[name] = {"t": o["t"][tsel], "w": wgrid, "V": np.array(V), "pi": np.array(P),
                     "pi_closed": np.array([C.hara_fraction(wgrid, t, T, MU, R, SIG, gamma, floor) for t in o["t"][tsel]])}
    return _json({"gamma": gamma, "T": T, "mu": MU, "r": R, "sigma": SIG, "pi_merton": C.merton_fraction(MU, R, SIG, gamma),
                  **res})


def compute_merton_us() -> dict:
    d, x, rf = _us_monthly()
    m = 12 * x.mean()
    s = np.sqrt(12) * x.std(ddof=1)
    se_m = s / np.sqrt(len(x) / 12)
    gam = np.arange(1, 11)
    return _json({"n_months": len(x), "excess": m, "sigma": s, "se_excess": se_m, "gammas": gam,
                  "fraction": m / (gam * s ** 2), "fraction_lo": (m - 2 * se_m) / (gam * s ** 2),
                  "fraction_hi": (m + 2 * se_m) / (gam * s ** 2), "rf": 12 * rf.mean()})


def compute_kelly_us() -> dict:
    d, x, rf = _us_monthly()
    f = np.linspace(0, 5, 251)
    g = C.realized_growth(f, x, rf) * 12
    best = float(f[np.nanargmax(np.where(np.isfinite(g), g, -np.inf))])
    # block bootstrap of the best fraction (12-month blocks)
    rng = np.random.default_rng(80)
    n, b = len(x), 12
    starts_all = np.arange(n - b + 1)
    best_bs = []
    for _ in range(400):
        st = rng.choice(starts_all, n // b)
        idx = (st[:, None] + np.arange(b)).ravel()
        gb = C.realized_growth(f, x[idx], rf[idx])
        best_bs.append(f[np.nanargmax(np.where(np.isfinite(gb), gb, -np.inf))])
    best_bs = np.array(best_bs)
    # split sample: choose the fraction on 1926-1972, use it on 1973-2020
    half = int(np.searchsorted(d, 197301))
    g1 = C.realized_growth(f, x[:half], rf[:half])
    f1 = float(f[np.nanargmax(np.where(np.isfinite(g1), g1, -np.inf))])
    g2 = C.realized_growth(f, x[half:], rf[half:]) * 12
    f2 = float(f[np.nanargmax(np.where(np.isfinite(g2), g2, -np.inf))])
    at = lambda arr, v: float(arr[int(np.argmin(abs(f - v)))])  # noqa: E731
    # the worst month, and the leverage at which it would have wiped out the account
    worst = float(x.min())
    worst_date = int(d[np.argmin(x)])
    return _json({"f": f, "growth": g, "best": best, "best_bs": best_bs, "bs_p05": float(np.percentile(best_bs, 5)),
                  "bs_p95": float(np.percentile(best_bs, 95)), "split_f1": f1, "split_f2": f2,
                  "split_g2_at_f1": at(g2, f1), "split_g2_at_half": at(g2, f1 / 2), "split_g2_best": at(g2, f2),
                  "growth_at_1": at(g, 1.0), "growth_at_best": at(g, best), "growth_at_0": at(g, 0.0),
                  "worst_month": worst, "worst_date": worst_date, "ruin_leverage": float(-1 / worst)})


def compute_fractional() -> dict:
    ex, s = MU - R, SIG
    k = ex / s ** 2
    rng = np.random.default_rng(81)
    years, per = 10, 252
    dt = 1 / per
    z = rng.standard_normal((4000, years * per))
    out = {}
    for mult in (0.5, 1.0, 2.0):
        f = mult * k
        lw = np.cumsum((R + f * ex - 0.5 * f ** 2 * s ** 2) * dt + f * s * np.sqrt(dt) * z, axis=1)
        W = np.exp(lw[:, -1])
        peak = np.maximum.accumulate(np.maximum(lw, 0), axis=1)
        dd = 1 - np.exp(np.min(lw - peak, axis=1))
        out[f"{mult:.1f}"] = {"fraction": f, "growth": float(C.growth_continuous(f, ex, s, R)), "vol": f * s,
                              "median": float(np.median(W)), "p05": float(np.percentile(W, 5)),
                              "p95": float(np.percentile(W, 95)), "p_dd50": float(np.mean(dd >= 0.5)),
                              "p_loss": float(np.mean(W < 1))}
        if mult == 1.0:
            sample = np.exp(lw[:20, ::21])
    fm = np.linspace(0, 2.5, 101)
    return _json({"kelly": k, "by_mult": out, "mult": fm, "growth_rel": C.growth_continuous(fm * k, ex, s, 0) /
                  C.growth_continuous(k, ex, s, 0), "paths": sample})


def compute_samuelson() -> dict:
    ex, s, gamma = MU - R, SIG, 3.0
    fk, fm = ex / s ** 2, ex / (gamma * s ** 2)
    T = np.array([1, 2, 5, 10, 20, 30, 50, 100, 200])
    mk, mm = C.growth_continuous(fk, ex, s, R), C.growth_continuous(fm, ex, s, R)
    p_beat = sst.norm.cdf((mk - mm) * np.sqrt(T) / ((fk - fm) * s))
    ce = lambda f: R + f * ex - 0.5 * gamma * f ** 2 * s ** 2  # noqa: E731  (CE growth rate for gamma)
    # Monte Carlo check at T = 30
    rng = np.random.default_rng(82)
    zz = rng.standard_normal(200000) * np.sqrt(30)
    wk = mk * 30 + fk * s * zz
    wm = mm * 30 + fm * s * zz
    return _json({"gamma": gamma, "f_kelly": fk, "f_merton": fm, "T": T, "p_kelly_richer": p_beat,
                  "ce_rate_kelly": ce(fk), "ce_rate_merton": ce(fm), "mc_p30": float(np.mean(wk > wm)),
                  "ce30_kelly": float(np.exp(ce(fk) * 30)), "ce30_merton": float(np.exp(ce(fm) * 30))})


def compute_ergodic() -> dict:
    rng = np.random.default_rng(83)
    n, t = 100000, 60
    up = rng.random((n, t)) < 0.5
    w = np.cumprod(np.where(up, 1.5, 0.6), axis=1)
    w = np.column_stack([np.ones(n), w])
    return _json({"t": np.arange(t + 1), "ensemble": w.mean(axis=0), "median": np.median(w, axis=0),
                  "expected": 1.05 ** np.arange(t + 1), "typical": 0.9 ** (np.arange(t + 1) / 2),
                  "paths": w[:12], "share_below_1": float(np.mean(w[:, -1] < 1)),
                  "share_of_wealth_top1pct": float(np.sort(w[:, -1])[-n // 100:].sum() / w[:, -1].sum())})


def compute_ltcm() -> dict:
    ex, vol = 0.01, 0.01  # an illustrative convergence trade: 1% a year over funding, 1% volatility, unlevered
    L = np.linspace(0, 120, 241)
    g_before = L * ex - 0.5 * L ** 2 * vol ** 2
    g_after = L * ex - 0.5 * L ** 2 * (3 * vol) ** 2
    return _json({"excess": ex, "vol": vol, "L": L, "g_before": g_before, "g_after": g_after,
                  "kelly_before": ex / vol ** 2, "kelly_after": ex / (3 * vol) ** 2, "ltcm_L": 28.0,
                  "g28_before": 28 * ex - 0.5 * 28 ** 2 * vol ** 2, "g28_after": 28 * ex - 0.5 * 28 ** 2 * (3 * vol) ** 2})


def compute_secretary() -> dict:
    n = 100
    k = np.arange(0, 100, 2)
    return _json({"n": n, "k": k, "sim": C.secretary(n, k, trials=20000, seed=84),
                  "exact": [C.secretary_exact(n, int(j)) for j in k], "best_k": int(max(range(1, n),
                                                                                   key=lambda j: C.secretary_exact(n, j))),
                  "best_p": max(C.secretary_exact(n, j) for j in range(1, n))})


def compute_american() -> dict:
    S, K, T, s, r = 100.0, 100.0, 1.0, 0.3, 0.05
    am = trees.crr(S, K, T, s, r, N=500, cp=-1, american=True, boundary=True)
    eu = trees.crr(S, K, T, s, r, N=500, cp=-1)
    return _json({"t": np.linspace(0, T, 501)[:-1], "boundary": am["boundary"], "american": am["price"],
                  "european": eu["price"], "K": K, "T": T, "sigma": s, "r": r})


def compute_bsde() -> dict:
    from explainer.quant.house import bs
    pay = lambda x: np.maximum(x - 95, 0) - 2 * np.maximum(x - 105, 0)  # noqa: E731
    S0, T, s, mu, r, Rb = 100.0, 0.5, 0.2, 0.05, 0.01, 0.06
    bs_r = float(bs.price(S0, 95, T, s, r) - 2 * bs.price(S0, 105, T, s, r))
    bs_R = float(bs.price(S0, 95, T, s, Rb) - 2 * bs.price(S0, 105, T, s, Rb))
    pde = C.hjb_two_rates(pay, S0, T, s, r, Rb, n_s=800)
    runs = {}
    for paths in (5000, 20000, 100000, 300000):
        runs[str(paths)] = [C.bsde_regression(pay, S0, T, s, mu, r, R=Rb, steps=50, paths=paths, hats=20, seed=sd)["Y0"]
                            for sd in range(3)]
        print(f"    bsde {paths}: {np.mean(runs[str(paths)]):.4f}", flush=True)
    # polynomials cannot follow the payoff's kinks: the same scheme with a degree-6 basis is biased low
    poly = float(np.mean([C.bsde_regression(pay, S0, T, s, mu, r, R=Rb, steps=50, paths=100000, deg=6, seed=sd)["Y0"]
                          for sd in range(3)]))
    lin = C.bsde_regression(pay, S0, T, s, mu, r, steps=50, paths=100000, hats=20, seed=9)["Y0"]
    sgrid = np.linspace(60, 140, 81)
    return _json({"bs_r": bs_r, "bs_R": bs_R, "pde": pde, "runs": runs, "linear_bsde": lin, "poly": poly, "S": sgrid,
                  "payoff": pay(sgrid), "params": {"S0": S0, "T": T, "sigma": s, "mu": mu, "r": r, "R": Rb}})


def compute_ppo() -> dict:
    T, steps = 10.0, 40
    out = C.ppo_merton(MU, R, SIG, T=T, steps=steps, iters=300, batch=1024, seed=0, lam=0.0, explore=0.8,
                       snapshots=(0, 10, 25, 50, 100, 200, 299))
    return _json({"mean_fraction": out["mean_fraction"], "snapshots": out["snapshots"], "grid_t": out["grid_t"],
                  "grid_logw": out["grid_logw"], "final_std": out["final_std"],
                  "merton": C.merton_fraction(MU, R, SIG, 1.0),
                  "discrete": C.merton_discrete_optimum(MU, R, SIG, T / steps), "iters": 300, "batch": 1024,
                  "steps": steps, "explore": 0.8})


def compute_envelope() -> dict:
    reg = {"kelly_us_split": pit.register("kelly_us_split", inspect.getsource(compute_kelly_us),
                                          {"choose": "1926-1972", "apply": "1973-2020", "grid": "0..5 step 0.02"},
                                          trials=1)}
    return _json({"registered": reg, "trials": pit.trials_so_far()})



# ---------------------------------------------------------------------------
# The November 2026 expansion: live simulations, labs, replays, and the new chapters
# ---------------------------------------------------------------------------
def compute_coin_live() -> dict:
    """160 players at each of four fractions, flipping the same 60% coin together for 300 flips ($25, $250 cap)."""
    g = np.random.default_rng(88)
    n, flips = 160, 300
    wins = g.random((n, flips)) < 0.6
    out = {}
    for f in (0.1, 0.2, 0.4, 1.0):
        w = np.full(n, 25.0)
        rows = [w.copy()]
        done = np.zeros(n, bool)
        for t in range(flips):
            w = np.where(done, w, w + np.where(wins[:, t], 1, -1) * f * w)
            hit = w >= 250
            w = np.where(hit & ~done, 250.0, w)
            done |= hit
            w = np.where(w < 0.01, 0.0, w)
            done |= w <= 0
            rows.append(w.copy())
        W = np.array(rows).T
        out[f"{f:.1f}"] = {"logw": np.log10(np.maximum(W, 0.01)), "p_cap": float(np.mean(W[:, -1] >= 250)),
                           "p_bust": float(np.mean(W[:, -1] < 0.01)), "median": float(np.median(W[:, -1])),
                           "p_below_start": float(np.mean(W[:, -1] < 25))}
    return _json({"fractions": [0.1, 0.2, 0.4, 1.0], "n": n, "flips": flips, "by_fraction": out})


def compute_utility_check() -> dict:
    """Certainty equivalents of 50-or-150 over gamma, and the Arrow-Pratt premium against the exact one."""
    gam = np.round(np.geomspace(0.5, 30, 61), 4)
    ce = [C.certainty_equivalent([50, 150], [0.5, 0.5], g_) for g_ in gam]
    rows = []
    for g_ in (1.0, 3.0):
        for a in (10.0, 50.0):
            exact = 100 - C.certainty_equivalent([100 - a, 100 + a], [0.5, 0.5], g_)
            rows.append({"gamma": g_, "stake": a, "exact": exact, "approx": C.pratt_premium(100, a, g_)})
    return _json({"gammas": gam, "ce": ce, "premia": rows, "ce_g3": C.certainty_equivalent([50, 150], [0.5, 0.5], 3.0),
                  "ce_g1": C.certainty_equivalent([50, 150], [0.5, 0.5], 1.0)})


def _ev_curve(o, n, w, pis, gamma, nodes=15):
    """E[V_{n+1}] (as a certainty equivalent) for each fraction, at wealth w and step n of a ``bellman_merton`` run."""
    T = o["t"][-1]
    dt = T / (len(o["t"]) - 1)
    z, wq = np.polynomial.hermite_e.hermegauss(nodes)
    wq = wq / wq.sum()
    Rs = np.exp((MU - 0.5 * SIG ** 2) * dt + SIG * np.sqrt(dt) * z) - 1
    gross = 1 + R_RATE * dt + pis[:, None] * (Rs[None, :] - R_RATE * dt)
    c_next = np.maximum(w * gross - o["pv_floor"][n + 1], 1e-9)
    lce = np.interp(np.log(c_next), np.log(o["cushion"]), np.log(C.crra_inv(o["V"][n + 1], gamma)))
    ev = C.crra(np.exp(lce), gamma) @ wq
    return C.crra_inv(ev, gamma)


R_RATE = R


def compute_bellman_sweep() -> dict:
    """The floor problem solved backwards, kept every 6th month for the replay: the policy over wealth, and the
    expected next value against the fraction at wealth 1 (whose peak is the decision)."""
    gamma, T, steps = 3.0, 10.0, 120
    pis = np.linspace(0, 1.5, 151)
    res = {}
    for name, floor in (("merton", 0.0), ("floor", 0.6)):
        o = C.bellman_merton(MU, R, SIG, gamma, T=T, steps=steps, floor=floor, n_w=200, w_max=6.0, pis=pis)
        wgrid = np.linspace(0.65 if floor else 0.2, 3.0, 48)
        sel = np.arange(steps - 6, -1, -6)[::-1]
        P, EV, best = [], [], []
        for n in sel:
            c = wgrid - o["pv_floor"][n]
            P.append(np.interp(np.log(c), np.log(o["cushion"]), o["pi"][n]))
            ev = _ev_curve(o, int(n), 1.0, pis, gamma)
            EV.append(ev)
            best.append(float(pis[int(np.argmax(ev))]))
        res[name] = {"t": o["t"][sel], "w": wgrid, "pi": np.array(P), "ev": np.array(EV), "best_at_1": best,
                     "closed_at_1": [float(C.hara_fraction(1.0, t, T, MU, R, SIG, gamma, floor)) for t in o["t"][sel]]}
    return _json({"pis": pis, "gamma": gamma, "pi_merton": C.merton_fraction(MU, R, SIG, gamma), **res})


def compute_hjb_fd() -> dict:
    """Merton's HJB by implicit finite differences and policy iteration, against the closed form."""
    gamma = 3.0
    o = C.hjb_fd_merton(MU, R, SIG, gamma, T=10.0, n_t=400, n_y=401, y_lim=2.0)
    inner = np.abs(o["y"]) <= 1.5
    rel = np.abs(o["V"] / o["exact"] - 1)
    conv = []
    for n_t, n_y in ((50, 51), (100, 101), (200, 201), (400, 401)):
        q = C.hjb_fd_merton(MU, R, SIG, gamma, T=10.0, n_t=n_t, n_y=n_y, y_lim=2.0)
        m = np.abs(q["y"]) <= 1.5
        conv.append({"n_t": n_t, "n_y": n_y, "rel_err": float(np.max(np.abs(q["V"][m] / q["exact"][m] - 1))),
                     "pi_err": float(np.max(np.abs(q["pi"][m] - C.merton_fraction(MU, R, SIG, gamma))))})
    return _json({"y": o["y"], "pi": o["pi"], "rel_err": float(rel[inner].max()), "passes": o["passes"],
                  "pass_counts": np.bincount(o["passes"]), "pi_merton": C.merton_fraction(MU, R, SIG, gamma),
                  "pi_err": float(np.max(np.abs(o["pi"][inner] - C.merton_fraction(MU, R, SIG, gamma)))),
                  "convergence": conv, "gamma": gamma, "n_t": 400, "n_y": 401,
                  "f0": float(C.merton_value_factor(MU, R, SIG, gamma, 10.0))})


def compute_viscosity() -> dict:
    """u_t + |u_x| = 1 marched to steady state by a monotone (upwind) and a non-monotone (central) scheme."""
    times = (0.1, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0)
    out = {"grids": {}}
    for n in (21, 81, 321):
        row = {}
        for sc in ("upwind", "central"):
            e = C.eikonal_march(n, sc, t_end=6.0, snapshots=times)
            err = np.abs(e["u"] - (1 - np.abs(e["x"])))
            row[sc] = float(np.nanmax(np.where(np.isfinite(err), err, np.inf)))
            if n == 81:
                out[f"{sc}_snaps"] = np.array([np.clip(np.nan_to_num(e["snaps"][t], nan=1e3, posinf=1e3, neginf=-1e3),
                                                       -1e3, 1e3) for t in times])
                out["x"] = e["x"]
        out["grids"][str(n)] = row
    out["times"] = list(times)
    return _json(out)


def compute_rebalance_sim() -> dict:
    """Constant mix (Merton, rebalanced monthly) against buy-and-hold from the same start, 30 years, for gamma 3;
    and one path for the picture."""
    gamma = 3.0
    pi = C.merton_fraction(MU, R, SIG, gamma)
    g = np.random.default_rng(85)
    n, years, per = 20000, 30, 12
    dt = 1 / per
    z = g.standard_normal((n, years * per))
    R_ = np.exp((MU - 0.5 * SIG ** 2) * dt + SIG * np.sqrt(dt) * z)
    Rf = np.exp(R * dt)
    lw_mix = np.sum(np.log(pi * R_ + (1 - pi) * Rf), axis=1)
    stock = pi * np.prod(R_, axis=1)
    bond = (1 - pi) * Rf ** (years * per)
    w_bh = stock + bond

    def ce_rate(W):
        return float(np.log(np.mean(W ** (1 - gamma)) ** (1 / (1 - gamma))) / years)

    W_mix = np.exp(lw_mix)
    bh_frac_end = stock / w_bh
    # one five-year path, monthly: the mix before rebalancing, and buy-and-hold's drifting fraction
    zz = g.standard_normal(60)
    Rp = np.exp((MU - 0.5 * SIG ** 2) * dt + SIG * np.sqrt(dt) * zz)
    pre, bh, price = [], [pi], [1.0]
    s_bh, b_bh = pi, 1 - pi
    for r_ in Rp:
        G = pi * r_ + (1 - pi) * Rf
        pre.append(pi * r_ / G)
        s_bh, b_bh = s_bh * r_, b_bh * Rf
        bh.append(s_bh / (s_bh + b_bh))
        price.append(price[-1] * r_)
    se = lambda W: float(np.std(np.log(W)) / np.sqrt(n) / years)  # noqa: E731
    return _json({"pi": pi, "gamma": gamma, "ce_mix": ce_rate(W_mix), "ce_bh": ce_rate(w_bh),
                  "median_mix": float(np.median(W_mix)), "median_bh": float(np.median(w_bh)),
                  "bh_frac_p10": float(np.percentile(bh_frac_end, 10)), "bh_frac_p90": float(np.percentile(bh_frac_end, 90)),
                  "path_price": price, "path_pre": pre, "path_bh": bh, "n": n, "years": years, "se": se(W_mix)})


def compute_consumption() -> dict:
    """Merton (1971): the consumption rate by gamma, by patience, and over a 40-year life."""
    rho = 0.03
    gam = [1.0, 2.0, 3.0, 5.0, 10.0]
    nu = [C.merton_consumption_rate(rho, MU, R, SIG, g_) for g_ in gam]
    tau = np.linspace(40, 0.25, 160)
    life = C.merton_consumption_rate(rho, MU, R, SIG, 3.0, tau=tau)
    return _json({"rho": rho, "gammas": gam, "nu": nu, "nu_patient": C.merton_consumption_rate(0.01, MU, R, SIG, 3.0),
                  "t": 40 - tau, "life": life, "life_t0": float(life[0]), "life_last_year": float(
                      C.merton_consumption_rate(rho, MU, R, SIG, 3.0, tau=1.0)), "theta": (MU - R) / SIG})


def compute_martingale_check() -> dict:
    """Constant-mix paths rebalanced daily for 10 years land on the power claim X_T = c xi_T^(-1/gamma)."""
    gamma, T, per, n = 3.0, 10.0, 252, 2000
    theta = (MU - R) / SIG
    pi = C.merton_fraction(MU, R, SIG, gamma)
    g = np.random.default_rng(86)
    dt = 1 / per
    lx = np.zeros(n)
    W = np.zeros(n)
    for _ in range(int(T * per)):
        dW = g.standard_normal(n) * np.sqrt(dt)
        Rs = np.exp((MU - 0.5 * SIG ** 2) * dt + SIG * dW) - 1
        rf = np.exp(R * dt) - 1
        lx += np.log(1 + rf + pi * (Rs - rf))
        W += dW
    xi = np.exp(-(R + theta ** 2 / 2) * T - theta * W)
    XT = np.exp(lx)
    # the static solution: X_T = c xi^(-1/gamma), c from the budget E[xi X_T] = 1 (closed form)
    c = 1 / np.exp((1 - 1 / gamma) * (-(R + theta ** 2 / 2) * T) + 0.5 * (1 - 1 / gamma) ** 2 * theta ** 2 * T)
    formula = c * xi ** (-1 / gamma)
    rel = np.abs(XT / formula - 1)
    curves = {}
    xs = np.geomspace(np.percentile(xi, 0.5), np.percentile(xi, 99.5), 80)
    for g_ in (1.5, 3.0, 6.0):
        cg = 1 / np.exp((1 - 1 / g_) * (-(R + theta ** 2 / 2) * T) + 0.5 * (1 - 1 / g_) ** 2 * theta ** 2 * T)
        curves[f"{g_:g}"] = cg * xs ** (-1 / g_)
    return _json({"xi": xi, "XT": XT, "max_rel": float(rel.max()), "median_rel": float(np.median(rel)),
                  "budget": float(np.mean(xi * XT)), "xs": xs, "curves": curves, "gamma": gamma, "T": T,
                  "pi": pi, "theta": theta})


def compute_davis_norman() -> dict:
    """The no-trade band by dynamic programming (gamma 3, monthly, 30 years; and gamma 1, quarterly, 10 years),
    against the small-cost asymptotics; a wealth dot reflected at the band's edges; and the band's payoff net of
    costs against rebalancing to Merton every quarter."""
    gamma = 3.0
    rows = []
    for eps in (0.001, 0.005, 0.01, 0.02):
        b = C.no_trade_band(MU, R, SIG, gamma, eps, 1 / 12, 360)
        rows.append({"eps": eps, "lo": b["lo"], "hi": b["hi"], "half": 0.5 * (b["hi"] - b["lo"]),
                     "asym": C.band_halfwidth_asymptotic(MU, R, SIG, gamma, eps)})
    eps_grid = np.geomspace(0.0005, 0.03, 40)
    asym = [C.band_halfwidth_asymptotic(MU, R, SIG, gamma, e) for e in eps_grid]
    one = C.no_trade_band(MU, R, SIG, 1.0, 0.01, 0.25, 40, grid=np.linspace(0, 3.5, 701), nodes=21)
    lo1, hi1 = one["lo"], one["hi"]
    pm1 = C.merton_fraction(MU, R, SIG, 1.0)
    band = C.simulate_rebalance(lambda n, p: np.clip(p, lo1, hi1), MU, R, SIG, 0.01, 10.0, 40, seed=87)
    merton = C.simulate_rebalance(lambda n, p: np.full_like(p, pm1), MU, R, SIG, 0.01, 10.0, 40, seed=87)
    free = C.simulate_rebalance(lambda n, p: np.full_like(p, pm1), MU, R, SIG, 0.0, 10.0, 40, seed=87)
    # the wedge picture: gamma 3, eps 1%, weekly steps for 15 years; bond x and stock y in dollars
    lo3, hi3 = rows[2]["lo"], rows[2]["hi"]
    pm3 = C.merton_fraction(MU, R, SIG, gamma)
    g = np.random.default_rng(89)
    dt, n = 1 / 52, 52 * 15
    x, y = (1 - pm3), pm3
    xr, yr = (1 - pm3), pm3
    pts, trades, turn_band, turn_ray = [(x, y)], [], 0.0, 0.0
    for k in range(n):
        Rk = np.exp((MU - 0.5 * SIG ** 2) * dt + SIG * np.sqrt(dt) * g.standard_normal())
        x, y = x * np.exp(R * dt), y * Rk
        p = y / (x + y)
        if p > hi3 or p < lo3:
            tgt = hi3 if p > hi3 else lo3
            # trade to the edge, paying eps on the amount traded
            wv = x + y
            dy = (tgt * wv - y) / (1 + 0.01 * tgt * np.sign(tgt * wv - y))
            y += dy
            x -= dy + 0.01 * abs(dy)
            turn_band += abs(dy) / wv
            trades.append(k + 1)
        xr, yr = xr * np.exp(R * dt), yr * Rk
        wr = xr + yr
        turn_ray += abs(pm3 * wr - yr) / wr
        yr, xr = pm3 * wr, (1 - pm3) * wr
        pts.append((x, y))
    return _json({"gamma": gamma, "rows": rows, "eps_grid": eps_grid, "asym": asym, "pi_merton": pm3,
                  "g1": {"lo": lo1, "hi": hi1, "pi_merton": pm1, "band": band, "merton": merton, "free": free,
                         "gain": band["growth"] - merton["growth"]},
                  "wedge": {"lo": lo3, "hi": hi3, "path": np.array(pts), "trades": trades, "years": 15,
                            "turn_band": turn_band / 15, "turn_ray": turn_ray / 15}})


def compute_kelly_live() -> dict:
    """Three fans of 60 paths, at a half, one and two times Kelly, monthly for 40 years (log10 wealth)."""
    ex = MU - R
    k = ex / SIG ** 2
    g = np.random.default_rng(90)
    years, per = 40, 12
    dt = 1 / per
    z = g.standard_normal((60, years * per))
    out = {}
    for mult in (0.5, 1.0, 2.0):
        f = mult * k
        lw = np.cumsum((R + f * ex - 0.5 * f ** 2 * SIG ** 2) * dt + f * SIG * np.sqrt(dt) * z, axis=1)
        lw = np.column_stack([np.zeros(60), lw]) / np.log(10)
        out[f"{mult:.1f}"] = {"paths": lw, "median": np.median(lw, axis=0),
                              "g": float(C.growth_continuous(f, ex, SIG, R)), "f": f}
    return _json({"kelly": k, "t": np.arange(years * per + 1) / per, "fans": out, "r": R})


def compute_breiman_race() -> dict:
    """Kelly against half and twice Kelly on the same 10,000 markets: the chance Kelly is ahead, by year."""
    ex = MU - R
    k = ex / SIG ** 2
    g = np.random.default_rng(91)
    years, per, n = 100, 12, 10000
    dt = 1 / per
    W = np.zeros(n)
    lk = np.zeros(n)
    lh = np.zeros(n)
    l2 = np.zeros(n)
    ahead_h, ahead_2 = [], []
    for m in range(years * per):
        dW = g.standard_normal(n) * np.sqrt(dt)
        for arr, f in ((lk, k), (lh, 0.5 * k), (l2, 2 * k)):
            arr += (R + f * ex - 0.5 * f ** 2 * SIG ** 2) * dt + f * SIG * dW
        if (m + 1) % per == 0:
            ahead_h.append(float(np.mean(lk > lh)))
            ahead_2.append(float(np.mean(lk > l2)))
    T = np.arange(1, years + 1)

    def closed(c):
        dg = 0.5 * (ex / SIG) ** 2 * (1 - (2 * c - c ** 2))
        return sst.norm.cdf(dg * np.sqrt(T) / (abs(1 - c) * k * SIG))

    return _json({"years": T, "vs_half": ahead_h, "vs_double": ahead_2, "closed_half": closed(0.5),
                  "closed_double": closed(2.0), "kelly": k})


def compute_edge_error() -> dict:
    """Full and half Kelly when the edge is overestimated by a factor k (closed form, and 2,000 thirty-year paths)."""
    ex = MU - R
    k = ex / SIG ** 2
    ks = np.linspace(0.5, 4.5, 81)
    full = ks * (2 - ks)
    half = 0.5 * ks * (2 - 0.5 * ks)
    g = np.random.default_rng(92)
    mc = []
    years, n = 30, 2000
    z = g.standard_normal((n, years))
    for kk in (1.0, 2.0, 3.0):
        row = {"k": kk}
        for c in (1.0, 0.5):
            f = c * kk * k
            lw = np.sum((R + f * ex - 0.5 * f ** 2 * SIG ** 2) + f * SIG * z, axis=1)
            row[f"c{c:g}"] = float((np.mean(lw) / years - R) / (0.5 * ex ** 2 / SIG ** 2))
        mc.append(row)
    return _json({"ks": ks, "full": full, "half": half, "mc": mc})


def compute_ergodic_live() -> dict:
    """Peters' coin, 100,000 players: the histogram of log10 wealth after every flip."""
    g = np.random.default_rng(83)
    n, t = 100000, 60
    w = np.zeros(n)
    bins = np.linspace(-6, 6, 49)
    H, mean, med = [], [0.0], [0.0]
    H.append(np.histogram(w, bins=bins)[0] / n)
    for _ in range(t):
        w += np.where(g.random(n) < 0.5, np.log10(1.5), np.log10(0.6))
        H.append(np.histogram(np.clip(w, -5.99, 5.99), bins=bins)[0] / n)
        mean.append(float(np.log10(np.mean(10 ** w))))
        med.append(float(np.median(w)))
    return _json({"bins": bins, "hist": np.array(H), "log_mean": mean, "log_median": med,
                  "expected": np.arange(t + 1) * np.log10(1.05), "kelly_stake": 0.25,
                  "kelly_growth": float(0.5 * np.log(1 + 0.25 * 0.5) + 0.5 * np.log(1 - 0.25 * 0.4))})


SNELL_G = np.array([0, 2, 5, 3, 1, 4, 8, 6, 3, 2, 3, 5, 9, 7, 6, 4, 2, 3, 6, 4, 0], float)


def compute_snell_rw() -> dict:
    """The Snell envelope of a skyline of pegs under a symmetric random walk, by value iteration, against the least
    concave majorant."""
    o = C.snell_envelope(SNELL_G, tol=1e-14, every=1)
    hist = np.array(o["history"])
    keep = sorted(set(np.unique(np.round(np.geomspace(1, len(hist) - 1, 40)).astype(int)).tolist() + [0, len(hist) - 1]))
    maj = C.concave_majorant(SNELL_G)
    stop = np.isclose(o["U"], SNELL_G, atol=1e-9)
    return _json({"g": SNELL_G, "U": o["U"], "sweeps": o["sweeps"], "history": hist[keep], "history_sweeps": keep,
                  "majorant": maj, "max_gap": float(np.max(np.abs(o["U"] - maj))), "stop": stop.astype(int),
                  "U0_mid": float(o["U"][10])})


def compute_perpetual_put() -> dict:
    """McKean's perpetual put by smooth fit, against a 40-year CRR tree; the value of each exercise level."""
    K, r, s = 100.0, 0.05, 0.3
    pp = C.perpetual_put(K, r, s)
    bs_ = np.linspace(30, 95, 131)
    vals = [float(C.perpetual_put_value(100.0, K, r, s, b)) for b in bs_]
    tree = trees.crr(100.0, K, 40.0, s, r, N=4000, cp=-1, american=True, boundary=True)
    bnd = np.asarray(tree["boundary"])
    S = np.linspace(20, 200, 181)
    return _json({"K": K, "r": r, "sigma": s, "beta": pp["beta"], "b_star": pp["b"],
                  "v100": float(C.perpetual_put_value(100.0, K, r, s, pp["b"])), "b_grid": bs_, "v_of_b": vals,
                  "tree_price": float(tree["price"]), "tree_boundary0": float(np.nanmean(bnd[:40])),
                  "S": S, "V": C.perpetual_put_value(S, K, r, s, pp["b"]),
                  "b_star_r7": C.perpetual_put(K, 0.07, s)["b"], "b_star_r3": C.perpetual_put(K, 0.03, s)["b"]})


def _us_monthly_total():
    d, x, rf = _us_monthly()
    return d, x + rf, rf


def compute_myopic_loss() -> dict:
    """Benartzi and Thaler (1995) redone: the prospect-theory value of stocks and of T-bills, evaluated every h
    months (overlapping windows of US history, 1926-2020, TK 1992 parameters)."""
    d, m, rf = _us_monthly_total()
    lm, lb = np.log1p(m), np.log1p(rf)
    cs, cb = np.concatenate([[0], np.cumsum(lm)]), np.concatenate([[0], np.cumsum(lb)])
    H = np.arange(1, 37)
    vs, vb = [], []
    for h in H:
        vs.append(C.cpt_value(np.exp(cs[h:] - cs[:-h]) - 1))
        vb.append(C.cpt_value(np.exp(cb[h:] - cb[:-h]) - 1))
    vs, vb = np.array(vs), np.array(vb)
    above = np.where(vs > vb)[0]
    cross = int(H[above[0]]) if len(above) else None
    # the reference curves for the picture: stock returns over 1 and 24 months
    ret1 = np.exp(cs[1:] - cs[:-1]) - 1
    ret24 = np.exp(cs[24:] - cs[:-24]) - 1
    reg = pit.register("myopic_loss_aversion_us", inspect.getsource(compute_myopic_loss),
                       {"data": "French monthly 1926-2020", "cpt": "TK 1992", "horizons": "1..36"}, trials=1)
    return _json({"h": H, "stocks": vs, "bills": vb, "crossover": cross, "ret1": ret1, "ret24": ret24,
                  "registered": reg})


def compute_robust_fraction() -> dict:
    """Maenhout's robust Merton fraction with theta set by detection-error probabilities on 94 years of data."""
    m = load("merton_us")
    ex, s, years, gamma = m["excess"], m["sigma"], m["n_months"] / 12, 3.0
    rows = []
    for p in (0.3, 0.2, 0.1, 0.05):
        th = C.theta_for_detection(p, ex + R, R, s, gamma, years)
        rows.append({"p": p, "theta": th, "pi": float(C.robust_fraction(ex + R, R, s, gamma, th)),
                     "drift_cut": float(th * ex / (gamma + th))})
    thetas = np.linspace(0, 8, 81)
    pis = C.robust_fraction(ex + R, R, s, gamma, thetas)
    det = [C.detection_error(t * ex / (gamma + t), s, years) for t in thetas]
    return _json({"rows": rows, "thetas": thetas, "pis": pis, "detect": det, "excess": ex, "sigma": s,
                  "years": years, "gamma": gamma, "pi_plain": float(ex / (gamma * s ** 2))})


def compute_mfg_crowd() -> dict:
    """The liquidation game: fictitious play for N = 2, 10 and the mean field, against the closed form; and a crowd
    of 500 traders with different inventories, each best-responding to the mean field."""
    kappa, eta, T = 4.0, 1.0, 1.0  # kappa T/(2 eta) = 2
    out = {"kappa": kappa, "eta": eta, "T": T, "runs": {}}
    t = None
    for N in (1, 2, 10, np.inf):
        o = C.mfg_liquidation(N, kappa, eta, T=T, n=1000, iters=500, damping=0.5)
        t = o["t"]
        cl = C.liquidation_closed(N, kappa, eta, T, t)
        k = int(round(len(t) / 5))
        key = "inf" if not np.isfinite(N) else str(N)
        out["runs"][key] = {"Q": o["Q"][::25, 0], "closed": cl[::25], "residual": o["residual"],
                            "share_fifth": float(1 - o["Q"][k, 0]), "share_fifth_closed": float(1 - cl[k]),
                            "gap": float(np.max(np.abs(o["Q"][:, 0] - cl))), "iters": len(o["residual"])}
    out["t"] = t[::25]
    # fictitious play replay (mean field): the crowd's rate after each iteration
    reps, m = [], np.zeros(1001)
    from scipy.linalg import solve_banded  # noqa: F401  (same scheme as the House function, iterate by iterate)
    for it in range(12):
        o = C.mfg_liquidation(np.inf, kappa, eta, T=T, n=1000, iters=it + 1, damping=0.5, tol=0)
        reps.append({"m": o["m"][::25], "Q": o["Q"][::25, 0]})
    out["replay"] = reps
    g = np.random.default_rng(93)
    q0 = g.uniform(0.5, 1.5, 500)
    o = C.mfg_liquidation(np.inf, kappa, eta, T=T, n=200, iters=500, damping=0.5, q0=q0)
    out["crowd"] = {"t": o["t"][::10], "Q": o["Q"][::10], "q0": q0}
    return _json(out)


def _ppo_seed(seed):
    T, steps = 10.0, 40
    o = C.ppo_merton(MU, R, SIG, T=T, steps=steps, iters=300, batch=1024, seed=seed, lam=0.0, explore=0.8,
                     snapshots=(0, 10, 25, 50, 100, 200, 299))
    return {"mean_fraction": o["mean_fraction"], "snapshots": o["snapshots"], "final_std": o["final_std"]}


def compute_ppo_s1() -> dict:
    return _json(_ppo_seed(1))


def compute_ppo_s2() -> dict:
    return _json(_ppo_seed(2))


def compute_ppo_s3() -> dict:
    return _json(_ppo_seed(3))


def compute_ppo_s4() -> dict:
    return _json(_ppo_seed(4))


def compute_ppo_seeds() -> dict:
    """PPO on Merton (log utility), five seeds: seed 0 is the ``ppo`` item; the spread, and each seed's final policy
    scored by its growth shortfall against the discrete-time optimum."""
    base = load("ppo")
    runs = [np.asarray(base["mean_fraction"])] + [np.asarray(load(f"ppo_s{k}")["mean_fraction"]) for k in range(1, 5)]
    snaps = [base["snapshots"]] + [load(f"ppo_s{k}")["snapshots"] for k in range(1, 5)]
    opt = base["discrete"]
    finals = [float(np.mean(np.asarray(s_[list(s_.keys())[-1]]))) for s_ in snaps]
    short = [float(C.growth_continuous(opt, MU - R, SIG, R) - C.growth_continuous(f, MU - R, SIG, R)) for f in finals]
    ck = [int(k) for k in base["snapshots"].keys()]
    return _json({"runs": np.array(runs), "finals": finals, "shortfall": short, "discrete": opt,
                  "merton": base["merton"], "checkpoints": ck,
                  "snap_mean": [[float(np.mean(np.asarray(s_[str(c)] if str(c) in s_ else s_[c]))) for c in ck]
                                for s_ in snaps]})


EPS_RL = 0.01


def _ppo_cost_seed(seed):
    o = C.ppo_rebalance(MU, R, SIG, EPS_RL, T=10.0, steps=40, iters=300, batch=1024, seed=seed, explore=0.3)
    pol = o["policy"]
    ev = C.simulate_rebalance(lambda n, p: pol(n / 40, p), MU, R, SIG, EPS_RL, 10.0, 40, seed=94)
    return {"mean_target": o["mean_target"], "snapshots": o["snapshots"], "grid_p": o["grid_p"], "final": o["final"],
            "eval": ev}


def compute_ppo_cost_s0() -> dict:
    return _json(_ppo_cost_seed(0))


def compute_ppo_cost_s1() -> dict:
    return _json(_ppo_cost_seed(1))


def compute_ppo_cost_s2() -> dict:
    return _json(_ppo_cost_seed(2))


def compute_ppo_cost_s3() -> dict:
    return _json(_ppo_cost_seed(3))


def compute_ppo_cost_s4() -> dict:
    return _json(_ppo_cost_seed(4))


def compute_ppo_costs() -> dict:
    """PPO with a 1% trading cost, five seeds, against the dynamic-programming band and quarterly rebalancing to
    Merton, all scored on the same 200,000 simulated markets."""
    dn = load("davis_norman")["g1"]
    lo, hi, pm = dn["lo"], dn["hi"], dn["pi_merton"]
    band = C.simulate_rebalance(lambda n, p: np.clip(p, lo, hi), MU, R, SIG, EPS_RL, 10.0, 40, seed=94)
    merton = C.simulate_rebalance(lambda n, p: np.full_like(p, pm), MU, R, SIG, EPS_RL, 10.0, 40, seed=94)
    hold = C.simulate_rebalance(lambda n, p: p, MU, R, SIG, EPS_RL, 10.0, 40, seed=94)
    seeds = [load(f"ppo_cost_s{k}") for k in range(5)]
    gp = np.asarray(seeds[0]["grid_p"])
    edges = []
    for s_ in seeds:
        fin = np.asarray(s_["final"])
        still = np.abs(fin - gp) < 0.02
        edges.append([float(gp[still].min()), float(gp[still].max())] if still.any() else [None, None])
    ev = [s_["eval"] for s_ in seeds]
    return _json({"band": band, "merton": merton, "hold": hold, "lo": lo, "hi": hi, "pi_merton": pm,
                  "seeds": ev, "edges": edges, "grid_p": gp, "finals": [s_["final"] for s_ in seeds],
                  "runs": np.array([s_["mean_target"] for s_ in seeds]),
                  "snapshots": seeds[0]["snapshots"], "ppo_growth": [e["growth"] for e in ev],
                  "ppo_turnover": [e["turnover"] for e in ev]})


def compute_drawdown_policy() -> dict:
    """Kelly against Grossman-Zhou (never below 80% of the running peak), 2,000 thirty-year paths, weekly."""
    ex = MU - R
    pk = ex / SIG ** 2
    alpha = 0.8
    g = np.random.default_rng(95)
    n, years, per = 2000, 30, 52
    dt = 1 / per
    wk, wg = np.ones(n), np.ones(n)
    mk, mg = np.ones(n), np.ones(n)
    worst_k, worst_g = np.ones(n), np.ones(n)
    sample_k, sample_g, sample_m = [], [], []
    for s in range(years * per):
        z = g.standard_normal(n)
        Rs = np.exp((MU - 0.5 * SIG ** 2) * dt + SIG * np.sqrt(dt) * z) - 1
        rf = np.exp(R * dt) - 1
        wk = wk * np.maximum(1 + rf + pk * (Rs - rf), 1e-12)
        f = C.grossman_zhou_fraction(wg, mg, alpha, pk)
        wg = wg * np.maximum(1 + rf + f * (Rs - rf), 1e-12)
        mk, mg = np.maximum(mk, wk), np.maximum(mg, wg)
        worst_k, worst_g = np.minimum(worst_k, wk / mk), np.minimum(worst_g, wg / mg)
        if s % 4 == 0:
            sample_k.append(wk[:3].copy()), sample_g.append(wg[:3].copy()), sample_m.append(mg[:3].copy())
    return _json({"alpha": alpha, "kelly": pk, "median_growth_kelly": float(np.median(np.log(wk)) / years),
                  "median_growth_gz": float(np.median(np.log(wg)) / years),
                  "worst_dd_kelly": float(1 - worst_k.min()), "worst_dd_gz": float(1 - worst_g.min()),
                  "p_dd20_kelly": float(np.mean(worst_k < alpha)), "p_dd20_gz": float(np.mean(worst_g < alpha - 1e-9)),
                  "sample_k": np.log10(np.array(sample_k)).T, "sample_g": np.log10(np.array(sample_g)).T,
                  "sample_m": np.log10(np.array(sample_m)).T, "years": years})


def compute_vol_target() -> dict:
    """Volatility targeting on US history (Moreira and Muir 2017's test, redone): each month hold c/sigma_hat^2 of
    the market, sigma_hat from the previous month's daily returns, c chosen so the average exposure is 1, against
    holding the market.  Registered with the trial counter."""
    k = data.ken_french_daily(through="2020-12-31")
    d = np.asarray(k["date"])
    x = np.asarray(k["mkt_rf"])
    rf = np.asarray(k["rf"])
    month = d // 100
    ms = np.unique(month)
    rv, ret, rfm = [], [], []
    for m_ in ms:
        sel = month == m_
        rv.append(np.sum(x[sel] ** 2) * 21 / sel.sum())
        ret.append(np.prod(1 + x[sel] + rf[sel]) - np.prod(1 + rf[sel]))
        rfm.append(np.prod(1 + rf[sel]) - 1)
    rv, ret, rfm = np.array(rv), np.array(ret), np.array(rfm)
    w = 1 / rv[:-1]
    w = w / w.mean()
    ex_scaled = w * ret[1:]
    ex_mkt = ret[1:]
    sr = lambda e: float(np.mean(e) / np.std(e) * np.sqrt(12))  # noqa: E731
    gr = lambda e, f: float(np.mean(np.log1p(e + f)) * 12)  # noqa: E731
    # the alpha of the scaled portfolio on the market (Moreira and Muir's test), with its t-statistic
    X = np.column_stack([np.ones(len(ex_mkt)), ex_mkt])
    b, *_ = np.linalg.lstsq(X, ex_scaled, rcond=None)
    resid = ex_scaled - X @ b
    cov = np.linalg.inv(X.T @ X) * resid.var(ddof=2)
    reg = pit.register("vol_target_us_market", inspect.getsource(compute_vol_target),
                       {"data": "French daily 1926-2020", "window": "previous month", "rebalance": "monthly"}, trials=1)
    return _json({"sr_mkt": sr(ex_mkt), "sr_scaled": sr(ex_scaled), "growth_mkt": gr(ex_mkt, rfm[1:]),
                  "growth_scaled": gr(ex_scaled, rfm[1:]), "alpha": float(b[0] * 12),
                  "alpha_t": float(b[0] / np.sqrt(cov[0, 0])), "beta": float(b[1]), "max_w": float(w.max()),
                  "min_w": float(w.min()), "months": int(len(ex_mkt)), "w": w, "dates": ms[1:],
                  "registered": reg})


def compute_bsde_replay() -> dict:
    """The two-rate BSDE by regression, kept every 5th step for the replay: a sample of (S_n, Y_{n+1}) and the fitted
    E[Y_{n+1} | S_n] and Y_n on a grid of spots."""
    from explainer.quant.house import bs
    pay = lambda x: np.maximum(x - 95, 0) - 2 * np.maximum(x - 105, 0)  # noqa: E731
    S0, T, s, mu, r, Rb = 100.0, 0.5, 0.2, 0.05, 0.01, 0.06
    steps, paths, hats = 50, 20000, 20
    g = np.random.default_rng(96)
    dt = T / steps
    dW = g.standard_normal((paths, steps)) * np.sqrt(dt)
    logS = np.log(S0) + np.cumsum((mu - 0.5 * s ** 2) * dt + s * dW, axis=1)
    S = np.column_stack([np.full(paths, S0), np.exp(logS)])
    theta = (mu - r) / s
    Y = pay(S[:, -1])
    grid = np.linspace(75, 125, 101)
    frames = []
    sub = g.choice(paths, 300, replace=False)
    for n in range(steps - 1, -1, -1):
        x = (S[:, n] - S0) / S0
        if n == 0:
            Zn = np.full(paths, np.mean(Y * dW[:, n]) / dt)
            EY = np.full(paths, Y.mean())
            ey_grid = np.full(len(grid), Y.mean())
        else:
            knots = np.quantile(x, np.linspace(0.001, 0.999, hats))
            B = C._basis(x, 6, knots)
            cz, *_ = np.linalg.lstsq(B, Y * dW[:, n] / dt, rcond=None)
            cy, *_ = np.linalg.lstsq(B, Y, rcond=None)
            Zn, EY = B @ cz, B @ cy
            ey_grid = C._basis((grid - S0) / S0, 6, knots) @ cy
        f = -r * EY - theta * Zn - (Rb - r) * np.minimum(EY - Zn / s, 0.0)
        if n % 5 == 0 or n == steps - 1:
            frames.append({"n": n, "S": S[sub, n], "Ynext": Y[sub], "fit": ey_grid})
        Y = EY + f * dt
    bs_r = float(bs.price(S0, 95, T, s, r) - 2 * bs.price(S0, 105, T, s, r))
    bs_R = float(bs.price(S0, 95, T, s, Rb) - 2 * bs.price(S0, 105, T, s, Rb))
    fan = S[g.choice(paths, 40, replace=False)][:, ::2]
    return _json({"frames": frames, "grid": grid, "Y0": float(Y.mean()), "bs_r": bs_r, "bs_R": bs_R,
                  "fan": fan, "t": np.linspace(0, T, steps + 1)[::2], "payoff": pay(grid)})

def compute_estrisk_theory() -> dict:
    """The research chapter: estimation risk in Merton's and Kelly's rule.  With an estimated mean, the plug-in
    fraction's expected certainty equivalent is (theta^2 - 1/T)/(2 gamma) a year; scaling it by c gives
    (c theta^2 - c^2 (theta^2 + 1/T)/2)/gamma, maximised at c* = T theta^2/(T theta^2 + 1) (Kan and Zhou 2007, one
    asset).  Checked by simulation with both moments estimated from monthly data, then run on the US market with an
    expanding window from 1936."""
    theta, sig = 0.4, 0.18
    Ts = np.arange(1, 101)
    ce = lambda c, T, g: (c * theta ** 2 - c ** 2 * (theta ** 2 + 1 / T) / 2) / g  # noqa: E731
    cstar = Ts * theta ** 2 / (Ts * theta ** 2 + 1)
    out = {"theta": theta, "sigma": sig, "T": Ts, "ce_max": theta ** 2 / 2,
           "theory": {"plug": ce(1, Ts, 1), "half": ce(0.5, Ts, 1), "star": ce(cstar, Ts, 1)}, "cstar": cstar}
    rng = np.random.default_rng(808)
    mu = theta * sig
    sims = {}
    for T in (5, 10, 20, 50):
        M = 20000
        R = rng.normal(mu / 12, sig / np.sqrt(12), (M, 12 * T))
        mh = R.mean(1) * 12
        sh = R.std(1, ddof=1) * np.sqrt(12)
        pi = mh / sh ** 2                         # gamma = 1: Kelly
        th2 = (mh / sh) ** 2
        chat = np.clip(1 - 1 / (T * th2), 0, 1)
        real = lambda w: w * mu - w ** 2 * sig ** 2 / 2  # noqa: E731
        n = 12 * T
        a1, a2 = (n - 1) / (n - 3), (n - 1) ** 2 / ((n - 3) * (n - 5))  # E[sigma^2/s^2], E[sigma^4/s^4], normal data
        sims[str(T)] = {"plug": float(np.mean(real(pi))), "half": float(np.mean(real(pi / 2))),
                        "plug_se": float(np.std(real(pi)) / np.sqrt(M)),
                        "plug_theory_s": float(a1 * theta ** 2 - a2 * (theta ** 2 + 1 / T) / 2),
                        "chat": float(np.mean(real(chat * pi))), "plug_theory": float(ce(1, T, 1)),
                        "star_theory": float(ce(T * theta ** 2 / (T * theta ** 2 + 1), T, 1)),
                        "p_negative_ce": float(np.mean(real(pi) < 0))}
    out["sims"] = sims
    # the US market, monthly 1926-2020: an expanding window from 1936, gamma = 2
    ym, x, rf = _us_monthly()
    x = np.asarray(x, float)
    g = 2.0
    start = 120
    rules = {"plug": [], "half": [], "chat": []}
    for t in range(start, len(x)):
        h = x[:t]
        m_, s2 = h.mean() * 12, h.var(ddof=1) * 12
        pi = m_ / (g * s2)
        T_ = t / 12
        th2 = m_ ** 2 / s2
        c_ = max(0.0, 1 - 1 / (T_ * th2)) if th2 > 0 else 0.0
        for k, w in (("plug", pi), ("half", pi / 2), ("chat", c_ * pi)):
            rules[k].append(w * x[t])
    full = x.mean() * 12 / (g * x.var(ddof=1) * 12)
    out["us_theta"] = float(x[start:].mean() * 12 / (x[start:].std(ddof=1) * np.sqrt(12)))
    out["us_theta_all"] = float(x.mean() * 12 / (x.std(ddof=1) * np.sqrt(12)))
    out["us_pi_path"] = [float(r / x[start + i]) if x[start + i] != 0 else None for i, r in enumerate(rules["plug"])][::12]
    out["us_c_path"] = [float(c / p) if p else None for c, p in zip(rules["chat"][::12], rules["plug"][::12])]
    rules["hindsight"] = list(full * x[start:])
    rules["market"] = list(x[start:])
    us = {}
    for k, v in rules.items():
        v = np.asarray(v)
        us[k] = {"ce": float(v.mean() * 12 - g / 2 * v.var(ddof=1) * 12), "mean": float(v.mean() * 12),
                 "vol": float(v.std(ddof=1) * np.sqrt(12))}
    out["us"] = us
    out["us_first"], out["us_last"], out["gamma_us"] = int(ym[start]), int(ym[-1]), g
    return _json(out)


ITEMS = {"estrisk_theory": compute_estrisk_theory, "coin": compute_coin, "bellman": compute_bellman, "merton_us": compute_merton_us, "kelly_us": compute_kelly_us,
         "fractional": compute_fractional, "samuelson": compute_samuelson, "ergodic": compute_ergodic,
         "ltcm": compute_ltcm, "secretary": compute_secretary, "american": compute_american, "bsde": compute_bsde,
         "ppo": compute_ppo, "envelope": compute_envelope,
         "coin_live": compute_coin_live, "utility_check": compute_utility_check, "bellman_sweep": compute_bellman_sweep,
         "hjb_fd": compute_hjb_fd, "viscosity": compute_viscosity, "rebalance_sim": compute_rebalance_sim,
         "consumption": compute_consumption, "martingale_check": compute_martingale_check,
         "davis_norman": compute_davis_norman, "kelly_live": compute_kelly_live, "breiman_race": compute_breiman_race,
         "edge_error": compute_edge_error, "ergodic_live": compute_ergodic_live, "snell_rw": compute_snell_rw,
         "perpetual_put": compute_perpetual_put, "myopic_loss": compute_myopic_loss,
         "robust_fraction": compute_robust_fraction, "mfg_crowd": compute_mfg_crowd,
         "ppo_s1": compute_ppo_s1, "ppo_s2": compute_ppo_s2, "ppo_s3": compute_ppo_s3, "ppo_s4": compute_ppo_s4,
         "ppo_seeds": compute_ppo_seeds, "ppo_cost_s0": compute_ppo_cost_s0, "ppo_cost_s1": compute_ppo_cost_s1,
         "ppo_cost_s2": compute_ppo_cost_s2, "ppo_cost_s3": compute_ppo_cost_s3, "ppo_cost_s4": compute_ppo_cost_s4,
         "ppo_costs": compute_ppo_costs, "drawdown_policy": compute_drawdown_policy, "vol_target": compute_vol_target,
         "bsde_replay": compute_bsde_replay}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
