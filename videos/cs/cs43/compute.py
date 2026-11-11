"""Precompute everything numerical in Part 43 of *Computer Science, Built* ("APIs and Services").

    python -m videos.cs.cs43.compute              # everything missing
    python -m videos.cs.cs43.compute --force job

Results are cached in ``.cache/cs43/<name>.json``; scenes call ``load(name)``.  The instruments are
``explainer/cs/api/`` (wire, delivery, services); tests in tests/test_cs43_api.py.

Items:
    published   our varint, zigzag and message encoder against the encoding documentation's examples
    sizes       bytes per varint; negative numbers with and without zigzag
    compare     one record as JSON and as protobuf
    doubles     JSON integers past 2^53
    evolution   seven schema changes: backward and forward compatible or not
    semantics   at most, at least and exactly once on a lossy, duplicating network
    modelcheck  every execution of retry-until-acknowledged, with and without deduplication, explored
    job         the Job as three services: counts with and without idempotency keys, over loss and duplication
    pagination  offset against cursor paging under concurrent inserts, over insert rates
    storm       a ten-second outage: immediate retries, backoff with jitter, a retry budget
    outbox      commit-then-publish, publish-then-commit and the transactional outbox under crashes
    saga        an order saga: outcomes, compensations and the consistency invariant
    fanout      latency of a fan-out to 1-100 back ends: medians and tails
    budget      a deadline propagated down a call chain
    queue       an M/M/1 queue in front of a service, unbounded and bounded
    nplus1      GraphQL's N + 1 queries and batching
    visibility  visibility timeouts and dead-letter queues
    jwt         JWT verification with and without a pinned algorithm
    balance     client-side load balancing: random, round robin, two choices, least loaded
    time        clocks: a daylight-saving gap, half-hour zones, leap seconds, 2038
"""

from __future__ import annotations

from explainer.ai.cache import Cache

CACHE = Cache("cs43")
load = CACHE.load


def _novels():
    from videos.cs.cs31.compute import _full_text
    return _full_text().decode("latin-1")


def compute_published() -> dict:
    from explainer.cs.api import wire
    return wire.check_published()


def compute_sizes() -> dict:
    from explainer.cs.api import wire
    return wire.varint_sizes()


def compute_compare() -> dict:
    from explainer.cs.api import wire
    return wire.size_comparison()


def compute_doubles() -> dict:
    from explainer.cs.api import wire
    return wire.json_doubles()


def compute_evolution() -> dict:
    from explainer.cs.api import wire
    return {"cases": wire.evolution_cases()}


def compute_semantics() -> dict:
    from explainer.cs.api import delivery
    return delivery.semantics(10_000, 0.05, 0.02)


def compute_modelcheck() -> dict:
    from explainer.cs.api import delivery
    return {"dedup": delivery.model_check(True), "plain": delivery.model_check(False),
            "dedup3": delivery.model_check(True, n_msgs=3, retries=1),
            "growth": [{"messages": n, "states": delivery.model_check(True, n_msgs=n, retries=1)["states"]}
                       for n in (1, 2, 3, 4)]}


def compute_job() -> dict:
    from explainer.cs.api import delivery
    text = _novels()[:400_000]
    base = {d: delivery.job_services(text, dedup=d) for d in (True, False)}
    sweep = []
    for loss, dup in ((0.0, 0.0), (0.01, 0.01), (0.05, 0.02), (0.1, 0.05), (0.2, 0.1)):
        a = delivery.job_services(text, loss=loss, dup=dup, dedup=True)
        b = delivery.job_services(text, loss=loss, dup=dup, dedup=False)
        sweep.append({"loss": loss, "dup": dup, "with_keys_wrong": a["wrong_counts"], "with_keys_over": a["overcount"],
                      "without_wrong": b["wrong_counts"], "without_over": b["overcount"],
                      "messages": a["messages"]})
    return {"with_keys": base[True], "without": base[False], "sweep": sweep}


def compute_pagination() -> dict:
    from explainer.cs.api import delivery
    rows = [delivery.pagination(1000, 50, k) for k in (0, 1, 3, 10)]
    return {"rows": rows}


def compute_storm() -> dict:
    from explainer.cs.api import delivery
    return {p: delivery.retry_storm(policy=p) for p in ("immediate", "backoff", "budget")}


def compute_outbox() -> dict:
    from explainer.cs.api import services
    return services.dual_write()


def compute_saga() -> dict:
    from explainer.cs.api import services
    return services.saga_experiment()


def compute_fanout() -> dict:
    from explainer.cs.api import services
    return services.call_graph()


def compute_budget() -> dict:
    from explainer.cs.api import services
    return services.budget()


def compute_queue() -> dict:
    from explainer.cs.api import services
    return {"unbounded": services.queueing(), "bounded": services.queueing(bound=20)}


def compute_nplus1() -> dict:
    from explainer.cs.api import services
    return services.n_plus_one()


def compute_visibility() -> dict:
    from explainer.cs.api import services
    return services.visibility()


def compute_jwt() -> dict:
    from explainer.cs.api import services
    return services.jwt_demo()


def compute_time() -> dict:
    from explainer.cs.api import services
    return services.time_pitfalls()


def compute_balance() -> dict:
    from explainer.cs.api import services
    return services.balancing()


ITEMS = {k[8:]: v for k, v in globals().items() if k.startswith("compute_")}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
