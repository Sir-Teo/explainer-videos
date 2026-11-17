"""Precompute every number in Part 41 of *Psychology, Built* ("Psychosis, Addiction and Development").

    python -m videos.psychology.psych41.compute            # everything missing (a few seconds)
    python -m videos.psychology.psych41.compute --force halluc

Results are cached in ``.cache/psych41/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Models are Psyche's
(``explainer.psychology.psyche.clinic``).  Published numbers are quoted in the scenes with their sources.
Simulations use fixed seeds; where a scene shows one simulated run, it is the median of many by a rule fixed in
advance.

Items:
    mask        the hollow mask on a Gaussian observer: the chance of seeing it convex against the prior's precision,
                and in two simulated groups of 2,000 whose prior precisions differ (log-normal, medians 8 and 3);
                the expected error of strong and weak priors in a typical (95%) and a less typical (60%) world
    halluc      conditioned hallucinations: reports of a tone on tone-absent trials, by block, for prior weights 0.3
                and 1.5 (200 learners each), and overall across weights 0 to 2
    salience    aberrant salience: 20 cues, one rewarded, 2,000 trials, with dopamine bursts at rates 0, 0.1, 0.2 and
                0.3 (the run with the median count of salient cues of 21)
    redish      Redish's model: the value of a natural reward, of a drug (reward 0.5, surge 0.2) and of the drug with a
                cost of 1.0, over 300 trials
    discount    hyperbolic discounting with k = 0.01 and 0.05 per day: the value of 100 at delays up to a year, and
                the delay at which 100 later stops beating 50 now
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.psychology.psyche import clinic as K

CACHE = Cache("psych41")
load = CACHE.load


def compute_mask() -> dict:
    pp = np.linspace(0.0, 14.0, 141)
    curve = np.array([K.hollow_mask(float(p))["p_convex"] for p in pp])
    rng = np.random.default_rng(41)
    groups = {}
    for name, med in (("typical", 8.0), ("lower", 3.0)):
        prec = np.exp(rng.normal(np.log(med), 0.5, 2000))
        p = np.array([K.hollow_mask(float(x))["p_convex"] for x in prec])
        seen = rng.random(2000) < p
        groups[name] = {"precision": prec, "fooled": float(seen.mean())}
    grid = np.linspace(0.0, 20.0, 201)
    tr = {}
    for pt in (0.95, 0.6):
        mse = K.prior_tradeoff(grid, p_typical=pt)
        tr[str(pt)] = {"mse": mse, "best": float(grid[int(np.argmin(mse))])}
    return {"pp": pp, "curve": curve, "fooled_typical": groups["typical"]["fooled"],
            "fooled_lower": groups["lower"]["fooled"], "prec_typical": groups["typical"]["precision"],
            "prec_lower": groups["lower"]["precision"], "grid": grid, "mse95": tr["0.95"]["mse"],
            "mse60": tr["0.6"]["mse"], "best95": tr["0.95"]["best"], "best60": tr["0.6"]["best"]}


def compute_halluc() -> dict:
    lo, hi = K.conditioned_hallucinations(0.3, seed=41), K.conditioned_hallucinations(1.5, seed=41)
    ws = np.linspace(0.0, 2.0, 11)
    overall = np.array([K.conditioned_hallucinations(float(w), seed=41, reps=100)["overall"] for w in ws])
    return {"low": lo["by_block"], "high": hi["by_block"], "low_all": lo["overall"], "high_all": hi["overall"],
            "blocks": lo["blocks"], "weights": ws, "overall": overall}


def compute_salience() -> dict:
    out = {}
    for q in (0.0, 0.1, 0.2, 0.3):
        runs = [K.aberrant_salience(q, seed=s) for s in range(21)]
        counts = np.array([r["salient"] for r in runs])
        k = int(np.argsort(counts, kind="stable")[len(counts) // 2])
        out[f"V{int(q * 100)}"] = runs[k]["V"]
        out[f"n{int(q * 100)}"] = int(counts[k])
    return out


def compute_redish() -> dict:
    return {"natural": K.redish(0.0), "drug": K.redish(0.2, reward=0.5), "drug_cost": K.redish(0.2, reward=0.5, cost=1.0),
            "natural_cost": K.redish(0.0, cost=1.0)}


def compute_discount() -> dict:
    d = np.linspace(0, 365, 366)
    out = {"delay": d}
    for k in (0.01, 0.05):
        out[f"v{int(k * 100)}"] = K.discount(100, d, k)
        out[f"switch{int(k * 100)}"] = float((100 / 50 - 1) / k)
    return out


ITEMS = {"mask": compute_mask, "halluc": compute_halluc, "salience": compute_salience, "redish": compute_redish,
         "discount": compute_discount}

if __name__ == "__main__":
    CACHE.main(ITEMS)
