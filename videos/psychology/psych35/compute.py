"""Precompute every number in Part 35 of *Psychology, Built* ("Social Cognition").

    python -m videos.psychology.psych35.compute            # everything missing (a few seconds)
    python -m videos.psychology.psych35.compute --force goals

Results are cached in ``.cache/psych35/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Models are Psyche's
(``explainer.psychology.psyche.social``).  Published numbers are quoted in the scenes with their sources.
Simulations use fixed seeds.

Items:
    kelley      three patterns of Kelley's cube (person, entity, circumstance) and the share of variance each main
                effect carries
    essays      a rational observer of Jones and Harris's essays: the attitude inferred from a pro or anti essay when
                the writer chose, and when the observer is not sure the assignment fully constrained the essay
    dk          the Dunning-Kruger quartile plot from a modest correlation and a better-than-average shift, and from
                a perfect correlation with no shift
    goals       inverse planning in a gridworld: three goals, two walks, the posterior over goals after every step
    curse       the winner's curse: small studies of a true effect of zero or 0.2, the ones that reach significance,
                and how large they look, against one large study
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.psychology.psyche import social as S

CACHE = Cache("psych35")
load = CACHE.load

SHAPE = (7, 9)
WALLS = [(r, 4) for r in range(1, 6)]
GOALS = [(0, 8), (6, 8), (3, 0)]


def compute_kelley() -> dict:
    out = {}
    for name in ("person", "entity", "circumstance"):
        T = np.zeros((5, 5, 4))
        if name == "person":  # only person 0, with every entity, every time
            T[0, :, :] = 1
        elif name == "entity":  # everyone, only with entity 0, every time
            T[:, 0, :] = 1
        else:  # person 0 with entity 0, on one occasion only
            T[0, 0, 0] = 1
        k = S.kelley(T)
        out[name] = {"shares": k["shares"], "consensus": k["consensus"], "distinctiveness": k["distinctiveness"],
                     "consistency": k["consistency"]}
    return out


def compute_essays() -> dict:
    """Attitude a ~ N(0, 1).  A writer who chooses writes pro with probability Phi(2a).  An assigned writer's essay
    is pro by assignment; the observer thinks there is a chance pi that the assignment was not binding (the writer's
    attitude still shaped what was written).  Returns the posterior mean of a for pro and anti essays."""
    from scipy.stats import norm
    a = np.linspace(-4, 4, 4001)
    prior = norm.pdf(a)
    lik_pro = norm.cdf(2 * a)
    out = {}
    for pi in (1.0, 0.3, 0.0):
        lp = pi * lik_pro + (1 - pi) * 0.5
        la = pi * (1 - lik_pro) + (1 - pi) * 0.5
        mp = float(np.sum(a * prior * lp) / np.sum(prior * lp))
        ma = float(np.sum(a * prior * la) / np.sum(prior * la))
        out[f"pi{int(pi * 100)}"] = [mp, ma]
    return out


def compute_dk() -> dict:
    a = S.dunning_kruger(n=4000, rho=0.3, shift=15, seed=35)
    b = S.dunning_kruger(n=4000, rho=1.0, shift=0, seed=35)
    c = S.dunning_kruger(n=4000, rho=0.0, shift=0, seed=35)
    return {"actual": a["actual"], "noisy": a["perceived"], "perfect": b["perceived"], "random": c["perceived"]}


def compute_goals() -> dict:
    walks = {
        "up": [(3, 3), (2, 3), (1, 3), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8)],
        "turn": [(3, 6), (2, 6), (1, 6), (0, 6), (0, 5), (0, 4), (0, 3), (1, 3), (2, 3), (3, 3), (3, 2), (3, 1),
                 (3, 0)],
    }
    out = {"walls": WALLS, "goals": GOALS}
    for k, path in walks.items():
        out[f"path_{k}"] = path
        out[f"post_{k}"] = S.goal_posterior(path, SHAPE, WALLS, GOALS, beta=0.7)
    return out


def compute_curse() -> dict:
    """Two-group studies with n per group; d_true 0 or 0.2.  Among small studies (n = 21 per group, as in a study of
    42) that reach p < .05 in the predicted direction, the observed d; and the share that reach it."""
    rng = np.random.default_rng(35)
    from scipy.stats import t as tdist
    out = {}
    for dt in (0.0, 0.2):
        for n in (21, 100):
            reps = 20000
            x = rng.normal(dt, 1, (reps, n))
            y = rng.normal(0, 1, (reps, n))
            diff = x.mean(1) - y.mean(1)
            sp = np.sqrt((x.var(1, ddof=1) + y.var(1, ddof=1)) / 2)
            d = diff / sp
            tt = diff / (sp * np.sqrt(2 / n))
            sig = tt > tdist.ppf(0.975, 2 * n - 2)
            key = f"d{int(dt * 10)}_n{n}"
            out[key + "_power"] = float(sig.mean())
            out[key + "_dsig"] = float(d[sig].mean())
            out[key + "_hist"] = np.histogram(d[sig], bins=np.linspace(0, 1.6, 33))[0]
    return out


ITEMS = {"kelley": compute_kelley, "essays": compute_essays, "dk": compute_dk, "goals": compute_goals,
         "curse": compute_curse}


if __name__ == "__main__":
    CACHE.main(ITEMS)
