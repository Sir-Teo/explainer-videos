"""Precompute everything numerical in Part 59 of *Computer Science, Built* ("Distributed Computing Theory").

    python -m videos.cs.cs59.compute              # everything missing

Results are cached in ``.cache/cs59/<name>.json``; scenes call ``load(name)``.  The instrument is
``explainer/cs/disttheory/theory.py`` (and Part 38's ``explainer/cs/dist/consensus.py``); tests in
tests/test_cs59_disttheory.py.

Items:
    cv          Cole-Vishkin on a ring of a million nodes: rounds, colours per round, the first nodes' colours
    cvscale     rounds against log* n from 10 to a million nodes
    logstar     log* of 2, 4, 16, 65,536 and 2^65,536
    hexagon     the hexagon argument run against a majority protocol: the pairs that must disagree
    floodset    FloodSet with f crashes needs f + 1 rounds: exhaustive checks
    benor       Ben-Or's rounds with split inputs, by n and f
    sperner     a Sperner colouring of a subdivided triangle and its rainbow triangles; parity over 200 trials
    majority    the four-state exact-majority population protocol: a run and parallel time against n
"""

from __future__ import annotations

from explainer.ai.cache import Cache

CACHE = Cache("cs59")
load = CACHE.load


def _T():
    from explainer.cs.disttheory import theory
    return theory


def compute_cv() -> dict:
    return _T().cole_vishkin()


def compute_cvscale() -> dict:
    return {"rows": _T().cv_scaling()}


def compute_logstar() -> dict:
    return {"rows": _T().log_star_table()}


def compute_hexagon() -> dict:
    return _T().hexagon()


def compute_floodset() -> dict:
    return {"rows": _T().floodset_table()}


def compute_benor() -> dict:
    return {"rows": _T().ben_or_rounds()}


def compute_sperner() -> dict:
    return {"example": _T().sperner(), "check": _T().sperner_check()}


def compute_majority() -> dict:
    return {"run": _T().majority(n=100, margin=4, trials=1), "scaling": _T().majority_scaling()}


ITEMS = {k[8:]: v for k, v in globals().items() if k.startswith("compute_")}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
