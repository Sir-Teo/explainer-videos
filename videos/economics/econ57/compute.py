"""Precompute every number in Part 57 of *Economics, Built* ("Reading the Economy in Real Time").

    python -m videos.economics.econ57.compute            # everything missing (under a minute)
    python -m videos.economics.econ57.compute --force score

Results are cached in ``.cache/econ57/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Models: Agora's
``nowcast`` module.  Data: the Philadelphia Fed's real-time data set (first and latest estimates of real GDP growth,
and every vintage of 2006-2010), its Survey of Professional Forecasters (every median growth forecast and probability
of decline since 1968) and its Greenbook data set; FRED's payrolls with and without seasonal adjustment, industrial
production, real GDP, the GDP deflator, the unemployment rate and the real-time Sahm rule, the 10-year and 3-month
Treasury rates, the NBER's recession months and the news-based economic policy uncertainty index.

Items:
    revisions   first against latest estimates of real GDP growth since 1965Q4; 2008Q4 vintage by vintage
    seasonal    payrolls unadjusted, as the BLS adjusts them and by a simplified X-11, with and without its outlier step
    island      the Island's factor model: the Play-it quarter release by release, and errors over 380 quarters
    bridge      bridge-equation nowcasts of American GDP growth, 1985-2026, by month of the quarter (pseudo real time)
    probit      Estrella and Mishkin's yield-curve probit, 1959-2026, with every inversion
    sahm        the Sahm rule on today's data and in real time, against the NBER's recessions
    score       the professional forecasters' growth forecasts by horizon against first releases and two benchmarks
    score_all   the same with the pandemic quarters left in
    anxious     the professional forecasters' probability of a decline next quarter, with recessions
    greenbook   the Federal Reserve staff against the professional forecasters on inflation, and their combination
    regimes     a regime-switching economy: the best forecast a year ahead is never a fall
    epu         the news-based economic policy uncertainty index and its peaks
    record      Parts 1 and 28's forecasts at the turns
    film        the intermission's data film: the anxious index, 1968-2026
    melody      its data melody
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.economics import score as SC
from explainer.economics.agora import nowcast as N

CACHE = Cache("econ57")
load = CACHE.load
TRUTH: dict = {}
FILM_SECONDS = 44.0
MELODY_SECONDS = FILM_SECONDS + 8.0


def _jsonable(x):
    if isinstance(x, dict):
        return {k: _jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_jsonable(v) for v in x]
    if isinstance(x, np.ndarray):
        return x.tolist()
    if isinstance(x, (np.floating, np.integer)):
        return x.item()
    if isinstance(x, (np.bool_,)):
        return bool(x)
    return x


def compute_revisions() -> dict:
    return _jsonable(N.revisions())


def compute_seasonal() -> dict:
    return _jsonable(N.seasonal_payrolls())


def compute_island() -> dict:
    return _jsonable(N.island_nowcast())


def compute_bridge() -> dict:
    return _jsonable(N.bridge_nowcast())


def _recession_spans() -> list:
    from explainer.economics import data

    d = data.fred("USREC")
    spans, start = [], None
    for k, v in zip(d["date"], d["value"]):
        t = int(k[:4]) + (int(k[5:7]) - 1) / 12
        if v == v and v > 0.5 and start is None:
            start = t
        if v == v and v <= 0.5 and start is not None:
            spans.append((start, t))
            start = None
    return [s for s in spans if s[0] >= 1955]


def compute_probit() -> dict:
    out = N.yield_curve_probit()
    out["spans"] = _recession_spans()
    return _jsonable(out)


def compute_sahm() -> dict:
    out = N.sahm_rule()
    out["spans"] = _recession_spans()
    return _jsonable(out)


def compute_score() -> dict:
    return _jsonable(N.score_spf())


def compute_score_all() -> dict:
    out = N.score_spf(skip=())
    return _jsonable({"rows": [{k: r[k] for k in ("h", "n", "rmse", "rmse_mean", "rmse_rw", "bias")}
                               for r in out["rows"]]})


def compute_anxious() -> dict:
    return _jsonable(N.anxious_index())


def compute_greenbook() -> dict:
    return _jsonable(N.greenbook_vs_spf())


def compute_regimes() -> dict:
    return _jsonable(N.regime_forecasts())


def compute_epu() -> dict:
    return _jsonable(N.epu_peaks())


def compute_record() -> dict:
    from videos.economics.econ1.compute import compute_spf
    from videos.economics.econ28.compute import compute_transitory

    s, t = compute_spf(), compute_transitory()
    return {"g_forecast": 100 * s["aug_2009"], "g_actual": 100 * s["actual_2009"],
            "pi_forecast": t["projected_2022"], "pi_actual": t["actual_2022"]}


def _qt(q: str) -> float:
    return int(q[:4]) + (int(q[-1]) - 1) / 4


def film_time(t: float, first: float = 1968.75, last: float = 2026.75) -> float:
    return 1.5 + FILM_SECONDS * (t - first) / (last - first)


def compute_film() -> dict:
    a = N.anxious_index()
    t = [_qt(q) for q in a["quarters"]]
    rec = [_qt(q) for q in a["recession_quarters"]]
    spans, cur = [], None
    for x in rec:
        if cur is None or x - cur[1] > 0.3:
            if cur is not None:
                spans.append((cur[0], cur[1] + 0.25))
            cur = [x, x]
        else:
            cur[1] = x
    if cur is not None:
        spans.append((cur[0], cur[1] + 0.25))
    p = [float(x) for x in a["p"]]
    k = int(np.nanargmax(p))
    return {"t": t, "p": p, "times": [film_time(x) for x in t], "recessions": spans, "first": a["quarters"][0],
            "last": a["quarters"][-1], "max": p[k], "max_q": a["quarters"][k], "mean": a["mean"]}


def compute_melody() -> dict:
    from explainer.music.monochord.audio import Clip, ClipStore

    f = compute_film()
    vals = np.array(f["p"])
    times = f["times"]
    mel = SC.data_melody(vals, MELODY_SECONDS, times=times, act=11, log=False, low=45, high=86)
    events = {"film_end": film_time(f["t"][-1]) + 6.0, "first": times[0]}
    clip = Clip(mel["y"], SC.SR, events=events,
                notes=[{"t": float(tt), "dur": 0.2, "hz": SC.hz(nn), "name": f"{x:.0f}%"}
                       for tt, nn, x in zip(times, mel["notes"], vals)],
                meta={"label": "the professional forecasters' median probability of a fall in real GDP next "
                               "quarter, every survey 1968-2026 (Philadelphia Fed), as a tune (computed)",
                      "kind": "synthesized"})
    ClipStore("econ57").save("intermission.melody", clip)
    return {"times": times, "notes": mel["notes"], "seconds": MELODY_SECONDS}


ITEMS = {
    "revisions": compute_revisions,
    "seasonal": compute_seasonal,
    "island": compute_island,
    "bridge": compute_bridge,
    "probit": compute_probit,
    "sahm": compute_sahm,
    "score": compute_score,
    "score_all": compute_score_all,
    "anxious": compute_anxious,
    "greenbook": compute_greenbook,
    "regimes": compute_regimes,
    "epu": compute_epu,
    "record": compute_record,
    "film": compute_film,
    "melody": compute_melody,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
