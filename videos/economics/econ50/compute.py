"""Precompute every number in Part 50 of *Economics, Built* ("The Policy Memo").

    python -m videos.economics.econ50.compute            # everything missing (a minute or two)
    python -m videos.economics.econ50.compute --force island

Results are cached in ``.cache/econ50/<name>.json`` (+ ``.npz``); scenes call ``load(name)``. Data: the Data Room
(``explainer.economics.data``: the Census Bureau's official poverty rates for children and for everyone, from the
Small Area Income and Poverty Estimates, via FRED; BEA's GDP and consumption, via FRED; the tables of Part 50).
Models: Agora's policy memo (``agora.memo``) with the Island's Part 50 truths.

Items:
    families    the Island's families with children: who they are
    schedules   the old credit and the allowance (with the EITC) for a single parent of two, by earnings
    island      the old credit against the allowance at the central dials: poverty, deep poverty, work, cost
    fan         the same across participation elasticities from 0 to 0.5
    deciles     who gains: the average gain by decile of income under the old credit
    budget      the cost, the fiscal externality, and the MVPF by children's later repayment and the cost of funds
    economy     the cost scaled to the United States against GDP and consumption; the cost of funds from a top surtax
    tornado     how each dial moves child poverty and the cost per child
    options     the allowance against the same with the work requirement kept for the old credit, at two elasticities
    record      the official poverty rate of children and of everyone, 1989-2024, and the SPM points
    film        the intermission's data film: the official child poverty rate, 1989-2024
    melody      its data melody
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.economics import data, island, score
from explainer.economics.agora import memo
from explainer.economics.data import tables

CACHE = Cache("econ50")
load = CACHE.load
TRUTH = island.truths(50)
FILM_SECONDS = 48.0
MELODY_SECONDS = FILM_SECONDS + 8.0


def _families():
    return memo.families(**TRUTH["families"])


def compute_families() -> dict:
    F = _families()
    pot = np.array(F["potential"])
    return {"n": F["n"], "single": float(np.mean(F["married"] == 0)), "children": int(np.sum(F["kids"])),
            "kids_dist": [float(np.mean(F["kids"] == k)) for k in (1, 2, 3, 4)],
            "young_share": float(np.sum(F["young"]) / np.sum(F["kids"])),
            "median_single": float(np.median(pot[F["married"] == 0])),
            "median_couple": float(np.median(pot[F["married"] == 1]))}


def compute_schedules() -> dict:
    e = np.linspace(0, 150000, 301)            # steps of 500: index 40 is 20,000
    one = np.ones_like(e)
    single = np.zeros_like(e, dtype=int)
    eitc = memo.eitc_2021(e, 2 * one, single)
    old = memo.ctc_2020(e, 2 * one, single)
    new = memo.allowance_2021(e, one, one, single)
    tax = memo.income_tax(e, single)
    net_old = e - tax + eitc + old
    net_new = e - tax + eitc + new
    return {"earnings": e.tolist(), "eitc": eitc.tolist(), "ctc": old.tolist(), "allowance": new.tolist(),
            "net_old": net_old.tolist(), "net_new": net_new.tolist(), "at0_old": float(old[0] + eitc[0]),
            "at0_new": float(new[0] + eitc[0]), "gain_work_old_20k": float(net_old[40] - net_old[0]),
            "gain_work_new_20k": float(net_new[40] - net_new[0]), "old_full": float(old[e == 50000][0]),
            "new_full": float(new[e == 50000][0]), "diff_zero_at": float(e[np.argmax((new - old) <= 0.5)]),
            "old_at_20k": float(old[40]), "eitc_at_20k": float(eitc[40]), "tax_at_20k": float(tax[40])}


def _summary(r):
    return {"old": r["old"], "new": r["new"], "static_child_poverty": r["static_child_poverty"], "cost": r["cost"],
            "static_cost": r["static_cost"], "per_child": r["per_child"], "exits": r["exits"],
            "parents": r["parents"], "earnings_change": r["earnings_change"]}


def compute_island() -> dict:
    F = _families()
    r = memo.compare(F, line_base=TRUTH["line_base"], **TRUTH["base"])
    out = _summary(r)
    out["exit_share"] = r["exits"] / float(np.sum(r["old_work"]))
    out["fall"] = 1 - r["new"]["child_poverty"] / r["old"]["child_poverty"]
    out["static_fall"] = 1 - r["static_child_poverty"] / r["old"]["child_poverty"]
    quit_ = np.asarray(r["old_work"]) & ~np.asarray(r["new_work"])
    start = ~np.asarray(r["old_work"]) & np.asarray(r["new_work"])
    pot = np.asarray(F["potential"])
    out["quit_single_share"] = float(np.mean(F["married"][quit_] == 0))
    out["quit_median_potential"] = float(np.median(pot[quit_]))
    out["starts"] = int(np.sum(start))
    edges = [0, 10000, 20000, 30000, 40000, 60000, 1e9]
    out["quit_by_potential"] = {"edges": edges[:-1],
                                "rate": [float(np.mean(quit_[(pot >= a) & (pot < b) & np.asarray(r["old_work"])]))
                                         for a, b in zip(edges[:-1], edges[1:])]}
    return out


def compute_fan() -> dict:
    F = _families()
    els = np.round(np.linspace(0.0, 0.5, 11), 3)
    rows = [memo.compare(F, elasticity=float(e), income_effect=TRUTH["base"]["income_effect"],
                         take_up=TRUTH["base"]["take_up"], line_base=TRUTH["line_base"]) for e in els]
    dn = np.array([r["new"]["deep"] for r in rows])
    d0 = rows[0]["old"]["deep"]
    k = int(np.argmax(dn > d0))
    cross = float(els[k - 1] + (d0 - dn[k - 1]) / (dn[k] - dn[k - 1]) * (els[k] - els[k - 1])) if k > 0 else None
    return {"elasticity": els.tolist(), "old": rows[0]["old"]["child_poverty"], "deep_cross": cross,
            "new": [r["new"]["child_poverty"] for r in rows], "deep_old": rows[0]["old"]["deep"],
            "deep_new": [r["new"]["deep"] for r in rows], "exits": [r["exits"] for r in rows],
            "cost": [r["cost"] for r in rows], "static": rows[0]["static_child_poverty"],
            "parents": rows[0]["parents"]}


def compute_deciles() -> dict:
    F = _families()
    r = memo.compare(F, line_base=TRUTH["line_base"], **TRUTH["base"])
    inc = np.array(r["old_income"])
    gain = np.array(r["new_income"]) - inc
    q = np.quantile(inc, np.linspace(0, 1, 11))
    mean_gain, share = [], []
    for i in range(10):
        k = (inc >= q[i]) & (inc <= q[i + 1]) if i == 9 else (inc >= q[i]) & (inc < q[i + 1])
        mean_gain.append(float(gain[k].mean()))
        share.append(float(gain[k].sum() / max(inc[k].sum(), 1.0)))
    losers = float(np.mean(gain < -1))
    return {"edges": q.tolist(), "mean_gain": mean_gain, "share_of_income": share, "losers": losers,
            "gain_total": float(gain.sum())}


def compute_budget() -> dict:
    isl = compute_island()
    wtp = isl["static_cost"]                 # what families receive at unchanged behaviour
    cost = isl["cost"]                        # the budget cost with behaviour, before any long-run return
    fe = cost - wtp                           # the fiscal externality of changed work
    rows = []
    st = TRUTH["surtax"]
    mcpfs = [1.0] + [memo.top_mcpf(st["tau"], st["a"], e) for e in st["e"][1:]]
    for cr in TRUTH["child_return"]:
        for mc in mcpfs:
            net = mc * (cost - cr * wtp)
            rows.append({"child_return": cr, "mcpf": mc, "mvpf": memo.mvpf(wtp, net)})
    # scaled to the United States: the Island's cost per child times about 70 million children
    us_children = 70e6
    return {"wtp": wtp, "cost": cost, "fiscal_externality": fe, "fe_share": fe / wtp, "rows": rows, "mcpfs": mcpfs,
            "per_child": isl["per_child"], "us_cost": isl["per_child"] * us_children, "us_children": us_children}


def compute_economy() -> dict:
    B = compute_budget()
    gdp = data.fred("GDPA")
    pce = data.fred("PCECA")
    y = [int(d[:4]) for d in gdp["date"]]
    g24 = float(gdp["value"][y.index(2024)]) * 1e9
    yp = [int(d[:4]) for d in pce["date"]]
    c24 = float(pce["value"][yp.index(2024)]) * 1e9
    tau, a = TRUTH["surtax"]["tau"], TRUTH["surtax"]["a"]
    es = TRUTH["surtax"]["e"]
    return {"us_cost": B["us_cost"], "gdp_2024": g24, "pce_2024": c24, "share_gdp": B["us_cost"] / g24,
            "share_pce": B["us_cost"] / c24, "tau": tau, "a": a, "e": list(es),
            "mcpf": [memo.top_mcpf(tau, a, e) for e in es], "curve_e": np.linspace(0, 0.6, 61).tolist(),
            "curve_mcpf": [memo.top_mcpf(tau, a, e) for e in np.linspace(0, 0.6, 61)]}


def compute_tornado() -> dict:
    F = _families()
    out = {}
    for metric in ("child_poverty", "per_child"):
        out[metric] = memo.tornado(F, {**TRUTH["base"], "line_base": TRUTH["line_base"]}, TRUTH["ranges"],
                                   metric=metric)
    base = memo.compare(F, line_base=TRUTH["line_base"], **TRUTH["base"])
    return {**out, "base_poverty": base["new"]["child_poverty"], "base_per_child": base["per_child"],
            "old_poverty": base["old"]["child_poverty"]}


def compute_options() -> dict:
    F = _families()
    out = {}
    for pol in ("allowance", "hybrid"):
        rows = []
        for e in (0.25, 0.5):
            r = memo.compare(F, elasticity=e, income_effect=TRUTH["base"]["income_effect"],
                             take_up=TRUTH["base"]["take_up"], line_base=TRUTH["line_base"], policy=pol)
            rows.append({"elasticity": e, "poverty": r["new"]["child_poverty"], "deep": r["new"]["deep"],
                         "exits": r["exits"], "per_child": r["per_child"], "static_cost": r["static_cost"],
                         "cost": r["cost"], "mvpf": memo.mvpf(r["static_cost"], r["cost"])})
        out[pol] = rows
    base = memo.compare(F, line_base=TRUTH["line_base"], **TRUTH["base"])
    out["old"] = {"poverty": base["old"]["child_poverty"], "deep": base["old"]["deep"]}
    return out


def compute_record() -> dict:
    kids = data.fred("PPU18US00000A156NCEN")
    allp = data.fred("PPAAUS00000A156NCEN")
    y = [int(d[:4]) for d, v in zip(kids["date"], kids["value"]) if v == v]
    v = [float(v) for v in kids["value"] if v == v]
    ya = [int(d[:4]) for d, x in zip(allp["date"], allp["value"]) if x == x]
    va = [float(x) for x in allp["value"] if x == x]
    T = tables.CTC_2021.data
    return {"year": y, "children": v, "year_all": ya, "all": va,
            "spm": {"2020": T["spm_2020"], "2021": T["spm_2021"], "2022": T["spm_2022"]},
            "first_year": y[0], "last_year": y[-1], "last": v[-1], "v2020": v[y.index(2020)],
            "v2021": v[y.index(2021)], "peak": max(v), "peak_year": y[int(np.argmax(v))]}


def film_time(t: float, first: float = 1989.0, last: float = 2024.0) -> float:
    return 1.5 + FILM_SECONDS * (t - first) / (last - first)


def compute_film() -> dict:
    R = compute_record()
    return {"t": R["year"], "v": R["children"], "times": [film_time(t) for t in R["year"]], "first": R["children"][0],
            "last": R["last"], "peak": R["peak"], "peak_t": R["peak_year"], "v2021": R["v2021"]}


def compute_melody() -> dict:
    from explainer.music.monochord.audio import Clip, ClipStore

    f = compute_film()
    vals = np.array(f["v"])
    times = f["times"]
    mel = score.data_melody(vals, MELODY_SECONDS, times=times, act=9, log=False, low=40, high=84)
    events = {"film_end": film_time(f["t"][-1]) + 6.0, "first": times[0], "peak": film_time(f["peak_t"]),
              "y2021": film_time(2021)}
    clip = Clip(mel["y"], score.SR, events=events,
                notes=[{"t": float(tt), "dur": 0.3, "hz": score.hz(nn), "name": f"{x:.1f}"}
                       for tt, nn, x in zip(times, mel["notes"], vals)],
                meta={"label": "the official poverty rate of American children, 1989-2024 (Census SAIPE, via FRED), "
                               "as a tune (computed)", "kind": "synthesized"})
    ClipStore("econ50").save("intermission.melody", clip)
    return {"times": times, "notes": mel["notes"], "seconds": MELODY_SECONDS}


ITEMS = {
    "families": compute_families,
    "schedules": compute_schedules,
    "island": compute_island,
    "fan": compute_fan,
    "deciles": compute_deciles,
    "budget": compute_budget,
    "economy": compute_economy,
    "tornado": compute_tornado,
    "options": compute_options,
    "record": compute_record,
    "film": compute_film,
    "melody": compute_melody,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
