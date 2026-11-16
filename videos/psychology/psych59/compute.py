"""Precompute every number in Part 59 of *Psychology, Built* ("Computational Psychiatry").

    python -m videos.psychology.psych59.compute            # everything missing (a minute)

Results are cached in ``.cache/psych59/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Models are Psyche's
(``explainer.psychology.psyche.precision``).

Items:
    paradox     a Stroop-like task, test and retest: an enormous group effect, a modest retest correlation
    tradeoff    group effect size against individual reliability, by design and trials
    attenuate   how unreliable measures shrink a parameter-symptom correlation
    biotypes    clustering structureless data, and data with real subgroups: symptom differences and stability
    travel      outcome prediction: apparent, cross-validated, and in a new trial
    pai         the sample a treatment-selection rule needs
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.psychology.psyche import precision as Pr

CACHE = Cache("psych59")
load = CACHE.load


def compute_paradox() -> dict:
    p = Pr.paradox(n_people=400, seed=5901)
    return {k: v for k, v in p.items()}


def compute_tradeoff() -> dict:
    return Pr.design_tradeoff()


def compute_attenuate() -> dict:
    rels = np.array([0.2, 0.4, 0.6, 0.8, 1.0])
    return {"rel": rels, "observed": np.array([Pr.attenuated_r(0.5, r, 0.8) for r in rels]), "true": 0.5}


def compute_biotypes() -> dict:
    none = [Pr.biotypes(structure=0.0, seed=5902 + r) for r in range(10)]
    real = [Pr.biotypes(structure=1.5, seed=5950 + r) for r in range(10)]
    return {"none_p": np.array([b["symptom_p"] for b in none]), "none_ari": np.array([b["stability_ari"] for b in none]),
            "real_p": np.array([b["symptom_p"] for b in real]), "real_ari": np.array([b["stability_ari"] for b in real])}


def compute_travel() -> dict:
    return Pr.cross_trial(reps=60, seed=5903)


def compute_pai() -> dict:
    ds = np.array([0.2, 0.3, 0.4, 0.5])
    rows = [Pr.pai_sample(float(d)) for d in ds]
    return {"d": ds, "main": np.array([r["main_total"] for r in rows]), "inter": np.array([r["interaction_total"]
                                                                                           for r in rows])}


def compute_mood() -> dict:
    """Rutledge et al.'s momentary-happiness model run forward on one sequence of 40 gambles (a run of losses in
    the middle), for two people who differ only in how slowly past prediction errors fade (gamma 0.5 and 0.85).
    Weights are illustrative.  Happiness = w0 + w_ev * sum gamma^k EV + w_rpe * sum gamma^k RPE."""
    rng = np.random.default_rng(5904)
    T = 40
    ev = rng.uniform(0.0, 1.0, T)
    out = ev + rng.choice([-1.0, 1.0], T) * rng.uniform(0.3, 1.0, T)
    out[16:23] = ev[16:23] - rng.uniform(0.6, 1.0, 7)
    rpe = out - ev

    def mood(g):
        h, a, b = [], 0.0, 0.0
        for t in range(T):
            a, b = g * a + ev[t], g * b + rpe[t]
            h.append(0.5 + 0.05 * a + 0.12 * b)
        return np.clip(np.array(h), 0, 1)

    fast, slow = mood(0.5), mood(0.85)
    below = lambda h: int(np.sum(h[16:] < 0.45))
    return {"rpe": rpe, "fast": fast, "slow": slow, "below_fast": below(fast), "below_slow": below(slow)}


ITEMS = {"paradox": compute_paradox, "tradeoff": compute_tradeoff, "attenuate": compute_attenuate,
         "biotypes": compute_biotypes, "travel": compute_travel, "pai": compute_pai, "mood": compute_mood}

if __name__ == "__main__":
    CACHE.main(ITEMS)
