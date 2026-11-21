"""Precompute every number in Part 61 of *Economics, Built* ("Economics at the Platforms").

    python -m videos.economics.econ61.compute            # everything missing (about a minute)
    python -m videos.economics.econ61.compute --force ads

Results are cached in ``.cache/econ61/<name>.json``; scenes call ``load(name)``.  Models: Agora's ``platform`` module
(the Island's ride-hailing app and its marketplace).  Data: FRED's share of American retail sold online (the
intermission).

Items:
    night       New Year's Eve on the Island: surge on and surge off, minute by minute
    surplus     riders' sessions at random surge levels: the demand curve and consumer surplus per dollar
    commission  the two-sided market by commission: trips, drivers, waits, the platform's take, both sides' surplus
    ranking     a position-based click model, and a sponsored listing in the top slot
    reputation  percent positive against effective percent positive
    gsp         the generalized second-price auction with and without quality scores, and with a reserve
    ads         the Island's marketplace buys search ads: attribution, regression and experiment
    adpower     Lewis and Rao's arithmetic: the sample an advertising experiment needs
    peeking     A/A tests read every day
    cuped       variance reduction with a pre-period covariate
    switchback  a rider discount tested by user, by switchback and by city
    uplift      targeting a promotion by estimated effects
    longterm    a discount's short-term and long-term effects, and the surrogate index
    flex        drivers' surplus from flexible hours against fixed shifts
    wta         what a free search engine is worth: a willingness-to-accept survey
    film        the intermission's data film: e-commerce's share of American retail, 1999-2026
    melody      its data melody
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.economics import data
from explainer.economics import score as SC
from explainer.economics.agora import platform as PL

CACHE = Cache("econ61")
load = CACHE.load
TRUTH = {"night": "riders' demand, drivers' response and the surge rule are planted (NIGHT in agora.platform)",
         "commission": "riders' and drivers' choice models are planted (COMMISSION in agora.platform)",
         "ads": "the share of regular buyers and the ad's true lift are planted (agora.platform.search_ads)"}
FILM_SECONDS = 44.0
MELODY_SECONDS = FILM_SECONDS + 12.0
FILM_YEARS = (1999.5, 2027.0)


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


def compute_night() -> dict:
    on, off = PL.surge_night(True), PL.surge_night(False)
    return _jsonable({"on": on, "off": off, "params": PL.NIGHT})


def compute_surplus() -> dict:
    return _jsonable(PL.surge_surplus())


def compute_commission() -> dict:
    return _jsonable({**PL.commission(), "params": PL.COMMISSION,
                      "options": {str(c): PL.commission_market(c) for c in (0.1, 0.2, 0.3, 0.45)}})


def compute_ranking() -> dict:
    return _jsonable(PL.ranking())


def compute_reputation() -> dict:
    R = PL.reputation()
    keep = slice(0, 500)
    return _jsonable({**{k: v for k, v in R.items() if k not in ("quality", "pp", "epp")},
                      "quality": R["quality"][keep], "pp": R["pp"][keep], "epp": R["epp"][keep],
                      "pp_hist": np.histogram(R["pp"], bins=np.linspace(0.9, 1.0, 21))[0],
                      "epp_hist": np.histogram(R["epp"], bins=np.linspace(0.4, 0.65, 21))[0]})


def compute_gsp() -> dict:
    return _jsonable({"plain": PL.gsp(), "reserve": PL.gsp(reserve=1.5),
                      "bids": [4.0, 3.0, 2.5, 1.0], "quality": [0.5, 1.0, 0.7, 0.9], "ctr": [0.30, 0.18, 0.10]})


def compute_ads() -> dict:
    return _jsonable(PL.search_ads())


def compute_adpower() -> dict:
    return _jsonable(PL.ad_power())


def compute_peeking() -> dict:
    return _jsonable(PL.peeking())


def compute_cuped() -> dict:
    return _jsonable(PL.cuped(reps=1000))


def compute_switchback() -> dict:
    return _jsonable(PL.switchback())


def compute_uplift() -> dict:
    return _jsonable(PL.uplift())


def compute_longterm() -> dict:
    return _jsonable(PL.long_term())


def compute_flex() -> dict:
    return _jsonable(PL.flexibility())


def compute_wta() -> dict:
    return _jsonable(PL.wta_survey())


def _ecom():
    s = data.fred("ECOMPCTSA")
    yrs = np.array([int(d[:4]) + (int(d[5:7]) - 1) / 12 + 0.125 for d in s["date"]])
    return yrs, np.array(s["value"], float), s["date"], data.FRED_RETRIEVED["ECOMPCTSA"]


def compute_film() -> dict:
    yrs, v, dates, retrieved = _ecom()
    annual = {}
    for y, x in zip(yrs, v):
        annual.setdefault(int(y), []).append(x)
    ys = sorted(y for y in annual if len(annual[y]) == 4)
    vals = [float(np.mean(annual[y])) for y in ys]
    return _jsonable({"years": yrs, "share": v, "t": [film_time(y) for y in yrs], "first": dates[0],
                      "last": dates[-1], "retrieved": retrieved, "ann_years": ys, "ann_share": vals,
                      "ann_t": [film_time(y + 0.5) for y in ys],
                      "events": [{"year": 2008.75, "what": "the financial crisis", "t": film_time(2008.75)},
                                 {"year": 2020.3, "what": "the pandemic", "t": film_time(2020.3)}]})


def compute_melody() -> dict:
    from explainer.music.monochord.audio import Clip, ClipStore

    f = compute_film()
    vals = np.array(f["ann_share"])
    times = f["ann_t"]
    mel = SC.data_melody(vals, MELODY_SECONDS, times=times, act=11, log=False, low=45, high=84)
    events = {"film_end": film_time(FILM_YEARS[1]) + 4.0, "first": times[0]}
    clip = Clip(mel["y"], SC.SR, events=events,
                notes=[{"t": float(tt), "dur": 0.2, "hz": SC.hz(nn), "name": f"{x:.1f}%"}
                       for tt, nn, x in zip(times, mel["notes"], vals)],
                meta={"label": "e-commerce's share of American retail sales, yearly averages 2000-2025 (Census "
                               "Bureau via FRED), as a tune (computed)", "kind": "synthesized"})
    ClipStore("econ61").save("intermission.melody", clip)
    return {"times": times, "notes": mel["notes"], "seconds": MELODY_SECONDS}


ITEMS = {
    "night": compute_night,
    "surplus": compute_surplus,
    "commission": compute_commission,
    "ranking": compute_ranking,
    "reputation": compute_reputation,
    "gsp": compute_gsp,
    "ads": compute_ads,
    "adpower": compute_adpower,
    "peeking": compute_peeking,
    "cuped": compute_cuped,
    "switchback": compute_switchback,
    "uplift": compute_uplift,
    "longterm": compute_longterm,
    "flex": compute_flex,
    "wta": compute_wta,
    "film": compute_film,
    "melody": compute_melody,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
