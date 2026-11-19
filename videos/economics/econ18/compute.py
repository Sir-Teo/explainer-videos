"""Precompute every number in Part 18 of *Economics, Built* ("Social Choice and Welfare").

    python -m videos.economics.econ18.compute            # everything missing (seconds)
    python -m videos.economics.econ18.compute --force playit

Results are cached in ``.cache/econ18/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Data: the Data Room
(``explainer.economics.data``: V-Dem's electoral democracy index via Our World in Data; the UNDP's Human Development
Report data; FRED's CPI-U for converting dollars; transcribed values of a statistical life and Duverger's law).  Models:
Agora's social choice module (``agora.choice``), with the Island's Part 18 truths.

Items:
    playit      the 38 islanders: tallies and winners under five rules
    cycle       Condorcet's three voters, and who wins under each agenda
    iia         Borda's failure of independence, found on the Play it ballots
    pivot       Geanakoplos's first step on a dictatorship
    peaks       single-peaked voters: the median beats everything
    strategy    blocs who gain by misreporting under each rule
    welfare     five incomes: utilitarian, Rawlsian, Atkinson's family; Okun's leaky bucket
    veil        Harsanyi's and Rawls's choices between two societies
    pareto      Scitovsky's reversal and Sen's liberal paradox
    cba         a jetty judged with and without distributional weights
    vsl         the arithmetic of a statistical life, and the dial's rows
    discount    a benefit a century away at three discount rates
    hdi         income against life expectancy and the HDI, 2023
    film        the intermission's data film: electoral democracy, 1789-2025
    melody      its data melody: the world's index, every other year
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.economics import data, dials, island, score
from explainer.economics.agora import choice as ch
from explainer.economics.data import tables

CACHE = Cache("econ18")
load = CACHE.load
TRUTH = island.truths(18)
PROF = [(n, tuple(r)) for n, r in TRUTH["playit"]["profile"]]


def compute_playit() -> dict:
    ir = ch.instant_runoff(PROF)
    ru = ch.runoff(PROF)
    return {"profile": [[n, list(r)] for n, r in PROF], "winners": ch.all_rules(PROF),
            "plurality": ch.plurality(PROF)["tally"], "runoff": {"finalists": list(ru["finalists"]),
                                                                 "votes": list(ru["votes"])},
            "irv": ir["rounds"], "borda": ch.borda(PROF)["points"], "pairwise": ch.pairwise(PROF),
            "copeland": ch.copeland(PROF)["score"], "voters": sum(n for n, _ in PROF)}


def compute_cycle() -> dict:
    m = ch.majority_cycle()
    ag = ch.agendas(m["profile"])
    return {**m, "agenda_list": {c: [list(o) for o in v] for c, v in ag.items()}}


def compute_iia() -> dict:
    return ch.iia_violation(PROF)


def compute_pivot() -> dict:
    return ch.geanakoplos_pivot(**TRUTH["arrow"])


def compute_peaks() -> dict:
    return ch.single_peaked(**TRUTH["peaks"])


def compute_strategy() -> dict:
    return {r: ch.manipulations(PROF, r) for r in ("plurality", "runoff", "instant runoff", "Borda")}


def compute_welfare() -> dict:
    eps = np.linspace(0, 6, 61)
    w = ch.welfare(TRUTH["incomes"], tuple(float(e) for e in eps))
    pick = ch.welfare(TRUTH["incomes"])
    return {"incomes": list(TRUTH["incomes"]), "eps": eps, "ede": [w["ede"][float(e)] for e in eps],
            "atkinson": [w["atkinson"][float(e)] for e in eps], "mean": w["mean"], "min": w["min"],
            "table": {str(k): v for k, v in pick["ede"].items()}, "index": {str(k): v for k, v in
                                                                       pick["atkinson"].items()},
            # Okun's leaky bucket: the share of a dollar taken from the richest that may leak away on its way to the
            # poorest before the transfer lowers welfare, 1 - (poorest / richest)^e
            "leak": {str(e): 1 - (min(TRUTH["incomes"]) / max(TRUTH["incomes"])) ** e for e in (0.0, 0.5, 1.0, 2.0)}}


def compute_veil() -> dict:
    v = ch.veil(TRUTH["veil"]["A"], TRUTH["veil"]["B"], (0.0, 0.5, 1.0, 2.0, 5.0, 20.0))
    eps = np.linspace(0, 8, 81)
    va = ch.welfare(TRUTH["veil"]["A"], tuple(float(e) for e in eps))
    vb = ch.welfare(TRUTH["veil"]["B"], tuple(float(e) for e in eps))
    cross = next(float(e) for e in eps if vb["ede"][float(e)] <= va["ede"][float(e)])
    return {"harsanyi": {str(k): x for k, x in v["harsanyi"].items()}, "rawls": v["rawls"],
            "A": list(TRUTH["veil"]["A"]), "B": list(TRUTH["veil"]["B"]), "eps": eps,
            "ede_A": [va["ede"][float(e)] for e in eps], "ede_B": [vb["ede"][float(e)] for e in eps],
            "cross": cross, "mean_A": va["mean"], "mean_B": vb["mean"]}


def compute_pareto() -> dict:
    s = ch.scitovsky()
    return {"scitovsky": {"s1": s["s1"], "s2": s["s2"], "u1": s["utility_s1"], "u2": s["utility_s2"],
                          "1_to_2": s["1_to_2"], "2_to_1": s["2_to_1"],
                          "split_12": [list(map(float, x)) for x in s["split_12"]],
                          "split_21": [list(map(float, x)) for x in s["split_21"]]},
            "liberal": ch.liberal_paradox()}


def compute_cba() -> dict:
    """A jetty that gives the richest islander 30 baskets' worth and costs the poorest 10, judged with no weights and
    with Atkinson's weights (mean income / own income)^e."""
    inc = TRUTH["incomes"]
    mean = float(np.mean(inc))
    who = [("ana", max(inc), 30.0), ("friday", min(inc), -10.0)]
    net = {}
    for e in (0.0, 0.5, 1.0):
        net[str(e)] = {"weights": [(mean / y) ** e for _, y, _ in who],
                       "net": float(sum((mean / y) ** e * g for _, y, g in who))}
    return {"who": [list(w) for w in who], "mean": mean, "net": net}


def compute_vsl() -> dict:
    t = TRUTH["vsl"]
    rows = [(e.who, e.year, e.design, e.sample, e.value, e.lo, e.hi) for e in dials.DIALS["vsl"].estimates]
    return {"extra_risk": t["extra_risk"], "extra_pay": t["extra_pay"], "vsl": t["extra_pay"] / t["extra_risk"],
            "per_10000": t["extra_pay"], "rows": rows, "table": tables.VSL.data}


def compute_discount() -> dict:
    t = TRUTH["discount"]
    pv = {str(r): t["amount"] / (1 + r) ** t["years"] for r in t["rates"]}
    yrs = np.arange(0, t["years"] + 1)
    curves = {str(r): (1 / (1 + r) ** yrs).tolist() for r in t["rates"]}
    return {**t, "pv": pv, "years_axis": yrs, "curves": curves}


def compute_hdi() -> dict:
    rows = []
    for r in data.hdr():
        if 2023 in r["hdi"] and 2023 in r["le"] and 2023 in r["gnipc"]:
            rows.append({"code": r["code"], "country": r["country"], "hdi": r["hdi"][2023], "le": r["le"][2023],
                         "gni": r["gnipc"][2023]})
    rows.sort(key=lambda x: -x["gni"])
    for k, r in enumerate(rows):
        r["gni_rank"] = k + 1
    for k, r in enumerate(sorted(rows, key=lambda x: -x["hdi"])):
        r["hdi_rank"] = k + 1
    gap = sorted(rows, key=lambda r: r["gni_rank"] - r["hdi_rank"])
    named = {c: next((r for r in rows if r["code"] == c), None) for c in ("USA", "CUB", "LKA", "QAT", "CRI", "GNQ",
                                                                        "VNM", "NGA", "KWT", "CHL")}
    return {"rows": rows, "biggest_rise": gap[-5:], "biggest_fall": gap[:5], "named": named}


# ---------------------------------------------------------------------------------------------------------------
# the intermission: two centuries of democracy

FILM_SECONDS = 40.0
MELODY_SECONDS = 55.0
FILM_LINES = ("World", "United States", "United Kingdom", "France", "India")


def film_time(k: int, n: int) -> float:
    return 1.5 + FILM_SECONDS * k / (n - 1)


def compute_film() -> dict:
    series = {e: data.democracy(e) for e in FILM_LINES}
    years = sorted(set.intersection(*[set(s["year"]) for s in series.values()]))
    out = {"years": years, "times": [film_time(k, len(years)) for k in range(len(years))]}
    for e, s in series.items():
        m = dict(zip(s["year"], s["value"]))
        out[e] = [float(m[y]) for y in years]
    w = out["World"]
    k = int(np.argmax(w))
    out["world_peak_year"], out["world_peak"] = years[k], w[k]
    out["world_1789"], out["world_last"], out["last_year"] = w[0], w[-1], years[-1]
    idx = {y: i for i, y in enumerate(years)}
    out["key"] = {e: {y: out[e][idx[y]] for y in (1848, 1900, 1920, 1945, 1950, 1975, 1990, 2012, years[-1])}
                  for e in FILM_LINES}
    return out


def compute_melody() -> dict:
    from explainer.music.monochord.audio import Clip, ClipStore

    f = compute_film()
    years = f["years"]
    idx = np.arange(0, len(years), 2)                  # every other year: about 118 notes
    times = [f["times"][i] for i in idx]
    mel = score.data_melody(np.array(f["World"])[idx], MELODY_SECONDS, times=times, act=4, log=False, low=45, high=84)
    events = {"film_end": f["times"][-1] + 6.0, "first": times[0], "half": times[len(times) // 2]}
    clip = Clip(mel["y"], score.SR, events=events,
                notes=[{"t": float(t), "dur": 0.25, "hz": score.hz(nn), "name": str(years[i])}
                       for t, nn, i in zip(times, mel["notes"], idx)],
                meta={"label": "the world's electoral democracy index, 1789-2025 (V-Dem v16 via Our World in Data), "
                               "as a tune (computed)", "kind": "synthesized"})
    ClipStore("econ18").save("intermission.melody", clip)
    return {"times": times, "notes": mel["notes"], "years": [years[i] for i in idx], "seconds": MELODY_SECONDS}


ITEMS = {
    "playit": compute_playit,
    "cycle": compute_cycle,
    "iia": compute_iia,
    "pivot": compute_pivot,
    "peaks": compute_peaks,
    "strategy": compute_strategy,
    "welfare": compute_welfare,
    "veil": compute_veil,
    "pareto": compute_pareto,
    "cba": compute_cba,
    "vsl": compute_vsl,
    "discount": compute_discount,
    "hdi": compute_hdi,
    "film": compute_film,
    "melody": compute_melody,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
