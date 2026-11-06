"""Precompute everything numerical in Part 38 of *Computer Science, Built* ("Distributed Systems I: Agreement").

    python -m videos.cs.cs38.compute              # everything missing
    python -m videos.cs.cs38.compute --force raft

Results are cached in ``.cache/cs38/<name>.json``; scenes call ``load(name)``.  The instruments are
``explainer/cs/dist/`` (clocks, consensus, raft, byzantine); tests in tests/test_cs38_dist.py.

Items:
    hook        five Pebbles running Raft through a storm of crashes, partitions and lost messages: commands
                committed, leaders elected, invariants violated (none), and one run's timeline
    generals    the two generals over a lossy link: messengers needed for a given confidence, and why no number is
                enough
    clocks      a three-process execution stamped with Lamport and vector clocks; causality checked on 200 random
                executions; NTP's offset and its error under asymmetric delay
    snapshot    Chandy-Lamport on a bank of four processes: recorded balances and money in transit, against a naive
                survey
    floodset    synchronous crash consensus: f rounds fail (with a counterexample), f + 1 rounds succeed, checked over
                every crash pattern
    flp         two tiny protocols explored exhaustively: one can disagree, the other can block; valency of every
                initial configuration
    benor       Ben-Or's randomized consensus: the distribution of rounds to decide
    paxos       single-decree Paxos with one to four proposers under loss: attempts, messages, safety
    raft        the fault campaign: correct Raft and three planted bugs, random and targeted fault injection
    election    leader election against the randomization of timeouts: split votes and time to a leader
    byzantine   OM(m) exhaustively: three generals with one traitor fail, four succeed; messages for OM, PBFT and
                HotStuff
    nakamoto    the double-spend probability: Nakamoto's formula, the exact one, simulation; selfish mining
"""

from __future__ import annotations

import random
import statistics

from explainer.ai.cache import Cache

CACHE = Cache("cs38")
load = CACHE.load


def _campaign(bug=None, runs=1000, crash_after_vote=0.0, rate=8, until=6):
    from explainer.cs.dist.raft import Cluster, random_faults
    bad, first, kinds, committed, terms, msgs = 0, None, {}, [], [], []
    for s in range(runs):
        c = Cluster(5, seed=s, loss=0.1, bug=bug, delay=(0.005, 0.08), crash_after_vote=crash_after_vote)
        random_faults(c, until, rate=rate)
        c.run(until=until, client_rate=40)
        sm = c.summary()
        committed.append(sm["committed"])
        terms.append(sm["terms"])
        msgs.append(sm["messages"])
        if c.violations:
            bad += 1
            if first is None:
                first = {"seed": s, "violation": list(c.violations[0][1:]), "time": c.violations[0][0]}
            for v in c.violations:
                kinds[v[1]] = kinds.get(v[1], 0) + 1
    return {"bug": bug, "runs": runs, "violating_runs": bad, "first": first, "kinds": kinds,
            "mean_committed": statistics.mean(committed), "mean_terms": statistics.mean(terms),
            "mean_messages": statistics.mean(msgs), "targeted": crash_after_vote}


def compute_hook() -> dict:
    from explainer.cs.dist.raft import Cluster
    crashed = []
    # a scripted storm: the leader crashes, a partition isolates two nodes, a second crash, healing
    c = Cluster(5, seed=7, loss=0.05, delay=(0.005, 0.03))
    samples = []
    actions = {1.5: ("crash_leader",), 3.0: ("partition", [[0, 1], [2, 3, 4]]), 4.5: ("heal",),
               5.0: ("restart_all",), 6.0: ("crash_leader",), 7.5: ("restart_all",)}
    rng = random.Random(3)
    t = 0.0
    while t < 9.0:
        nt = round(t + 0.05, 3)
        c.run(until=nt, client_rate=0)
        for _ in range(rng.randint(0, 3)):
            c.submit()
        t = nt
        if t in actions:
            a = actions[t]
            if a[0] == "crash_leader":
                for nd in c.nodes:
                    if nd.up and nd.role == "leader":
                        c.crash(nd.id)
                        crashed.append(nd.id)
                        break
            elif a[0] == "restart_all":
                for i in crashed:
                    c.restart(i)
                crashed = []
            elif a[0] == "partition":
                c.partition(a[1])
            elif a[0] == "heal":
                c.heal()
        samples.append([t, [[nd.role if nd.up else "down", nd.term, len(nd.log), nd.commit] for nd in c.nodes]])
    camp = _campaign(None, runs=1000)
    return {"timeline": samples, "events": [[t, k, kw] for t, k, kw in c.history if k in ("leader", "crash", "restart",
                                                                                         "partition", "heal")],
            "violations": len(c.violations), "committed": len(c.committed), "terms": max(nd.term for nd in c.nodes),
            "campaign": camp}


def compute_generals() -> dict:
    rows = []
    for p in (0.1, 0.3, 0.5):
        for target in (0.99, 0.999999):
            k = 1
            while 1 - p ** k < target:
                k += 1
            rows.append({"loss": p, "confidence": target, "messengers": k})
    return {"rows": rows}


def compute_clocks() -> dict:
    from explainer.cs.dist import clocks as C
    tr = C.random_trace(3, 11, seed=4, p_send=0.5)
    out = {"trace": [list(e) for e in tr], "lamport": C.lamport(tr), "vector": [list(v) for v in C.vector(tr)],
           "check": C.check_vector(tr)}
    agg = {"runs": 0, "vector_ok": 0, "lamport_ok": 0, "pairs": 0, "concurrent": 0, "lamport_orders": 0}
    for s in range(200):
        r = C.check_vector(C.random_trace(4, 20, seed=100 + s))
        agg["runs"] += 1
        agg["vector_ok"] += r["vector_characterizes"]
        agg["lamport_ok"] += r["lamport_condition"]
        agg["pairs"] += r["pairs"]
        agg["concurrent"] += r["concurrent"]
        agg["lamport_orders"] += r["lamport_orders_concurrent"]
    out["aggregate"] = agg
    # NTP: true offset 5.000 s, delays 40 ms out and 40 ms back, then 70 ms out and 10 back
    ntp = []
    for d_out, d_back in ((0.04, 0.04), (0.07, 0.01), (0.1, 0.0)):
        t0 = 100.0
        t1 = t0 + 5.0 + d_out
        t2 = t1 + 0.001
        t3 = t2 - 5.0 + d_back
        off, dl = C.ntp(t0, t1, t2, t3)
        ntp.append({"out_ms": d_out * 1000, "back_ms": d_back * 1000, "offset": off, "delay_ms": dl * 1000,
                    "error_ms": (off - 5.0) * 1000})
    out["ntp"] = ntp
    return out


def compute_snapshot() -> dict:
    from explainer.cs.dist import clocks as C
    runs = [C.Bank(4, seed=s).run() for s in range(50)]
    demo = runs[2]
    return {"demo": demo, "consistent": sum(r["consistent"] for r in runs), "runs": len(runs),
            "survey_wrong": sum(r["survey_total"] != r["total"] for r in runs),
            "survey_range": [min(r["survey_total"] for r in runs), max(r["survey_total"] for r in runs)]}


def compute_floodset() -> dict:
    from explainer.cs.dist import consensus as K
    rows = []
    for n, f in ((3, 1), (4, 1), (4, 2), (5, 2)):
        for rounds in (f, f + 1):
            r = K.floodset(n, f, rounds)
            rows.append({"n": n, "f": f, "rounds": rounds, "patterns": r["patterns"], "checked": r["checked"],
                         "agreement": r["agreement"], "counterexample": r["counterexample"]})
    return {"rows": rows}


def compute_flp() -> dict:
    from explainer.cs.dist import consensus as K
    return {p: K.flp_table(p) for p in ("wait-n-f", "wait-all")}


def compute_benor() -> dict:
    from explainer.cs.dist import consensus as K
    out = {}
    for label, inputs in (("split", [0, 1, 0, 1, 1]), ("random", None)):
        rs = [K.ben_or(5, 2, inputs=inputs, seed=s)["rounds"] for s in range(2000)]
        hist = {}
        for r in rs:
            hist[r] = hist.get(r, 0) + 1
        out[label] = {"mean": statistics.mean(rs), "max": max(rs), "hist": sorted(hist.items()),
                      "p_le_5": sum(1 for r in rs if r <= 5) / len(rs)}
    return out


def compute_paxos() -> dict:
    from explainer.cs.dist import consensus as K
    rows = []
    for P in (1, 2, 3, 4):
        for bo in (True, False):
            res = [K.paxos(5, P, loss=0.05, seed=s, backoff=bo, until=5, retry=0.035, delay=(0.005, 0.015))
                   for s in range(400)]
            rows.append({"proposers": P, "backoff": bo, "safe": all(r["safe"] for r in res),
                         "decided": sum(1 for r in res if r["chosen"]), "runs": len(res),
                         "attempts": statistics.mean(r["attempts"] for r in res),
                         "messages": statistics.mean(r["messages"] for r in res),
                         "time_ms": statistics.mean([r["first"] for r in res if r["first"] is not None] or [0]) * 1000})
    return {"rows": rows, "retry_ms": 35, "rtt_ms": [10, 30]}


def compute_raft() -> dict:
    out = {"correct": _campaign(None, 1000)}
    for bug in ("commit-old-term", "no-log-check", "forget-vote"):
        out[bug] = _campaign(bug, 1000)
    out["forget-vote targeted"] = _campaign("forget-vote", 1000, crash_after_vote=0.3)
    out["correct targeted"] = _campaign(None, 1000, crash_after_vote=0.3)
    return out


def compute_election() -> dict:
    from explainer.cs.dist.raft import Cluster
    rows = []
    for sp in (0.0, 0.02, 0.1, 0.5, 1.0):
        times, terms, never = [], [], 0
        for s in range(300):
            c = Cluster(5, seed=s, spread=sp, delay=(0.002, 0.012))
            c.run(until=1.0, client_rate=0)
            lead = [nd.id for nd in c.nodes if nd.role == "leader"]
            if not lead:
                never += 1
                continue
            term0 = max(nd.term for nd in c.nodes)
            c.crash(lead[0])
            c.run(until=6.0, client_rate=0)
            new = [(t, kw) for t, k, kw in c.history if k == "leader" and t > 1.0]
            if not new:
                never += 1
                continue
            times.append(new[0][0] - 1.0)
            terms.append(new[0][1]["term"] - term0)
        rows.append({"spread": sp, "runs": 300, "no_leader": never,
                     "median_ms": statistics.median(times) * 1000 if times else None,
                     "p99_ms": sorted(times)[int(0.99 * len(times))] * 1000 if times else None,
                     "mean_terms": statistics.mean(terms) if terms else None})
    return {"rows": rows, "timeout_ms": 150}


def compute_byzantine() -> dict:
    from explainer.cs.dist import byzantine as B
    cases = [(3, 1, {1}), (3, 1, {0}), (4, 1, {0}), (4, 1, {2}), (4, 1, {1, 2}), (7, 2, {0, 3}), (7, 2, {2, 5})]
    rows = []
    for n, m, tr in cases:
        r = B.om_exhaustive(n, m, tr)
        rows.append({"n": n, "m": m, "traitors": sorted(tr), "strategies": r["strategies"], "slots": r["slots"],
                     "agree": r["always_agree"], "counterexample": r["counterexample"]})
    msgs = [{"n": n, "f": (n - 1) // 3, "om": B.bft_messages(n, "om"), "pbft": B.bft_messages(n, "pbft"),
             "hotstuff": B.bft_messages(n, "hotstuff")} for n in (4, 7, 10, 31, 100)]
    for m in msgs:
        m["om"] = str(m["om"]) if m["om"] > 10 ** 15 else m["om"]
    return {"rows": rows, "messages": msgs}


def compute_nakamoto() -> dict:
    from explainer.cs.dist import byzantine as B
    rows = []
    for q in (0.1, 0.3):
        for z in (1, 2, 4, 6, 10):
            rows.append({"q": q, "z": z, "nakamoto": B.nakamoto_p(q, z), "exact": B.rosenfeld(q, z),
                         "simulated": B.double_spend_mc(q, z, 200000, seed=z)})
    need = {}
    for q in (0.1, 0.2, 0.3, 0.4):
        z = 0
        while B.rosenfeld(q, z) > 0.001 and z < 200:
            z += 1
        need[q] = z
    sm = [B.selfish(a / 100, g, blocks=200000, seed=a) for g in (0.0, 0.5) for a in range(5, 50, 5)]
    return {"rows": rows, "need_0.1pct": need, "selfish": sm}


ITEMS = {k[8:]: v for k, v in globals().items() if k.startswith("compute_")}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
