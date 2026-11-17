"""Precompute every number in Part 54 of *Psychology, Built* ("The Science of Learning").

    python -m videos.psychology.psych54.compute            # everything missing (a minute)

Results are cached in ``.cache/psych54/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Models are Psyche's
(``explainer.psychology.psyche.work`` and Part 21's ``memory``).

Items:
    policies    four review policies at four reviews each: recall at a test on day 60
    budget      recall at day 60 by number of reviews, for massed and fixed spacing
    curves      recall over 60 days for one item under each policy
    ridge       Part 21's spacing ridgeline: the best gap grows with the retention interval
    reading     the simple view of reading on 400 simulated children
"""

from __future__ import annotations

import warnings

import numpy as np

from explainer.ai.cache import Cache
from explainer.psychology.psyche import memory as Mem
from explainer.psychology.psyche import work as Wk

warnings.filterwarnings("ignore", category=RuntimeWarning)
CACHE = Cache("psych54")
load = CACHE.load
POLICIES = ("massed", "expanding", "fixed", "model")
BASE = 0.6


def compute_policies() -> dict:
    res = {p: Wk.schedule(p, seed=5401, base=BASE) for p in POLICIES}
    return {"policies": list(POLICIES), "recall": np.array([res[p]["recall"] for p in POLICIES]),
            "times": np.array([res[p]["first_item_times"] for p in POLICIES])}


def compute_budget() -> dict:
    ks = np.array([1, 2, 3, 4, 6, 8])
    return {"reviews": ks,
            "massed": np.array([Wk.schedule("massed", reviews=int(k), seed=5402, base=BASE)["recall"] for k in ks]),
            "fixed": np.array([Wk.schedule("fixed", reviews=int(k), seed=5402, base=BASE)["recall"] for k in ks])}


def compute_curves() -> dict:
    pol = compute_policies()
    days = np.linspace(0.05, 60, 240)
    out = {}
    for p, times in zip(POLICIES, pol["times"]):
        r = []
        for d in days:
            seen = [t for t in times if t <= d]
            r.append(float(Mem.pa_recall(Wk.pa_activation_capped(seen, d) - BASE)))
        out[p] = np.array(r)
    return {"days": days, **{p: out[p] for p in POLICIES}}


def compute_ridge() -> dict:
    gaps = np.array([0.02, 0.5, 1, 2, 4, 7, 14, 21, 35, 60, 90])
    ret = np.array([7, 35, 70, 350])
    m = Mem.spacing_ridge(gaps, ret)
    return {"gaps": gaps, "retention": ret, "recall": m, "best_gap": gaps[np.argmax(m, axis=1)]}


def compute_reading() -> dict:
    rng = np.random.default_rng(5403)
    n = 400
    dec = np.clip(rng.beta(4, 2, n) + 0.0, 0, 1)
    lc = np.clip(rng.beta(4, 2, n), 0, 1)
    rc = Wk.simple_view(dec, lc) + rng.normal(0, 0.04, n)
    low_dec = (dec < 0.45) & (lc >= 0.6)
    low_lc = (lc < 0.45) & (dec >= 0.6)
    return {"dec": dec, "lc": lc, "rc": rc, "r_dec": float(np.corrcoef(dec, rc)[0, 1]),
            "r_lc": float(np.corrcoef(lc, rc)[0, 1]), "n_low_dec": int(low_dec.sum()), "n_low_lc": int(low_lc.sum()),
            "rc_low_dec": float(rc[low_dec].mean()), "rc_low_lc": float(rc[low_lc].mean()),
            "rc_good": float(rc[(dec >= 0.6) & (lc >= 0.6)].mean())}


ITEMS = {"policies": compute_policies, "budget": compute_budget, "curves": compute_curves, "ridge": compute_ridge,
         "reading": compute_reading}

if __name__ == "__main__":
    CACHE.main(ITEMS)
