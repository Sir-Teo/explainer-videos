"""Precompute every number in Part 51 of *Psychology, Built* ("Human Factors").

    python -m videos.psychology.psych51.compute            # everything missing (seconds)

Results are cached in ``.cache/psych51/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Models are Psyche's
(``explainer.psychology.psyche.work``).

Items:
    fitts       simulated pointing and the fitted Fitts's law
    hick        choice reaction time by number of alternatives, compatible and incompatible mappings
    vigilance   a two-hour watch, pooled over 60 simulated watchers, analysed by signal detection per half hour
    onewatch    the same watch for a single watcher: the noise an individual record carries
    prevalence  misses at each prevalence, for an optimal observer and one who shifts only part of the way
    tlx         a NASA-TLX worked example
    takeover    takeover within a time budget by automation reliability
    alarm       an alarm's hit rate, positive predictive value and the share of events answered, by threshold
    cheese      the Swiss cheese model: four layers, holes independent or correlated
    fatigue     hours awake against blood-alcohol equivalents
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.psychology.psyche import work as Wk

CACHE = Cache("psych51")
load = CACHE.load


def compute_fitts() -> dict:
    return Wk.fitts_trials(seed=51)


def compute_hick() -> dict:
    n = np.array([1, 2, 3, 4, 6, 8])
    return {"n": n, "compatible": Wk.hick_rt(n), "incompatible": Wk.hick_rt(n, compatible=False)}


def compute_vigilance() -> dict:
    return Wk.vigilance(watchers=60, seed=5101)


def compute_onewatch() -> dict:
    return Wk.vigilance(watchers=1, seed=5102)


def compute_prevalence() -> dict:
    o = Wk.prevalence(prevs=(0.5, 0.1, 0.02, 0.01))
    p = Wk.prevalence_partial(prevs=(0.5, 0.1, 0.02, 0.01), shift=0.35)
    return {"prev": o["prev"], "miss_opt": o["miss"], "fa_opt": o["fa"], "miss_partial": p["miss"],
            "fa_partial": p["fa"]}


def compute_tlx() -> dict:
    ratings = [70, 20, 60, 40, 65, 50]
    weights = [4, 0, 3, 2, 4, 2]
    return {"scales": list(Wk.TLX), "ratings": np.array(ratings), "weights": np.array(weights),
            "score": Wk.nasa_tlx(ratings, weights), "raw": float(np.mean(ratings))}


def compute_takeover() -> dict:
    return Wk.takeover(seed=5103)


def compute_alarm() -> dict:
    return Wk.alarm()


def compute_cheese() -> dict:
    rhos = np.array([0.0, 0.2, 0.4, 0.6])
    return {"rho": rhos, "p": np.array([Wk.swiss_cheese(rho=float(r), seed=5104) for r in rhos]), "indep": 0.1 ** 4}


def compute_fatigue() -> dict:
    h = np.arange(8, 27)
    return {"hours": h, "bac": Wk.awake_bac(h)}


ITEMS = {"fitts": compute_fitts, "hick": compute_hick, "vigilance": compute_vigilance, "onewatch": compute_onewatch,
         "prevalence": compute_prevalence, "tlx": compute_tlx, "takeover": compute_takeover, "alarm": compute_alarm,
         "cheese": compute_cheese, "fatigue": compute_fatigue}

if __name__ == "__main__":
    CACHE.main(ITEMS)
