"""Precompute everything in Part 41 of *Philosophy, Built* ("Fair Machines").

    python -m videos.philosophy.philosophy41.compute            # everything missing (seconds)

Items:
    criteria      one threshold, two groups: rates, Chouldechova's identity, balance and calibration
    sweep         rates and score histograms as the threshold moves
    thresholds    group-specific thresholds: equal false-positive rates, or equal precision
    unaware       fairness through unawareness fails: a proxy carries the group
    trilemma      the Price List for the fairness impossibility
    cf            counterfactual fairness on a structural causal model
    laplace       the Laplace mechanism at four privacy levels
    rr            randomized response, simulated
    compose       basic and advanced composition of privacy loss
    reconstruct   a reconstruction attack on noisy subset sums
    explain       Shapley values and a counterfactual explanation for a toy credit model
"""

from __future__ import annotations

from explainer.ai.cache import Cache
from explainer.philosophy.reasoner import fairness as F
from explainer.philosophy.reasoner import prop

CACHE = Cache("philosophy41")
load = CACHE.load

TRILEMMA = [
    ("CAL", r"the score is calibrated in each group"),
    ("BAL", r"error rates are equal across groups"),
    ("BASE", r"the groups' base rates differ"),
    ("IMPERF", r"prediction is imperfect"),
]


def compute_trilemma():
    claims = {k: prop.Var(k) for k, _ in TRILEMMA}
    bg = [prop.Not(prop.And(*[prop.Var(k) for k, _ in TRILEMMA]))]
    res = prop.mus_mcs(claims, bg)
    return {"claims": [{"key": k, "text": t} for k, t in TRILEMMA], "mus": [sorted(x) for x in res["mus"]],
            "mcs": [sorted(x) for x in res["mcs"]]}


ITEMS = {"criteria": F.criteria, "sweep": F.sweep, "thresholds": F.group_thresholds, "unaware": F.unawareness, "trilemma": compute_trilemma,
         "cf": F.counterfactual, "laplace": F.laplace, "rr": F.randomized_response, "compose": F.composition,
         "reconstruct": F.reconstruction, "explain": F.explain}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
