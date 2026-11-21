"""Precompute every number in Part 64 of *Economics, Built* ("Machines that Learn").

    python -m videos.economics.econ64.compute            # everything missing (about five minutes)
    python -m videos.economics.econ64.compute --force courts

Results are cached in ``.cache/econ64/<name>.json``; scenes call ``load(name)``.  Models: Agora's ``learn`` module
(the Island's bail courts, a job programme, a partially linear model, a corpus of news, the growth model, pricing
agents, two groups of defendants), over statkit's forests, causal forest and PPI and the series' autodiff.  Data:
Rupp's transistors per microprocessor, 1971-2021 (the intermission).

Items:
    courts      the bail courts: policy frontier against the judges, by leniency quintile
    contraction the contraction design, and the naive evaluation against the truth
    cases       ten defendants for the Play-it
    targeting   a job programme targeted by risk, by true effect, by a causal forest's estimate, at random
    dml         double machine learning against OLS and a plug-in estimator, Monte Carlo
    text        the share of layoff news: classifier, hand labels, prediction-powered inference
    euler       a neural network trained on Euler-equation errors, against Brock and Mirman
    agents      Q-learning price setters, eight sessions
    fairness    a calibrated score for two groups: error rates and Chouldechova's identity
    sweep       the algorithm's advantage as the judges' courtroom signal grows
    film        the intermission's data film: transistors per microprocessor, 1971-2021
    melody      its data melody
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.economics import data
from explainer.economics import score as SC
from explainer.economics.agora import learn as L

CACHE = Cache("econ64")
load = CACHE.load
TRUTH = {"courts": "each defendant's risk, the judges' courtroom signal and their leniency are planted "
                   "(agora.learn.defendants, courts)",
         "targeting": "the programme's effect for each person is planted (agora.learn.targeting)"}
FILM_SECONDS = 46.0
MELODY_SECONDS = FILM_SECONDS + 12.0
FILM_YEARS = (1970.0, 2022.0)


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


_COURTS = {}


def _courts():
    if "C" not in _COURTS:
        _COURTS["C"] = L.courts()
    return _COURTS["C"]


def compute_courts() -> dict:
    C = _courts()
    t = C["test"]
    r, p, y, rel = C["risk"][t], C["p"][t], C["y"][t], C["released"][t]
    edges = np.quantile(r, np.linspace(0, 1, 11))
    cal = []
    for a, b in zip(edges[:-1], edges[1:]):
        m = (r >= a) & (r <= b)
        cal.append({"predicted": float(r[m].mean()), "truth": float(p[m].mean()),
                    "observed": float(y[m & rel].mean()) if (m & rel).any() else None,
                    "released": float(rel[m].mean())})
    return _jsonable({**L.policy_curves(C), "rates": C["rate"], "n": len(C["y"]), "n_train": C["n_train"],
                      "released": float(C["released"].mean()), "calibration": cal})


def compute_contraction() -> dict:
    return _jsonable(L.contraction(_courts()))


def compute_cases() -> dict:
    return _jsonable(L.cases(_courts()))


def compute_targeting() -> dict:
    return _jsonable(L.targeting())


def compute_dml() -> dict:
    return _jsonable(L.dml_study())


def compute_text() -> dict:
    return _jsonable(L.text_measure())


def compute_euler() -> dict:
    E = L.euler_net()
    E["loss"] = E["loss"][::10]
    return _jsonable(E)


def compute_agents() -> dict:
    return _jsonable(L.pricing_agents())


def compute_fairness() -> dict:
    return _jsonable(L.fairness())


def compute_sweep() -> dict:
    return _jsonable(L.signal_sweep())


def compute_film() -> dict:
    t = data.transistors()
    yrs = np.array(t["year"], float)
    v = np.array(t["transistors"], float)
    lv = np.log10(v)
    # doubling time over the whole period, by least squares on log2
    b = np.polyfit(yrs, np.log2(v), 1)[0]
    early = np.polyfit(yrs[yrs <= 2005], np.log2(v[yrs <= 2005]), 1)[0]
    late = np.polyfit(yrs[yrs >= 2005], np.log2(v[yrs >= 2005]), 1)[0]
    return _jsonable({"years": yrs, "count": v, "log10": lv, "t": [film_time(y) for y in yrs],
                      "doubling": 1 / b, "doubling_early": 1 / early, "doubling_late": 1 / late,
                      "first": int(yrs[0]), "last": int(yrs[-1]), "first_count": v[0], "last_count": v[-1]})


def compute_melody() -> dict:
    from explainer.music.monochord.audio import Clip, ClipStore

    f = compute_film()
    vals = np.array(f["log10"])
    times = f["t"]
    mel = SC.data_melody(vals, MELODY_SECONDS, times=times, act=12, log=False, low=45, high=86)
    events = {"film_end": film_time(FILM_YEARS[1]) + 4.0, "first": times[0]}
    clip = Clip(mel["y"], SC.SR, events=events,
                notes=[{"t": float(tt), "dur": 0.2, "hz": SC.hz(nn), "name": f"10^{x:.1f}"}
                       for tt, nn, x in zip(times, mel["notes"], vals)],
                meta={"label": "transistors on the largest microprocessor of each year, 1971-2021 (Rupp via Our "
                               "World in Data), as a rising tune (computed)", "kind": "synthesized"})
    ClipStore("econ64").save("intermission.melody", clip)
    return {"times": times, "notes": mel["notes"], "seconds": MELODY_SECONDS}


ITEMS = {
    "courts": compute_courts,
    "contraction": compute_contraction,
    "cases": compute_cases,
    "targeting": compute_targeting,
    "dml": compute_dml,
    "text": compute_text,
    "euler": compute_euler,
    "agents": compute_agents,
    "fairness": compute_fairness,
    "sweep": compute_sweep,
    "film": compute_film,
    "melody": compute_melody,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
