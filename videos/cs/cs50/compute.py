"""Precompute everything numerical in Part 50 of *Computer Science, Built* ("Keeping It Running").

    python -m videos.cs.cs50.compute              # everything missing
    python -m videos.cs.cs50.compute --force overload

Results are cached in ``.cache/cs50/<name>.json``; scenes call ``load(name)``.  The instruments are in
``explainer/cs/ops/`` (reliability, slo, overload, observe, profile, chaos); tests in tests/test_cs50_ops.py.

Items:
    nines       allowed downtime per year, month and week at two to five nines
    compose     series and parallel laws; a request path as a circuit, replicated against single components
    renewal     A = MTBF / (MTBF + MTTR) checked by simulation; repair as the cheaper lever
    common      common-mode failures: three replicas when a share of downtime is shared
    groups      a Raft majority's availability; N + k capacity
    slo         a synthetic month: incidents, the budget draining, five alerting rules scored; burn thresholds
    jitter      backoff on a contended resource: no backoff, exponential, full, equal and decorrelated jitter
    overload    a metastable failure and six client and server policies against it
    trigger     which triggers tip the retrying system into its bad state
    bulkhead    one shared thread pool against two, when one dependency turns slow
    hedging     hedged requests: tail latency against extra load
    sketches    DDSketch, a log-linear (HDR-style) histogram, KLL and a sample against the true quantiles
    averages    the mean, the median, the mean of per-server p99s and the fleet's p99
    trace       a synthetic distributed trace and its critical path
    sampling    head against tail sampling: errors and slow traces kept
    omission    coordinated omission: a closed-loop load generator against the true latencies
    openclosed  open against closed load at the same throughput
    changepoint a 3% regression in noisy benchmarks: naive alerts against change-point detection
    profile     a sampling profile of the Job on the Pebble emulator (guest), checked against exact counts
    host        a timer-signal profile of the emulator's own Python (host)
    capacity    capacity plans for the Job service by Erlang C at growing load
    chaos       the Job service under a crash, a partition and a slow replica, three client configurations
    raft        Part 38's Raft cluster under a script of faults
    job         ledger row 19: the thirty books with one slow worker, with and without hedging
"""

from __future__ import annotations

import json

from explainer.ai.cache import Cache

CACHE = Cache("cs50")
load = CACHE.load


def compute_nines() -> dict:
    from explainer.cs.ops import reliability as R
    return {"rows": R.nines_table()}


def compute_compose() -> dict:
    from explainer.cs.ops import reliability as R
    return {"laws": R.series_parallel(), "path": R.request_path()}


def compute_renewal() -> dict:
    from explainer.cs.ops import reliability as R
    return {"sim": R.renewal(), "lever": R.mttr_lever()}


def compute_common() -> dict:
    from explainer.cs.ops import reliability as R
    return {"rows": R.common_mode()}


def compute_groups() -> dict:
    from explainer.cs.ops import reliability as R
    return {"raft": R.raft_table(), "n_plus_k": R.n_plus_k()}


def compute_slo() -> dict:
    from explainer.cs.ops import slo as S
    return S.score()


def compute_jitter() -> dict:
    from explainer.cs.ops import overload as O
    return O.jitter_experiment()


def compute_overload() -> dict:
    from explainer.cs.ops import overload as O
    return O.overload_experiment()


def compute_trigger() -> dict:
    from explainer.cs.ops import overload as O
    return {"rows": O.trigger_sizes()}


def compute_bulkhead() -> dict:
    from explainer.cs.ops import overload as O
    return {"shared": O.bulkhead(False), "bulkheads": O.bulkhead(True)}


def compute_hedging() -> dict:
    from explainer.cs.ops import overload as O
    return {"rows": O.hedging()}


def compute_sketches() -> dict:
    from explainer.cs.ops import observe as O
    return O.sketch_experiment()


def compute_averages() -> dict:
    from explainer.cs.ops import observe as O
    return O.averages_lie()


def compute_trace() -> dict:
    from explainer.cs.ops import observe as O
    return O.example_trace()


def compute_sampling() -> dict:
    from explainer.cs.ops import observe as O
    return O.sampling()


def compute_omission() -> dict:
    from explainer.cs.ops import observe as O
    return O.coordinated_omission()


def compute_openclosed() -> dict:
    from explainer.cs.ops import observe as O
    return {"rows": O.open_closed()}


def compute_changepoint() -> dict:
    from explainer.cs.ops import observe as O
    return O.change_point()


def compute_profile() -> dict:
    from explainer.cs.ops import profile as P
    return P.guest_profile()


def compute_host() -> dict:
    from explainer.cs.ops import profile as P
    return P.host_profile()


def compute_capacity() -> dict:
    """Servers for the Job service (80 ms a book) so that the mean wait stays under 20 ms and at most 20% of
    requests wait at all, as load grows."""
    from explainer.cs.cloud.control import erlang_c, servers_for
    rows = []
    for lam in (12, 35, 100, 300, 1000):
        r = servers_for(lam, 1 / 0.08, 0.02)
        c = r["servers"] if isinstance(r, dict) else r
        rows.append({"per_s": lam, "erlangs": lam * 0.08, "servers": c, "util": lam * 0.08 / c,
                     "p_wait": erlang_c(c, lam * 0.08)})
    return {"rows": rows}


def compute_chaos() -> dict:
    from explainer.cs.ops import chaos as C
    return C.service_experiment()


def compute_raft() -> dict:
    from explainer.cs.ops import chaos as C
    return C.raft_chaos()


def compute_job() -> dict:
    """Thirty books on thirty of the service's 42 workers, one of which is ten times slow.  Without hedging the
    slowest book sets the time; with a hedge after 240 ms (the 95th percentile of an 80 ms exponential) a copy goes
    to a healthy worker."""
    import random
    rng = random.Random(0)
    trials = 20000
    plain, hedged, extra = [], [], 0
    for _ in range(trials):
        workers = rng.sample(range(42), 30)
        ts, hs = [], []
        for w in workers:
            t = rng.expovariate(1 / 0.08) * (10 if w == 0 else 1)
            ts.append(t)
            if t > 0.24:
                extra += 1
                t = min(t, 0.24 + rng.expovariate(1 / 0.08))
            hs.append(t)
        plain.append(max(ts))
        hedged.append(max(hs))
    mean = lambda xs: sum(xs) / len(xs)  # noqa: E731
    led = json.loads((Cache("cs49").dir / "ledger.json").read_text())
    led = [x for x in led if x["part"] != 50]
    prev = led[-1]
    row = {"part": 50, "label": r"one slow worker, \ hedged", "seconds": mean(hedged),
           "unhedged_seconds": mean(plain), "dollars": prev.get("dollars", 0) * (1 + extra / trials / 30),
           "extra_requests": extra / trials}
    led.append(row)
    CACHE.dir.mkdir(parents=True, exist_ok=True)
    (CACHE.dir / "ledger.json").write_text(json.dumps(led, indent=1))
    return {**row, "healthy_seconds": prev["seconds"], "ledger": led}


ITEMS = {k[8:]: v for k, v in globals().items() if k.startswith("compute_")}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
