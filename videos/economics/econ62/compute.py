"""Precompute every number in Part 62 of *Economics, Built* ("Inside the Firm").

    python -m videos.economics.econ62.compute            # everything missing (under a minute)
    python -m videos.economics.econ62.compute --force experiment

Results are cached in ``.cache/econ62/<name>.json``; scenes call ``load(name)``.  Models: Agora's ``org`` module (the
Island's plants, managers and owners) and ``contracts.relational`` (Part 14).  Data: FRED's output per hour in the
nonfarm business sector (the intermission).

Items:
    dispersion  plants' productivity spread among survivors, by the intensity of competition
    management  the Island's management scores by ownership, and their relation to productivity
    practices   the Play-it: four practices for one plant, valued over three years
    experiment  the Island's management experiment: 28 plants, consulting randomized by firm
    piece       piece rates against an hourly wage: effort and sorting
    peter       promoting the best seller against the best manager
    ceo         CEO pay by firm size (Gabaix and Landier), and pay for luck
    tradeoff    firm value by leverage: the tax shield against distress
    perks       Jensen and Meckling's owner-manager
    buyouts     establishments of buyout targets against controls
    hierarchy   Garicano's knowledge hierarchy by communication and knowledge costs
    wfh         a randomized working-from-home trial
    relational  a relational contract's self-enforcing effort by patience
    conglomerates  the diversification discount, and how much was there before
    film        the intermission's data film: output per hour, 1947-2026
    melody      its data melody
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.economics import data
from explainer.economics import score as SC
from explainer.economics.agora import contracts as K
from explainer.economics.agora import org as O

CACHE = Cache("econ62")
load = CACHE.load
TRUTH = {"experiment": "the practices' effect (17%) and its phase-in are planted (agora.org.experiment)",
         "management": "the ownership means and the productivity slope are planted (agora.org.OWNERS)"}
FILM_SECONDS = 46.0
MELODY_SECONDS = FILM_SECONDS + 12.0
FILM_YEARS = (1947.0, 2027.0)


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


def compute_dispersion() -> dict:
    return _jsonable(O.dispersion())


def compute_management() -> dict:
    M = O.management()
    keep = slice(0, 600)
    return _jsonable({**{k: v for k, v in M.items() if k not in ("score", "log_tfp", "owner")},
                      "score": M["score"][keep], "log_tfp": M["log_tfp"][keep], "owner": M["owner"][keep],
                      "owners": O.OWNERS})


def compute_practices() -> dict:
    return _jsonable({**O.practices(), "table": O.PRACTICES})


def compute_experiment() -> dict:
    return _jsonable(O.experiment())


def compute_piece() -> dict:
    return _jsonable(O.piece_rates())


def compute_peter() -> dict:
    return _jsonable(O.peter())


def compute_ceo() -> dict:
    C = O.ceo_pay()
    idx = np.unique(np.r_[np.geomspace(1, 500, 60).astype(int) - 1])
    return _jsonable({**{k: v for k, v in C.items() if k not in ("rank", "size", "pay", "pay_x6")},
                      "rank": np.array(C["rank"])[idx], "size": np.array(C["size"])[idx],
                      "pay": np.array(C["pay"])[idx], "pay_x6": np.array(C["pay_x6"])[idx],
                      "luck": O.pay_for_luck()})


def compute_tradeoff() -> dict:
    return _jsonable(O.tradeoff())


def compute_perks() -> dict:
    return _jsonable(O.perks())


def compute_buyouts() -> dict:
    return _jsonable(O.buyouts())


def compute_hierarchy() -> dict:
    return _jsonable(O.hierarchy())


def compute_wfh() -> dict:
    return _jsonable(O.wfh())


def compute_relational() -> dict:
    deltas = np.round(np.linspace(0.05, 0.95, 46), 3)
    return _jsonable({**K.relational(deltas), "deltas": deltas})


def compute_conglomerates() -> dict:
    return _jsonable(O.conglomerates())


def _productivity():
    s = data.fred("OPHNFB")
    yrs = np.array([int(d[:4]) + (int(d[5:7]) - 1) / 12 + 0.125 for d in s["date"]])
    return yrs, np.array(s["value"], float), s["date"], data.FRED_RETRIEVED["OPHNFB"]


def compute_film() -> dict:
    yrs, v, dates, retrieved = _productivity()
    annual = {}
    for y, x in zip(yrs, v):
        annual.setdefault(int(y), []).append(x)
    ys = sorted(y for y in annual if len(annual[y]) == 4 and (y - 1) in annual and len(annual[y - 1]) == 4)
    growth = [float(100 * (np.mean(annual[y]) / np.mean(annual[y - 1]) - 1)) for y in ys]
    # average growth by era
    eras = [(1948, 1973), (1974, 1995), (1996, 2004), (2005, 2019), (2020, 2025)]
    era_growth = []
    for a, b in eras:
        if a - 1 in annual and b in annual:
            g = (np.mean(annual[b]) / np.mean(annual[a - 1])) ** (1 / (b - a + 1)) - 1
            era_growth.append({"from": a, "to": b, "growth": float(100 * g)})
    return _jsonable({"years": yrs, "index": v, "t": [film_time(y) for y in yrs], "first": dates[0],
                      "last": dates[-1], "retrieved": retrieved, "ann_years": ys, "growth": growth,
                      "ann_t": [film_time(y + 0.5) for y in ys], "eras": era_growth})


def compute_melody() -> dict:
    from explainer.music.monochord.audio import Clip, ClipStore

    f = compute_film()
    vals = np.array(f["growth"])
    times = f["ann_t"]
    mel = SC.data_melody(vals, MELODY_SECONDS, times=times, act=11, log=False, low=45, high=84)
    events = {"film_end": film_time(FILM_YEARS[1]) + 4.0, "first": times[0]}
    clip = Clip(mel["y"], SC.SR, events=events,
                notes=[{"t": float(tt), "dur": 0.2, "hz": SC.hz(nn), "name": f"{x:+.1f}%"}
                       for tt, nn, x in zip(times, mel["notes"], vals)],
                meta={"label": "growth of output per hour in American business, year by year since 1948 (BLS via "
                               "FRED), as a tune (computed)", "kind": "synthesized"})
    ClipStore("econ62").save("intermission.melody", clip)
    return {"times": times, "notes": mel["notes"], "seconds": MELODY_SECONDS}


ITEMS = {
    "dispersion": compute_dispersion,
    "management": compute_management,
    "practices": compute_practices,
    "experiment": compute_experiment,
    "piece": compute_piece,
    "peter": compute_peter,
    "ceo": compute_ceo,
    "tradeoff": compute_tradeoff,
    "perks": compute_perks,
    "buyouts": compute_buyouts,
    "hierarchy": compute_hierarchy,
    "wfh": compute_wfh,
    "relational": compute_relational,
    "conglomerates": compute_conglomerates,
    "film": compute_film,
    "melody": compute_melody,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
