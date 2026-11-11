"""Precompute everything numerical in Part 54 of *Computer Science, Built* ("Proving Programs Correct").

    python -m videos.cs.cs54.compute              # everything missing

Results are cached in ``.cache/cs54/<name>.json``; scenes call ``load(name)``.  The instruments are in
``explainer/cs/verify/`` (hoare, absint, lcf, models, bdd, testing); tests in tests/test_cs54_logic.py and
tests/test_cs54_check.py.

Items:
    hoare       verification conditions bit-blasted to Part 26's SAT solver: max, swap, Gauss, binary search;
                the midpoint study (Bloch 2006) with SAT's counterexamples; the backward flow of assertions
    absint      interval analysis with and without widening; the relation intervals cannot see
    lcf         an LCF kernel: four proofs, five refused steps, the kernel's size
    peterson    Peterson's algorithm: mutual exclusion, liveness under fairness, a broken variant's counterexample
    philosophers dining philosophers: state explosion, deadlock found, starvation under weak fairness
    twophase    two-phase commit as a TLA+-style state machine: invariant, refinement, a timeout bug
    raft        Raft-lite: election safety, and the forget-vote bug's two leaders
    bdd         variable order; symbolic reachability up to 16 philosophers; bounded model checking
    pbt         property-based testing with shrinking
    fuzz        a planted constant-folding bug found by differential fuzzing and delta debugging
    job         the Job compiled at every level, against the interpreter and Python (differential testing)
    coverage    what coverage does and does not tell you
"""

from __future__ import annotations

from explainer.ai.cache import Cache

CACHE = Cache("cs54")
load = CACHE.load


def compute_hoare() -> dict:
    from explainer.cs.verify import hoare
    return hoare.examples()


def compute_absint() -> dict:
    from explainer.cs.verify import absint
    return {"examples": absint.examples(), "gap": absint.relational_gap()}


def compute_lcf() -> dict:
    from explainer.cs.verify import lcf
    return {"proofs": lcf.proofs(), "illegal": lcf.illegal_steps(), "size": lcf.kernel_size()}


def compute_peterson() -> dict:
    from explainer.cs.verify import models
    return models.peterson_results()


def compute_philosophers() -> dict:
    from explainer.cs.verify import models
    return models.philosopher_results()


def compute_twophase() -> dict:
    from explainer.cs.verify import models
    return models.two_phase_results()


def compute_raft() -> dict:
    from explainer.cs.verify import models
    return models.raft_results()


def compute_bdd() -> dict:
    from explainer.cs.verify import bdd
    return bdd.all_results()


def compute_pbt() -> dict:
    from explainer.cs.verify import testing
    return testing.pbt_results()


def compute_fuzz() -> dict:
    from explainer.cs.verify import testing
    return testing.fuzz_results()


def compute_job() -> dict:
    from explainer.cs.verify import testing
    return testing.job_differential()


def compute_coverage() -> dict:
    from explainer.cs.verify import testing
    return testing.coverage_results()


ITEMS = {k[8:]: v for k, v in globals().items() if k.startswith("compute_")}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
