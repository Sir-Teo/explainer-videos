"""Precompute everything in Part 28 of *Philosophy, Built* ("Meaning in Use").

    python -m videos.philosophy.philosophy28.compute            # everything missing (seconds to a minute)

Items:
    opn         the Tractatus: all 16 truth functions from operation N
    family      family resemblance among six games
    quus        plus and quus on a record of 1000 sums
    proxy       Quine's proxy functions on 300 random sentences
    gavagai     stimulus meaning under three translations
    charity     radical interpretation: charity picks a translation scheme
    reference   the RSA reference game
    scalar      the RSA scalar implicature 'some, not all'
    alphas      the pragmatic listener's 'not all' as rationality grows
    sig2        a 2x2 signalling game learned by Roth-Erev reinforcement
    sig3        a 3x3 signalling game learned by Roth-Erev reinforcement
    vectors     word vectors from a small corpus
    probe       probes for category and for fictionality
    ground      the Price List for the grounding question
    sweep       charity against the speakers' error rate, 200 trials each
    levels      RSA listeners at recursion depths 0..6
    score       Brandom's deontic scorekeeping on a six-move conversation
    analogies   three vector analogies on the small corpus
"""

from __future__ import annotations

from explainer.ai.cache import Cache
from explainer.philosophy.reasoner import pragmatics as G
from explainer.philosophy.reasoner import prop

CACHE = Cache("philosophy28")
load = CACHE.load

GROUND = [
    ("M", r"meaning requires reference"),
    ("R", r"reference requires causal contact with what is referred to"),
    ("T", r"a model trained only on text has no such contact"),
    ("O", r"a language model's outputs are meaningful"),
]


def compute_ground():
    claims = {k: prop.Var(k) for k, _ in GROUND}
    bg = [prop.Not(prop.And(*[prop.Var(k) for k, _ in GROUND]))]
    res = prop.mus_mcs(claims, bg)
    return {"claims": [{"key": k, "text": t} for k, t in GROUND], "mus": [sorted(x) for x in res["mus"]],
            "mcs": [sorted(x) for x in res["mcs"]]}


def compute_alphas():
    rows = []
    for a in (0.5, 1.0, 2.0, 4.0, 8.0):
        r = G.scalar(alpha=a)
        rows.append({"alpha": a, "p_all_given_some": r["L1"][1][3], "p_some_lit": r["L0"][1][3]})
    return {"rows": rows}


ITEMS = {"opn": G.operation_n, "family": G.family, "quus": G.plus_quus, "proxy": G.proxy, "gavagai": G.gavagai,
         "charity": G.charity, "reference": G.reference_game, "scalar": G.scalar, "alphas": compute_alphas,
         "sig2": lambda: G.signalling(2, rounds=6000, runs=200), "sig3": lambda: G.signalling(3, rounds=6000, runs=200),
         "vectors": G.vectors, "probe": G.probe, "ground": compute_ground, "sweep": G.charity_sweep,
         "levels": G.recursion, "score": G.scorekeeping, "analogies": G.analogies}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
