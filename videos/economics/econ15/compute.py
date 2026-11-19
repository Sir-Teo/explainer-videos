"""Precompute every number in Part 15 of *Economics, Built* ("Spillovers").

    python -m videos.economics.econ15.compute            # everything missing (seconds)
    python -m videos.economics.econ15.compute --force playit

Results are cached in ``.cache/econ15/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Data: the Data Room
(``explainer.economics.data``: CEDS sulphur dioxide emissions via Our World in Data; transcribed passages from Coase
1960, Cheung 1973, Schmalensee and Stavins 2013, Duranton and Turner 2011 and Currie and Walker 2011).  Models:
Agora's spillovers (``agora.public``), with the Island's Part 15 truths.

Items:
    playit      the shared pot: your payoff for each gift against what the others give
    vcm         Agora's typed players, ten rounds, with and without punishment
    kiln        Bo's kiln: the market, the efficient output, the triangle and Pigou's tax
    coase       Coase's cattle and corn under each liability rule, with transaction costs
    bees        Cheung's rents per hive, in money and in nectar
    lighthouse  Samuelson's condition, voluntary provision and Lindahl's prices for four ship-owners
    fishery     the lagoon: sustainable yield, open access, maximum economic and sustainable yield
    acid        the SO2 market's record
    weitzman    prices against quantities, for two pairs of slopes
    bottleneck  the causeway's queue, its cost, and the toll that removes it
    lockin      Arthur's adopters: two standards, increasing returns, and lock-in by early luck
    dial        the road-traffic dial's rows
    film        the intermission's data film: SO2 emissions, 1900-2022
    melody      its data melody: US emissions, year by year
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.economics import data, dials, island, score
from explainer.economics.agora import public as pb
from explainer.economics.data import tables

CACHE = Cache("econ15")
load = CACHE.load
TRUTH = island.truths(15)


def compute_playit() -> dict:
    t = TRUTH["playit"]
    n, w, m = t["n"], t["endowment"], t["mpcr"]
    others = np.linspace(0, 3 * w, 61)               # what the three others give in all
    rows = []
    for g in t["gives"]:
        rows.append({"give": g, "pay_if_others_0": w - g + m * g, "pay_if_others_all": w - g + m * (g + 3 * w),
                     "pay_curve": [float(w - g + m * (g + o)) for o in others]})
    return {"rows": rows, "others": others, "all_give": float(w - w + m * n * w), "none_give": float(w),
            "keep_per_shell": float(1 - m), "n": n, "endowment": w, "mpcr": m, "multiplier": float(n * m),
            "gives": list(t["gives"])}


def compute_vcm() -> dict:
    t = TRUTH["vcm"]
    a, b = pb.vcm(**t, punish=False), pb.vcm(**t, punish=True)
    return {**t, "n_rounds": t["rounds"], "rounds": a["rounds"], "plain": a["share"], "punish": b["share"],
            "pay_plain": a["payoff"], "pay_punish": b["payoff"]}


def compute_kiln() -> dict:
    t = TRUTH["kiln"]
    e = pb.externality(**t)
    qs = np.linspace(0, 70, 141)
    return {**e, "qs": qs, "demand": t["a"] - t["b"] * qs, "private": t["c"] + t["e"] * qs,
            "social": t["c"] + (t["e"] + t["d"]) * qs, "damage": t["d"] * qs}


def compute_coase() -> dict:
    t = TRUTH["coase"]
    runs = {f"{tc:g}": pb.coase(t["values"], transaction_cost=tc) for tc in t["transaction_costs"]}
    return {"base": runs["0"], "runs": runs, "table": tables.COASE_1960.data}


def compute_bees() -> dict:
    d = tables.CHEUNG_1973.data
    return {"pollination": d["pollination_season"], "honey": d["honey_season"], "corr": d["corr_money_nectar"],
            "survey": d["survey"], "state": d["state"]}


def compute_lighthouse() -> dict:
    t = TRUTH["lighthouse"]
    g = pb.public_good(t["thetas"], t["mc"])
    gs = np.linspace(0, 14, 141)
    th = np.array(t["thetas"])
    mbs = [(th_i / (1 + gs)).tolist() for th_i in th]
    return {**g, "gs": gs, "mbs": mbs, "sum_mb": (th.sum() / (1 + gs)).tolist()}


def compute_fishery() -> dict:
    return {**pb.fishery(**TRUTH["fishery"]), **TRUTH["fishery"]}


def compute_acid() -> dict:
    return tables.ACID_RAIN.data


def compute_weitzman() -> dict:
    t = TRUTH["weitzman"]
    return {"cases": [pb.prices_quantities(mb, mc, t["sigma"]) for mb, mc in t["cases"]], "sigma": t["sigma"]}


def compute_bottleneck() -> dict:
    return pb.bottleneck(**TRUTH["bottleneck"])


def compute_lockin() -> dict:
    return {**pb.lock_in(**TRUTH["lockin"]), **TRUTH["lockin"]}


def compute_dial() -> dict:
    rows = [(e.who, e.year, e.design, e.sample, e.value, e.lo, e.hi) for e in dials.DIALS["road_traffic"].estimates]
    return {"rows": rows, "roads": tables.ROADS.data}


# ---------------------------------------------------------------------------------------------------------------
# the intermission: a century of sulphur

FILM_SECONDS = 40.0
MELODY_SECONDS = 55.0
FILM_ENTITIES = ("United States", "United Kingdom", "China", "India")


def film_time(k: int, n: int) -> float:
    return 1.5 + FILM_SECONDS * k / (n - 1)


def compute_film() -> dict:
    series = {e: data.so2(e) for e in FILM_ENTITIES}
    years = sorted(set.intersection(*[set(s["year"]) for s in series.values()]))
    years = [y for y in years if 1900 <= y <= 2022]
    out = {"years": years, "times": [film_time(k, len(years)) for k in range(len(years))]}
    for e, s in series.items():
        m = dict(zip(s["year"], s["value"]))
        out[e] = [float(m[y]) / 1e6 for y in years]          # million tonnes
    us = out["United States"]
    k_peak = int(np.argmax(us))
    out["us_peak_year"], out["us_peak"] = years[k_peak], us[k_peak]
    cn = out["China"]
    k_cn = int(np.argmax(cn))
    out["cn_peak_year"], out["cn_peak"] = years[k_cn], cn[k_cn]
    out["us_2022"], out["cn_2022"], out["in_2022"], out["uk_2022"] = us[-1], cn[-1], out["India"][-1], \
        out["United Kingdom"][-1]
    return out


def compute_melody() -> dict:
    from explainer.music.monochord.audio import Clip, ClipStore

    f = compute_film()
    times = f["times"]
    mel = score.data_melody(np.array(f["United States"]), MELODY_SECONDS, times=times, act=4, log=False, low=45,
                            high=84)
    events = {"film_end": times[-1] + 6.0, "first": times[0], "half": times[len(times) // 2]}
    clip = Clip(mel["y"], score.SR, events=events,
                notes=[{"t": float(t), "dur": 0.3, "hz": score.hz(nn), "name": str(y)}
                       for t, nn, y in zip(times, mel["notes"], f["years"])],
                meta={"label": "US sulphur dioxide emissions, year by year, 1900-2022 (CEDS via Our World in Data), as "
                               "a tune (computed)", "kind": "synthesized"})
    ClipStore("econ15").save("intermission.melody", clip)
    return {"times": times, "notes": mel["notes"], "years": f["years"], "seconds": MELODY_SECONDS}


ITEMS = {
    "playit": compute_playit,
    "vcm": compute_vcm,
    "kiln": compute_kiln,
    "coase": compute_coase,
    "bees": compute_bees,
    "lighthouse": compute_lighthouse,
    "fishery": compute_fishery,
    "acid": compute_acid,
    "weitzman": compute_weitzman,
    "bottleneck": compute_bottleneck,
    "lockin": compute_lockin,
    "dial": compute_dial,
    "film": compute_film,
    "melody": compute_melody,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
