"""Precompute everything in Part 15 of *Philosophy, Built* ("The Problem of Induction").

    python -m videos.philosophy.philosophy15.compute            # everything missing (a few seconds)

Items:
    laplace     the rule of succession, the sunrise, and Carnap's lambda-continuum
    wheel       Dignāga's wheel of reasons, checked on nine small universes
    ravens      Bayes factors for a black raven and a white shoe; the ravens Price List
    measures    six confirmation measures on two pieces of evidence that the measures rank differently
    grue        one learner, two encodings; and a small network with a feature the data never fix
    popper      the Miller--Tichý theorem over three atoms; Tichý's likeness and Miller's translation
    explain     Douven's explanationist against a Bayesian: speed, accuracy, and false confidence
    merging     two Bayesians' predictions converging, and a dogmatist who never does
    gold        Gold's adversary against a learner; Putnam's diagonal against Laplace
    ockham      Kelly's retraction game
    solomonoff  a mixture over repeating programs predicting 011011...
    mdl         two-part code lengths for polynomial degree
    lunch       no free lunch over all 256 Boolean targets; and in a smooth world
    straight    Reichenbach's straight rule
    meta        meta-induction: exponential weights over five methods, and its regret bound
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.philosophy.reasoner import induction as I
from explainer.philosophy.reasoner import prop

CACHE = Cache("philosophy15")
load = CACHE.load

RAVENS = [("R1", r"Nicod: \ a black raven confirms `all ravens are black'", "a"),
          ("R2", r"equivalence: \ what confirms a claim confirms its logical equivalents", "b"),
          ("R3", r"a white shoe does not confirm `all ravens are black'", "c")]


def compute_laplace() -> dict:
    lam = {}
    for L in (0, 1, 2, 10, 100):
        lam[str(L)] = [[n, (0.8 * n + L / 2) / (n + L) if n + L > 0 else 0.5] for n in range(0, 51)]
    return {"sunrise": I.sunrise(), "after_8_of_10": {str(L): (8 + L / 2) / (10 + L) for L in (0, 2, 10, 100)},
            "lambda": lam}


def compute_wheel() -> dict:
    return {"cells": I.hetucakra()}


def compute_ravens() -> dict:
    claims = {k: prop.parse(f) for k, _, f in RAVENS}
    res = prop.mus_mcs(claims, [prop.parse("(a & b & c) -> F"), prop.parse("~F")])
    return {"bayes": I.ravens(), "claims": [{"key": k, "text": t} for k, t, _ in RAVENS],
            "mus": [sorted(x) for x in res["mus"]], "mcs": [sorted(x) for x in res["mcs"]]}


def compute_measures() -> dict:
    return {**I.ordinal_disagreement(), "desiderata": I.desiderata()}


def _mlp(x, y, xs_out, hidden=8, steps=3000, lr=0.5, seed=0, extra=None, extra_out=None):
    """A one-hidden-layer tanh network with a sigmoid output, trained by full-batch gradient descent."""
    rng = np.random.default_rng(seed)
    X = x[:, None] if extra is None else np.stack([x, extra], axis=1)
    Xo = xs_out[:, None] if extra_out is None else np.stack([xs_out, extra_out], axis=1)
    W1 = rng.normal(scale=1.0, size=(X.shape[1], hidden))
    b1 = rng.normal(scale=0.5, size=hidden)
    W2 = rng.normal(scale=1.0, size=hidden)
    b2 = 0.0
    for _ in range(steps):
        h = np.tanh(X @ W1 + b1)
        p = 1 / (1 + np.exp(-(h @ W2 + b2)))
        g = (p - y) / len(y)
        W2 -= lr * h.T @ g
        b2 -= lr * g.sum()
        gh = np.outer(g, W2) * (1 - h ** 2)
        W1 -= lr * X.T @ gh
        b1 -= lr * gh.sum(axis=0)
    h = np.tanh(Xo @ W1 + b1)
    return 1 / (1 + np.exp(-(h @ W2 + b2)))


def compute_grue() -> dict:
    T, H = 10, 20
    t = np.arange(T) / H
    tf = np.arange(H) / H
    y = np.ones(T)
    # the same network, the same data, two ways of labelling it
    green = _mlp(t, y, tf)                       # P(green)
    grue = _mlp(t, y, tf)                        # P(grue): after T, grue means blue
    # a network that is also told 'is it after T?': in training that feature is always 0, so the data never fix
    # its weight, and different initializations project differently
    after = 3.0 * (np.arange(H) >= T).astype(float)
    runs = []
    for seed in range(8):
        p = _mlp(t, y, tf, seed=seed, steps=400, extra=np.zeros(T), extra_out=after)
        runs.append([float(v) for v in p])
    return {"T": T, "H": H, "basic": I.grue(), "green": [float(v) for v in green], "grue": [float(v) for v in grue],
            "stepped": runs, "after_T_green": [float(np.mean(r[T:])) for r in runs],
            "train_fit": [float(np.mean(r[:T])) for r in runs]}


def compute_popper() -> dict:
    return {"mt": I.miller_tichy(), "lang": I.miller_language()}


def compute_explain() -> dict:
    d = I.explanationist()
    for k in ("bayes", "ibe"):
        d[k]["curve"] = d[k]["curve"][::3]
    return d


def compute_merging() -> dict:
    m = I.merging()
    keep = list(range(0, m["n"] + 1, 4))
    return {"truth": m["truth"], "n": m["n"], "idx": keep, "a": [m["a"][i] for i in keep],
            "b": [m["b"][i] for i in keep], "c": [m["c"][i] for i in keep], "gap": [m["gap"][i] for i in keep]}


def compute_gold() -> dict:
    g = I.gold_adversary(I.conservative_learner(3), steps=30)
    d = I.putnam_diagonal(I.laplace_predictor, 24)
    return {"gold": g, "putnam": d}


def compute_ockham() -> dict:
    return I.ockham()


def compute_solomonoff() -> dict:
    return {"run": I.solomonoff_run("011", 18), "count": sum(1 for _ in I.programs(8))}


def compute_mdl() -> dict:
    return I.mdl_degree()


def compute_lunch() -> dict:
    return {"all": I.no_free_lunch(), "smooth": I.smooth_world_lunch(), "slice": I.nfl_slice(), "vc": I.shattering()}


def compute_straight() -> dict:
    return I.straight_rule()


def compute_meta() -> dict:
    m = I.meta_induction()
    keep = list(range(0, m["T"], 3)) + [m["T"] - 1]
    return {**{k: m[k] for k in ("T", "names", "bound", "final", "final_forecaster", "eta")}, "idx": keep,
            "cum": {n: [m["cum"][n][i] for i in keep] for n in m["names"]},
            "forecaster": [m["forecaster"][i] for i in keep], "regret": [m["regret"][i] for i in keep],
            "max_regret": max(m["regret"])}


ITEMS = {"laplace": compute_laplace, "wheel": compute_wheel, "ravens": compute_ravens, "measures": compute_measures,
         "grue": compute_grue, "popper": compute_popper, "explain": compute_explain, "merging": compute_merging, "gold": compute_gold, "ockham": compute_ockham,
         "solomonoff": compute_solomonoff, "mdl": compute_mdl, "lunch": compute_lunch, "straight": compute_straight, "meta": compute_meta}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
