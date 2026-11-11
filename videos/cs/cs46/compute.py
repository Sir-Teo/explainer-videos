"""Precompute everything numerical in Part 46 of *Computer Science, Built* ("Logs, Streams and Warehouses").

    python -m videos.cs.cs46.compute              # everything missing
    python -m videos.cs.cs46.compute --force job

Results are cached in ``.cache/cs46/<name>.json``; scenes call ``load(name)``.  The instruments are
``explainer/cs/data/`` (log, stream, columnar); tests in tests/test_cs46_data.py.

Items:
    rebalance   consumer-group assignments of 12 partitions as members join and leave: range against sticky
    ordering    per-key order in a partitioned log
    compaction  2,000 updates to 50 keys compacted to 50 records, rebuilding the same state
    plot        a small stream for the event-time / processing-time plot, with its watermark
    watermark   completeness against latency for watermark lags from 0 to 60 s; with allowed lateness
    windows     tumbling, sliding and session windows for a few events
    checkpoint  a crash and recovery from an asynchronous barrier snapshot: exact, and the naive overcount
    encodings   one column of the novels' words: plain, dictionary, bit-packed, run-length (sorted), gzip
    ints        a timestamp column: plain against delta
    pushdown    row groups skipped by min/max statistics on a sorted and a random column
    dremel      repetition and definition levels for a nested column, and the column rebuilt from them
    joins       broadcast against shuffle hash join, bytes moved; the crossover
    skew        a hot key overloading one worker, and salting
    quantiles   a KLL sketch's p50, p99 and p99.9 of 200,000 latencies, at three sizes, against exact
    commits     optimistic commits to a lakehouse table: retries against writers, conflicting and disjoint
    job         the Job as a stream of thirty novels, some late and two duplicated: exact, no dedup, early cut;
                ledger row 17
"""

from __future__ import annotations

import json

from explainer.ai.cache import Cache

CACHE = Cache("cs46")
load = CACHE.load


def _words():
    from videos.cs.cs31.compute import _full_text
    return _full_text().decode("latin-1").lower().split()


def compute_rebalance() -> dict:
    from explainer.cs.data import log as L
    return L.rebalance_demo()


def compute_ordering() -> dict:
    from explainer.cs.data import log as L
    return L.ordering_demo("the whale and the sea and the ship and the whale".split())


def compute_compaction() -> dict:
    from explainer.cs.data import log as L
    return L.compaction_demo()


def compute_plot() -> dict:
    from explainer.cs.data import stream as S
    return S.plot_points()


def compute_watermark() -> dict:
    from explainer.cs.data import stream as S
    ev = S.make_events()
    rows = [S.run_windows(ev, watermark_lag=lg) for lg in (0.0, 1.0, 2.0, 5.0, 10.0, 20.0, 60.0)]
    late = S.run_windows(ev, watermark_lag=5.0, allowed_late=60.0)
    return {"rows": rows, "allowed_lateness": late, "events": len(ev)}


def compute_windows() -> dict:
    from explainer.cs.data import stream as S
    ts = [1.0, 2.5, 3.2, 9.0, 9.5, 17.0, 23.0, 24.0]
    return {"times": ts, "tumbling": [S.tumbling(t, 10)[0] for t in ts],
            "sliding": [S.sliding(t, 10, 5) for t in ts], "sessions": S.sessions(ts, 4.0)}


def compute_checkpoint() -> dict:
    from explainer.cs.data import stream as S
    return S.barrier_snapshot(S.make_events())


def compute_encodings() -> dict:
    from explainer.cs.data import columnar as C
    return C.encode_words(_words()[:300_000])


def compute_ints() -> dict:
    from explainer.cs.data import columnar as C
    return C.int_column()


def compute_pushdown() -> dict:
    from explainer.cs.data import columnar as C
    return {"sorted": C.pushdown(), "random": C.pushdown(sorted_=False)}


def compute_dremel() -> dict:
    from explainer.cs.data import columnar as C
    d = C.dremel_example()
    d["rebuilt"] = C.reassemble(d["levels"])
    return d


def compute_joins() -> dict:
    from explainer.cs.data import columnar as C
    return {"rows": [C.join_cost(small_rows=s) for s in (1e4, 1e5, 1e6, 1e7, 1e8)]}


def compute_skew() -> dict:
    from explainer.cs.data import columnar as C
    return C.skew()


def compute_quantiles() -> dict:
    from explainer.cs.data import columnar as C
    return C.quantile_experiment()


def compute_commits() -> dict:
    from explainer.cs.data import columnar as C
    return {"conflicting": C.optimistic_commits(), "disjoint_appends": C.optimistic_commits(disjoint=True)}


def compute_job() -> dict:
    import time
    from explainer.cs.data import stream as S
    from videos.cs.cs31.compute import _full_text
    text = _full_text()
    r = S.job_stream(text)
    t0 = time.perf_counter()
    S.job_stream(text, modes=("exactly once",))
    sec = time.perf_counter() - t0
    led = json.loads((Cache("cs45").dir / "ledger.json").read_text())
    led = [x for x in led if x["part"] != 46]
    led.append({"part": 46, "label": r"a live top twenty over a stream, \ exactly once", "seconds": sec})
    CACHE.dir.mkdir(parents=True, exist_ok=True)
    (CACHE.dir / "ledger.json").write_text(json.dumps(led, indent=1))
    return {**r, "seconds": sec, "ledger": led}


ITEMS = {k[8:]: v for k, v in globals().items() if k.startswith("compute_")}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
