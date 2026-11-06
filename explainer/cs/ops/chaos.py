"""Chaos experiments (Part 50): faults injected into the Job's counting service and into Part 38's Raft cluster,
with the steady-state hypothesis checked after each.  The service: three replicas behind a client-side balancer;
one replica crashes, one is cut off, one turns slow.  Three client configurations: naive; timeouts and one retry
elsewhere; and timeouts, retries, outlier ejection and hedging."""

from __future__ import annotations

import math
import random

FAULTS = [("crash", 0, 10, 15), ("partition", 1, 25, 30), ("slow", 2, 40, 50)]   # (kind, replica, from, to) minutes
CONFIGS = ("naive", "timeouts and retry", "retry, ejection and hedging")


def _state(rep, minute):
    for kind, r, a, b in FAULTS:
        if r == rep and a <= minute < b:
            return kind
    return "ok"


def service(config: str, minutes: int = 60, rate: float = 20.0, slo_ms: float = 300.0, median_ms: float = 40.0,
            sigma: float = 0.5, slow_x: float = 10.0, seed: int = 0) -> dict:
    """Requests at ``rate`` a second for ``minutes``.  A request is good if it succeeds within ``slo_ms``.
    Returns the share of good requests per minute and overall, and the share of a 99.9% monthly error budget that
    this hour consumed."""
    rng = random.Random(seed)
    mu = math.log(median_ms)
    rr = 0
    errors_in_row = [0, 0, 0]
    ejected_until = [-1.0, -1.0, -1.0]
    good_m = [0] * minutes
    tot_m = [0] * minutes
    extra = 0

    def attempt(rep, t):
        """(outcome, latency in ms) of one try on a replica."""
        st = _state(rep, t / 60)
        if st == "crash":
            return "refused", 1.0
        if st == "partition":
            return "silent", float("inf")
        lat = rng.lognormvariate(mu, sigma) * (slow_x if st == "slow" else 1.0)
        return "ok", lat

    t = 0.0
    while True:
        t += rng.expovariate(rate)
        if t >= minutes * 60:
            break
        m = int(t / 60)
        tot_m[m] += 1
        live = [r for r in range(3) if config != "retry, ejection and hedging" or ejected_until[r] <= t]
        if not live:
            live = [0, 1, 2]
        rep = live[rr % len(live)]
        rr += 1
        if config == "naive":
            out, lat = attempt(rep, t)
            ok = out == "ok" and lat <= 1000
            good = ok and lat <= slo_ms
        else:
            timeout = 150.0
            out, lat = attempt(rep, t)
            first_ok = out == "ok" and lat <= timeout
            if config == "retry, ejection and hedging":
                errors_in_row[rep] = 0 if first_ok else errors_in_row[rep] + 1
                if errors_in_row[rep] >= 5:
                    ejected_until[rep] = t + 10.0           # out of rotation for ten seconds, then probed
                    errors_in_row[rep] = 0
            if first_ok:
                elapsed = lat
            else:
                waited = 1.0 if out == "refused" else timeout
                others = [r for r in live if r != rep] or [r for r in range(3) if r != rep]
                r2 = rng.choice(others)
                hedge = config == "retry, ejection and hedging" and out != "refused"
                if hedge:                                  # the hedge went out at 100 ms, not at the timeout
                    waited = 100.0
                extra += 1
                out2, lat2 = attempt(r2, t)
                elapsed = waited + lat2 if out2 == "ok" else float("inf")
                if hedge and out == "ok":
                    elapsed = min(lat, elapsed)
            good = elapsed <= slo_ms
        good_m[m] += good
    share = [g / max(1, n) for g, n in zip(good_m, tot_m)]
    bad = sum(tot_m) - sum(good_m)
    month_budget = 0.001 * sum(tot_m) * 30 * 24
    return {"config": config, "per_minute": share, "good": sum(good_m) / sum(tot_m), "bad": bad,
            "budget_share": bad / month_budget, "extra_load": extra / sum(tot_m),
            "by_fault": {k: sum(good_m[a:b]) / max(1, sum(tot_m[a:b])) for k, _, a, b in FAULTS}}


def service_experiment(seed: int = 0) -> dict:
    return {"faults": [{"kind": k, "replica": r, "from": a, "to": b} for k, r, a, b in FAULTS],
            "runs": {c: service(c, seed=seed) for c in CONFIGS}}


def _run(c, until, rate):
    """Resume the cluster with clients at ``rate``: drop the queued client arrival, since run() schedules one."""
    import heapq
    c.events = [e for e in c.events if e[2] != "client"]
    heapq.heapify(c.events)
    c.run(until=until, client_rate=rate)


def raft_chaos(seconds: float = 60.0, seed: int = 1, rate: float = 20.0) -> dict:
    """Part 38's five-node Raft cluster under a script of faults; per second, the share of client commands that
    were accepted and eventually committed."""
    from explainer.cs.dist.raft import Cluster
    c = Cluster(5, seed=seed, loss=0.01, delay=(0.005, 0.02))
    sent = []
    orig = c.submit

    def submit(cmd=None):
        name = f"c{c.next_cmd}"
        ok = orig(name)
        sent.append((c.t, name, ok))
        return ok

    c.submit = submit
    script = [(10.0, "crash the leader"), (20.0, "restart it"), (30.0, "partition 2 | 3"), (40.0, "heal"),
              (45.0, "crash two followers"), (55.0, "restart them")]

    def leader():
        for nd in c.nodes:
            if nd.up and nd.role == "leader":
                return nd.id
        return 0

    marks = []
    crashed = []
    for t, what in script:
        _run(c, t, rate)
        L = leader()
        if what == "crash the leader":
            c.crash(L)
            crashed = [L]
        elif what == "restart it":
            for i in crashed:
                c.restart(i)
        elif what == "partition 2 | 3":
            others = [i for i in range(5) if i != L]
            c.partition([[L, others[0]], others[1:]])          # the leader is cut off in the minority
        elif what == "heal":
            c.heal()
        elif what == "crash two followers":
            crashed = [i for i in range(5) if i != L][:2]
            for i in crashed:
                c.crash(i)
        elif what == "restart them":
            for i in crashed:
                c.restart(i)
        marks.append({"t": t, "what": what, "leader": L})
    _run(c, seconds, rate)
    done = {cmd for _, cmd, _ in c.committed.values()}
    per = []
    for s in range(int(seconds)):
        xs = [(ok, name in done) for t, name, ok in sent if s <= t < s + 1]
        per.append(sum(1 for ok, d in xs if d) / max(1, len(xs)))
    return {"per_second": per, "script": marks, "committed": len(done), "sent": len(sent),
            "violations": len(c.violations), "available": sum(per) / len(per)}
