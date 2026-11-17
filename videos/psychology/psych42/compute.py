"""Precompute every number in Part 42 of *Psychology, Built* ("Does Therapy Work?").

    python -m videos.psychology.psych42.compute            # everything missing (a few seconds)
    python -m videos.psychology.psych42.compute --force bias

Results are cached in ``.cache/psych42/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Models are Psyche's
(``explainer.psychology.psyche.clinic``).  Published numbers are quoted in the scenes with their sources.
Simulations use fixed seeds.

Items:
    arms        the trial simulator: 200 people per arm who enrol at a score of 20 or more (no treatment, waiting
                list, placebo therapy, active therapy); entry and end means; and the active arm's effect against
                each control in 2,000 per arm
    forest      twelve simulated trials of a therapy with true effect 0.5 (between-trial SD 0.15) and their
                DerSimonian-Laird random-effects summary
    bias        400 trials of a true effect of 0.3; the published ones (significant, plus a fifth of the rest);
                random-effects summaries of all and of the published
    allegiance  60 comparisons of two equally good therapies, half run by each side's loyal team (bias 0.25)
    rci         Jacobson and Truax for a depression scale (SD 7, reliability 0.85; clinical mean 28 SD 6, well mean 7
                SD 5): the reliable-change threshold, the cut-off, and four example patients
    categories  Jacobson and Truax's categories (recovered, improved, unchanged, deteriorated) in 2,000 people per arm
                of the trial simulator (SD 7.07, the population's; reliability 0.85; cut-off between the enrolled and
                the population), for the four arms and for a therapy that makes people 3 points worse
    dose        the share improved after 0 to 52 sessions (half by 8, three quarters by 26)
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.psychology.psyche import clinic as K

CACHE = Cache("psych42")
load = CACHE.load


def compute_arms() -> dict:
    out = {}
    for a in K.ARMS:
        r = K.therapy_trial(a, seed=42)
        out[f"{a}_pre"] = float(r["pre"].mean())
        out[f"{a}_post"] = float(r["post"].mean())
    for b in ("none", "waitlist", "placebo"):
        out[f"d_{b}"] = K.trial_effect("active", b, n=2000, seed=42)
    return out


def compute_forest() -> dict:
    rng = np.random.default_rng(42)
    n = np.array([18, 25, 30, 40, 22, 60, 35, 80, 28, 45, 120, 50])
    theta = rng.normal(0.5, 0.15, len(n))
    v = 2 / n + theta ** 2 / (4 * n)
    d = rng.normal(theta, np.sqrt(v))
    r = K.random_effects(d, v)
    return {"d": d, "v": v, "n": n, **{k: float(x) for k, x in r.items()}}


def compute_bias() -> dict:
    p = K.publication_filter(seed=42)
    a = K.random_effects(p["d"], p["v"])
    b = K.random_effects(p["d"][p["published"]], p["v"][p["published"]])
    return {"d": p["d"], "v": p["v"], "published": p["published"].astype(float), "mu_all": a["mu"], "mu_pub": b["mu"],
            "n_pub": int(p["published"].sum()), "share_sig_pub": float(p["significant"][p["published"]].mean()),
            "share_sig_all": float(p["significant"].mean())}


def compute_allegiance() -> dict:
    a = K.allegiance(seed=42)
    allr = K.random_effects(a["d"], a["v"])
    pa = K.random_effects(a["d"][a["loyal"] > 0], a["v"][a["loyal"] > 0])
    pb = K.random_effects(a["d"][a["loyal"] < 0], a["v"][a["loyal"] < 0])
    return {"d": a["d"], "loyal": a["loyal"], "mu_all": allr["mu"], "mu_a": pa["mu"], "mu_b": pb["mu"]}


def compute_rci() -> dict:
    sd, rxx = 7.0, 0.85
    thr = 1.96 * np.sqrt(2) * sd * np.sqrt(1 - rxx)
    c = K.jt_cutoff(28.0, 6.0, 7.0, 5.0)
    pts = np.array([[30, 14], [30, 25], [22, 15], [34, 20]], float)
    rci = K.reliable_change(pts[:, 0], pts[:, 1], sd, rxx)
    return {"threshold": float(thr), "cutoff": float(c), "pre": pts[:, 0], "post": pts[:, 1], "rci": rci}


def compute_categories() -> dict:
    sd = float(np.sqrt(50.0))
    ref = K.therapy_trial("none", n=2000, seed=42)
    cut = K.jt_cutoff(float(ref["pre"].mean()), float(ref["pre"].std()), 14.0, sd)
    out = {"cutoff": cut}
    arms = dict(K.ARMS, harmful=-3.0)
    for a in arms:
        r = K.therapy_trial(a, n=2000, seed=42, effects=arms)
        c = K.jt_categories(r["pre"], r["post"], sd, 0.85, cut)
        for k, v in c.items():
            out[f"{a}_{k}"] = float(v)
    return out


def compute_dose() -> dict:
    s = np.linspace(0, 52, 209)
    return {"sessions": s, "share": K.dose_response(s)}


ITEMS = {"arms": compute_arms, "forest": compute_forest, "bias": compute_bias, "allegiance": compute_allegiance,
         "rci": compute_rci, "categories": compute_categories, "dose": compute_dose}

if __name__ == "__main__":
    CACHE.main(ITEMS)
