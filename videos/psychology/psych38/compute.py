"""Precompute every number in Part 38 of *Psychology, Built* ("Culture and Morals").

    python -m videos.psychology.psych38.compute            # everything missing (a few seconds)
    python -m videos.psychology.psych38.compute --force trolley

Results are cached in ``.cache/psych38/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Models are Psyche's
(``explainer.psychology.psyche.culture``).  Published numbers are quoted in the scenes with their sources.
Simulations use fixed seeds; where a scene shows one simulated sample, it is the median of many by a rule fixed in
advance.

Items:
    conform     conformist transmission (D = 0.3): the expected share of a variant from four starting shares, and
                one finite population of 200 learners per start (the run with the median final share of 21)
    prestige    copying the most successful of five models: a useless marker carried by 10% of the population,
                mostly the skilled, over 30 generations (the run with the median final share of 21)
    tasmania    Henrich's model (alpha = 4.5, beta = 1): the expected gain per generation against population size,
                the critical size, and the best skill over 60 generations for 20, 50 and 200 learners (median run
                of 21 by final skill)
    refgroup    two cultures 0.8 SD apart on a trait; self-reports on a 1-7 scale made relative to one's own
                culture, and an absolute behavioural measure
    trolley     42 simulated countries, 600 people each, answering switch, loop and footbridge; the additive fit
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.psychology.psyche import culture as C

CACHE = Cache("psych38")
load = CACHE.load

STARTS = (0.3, 0.45, 0.55, 0.7)


def _median_run(runs, key):
    vals = np.array([key(r) for r in runs])
    return runs[int(np.argsort(vals)[len(vals) // 2])]


def compute_conform() -> dict:
    out = {"starts": np.array(STARTS), "D": 0.3}
    for k, p0 in enumerate(STARTS):
        out[f"expected_{k}"] = C.conformist_path(p0, 0.3, 40)
        runs = [C.conformist_sim(200, p0, 0.3, 40, seed=s) for s in range(21)]
        out[f"sim_{k}"] = _median_run(runs, lambda r: r[-1])
    out["step_p"] = np.linspace(0, 1, 101)
    out["step_dp"] = C.conformist_step(out["step_p"], 0.3) - out["step_p"]
    return out


def compute_prestige() -> dict:
    runs = [C.prestige_sim(seed=s) for s in range(21)]
    r = _median_run(runs, lambda r: r["share"][-1])
    finals = np.array([x["share"][-1] for x in runs])
    return {"share": r["share"], "skill": r["skill"], "finals": finals}


def compute_tasmania() -> dict:
    N = np.unique(np.round(np.logspace(0.5, 3, 80)).astype(int))
    out = {"N": N, "gain": C.skill_change(N), "critical": C.critical_size()}
    for n in (20, 50, 200):
        runs = [C.tasmania(n, seed=s) for s in range(21)]
        out[f"path_{n}"] = np.maximum(_median_run(runs, lambda r: r[-1]), 0.0)
    return out


def compute_refgroup() -> dict:
    r = C.reference_group()
    (ra, rb), (ba, bb) = r["report"], r["behaviour"]
    cnt = lambda x: np.array([(x == v).mean() for v in range(1, 8)])
    return {"report_a": cnt(ra), "report_b": cnt(rb), "mean_report": np.array([ra.mean(), rb.mean()]),
            "mean_behaviour": np.array([ba.mean(), bb.mean()]), "gap_report": r["gap_report"],
            "gap_behaviour": r["gap_behaviour"], "gap_trait": r["gap_trait"],
            "beh_a": np.histogram(ba, bins=np.linspace(-4, 5, 37))[0] / len(ba),
            "beh_b": np.histogram(bb, bins=np.linspace(-4, 5, 37))[0] / len(bb)}


def compute_trolley() -> dict:
    t = C.trolley(seed=38)
    f = C.fit_trolley(t["share"])
    order = np.argsort(t["share"][:, 0])
    return {"cases": t["cases"], "share": t["share"][order], "level": t["level"][order],
            "mean": t["share"].mean(axis=0), "lo": t["share"].min(axis=0), "hi": t["share"].max(axis=0),
            "case_fit": f["case"], "order_same": f["order_same"], "resid_sd": f["resid_sd"]}


ITEMS = {"conform": compute_conform, "prestige": compute_prestige, "tasmania": compute_tasmania,
         "refgroup": compute_refgroup, "trolley": compute_trolley}

if __name__ == "__main__":
    CACHE.main(ITEMS)
