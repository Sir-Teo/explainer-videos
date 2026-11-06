"""Precompute everything numerical in Part 49 of *Computer Science, Built* ("System Design II: Case Studies").

    python -m videos.cs.cs49.compute              # everything missing
    python -m videos.cs.cs49.compute --force abr

Results are cached in ``.cache/cs49/<name>.json``; scenes call ``load(name)``.  The instruments are
``explainer/cs/design/cases.py`` (and Parts 39's and 48's); tests in tests/test_cs49_cases.py.

Items:
    shortener   base62 lengths for 10^6-10^12 links; expected collisions of truncated hashes
    feed        fan-out on write against on read over a power-law follower graph; the hybrid by threshold
    crawler     a billion pages in a month: rates, machines, bandwidth, politeness, a Bloom filter's size
    bloom       a Bloom filter at 9.6 bits per URL: measured false positives against theory
    dispatch    greedy nearest-driver against batched assignment: mean and worst pickup distance
    abr         rate-based, buffer-based and RobustMPC bitrate adaptation on bandwidth traces
    payments    double-entry payments with and without idempotency keys: double charges, the zero-sum invariant
    ot          operational transformation: convergence with and without transformation
    rga         collaborative editing with Part 39's sequence CRDT: convergence across three users
    quorum      Dynamo-style quorums (N, R, W): probability of a stale read (Part 39's PBS model)
    cardinality time-series cardinality as labels are added
    job         the Job at a million books a day: servers, p50 and p99 at the peak, monthly cost; ledger row 18
"""

from __future__ import annotations

import json

from explainer.ai.cache import Cache

CACHE = Cache("cs49")
load = CACHE.load


def compute_shortener() -> dict:
    from explainer.cs.design import cases as C
    return {**C.shortener(), "example": {"n": 10 ** 12, "code": C.base62(10 ** 12)}}


def compute_feed() -> dict:
    from explainer.cs.design import cases as C
    return C.feed_cost()


def compute_crawler() -> dict:
    from explainer.cs.design import cases as C
    return C.crawler()


def compute_bloom() -> dict:
    from explainer.cs.design import cases as C
    return C.bloom_check()


def compute_dispatch() -> dict:
    from explainer.cs.design import cases as C
    return C.dispatch()


def compute_abr() -> dict:
    from explainer.cs.design import cases as C
    return C.abr_experiment()


def compute_payments() -> dict:
    from explainer.cs.design import cases as C
    return {"idempotent": C.ledger(), "naive": C.ledger(idempotent=False)}


def compute_ot() -> dict:
    from explainer.cs.design import cases as C
    return C.ot_experiment()


def compute_rga() -> dict:
    from explainer.cs.dist import replicas as R
    out = {}
    for kind in ("rga", "naive"):
        rs = [R.edit_session(kind, users=3, ops=30, seed=s) for s in range(50)]
        out[kind] = {"converged": sum(1 for r in rs if r.get("converged")) / len(rs), "example": rs[0]}
    return out


def compute_quorum() -> dict:
    from explainer.cs.dist import scale as S
    rows = []
    for N, R, W in ((3, 1, 1), (3, 1, 2), (3, 2, 2), (3, 1, 3), (5, 2, 2), (5, 3, 3)):
        rows.append({"N": N, "R": R, "W": W, "overlap": R + W > N,
                     "stale_now": S.pbs(N=N, R=R, W=W, t=0.0), "stale_after_10ms": S.pbs(N=N, R=R, W=W, t=10.0)})
    return {"rows": rows}


def compute_cardinality() -> dict:
    from explainer.cs.design import cases as C
    return C.cardinality()


def compute_job() -> dict:
    from explainer.cs.design import cases as C
    r = C.job_million()
    led = json.loads((Cache("cs46").dir / "ledger.json").read_text())
    led = [x for x in led if x["part"] != 49]
    # the thirty novels as thirty parallel requests: the slowest of thirty exponential jobs of mean 80 ms
    thirty = 0.08 * sum(1 / k for k in range(1, 31))
    led.append({"part": 49, "label": r"the service, \ thirty books in parallel",
                "seconds": thirty, "dollars": 30 * r["dollars_per_book"], "workers": r["servers"]})
    CACHE.dir.mkdir(parents=True, exist_ok=True)
    (CACHE.dir / "ledger.json").write_text(json.dumps(led, indent=1))
    return {**r, "ledger": led}


ITEMS = {k[8:]: v for k, v in globals().items() if k.startswith("compute_")}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
