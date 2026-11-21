"""Precompute every number in Part 65 of *Economics, Built* ("The Economics of AI").

    python -m videos.economics.econ65.compute            # everything missing (about a minute)
    python -m videos.economics.econ65.compute --force race

Results are cached in ``.cache/econ65/<name>.json``; scenes call ``load(name)``.  Models: Agora's ``automation``
module (the task model, the J-curve, the Island's support desk, Hulten's arithmetic, growth with automated research,
Baumol's two sectors, the race between automation and capital, Varian's shoppers, a toy of frontier-model entry).
Data: the Maddison Project (GDP per head, 1930 and 2022), the Penn World Table 11.0 (hours worked and the labour
share), FRED (output per hour in American business; payroll employment), Rupp's transistors per microprocessor.

Items:
    keynes      Keynes's two forecasts against the record: living standards since 1930, hours since 1950
    engels      Engels's pause: real wages against GDP per head in England, 1760-1880 (the Bank of England's
                millennium series)
    tasks       the task model: automation in the short and long run, new tasks, the wage decomposition
    soso        so-so automation: the wage gain from automating a task by how much cheaper the machine is
    jcurve      a general-purpose technology's measured and true productivity
    desk        the Island's support desk: an assistant given to half the agents at random
    hulten      from tasks to aggregates: Acemoglu's arithmetic and two other readings
    growth      growth when research tasks are automated: shares 0, 50, 75, 90 and 100 percent
    baumol      two sectors, one automated: spending shares and aggregate growth
    race        wages when the automation frontier races capital: three scenarios
    nordhaus    Nordhaus's tests on the record: productivity growth by decade, the capital share, computing
    shoppers    Varian's model of sales: prices when a share of buyers has a shopping agent
    entry       a toy of frontier-model entry when training costs grow faster than the market
    frey        payroll employment since Frey and Osborne's 2013 paper
    film        the intermission's data film: annual hours worked per worker, six countries, 1950-2023
    melody      its data melody
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.economics import data
from explainer.economics import score as SC
from explainer.economics.agora import automation as A

CACHE = Cache("econ65")
load = CACHE.load
TRUTH = {"desk": "each agent's skill and the assistant's effect on them are planted (agora.automation.support_desk)",
         "race": "the automation frontier and the technology are assumed (agora.automation.race)"}
FILM_SECONDS = 46.0
MELODY_SECONDS = FILM_SECONDS + 12.0
FILM_YEARS = (1950.0, 2024.0)
COUNTRIES = ("USA", "GBR", "DEU", "FRA", "JPN", "KOR")
SHARES = (0.0, 0.5, 0.75, 0.9, 1.0)


def film_time(year: float) -> float:
    a, b = FILM_YEARS
    return 2.0 + (year - a) / (b - a) * (FILM_SECONDS - 4.0)


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


def compute_keynes() -> dict:
    k = A.keynes(COUNTRIES)
    hours = {}
    for c, h in k["hours"].items():
        d = dict(zip(h["year"], h["hours"]))
        first = min(y for y in d if y >= 1950)
        last = max(d)
        hours[c] = {"name": h["name"], "first_year": first, "first": d[first], "last_year": last, "last": d[last],
                    "fall": 1 - d[last] / d[first]}
    ratio = k["ratio"]
    return _jsonable({"ratio": ratio, "ratio_min": min(ratio.values()), "ratio_max": max(ratio.values()),
                      "hours": hours, "keynes_hours": k["keynes_hours"],
                      "lowest": min(hours, key=lambda c: hours[c]["last"])})


def compute_engels() -> dict:
    m = data.millennium()
    y = np.array(m["year"])
    keep = (y >= 1760) & (y <= 1880)
    base = {k: dict(zip(m["year"], m[k]))[1770] for k in ("real_wage", "gdppc")}
    out = {"year": y[keep]}
    for k in ("real_wage", "gdppc"):
        out[k] = 100 * np.array(m[k], float)[keep] / base[k]
    d = {k: dict(zip(out["year"].tolist(), out[k].tolist())) for k in ("real_wage", "gdppc")}
    out["at"] = {str(yy): {"real_wage": d["real_wage"][yy], "gdppc": d["gdppc"][yy]} for yy in (1800, 1840, 1870)}
    return _jsonable(out)


def compute_tasks() -> dict:
    return _jsonable(A.task_paths())


def compute_soso() -> dict:
    return _jsonable(A.so_so())


def compute_jcurve() -> dict:
    return _jsonable(A.j_curve())


def compute_desk() -> dict:
    return _jsonable(A.support_desk())


def compute_hulten() -> dict:
    out = A.hulten_scenarios()
    ex = np.linspace(0.05, 0.6, 12)
    ad = np.linspace(0.1, 1.0, 10)
    grid = A.hulten_ai(ex[:, None], ad[None, :], 0.27)["tfp"]
    out["grid"] = {"exposed": ex, "adopted": ad, "tfp": grid}
    return _jsonable(out)


def compute_growth() -> dict:
    paths = {}
    for b in SHARES:
        g = A.ideas_growth(b)
        paths[f"{b:.2f}"] = {"year": g["year"], "growth": g["growth"], "exploded": g["exploded"],
                             "people_share": g["people_share"],
                             "peak": float(np.max(g["growth"])), "peak_year": int(np.argmax(g["growth"])),
                             "at100": g["growth"][100] if len(g["growth"]) > 100 else None,
                             "last_year": g["year"][-1]}
    return _jsonable({"shares": list(SHARES), "paths": paths})


def compute_baumol() -> dict:
    return _jsonable(A.baumol())


def compute_race() -> dict:
    return _jsonable(A.race_scenarios())


def compute_nordhaus() -> dict:
    f = data.fred("OPHNFB")
    yrs = np.array([int(d[:4]) for d in f["date"]])
    v = np.array(f["value"], float)
    annual = {y: v[yrs == y].mean() for y in np.unique(yrs) if (yrs == y).sum() == 4}
    decades = []
    for a in (1950, 1960, 1970, 1980, 1990, 2000, 2010):
        b = a + 10
        if a in annual and b in annual:
            decades.append({"from": a, "to": b, "growth": (annual[b] / annual[a]) ** 0.1 - 1})
    last = max(annual)
    decades.append({"from": 2020, "to": last, "growth": (annual[last] / annual[2020]) ** (1 / (last - 2020)) - 1})
    q = {d: x for d, x in zip(f["date"], v)}

    def rate(a, b):
        return (q[f"{b}-01-01"] / q[f"{a}-01-01"]) ** (1 / (b - a)) - 1
    last_q = max(int(d[:4]) for d in f["date"] if d.endswith("-01-01"))
    periods = [{"from": a, "to": b, "growth": rate(a, b)}
               for a, b in ((1948, 1973), (1973, 1995), (1995, 2004), (2004, 2019), (2019, last_q))]
    rows = [r for r in data.pwt("USA") if r["year"] >= 1950 and np.isfinite(r["labsh"])]
    cap = {"year": [r["year"] for r in rows], "capital_share": [1 - r["labsh"] for r in rows]}
    t = data.transistors()
    ty, tv = np.array(t["year"], float), np.array(t["transistors"], float)
    doubling = 1 / np.polyfit(ty, np.log2(tv), 1)[0]
    return _jsonable({"decades": decades, "periods": periods, "last_year": last, "capital": cap, "doubling": doubling,
                      "cap_first": cap["capital_share"][0], "cap_last": cap["capital_share"][-1],
                      "cap_first_year": cap["year"][0], "cap_last_year": cap["year"][-1],
                      "retrieved": data.FRED_RETRIEVED.get("OPHNFB")})


def compute_shoppers() -> dict:
    return _jsonable(A.shoppers())


def compute_entry() -> dict:
    return _jsonable(A.frontier_entry())


def compute_frey() -> dict:
    p = data.fred("PAYEMS")
    d = dict(zip(p["date"], p["value"]))
    start, last = "2013-09-01", p["date"][-1]
    return _jsonable({"start": start, "start_value": d[start], "last": last, "last_value": d[last],
                      "growth": d[last] / d[start] - 1, "retrieved": data.FRED_RETRIEVED.get("PAYEMS")})


def compute_film() -> dict:
    k = A.keynes(COUNTRIES)
    series = {}
    for c, h in k["hours"].items():
        ys = [y for y in h["year"] if y >= 1950]
        hs = [x for y, x in zip(h["year"], h["hours"]) if y >= 1950]
        series[c] = {"name": h["name"], "year": ys, "hours": hs, "t": [film_time(y) for y in ys]}
    years = sorted(set().union(*[set(s["year"]) for s in series.values()]))
    mean = []
    for y in years:
        vals = [s["hours"][s["year"].index(y)] for s in series.values() if y in s["year"]]
        mean.append(float(np.mean(vals)))
    return _jsonable({"series": series, "years": years, "mean": mean, "t": [film_time(y) for y in years],
                      "keynes": k["keynes_hours"], "first": years[0], "last": years[-1]})


def compute_melody() -> dict:
    from explainer.music.monochord.audio import Clip, ClipStore

    f = compute_film()
    vals = np.array(f["mean"])
    times = f["t"]
    mel = SC.data_melody(vals, MELODY_SECONDS, times=times, act=12, log=False, low=48, high=79)
    events = {"film_end": film_time(FILM_YEARS[1]) + 4.0, "first": times[0]}
    clip = Clip(mel["y"], SC.SR, events=events,
                notes=[{"t": float(tt), "dur": 0.2, "hz": SC.hz(nn), "name": f"{x:.0f} hours"}
                       for tt, nn, x in zip(times, mel["notes"], vals)],
                meta={"label": "average annual hours worked per worker in six countries, 1950-2023 (Penn World "
                               "Table 11.0), as a falling tune (computed)", "kind": "synthesized"})
    ClipStore("econ65").save("intermission.melody", clip)
    return {"times": times, "notes": mel["notes"], "seconds": MELODY_SECONDS}


ITEMS = {
    "keynes": compute_keynes,
    "engels": compute_engels,
    "tasks": compute_tasks,
    "soso": compute_soso,
    "jcurve": compute_jcurve,
    "desk": compute_desk,
    "hulten": compute_hulten,
    "growth": compute_growth,
    "baumol": compute_baumol,
    "race": compute_race,
    "nordhaus": compute_nordhaus,
    "shoppers": compute_shoppers,
    "entry": compute_entry,
    "frey": compute_frey,
    "film": compute_film,
    "melody": compute_melody,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
