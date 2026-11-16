"""Precompute every number in Part 61 of *Psychology, Built* ("The Next Psychology").

    python -m videos.psychology.psych61.compute            # everything missing (seconds)

Results are cached in ``.cache/psych61/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Models are Psyche's
(``explainer.psychology.psyche.community``).

Items:
    challenge   160 modelling teams against a four-variable regression on a simulated cohort
    labs        one effect in 40 labs, with no true variation and with some
    selection   a self-selected sample at sizes from 100 to a million
    space       a space of 1,024 experiments, 120 of them run, and a surrogate model's predictions
    science     the natural selection of bad science, under two publication rules
    adaptive    adaptive against fixed design for telling a power law of forgetting from an exponential
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.psychology.psyche import community as Cm

CACHE = Cache("psych61")
load = CACHE.load


def compute_challenge() -> dict:
    return Cm.challenge(seed=6100)


def compute_labs() -> dict:
    a = Cm.many_labs(tau=0.0, seed=6101)
    b = Cm.many_labs(tau=0.2, seed=6102)
    return {"none_est": a["est"], "none_se": a["se"], "none_I2": a["I2"], "none_pooled": a["pooled"],
            "het_est": b["est"], "het_se": b["se"], "het_I2": b["I2"], "het_pooled": b["pooled"]}


def compute_selection() -> dict:
    return Cm.selected_sample(seed=6103)


def compute_space() -> dict:
    return Cm.integrative(seed=6104)


def compute_science() -> dict:
    a = Cm.bad_science(rule="positive", seed=6105)
    b = Cm.bad_science(rule="registered", seed=6106)
    return {"pos_effort": a["effort"], "pos_fdr": a["fdr"], "reg_effort": b["effort"], "reg_fdr": b["fdr"]}


def compute_overfit() -> dict:
    """Least squares on the first k of the cohort's 400 variables (n = 1,000 to train, 3,000 held out): in-sample
    R^2 rises with every variable added; held-out R^2 peaks and then falls."""
    X, y, r2 = Cm.cohort(n=4000, seed=6107)
    tr, te = slice(0, 1000), slice(1000, 4000)
    ks = np.array([1, 2, 4, 8, 16, 32, 64, 128, 256, 400])
    ins, out = [], []
    for k in ks:
        A = np.column_stack([np.ones(1000), X[tr, :k]])
        w = np.linalg.lstsq(A, y[tr], rcond=None)[0]
        ins.append(1 - np.mean((y[tr] - A @ w) ** 2) / np.var(y[tr]))
        B = np.column_stack([np.ones(3000), X[te, :k]])
        out.append(1 - np.mean((y[te] - B @ w) ** 2) / np.var(y[te]))
    return {"k": ks, "in": np.array(ins), "out": np.array(out), "true_r2": r2}


def compute_ecological() -> dict:
    """3,000 counties of 1,000 people.  A county's income drives both the share of hostile words its people post
    and its heart-disease rate; for a person, hostile posting has almost nothing to do with their own heart.  The
    county-level correlation is large; the person-level one is near zero."""
    rng = np.random.default_rng(6108)
    C, m = 3000, 1000
    income = rng.standard_normal(C)
    word_c = -0.8 * income + 0.6 * rng.standard_normal(C)
    risk_c = -0.8 * income + 0.6 * rng.standard_normal(C)
    words = word_c[:, None] + 3.0 * rng.standard_normal((C, m))
    risk = risk_c[:, None] + 3.0 * rng.standard_normal((C, m))
    county_r = float(np.corrcoef(words.mean(1), risk.mean(1))[0, 1])
    person_r = float(np.corrcoef(words.ravel(), risk.ravel())[0, 1])
    within = words - words.mean(1, keepdims=True), risk - risk.mean(1, keepdims=True)
    within_r = float(np.corrcoef(within[0].ravel(), within[1].ravel())[0, 1])
    idx = rng.choice(C, 400, replace=False)
    return {"cx": words.mean(1)[idx], "cy": risk.mean(1)[idx], "county_r": county_r, "person_r": person_r,
            "within_r": within_r}


def compute_adaptive() -> dict:
    """Two forgetting theories, power and exponential, told apart by recall tests at ten lags: a fixed design that
    cycles through the lags against an adaptive design that picks the most informative lag before each trial."""
    return Cm.adaptive_design(people=2000, trials=80, seed=6109)


ITEMS = {"challenge": compute_challenge, "labs": compute_labs, "selection": compute_selection,
         "space": compute_space, "science": compute_science, "overfit": compute_overfit,
         "ecological": compute_ecological, "adaptive": compute_adaptive}

if __name__ == "__main__":
    CACHE.main(ITEMS)
