"""Every number in Part 34 (Inside a Quant Firm), computed and cached in .cache/quant34/.

    python -m videos.quant.quant34.compute [items] [--force]

This part is about firms, so most of its facts are quoted from the public record; what is computed is the firm's
arithmetic: what a disclosed statistic implies, how a drawdown stop behaves, and what a platform of managers earns.

* ``virtu``     one losing day in 1,238 (Virtu's 2014 S-1): the daily Sharpe ratio it implies, under normal and fat
                tails, its confidence bound, and the trades a day that make it;
* ``theory``    the research chapter: the expected time to a drawdown stop and the peak before it (Taylor 1975;
                Lehoczky 1977), on a grid of Sharpe ratios and stop depths, checked by simulation;
* ``power``     the stop as a test: the chance a manager of each true Sharpe ratio is stopped within one and three
                years;
* ``platform``  a simulated multi-manager platform: stops, firings, payouts and what investors keep;
* ``stops``     drawdown stops on Kenneth French's factors, 1963-2020: do they help a strategy with a real premium?
"""

from __future__ import annotations

import json
import math
import warnings

import numpy as np

from explainer.ai.cache import Cache
from explainer.quant import data
from explainer.quant.house import firm as F, pit, systematic as SY

warnings.filterwarnings("ignore", category=RuntimeWarning)

CACHE = Cache("quant34")
load = pit.counted(CACHE.load, 34)
THROUGH = "2020-12"
RHO = 0.1        # the correlation of managers' shocks on the simulated platform
SEEDS = 8        # platform runs averaged


def _json(d):
    return json.loads(json.dumps(d, default=lambda o: o.tolist() if hasattr(o, "tolist") else float(o)))


# ---------------------------------------------------------------------------
# What a disclosed statistic implies
# ---------------------------------------------------------------------------
def compute_virtu() -> dict:
    L, N = 1, 1238
    out = {"losing": L, "days": N, "p": L / N}
    out["normal"] = F.implied_daily_sharpe(L, N)
    out["t4"] = F.implied_daily_sharpe(L, N, df=4)
    out["t3"] = F.implied_daily_sharpe(L, N, df=3)
    up = F.binomial_upper(L, N)
    out["p_upper"] = up
    from scipy import stats
    out["normal_lower"] = float(-stats.norm.ppf(up))
    out["annual"] = out["normal"] * math.sqrt(252)
    out["annual_lower"] = out["normal_lower"] * math.sqrt(252)
    out["annual_t4"] = out["t4"] * math.sqrt(252)
    # how many independent trades a day give that daily ratio, for a per-trade edge-to-noise ratio e/s
    out["trades"] = {str(r): (out["normal"] / r) ** 2 for r in (0.005, 0.01, 0.02, 0.05)}
    # a simulated market maker: n trades a day, each with edge/noise 0.01; the share of losing days
    rng = np.random.default_rng(34)
    sims = []
    for n in (100, 1000, 10000, 100000):
        daily = rng.normal(0.01 * n, math.sqrt(n), 20000)
        sims.append({"n": n, "lose": float(np.mean(daily < 0)), "sharpe_daily": 0.01 * math.sqrt(n)})
    out["sims"] = sims
    # for comparison: a Sharpe-2 fund loses on about Phi(-2/sqrt(252)) of days
    out["fund_lose"] = {str(s): float(stats.norm.cdf(-s / math.sqrt(252))) for s in (0.5, 1, 2, 3)}
    return _json(out)


# ---------------------------------------------------------------------------
# The research chapter: the drawdown stop
# ---------------------------------------------------------------------------
def compute_theory() -> dict:
    Ss = [0.0, 0.5, 1.0, 1.5, 2.0, 3.0]
    ds = [0.5, 0.75, 1.0, 1.5, 2.0]
    grid = [[F.stop_time_sharpe(S, d) for d in ds] for S in Ss]
    peak = [[F.peak_at_stop(S, 1.0, d) for d in ds] for S in Ss]
    sims = []
    for S, d in [(0.0, 1.0), (0.5, 1.0), (1.0, 0.5), (1.0, 1.0), (2.0, 1.0), (1.0, 1.5)]:
        a = F.simulate_stop(S, 1.0, d, n=4000, dt=1 / 252, horizon=200, seed=11)
        b = F.simulate_stop(S, 1.0, d, n=4000, dt=1 / 2016, horizon=200, seed=12)
        x1, x2 = math.sqrt(1 / 252), math.sqrt(1 / 2016)
        ex_t = b["tau"] - (a["tau"] - b["tau"]) * x2 / (x1 - x2)
        ex_m = b["peak"] - (a["peak"] - b["peak"]) * x2 / (x1 - x2)
        # the peak at the stop is exponential: its coefficient of variation is one
        cv = float(np.std(b["taus"]) / np.mean(b["taus"]))
        sims.append({"S": S, "d": d, "theory": F.stop_time_sharpe(S, d), "sim_daily": a["tau"], "sim_fine": b["tau"],
                     "extrap": ex_t, "peak_theory": F.peak_at_stop(S, 1.0, d), "peak_extrap": ex_m,
                     "stopped": b["stopped"], "cv_tau": cv})
    # the stop-time distribution for one case, for a histogram
    h = F.simulate_stop(1.0, 1.0, 1.0, n=6000, dt=1 / 1008, horizon=200, seed=13)
    # the exponential law of the peak: P(M > x) = exp(-x/E M), checked by simulation
    pk = F.simulate_stop(1.0, 1.0, 1.0, n=6000, dt=1 / 1008, horizon=200, seed=14)
    return _json({"S": Ss, "d": ds, "grid": grid, "peak": peak, "sims": sims, "hist": h["taus"],
                  "peak_mean_sim": pk["peak"], "peak_mean_theory": F.peak_at_stop(1.0, 1.0, 1.0)})


def compute_power() -> dict:
    out = []
    for S in (-1.0, -0.5, 0.0, 0.5, 1.0, 2.0):
        row = {"S": S}
        for d in (1.0, 1.5):
            s = F.simulate_stop(S, 1.0, d, n=6000, dt=1 / 252, horizon=3.0, seed=int(100 * S + 10 * d) + 500)
            taus = np.asarray(s["taus"])
            row[f"d{d}_1y"] = float(np.sum(taus <= 1.0) / 6000)
            row[f"d{d}_3y"] = float(np.sum(taus <= 3.0) / 6000)
        out.append(row)
    return _json({"rows": out})


# ---------------------------------------------------------------------------
# A platform of pods
# ---------------------------------------------------------------------------
def compute_platform() -> dict:
    cases = {
        "10% vol, halve 5%, cut 7.5%": dict(vol=0.10, halve=0.05, cut=0.075),
        "5% vol, halve 5%, cut 7.5%": dict(vol=0.05, halve=0.05, cut=0.075),
        "5% vol, no stops": dict(vol=0.05, halve=None, cut=None),
    }
    out = {}
    for skill_sd in (0.5, 0.0):
        for name, kw in cases.items():
            runs = []
            for seed in range(SEEDS):
                p = F.platform(200, 30, 0.5, skill_sd, kw["vol"], kw["halve"], kw["cut"], payout=0.2, seed=seed,
                               rho=RHO)
                r = {k: v for k, v in p.items() if not hasattr(v, "shape")}
                r["platform_sharpe"] = float(np.mean(p["annual"]) / np.std(p["annual"], ddof=1))
                r["investor_sharpe"] = float(np.mean(p["net"]) / np.std(p["net"], ddof=1))
                runs.append(r)
            key = f"{name} | skill sd {skill_sd}"
            out[key] = {k: float(np.nanmean([r[k] for r in runs])) for k in runs[0]}
            out[key]["investor_sharpe_se"] = float(np.std([r["investor_sharpe"] for r in runs]) / math.sqrt(SEEDS))
    return _json(out)


# ---------------------------------------------------------------------------
# Stops on real premia
# ---------------------------------------------------------------------------
def _factors():
    k = data.ken_french_monthly("F-F_Research_Data_5_Factors_2x3_CSV.zip", "ff5_monthly", "2025-12")
    r = k["returns"]
    f = {"date": k["date"], "Mkt-RF": r[:, 0], "SMB": r[:, 1], "HML": r[:, 2], "RMW": r[:, 3], "CMA": r[:, 4]}
    m = data.ken_french_monthly("F-F_Momentum_Factor_CSV.zip", "mom_monthly", "2025-12")
    idx = {int(a): i for i, a in enumerate(m["date"])}
    f["UMD"] = np.array([m["returns"][idx[int(a)], 0] if int(a) in idx else np.nan for a in f["date"]])
    return f


def compute_stops() -> dict:
    f = _factors()
    d = np.asarray(f["date"])
    keep = d <= 202012
    out = {"names": [], "rows": []}
    for name in ("Mkt-RF", "SMB", "HML", "RMW", "CMA", "UMD"):
        r = np.asarray(f[name], float)[keep]
        ok = np.isfinite(r)
        r = r[ok]
        # scale to 10% a year using the trailing 36 months' volatility (no look-ahead), from the 37th month
        vol = np.array([np.std(r[max(0, t - 36):t], ddof=1) if t >= 36 else np.nan for t in range(len(r))])
        x = 0.10 / math.sqrt(12) / vol * r
        x = x[36:]
        base = {"mean": float(np.mean(x) * 12), "sharpe": float(np.mean(x) / np.std(x, ddof=1) * math.sqrt(12)),
                "maxdd": SY.max_drawdown(x)}
        rows = {"none": base}
        for dd in (0.10, 0.15, 0.20):
            for wait in (3, 12):
                y, n = F.apply_stop(x, dd, wait)
                # the i.i.d. null: the same rule on the months shuffled, which keeps the distribution and removes
                # every serial dependence (volatility clustering, slow drawdowns)
                rng = np.random.default_rng(int(1000 * dd) + wait)
                null = []
                for _ in range(200):
                    z = rng.permutation(x)
                    yz, _n = F.apply_stop(z, dd, wait)
                    null.append(np.mean(yz) / np.std(yz, ddof=1) * math.sqrt(12) - np.mean(z) / np.std(z, ddof=1)
                                * math.sqrt(12))
                sh = float(np.mean(y) / np.std(y, ddof=1) * math.sqrt(12))
                rows[f"{int(100 * dd)}%/{wait}m"] = {"mean": float(np.mean(y) * 12), "sharpe": sh,
                                                     "maxdd": SY.max_drawdown(y), "stops": n,
                                                     "time_out": float(np.mean(y == 0)),
                                                     "null_change": float(np.mean(null)),
                                                     "null_sd": float(np.std(null)),
                                                     "change": sh - base["sharpe"]}
        out["names"].append(name)
        out["rows"].append(rows)
    out["start"] = int(d[keep][36])
    return _json(out)


# ---------------------------------------------------------------------------
# The House's own record: from research to the sealed years
# ---------------------------------------------------------------------------
def compute_house() -> dict:
    from explainer.quant.house import track
    rows = track.rows(upto_part=33)
    names = sorted(rows)
    rs = np.array([rows[k]["research"]["sharpe"] for k in names])
    hs = np.array([rows[k]["holdout"]["sharpe"] for k in names])
    ses = np.array([rows[k]["holdout"]["sharpe_se"] for k in names])
    keep = rs < 3.0            # leave out Part 25's SDF row, whose research Sharpe is an in-sample fit, not a backtest
    b, a = np.polyfit(rs[keep], hs[keep], 1)
    return _json({"names": names, "research": rs, "holdout": hs, "se": ses, "parts": [rows[k]["part"] for k in names],
                  "slope": float(b), "intercept": float(a), "n": int(keep.sum()),
                  "mean_research": float(rs[keep].mean()), "mean_holdout": float(hs[keep].mean()),
                  "share_positive": float(np.mean(hs > 0)), "trials": int(pit.trials_so_far())})


ITEMS = {"virtu": compute_virtu, "theory": compute_theory, "power": compute_power, "platform": compute_platform,
         "stops": compute_stops, "house": compute_house}


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
