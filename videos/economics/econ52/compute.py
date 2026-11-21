"""Precompute every number in Part 52 of *Economics, Built* ("Many Agents").

    python -m videos.economics.econ52.compute            # everything missing (about five minutes)
    python -m videos.economics.econ52.compute --force aiyagari

Results are cached in ``.cache/econ52/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Models: Agora's many
agents (``agora.hetero``) with the Island's Part 52 truths, and the continuous-time household of Agora's solver
(``agora.solve``).  Data: the Federal Reserve's Distributional Financial Accounts (wealth shares of the top 1%, the
next 9% and the bottom half, via FRED) for the wealth chapter and the intermission.  Times are wall clock on the
machine that builds the cache; the ratios are what matter.

Items:
    gorman      three households with linear Engel curves: a transfer with equal and unequal slopes
    huggett     Huggett's bond economy in continuous time: the bond demand curve, the equilibrium and its
                distribution
    aiyagari    Aiyagari's economy: the household's rules, the supply and demand for capital, the equilibrium, the
                distribution, its Gini, top shares, MPCs and the share at the limit
    island      100,000 simulated households following the equilibrium rules: wealth, five paths
    table       the equilibrium interest rate over persistence, the spread of earnings and risk aversion
    wealth      the top shares in the data and in the models: Aiyagari, patience types, a business state
    ks          Krusell and Smith: the forecasting rule, its fit, Den Haan's errors, the simulated path, who holds
                the capital and how they save
    hank        household blocks with liquid wealth of 1 to 16 quarters: MPCs, the rate cut split into direct and
                indirect effects against the representative household, multipliers, iMPCs, forward guidance
    playit      the Island's HANK: the rate cut's effect on spending by fifth of wealth, direct and indirect
    jacobian    the fake-news Jacobians against brute force, timed; the matrix of iMPCs
    continuous  the continuous-time household: the sparse matrix, timings against the discrete method
    firms       Hopenhayn's industry at two entry costs; plants with a fixed cost of adjusting
    nominal     three households' nominal positions and a surprise rise in prices
    dials       the MPC dial against the models' MPCs
    film        the intermission's data film: the top 1%'s and bottom half's shares of wealth, 1989-2026
    melody      its data melody
"""

from __future__ import annotations

import time

import numpy as np

from explainer.ai.cache import Cache
from explainer.economics import data, dials, island, score
from explainer.economics.agora import hetero as H
from explainer.economics.agora import solve as S

CACHE = Cache("econ52")
load = CACHE.load
TRUTH = island.truths(52)
FILM_SECONDS = 46.0
MELODY_SECONDS = FILM_SECONDS + 8.0


def _aiy_kw(**over) -> dict:
    A = TRUTH["aiyagari"]
    kw = {"beta": A["beta"], "gamma": A["gamma"], "rho": A["rho"], "sigma": A["sd"] * np.sqrt(1 - A["rho"] ** 2),
          "n_e": A["n_e"], "alpha": A["alpha"], "delta": A["delta"], "n_a": A["n_a"], "a_max": A["a_max"]}
    kw.update(over)
    return kw


def compute_gorman() -> dict:
    m = [20.0, 60.0, 120.0]
    a = [4.0, 12.0, 20.0]
    same = H.gorman_demand(m, a, [0.5, 0.5, 0.5], 20.0, 2, 0)
    diff = H.gorman_demand(m, a, [0.9, 0.6, 0.3], 20.0, 2, 0)
    return {"incomes": m, "a": a, "b_same": [0.5] * 3, "b_diff": [0.9, 0.6, 0.3], "transfer": 20.0,
            "same": same, "diff": diff}


def compute_huggett() -> dict:
    T = TRUTH["huggett"]
    eq = H.huggett_ct(**T)
    rs = np.linspace(0.0, T["rho"] - 0.002, 25)
    curve = []
    for r in rs:
        res = S.hjb_household(r=float(r), **T)
        a, g = np.array(res["a"]), np.array(res["g"])
        curve.append(float((a[:, None] * g).sum() * (a[1] - a[0])))
    return {"r": eq["r"], "rho": T["rho"], "rs": rs.tolist(), "B": curve, "a": eq["a"], "g": eq["g"],
            "s": eq["s"], "a_min": T["a_min"]}


def compute_aiyagari() -> dict:
    kw = _aiy_kw()
    t0 = time.perf_counter()
    res = H.aiyagari(**kw)
    sec = time.perf_counter() - t0
    rho_time = 1 / kw["beta"] - 1
    rs = np.linspace(0.0, rho_time - 0.0015, 18)
    curve = H.capital_supply(rs, **{k: kw[k] for k in ("beta", "gamma", "rho", "sigma", "n_e", "alpha", "delta",
                                                       "n_a", "a_max")})
    a = res["a"]
    marg = res["D"].sum(axis=1)
    m = res["mpc"]
    ap = res["ap"]
    return {"r": res["r"], "K": res["K"], "w": res["w"], "rho_time": rho_time,
            "K_rep": H.capital_demand(rho_time, kw["alpha"], kw["delta"]), "saving_rate": res["saving_rate"],
            "gini": res["gini"], "top1": res["top1"], "top10": res["top10"], "at_limit": res["at_limit"],
            "mean_mpc": res["mean_mpc"], "seconds": sec, "curve": curve, "a": a, "e": res["e"], "pi": res["pi"],
            "c": res["c"], "ap": ap, "marg": marg, "mpc_low": m[:, 0], "mpc_high": m[:, -1],
            "D": res["D"], "P": res["P"]}


def compute_island() -> dict:
    res = H.aiyagari(**_aiy_kw())
    sim = H.simulate(res, n=TRUTH["island_n"], T=400, seed=52, keep=5)
    w = sim["wealth"]
    bins = np.linspace(0, 60, 61)
    hist, _ = np.histogram(np.clip(w, 0, 59.999), bins=bins)
    ones = np.ones_like(w)
    return {"n": int(len(w)), "mean": float(w.mean()), "K": res["K"], "gini_sim": H.gini(w, ones),
            "gini_hist": res["gini"], "top1_sim": H.top_share(w, ones, 0.01), "top1_hist": res["top1"],
            "at_limit_sim": float(np.mean(w <= 1e-9)), "at_limit_hist": res["at_limit"], "bins": bins.tolist(),
            "hist": (hist / len(w)).tolist(), "paths": sim["paths"][:200].T.tolist(), "max": float(w.max())}


def compute_table() -> dict:
    T = TRUTH["table"]
    rows = []
    kw = _aiy_kw()
    for sd in T["sds"]:
        for rho in T["rhos"]:
            for g in T["gammas"]:
                res = H.aiyagari(**{**kw, "rho": rho, "sigma": sd * np.sqrt(1 - rho ** 2), "gamma": g})
                rows.append({"sd": sd, "rho": rho, "gamma": g, "r": 100 * res["r"],
                             "saving_rate": 100 * res["saving_rate"]})
    return {"rows": rows, "rho_time": 100 * (1 / kw["beta"] - 1), **{k: list(v) for k, v in T.items()}}


def compute_wealth() -> dict:
    keys = {"top1": "WFRBST01134", "next9": "WFRBSN09161", "bottom50": "WFRBSB50215"}
    series = {k: data.fred(v) for k, v in keys.items()}
    last = {k: s["value"][-1] for k, s in series.items()}
    date = series["top1"]["date"][-1]
    top10 = last["top1"] + last["next9"]
    alpha_data = H.pareto_from_shares(last["top1"] / 100, top10 / 100)
    base = H.aiyagari(**_aiy_kw())
    types = H.aiyagari_types(betas=TRUTH["betas"], **{k: v for k, v in _aiy_kw().items() if k != "beta"})
    R = TRUTH["returns"]
    hh = {k: v for k, v in _aiy_kw().items() if k in ("beta", "gamma", "rho", "sigma", "n_e")}
    rets = [H.aiyagari_returns(base["r"], base["w"], premium=p, p_up=R["p_up"], p_down=R["p_down"],
                               a_max=R["a_max"], n_a=R["n_a"], **hh) for p in R["premiums"]]
    tail_base = H.pareto_tail(base["a"], base["D"].sum(axis=1))
    models = [
        {"name": "Aiyagari", "top1": 100 * base["top1"], "top10": 100 * base["top10"], "gini": base["gini"],
         "alpha": H.pareto_from_shares(base["top1"], base["top10"])},
        {"name": "patience", "top1": 100 * types["top1"], "top10": 100 * types["top10"], "gini": types["gini"],
         "alpha": H.pareto_from_shares(types["top1"], types["top10"])},
    ]
    models += [{"name": f"returns {100 * p:.0f}", "premium": p, "top1": 100 * x["top1"], "top10": 100 * x["top10"],
                "gini": x["gini"], "alpha": H.pareto_from_shares(x["top1"], x["top10"]), "A": x["A"]}
               for p, x in zip(R["premiums"], rets)]
    return {"date": date, "data": {"top1": last["top1"], "top10": top10, "bottom50": last["bottom50"],
                                   "alpha": alpha_data},
            "models": models, "betas": list(TRUTH["betas"]), "returns": R,
            "tails": [x["pareto"] for x in rets], "tail_base": tail_base, "business_share": rets[0]["business_share"],
            "r_types": types["r"], "r_base": base["r"], "K_base": base["K"],
            "data_tail": {"alpha": alpha_data, "top1": last["top1"] / 100, "top10": top10 / 100}}


def compute_ks() -> dict:
    t0 = time.perf_counter()
    ks = H.krusell_smith()
    sec = time.perf_counter() - t0
    D = ks["D_last"].sum(axis=1)
    return {**{k: ks[k] for k in ("b", "r2", "rounds", "K", "K_rule", "z", "burn", "dh_max", "dh_mean",
                                  "one_step_max", "rich_half_share", "K_mean")},
            "seconds": sec, "a": ks["a"], "ap_mid": ks["ap_mid"], "mps": ks["mps"], "dist": D,
            "history": [{"round": h["round"], "b": h["b"], "diff": h["diff"]} for h in ks["history"]]}


def _hank(liq):
    T = TRUTH["hank"]
    t0 = time.perf_counter()
    ss = H.hank_steady_state(liq, r=T["r"])
    t1 = time.perf_counter()
    jac = H.jacobians(ss, T=T["T"])
    t2 = time.perf_counter()
    return ss, jac, t1 - t0, t2 - t1


def compute_hank() -> dict:
    T = TRUTH["hank"]
    rows = []
    for liq in T["liquid"]:
        ss, jac, s_ss, s_jac = _hank(liq)
        rc = H.hank_rate_cut(ss, jac, T["cut"], T["persist"])
        md = H.hank_multiplier(ss, jac, T["rho_g"], T["phi"], "deficit")
        mb = H.hank_multiplier(ss, jac, T["rho_g"], T["phi"], "balanced")
        fg = H.forward_guidance(ss, jac, list(range(1, 21)), T["cut"])
        rows.append({"liquid": liq, "beta": ss["beta"], "mpc": ss["mean_mpc"], "at_limit": ss["at_limit"],
                     "dC": rc["dC"][:24].tolist(), "direct": rc["direct"][:24].tolist(),
                     "indirect": rc["indirect"][:24].tolist(), "share_impact": rc["direct_share_impact"],
                     "share_year": rc["direct_share_year"], "mult_deficit": md["multiplier"],
                     "mult_balanced": mb["multiplier"], "dY_deficit": md["dY"][:24].tolist(),
                     "impc": H.impc(jac).tolist(), "fg": fg["ha"], "seconds_ss": s_ss, "seconds_jac": s_jac,
                     "residual": rc["goods_residual"]})
    dr = np.zeros(T["T"])
    dr[1:] = T["cut"] * T["persist"] ** np.arange(T["T"] - 1)
    ra = H.ra_rate_cut(T["r"], T["island"], dr)
    ra16 = H.ra_rate_cut(T["r"], 16.0, dr)
    return {"rows": rows, "dr": dr[:24].tolist(), "ra": {"dC": ra["dC"][:24].tolist(),
                                                         "direct": ra["direct"][:24].tolist(),
                                                         "share_impact": ra["direct_share_impact"],
                                                         "share_year": ra["direct_share_year"],
                                                         "share_impact_16": ra16["direct_share_impact"]},
            "fg_ra": float(-T["cut"] / (1 + T["r"])), "r": T["r"], "island": T["island"],
            "cut": T["cut"], "persist": T["persist"]}


def compute_playit() -> dict:
    T = TRUTH["hank"]
    ss, jac, _, _ = _hank(T["island"])
    rc = H.hank_rate_cut(ss, jac, T["cut"], T["persist"])
    tot = H.response(ss, rc["dr"], rc["dZ"])
    dirc = H.response(ss, rc["dr"], np.zeros(T["T"]))
    gt, gd = H.by_wealth_group(ss, tot), H.by_wealth_group(ss, dirc)
    rows = [{"group": a["group"], "total": a["pct"], "direct": b["pct"], "indirect": a["pct"] - b["pct"],
             "wealth_share": a["wealth_share"], "mass": a["mass"]} for a, b in zip(gt, gd)]
    return {"rows": rows, "mpc": ss["mean_mpc"], "at_limit": ss["at_limit"], "liquid": T["island"],
            "total_pct": float(100 * rc["dC"][0] / ss["C"]), "share_impact": rc["direct_share_impact"]}


def compute_jacobian() -> dict:
    T = TRUTH["hank"]
    ss = H.hank_steady_state(T["island"], r=T["r"])
    t0 = time.perf_counter()
    jac = H.jacobians(ss, T=T["T"])
    fake = time.perf_counter() - t0
    cols = [0, 10, 25]
    t0 = time.perf_counter()
    brute = {s: H.jacobian_column_brute(ss, "Z", s, T=T["T"]) for s in cols}
    per_col = (time.perf_counter() - t0) / len(cols)
    err = max(float(np.max(np.abs(brute[s]["C"] - jac["J"][("C", "Z")][:, s]))) for s in cols)
    J = jac["J"][("C", "Z")]
    return {"fake_seconds": fake, "brute_seconds_col": per_col, "brute_seconds_all": per_col * 2 * T["T"],
            "max_error": err, "T": T["T"], "cols": cols,
            "J": J[:40, :40], "col_fake": {str(s): J[:40, s].tolist() for s in cols},
            "col_brute": {str(s): brute[s]["C"][:40].tolist() for s in cols}, "n_states": int(ss["D"].size)}


def compute_continuous() -> dict:
    T = TRUTH["huggett"]
    t0 = time.perf_counter()
    eq = H.huggett_ct(**T)
    sec = time.perf_counter() - t0
    t0 = time.perf_counter()
    res = S.hjb_household(r=eq["r"], **T)
    one = time.perf_counter() - t0
    n = T["n"]
    return {"r": eq["r"], "seconds_eq": sec, "seconds_one": one, "n": n, "unknowns": 2 * n,
            "nonzeros": 2 * n + 2 * (2 * n - 2) + 2 * n, "dense": (2 * n) ** 2, "a": res["a"], "g": res["g"],
            "s": res["s"], "c": res["c"], "iters": res.get("iters")}


def compute_firms() -> dict:
    T = TRUTH["hopenhayn"]
    out = []
    for ce in T["c_e"]:
        h = H.hopenhayn(c_e=ce, c_f=T["c_f"], entrant_shift=T["entrant_shift"])
        out.append({k: h[k] for k in ("p", "M", "firms", "entry_rate", "exit_rate", "threshold", "mean_size",
                                      "entrant_size", "productivity", "output_weighted_productivity",
                                      "emp_share_big")} | {
            "c_e": ce, "phi": h["phi"], "n_l": h["n_l"], "mu": h["mu"], "stay": h["stay"].astype(float),
            "survival": h["survival"][:21], "size_by_age": h["size_by_age"][:21], "nu": h["nu"],
            "cum_firms": h["cum_firms"], "cum_emp": h["cum_emp"]})
    P = TRUTH["plants"]
    L = H.lumpy_plants(n=P["n"], T=P["T"], band=P["band"], shock_at=P["shock_at"])
    return {"rows": out, "plants": L["plants"][20:], "aggregate": L["aggregate"][20:],
            "share_adjusting": L["share_adjusting"][20:], "shock_at": P["shock_at"] - 20,
            "zero_share": float(np.mean(L["plants"][20:] == 0)), "c_f": T["c_f"]}


def compute_nominal() -> dict:
    N = TRUTH["nominal"]
    pi = N["surprise"]
    rows = [{"who": w, "position": p, "change": p / (1 + pi) - p} for w, p in N["households"]]
    return {"surprise": pi, "rows": rows}


def compute_dials() -> dict:
    d = dials.DIALS["mpc_windfall"]
    hank = load("hank")
    a = load("aiyagari")
    models = [{"name": "representative household", "mpc": 100 * TRUTH["hank"]["r"] / (1 + TRUTH["hank"]["r"]),
               "liquid": None}]
    models += [{"name": f"liquid wealth {r['liquid']:g} quarters", "mpc": 100 * r["mpc"], "liquid": r["liquid"]}
               for r in hank["rows"]]
    return {"key": d.key, "models": models, "aiyagari_year": 100 * a["mean_mpc"],
            "rows": [{"who": e.who, "year": e.year, "value": e.value} for e in d.estimates]}


def film_time(t: float, first: float = 1989.5, last: float = 2026.25) -> float:
    return 1.5 + FILM_SECONDS * (t - first) / (last - first)


def compute_film() -> dict:
    top = data.fred("WFRBST01134")
    bot = data.fred("WFRBSB50215")
    t = [int(d[:4]) + (int(d[5:7]) - 1) / 12 for d in top["date"]]
    v, b = top["value"], bot["value"]
    k = int(np.argmin(b))
    return {"t": t, "top1": v, "bottom50": b, "times": [film_time(x) for x in t], "first": v[0], "last": v[-1],
            "b_first": b[0], "b_last": b[-1], "b_low": b[k], "b_low_t": t[k], "first_date": top["date"][0],
            "last_date": top["date"][-1], "peak": max(v), "peak_t": t[int(np.argmax(v))]}


def compute_melody() -> dict:
    from explainer.music.monochord.audio import Clip, ClipStore

    f = compute_film()
    vals = np.array(f["top1"])
    times = f["times"]
    mel = score.data_melody(vals, MELODY_SECONDS, times=times, act=10, log=False, low=45, high=84)
    events = {"film_end": film_time(f["t"][-1]) + 6.0, "first": times[0]}
    clip = Clip(mel["y"], score.SR, events=events,
                notes=[{"t": float(tt), "dur": 0.2, "hz": score.hz(nn), "name": f"{x:.1f}%"}
                       for tt, nn, x in zip(times, mel["notes"], vals)],
                meta={"label": "the top 1%'s share of US household net worth, 1989-2026 (Federal Reserve, "
                               "Distributional Financial Accounts, via FRED), as a tune (computed)",
                      "kind": "synthesized"})
    ClipStore("econ52").save("intermission.melody", clip)
    return {"times": times, "notes": mel["notes"], "seconds": MELODY_SECONDS}


ITEMS = {
    "gorman": compute_gorman,
    "huggett": compute_huggett,
    "aiyagari": compute_aiyagari,
    "island": compute_island,
    "table": compute_table,
    "wealth": compute_wealth,
    "ks": compute_ks,
    "hank": compute_hank,
    "playit": compute_playit,
    "jacobian": compute_jacobian,
    "continuous": compute_continuous,
    "firms": compute_firms,
    "nominal": compute_nominal,
    "dials": compute_dials,
    "film": compute_film,
    "melody": compute_melody,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
