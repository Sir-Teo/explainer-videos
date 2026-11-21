"""Precompute every number in Part 47 of *Economics, Built* ("Political Economy").

    python -m videos.economics.econ47.compute            # everything missing (under a minute)
    python -m videos.economics.econ47.compute --force senate

Results are cached in ``.cache/econ47/<name>.json`` (+ ``.npz``); scenes call ``load(name)``. Data: the Data Room
(``explainer.economics.data``: Cattaneo, Frandsen and Titiunik's Senate elections, via the R package rdrobust; the
World Bank's Pink Sheet sugar prices, world and US; V-Dem's electoral democracy index via Our World in Data; the World
Bank's tax revenue and the Worldwide Governance Indicators' control of corruption; the tables of Part 47). Models:
Agora's political economy (``agora.politics``) with the Island's Part 47 truths.

Items:
    roads       the Island's road projects: missing spending by arm, audits and meetings, perceptions
    olson       a group's lobbying effort as the group grows
    sugar       US and world sugar prices, 1960-2026 (World Bank), and the stakes per head of farms and consumers
    tokens      Play it: the public good or the lobby, Nash against the best
    tullock     rent seeking: spending per player and the share of the prize dissipated as players enter
    voting      probabilistic voting: transfers to swing and organized groups
    senate      Senate elections, 1914-2010: the party's vote share at the seat's next election against today's
                margin; the jump at zero by local linear regression, and its robustness to the bandwidth
    mayors      first-term and lame-duck mayors: the share misappropriated
    franchise   the elite's choice, promise, the vote or revolution, over threats and their costs
    wgi         control of corruption against GDP per head (World Bank)
    tax         tax revenue against GDP per head (World Bank)
    democracy   V-Dem's index for countries that democratized and countries that backslid
    conflict    rainfall, growth and conflict: OLS and 2SLS
    persuasion  the persuasion rate on an Island example
    cycle       an election cycle in unemployment and inflation, and delegation
    film        the intermission's data film: the world's electoral democracy index, 1900-2025
    melody      its data melody
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.economics import data, island, score
from explainer.economics.agora import politics

CACHE = Cache("econ47")
load = CACHE.load
TRUTH = island.truths(47)
FILM_SECONDS = 52.0
MELODY_SECONDS = FILM_SECONDS + 8.0
H_SENATE = 17.754     # rdrobust's MSE-optimal bandwidth for these data (its documented example)


def compute_roads() -> dict:
    return politics.road_projects(**TRUTH["roads"])


def compute_olson() -> dict:
    O = TRUTH["olson"]
    n = np.arange(1, 121)
    e = politics.olson_effort(O["B"], n, O["K"])
    p = e / (e + O["K"])
    return {"n": n.tolist(), "effort": e.tolist(), "p": p.tolist(), "B": O["B"], "K": O["K"]}


def compute_sugar() -> dict:
    u, w = data.pinksheet("sugar_us"), data.pinksheet("sugar")
    years: dict = {}
    for m, a, b in zip(u["month"], u["value"], w["value"]):
        if a is not None and b is not None and np.isfinite(a) and np.isfinite(b):
            years.setdefault(int(m[:4]), []).append((a, b))
    ys = sorted(y for y in years if len(years[y]) >= 6)
    us = [float(np.mean([a for a, _ in years[y]])) for y in ys]
    wd = [float(np.mean([b for _, b in years[y]])) for y in ys]
    ratio = [a / b for a, b in zip(us, wd)]
    S = TRUTH["sugar"]
    g = politics.group_contest(**S)
    recent = [r for y, r in zip(ys, ratio) if y >= 2015]
    return {"year": ys, "us": us, "world": wd, "ratio": ratio, "median_ratio": float(np.median(ratio)),
            "recent_ratio": float(np.mean(recent)), "per_farm": S["B_small"] / S["n_small"],
            "per_person": S["B_large"] / S["n_large"], "contest": g, "last_year": ys[-1]}


def compute_tokens() -> dict:
    T = TRUTH["tokens"]
    g = politics.tokens_game(**T)
    N = T["N"]
    # a few illustrative societies: all build; all lobby at the equilibrium; half build, half lobby
    half_b = np.r_[np.full(N // 2, T["endowment"]), np.zeros(N - N // 2)]
    half_l = np.r_[np.zeros(N // 2), np.full(N - N // 2, 36.0)]
    mixed = politics.tokens_game(**T, build=half_b, lobby=half_l)
    return {**g, "mixed_builders": mixed["payoffs"][0], "mixed_lobbyists": mixed["payoffs"][-1], **T}


def compute_tullock() -> dict:
    ns = list(range(2, 21))
    rows = [politics.tullock(1.0, n) for n in ns]
    return {"n": ns, "each": [r["each"] for r in rows], "dissipated": [r["dissipated"] for r in rows]}


def compute_voting() -> dict:
    V = TRUTH["voting"]
    plain = politics.probabilistic_voting(V["alpha"], V["phi"], V["income"])
    lobby = politics.probabilistic_voting(V["alpha"], V["phi"], V["income"], V["organized"], V["h"])
    return {"plain": plain, "lobby": lobby, **{k: list(v) if isinstance(v, tuple) else v for k, v in V.items()}}


def compute_senate() -> dict:
    d = data.rdsenate()
    x, y = np.array(d["margin"], float), np.array(d["vote"], float)
    main = politics.rd_local_linear(x, y, H_SENATE)
    rob = [{"h": h, **politics.rd_local_linear(x, y, h)} for h in (5.0, 10.0, H_SENATE, 25.0, 50.0, 100.0)]
    uni = politics.rd_local_linear(x, y, H_SENATE, kernel="uniform")
    bins = politics.rd_bins(x, y, -50, 50, 2.5)
    ok = np.isfinite(x) & np.isfinite(y)
    yr = np.array(d["year"], float)[ok]
    return {"jump": main["jump"], "se": main["se"], "h": H_SENATE, "n_left": main["n_left"],
            "n_right": main["n_right"], "fit_left": main["fit_left"], "fit_right": main["fit_right"],
            "robust": rob, "uniform": uni["jump"], "bins": bins, "n": int(ok.sum()), "first": int(yr.min()),
            "last": int(yr.max())}


def compute_mayors() -> dict:
    return politics.mayors(**TRUTH["mayors"])


def compute_franchise() -> dict:
    F = TRUTH["franchise"]
    qs = np.linspace(0.02, 0.98, 25)
    mus = np.linspace(0.40, 0.95, 23)
    m = politics.franchise_map(qs, mus, **F)
    ex = {f"{q:.1f}": politics.franchise(q, 0.6, **F) for q in (0.1, 0.9)}
    return {**m, "examples": ex, **F}


def _wdi(col: str) -> dict:
    rows = data.wdi_state()
    keep = [r for r in rows if np.isfinite(r[col]) and np.isfinite(r["gdppc"])]
    x = np.log10([r["gdppc"] for r in keep])
    y = np.array([r[col] for r in keep])
    b = np.polyfit(x, y, 1)
    q = np.quantile(x, [0.25, 0.75])
    pick = {}
    for c in ("USA", "DNK", "SGP", "CHN", "IND", "NGA", "RUS", "VEN", "BRA", "KEN", "BGD", "DEU", "GEO", "RWA",
              "BWA"):
        for r in keep:
            if r["code"] == c:
                pick[c] = {"name": r["country"], "x": float(np.log10(r["gdppc"])), "y": float(r[col])}
    return {"x": x.tolist(), "y": y.tolist(), "codes": [r["code"] for r in keep], "slope": float(b[0]),
            "intercept": float(b[1]), "corr": float(np.corrcoef(x, y)[0, 1]), "n": len(keep),
            "median_poorest": float(np.median(y[x <= q[0]])), "median_richest": float(np.median(y[x >= q[1]])),
            "pick": pick}


def compute_wgi() -> dict:
    return _wdi("cc")


def compute_tax() -> dict:
    return _wdi("tax")


DEMOCRATIZED = (("Spain", 1977), ("Chile", 1990), ("South Korea", 1988), ("Poland", 1989), ("Taiwan", 1996),
                ("Indonesia", 1999), ("Ghana", 1996))
BACKSLID = ("Hungary", "Turkey", "Venezuela", "Russia")


def compute_democracy() -> dict:
    out = {"democratized": {}, "backslid": {}}
    for c, yr in DEMOCRATIZED:
        d = data.democracy(c)
        out["democratized"][c] = {"year": d["year"], "value": d["value"], "transition": yr}
    for c in BACKSLID:
        d = data.democracy(c)
        out["backslid"][c] = {"year": d["year"], "value": d["value"],
                              "peak": float(max(v for y, v in zip(d["year"], d["value"]) if y >= 1990)),
                              "last": float(d["value"][-1])}
    w = data.democracy("World")
    out["world"] = {"year": w["year"], "value": w["value"]}
    return out


def compute_conflict() -> dict:
    return politics.rain_conflict(**TRUTH["conflict"])


def compute_persuasion() -> dict:
    # an Island town where a new channel reaches 30% of homes against 20% elsewhere, and the party's share is 50.4%
    # against 50.0%: the persuasion rate
    yT, yC, eT, eC = 0.504, 0.500, 0.30, 0.20
    return {"yT": yT, "yC": yC, "eT": eT, "eC": eC, "rate": politics.persuasion_rate(yT, yC, eT, eC)}


def compute_cycle() -> dict:
    return politics.election_cycle(**TRUTH["cycle"])


def film_time(t: float, first: float = 1900.0, last: float = 2025.0) -> float:
    return 1.5 + FILM_SECONDS * (t - first) / (last - first)


def compute_film() -> dict:
    w = data.democracy("World")
    ys = [y for y in w["year"] if y >= 1900]
    vs = [v for y, v in zip(w["year"], w["value"]) if y >= 1900]
    k = int(np.argmax(vs))
    return {"t": ys, "v": vs, "times": [film_time(t) for t in ys], "first": vs[0], "last": vs[-1], "peak": vs[k],
            "peak_t": ys[k], "v1945": vs[ys.index(1945)], "v1990": vs[ys.index(1990)]}


def compute_melody() -> dict:
    from explainer.music.monochord.audio import Clip, ClipStore

    f = compute_film()
    vals = np.array(f["v"])
    times = f["times"]
    mel = score.data_melody(vals, MELODY_SECONDS, times=times, act=9, log=False, low=40, high=84)
    events = {"film_end": film_time(f["t"][-1]) + 6.0, "first": times[0], "y1945": film_time(1945),
              "y1990": film_time(1990), "peak": film_time(f["peak_t"])}
    clip = Clip(mel["y"], score.SR, events=events,
                notes=[{"t": float(tt), "dur": 0.3, "hz": score.hz(nn), "name": f"{x:.2f}"}
                       for tt, nn, x in zip(times, mel["notes"], vals)],
                meta={"label": "the world's electoral democracy index, 1900-2025 (V-Dem, via Our World in Data), as "
                               "a tune (computed)", "kind": "synthesized"})
    ClipStore("econ47").save("intermission.melody", clip)
    return {"times": times, "notes": mel["notes"], "seconds": MELODY_SECONDS}


ITEMS = {
    "roads": compute_roads,
    "olson": compute_olson,
    "sugar": compute_sugar,
    "tokens": compute_tokens,
    "tullock": compute_tullock,
    "voting": compute_voting,
    "senate": compute_senate,
    "mayors": compute_mayors,
    "franchise": compute_franchise,
    "wgi": compute_wgi,
    "tax": compute_tax,
    "democracy": compute_democracy,
    "conflict": compute_conflict,
    "persuasion": compute_persuasion,
    "cycle": compute_cycle,
    "film": compute_film,
    "melody": compute_melody,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
