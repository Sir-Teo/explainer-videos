"""Precompute everything numerical in Part 39 of *Computer Science, Built* ("Distributed Systems II: Scale").

    python -m videos.cs.cs39.compute              # everything missing
    python -m videos.cs.cs39.compute --force job

Results are cached in ``.cache/cs39/<name>.json``; scenes call ``load(name)``.  The instruments are
``explainer/cs/dist/`` (scale, mapreduce); tests in tests/test_cs39_scale.py.

Items:
    latency     latency numbers every programmer should know, rescaled so that one CPU cycle is one second
    lag         asynchronous replication: read-your-writes violations against time since the write
    quorum      probabilistically bounded staleness for N, R, W configurations, against time since the write
    cap         a partition: what CP and AP each give up, counted
    crdt        convergence of four CRDTs, and of a naive set, under random gossip orders
    hashing     load on a consistent-hash ring against virtual nodes; keys moved when a node joins
    chord       Chord's lookup hops against the number of nodes
    txn         two-phase commit blocking behind a crashed coordinator; Spanner's commit wait for three epsilons
    job         the Job as MapReduce on sixteen Pebbles: plain, a crash, a straggler with and without backup
                tasks; scaling with the number of workers; ledger row 15
    tail        fan-out against tail latency; hedged requests; the power of two choices
    meta        a metastable failure: a ten-second spike, and retries that keep the server down
    lww         two leaders writing one key: concurrent writes and clock-skew inversions under last-writer-wins
    merkle      anti-entropy between two replicas of a million keys: Merkle-tree bytes against one hash per key
    rga         a sequence CRDT (RGA) against positional replay: a two-person edit, and random editing sessions
    hot         hot keys on 100 hash shards under Zipf popularity, and with the hottest keys salted
    balance     load balancing as queueing: random, round robin, two choices, shortest queue against load
    nines       availability in series and in parallel; replicas in one rack against three racks
    detect      failure detection: false suspicions against detection time, fixed timeouts and phi accrual
    hlc         physical, Lamport and hybrid logical clocks on four skewed processes: causality and drift
    history     an Elle-style check of 2,000 list-append transactions, serializable and on a stale replica
    chain       tails through a chain of services; retry amplification through layers
    overhead    an RGA document after 20,000 edits: tombstones and metadata bytes per visible character
"""

from __future__ import annotations

import json
import statistics

from explainer.ai.cache import Cache

CACHE = Cache("cs39")
load = CACHE.load


def compute_latency() -> dict:
    # cited orders of magnitude (Dean; Norvig; updated figures as commonly quoted, 2020s hardware)
    rows = [("CPU cycle (3 GHz)", 0.33e-9), ("L1 cache hit", 1e-9), ("L2 cache hit", 4e-9),
            ("main memory", 100e-9), ("1 KB over 10 Gb/s", 1e-6), ("SSD random read", 100e-6),
            ("round trip in a datacenter", 500e-6), ("disk seek", 10e-3), ("California to Europe and back", 150e-3),
            ("TCP retransmission timeout", 1.0)]
    cyc = rows[0][1]
    out = [{"name": n, "seconds": s, "scaled_s": s / cyc} for n, s in rows]
    return {"rows": out}


def compute_lag() -> dict:
    from explainer.cs.dist import scale as S
    return {"rows": S.replication_lag(), "lag_ms": 100, "followers": 2}


def compute_quorum() -> dict:
    from explainer.cs.dist import scale as S
    rows = []
    for N, R, W in ((3, 1, 1), (3, 1, 2), (3, 2, 1), (3, 2, 2), (3, 1, 3), (5, 1, 1), (5, 2, 2), (5, 3, 3)):
        rows.append({"N": N, "R": R, "W": W, "strict": R + W > N,
                     "stale": [S.pbs(N, R, W, t, 20000, seed=N * 100 + R * 10 + W) for t in (0, 5, 20, 50)]})
    return {"rows": rows, "ts": [0, 5, 20, 50], "w_mean": 10, "r_mean": 10}


def compute_cap() -> dict:
    from explainer.cs.dist import scale as S
    return S.cap()


def compute_crdt() -> dict:
    from explainer.cs.dist import scale as S
    rows = [S.crdt_converge(k, replicas=4, ops=40, trials=1000, seed=7) for k in S.KINDS]
    # a worked G-counter: three replicas
    a, b, c = S.GCounter(3, 0), S.GCounter(3, 1), S.GCounter(3, 2)
    steps = []
    a.inc(2)
    b.inc(1)
    steps.append(["A +2, B +1", a.state(), b.state(), c.state()])
    c.merge(a)
    steps.append(["C merges A", a.state(), b.state(), c.state()])
    a.merge(b)
    steps.append(["A merges B", a.state(), b.state(), c.state()])
    b.merge(c)
    c.merge(a)
    b.merge(c)
    steps.append(["gossip until quiet", a.state(), b.state(), c.state()])
    return {"rows": rows, "gcounter": steps, "value": a.value()}


def compute_hashing() -> dict:
    from explainer.cs.dist import scale as S
    loads = [S.ring_load(10, v, 100000) for v in (1, 4, 16, 64, 256)]
    moved = S.moved_fraction(10, keys=50000)
    return {"loads": loads, "moved": moved}


def compute_chord() -> dict:
    from explainer.cs.dist import scale as S
    return {"rows": [S.chord_hops(n, 2000) for n in (16, 64, 256, 1024, 4096, 16384)]}


def compute_txn() -> dict:
    from explainer.cs.dist import scale as S
    return {"two_pc": S.two_pc(), "spanner": [S.spanner(e) for e in (1.0, 4.0, 7.0)]}


def compute_job() -> dict:
    from explainer.cs.dist.mapreduce import run_job
    from explainer.cs.pebble import programs as PR
    from videos.cs.cs31.compute import _full_text
    text = _full_text()
    ref = [(ln.split()[0], int(ln.split()[1])) for ln in PR.job_reference(text).decode().splitlines()]
    runs = {}
    for name, kw in (("plain", {}), ("crash", {"crash": (3, 0.4)}), ("straggler", {"slow": {5: 8.0}}),
                     ("straggler, no backups", {"slow": {5: 8.0}, "backup": False}),
                     ("crash and straggler", {"crash": (3, 0.4), "slow": {5: 8.0}})):
        r = run_job(text, workers=16, maps=48, reduces=16, **kw)
        r["correct"] = [tuple(x) for x in r["top"]] == [tuple(x) for x in ref]
        runs[name] = r
    scaling = []
    for w in (1, 2, 4, 8, 16, 32, 64):
        r = run_job(text, workers=w, maps=max(4 * w, 16), reduces=min(16, max(1, w)), backup=True)
        scaling.append({"workers": w, "seconds": r["time"]})
    led = json.loads((Cache("cs37").dir / "ledger.json").read_text())
    led = [r for r in led if r["part"] != 39]
    cr = runs["crash"]
    led.append({"part": 39, "label": r"MapReduce, \ 16 Pebbles, \ one crashes", "seconds": cr["time"],
                "workers": 16, "reexecuted": cr["reexecuted"], "backups": cr["backups"]})
    CACHE.dir.mkdir(parents=True, exist_ok=True)
    (CACHE.dir / "ledger.json").write_text(json.dumps(led, indent=1))
    slim = {k: {kk: vv for kk, vv in v.items() if kk != "timeline"} | {"timeline": v["timeline"]}
            for k, v in runs.items()}
    return {"runs": slim, "scaling": scaling, "ledger": led, "reference": ref, "bytes": len(text)}


def compute_tail() -> dict:
    from explainer.cs.dist import scale as S
    plain = S.tail(fanouts=(1, 10, 100, 1000), trials=200000)
    hedged = S.tail(fanouts=(1, 10, 100, 1000), trials=200000, hedge_at=30)
    choices = {d: S.two_choices(1000, d=d, trials=30) for d in (1, 2, 3)}
    return {"plain": plain, "hedged": hedged, "two_choices": choices, "p_slow": 0.01, "fast_ms": 10,
            "slow_ms": 1000, "hedge_ms": 30}


def compute_meta() -> dict:
    from explainer.cs.dist import scale as S
    out = {}
    for name, kw in (("no retries", {"retries": 0}), ("retries", {"retries": 3}),
                     ("retries, backoff", {"retries": 3, "backoff": True}),
                     ("retries, drop expired", {"retries": 3, "drop_expired": True})):
        r = S.metastable(**kw)
        r["after"] = statistics.mean(r["goodput"][60:])
        out[name] = r
    return out


def compute_lww() -> dict:
    from explainer.cs.dist import replicas as RP
    return {"rows": RP.lww_pairs(), "delta_ms": 50, "rate": 5}


def compute_merkle() -> dict:
    from explainer.cs.dist import replicas as RP
    return RP.merkle_sync()


def compute_rga() -> dict:
    from explainer.cs.dist import replicas as RP
    sess = {k: sum(RP.edit_session(k, seed=s)["converged"] for s in range(500)) for k in ("rga", "naive")}
    return {"demo": RP.rga_demo(), "sessions": sess, "trials": 500, "users": 3, "ops": 30}


def compute_hot() -> dict:
    from explainer.cs.dist import replicas as RP
    return RP.hot_shards()


def compute_balance() -> dict:
    from explainer.cs.dist import service as SV
    return {"rows": SV.balance_table(jobs=200_000), "servers": 100}


def compute_nines() -> dict:
    from explainer.cs.dist import service as SV
    return SV.availability()


def compute_detect() -> dict:
    from explainer.cs.dist import service as SV
    return SV.detector(timeouts_ms=(130, 150, 175, 200, 300, 500, 1000, 2000, 3000),
                       phis=(1, 2, 3, 4, 6, 8, 12, 16), window=300)


def compute_hlc() -> dict:
    from explainer.cs.dist import clocks as CL
    return CL.hlc_trace()


def compute_history() -> dict:
    from explainer.cs.dist import history as HI
    out = HI.campaign()
    for v in out.values():
        for e in v["example"] or []:
            e["ops"] = [[op[0], op[1], list(op[2])[-3:]] if op[0] == "r" else list(op) for op in e["ops"]]
    return out


def compute_chain() -> dict:
    from explainer.cs.dist import service as SV
    return {"chain": SV.call_chain(), "retries": SV.retry_amplification(), "median_ms": 10.0, "sigma": 0.8}


def compute_overhead() -> dict:
    from explainer.cs.dist import replicas as RP
    return {"rows": RP.rga_overhead(p_delete=0.3), "p_delete": 0.3, "id_bytes": 12}


ITEMS = {k[8:]: v for k, v in globals().items() if k.startswith("compute_")}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
