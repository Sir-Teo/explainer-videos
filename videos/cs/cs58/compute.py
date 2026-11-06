"""Precompute everything numerical in Part 58 of *Computer Science, Built* ("Semantics").

    python -m videos.cs.cs58.compute              # everything missing

Results are cached in ``.cache/cs58/<name>.json``; scenes call ``load(name)``.  The instrument is
``explainer/cs/semantics/meaning.py``; tests in tests/test_cs58_semantics.py.

Items:
    agree       small-step, big-step and CEK agree on 300 random programs; an example reduction
    fact        the small-step trace of factorial 3
    kleene      the Kleene chain of the factorial functional
    nbe         normalization by evaluation against normal-order reduction on Church numerals
    free        free theorems checked by property tests, and sort's counterexample for a non-monotone map
    bisim       a.(b + c) against a.b + a.c: the same traces, not bisimilar; two vending machines that are
    monads      one program in the Maybe, State and List monads
"""

from __future__ import annotations

from explainer.ai.cache import Cache

CACHE = Cache("cs58")
load = CACHE.load


def _M():
    from explainer.cs.semantics import meaning
    return meaning


def compute_agree() -> dict:
    return _M().agreement()


def compute_fact() -> dict:
    return _M().fact_trace()


def compute_kleene() -> dict:
    return {"rows": _M().kleene()}


def compute_nbe() -> dict:
    return {"rows": _M().nbe_experiment()}


def compute_free() -> dict:
    return _M().free_theorems()


def compute_bisim() -> dict:
    return _M().bisim_examples()


def compute_monads() -> dict:
    return _M().monads()


ITEMS = {k[8:]: v for k, v in globals().items() if k.startswith("compute_")}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
