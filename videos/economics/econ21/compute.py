"""Precompute every number in Part 21 of *Economics, Built* ("Growth II: Ideas and Institutions").

    python -m videos.economics.econ21.compute            # everything missing (seconds)
    python -m videos.economics.econ21.compute --force ah

Results are cached in ``.cache/econ21/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Data: the Data Room
(``explainer.economics.data``: Nordhaus's labour price of light and Bloom et al.'s research numbers, transcribed;
Acemoglu, Johnson and Robinson's base sample; the Penn World Table 11.0).  Models: Agora's ideas
(``agora.ideas``), misallocation (``agora.ge``) and the econometrician's 2SLS, with the Island's Part 21 truths.

Items:
    light        the labour price of light, from the open fire to the compact fluorescent bulb
    playit       the game's options and its answer
    replication  why ideas bring increasing returns
    ak           the AK economy
    romer        Romer's balanced path, its research share and its scale effect
    ah           Aghion and Howitt: decentralized and optimal research across step sizes; a simulated ladder
    semi         semi-endogenous growth: idea growth converging to lam n / (1 - phi); research productivity falling
    bloom        Bloom, Jones, Van Reenen and Webb's research effort and productivity
    plants       the Island's plants: misallocation in two economies, Hsieh and Klenow's measure
    ajr          settler mortality, expropriation risk and income: OLS, first stage, reduced form, 2SLS
    directed     directed technical change: the skill premium against relative supply, short and long run
    tfp          TFP levels relative to the United States across countries (PWT), for the levels chapter
    film         the intermission's data film: the labour price of light, 1800-1992
    melody       its data melody
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.economics import data, island, score
from explainer.economics.agora import econometrician as em
from explainer.economics.agora import ge
from explainer.economics.agora import ideas as idx
from explainer.economics.data import tables

CACHE = Cache("econ21")
load = CACHE.load
TRUTH = island.truths(21)


def _light_rows():
    return [dict(zip(("device", "tech", "year", "printed", "hours"), r)) for r in tables.NORDHAUS_LIGHT.data["rows"]]


def compute_light() -> dict:
    rows = _light_rows()
    by = {(r["device"], r["tech"], r["printed"]): r["hours"] for r in rows}
    tallow = by[("candle", "tallow", "1800")]
    cfl = by[("electric lamp", "compact fluorescent", "1992")]
    babylon = by[("Babylonian lamp", "sesame oil", "1750 B.C.")]
    edison = by[("electric lamp", "Edison carbon lamp", "1883")]
    dated = [r for r in rows if r["year"] is not None and r["year"] >= 1800]
    # the cheapest light available by each date (the frontier)
    years = sorted({r["year"] for r in dated})
    frontier = []
    best = np.inf
    for y in years:
        best = min(best, min(r["hours"] for r in dated if r["year"] <= y))
        frontier.append(best)
    return {"rows": rows, "tallow_1800": tallow, "cfl_1992": cfl, "babylon": babylon, "edison_1883": edison,
            "ratio_1800_1992": tallow / cfl, "ratio_babylon_1992": babylon / cfl,
            "rate_1800_1992": (cfl / tallow) ** (1 / 192) - 1, "seconds_1992": cfl * 3600,
            "frontier_years": years, "frontier": frontier,
            "overstatement": tables.NORDHAUS_LIGHT.data["traditional_overstatement"],
            "bias": tables.NORDHAUS_LIGHT.data["traditional_bias"]}


def compute_playit() -> dict:
    l_ = compute_light()
    opts = list(TRUTH["playit"]["options"])
    answer = min(range(len(opts)), key=lambda i: abs(np.log(opts[i]) - np.log(l_["cfl_1992"])))
    return {"options": opts, "answer": answer, "truth": l_["cfl_1992"], "start": l_["tallow_1800"],
            "ratio": l_["ratio_1800_1992"], "seconds": l_["seconds_1992"]}


def compute_replication() -> dict:
    return idx.replication()


def compute_ak() -> dict:
    a = idx.ak_path(s=0.2, A=0.4, delta=0.05, years=60)
    from explainer.economics.agora import growth as gr
    sol = gr.solow_path(0.2, 60, k0=gr.solow_steady(0.2, n=0, g=0, delta=0.05, alpha=1 / 3)["k"] * 0.25, n=0, g=0,
                        delta=0.05, alpha=1 / 3)
    return {**a, "solow_y": sol["y"], "solow_k": sol["k"]}


def compute_romer() -> dict:
    t = TRUTH["romer"]
    kw = {k: t[k] for k in ("delta", "alpha", "rho", "theta")}
    path = idx.romer_path(L=t["L"], years=80, **kw)
    scale = idx.romer_scale(np.linspace(0.2, 2.0, 37), **kw)
    sizes = {f"{L:g}": idx.romer_bgp(L=L, **kw) for L in t["sizes"]}
    return {**path, "scale": scale, "sizes": sizes, "params": kw}


def compute_ah() -> dict:
    t = TRUTH["ah"]
    kw = {k: t[k] for k in ("lam", "alpha", "rho", "L")}
    gammas = np.exp(np.linspace(np.log(1.005), np.log(3.0), 120))
    rows = [idx.ah_research(gamma=float(g), **kw) for g in gammas]
    cross = next(float(g) for g, r in zip(gammas, rows) if not r["too_much"] and r["n_star"] > 0)
    ladder = idx.ah_sectors(lam=t["lam"], n=t["n"], gamma=t["gamma"], years=t["years"], sectors=t["sectors"],
                            seed=t["seed"])
    at = idx.ah_research(gamma=t["gamma"], **kw)
    small = idx.ah_research(gamma=1.2, **kw)
    big = idx.ah_research(gamma=2.5, **kw)
    return {"gammas": gammas.tolist(), "n_dec": [r["n_dec"] for r in rows], "n_star": [r["n_star"] for r in rows],
            "cross": cross, "ladder": ladder, "at": at, "small": small, "big": big, "params": {**kw, "gamma": t["gamma"],
                                                                                 "n": t["n"]}}


def compute_semi() -> dict:
    t = TRUTH["semi"]
    s = idx.semi_endogenous(lam=t["lam"], phi=t["phi"], n=t["n"], theta=t["theta"], years=t["years"])
    return {**s, "params": t}


def compute_bloom() -> dict:
    return dict(tables.BLOOM_2020.data)


def compute_plants() -> dict:
    t = TRUTH["plants"]
    rng = np.random.default_rng(t["seed"])
    logA = rng.normal(0, t["sd_logA"], t["n"])
    out = {}
    for sd in t["sd_wedge"]:
        w = rng.normal(0, sd, t["n"])
        m = ge.misallocation(logA, w, sigma=t["sigma"])
        out[f"{sd:.2f}"] = {"log_tfpr": w.tolist(), **m}
    lo, hi = (f"{x:.2f}" for x in t["sd_wedge"])
    return {"economies": out, "sigma": t["sigma"], "n": t["n"], "lo": lo, "hi": hi}


def compute_ajr() -> dict:
    d = data.ajr()
    y, x, z = np.array(d["GDP"]), np.array(d["Exprop"]), np.array(d["logMort"])
    b_ols = np.polyfit(x, y, 1)
    fs = np.polyfit(z, x, 1)
    rf = np.polyfit(z, y, 1)
    iv = em.iv(y, x, z)
    n = len(y)
    # classical standard errors for the first stage (as AJR report)
    Z = np.column_stack([np.ones(n), z])
    u = x - Z @ fs[::-1]
    fs_se = float(np.sqrt(u @ u / (n - 2) * np.linalg.inv(Z.T @ Z)[1, 1]))
    return {"logMort": z.tolist(), "Exprop": x.tolist(), "GDP": y.tolist(), "neo": d["Neo"], "n": n,
            "ols": float(b_ols[0]), "first": float(fs[0]), "first_se": fs_se, "reduced": float(rf[0]),
            "iv": iv["estimate"], "iv_se": iv["se"], "F": iv["F"], "wald_ratio": float(rf[0] / fs[0]),
            "published": {"iv": 0.94, "iv_se": 0.16, "first": -0.61, "first_se": 0.13, "ols": 0.52},
            "mort_range": [float(np.min(d["Mort"])), float(np.max(d["Mort"]))]}


def compute_directed() -> dict:
    ratios = np.exp(np.linspace(np.log(0.5), np.log(2.0), 41))
    return {f"{s:g}": idx.directed(s, ratios) for s in TRUTH["directed"]["sigmas"]}


def compute_tfp() -> dict:
    rows = [r for r in data.pwt(year=2019) if np.isfinite(r["ctfp"]) and np.isfinite(r["pop"]) and r["pop"] >= 1]
    vals = sorted(((r["countrycode"], r["ctfp"]) for r in rows), key=lambda t: t[1])
    v = np.array([b for _, b in vals])
    return {"codes": [a for a, _ in vals], "ctfp": v.tolist(), "n": len(vals), "p10": float(np.percentile(v, 10)),
            "p90": float(np.percentile(v, 90)), "ratio_90_10": float(np.percentile(v, 90) / np.percentile(v, 10))}


# ---------------------------------------------------------------------------------------------------------------
# the intermission: two centuries of light

FILM_SECONDS = 40.0
MELODY_SECONDS = 50.0
FILM_FIRST, FILM_LAST = 1800, 1993


def film_time(year: float) -> float:
    return 1.5 + FILM_SECONDS * (year - FILM_FIRST) / (FILM_LAST - FILM_FIRST)


def compute_film() -> dict:
    l_ = compute_light()
    pts = sorted([r for r in l_["rows"] if r["year"] is not None and r["year"] >= 1800], key=lambda r: r["year"])
    return {"points": pts, "times": [film_time(r["year"]) for r in pts], "frontier_years": l_["frontier_years"],
            "frontier": l_["frontier"], "frontier_times": [film_time(y) for y in l_["frontier_years"]]}


def compute_melody() -> dict:
    from explainer.music.monochord.audio import Clip, ClipStore

    f = compute_film()
    years = list(range(FILM_FIRST, FILM_LAST + 1, 2))
    fy, fv = np.array(f["frontier_years"], float), np.log(np.array(f["frontier"]))
    vals = np.exp(np.interp(years, fy, fv))
    times = [film_time(y) for y in years]
    mel = score.data_melody(vals, MELODY_SECONDS, times=times, act=5, log=True, low=40, high=84)
    events = {"film_end": film_time(FILM_LAST) + 6.0, "first": times[0], "half": times[len(times) // 2]}
    clip = Clip(mel["y"], score.SR, events=events,
                notes=[{"t": float(t), "dur": 0.25, "hz": score.hz(nn), "name": str(y)}
                       for t, nn, y in zip(times, mel["notes"], years)],
                meta={"label": "the cheapest light's labour price, 1800-1993 (Nordhaus 1996), as a tune on a log scale "
                               "(computed)", "kind": "synthesized"})
    ClipStore("econ21").save("intermission.melody", clip)
    return {"times": times, "notes": mel["notes"], "years": years, "seconds": MELODY_SECONDS}


ITEMS = {
    "light": compute_light,
    "playit": compute_playit,
    "replication": compute_replication,
    "ak": compute_ak,
    "romer": compute_romer,
    "ah": compute_ah,
    "semi": compute_semi,
    "bloom": compute_bloom,
    "plants": compute_plants,
    "ajr": compute_ajr,
    "directed": compute_directed,
    "tfp": compute_tfp,
    "film": compute_film,
    "melody": compute_melody,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
