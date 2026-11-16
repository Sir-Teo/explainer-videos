"""Precompute every number in Part 39 of *Psychology, Built* ("What Is a Disorder?").

    python -m videos.psychology.psych39.compute            # everything missing (about a minute)
    python -m videos.psychology.psych39.compute --force sweep

Results are cached in ``.cache/psych39/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Models are Psyche's
(``explainer.psychology.psyche.clinic``).  Published numbers are quoted in the scenes with their sources.
Simulations use fixed seeds; where a scene shows one simulated sample, it is the median of many by a rule fixed in
advance.

Items:
    kappa       two clinicians rating 2,000 patients (20% true cases) with observation noise from 0 to 2.5 SD:
                their kappa, and their agreement with the true state, averaged over 20 samples per noise level
    combos      the symptom combinations that meet a five-of-nine rule with one of two core symptoms (227), and the
                smallest overlap between two qualifying combinations
    comorbid    nine diagnoses from a general factor and three domains (20,000 people): correlations, the first
                principal component's share, how many people with one diagnosis have another
    sweep       a nine-symptom network with strong (c = 1) and weak (c = 0.2) connections, stress raised and then
                lowered (30 runs each): active symptoms on the way up and down
    episode     the strong network under everyday stress (1.6) with a stress spike between steps 60 and 120: the run
                with the median time to recover, of 21
    screen      a test with 90% sensitivity and 91% specificity for a condition with 1% prevalence, in 10,000 people
    meehl       a five-cue outcome predicted by true weights, fitted weights, equal weights and a clinician whose weights
                wander case to case: correlation with the outcome on new cases, over 50 samples
"""

from __future__ import annotations

from itertools import combinations

import numpy as np

from explainer.ai.cache import Cache
from explainer.psychology.psyche import clinic as K

CACHE = Cache("psych39")
load = CACHE.load


def compute_kappa() -> dict:
    noise = np.linspace(0.0, 2.5, 11)
    kap, val = [], []
    for nz in noise:
        rs = [K.two_clinicians(noise=float(nz), seed=s) for s in range(20)]
        kap.append(np.mean([r["kappa"] for r in rs]))
        val.append(np.mean([r["validity"] for r in rs]))
    return {"noise": noise, "kappa": np.array(kap), "validity": np.array(val)}


def compute_combos() -> dict:
    sets = [set(c) for r in range(5, 10) for c in combinations(range(9), r) if 0 in c or 1 in c]
    five = [s for s in sets if len(s) == 5]
    min_overlap = min(len(a & b) for a in five for b in five)
    return {"n": len(sets), "min_overlap": min_overlap, "n_five": len(five)}


def compute_comorbid() -> dict:
    m = K.comorbidity()
    return {"names": m["names"], "domain": m["domain"], "R": m["R"], "pc1": m["pc1"],
            "share_comorbid": m["share_comorbid"], "any": m["any"]}


def compute_sweep() -> dict:
    out = {}
    for tag, c in (("strong", 1.0), ("weak", 0.2)):
        s = K.sweep(c=c, reps=30, seed=39)
        out["levels"] = s["levels"]
        out[f"{tag}_up"], out[f"{tag}_down"] = s["up"], s["down"]
    return out


def compute_episode() -> dict:
    def run(seed, c):
        rng = np.random.default_rng(seed)
        net = K.ising_network(c=c, b=-4.0 - c * 4 + 2.0, seed=seed)
        x = np.zeros(9)
        out = []
        for t in range(300):
            s = 4.0 if 60 <= t < 120 else 1.6
            x = K._run(net, x, s, 20, rng)
            out.append(x.sum())
        return np.array(out)

    def recover(r):
        after = np.where(r[120:] <= 2)[0]
        return after[0] if len(after) else 180

    res = {}
    for tag, c in (("strong", 1.0), ("weak", 0.2)):
        runs = [run(s, c) for s in range(21)]
        rec = np.array([recover(r) for r in runs])
        k = int(np.argsort(rec)[len(rec) // 2])
        res[f"{tag}_path"], res[f"{tag}_recover"] = runs[k], int(rec[k])
        res[f"{tag}_onset"] = int(np.where(runs[k][60:] >= 6)[0][0]) if np.any(runs[k][60:] >= 6) else -1
    return res


def compute_screen() -> dict:
    return K.screen()


def compute_meehl() -> dict:
    rs = [K.clinician_vs_formula(seed=s) for s in range(50)]
    return {k: float(np.mean([r[k] for r in rs])) for k in rs[0]}


ITEMS = {"kappa": compute_kappa, "combos": compute_combos, "comorbid": compute_comorbid, "sweep": compute_sweep,
         "episode": compute_episode, "screen": compute_screen, "meehl": compute_meehl}

if __name__ == "__main__":
    CACHE.main(ITEMS)
