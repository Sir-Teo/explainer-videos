"""Overload and its defences (Part 50): backoff with and without jitter on a contended resource (after Brooker,
2015); a metastable failure, where retries keep a server overloaded after its trigger has passed, and what
backoff, retry budgets, load shedding and a circuit breaker do to it; bulkheads; hedged requests."""

from __future__ import annotations

import heapq
import math
import random
from collections import deque

# ---------------------------------------------------------------- backoff and jitter

STRATEGIES = ("no backoff", "exponential", "full jitter", "equal jitter", "decorrelated jitter")


def _delay(strategy, attempt, prev, rng, base, cap):
    if strategy == "no backoff":
        return base
    v = min(cap, base * 2 ** attempt)
    if strategy == "exponential":
        return v
    if strategy == "full jitter":
        return rng.uniform(0, v)
    if strategy == "equal jitter":
        return v / 2 + rng.uniform(0, v / 2)
    if strategy == "decorrelated jitter":
        return min(cap, rng.uniform(base, prev * 3))
    raise ValueError(strategy)


def contention(strategy: str, clients: int = 50, base: float = 1.0, cap: float = 1000.0, noise: float = 0.1,
               limit: float = 20_000.0, seed: int = 0, keep: bool = False) -> dict:
    """``clients`` each need one successful write to a resource that takes one time unit per write and fails
    every write that overlaps another (optimistic concurrency: an attempt starting at t succeeds only if no other
    starts in (t - 1, t + 1)).  They all start at once; after a failure each waits a delay chosen by ``strategy``,
    plus the network's own small jitter (up to ``noise``), and tries again.  Returns the total calls and the time
    until the last client succeeds (or how many finished before ``limit``)."""
    rng = random.Random(seed)
    heap = [(rng.uniform(0, noise), i, 0, base) for i in range(clients)]
    heapq.heapify(heap)
    active = deque()                         # [start, client, attempt, prev delay, failed]
    calls, finished, done_at, attempts = 0, 0, 0.0, []

    def settle(x):
        nonlocal finished, done_at
        st, i, a, prev, failed = x
        if not failed:
            finished += 1
            done_at = max(done_at, st + 1.0)
            return
        d = _delay(strategy, a, prev, rng, base, cap)
        heapq.heappush(heap, (st + 1.0 + d + rng.uniform(0, noise), i, a + 1, max(base, d)))

    while heap:
        t, i, a, prev = heapq.heappop(heap)
        while active and active[0][0] <= t - 1.0:
            settle(active.popleft())
        if t > limit:
            break
        calls += 1
        if keep and t < 3000:
            attempts.append((round(t, 3), i))
        x = [t, i, a, prev, False]
        if active:
            x[4] = True
            for y in active:
                y[4] = True
        active.append(x)
        if not heap:
            while active:
                settle(active.popleft())
    out = {"strategy": strategy, "clients": clients, "calls": calls, "finished": finished,
           "time": done_at if finished == clients else None, "calls_per_client": calls / clients}
    if keep:
        out["attempts"] = attempts
    return out


def jitter_experiment(clients=(10, 25, 50, 100), trials: int = 10, seed: int = 0) -> dict:
    rows = []
    for n in clients:
        for s in STRATEGIES:
            rs = [contention(s, clients=n, seed=seed + k) for k in range(trials)]
            times = [r["time"] for r in rs if r["time"] is not None]
            rows.append({"clients": n, "strategy": s, "calls": sum(r["calls"] for r in rs) / trials,
                         "time": sum(times) / len(times) if len(times) == trials else None,
                         "finished": sum(r["finished"] for r in rs) / trials})
    timelines = {s: contention(s, clients=20, seed=seed, keep=True)["attempts"] for s in
                 ("no backoff", "exponential", "full jitter")}
    return {"rows": rows, "timelines": timelines}


# ---------------------------------------------------------------- metastable failure and its defences

def overload(policy: str = "retries", seconds: int = 120, capacity: float = 100.0, base: float = 80.0,
             trigger=(30.0, 40.0, 0.5), timeout_s: float = 1.0, retries: int = 3, budget: float = 0.1,
             shed_after_s: float = 0.5, seed: int = 0) -> dict:
    """A server does ``capacity`` requests a second, first come first served.  Clients send ``base`` new requests
    a second, give up after ``timeout_s`` and retry.  The trigger: capacity falls to a fraction ``trigger[2]`` of
    normal between ``trigger[0]`` and ``trigger[1]`` seconds (a server lost, a long pause).

    Policies: "none" (no retries), "retries" (immediate), "backoff" (exponential with full jitter), "budget"
    (retries limited to a fraction ``budget`` of first attempts, a token bucket per client), "shed" (the server
    drops requests that have waited longer than ``shed_after_s`` instead of serving them late), "breaker" (clients
    stop sending for 5 s when more than half of the last second's requests failed, then probe).

    Returns goodput (requests answered in time) and offered load per second."""
    rng = random.Random(seed)
    dt = 0.01
    queue = deque()                             # (enqueue time, request id)
    state = {}                                  # id -> [deadline, attempt, done]
    deadlines = []                              # heap (deadline, id)
    retry_at = []                               # heap (time, attempt)
    nid = 0
    tokens = 10.0
    good_s = [0.0] * seconds
    offered_s = [0.0] * seconds
    shed_s = [0.0] * seconds
    work = 0.0
    recent = deque()                            # (time, ok) of finished client attempts
    open_until = -1.0
    breaker_s = [0] * seconds
    for step in range(int(seconds / dt)):
        t = step * dt
        sec = min(seconds - 1, int(t))
        cap = capacity * (trigger[2] if trigger[0] <= t < trigger[1] else 1.0)
        # breaker state
        while recent and recent[0][0] < t - 1.0:
            recent.popleft()
        if policy == "breaker" and t >= open_until and len(recent) > 20:
            fails = sum(1 for _, ok in recent if not ok)
            if fails > 0.5 * len(recent):
                open_until = t + 5.0
                recent.clear()
        is_open = policy == "breaker" and t < open_until
        breaker_s[sec] = max(breaker_s[sec], int(is_open))

        def send(attempt):
            nonlocal nid
            if is_open and rng.random() > 0.05:            # fail fast; let a few probes through
                return
            nid += 1
            state[nid] = [t + timeout_s, attempt, False]
            heapq.heappush(deadlines, (t + timeout_s, nid))
            queue.append((t, nid))
            offered_s[sec] += 1

        lam = base * dt
        n_new = 0
        L, p = math.exp(-lam), rng.random()
        while p > L:
            n_new += 1
            p *= rng.random()
        for _ in range(n_new):
            tokens = min(10.0, tokens + budget)
            send(0)
        while retry_at and retry_at[0][0] <= t:
            _, a = heapq.heappop(retry_at)
            send(a)
        # serve
        work += cap * dt
        while work >= 1 and queue:
            enq, i = queue.popleft()
            if i not in state:                            # long abandoned: the work is wasted
                work -= 1
                continue
            dl, a, done = state[i]
            if policy == "shed" and t - enq > shed_after_s:
                shed_s[sec] += 1
                work -= 0.02                              # rejecting costs a little
                continue
            work -= 1
            if t <= dl and not done:
                good_s[sec] += 1
                state[i][2] = True
                recent.append((t, True))
        if not queue:
            work = min(work, 1.0)
        # timeouts
        while deadlines and deadlines[0][0] <= t:
            _, i = heapq.heappop(deadlines)
            if i not in state:
                continue
            dl, a, done = state[i]
            if done:
                continue
            state[i][2] = True                            # the client gives up; the server may still work on it
            recent.append((t, False))
            if policy == "none" or a >= retries:
                continue
            if policy == "budget":
                if tokens < 1:
                    continue
                tokens -= 1
            if policy == "backoff":
                wait = rng.uniform(0, 0.1 * 2 ** (a + 1))
            else:
                wait = 0.0
            heapq.heappush(retry_at, (t + wait, a + 1))
        if step % 100 == 0:                               # forget finished requests
            for i in [k for k, v in state.items() if v[2] and v[0] < t - 30]:
                del state[i]
    recovered = next((s for s in range(int(trigger[1]), seconds) if good_s[s] >= 0.9 * base), None)
    return {"policy": policy, "goodput": good_s, "offered": offered_s, "shed": shed_s, "breaker_open": breaker_s,
            "capacity": capacity, "base": base, "trigger": list(trigger),
            "recovered_s": None if recovered is None else recovered - trigger[1]}


POLICIES = ("none", "retries", "backoff", "budget", "shed", "breaker")


def overload_experiment(seed: int = 0) -> dict:
    return {p: overload(p, seed=seed) for p in POLICIES}


def trigger_sizes(drops=(0.9, 0.8, 0.7, 0.6, 0.5), lengths=(2, 5, 10, 20), seed: int = 0) -> list[dict]:
    """Which triggers tip the retrying system into its bad state: capacity falling to ``drop`` of normal for
    ``length`` seconds.  Metastable if goodput has not recovered 60 seconds after the trigger ends."""
    rows = []
    for d in drops:
        for L in lengths:
            r = overload("retries", seconds=100 + L, trigger=(30.0, 30.0 + L, d), seed=seed)
            rows.append({"drop": d, "seconds": L, "stuck": r["recovered_s"] is None})
    return rows


# ---------------------------------------------------------------- bulkheads

def bulkhead(partitioned: bool, seconds: int = 60, threads: int = 30, rate_a: float = 40.0, rate_b: float = 20.0,
             slow=(20.0, 40.0), fast_s: float = 0.05, slow_s: float = 2.0, seed: int = 0) -> dict:
    """A service calls dependencies A and B from one pool of ``threads`` worker threads (or two pools of half the
    size, the bulkheads).  B becomes slow between ``slow[0]`` and ``slow[1]``.  A call that finds no free thread
    is rejected.  Returns the share of calls to A and to B that succeed each second."""
    rng = random.Random(seed)
    events = []
    for dep, rate in (("A", rate_a), ("B", rate_b)):
        t = 0.0
        while True:
            t += rng.expovariate(rate)
            if t >= seconds:
                break
            events.append((t, dep))
    events.sort()
    busy = {"A": [], "B": []} if partitioned else {"all": []}
    limit = {"A": threads // 2, "B": threads - threads // 2} if partitioned else {"all": threads}
    ok = {d: [0] * seconds for d in "AB"}
    tot = {d: [0] * seconds for d in "AB"}
    for t, dep in events:
        pool = dep if partitioned else "all"
        b = busy[pool]
        while b and b[0] <= t:
            heapq.heappop(b)
        s = int(t)
        tot[dep][s] += 1
        if len(b) >= limit[pool]:
            continue
        dur = slow_s if (dep == "B" and slow[0] <= t < slow[1]) else fast_s
        heapq.heappush(b, t + rng.expovariate(1 / dur))
        ok[dep][s] += 1
    share = {d: [ok[d][s] / max(1, tot[d][s]) for s in range(seconds)] for d in "AB"}
    return {"partitioned": partitioned, "share": share, "slow": list(slow), "threads": threads}


# ---------------------------------------------------------------- hedged requests

def hedging(hedge_at_ms=(None, 50.0, 20.0, 12.0), trials: int = 200_000, p_slow: float = 0.02,
            fast_ms: float = 5.0, slow_ms: float = 200.0, seed: int = 0) -> list[dict]:
    """Each server answers in an exponential time of mean ``fast_ms``, except a fraction ``p_slow`` of requests
    that hit a pause of ``slow_ms``.  A hedge sends a second copy to another server if the first has not answered
    after ``hedge_at_ms``; the first answer wins.  Tail latency against the extra load."""
    rng = random.Random(seed)
    rows = []
    for h in hedge_at_ms:
        lat, extra = [], 0
        for _ in range(trials):
            t = rng.expovariate(1 / fast_ms) + (slow_ms if rng.random() < p_slow else 0.0)
            if h is not None and t > h:
                extra += 1
                t = min(t, h + rng.expovariate(1 / fast_ms) + (slow_ms if rng.random() < p_slow else 0.0))
            lat.append(t)
        lat.sort()
        rows.append({"hedge_at_ms": h, "p50": lat[trials // 2], "p99": lat[int(trials * 0.99)],
                     "p999": lat[int(trials * 0.999)], "extra_load": extra / trials})
    return rows
