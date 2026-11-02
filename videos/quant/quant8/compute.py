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
load = CACHE.load

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


ITEMS = {"coin": compute_coin, "bellman": compute_bellman, "merton_us": compute_merton_us, "kelly_us": compute_kelly_us,
         "fractional": compute_fractional, "samuelson": compute_samuelson, "ergodic": compute_ergodic,
         "ltcm": compute_ltcm, "secretary": compute_secretary, "american": compute_american, "bsde": compute_bsde,
         "ppo": compute_ppo, "envelope": compute_envelope}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
