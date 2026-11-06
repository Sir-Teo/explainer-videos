"""Precompute everything numerical in Part 48 of *Computer Science, Built* ("System Design I: Building Blocks").

    python -m videos.cs.cs48.compute              # everything missing
    python -m videos.cs.cs48.compute --force caches

Results are cached in ``.cache/cs48/<name>.json``; scenes call ``load(name)``.  The instruments are
``explainer/cs/design/`` (blocks, keys) and, for balancing, ``explainer/cs/api/services.py``; tests in
tests/test_cs48_design.py.

Items:
    napkin      an estimation worksheet: daily users to peak queries per second, writes, storage, bandwidth
    balance     random, round robin, two choices and least loaded over 50 servers (from Part 43's instrument)
    maglev      Maglev against a hash ring: keys moved needlessly when a backend leaves, and load spread
    caches      LRU, LFU and W-TinyLFU hit rates on Zipf traffic against Che's approximation and the static optimum
    scan        a one-off scan through the cache: LRU against TinyLFU
    stampede    a hot key expiring: rebuilds without protection against probabilistic early expiration
    limiter     a token bucket's envelope; fixed windows admitting bursts; the sliding-window counter's error
    birthday    UUIDv4 collision probabilities
    ids         Snowflake, UUIDv7 and UUIDv4 examples
    btree       random against time-ordered keys in a B+ tree: fill, splits, pages touched
    curves      Z-order and Hilbert curves on an 8x8 grid; locality and ranges per query rectangle
    geohash     two cities' geohashes
    jobsvc      the Job as a service: p50 and p99 against load, with and without a cache
"""

from __future__ import annotations

from explainer.ai.cache import Cache

CACHE = Cache("cs48")
load = CACHE.load


def compute_napkin() -> dict:
    from explainer.cs.design import keys as K
    return K.napkin()


def compute_balance() -> dict:
    from explainer.cs.api import services
    return services.balancing()


def compute_maglev() -> dict:
    from explainer.cs.design import blocks as B
    r = B.disruption()
    r["slots_per_backend"] = {k: int(v) for k, v in r["slots_per_backend"].items()}
    return r


def compute_caches() -> dict:
    from explainer.cs.design import blocks as B
    return B.cache_experiment(n=400_000)


def compute_scan() -> dict:
    from explainer.cs.design import blocks as B
    return B.scan_resistance()


def compute_stampede() -> dict:
    from explainer.cs.design import blocks as B
    return {"plain": B.stampede(), "early": B.stampede(early=True)}


def compute_limiter() -> dict:
    from explainer.cs.design import blocks as B
    return B.limiter_experiment()


def compute_birthday() -> dict:
    from explainer.cs.design import keys as K
    return {"rows": K.birthday()}


def compute_ids() -> dict:
    from explainer.cs.design import keys as K
    return K.id_examples()


def compute_btree() -> dict:
    from explainer.cs.design import keys as K
    return {"random": K.btree_inserts(), "ordered": K.btree_inserts(ordered=True)}


def compute_curves() -> dict:
    from explainer.cs.design import keys as K
    return {"order3": K.curve_points(3), "locality": K.locality()}


def compute_geohash() -> dict:
    from explainer.cs.design import keys as K
    return {"london": K.geohash(51.5072, -0.1276), "new_york": K.geohash(40.7128, -74.0060),
            "london_prefixes": [K.geohash(51.5072, -0.1276, c) for c in range(1, 8)]}


def compute_jobsvc() -> dict:
    from explainer.cs.design import keys as K
    return {"plain": K.job_service(), "cached": K.job_service(cache_size=300,
                                                                qps_list=(5, 20, 60, 95, 150, 200, 250))}


ITEMS = {k[8:]: v for k, v in globals().items() if k.startswith("compute_")}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
