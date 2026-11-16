"""Precompute every number in Part 40 of *Psychology, Built* ("Fear and Sadness").

    python -m videos.psychology.psych40.compute            # everything missing (a few seconds)
    python -m videos.psychology.psych40.compute --force mood

Results are cached in ``.cache/psych40/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Models are Psyche's
(``explainer.psychology.psyche.clinic``).  Published numbers are quoted in the scenes with their sources.
Simulations use fixed seeds; where a scene shows one simulated sample, it is the median of many by a rule fixed in
advance.

Items:
    avoid       Mowrer's two factors: 20 pairings, then 60 trials without shock, with avoidance allowed (the run with
                the median final fear of 21) and with response prevention
    renewal     acquisition in context A, extinction in B, tests in B, A and a new context C
    contexts    extinction spread over 1 to 6 contexts, each sharing a quarter of its features with a new one: the
                fear that returns in the new context
    suicide     a risk factor with sensitivity and specificity 0.8 for a death with a base rate of 1 in 2,000 a year,
                in natural frequencies for 10,000 people
    helpless    the triadic design: escapable, inescapable and no pretreatment, 200 animals each, 10 test trials
    activation  the behavioural-activation trap: 90 days, an activity whose value starts low after a loss and is
                learned only by doing it, against rest; left alone, or with the activity scheduled for 14 days (21
                runs each; the run with the median share of active days in the last 30 is shown)
    mood        a 90-trial gambling task with happiness ratings, simulated with Rutledge and colleagues' weights and
                fitted; and the same person with reward prediction errors blunted to 40%
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.psychology.psyche import clinic as K

CACHE = Cache("psych40")
load = CACHE.load


def compute_avoid() -> dict:
    runs = [K.avoidance(seed=s) for s in range(21)]
    finals = np.array([r["fear"][-1] for r in runs])
    k = int(np.argsort(finals)[len(finals) // 2])
    exp = K.avoidance(prevent=True)
    return {"fear": runs[k]["fear"], "avoided": runs[k]["avoided"].astype(float), "exposure": exp["fear"],
            "share_avoided": float(runs[k]["avoided"][20:].mean()), "final": float(finals[k]),
            "final_exposure": float(exp["fear"][-1])}


def compute_renewal() -> dict:
    r = K.renewal()
    return {"trace": r["trace"], "B": r["test"]["B"], "A": r["test"]["A"], "C": r["test"]["C"]}


def compute_contexts() -> dict:
    r = K.renewal_contexts()
    return {"n": r["n"], "g": r["g"], "fear": r["fear"]}


def compute_suicide() -> dict:
    return K.screen(N=10000, prevalence=1 / 2000, sensitivity=0.8, specificity=0.8)


def compute_helpless() -> dict:
    return {p: K.helplessness(p, seed=40) for p in ("escapable", "inescapable", "none")}


def compute_activation() -> dict:
    out = {}
    for name, sch in (("alone", 0), ("scheduled", 14)):
        runs = [K.activation(sch, seed=s) for s in range(21)]
        share = np.array([r["active"][-30:].mean() for r in runs])
        k = int(np.argsort(share, kind="stable")[len(share) // 2])
        out[f"{name}_est"] = runs[k]["estimate"]
        out[f"{name}_act"] = runs[k]["active"].astype(float)
        out[f"{name}_share"] = float(share[k])
    return out


def compute_mood() -> dict:
    d = K.mood_task(seed=40)
    f = K.fit_mood(d)
    b = K.mood_task(seed=40, rpe_scale=0.4)
    return {"happy": d["happy"], "fit": f["fit"], "w": f["w"], "gamma": f["gamma"], "r2": f["r2"],
            "true_w": d["true_w"], "rpe": d["RPE"], "blunted": b["happy"],
            "sd_normal": float(np.std(d["happy"])), "sd_blunted": float(np.std(b["happy"]))}


ITEMS = {"avoid": compute_avoid, "renewal": compute_renewal, "contexts": compute_contexts, "suicide": compute_suicide, "helpless": compute_helpless, "activation": compute_activation, "mood": compute_mood}

if __name__ == "__main__":
    CACHE.main(ITEMS)
