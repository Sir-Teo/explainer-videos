"""Precompute every number in Part 55 of *Psychology, Built* ("Behaviour Change at Scale").

    python -m videos.psychology.psych55.compute            # everything missing (seconds)

Results are cached in ``.cache/psych55/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Models are Psyche's
(``explainer.psychology.psyche.work``).

Items:
    inertia     the two-type algebra of a default, from opt-in and opt-out enrolment
    mega        a megastudy: 53 arms, small true effects, the winner's curse and shrinkage
    curse       the winner's curse over 400 simulated megastudies
    gap         a publication filter on small academic trials against large nudge-unit trials
    hetero      one average effect, four groups: a simulated trial of 160,000 people by baseline quartile
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.psychology.psyche import work as Wk

CACHE = Cache("psych55")
load = CACHE.load


def compute_inertia() -> dict:
    return Wk.default_inertia(0.37, 0.86)


def compute_mega() -> dict:
    return Wk.megastudy(seed=5501)


def compute_curse() -> dict:
    est, tru, shr = [], [], []
    for r in range(400):
        m = Wk.megastudy(seed=5600 + r)
        est.append(m["winner_est"]); tru.append(m["winner_true"]); shr.append(m["winner_shrunk"])
    est, tru, shr = map(np.array, (est, tru, shr))
    return {"est": float(est.mean()), "true": float(tru.mean()), "shrunk": float(shr.mean()),
            "mse_raw": float(np.mean((est - tru) ** 2)), "mse_shrunk": float(np.mean((shr - tru) ** 2))}


def compute_gap() -> dict:
    g = Wk.publication_gap(seed=5502)
    return {"academic": g["academic"]["mean_reported"], "academic_share": g["academic"]["share_reported"],
            "academic_true": g["academic"]["mean_true_reported"], "units": g["units"]["mean_reported"],
            "truth": g["truth"]}


def compute_hetero() -> dict:
    """A reminder nudge whose true effect grows with how likely a person was to forget (four quartiles of a
    baseline score; true effects 0.2, 0.6, 1.4 and 3.4 points, averaging 1.4).  One trial of 160,000 people,
    half treated, base rates 50% down to 20%; each quartile's effect estimated with a 95% interval."""
    rng = np.random.default_rng(5503)
    n = 160_000
    q = rng.integers(0, 4, n)
    t = rng.random(n) < 0.5
    base = np.array([0.50, 0.40, 0.30, 0.20])
    eff = np.array([0.002, 0.006, 0.014, 0.034])
    y = rng.random(n) < base[q] + t * eff[q]
    est, se = [], []
    for k in range(4):
        a, b = y[(q == k) & t], y[(q == k) & ~t]
        est.append(a.mean() - b.mean())
        se.append(np.sqrt(a.var() / len(a) + b.var() / len(b)))
    ate = y[t].mean() - y[~t].mean()
    ate_se = np.sqrt(y[t].var() / t.sum() + y[~t].var() / (~t).sum())
    return {"true": eff, "est": np.array(est), "se": np.array(se), "ate": float(ate), "ate_se": float(ate_se),
            "share_top": float(eff[3] / eff.sum())}


ITEMS = {"inertia": compute_inertia, "mega": compute_mega, "curse": compute_curse, "gap": compute_gap,
         "hetero": compute_hetero}

if __name__ == "__main__":
    CACHE.main(ITEMS)
