"""Precompute every number in Part 59 of *Economics, Built* ("The Expert Witness").

    python -m videos.economics.econ59.compute            # everything missing (about four minutes)
    python -m videos.economics.econ59.compute --force towns

Results are cached in ``.cache/econ59/<name>.json``; scenes call ``load(name)``.  Models: Agora's ``merger`` module
(the Island's office-supply market, a nested logit with Bertrand pricing in sixty towns, and the review toolkit).
Data: FRED's consumer price indexes for airline fares and for everything (the intermission).

Items:
    towns       sixty towns: who is present, Alder's price, the true effect of a merger of Alder and Birch; the map
    regression  Alder's price on its rivals' presence, with and without controls; the multiverse of specifications
    playit      three pairs: diversion, margin, critical diversion
    market      the hypothetical-monopolist test for three candidate markets, its profit curves, the cellophane trap
    concentration  the guidelines' presumptions for five Island industries; each town's Herfindahl index
    upp         diversion ratios, upward pricing pressure, GUPPIs, the full simulation, compensating cost cuts
    forms       one set of elasticities, four demand curves, four predicted price rises
    agency      a plain-logit simulation town by town, against the truth
    efficiency  pass-through of cost savings; the merger's effect with and without Cedar in town
    vertical    the channel and the distributors: the fee rise, the saving, the departure rate that decides
    cartel      the Island's cement cartel: prices, the overcharge regression, damages, the variance screen
    witness     the regression cross-examined: towns left out, subsamples
    labour      two hospitals merge in a town of nurses
    retro       the merger consummated: difference in differences against the predictions
    regulated   a rate case, a price cap with resets, the access price
    film        the intermission's data film: airline fares in the consumer price index, deflated, 1964-2025
    melody      its data melody
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.economics import data
from explainer.economics import score as SC
from explainer.economics.agora import merger as M

CACHE = Cache("econ59")
load = CACHE.load
TRUTH = {"merger_effect": "the average true effect of the merger on Alder's price in the towns where Birch is "
                          "present, from the planted demand"}
FILM_SECONDS = 44.0
MELODY_SECONDS = FILM_SECONDS + 12.0
FILM_YEARS = (1964.0, 2026.0)


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
    if isinstance(x, float) and not np.isfinite(x):
        return None
    return x


def _towns() -> dict:
    """The towns, rebuilt from the cache (the simulation takes about forty seconds)."""
    t = load("towns")
    return {"n": t["n"], **{k: np.array(t[k], dtype=bool if k in ("birch", "cedar") else float)
                            for k in ("size", "cost", "birch", "cedar", "price", "true_price", "merger_effect",
                                      "share")}}


def compute_towns() -> dict:
    T = M.towns()
    rng = np.random.default_rng(591)
    # positions on the Island's map: an ellipse, bigger towns nearer the harbour on the west coast
    ang = rng.uniform(0, 2 * np.pi, T["n"])
    rad = np.sqrt(rng.uniform(0.05, 1.0, T["n"]))
    x = 5.2 * rad * np.cos(ang) - 0.6 * T["size"]
    y = 2.6 * rad * np.sin(ang)
    x = np.clip(x, -5.6, 5.6)
    groups = {}
    for name, mask in (("Alder alone", ~T["birch"] & ~T["cedar"]), ("Alder and Birch", T["birch"] & ~T["cedar"]),
                       ("Alder and Cedar", ~T["birch"] & T["cedar"]), ("all three", T["birch"] & T["cedar"])):
        groups[name] = {"n": int(mask.sum()), "price": float(np.mean(T["price"][mask]))}
    me = T["merger_effect"]
    return _jsonable({**T, "x": x, "y": y, "groups": groups,
                      "mean_effect": float(np.nanmean(me)),
                      "effect_cedar": float(np.nanmean(me[T["birch"] & T["cedar"]])),
                      "effect_no_cedar": float(np.nanmean(me[T["birch"] & ~T["cedar"]])),
                      "lone_premium": 100 * (groups["Alder alone"]["price"] / groups["all three"]["price"] - 1)})


def compute_regression() -> dict:
    T = _towns()
    full = M.price_regression(T, controls=True)
    bare = M.price_regression(T, controls=False)
    mv = M.multiverse(T)
    return _jsonable({"full": full, "bare": bare, "multiverse": mv,
                      "mv_min": min(r["effect"] for r in mv), "mv_max": max(r["effect"] for r in mv),
                      "truth": 100 * float(np.nanmean(T["merger_effect"]))})


def compute_playit() -> dict:
    return _jsonable({"pairs": M.playit_pairs(), "X": 0.05})


def compute_market() -> dict:
    cands = {"Alder alone": (0,), "Alder and Birch": (0, 1), "the three superstores": (0, 1, 2)}
    out = {}
    xs = np.linspace(0.0, 0.25, 26)
    for name, c in cands.items():
        h = M.hmt(candidate=c)
        curve = [M.hmt(candidate=c, X=float(x))["profit1"] / h["profit0"] - 1 for x in xs]
        out[name] = {**h, "curve": curve}
    cel = M.cellophane()
    curve_m = [M.hmt(candidate=(0, 1, 2), X=float(x), prices=cel["p_mono"])["profit1"] /
               cel["monopoly"]["profit0"] - 1 for x in xs]
    return _jsonable({"cands": out, "xs": 100 * xs, "cellophane": cel, "curve_mono": curve_m})


def compute_concentration() -> dict:
    T = _towns()
    tc = M.town_concentration(T)
    return _jsonable({"industries": M.industries(), "towns": tc["rows"], "thresholds": M.THRESHOLDS})


def compute_upp() -> dict:
    u = M.upp()
    return _jsonable(u)


def compute_forms() -> dict:
    return _jsonable(M.functional_forms())


def compute_agency() -> dict:
    return _jsonable(M.agency_logit(_towns()))


def compute_efficiency() -> dict:
    T = _towns()
    pt = M.pass_through()
    u = load("upp")
    return _jsonable({"pass_through": pt, "cmcr": u["cmcr"],
                      "effect_cedar": 100 * float(np.nanmean(T["merger_effect"][T["birch"] & T["cedar"]])),
                      "effect_no_cedar": 100 * float(np.nanmean(T["merger_effect"][T["birch"] & ~T["cedar"]])),
                      "n_cedar": int((T["birch"] & T["cedar"]).sum()),
                      "n_no_cedar": int((T["birch"] & ~T["cedar"]).sum())})


def compute_vertical() -> dict:
    return _jsonable({**M.vertical(), "curve": M.vertical_curve()})


def compute_cartel() -> dict:
    c = M.cartel()
    v = M.variance_screen(c["price"], c["cost"])
    return _jsonable({**c, "cv": v["cv"], "threshold": v["threshold"], "flag": v["flag"],
                      "cv_during": float(np.mean(v["cv"][c["start"] + 12:c["end"] - 1])),
                      "cv_outside": float(np.mean(np.r_[v["cv"][12:c["start"] - 1], v["cv"][c["end"] + 12:]]))})


def compute_witness() -> dict:
    return _jsonable(M.witness(_towns()))


def compute_labour() -> dict:
    out = M.labour_merger()
    betas = np.linspace(0.08, 0.6, 27)
    falls = [M.labour_merger(beta=float(b))["fall"] for b in betas]
    return _jsonable({**out, "betas": betas, "falls": falls})


def compute_retro() -> dict:
    T = _towns()
    r = M.retrospective(T)
    a = load("agency")
    return _jsonable({**r, "agency": a["mean_predicted"], "guppi": a["mean_guppi"]})


def compute_regulated() -> dict:
    return _jsonable({"rate": M.rate_case(), "cap": M.price_cap(), "ecpr": M.ecpr()})


def compute_film() -> dict:
    a, c = data.fred("CUUR0000SETG01"), data.fred("CPIAUCNS")

    def annual(d):
        out = {}
        for t, v in zip(d["date"], d["value"]):
            if v == v:
                out.setdefault(int(t[:4]), []).append(v)
        return {y: float(np.mean(v)) for y, v in out.items()}
    A, C = annual(a), annual(c)
    years = [y for y in sorted(A) if y in C and 1964 <= y <= 2025]
    real = np.array([A[y] / C[y] for y in years])
    real = 100 * real / real[years.index(1978)]
    events = [(1978, "deregulation"), (2001, "September 11"), (2008, "Delta and Northwest"),
              (2010, "United and Continental"), (2013, "American and US Airways"), (2020, "the pandemic"),
              (2024, "JetBlue and Spirit, blocked")]
    return _jsonable({"years": years, "real": real, "t": [film_time(y + 0.5) for y in years],
                      "events": [{"year": y, "what": w, "t": film_time(y + 0.5)} for y, w in events],
                      "peak_year": years[int(np.argmax(real))], "peak": float(real.max()),
                      "last": float(real[-1]), "retrieved": a["retrieved"]})


def compute_melody() -> dict:
    from explainer.music.monochord.audio import Clip, ClipStore

    f = compute_film()
    vals = np.array(f["real"])
    times = f["t"]
    mel = SC.data_melody(vals, MELODY_SECONDS, times=times, act=11, log=True, low=45, high=84)
    events = {"film_end": film_time(FILM_YEARS[1]) + 4.0, "first": times[0]}
    clip = Clip(mel["y"], SC.SR, events=events,
                notes=[{"t": float(tt), "dur": 0.2, "hz": SC.hz(nn), "name": f"{x:.0f}"}
                       for tt, nn, x in zip(times, mel["notes"], vals)],
                meta={"label": "airline fares in the consumer price index, deflated, 1978 = 100, 1964-2025 (BLS via "
                               "FRED), as a tune (computed)", "kind": "synthesized"})
    ClipStore("econ59").save("intermission.melody", clip)
    return {"times": times, "notes": mel["notes"], "seconds": MELODY_SECONDS}


ITEMS = {
    "towns": compute_towns,
    "regression": compute_regression,
    "playit": compute_playit,
    "market": compute_market,
    "concentration": compute_concentration,
    "upp": compute_upp,
    "forms": compute_forms,
    "agency": compute_agency,
    "efficiency": compute_efficiency,
    "vertical": compute_vertical,
    "cartel": compute_cartel,
    "witness": compute_witness,
    "labour": compute_labour,
    "retro": compute_retro,
    "regulated": compute_regulated,
    "film": compute_film,
    "melody": compute_melody,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
