"""Precompute every number in Part 13 of *Economics, Built* ("Lemons and Signals").

    python -m videos.economics.econ13.compute            # everything missing (seconds)
    python -m videos.economics.econ13.compute --force spiral

Results are cached in ``.cache/econ13/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Data: the Data Room
(``explainer.economics.data``: the CPI for used cars and trucks and for new vehicles, and the CPI for all items, via
FRED; transcribed passages from Akerlof 1970, Einav, Finkelstein and Cullen 2010, Cutler and Zeckhauser 1998, Tyler,
Murnane and Willett 2000, Chiappori and Salanié 2000, Finkelstein and McGarry 2006, Cabral and Hortaçsu 2010,
Hackmann, Kolstad and Kowalski 2015 and Handel 2013).  Models: Agora's markets with private information
(``agora.info``), with the Island's Part 13 truths.  Every random draw is seeded.

Items:
    lemons      Akerlof's market with an additive premium (partial unravelling) and a proportional one (total)
    offers      Play it: a single buyer's offers for a used boat it cannot inspect
    warranty    a guarantee that only a seller of good boats can afford
    spence      the signalling game: the separating range, least-cost separation, pooling
    screen      Rothschild and Stiglitz: the separating menu, the pooling contract, existence by the share of high risks
    spiral      Harvard's PPO (Cutler and Zeckhauser) beside Agora's death spiral
    efc         Einav, Finkelstein and Cullen's demand and cost curves, rebuilt from their Table 4
    tests       the positive-correlation test on simulated drivers, adverse, advantageous and none
    credit      Stiglitz and Weiss: the bank's expected repayment against the rate
    reputation  a buyer's belief in a seller, feedback by feedback, and the price it supports
    dial        the selection-cost dial's rows
    film        the intermission's data film: used and new car prices against all prices, 1953-2026
    melody      its data melody: the real price of used cars, year by year
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.economics import data, dials, island, score
from explainer.economics.agora import info
from explainer.economics.data import tables

CACHE = Cache("econ13")
load = CACHE.load
TRUTH = island.truths(13)


def compute_lemons() -> dict:
    b = TRUTH["boats"]
    add = info.lemons(b["lo"], b["hi"], b["premium"], "add")
    mult = info.lemons(b["lo"], b["hi"], 1.5, "mult")
    return {"prices": add["prices"], "add_value": add["value_offered"], "add_p": add["p_eq"],
            "add_share": add["share_traded"], "add_lost": add["lost_gains"], "mult_value": mult["value_offered"],
            "mult_p": mult["p_eq"], "mult_share": mult["share_traded"], "premium": b["premium"], "lo": b["lo"],
            "hi": b["hi"], "ak": tables.AKERLOF_1970.data}


def compute_offers() -> dict:
    b = TRUTH["boats"]
    rows = info.lemons_offers(b["offers"], b["lo"], b["hi"], b["premium"], "add")
    ps = np.linspace(0, 100, 201)
    curve = [r["expected_gain"] for r in info.lemons_offers(ps, b["lo"], b["hi"], b["premium"], "add")]
    best = ps[int(np.argmax(curve))]
    return {"rows": rows, "ps": ps, "curve": curve, "best": float(best), "best_gain": float(max(curve))}


def compute_warranty() -> dict:
    w = TRUTH["warranty"]
    r = info.warranty(w["good"], w["bad"], w["share_good"], w["fix"], w["break_good"], w["break_bad"])
    return {**r, **w, "cost_good": w["break_good"] * w["fix"], "cost_bad": w["break_bad"] * w["fix"],
            "premium_good": w["good"] - r["pooled_price"]}


def compute_spence() -> dict:
    t = TRUTH["spence"]
    s = info.spence(t["theta_low"], t["theta_high"], t["cost_low"], t["cost_high"], t["share_high"])
    es = np.linspace(0, 3, 121)
    # the wage schedule of the least-cost separating equilibrium and each type's indifference line through its choice
    low_line = t["theta_low"] + t["cost_low"] * es
    high_line = (t["theta_high"] - t["cost_high"] * s["least_cost"]) + t["cost_high"] * es
    many = info.spence(t["theta_low"], t["theta_high"], t["cost_low"], t["cost_high"], 0.9)
    return {**s, **t, "es": es, "low_line": low_line, "high_line": high_line, "pool_wage_many": many["pool_wage"],
            "high_prefers_pooling_many": many["high_prefers_pooling"]}


def compute_screen() -> dict:
    t = TRUTH["screen"]
    r = info.rothschild_stiglitz(t["W"], t["d"], t["p_low"], t["p_high"], t["share_high"])
    lams = np.linspace(0.02, 0.98, 49)
    ok = [info.rothschild_stiglitz(t["W"], t["d"], t["p_low"], t["p_high"], lam)["exists"] for lam in lams]
    # contracts as (cover, premium) points and the zero-profit lines
    xs = np.linspace(0, t["d"], 61)
    W, d = t["W"], t["d"]

    def eu(p, x, prem):
        return (1 - p) * np.log(W - prem) + p * np.log(W - d + x - prem)

    from scipy.optimize import brentq

    def through(p, x0, prem0):
        u0 = eu(p, x0, prem0)
        return np.array([brentq(lambda m: eu(p, x, m) - u0, -60.0, min(W, W - d + x) - 1e-6) for x in xs])

    ic_high = through(t["p_high"], d, t["p_high"] * d)
    ic_low = through(t["p_low"], r["x_low"], r["prem_low"])
    return {**r, "share_high": t["share_high"], "lams": lams, "exists_by_share": ok, "xs": xs,
            "line_low": t["p_low"] * xs, "line_high": t["p_high"] * xs, "line_pool": r["pbar"] * xs,
            "ic_high": ic_high, "ic_low": ic_low}


def compute_spiral() -> dict:
    sp = info.death_spiral(**TRUTH["spiral"])
    cz = tables.CUTLER_ZECKHAUSER_1998.data
    return {"rows": sp["rows"], "mean_extra": sp["mean_extra"], "harvard": cz["path"], "cz": cz}


def compute_efc() -> dict:
    d = tables.EFC_2010.data
    e = info.einav_finkelstein(d["demand"][0], d["demand"][1], d["cost"][0], d["cost"][1])
    return {**e, "paper": d}


def compute_tests() -> dict:
    t = TRUTH["drivers"]
    out = {s: info.positive_correlation(t["n"], s, t["seed"]) for s in ("adverse", "advantageous", "none")}
    return {"results": out, "n": t["n"], "papers": tables.INFO_TESTS.data}


def compute_credit() -> dict:
    c = TRUTH["credit"]
    r = info.stiglitz_weiss(c["s_safe"], c["y_safe"], c["s_risky"], c["y_risky"], c["share_safe"],
                            c["collection_cost"])
    top = float(np.nanmax(r["bank_return"][r["R"] > r["safe_leave"] + 1]))
    return {**r, **c, "risky_top": top}


def compute_reputation() -> dict:
    t = TRUTH["reputation"]
    r = info.reputation(t["prior"], t["honest_good"], t["cheat_good"], t["feedback"], t["value_honest"],
                        t["value_cheat"])
    k = list(t["feedback"]).index(0)
    return {**r, "bad_at": k + 1, "before_bad": float(r["price"][k]), "after_bad": float(r["price"][k + 1]),
            "start": float(r["price"][0]), "end": float(r["price"][-1]), "papers": tables.INFO_TESTS.data}


def compute_dial() -> dict:
    rows = [(e.who, e.year, e.design, e.sample, e.value, e.lo, e.hi) for e in dials.DIALS["selection_cost"].estimates]
    return {"rows": rows, "hkk": tables.HKK_2015.data}


# ---------------------------------------------------------------------------------------------------------------
# the intermission: used cars and new

FILM_SECONDS = 40.0
MELODY_SECONDS = 55.0


def film_time(k: int, n: int) -> float:
    return 1.5 + FILM_SECONDS * k / (n - 1)


def _monthly(series):
    r = data.fred(series)
    return {d[:7]: v for d, v in zip(r["date"], r["value"]) if np.isfinite(v)}


def compute_film() -> dict:
    used, new, cpi = _monthly("CUSR0000SETA02"), _monthly("CUSR0000SETA01"), _monthly("CPIAUCSL")
    months = [m for m in sorted(used) if m in new and m in cpi]
    u = np.array([used[m] / cpi[m] for m in months])
    v = np.array([new[m] / cpi[m] for m in months])
    k0 = months.index("1953-01")
    u, v = 100 * u / u[k0], 100 * v / v[k0]
    n = len(months)
    years = sorted({int(m[:4]) for m in months})
    jan = {int(m[:4]): k for k, m in reversed(list(enumerate(months))) if m.endswith("-01")}
    k_min = int(np.argmin(u))
    k21 = months.index("2022-01") if "2022-01" in months else n - 1
    k20 = months.index("2020-12") if "2020-12" in months else 0
    return {"months": months, "used": u, "new": v, "times": [film_time(k, n) for k in range(n)], "years": years,
            "year_times": [film_time(jan.get(y, 0), n) for y in years], "last": (months[-1], float(u[-1]),
                                                                                 float(v[-1])),
            "used_low": (months[k_min], float(u[k_min])), "jump_2021": float(u[k21] / u[k20] - 1)}


def compute_melody() -> dict:
    from explainer.music.monochord.audio import Clip, ClipStore

    f = compute_film()
    years = f["years"]
    u = np.array(f["used"])
    yr = np.array([int(m[:4]) for m in f["months"]])
    annual = np.array([u[yr == y].mean() for y in years])
    times = f["year_times"]
    mel = score.data_melody(annual, MELODY_SECONDS, times=times, act=4, log=True, low=45, high=84)
    events = {"film_end": f["times"][-1] + 6.0, "first": times[0], "half": times[len(times) // 2]}
    clip = Clip(mel["y"], score.SR, events=events,
                notes=[{"t": float(t), "dur": 0.3, "hz": score.hz(nn), "name": str(y)}
                       for t, nn, y in zip(times, mel["notes"], years)],
                meta={"label": "the price of used cars and trucks relative to all consumer prices, year by year, "
                               "1953-2026, as a tune (computed)", "kind": "synthesized"})
    ClipStore("econ13").save("intermission.melody", clip)
    return {"times": times, "notes": mel["notes"], "annual": annual, "years": years, "seconds": MELODY_SECONDS}


ITEMS = {
    "lemons": compute_lemons,
    "offers": compute_offers,
    "warranty": compute_warranty,
    "spence": compute_spence,
    "screen": compute_screen,
    "spiral": compute_spiral,
    "efc": compute_efc,
    "tests": compute_tests,
    "credit": compute_credit,
    "reputation": compute_reputation,
    "dial": compute_dial,
    "film": compute_film,
    "melody": compute_melody,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
