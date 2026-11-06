"""Precompute everything numerical in Part 45 of *Computer Science, Built* ("The Cloud").

    python -m videos.cs.cs45.compute              # everything missing
    python -m videos.cs.cs45.compute --force job

Results are cached in ``.cache/cs45/<name>.json``; scenes call ``load(name)``.  The instruments are
``explainer/cs/cloud/`` (packing, control, durability, cost); tests in tests/test_cs45_cloud.py.

Items:
    packing     next fit, first fit, best fit and FFD against the exact optimum on random small instances
    nextfit     the family on which next fit uses nearly twice the optimum
    vector      containers packed by CPU and memory together against by CPU alone
    partition   partition reduced to bin packing
    reconcile   level- against edge-triggered reconciliation with lost events
    autoscale   a proportional autoscaler with delay: settling, oscillating, saturating
    erlang      Erlang C: servers needed for a target wait, and utilization's economy of scale
    plan        an infrastructure plan: create, update, destroy, in dependency order
    durability  mean time to data loss for replication against erasure codes; a Monte Carlo check
    correlated  whole-rack failures against independent fragment failures
    serverless  Lambda against a server per month at steady load; the break-even rate
    spot        a ten-hour batch job on spot capacity, with and without checkpoints
    job         the Job's measured time, and its bill three ways; ledger row 16
"""

from __future__ import annotations

import json

from explainer.ai.cache import Cache

CACHE = Cache("cs45")
load = CACHE.load


def compute_packing() -> dict:
    from explainer.cs.cloud import packing as P
    return {"uniform": P.compare(n=20, trials=200), "structured": P.compare(n=20, trials=100, dist="structured")}


def compute_nextfit() -> dict:
    from explainer.cs.cloud import packing as P
    return {"rows": [P.next_fit_bad(k) for k in (4, 8, 12, 40, 200)]}


def compute_vector() -> dict:
    from explainer.cs.cloud import packing as P
    return P.vector_pack()


def compute_partition() -> dict:
    from explainer.cs.cloud import packing as P
    return {"yes": P.partition_reduction((3, 1, 1, 2, 2, 1)), "no": P.partition_reduction((3, 3, 3, 1))}


def compute_reconcile() -> dict:
    from explainer.cs.cloud import control as C
    return C.reconcile()


def compute_autoscale() -> dict:
    from explainer.cs.cloud import control as C
    return {f"{g}-{d}": C.autoscale(g, d) for g, d in ((0.2, 3), (0.5, 3), (1.0, 3), (0.3, 1))}


def compute_erlang() -> dict:
    from explainer.cs.cloud import control as C
    return {"rows": C.erlang_table(), "check": C.erlang_c(2, 1.0)}


def compute_plan() -> dict:
    from explainer.cs.cloud import control as C
    return C.plan_example()


def compute_durability() -> dict:
    from explainer.cs.cloud import durability as D
    return {"schemes": D.schemes(), "check": [D.simulate(), D.simulate(n=6, k=4)]}


def compute_correlated() -> dict:
    from explainer.cs.cloud import durability as D
    return D.correlated()


def compute_serverless() -> dict:
    from explainer.cs.cloud import cost as C
    return {**C.serverless_vs_server(), "prices": C.PRICES}


def compute_spot() -> dict:
    from explainer.cs.cloud import cost as C
    return C.spot()


def compute_job() -> dict:
    """Time the Job (count the words of thirty novels, top twenty) on one core of this machine, median of three,
    and price it; append ledger row 16."""
    import statistics
    import time
    from collections import Counter
    from explainer.cs.cloud import cost as C
    from videos.cs.cs31.compute import _full_text
    text = _full_text()
    ts = []
    for _ in range(3):
        t0 = time.perf_counter()
        top = Counter(text.decode("latin-1").lower().split()).most_common(20)
        ts.append(time.perf_counter() - t0)
    sec = statistics.median(ts)
    bill = C.job_bill(sec)
    led = json.loads((Cache("cs39").dir / "ledger.json").read_text())
    led = [r for r in led if r["part"] != 45]
    led.append({"part": 45, "label": r"16 functions in the cloud, \ about \$" + f"{bill['lambda']:.5f}",
                "seconds": bill["lambda_wall_seconds"], "dollars": bill["lambda"], "workers": 16})
    CACHE.dir.mkdir(parents=True, exist_ok=True)
    (CACHE.dir / "ledger.json").write_text(json.dumps(led, indent=1))
    return {"seconds": sec, "bytes": len(text), "top": top[:5], "bill": bill, "ledger": led, "prices": C.PRICES}


ITEMS = {k[8:]: v for k, v in globals().items() if k.startswith("compute_")}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
