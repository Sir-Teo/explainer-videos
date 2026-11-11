"""Distributed systems at scale (Part 39): quorums and their staleness, CRDTs, consistent hashing and Chord,
two-phase commit and Spanner's commit wait, and the tail at scale.

    pbs(N, R, W, t, trials)           Bailis et al.'s probabilistically bounded staleness: the chance that a read t
        ms after a write returns the old value, with exponential write and read latencies (Monte Carlo)
    crdt_converge(kind, replicas, ops, trials)   random operations at random replicas, delivered in random orders,
        merged pairwise: do all replicas end equal?  kinds: "gcounter", "pncounter", "orset", "lww", and a
        "naive-set" whose merge is not idempotent/commutative, for contrast
    ring_load(nodes, vnodes, keys)    keys per node on a consistent-hash ring (max / mean, coefficient of variation)
    moved_fraction(n, scheme)         keys that move when one node is added: modulo hashing, the ring, jump hash,
        rendezvous
    chord_hops(n, lookups)            hops of Chord's finger-table lookups on n nodes
    two_pc(coordinator_crash)         participants' states through 2PC with the coordinator crashing after prepare:
        blocked for as long as it is down
    spanner(epsilon, ...)             TrueTime intervals and commit wait: a transaction's timeline
    tail(fanout, p_slow, ...)         a request fanning out to many servers waits for the slowest: p99 against
        fan-out, and hedged requests
"""
from __future__ import annotations

import bisect
import hashlib
import math
import random
import statistics


# ---- quorums -----------------------------------------------------------------------------------------------------
def pbs(N=3, R=1, W=1, t=0.0, trials=20000, seed=0, w_mean=10.0, r_mean=10.0):
    """A write goes to all N replicas, each arriving after an exponential delay (mean w_mean ms); it is acknowledged
    once W have it.  A read starts t ms after the acknowledgement, contacts all N, and returns the newest of the
    first R responses; a replica's response reflects the write if the write reached it before the read request
    did (request delay exponential, mean r_mean / 2)."""
    rng = random.Random(seed)
    stale = 0
    for _ in range(trials):
        arr = [rng.expovariate(1 / w_mean) for _ in range(N)]   # when the write reaches each replica
        ack = sorted(arr)[W - 1]
        start = ack + t
        resp = []
        for i in range(N):
            req = rng.expovariate(2 / r_mean)
            back = rng.expovariate(2 / r_mean)
            fresh = arr[i] <= start + req
            resp.append((req + back, fresh))
        resp.sort()
        if not any(f for _, f in resp[:R]):
            stale += 1
    return stale / trials


# ---- CRDTs -------------------------------------------------------------------------------------------------------
class GCounter:
    def __init__(self, n, me):
        if n <= 0 or not 0 <= me < n:
            raise ValueError("counter needs a nonempty replica set and a valid local replica")
        self.v = [0] * n
        self.me = me

    def inc(self, k=1):
        if k < 0:
            raise ValueError("grow-only counters cannot decrement")
        self.v[self.me] += k

    def merge(self, o):
        if len(self.v) != len(o.v):
            raise ValueError("counter replica sets must match")
        self.v = [max(a, b) for a, b in zip(self.v, o.v)]

    def value(self):
        return sum(self.v)

    def state(self):
        return tuple(self.v)


class PNCounter:
    def __init__(self, n, me):
        self.p, self.m = GCounter(n, me), GCounter(n, me)

    def inc(self, k=1):
        self.p.inc(k)

    def dec(self, k=1):
        self.m.inc(k)

    def merge(self, o):
        self.p.merge(o.p)
        self.m.merge(o.m)

    def value(self):
        return self.p.value() - self.m.value()

    def state(self):
        return (self.p.state(), self.m.state())


class ORSet:
    """Observed-remove set: each add creates a unique tag; remove deletes the tags it has seen."""

    def __init__(self, n, me):
        self.me, self.adds, self.removes, self.k = me, set(), set(), 0

    def add(self, x):
        self.k += 1
        self.adds.add((x, (self.me, self.k)))

    def remove(self, x):
        self.removes |= {a for a in self.adds if a[0] == x}

    def merge(self, o):
        self.adds |= o.adds
        self.removes |= o.removes

    def value(self):
        return frozenset(x for x, _ in self.adds - self.removes)

    def state(self):
        return self.value()


class LWW:
    """Last-writer-wins register with (timestamp, replica) tags."""

    def __init__(self, n, me):
        self.me, self.v, self.ts = me, None, (0, -1)

    def set(self, x, ts):
        if (ts, self.me) > self.ts:
            self.v, self.ts = x, (ts, self.me)

    def merge(self, o):
        if o.ts > self.ts:
            self.v, self.ts = o.v, o.ts

    def value(self):
        return self.v

    def state(self):
        return (self.v, self.ts)


class NaiveSet:
    """A set whose 'merge' replays the other replica's operation log: not idempotent, order-dependent."""

    def __init__(self, n, me):
        self.s, self.log = set(), []

    def add(self, x):
        self.s.add(x)
        self.log.append(("add", x))

    def remove(self, x):
        self.s.discard(x)
        self.log.append(("rem", x))

    def merge(self, o):
        for op, x in o.log:
            (self.s.add if op == "add" else self.s.discard)(x)

    def value(self):
        return frozenset(self.s)

    def state(self):
        return self.value()


KINDS = {"gcounter": GCounter, "pncounter": PNCounter, "orset": ORSet, "lww": LWW, "naive-set": NaiveSet}


def crdt_converge(kind: str, replicas: int = 4, ops: int = 40, trials: int = 500, seed: int = 0):
    rng = random.Random(seed)
    agree = 0
    for _ in range(trials):
        reps = [KINDS[kind](replicas, i) for i in range(replicas)]
        for step in range(ops):
            r = reps[rng.randrange(replicas)]
            x = rng.randrange(5)
            if kind == "gcounter":
                r.inc()
            elif kind == "pncounter":
                r.inc() if rng.random() < 0.6 else r.dec()
            elif kind == "lww":
                r.set(x, step)
            else:
                r.add(x) if rng.random() < 0.6 else r.remove(x)
            if rng.random() < 0.3:                       # gossip: a random merge, in a random direction
                a, b = rng.sample(reps, 2)
                a.merge(b)
        # anti-entropy in a random order until every pair has merged, twice
        pairs = [(a, b) for a in range(replicas) for b in range(replicas) if a != b]
        for _ in range(2):
            rng.shuffle(pairs)
            for a, b in pairs:
                reps[a].merge(reps[b])
        agree += len({r.state() for r in reps}) == 1
    return {"kind": kind, "trials": trials, "converged": agree}


# ---- partitioning ------------------------------------------------------------------------------------------------
def _h(s: str) -> int:
    return int.from_bytes(hashlib.sha256(s.encode()).digest()[:8], "big")


def ring_load(nodes: int, vnodes: int = 1, keys: int = 100000, seed: int = 0):
    points = sorted((_h(f"n{n}-v{v}-{seed}"), n) for n in range(nodes) for v in range(vnodes))
    hs = [p for p, _ in points]
    load = [0] * nodes
    for k in range(keys):
        i = bisect.bisect(hs, _h(f"key{k}")) % len(points)
        load[points[i][1]] += 1
    mean = keys / nodes
    return {"nodes": nodes, "vnodes": vnodes, "max_over_mean": max(load) / mean,
            "cv": statistics.pstdev(load) / mean, "min_over_mean": min(load) / mean}


def jump_hash(key: int, buckets: int) -> int:
    """Lamping and Veach (2014)."""
    b, j = -1, 0
    key &= (1 << 64) - 1
    while j < buckets:
        b = j
        key = (key * 2862933555777941757 + 1) & ((1 << 64) - 1)
        j = int((b + 1) * (float(1 << 31) / float((key >> 33) + 1)))
    return b


def moved_fraction(n: int = 10, keys: int = 50000, vnodes: int = 100):
    def ring(m):
        pts = sorted((_h(f"n{x}-v{v}"), x) for x in range(m) for v in range(vnodes))
        hs = [p for p, _ in pts]
        return lambda k: pts[bisect.bisect(hs, _h(f"key{k}")) % len(pts)][1]
    r1, r2 = ring(n), ring(n + 1)
    out = {}
    out["modulo"] = sum(_h(f"key{k}") % n != _h(f"key{k}") % (n + 1) for k in range(keys)) / keys
    out["ring"] = sum(r1(k) != r2(k) for k in range(keys)) / keys
    out["jump"] = sum(jump_hash(_h(f"key{k}"), n) != jump_hash(_h(f"key{k}"), n + 1) for k in range(keys)) / keys

    def rv(k, m):
        return max(range(m), key=lambda x: _h(f"{k}|{x}"))
    out["rendezvous"] = sum(rv(k, n) != rv(k, n + 1) for k in range(keys // 10)) / (keys // 10)
    out["ideal"] = 1 / (n + 1)
    return out


def chord_hops(n: int = 1024, lookups: int = 2000, bits: int = 32, seed: int = 0):
    rng = random.Random(seed)
    M = 1 << bits
    ids = sorted(rng.sample(range(M), n))

    def succ(x):
        i = bisect.bisect_left(ids, x % M)
        return ids[i % n]
    fingers = {u: [succ(u + (1 << i)) for i in range(bits)] for u in ids}

    def between(x, a, b):                                  # x in (a, b] on the circle
        return (a < x <= b) if a < b else (x > a or x <= b)
    hops = []
    for _ in range(lookups):
        key = rng.randrange(M)
        u = rng.choice(ids)
        h = 0
        while not between(key, u, succ(u + 1)) and succ(key) != u:
            nxt = u
            for f in reversed(fingers[u]):
                if between(f, u, key) and f != key:
                    nxt = f
                    break
            if nxt == u:
                nxt = succ(u + 1)
            u = nxt
            h += 1
            if h > 4 * bits:
                break
        hops.append(h + 1)
    return {"n": n, "mean": statistics.mean(hops), "max": max(hops), "half_log2n": 0.5 * math.log2(n)}


# ---- transactions ------------------------------------------------------------------------------------------------
def two_pc(participants: int = 3, crash_at: float | None = 1.0, recover_at: float = 31.0, rtt: float = 0.01):
    """A timeline: prepare at 0, votes return at rtt; the coordinator logs commit and would send it at rtt, but
    crashes at ``crash_at`` (just after receiving the votes, before sending the decision).  Participants that
    voted yes hold their locks, uncertain, until it recovers."""
    ev = [(0.0, "coordinator", "PREPARE to all")]
    for p in range(participants):
        ev.append((rtt / 2, f"P{p + 1}", "vote YES, lock rows, wait"))
    ev.append((rtt, "coordinator", "all YES: decide COMMIT"))
    blocked = 0.0
    if crash_at is not None:
        ev.append((rtt + 1e-4, "coordinator", "crash"))
        ev.append((recover_at, "coordinator", "recover: read the log, resend COMMIT"))
        blocked = recover_at - rtt
        for p in range(participants):
            ev.append((recover_at + rtt / 2, f"P{p + 1}", "COMMIT, release locks"))
    else:
        for p in range(participants):
            ev.append((rtt * 1.5, f"P{p + 1}", "COMMIT, release locks"))
    return {"events": ev, "blocked_seconds": blocked}


def spanner(epsilon_ms: float = 7.0, lock_ms: float = 2.0, paxos_ms: float = 8.0):
    """TrueTime returns [now - eps, now + eps].  The coordinator picks s = TT.now().latest, then waits until
    TT.now().earliest > s before releasing locks: a commit wait of about 2 eps, overlapped with Paxos."""
    s = lock_ms + epsilon_ms                   # true time lock_ms, latest bound = true + eps
    wait_until = s + epsilon_ms               # earliest bound exceeds s once true time passes s + eps
    paxos_done = lock_ms + paxos_ms
    release = max(wait_until, paxos_done)
    return {"epsilon_ms": epsilon_ms, "timestamp_ms": s, "commit_wait_ms": wait_until - lock_ms,
            "paxos_done_ms": paxos_done, "release_ms": release, "visible_after_ms": release}


# ---- the tail ----------------------------------------------------------------------------------------------------
def tail(fanouts=(1, 10, 100, 1000), p_slow: float = 0.01, fast_ms: float = 10.0, slow_ms: float = 1000.0,
         trials: int = 20000, hedge_at: float | None = None, seed: int = 0):
    """Each server answers in fast_ms (exponential) with probability 1 - p_slow, else slow_ms; a request waits for
    all of its fan-out.  With hedging, a second copy is sent to another server if no reply after ``hedge_at`` ms,
    and the first reply wins."""
    rng = random.Random(seed)

    def one():
        t = rng.expovariate(1 / fast_ms) if rng.random() > p_slow else slow_ms
        if hedge_at is not None and t > hedge_at:
            t2 = hedge_at + (rng.expovariate(1 / fast_ms) if rng.random() > p_slow else slow_ms)
            t = min(t, t2)
        return t
    out = []
    for f in fanouts:
        lat = sorted(max(one() for _ in range(f)) for _ in range(max(200, trials // f)))
        out.append({"fanout": f, "p50": lat[len(lat) // 2], "p99": lat[int(0.99 * len(lat))],
                    "frac_slow": sum(1 for x in lat if x >= slow_ms * 0.9) / len(lat),
                    "formula": 1 - (1 - p_slow) ** f})
    return out


# ---- replication lag, CAP, two choices, metastable failure -----------------------------------------------------
def replication_lag(lag_ms: float = 100.0, delays=(0, 10, 50, 100, 200, 500), followers: int = 2, trials: int = 20000,
                    seed: int = 0):
    """Single-leader, asynchronous replication: each follower applies a write after an exponential lag.  A user
    writes, then reads t ms later from a random replica (the leader or a follower): how often does it miss its own
    write (a read-your-writes violation)?"""
    rng = random.Random(seed)
    out = []
    for t in delays:
        miss = 0
        for _ in range(trials):
            r = rng.randrange(followers + 1)
            if r > 0 and rng.expovariate(1 / lag_ms) > t:
                miss += 1
        out.append({"t_ms": t, "violations": miss / trials})
    return out


def cap(partition_s: float = 10.0, rate: float = 100.0, minority_share: float = 0.4):
    """Clients on both sides of a partition of a replicated register keep issuing reads and writes.  CP: the
    minority side refuses everything; AP: both sides accept, the minority's reads miss majority writes and
    conflicting writes must be merged afterwards."""
    total = rate * partition_s
    minority = total * minority_share
    return {"cp": {"available": 1 - minority_share, "stale_reads": 0.0, "conflicts": 0},
            "ap": {"available": 1.0, "stale_fraction_of_minority_reads": 1.0,
                   "conflicting_writes": int(minority / 2)}, "requests": int(total)}


def two_choices(n: int = 1000, balls: int | None = None, d: int = 2, trials: int = 20, seed: int = 0):
    rng = random.Random(seed)
    balls = balls or n
    mx = []
    for _ in range(trials):
        b = [0] * n
        for _ in range(balls):
            c = min((rng.randrange(n) for _ in range(d)), key=lambda i: b[i])
            b[c] += 1
        mx.append(max(b))
    return statistics.mean(mx)


def metastable(seconds: int = 120, capacity: float = 100.0, base: float = 80.0, spike=(30, 40, 160.0),
               timeout_s: float = 1.0, retries: int = 3, backoff: bool = False, drop_expired: bool = False,
               seed: int = 0):
    """A server handles ``capacity`` requests a second, first come first served; clients time out after
    ``timeout_s`` and retry (immediately, or with exponential backoff), up to ``retries`` times.  A request
    served after its client gave up is wasted work.  After a short spike in load, retries can keep the server
    overloaded indefinitely: goodput collapses and stays down although the spike has passed."""
    rng = random.Random(seed)
    queue = []                    # (arrival time, deadline, attempt)
    good = []
    load = []
    pending = []                  # retries scheduled: (time, attempt)
    t = 0.0
    dt = 0.01
    served_acc = 0.0
    for step in range(int(seconds / dt)):
        t = step * dt
        lam = spike[2] if spike[0] <= t < spike[1] else base
        n_new, p_acc, L = 0, rng.random(), math.exp(-lam * dt)        # Poisson arrivals (Knuth)
        while p_acc > L:
            n_new += 1
            p_acc *= rng.random()
        for _ in range(n_new):
            queue.append((t, t + timeout_s, 0))
        due = [p for p in pending if p[0] <= t]
        pending = [p for p in pending if p[0] > t]
        for _, a in due:
            queue.append((t, t + timeout_s, a))
        # timeouts: the client gives up (and schedules a retry) but the request stays queued: the server still
        # works on it later, wasting capacity
        served_acc += capacity * dt
        g = 0
        while served_acc >= 1 and queue:
            served_acc -= 1
            arr, dl, a = queue.pop(0)
            if t <= dl:
                g += 1
            elif drop_expired:
                served_acc += 1                       # discarding a dead request costs (almost) nothing
        if not queue:
            served_acc = min(served_acc, 1.0)
        # clients whose deadline passed this step retry
        for arr, dl, a in queue:
            if dl <= t < dl + dt and a < retries:
                wait = (2 ** a) * 0.5 * rng.random() if backoff else 0.0
                pending.append((t + wait, a + 1))
        good.append(g / dt)
        load.append(len(queue))
    sec = [statistics.mean(good[int(i / dt):int((i + 1) / dt)]) for i in range(seconds)]
    q = [load[int(i / dt)] for i in range(seconds)]
    return {"goodput": sec, "queue": q, "capacity": capacity, "base": base, "spike": list(spike),
            "retries": retries, "backoff": backoff, "drop_expired": drop_expired}
