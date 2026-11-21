"""Precompute every number in Part 68 of *Economics, Built* ("The Dissertation").

    python -m videos.economics.econ68.compute            # everything missing (about a minute)
    python -m videos.economics.econ68.compute --force did

Results are cached in ``.cache/econ68/<name>.json``; scenes call ``load(name)``.  Model: Agora's ``congestion``
module (year-on-year differences in differences, a regression discontinuity in time, a speed-flow curve with a
constant-elasticity demand for trips, a counterfactual toll with its uncertainty, the same study on the Island).  Data:
the MTA's open data on New York's Congestion Relief Zone (``data.mta_crossings``, ``crz_daily``, ``crz_tod``,
``cbd_vmt``, ``cbd_bus``), the state's and the courts' published facts (``tables.congestion_68``), and, for the
series' accounts, the Facts, the Dials and the Calls.

Items:
    entries     daily entries into the zone since 5 January 2025, and their weekday average
    crossings   monthly weekday traffic on the two tunnels into the zone and on the other crossings, 2019-2026
    did         the year-on-year difference in differences by month, with the placebo years
    buses       bus speeds inside and outside the central business district, and their difference in differences
    vmt         miles driven in the zone and on its excluded highways
    clock       the regression discontinuities at 9 pm and 5 am
    model       the smallest model, calibrated at the central assumptions
    cf          the original $15 plan and the narrow optimal toll, with their uncertainty
    island      the same study on the Island: no diversion, diversion, a pre-trend
    scorecard   the Facts with Agora's column
    dials       the Dials' final statuses, by act
    calls       the Called it? record
    film        the intermission's data film: daily entries into the zone
    melody      its data melody
"""

from __future__ import annotations

import datetime as dt

import numpy as np

from explainer.ai.cache import Cache
from explainer.economics import calls, data, dials, facts
from explainer.economics import score as SC
from explainer.economics.agora import congestion as CG
from explainer.economics.data import tables

CACHE = Cache("econ68")
load = CACHE.load
TRUTH = {"island": "the Island's effect, diversion and trend are assumed (agora.congestion.island_study)",
         "model": "the value of time, the miles in the zone and the other costs of a trip are assumptions"}
ASSUME = {"vot": 20.0, "vot_range": (14.0, 24.0), "miles": 3.0, "miles_range": (2.0, 5.0), "other": 25.0,
          "other_range": (15.0, 40.0), "mph": 10.0}
FILM_SECONDS = 42.0
MELODY_SECONDS = FILM_SECONDS + 12.0
ACTS = {1: (1, 4), 2: (5, 10), 3: (11, 18), 4: (19, 21), 5: (22, 26), 6: (27, 33), 7: (34, 37), 8: (38, 42),
        9: (43, 48), 10: (49, 56), 11: (57, 62), 12: (63, 68)}


def _jsonable(x):
    if isinstance(x, dict):
        return {str(k): _jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_jsonable(v) for v in x]
    if isinstance(x, np.ndarray):
        return [_jsonable(v) for v in x.tolist()]
    if isinstance(x, (np.floating, np.integer)):
        return x.item()
    if isinstance(x, (np.bool_,)):
        return bool(x)
    return x


def _days(date: str) -> float:
    return (dt.date.fromisoformat(date) - dt.date(2025, 1, 5)).days


def film_time(day: float, last: float) -> float:
    return 2.0 + day / last * (FILM_SECONDS - 4.0)


def compute_entries() -> dict:
    E = data.crz_daily()
    wk = [a for d, a in zip(E["date"], E["all"]) if dt.date.fromisoformat(d).weekday() < 5]
    cars = [c for d, c in zip(E["date"], E["cars"]) if dt.date.fromisoformat(d).weekday() < 5]
    return _jsonable({"date": E["date"], "all": E["all"], "cars": E["cars"], "weekday_all": float(np.mean(wk)),
                      "weekday_cars": float(np.mean(cars)), "first": E["date"][0], "last": E["date"][-1],
                      "days": len(E["date"]), "car_share": float(np.sum(E["cars"]) / np.sum(E["all"]))})


def compute_crossings() -> dict:
    P = CG.crossings_panel(data.mta_crossings())

    def group(keys):
        tot = None
        for k in keys:
            m = CG._monthly(P["weeks"], P["series"][k])
            tot = m if tot is None else {mm: tot[mm] + m[mm] for mm in tot if mm in m}
        return tot
    T, C = group(CG.TREATED), group(CG.CONTROLS)
    months = sorted(set(T) & set(C))
    base_t = np.mean([T[f"2019-{m:02d}"] for m in range(1, 13)])
    base_c = np.mean([C[f"2019-{m:02d}"] for m in range(1, 13)])
    return _jsonable({"months": months, "treated": [100 * T[m] / base_t for m in months],
                      "control": [100 * C[m] / base_c for m in months], "treated_2024": float(
                          np.mean([T[f"2024-{m:02d}"] for m in range(1, 13)])),
                      "control_2024": float(np.mean([C[f"2024-{m:02d}"] for m in range(1, 13)])),
                      "n_controls": len(CG.CONTROLS)})


def compute_did() -> dict:
    D = CG.yoy_did(CG.crossings_panel(data.mta_crossings()))
    adj = D["effect"] - D["placebo_mean"]
    se_adj = float(np.sqrt(D["se"] ** 2 + (D["placebo_sd"] / np.sqrt(24)) ** 2))
    assert D["effect"] < 0 and D["placebo_mean"] < 0, D
    return _jsonable({**D, "adjusted": adj, "se_adjusted": se_adj})


def compute_buses() -> dict:
    B = CG.bus_speeds(data.cbd_bus())
    bc = [r["cbd"] for r in B["rows"] if r["year"] == 2025]
    return _jsonable({**B, "cbd_change": float(np.mean(bc)), "cbd_se": float(np.std(bc, ddof=1) / np.sqrt(len(bc)))})


def compute_vmt() -> dict:
    V = CG.vmt(data.cbd_vmt())
    z = [r["crz"] for r in V["rows"]]
    return _jsonable({**V, "crz_se": float(np.std(z, ddof=1) / np.sqrt(len(z)))})


def compute_clock() -> dict:
    T = data.crz_tod()
    nine, five = CG.time_rd(T, 21.0), CG.time_rd(T, 5.0)
    assert nine["jump"] > 0.1 and five["jump"] < -0.2
    return _jsonable({"nine": nine, "five": five, "weekdays": T["weekdays"]})


def _inputs():
    V, B = compute_vmt(), compute_buses()
    return V["crz_change"], -B["cbd_change"], V["crz_se"], B["cbd_se"]


def compute_model() -> dict:
    dv, dT, sv, sT = _inputs()
    M = CG.congestion_model(dv, dT, 9.0, ASSUME["vot"], miles=ASSUME["miles"], mph=ASSUME["mph"],
                            other_cost=ASSUME["other"])
    opt = CG.optimal_toll(M)
    e15 = CG.equilibrium(M, 15.0)
    curve = [CG.equilibrium(M, t) for t in np.linspace(0, 20, 41)]
    return _jsonable({**M, "dlnV": dv, "dlnT": dT, "opt": opt, "at15": e15, "curve": curve, "assume": ASSUME})


def compute_cf() -> dict:
    dv, dT, sv, sT = _inputs()
    R = CG.counterfactual(dv, dT, sv, sT, 9.0, 15.0, vot=ASSUME["vot_range"], miles=ASSUME["miles_range"],
                          other=ASSUME["other_range"], mph=ASSUME["mph"], draws=2000)
    E = compute_entries()
    assert R["lnV"][2] < 0 and R["opt"][1] < 9
    return _jsonable({**R, "weekday_entries": E["weekday_all"], "dlnV": dv, "dlnT": dT, "se_V": sv, "se_T": sT})


def compute_island() -> dict:
    return _jsonable({"clean": CG.island_study(), "divert": CG.island_study(divert=0.3),
                      "trend": CG.island_study(pretrend=-0.015)})


def compute_scorecard() -> dict:
    S = facts.scorecard()
    groups: dict = {}
    for r in S:
        g = groups.setdefault(r["group"], [0, 0])
        g[1] += 1
        g[0] += 1 if r["agora"] else 0
    return _jsonable({"rows": S, "filled": sum(1 for r in S if r["agora"]), "n": len(S), "groups": groups,
                      "open": [r for r in S if not r["agora"]]})


def compute_dials() -> dict:
    by_act: dict = {}
    for d in dials.DIALS.values():
        first = min(d.parts)
        act = next(a for a, (lo, hi) in ACTS.items() if lo <= first <= hi)
        by_act.setdefault(act, {}).setdefault(d.status, 0)
        by_act[act][d.status] += 1
    st: dict = {}
    for d in dials.DIALS.values():
        st[d.status] = st.get(d.status, 0) + 1
    settled = sorted([d.name for d in dials.DIALS.values() if d.status == "settled within a range"])
    unident = sorted([d.name for d in dials.DIALS.values() if d.status == "not identified"])
    return _jsonable({"by_act": by_act, "statuses": st, "n": len(dials.DIALS),
                      "estimates": sum(len(d.estimates) for d in dials.DIALS.values()), "settled": settled,
                      "unidentified": unident})


def compute_calls() -> dict:
    C = list(calls.CALLS.values())
    v: dict = {}
    for c in C:
        v[c.verdict] = v.get(c.verdict, 0) + 1
    return _jsonable({"n": len(C), "verdicts": v})


def compute_film() -> dict:
    E = compute_entries()
    days = [_days(d) for d in E["date"]]
    last = max(days)
    # a seven-day average, so that weekends do not dominate the line
    a = np.array(E["all"], float)
    avg = np.convolve(a, np.ones(7) / 7, mode="valid")
    d7 = days[6:]
    return _jsonable({"days": d7, "avg": avg / 1000.0, "t": [film_time(x, last) for x in d7], "last": last,
                      "first": E["date"][0], "last_date": E["date"][-1], "max": float(avg.max() / 1000),
                      "min": float(avg.min() / 1000)})


def compute_melody() -> dict:
    from explainer.music.monochord.audio import Clip, ClipStore

    f = compute_film()
    qt, qv = [], []
    for k in range(0, len(f["avg"]), 7):            # a note a week
        qt.append(f["t"][k])
        qv.append(f["avg"][k])
    mel = SC.data_melody(np.array(qv), MELODY_SECONDS, times=qt, act=12, log=False, low=48, high=79)
    events = {"film_end": f["t"][-1] + 4.0, "first": qt[0]}
    clip = Clip(mel["y"], SC.SR, events=events,
                notes=[{"t": float(tt), "dur": 0.15, "hz": SC.hz(nn), "name": f"{x:.0f}k"}
                       for tt, nn, x in zip(qt, mel["notes"], qv)],
                meta={"label": "vehicles entering New York's Congestion Relief Zone, seven-day average, weekly, from "
                               "January 2025 (MTA open data), as a tune (computed)", "kind": "synthesized"})
    ClipStore("econ68").save("intermission.melody", clip)
    return {"times": qt, "notes": mel["notes"], "seconds": MELODY_SECONDS}


def compute_official() -> dict:
    return dict(tables.CONGESTION_68.data)


ITEMS = {
    "entries": compute_entries,
    "crossings": compute_crossings,
    "did": compute_did,
    "buses": compute_buses,
    "vmt": compute_vmt,
    "clock": compute_clock,
    "model": compute_model,
    "cf": compute_cf,
    "island": compute_island,
    "scorecard": compute_scorecard,
    "dials": compute_dials,
    "calls": compute_calls,
    "official": compute_official,
    "film": compute_film,
    "melody": compute_melody,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
