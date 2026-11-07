"""Precompute everything numerical in Part 61 of *Computer Science, Built* ("Doing Research", the coda).

    python -m videos.cs.cs61.compute              # everything missing

Results are cached in ``.cache/cs61/<name>.json``; scenes call ``load(name)``.  The instrument is
``explainer/cs/research/method.py``; tests in tests/test_cs61_research.py.

Items:
    bias        measurement bias on this machine: environment size and link order against a C version of the Job
    stack       does the stack start at the same address on every run? (a C probe, run 20 times)
    timing      the Job in Python, timed 30 times: bootstrap intervals, and how they narrow with runs
    means       arithmetic against geometric means of speedups
    goldbach    Goldbach's conjecture checked to two million, with its records
    collatz     the Collatz conjecture checked to a million, with its record stopping times
    open        the open problems the series met, with their records
    ledger      the final ledger: every row, from Part 6's single-cycle Pebble to Part 60's accelerator
"""

from __future__ import annotations

import json

from explainer.ai.cache import Cache

CACHE = Cache("cs61")
load = CACHE.load


def _M():
    from explainer.cs.research import method
    return method


def compute_bias() -> dict:
    return _M().measurement_bias()


def compute_stack() -> dict:
    return _M().stack_randomization()


def compute_timing() -> dict:
    return _M().job_timing()


def compute_means() -> dict:
    return _M().speedup_means()


def compute_goldbach() -> dict:
    return _M().goldbach()


def compute_collatz() -> dict:
    return _M().collatz()


def compute_open() -> dict:
    return {"rows": _M().open_problems()}


def compute_ledger() -> dict:
    for part in ("cs60", "cs55"):
        p = Cache(part).dir / "ledger.json"
        if p.exists():
            return {"rows": json.loads(p.read_text()), "source": part}
    raise FileNotFoundError("no ledger yet: run Part 55 and Part 60's compute first")


ITEMS = {k[8:]: v for k, v in globals().items() if k.startswith("compute_")}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
