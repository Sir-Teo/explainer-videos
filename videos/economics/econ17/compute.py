"""Precompute every number in Part 17 of *Economics, Built* ("Markets by Design").

    python -m videos.economics.econ17.compute            # everything missing (seconds)
    python -m videos.economics.econ17.compute --force board

Results are cached in ``.cache/econ17/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Data: the Data Room
(``explainer.economics.data``: the crude marriage rate from the OECD, the US Census Bureau and CDC via Our World in
Data; Roth's account of the medical market, its clearinghouses, New York's high-school match and kidney chains;
exam-school and charter-school estimates).  Models: Agora's matching module (``agora.matching``), with the Island's
Part 17 truths.

Items:
    playit      the workshops: what you get for each list you could submit, under the Boston rule and under DA
    board       the apprentices' board: deferred acceptance round by round; both sides proposing
    lattice     every stable matching of the board, with each side's ranks
    bridge      Clarke's pivot rule for the footbridge
    trade       Myerson and Satterthwaite: gains from trade under three rules
    huts        top trading cycles on four huts
    kidneys     the kidney pool: pairs, cycles and a chain
    assignment  Shapley and Shubik's two boats and two buyers: the efficient assignment and the core
    lottery     one oversubscribed school: OLS, IV without and with type controls, over many lotteries
    roth        the medical market's history and the clearinghouses (Roth 2012)
    schools     exam-school and Denver charter estimates
    dial        the school-effects dial's rows
    film        the intermission's data film: marriages per 1,000 people, the United States 1886-2022 and three others
    melody      its data melody: the US rate, year by year
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.economics import data, dials, island, score
from explainer.economics.agora import matching as mt
from explainer.economics.data import tables

CACHE = Cache("econ17")
load = CACHE.load
TRUTH = island.truths(17)


def _market():
    p = TRUTH["playit"]
    students = {k: list(v) for k, v in p["students"].items()}
    schools = {s: list(p["lottery"]) for s in p["capacity"]}
    return students, schools, dict(p["capacity"])


def compute_playit() -> dict:
    students, schools, cap = _market()
    b = mt.boston(students, schools, cap)
    d = mt.deferred_acceptance(students, schools, cap)
    return {"students": students, "lottery": list(TRUTH["playit"]["lottery"]), "capacity": cap,
            "boston": b["match"], "boston_log": b["log"], "da": d["match"], "da_log": d["log"],
            "boston_reports": [{"report": r["report"], "gets": r["gets"]}
                               for r in mt.outcomes_by_report("you", students, schools, cap, "boston")],
            "da_reports": [{"report": r["report"], "gets": r["gets"]}
                           for r in mt.outcomes_by_report("you", students, schools, cap, "da")],
            "boston_blocking": mt.blocking_pairs(b["match"], students, schools, cap),
            "da_blocking": mt.blocking_pairs(d["match"], students, schools, cap)}


def _board():
    b = TRUTH["board"]
    return ({k: list(v) for k, v in b["apprentices"].items()}, {k: list(v) for k, v in b["workshops"].items()})


def compute_board() -> dict:
    pa, pw = _board()
    a = mt.deferred_acceptance(pa, pw)
    w = mt.deferred_acceptance(pw, pa)
    return {"apprentices": pa, "workshops": pw, "a_match": a["match"], "a_log": a["log"], "a_rounds": a["rounds"],
            "w_match": {ap: wk for wk, ap in w["match"].items()}, "w_log": w["log"], "w_rounds": w["rounds"]}


def compute_lattice() -> dict:
    pa, pw = _board()
    st = mt.all_stable(pa, pw)
    for s in st:
        s["a_ranks"] = {a: pa[a].index(w) + 1 for a, w in s["match"].items()}
        s["w_ranks"] = {w: pw[w].index(a) + 1 for a, w in s["match"].items()}
    # one unstable matching to show a blocking pair: everyone's last choice
    bad = {a: pa[a][-1] for a in pa}
    if len(set(bad.values())) < len(bad):
        bad = dict(zip(pa, sorted(pw)))
    return {"stable": st, "unstable": bad, "blocking": mt.blocking_pairs(bad, pa, pw)}


def compute_bridge() -> dict:
    return mt.pivotal(**TRUTH["bridge"])


def compute_trade() -> dict:
    return mt.bilateral_trade()


def compute_huts() -> dict:
    h = {k: list(v) for k, v in TRUTH["huts"].items()}
    return {"prefs": h, **mt.top_trading_cycles(h)}


def compute_kidneys() -> dict:
    k = TRUTH["kidneys"]
    compat = {p: set(v) for p, v in k["compat"].items()}
    r = mt.kidney_exchange(compat, k["max_cycle"], {d: set(v) for d, v in k["altruists"].items()}, k["max_chain"])
    return {"compat": {p: sorted(v) for p, v in compat.items()}, "altruists": {d: list(v) for d, v in
                                                                               k["altruists"].items()},
            "pairs_only": r["pairs_only"], "cycles": r["cycles"], "with_chains": r["with_chains"],
            "best_pairs_only": r["best_pairs_only"], "best_cycles": r["best_cycles"], "best": r["best"],
            "n_pairs": r["n_pairs"]}


def compute_assignment() -> dict:
    return {**mt.assignment_game(TRUTH["assignment"]["values"]), "values": [list(r) for r in
                                                                           TRUTH["assignment"]["values"]]}


def compute_lottery() -> dict:
    t = dict(TRUTH["lottery"])
    reps = t.pop("reps")
    one = mt.lottery_study(**t)
    rows = []
    for k in range(reps):
        r = mt.lottery_study(**{**t, "seed": t["seed"] + 1 + k})
        rows.append((r["ols_everyone"], r["iv_no_controls"], r["iv_type_controls"]))
    arr = np.array(rows)
    return {**one, "reps": reps, "mean": arr.mean(axis=0).tolist(), "sd": arr.std(axis=0).tolist(),
            "draws": arr[:, 2].tolist(), "draws_nc": arr[:, 1].tolist()}


def compute_roth() -> dict:
    return tables.ROTH_2012.data


def compute_schools() -> dict:
    return tables.SCHOOL_EFFECTS.data


def compute_dial() -> dict:
    rows = [(e.who, e.year, e.design, e.sample, e.value, e.lo, e.hi) for e in dials.DIALS["school_effects"].estimates]
    return {"rows": rows, "schools": tables.SCHOOL_EFFECTS.data}


# ---------------------------------------------------------------------------------------------------------------
# the intermission: the oldest matching market

FILM_SECONDS = 40.0
MELODY_SECONDS = 55.0
FILM_OTHERS = ("Japan", "Italy", "Sweden")


def film_time(k: int, n: int) -> float:
    return 1.5 + FILM_SECONDS * k / (n - 1)


def compute_film() -> dict:
    us = data.marriage("United States")
    years = list(range(us["year"][0], us["year"][-1] + 1))
    usm = dict(zip(us["year"], us["value"]))
    known = np.array(us["year"], float)
    vals = np.interp(years, known, us["value"])          # the few missing years drawn straight across
    out = {"years": years, "us": vals.tolist(), "us_known": [y in usm for y in years],
           "times": [film_time(k, len(years)) for k in range(len(years))]}
    for e in FILM_OTHERS:
        s = data.marriage(e)
        out[e] = {"year": s["year"], "value": s["value"]}
    k = int(np.argmax(us["value"]))
    out["peak_year"], out["peak"] = us["year"][k], us["value"][k]
    k = int(np.argmin(us["value"]))
    out["low_year"], out["low"] = us["year"][k], us["value"][k]
    out["y1932"], out["y2022"], out["y1886"] = usm[1932], usm[2022], usm[1886]
    out["missing"] = [y for y in years if y not in usm]
    return out


def compute_melody() -> dict:
    from explainer.music.monochord.audio import Clip, ClipStore

    f = compute_film()
    years = f["years"]
    idx = np.linspace(0, len(years) - 1, 92).round().astype(int)        # about 92 notes, as in Part 16
    times = [f["times"][i] for i in idx]
    mel = score.data_melody(np.array(f["us"])[idx], MELODY_SECONDS, times=times, act=4, log=False, low=45, high=84)
    events = {"film_end": f["times"][-1] + 6.0, "first": times[0], "half": times[len(times) // 2]}
    clip = Clip(mel["y"], score.SR, events=events,
                notes=[{"t": float(t), "dur": 0.3, "hz": score.hz(nn), "name": str(years[i])}
                       for t, nn, i in zip(times, mel["notes"], idx)],
                meta={"label": "US marriages per 1,000 people, 1886-2022 (OECD, US Census Bureau and CDC via Our "
                               "World in Data), as a tune (computed)", "kind": "synthesized"})
    ClipStore("econ17").save("intermission.melody", clip)
    return {"times": times, "notes": mel["notes"], "years": [years[i] for i in idx], "seconds": MELODY_SECONDS}


ITEMS = {
    "playit": compute_playit,
    "board": compute_board,
    "lattice": compute_lattice,
    "bridge": compute_bridge,
    "trade": compute_trade,
    "huts": compute_huts,
    "kidneys": compute_kidneys,
    "assignment": compute_assignment,
    "lottery": compute_lottery,
    "roth": compute_roth,
    "schools": compute_schools,
    "dial": compute_dial,
    "film": compute_film,
    "melody": compute_melody,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
