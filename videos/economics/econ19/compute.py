"""Precompute every number in Part 19 of *Economics, Built* ("The Great Escape").

    python -m videos.economics.econ19.compute            # everything missing (seconds)
    python -m videos.economics.econ19.compute --force playit

Results are cached in ``.cache/econ19/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Data: the Data Room
(``explainer.economics.data``: the Bank of England's millennium dataset for England; the Maddison Project; Our World in
Data's long-run population, life expectancy, fertility and heights).  Models: Agora's long run (``agora.malthus``), with
the Island's Part 19 truths.

Items:
    playit      England's real GDP per head and real wages, 1270-2016, and the five candidate years
    malthus     the Malthusian island: a plague in year 100, a better plough in year 250
    vital       births and deaths per 1,000 against income (the diagram)
    elasticity  England's labour demand curve: log wages on log population, before and after 1600
    plague      England's population and real wages around the Black Death, 1300-1700
    divergence  Maddison's GDP per head, 1000-1850: Britain, the Netherlands, Italy, China, Japan, India
    industrial  growth of English GDP per head by period, 1700-1913; Engels's pause, 1780-1850
    transition  life expectancy and fertility: Britain, Sweden, the world and four countries
    unified     the unified growth toy, and the quantity-quality curve
    heights     men's height by decade of birth: Britain, the Netherlands, Sweden, the United States, France
    dial        English living standards, 1300-1700, three ways
    noise       Kelly's spatial noise: how often unrelated smooth fields look significantly related
    ehrlich     the world's population in 1968 and 2022
    film        the intermission's data film: GDP per head 1820-2022 for eight countries (Maddison)
    melody      its data melody: the world's GDP per head (Maddison), 1820-2022
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.economics import data, dials, island, score
from explainer.economics.agora import malthus as ml

CACHE = Cache("econ19")
load = CACHE.load
TRUTH = island.truths(19)


def _england():
    m = data.millennium()
    return m, {y: k for k, y in enumerate(m["year"])}


def _at(m, idx, key, y):
    return float(m[key][idx[y]])


def compute_playit() -> dict:
    m, idx = _england()
    years = [y for y in m["year"] if 1270 <= y <= 2016]
    g = [_at(m, idx, "gdppc", y) for y in years]
    w = [_at(m, idx, "real_wage", y) for y in years]
    keys = (1270, 1350, 1500, 1650, 1700, 1750, 1800, 1850, 1900, 1950, 2016)
    # the last year whose real wage is below the 1450 high: after it, wages never fall back that far
    peak = _at(m, idx, "real_wage", 1450)
    beyond = max(y for y, v in zip(years, w) if v < peak and y < 2000) + 1
    return {"years": years, "gdppc": g, "wage": w, "options": list(TRUTH["playit"]["options"]),
            "key": {str(y): {"gdppc": _at(m, idx, "gdppc", y), "wage": _at(m, idx, "real_wage", y)} for y in keys},
            "growth_1270_1650": ml.cagr(_at(m, idx, "gdppc", 1270), _at(m, idx, "gdppc", 1650), 380),
            "growth_1650_1800": ml.cagr(_at(m, idx, "gdppc", 1650), _at(m, idx, "gdppc", 1800), 150),
            "growth_1800_2016": ml.cagr(_at(m, idx, "gdppc", 1800), _at(m, idx, "gdppc", 2016), 216),
            "ratio_1800_2016": _at(m, idx, "gdppc", 2016) / _at(m, idx, "gdppc", 1800),
            "wage_1450": peak, "wage_beyond_1450": beyond}


def compute_malthus() -> dict:
    t = TRUTH["malthus"]
    s = ml.simulate(t["years"], L0=1.0, beta=t["beta"], lam=t["lam"], ybar=t["ybar"], plague=t["plague"],
                    invention=t["invention"])
    L0 = ml.steady_state(1.0, beta=t["beta"])
    return {**s, "beta": t["beta"], "lam": t["lam"], "plague": list(t["plague"]), "invention": list(t["invention"]),
            "L_star_before": L0, "L_star_after": s["L_star"], "jump_y": s["y"][t["plague"][0]],
            "jump_y_invention": s["y"][t["invention"][0]], "half_life": float(np.log(2) / (t["lam"] * t["beta"]))}


def compute_vital() -> dict:
    y = np.linspace(0.6, 1.6, 101)
    b, d = ml.vital_rates(y)
    return {"y": y, "births": b, "deaths": d}


def compute_elasticity() -> dict:
    m, idx = _england()
    t = TRUTH["elasticity"]
    before = ml.wage_elasticity(m["year"], m["population"], m["real_wage"], *t["before"])
    after = ml.wage_elasticity(m["year"], m["population"], m["real_wage"], *t["after"])
    # decade means for the scatter, 1270-1859
    pts = []
    for d0 in range(1270, 1860, 10):
        ys = [y for y in range(d0, d0 + 10) if y in idx]
        p = np.mean([_at(m, idx, "population", y) for y in ys])
        w = np.mean([_at(m, idx, "real_wage", y) for y in ys])
        pts.append({"decade": d0, "pop": float(p), "wage": float(w)})
    return {"before": before, "after": after, "points": pts}


def compute_plague() -> dict:
    m, idx = _england()
    years = list(range(1300, 1701))
    keys = (1300, 1348, 1351, 1400, 1450, 1500, 1550, 1600, 1650, 1700)
    k = {str(y): {"pop": _at(m, idx, "population", y), "wage": _at(m, idx, "real_wage", y)} for y in keys}
    return {"years": years, "pop": [_at(m, idx, "population", y) for y in years],
            "wage": [_at(m, idx, "real_wage", y) for y in years], "key": k,
            "drop": 1 - k["1351"]["pop"] / k["1348"]["pop"], "wage_x_1400": k["1400"]["wage"] / k["1348"]["wage"],
            "wage_x_1450": k["1450"]["wage"] / k["1348"]["wage"]}


DIV = ("GBR", "NLD", "ITA", "CHN", "JPN", "IND")


def compute_divergence() -> dict:
    out = {}
    for c in DIV:
        g = data.maddison_country(c)
        pts = [(y, v) for y, v in zip(g["year"], g["gdppc"]) if v and np.isfinite(v) and 1000 <= y <= 1850]
        out[c] = {"year": [p[0] for p in pts], "gdppc": [float(p[1]) for p in pts]}

    def near(c, y):
        ys, vs = out[c]["year"], out[c]["gdppc"]
        k = int(np.argmin([abs(a - y) for a in ys]))
        return {"year": ys[k], "gdppc": vs[k]}
    return {"series": out, "at": {c: {str(y): near(c, y) for y in (1000, 1300, 1500, 1600, 1700, 1800, 1850)}
                                  for c in DIV}}


def compute_industrial() -> dict:
    m, idx = _england()
    spans = ((1700, 1760), (1760, 1800), (1800, 1830), (1830, 1870), (1870, 1913))
    growth = [{"first": a, "last": b, "gdppc": ml.cagr(_at(m, idx, "gdppc", a), _at(m, idx, "gdppc", b), b - a)}
              for a, b in spans]
    years = list(range(1770, 1851))
    base_g, base_w = _at(m, idx, "gdppc", 1780), _at(m, idx, "real_wage", 1780)
    gi = [100 * _at(m, idx, "gdppc", y) / base_g for y in years]
    wi = [100 * _at(m, idx, "real_wage", y) / base_w for y in years]
    return {"growth": growth, "years": years, "gdppc_index": gi, "wage_index": wi,
            "gdppc_1840": gi[years.index(1840)], "wage_1840": wi[years.index(1840)],
            "wage_growth_1780_1840": ml.cagr(base_w, _at(m, idx, "real_wage", 1840), 60),
            "gdppc_growth_1780_1840": ml.cagr(base_g, _at(m, idx, "gdppc", 1840), 60)}


def compute_transition() -> dict:
    out = {"life": {}, "fert": {}}
    for e in ("United Kingdom", "Sweden", "World", "India", "China", "Nigeria", "Japan", "South Korea"):
        le = data.longrun("life-expectancy", e)
        out["life"][e] = {"year": le["year"], "value": le["value"]}
        f = data.longrun("children-born-per-woman", e)
        out["fert"][e] = {"year": f["year"], "value": f["value"]}

    def at(series, e, y):
        d = out[series][e]
        return float(d["value"][d["year"].index(y)]) if y in d["year"] else None
    out["key"] = {"uk_le_1543": at("life", "United Kingdom", 1543), "uk_le_1850": at("life", "United Kingdom", 1850),
                  "uk_le_1950": at("life", "United Kingdom", 1950), "uk_le_2023": at("life", "United Kingdom", 2023),
                  "se_le_1800": at("life", "Sweden", 1800), "se_le_1900": at("life", "Sweden", 1900),
                  "se_tfr_1891": at("fert", "Sweden", 1891), "se_tfr_1935": at("fert", "Sweden", 1935),
                  "world_le_1800": at("life", "World", 1800), "world_le_2023": at("life", "World", 2023),
                  "world_tfr_1950": at("fert", "World", 1950), "world_tfr_2023": at("fert", "World", 2023),
                  "kor_tfr_1950": at("fert", "South Korea", 1950), "kor_tfr_2023": at("fert", "South Korea", 2023),
                  "nga_tfr_2023": at("fert", "Nigeria", 2023), "ind_tfr_2023": at("fert", "India", 2023)}
    return out


def compute_unified() -> dict:
    t = TRUTH["unified"]
    u = ml.unified(generations=t["generations"], phi=t["phi"])
    return {**u, "qq": ml.quantity_quality(), "threshold": ml.threshold()}


def compute_heights() -> dict:
    out = {}
    for e in ("United Kingdom", "Netherlands", "Sweden", "United States", "France"):
        h = data.longrun("height", e)
        out[e] = {"year": h["year"], "value": h["value"]}
    uk = out["United Kingdom"]
    k = {y: v for y, v in zip(uk["year"], uk["value"])}
    return {"series": out, "uk": {str(y): k[y] for y in (1710, 1760, 1810, 1840, 1850, 1870, 1900, 1950, 1960) if
                                  y in k}}


def compute_dial() -> dict:
    d = dials.DIALS["preindustrial_growth"]
    m, idx = _england()
    mine = {"gdppc": 100 * ml.cagr(_at(m, idx, "gdppc", 1300), _at(m, idx, "gdppc", 1700), 400),
            "real_wage": 100 * ml.cagr(_at(m, idx, "real_wage", 1300), _at(m, idx, "real_wage", 1700), 400),
            "earnings_days": 100 * ml.cagr(_at(m, idx, "earnings_days", 1300), _at(m, idx, "earnings_days", 1700),
                                           400)}
    for e, k in zip(d.estimates, ("gdppc", "real_wage", "earnings_days")):
        assert abs(e.value - round(mine[k], 3)) < 1e-3, (e.who, e.value, mine[k])
    return {"computed": mine, "doubling": {k: float(np.log(2) / np.log(1 + v / 100)) for k, v in mine.items()}}


def compute_noise() -> dict:
    return ml.spatial_noise(**TRUTH["noise"])


def compute_ehrlich() -> dict:
    p = data.longrun("population", "World")
    k = dict(zip(p["year"], p["value"]))
    return {"pop_1968": k[1968], "pop_2022": k[2022], "growth_1968": k[1969] / k[1968] - 1}


# ---------------------------------------------------------------------------------------------------------------
# the intermission: the great divergence, and the great convergence

FILM_SECONDS = 40.0
MELODY_SECONDS = 55.0
FILM = ("GBR", "USA", "JPN", "KOR", "CHN", "IND", "NGA")


def film_time(k: int, n: int) -> float:
    return 1.5 + FILM_SECONDS * k / (n - 1)


def compute_film() -> dict:
    years = list(range(1820, 2023))
    out = {"years": years, "times": [film_time(k, len(years)) for k in range(len(years))]}
    for c in FILM:
        g = data.maddison_country(c)
        pts = {y: float(v) for y, v in zip(g["year"], g["gdppc"]) if v and np.isfinite(v) and y >= 1820}
        ys = sorted(pts)
        out[c] = [float(np.exp(np.interp(y, ys, np.log([pts[a] for a in ys])))) if ys[0] <= y else None
                  for y in years]
        out[c + "_first"] = ys[0]
    w = data.maddison_world()
    wy, wv = w["year"], w["World"]
    keep = [(y, v) for y, v in zip(wy, wv) if v and np.isfinite(v)]
    out["World"] = [float(np.exp(np.interp(y, [a for a, _ in keep], np.log([b for _, b in keep])))) for y in years]
    idx = {y: k for k, y in enumerate(years)}
    out["key"] = {c: {str(y): out[c][idx[y]] for y in (1820, 1870, 1913, 1950, 1980, 2000, 2022)
                      if out[c][idx[y]] is not None} for c in (*FILM, "World")}
    out["ratio_1820"] = out["GBR"][idx[1820]] / out["IND"][idx[1820]] if out["IND"][idx[1820]] else None
    return out


def compute_melody() -> dict:
    from explainer.music.monochord.audio import Clip, ClipStore

    f = compute_film()
    years = f["years"]
    idx = np.arange(0, len(years), 2)
    times = [f["times"][i] for i in idx]
    mel = score.data_melody(np.array(f["World"])[idx], MELODY_SECONDS, times=times, act=5, log=True, low=45, high=84)
    events = {"film_end": f["times"][-1] + 6.0, "first": times[0], "half": times[len(times) // 2]}
    clip = Clip(mel["y"], score.SR, events=events,
                notes=[{"t": float(t), "dur": 0.25, "hz": score.hz(nn), "name": str(years[i])}
                       for t, nn, i in zip(times, mel["notes"], idx)],
                meta={"label": "the world's GDP per head, 1820-2022 (Maddison Project Database 2023), as a tune, "
                               "on a log scale (computed)", "kind": "synthesized"})
    ClipStore("econ19").save("intermission.melody", clip)
    return {"times": times, "notes": mel["notes"], "years": [years[i] for i in idx], "seconds": MELODY_SECONDS}


ITEMS = {
    "playit": compute_playit,
    "malthus": compute_malthus,
    "vital": compute_vital,
    "elasticity": compute_elasticity,
    "plague": compute_plague,
    "divergence": compute_divergence,
    "industrial": compute_industrial,
    "transition": compute_transition,
    "unified": compute_unified,
    "heights": compute_heights,
    "dial": compute_dial,
    "noise": compute_noise,
    "ehrlich": compute_ehrlich,
    "film": compute_film,
    "melody": compute_melody,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
