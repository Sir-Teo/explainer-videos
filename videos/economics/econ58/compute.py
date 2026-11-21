"""Precompute every number in Part 58 of *Economics, Built* ("Scoring the Bill").

    python -m videos.economics.econ58.compute            # everything missing (under a minute)
    python -m videos.economics.econ58.compute --force bridge

Results are cached in ``.cache/econ58/<name>.json``; scenes call ``load(name)``.  Models: Agora's ``appraisal``
module.  Data: the Congressional Budget Office's evaluation files (every deficit projection since 1984, with its
outcome and its legislation-adjusted error) and FRED's real yield on 10-year inflation-protected Treasuries.

Items:
    bridge      the Island's bridge against Bo's ferry: a year's gains, present values, NPV by rate, the IRR
    tornado     the bridge's sensitivities
    hedonic     road noise priced from 3,000 house prices, with and without the harbour held fixed
    travel      the beach valued by the trips to it
    vsl         the wage premium for risk on the Island's jobs, three ways; values of a statistical life-year
    playit      a higher top rate scored statically and with behaviour, on a weighted survey of taxpayers
    discount    constant, Green Book and Weitzman discounting; the bridge under each; the market's real rate
    scoring     a dynamic score with growth and interest rates; the budget window and sunsets; CBO's record
    microsim    the household survey, a higher allowance and its financing, by decile
    cge         a two-sector economy with a tax on manufactures: equilibria, the social accounting matrix, the loss
    risk        the reference class, the Monte Carlo NPV and the option to wait
    rule        a regulation's net benefits by discount rate and value of a statistical life
    target      an emergency department's waits before and under a four-hour target
    film        the intermission's data film: every CBO baseline since 1984 against the outcomes
    melody      its data melody
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.economics import data
from explainer.economics import score as SC
from explainer.economics.agora import appraisal as A

CACHE = Cache("econ58")
load = CACHE.load
TRUTH: dict = {}
FILM_SECONDS = 44.0
MELODY_SECONDS = FILM_SECONDS + 8.0
FILM_YEARS = (1984.0, 2026.0)


def film_time(year: float) -> float:
    a, b = FILM_YEARS
    return 2.0 + (year - a) / (b - a) * (FILM_SECONDS - 4.0)


def _jsonable(x):
    if isinstance(x, dict):
        return {str(k): _jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_jsonable(v) for v in x]
    if isinstance(x, np.ndarray):
        return x.tolist()
    if isinstance(x, (np.floating, np.integer)):
        return x.item()
    if isinstance(x, (np.bool_,)):
        return bool(x)
    return x


def compute_bridge() -> dict:
    y = A.bridge_year()
    rates = np.round(np.arange(0.0, 0.1001, 0.0025), 4)
    by = {f"{r:.3f}": A.appraise(rate=r) for r in (0.02, 0.03, 0.035, 0.05, 0.07)}
    st = A.bridge_streams()
    total = sum(st["streams"].values())
    ben = sum(v for k, v in st["streams"].items() if k in ("time", "fares", "new trips", "safety"))
    return _jsonable({
        "year": y, "rates": rates, "npv": A.npv_curve(None, rates), "irr": A.irr(),
        "by_rate": {k: {"pv": v["pv"], "npv": v["npv"], "bcr": v["bcr"], "benefits": v["benefits"],
                        "costs": v["costs"]} for k, v in by.items()},
        "stream_t": st["t"][:45], "stream_total": total[:45], "stream_benefit": ben[:45],
        "params": {k: v for k, v in A.BRIDGE.items() if k != "build"}, "build": list(A.BRIDGE["build"]),
        "components": list(A.COMPONENTS), "lives_per_year": y["lives"],
        "npv_shadow": A.appraise({"idle_share": 0.5})["npv"], "npv_mcpf": A.appraise({"mcpf": 1.2})["npv"],
        "shadow_saving": sum(A.BRIDGE["build"]) * A.BRIDGE["labour_share"] * 0.5 * (1 - A.BRIDGE["shadow_wage"]),
    })


def compute_tornado() -> dict:
    base = A.appraise(rate=0.035)["npv"]
    return _jsonable({"base": base, "rows": [{"name": n, "lo": lo, "hi": hi} for n, lo, hi in A.tornado()]})


def compute_hedonic() -> dict:
    h = A.hedonic_houses()
    rng = np.random.default_rng(1)
    k = rng.choice(len(h["noise"]), 500, replace=False)
    return _jsonable({**{x: h[x] for x in ("naive", "naive_se", "full", "full_se", "truth", "corr")},
                      "noise": h["noise"][k], "price": h["price"][k] / 1000.0, "harbour": h["harbour"][k],
                      "n": len(h["noise"])})


def compute_travel() -> dict:
    return _jsonable(A.travel_cost())


def compute_vsl() -> dict:
    w = A.wage_risk()
    rng = np.random.default_rng(2)
    k = rng.choice(len(w["risk"]), 600, replace=False)
    ages = [(40, 40), (75, 10)]
    v = 13.7
    return _jsonable({**{x: w[x] for x in ("naive", "naive_se", "controls", "controls_se", "noisy", "noisy_se",
                                            "truth", "mean_risk", "premium")},
                      "risk": w["risk"][k], "wage": w["wage"][k], "ability": w["ability"][k], "n": len(w["risk"]),
                      "vsly": A.vsly(v, 40), "vsl_dot": v,
                      "by_age": [{"age": a, "years": yl, "value": A.vsly(v, 40) * A.annuity(yl, 0.03)}
                                 for a, yl in ages]})


def compute_playit() -> dict:
    T = A.taxpayers()
    s = A.score_top_rate(T)
    es = np.round(np.arange(0.0, 1.01, 0.025), 3)
    ratio = [A.score_top_rate(T, e=e)["ratio"] for e in es]
    e_c = float(np.interp(-60.0 / s["static"], -np.array(ratio), es))       # where it raises 60 million (option C)
    e_zero = float(np.interp(0.0, -np.array(ratio), es))                     # where it raises nothing
    z = T["z"][T["z"] > 150000.0]
    edges = np.linspace(150000.0, 1000000.0, 35)
    hist, _ = np.histogram(z, edges, weights=T["w"][T["z"] > 150000.0])
    return _jsonable({**s, "es": es, "ratios": ratio, "e_c": e_c, "e_zero": e_zero, "n_records": T["n"], "N": T["N"],
                      "pop_top": T["pop_top"], "grossed": float(np.sum(T["w"])), "edges": edges, "hist": hist,
                      "mean_top": float(np.average(z, weights=T["w"][T["z"] > 150000.0]))})


def compute_discount() -> dict:
    T = 105
    t = np.arange(T)
    W = A.weitzman([0.01, 0.07], [0.5, 0.5], np.arange(0, 301, 5))
    gb = A.discount_factors(301, schedule=A.GREEN_BOOK_2003)
    d = data.fred("DFII10")
    yrs = np.array([int(x[:4]) for x in d["date"]])
    vals = np.array(d["value"], float)
    annual = {int(y): float(np.nanmean(vals[yrs == y])) for y in range(2003, 2027)}
    m = (yrs >= 2003) & (yrs <= 2025) & np.isfinite(vals)
    bridge = {"gb2003": A.appraise(schedule=A.GREEN_BOOK_2003)["npv"]}
    for r in (0.02, 0.03, 0.035, 0.07):
        bridge[f"{r:.3f}"] = A.appraise(rate=r)["npv"]
    return _jsonable({"t": t, "df_7": A.discount_factors(T, 0.07), "df_3": A.discount_factors(T, 0.03),
                      "df_35": A.discount_factors(T, 0.035), "df_2": A.discount_factors(T, 0.02),
                      "gb_t": np.arange(301), "gb_df": gb, "weitzman": W, "stpr": A.stpr(),
                      "tips_annual": annual, "tips_mean": float(vals[m].mean()), "bridge": bridge,
                      "pound30": {r: (1 + r) ** -30 for r in (0.02, 0.03, 0.035, 0.07)},
                      "pound100": {r: (1 + r) ** -100 for r in (0.02, 0.035, 0.07)}})


def compute_scoring() -> dict:
    dyn = A.dynamic_score()
    win = A.window(100.0, 10, 8)
    R = A.cbo_record()
    b01 = R["paths"]["2001-05-01"]
    rows01 = [r for r in data.cbo()["projections"] if r["baseline"] == "2001-05-01"]
    dec = [{"year": r["fiscal_year"], "projected": 100 * r["projected"] / r["gdp"],
            "adjusted": 100 * r["adjusted"] / r["gdp"], "actual": 100 * r["actual"] / r["gdp"],
            "error": r["error_pct_gdp"]} for r in rows01]
    return _jsonable({"dynamic": dyn, "window": win, "horizon": R["horizon"], "b2001": b01, "dec2001": dec,
                      "n_baselines": len(R["paths"])})


def compute_microsim() -> dict:
    H = A.households()
    base = A.net_income(H)
    allow = A.with_allowance(A.SCHEDULE, 18000.0)
    pack = A.reform_schedule()
    t1 = A.distribution_table(H, base, A.net_income(H, allow))
    t2 = A.distribution_table(H, base, A.net_income(H, pack))
    return _jsonable({"n": H["n"], "households": t1["households"], "people": t1["people"],
                      "allowance": t1, "package": t2, "schedule": [list(b) for b in A.SCHEDULE[:-1]],
                      "top_rate": A.SCHEDULE[-1][1], "benefits": A.BENEFITS,
                      "tax_total": float(np.sum(H["w"] * base["tax"])) / 1e6,
                      "benefit_total": float(np.sum(H["w"] * base["benefits"])) / 1e6})


def compute_cge() -> dict:
    base, taxed = A.cge(0.0), A.cge(0.10)
    W = A.cge_welfare(0.10)
    ts = np.round(np.arange(0.0, 0.41, 0.02), 3)
    loss = [A.cge_welfare(t)["dwl"] for t in ts]
    tri = [A.cge_welfare(t)["harberger"] for t in ts]
    return _jsonable({"base": base, "taxed": taxed, "sam0": A.sam(base), "sam1": A.sam(taxed), "dwl": W["dwl"],
                      "harberger": W["harberger"], "revenue": taxed["revenue"], "ts": ts, "loss": loss, "tri": tri,
                      "params": A.CGE})


def compute_risk() -> dict:
    rc = A.reference_class()
    mc = A.monte_carlo()
    edges = np.linspace(-400, 400, 41)
    hist, _ = np.histogram(mc["npv"], edges)
    return _jsonable({"cost": rc["cost"], "traffic": rc["traffic"], "uplift50": rc["uplift50"],
                      "uplift80": rc["uplift80"], "share_over": rc["share_over"], "mean_cost": rc["mean_cost"],
                      "mean_traffic": rc["mean_traffic"], "mc_mean": mc["mean"], "p_negative": mc["p_negative"],
                      "p10": mc["p10"], "p90": mc["p90"], "forecast": mc["forecast"], "edges": edges, "hist": hist,
                      "wait": A.wait_option(), "wait_overrun": A.wait_option({"cost_ratio": 1.28}),
                      "uplifted": A.appraise({"cost_ratio": 1.0 + rc["uplift80"]})["npv"]})


def compute_rule() -> dict:
    r = A.rule_appraisal()
    lo = A.rule_appraisal(vsl=5.0)
    return _jsonable({**r, "low_vsl": lo["rows"]})


def compute_target() -> dict:
    g = A.target_gaming()
    edges = np.arange(0, 481, 10)
    h0, _ = np.histogram(g["before"], edges)
    h1, _ = np.histogram(g["after"], edges)
    return _jsonable({**{k: v for k, v in g.items() if not isinstance(v, np.ndarray)}, "edges": edges,
                      "h0": h0 / len(g["before"]), "h1": h1 / len(g["after"])})


def compute_film() -> dict:
    D = data.cbo()
    paths = {}
    for r in D["projections"]:
        paths.setdefault(r["baseline"], []).append((r["fiscal_year"], 100.0 * r["projected"] / r["gdp"]))
    base = []
    for k in sorted(paths):
        y = int(k[:4]) + (int(k[5:7]) - 1) / 12.0
        pts = sorted(paths[k])
        base.append({"date": k, "year": y, "t": film_time(y), "fy": [p[0] for p in pts], "v": [p[1] for p in pts]})
    actual = sorted(D["actual"].items())
    return _jsonable({"baselines": base, "actual_fy": [a for a, _ in actual], "actual": [v for _, v in actual],
                      "actual_t": [film_time(a + 0.75) for a, _ in actual], "first": base[0]["date"],
                      "last": base[-1]["date"]})


def compute_melody() -> dict:
    from explainer.music.monochord.audio import Clip, ClipStore

    f = compute_film()
    vals = np.array(f["actual"])
    times = f["actual_t"]
    mel = SC.data_melody(vals, MELODY_SECONDS, times=times, act=11, log=False, low=45, high=84)
    events = {"film_end": film_time(FILM_YEARS[1]) + 4.0, "first": times[0]}
    clip = Clip(mel["y"], SC.SR, events=events,
                notes=[{"t": float(tt), "dur": 0.2, "hz": SC.hz(nn), "name": f"{x:+.1f}%"}
                       for tt, nn, x in zip(times, mel["notes"], vals)],
                meta={"label": "the federal surplus or deficit, percent of GDP, fiscal years 1984-2025 (CBO), as a "
                               "tune (computed)", "kind": "synthesized"})
    ClipStore("econ58").save("intermission.melody", clip)
    return {"times": times, "notes": mel["notes"], "seconds": MELODY_SECONDS}


ITEMS = {
    "bridge": compute_bridge,
    "tornado": compute_tornado,
    "hedonic": compute_hedonic,
    "travel": compute_travel,
    "vsl": compute_vsl,
    "playit": compute_playit,
    "discount": compute_discount,
    "scoring": compute_scoring,
    "microsim": compute_microsim,
    "cge": compute_cge,
    "risk": compute_risk,
    "rule": compute_rule,
    "target": compute_target,
    "film": compute_film,
    "melody": compute_melody,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
