"""Precompute every number in Part 57 of *Psychology, Built* ("Health and Care").

    python -m videos.psychology.psych57.compute            # everything missing (seconds)

Results are cached in ``.cache/psych57/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Models are Psyche's
(``explainer.psychology.psyche.work``).

Items:
    placebo     the expectation model of placebo analgesia, and its effect by sensory precision
    care        a stepped-care service: therapy only, matched, stepped, and stepped with capacity rebalanced
    rtm         regression to the mean in a trial that enrols people on a bad day
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.psychology.psyche import work as Wk

CACHE = Cache("psych57")
load = CACHE.load


def compute_placebo() -> dict:
    p = Wk.placebo_pain()
    b = Wk.placebo_by_noise()
    return {**p, "sensory_sd": b["sensory_sd"], "by_noise": b["effect"]}


def compute_care() -> dict:
    rows = {"high_only": Wk.stepped_care("high_only", seed=5701), "matched": Wk.stepped_care("matched", seed=5701),
            "stepped": Wk.stepped_care("stepped", seed=5701),
            "rebalanced": Wk.stepped_care("stepped", low_slots=100, high_slots=60, seed=5701)}
    keys = list(rows)
    return {"policies": keys, **{m: np.array([rows[k][m] for k in keys])
                                 for m in ("recovered", "recovered_26", "mean_wait", "never_started", "stepped_up")}}


def compute_rtm() -> dict:
    """Regression to the mean, with no treatment at all: 20,000 people whose pain (0 to 10) is a stable level plus
    day-to-day variation; a trial enrols those scoring 7 or more on the screening day and measures them a week
    later.  The enrolled improve on average although nothing was done."""
    rng = np.random.default_rng(5702)
    n = 20_000
    level = np.clip(rng.normal(5.0, 1.2, n), 0, 10)
    day1 = np.clip(level + rng.normal(0, 1.5, n), 0, 10)
    day2 = np.clip(level + rng.normal(0, 1.5, n), 0, 10)
    enrol = day1 >= 7
    idx = rng.choice(n, 600, replace=False)
    return {"x": day1[idx], "y": day2[idx], "enrolled_share": float(enrol.mean()),
            "before": float(day1[enrol].mean()), "after": float(day2[enrol].mean()),
            "improved_share": float(np.mean(day2[enrol] < day1[enrol] - 1))}


ITEMS = {"placebo": compute_placebo, "care": compute_care, "rtm": compute_rtm}

if __name__ == "__main__":
    CACHE.main(ITEMS)
