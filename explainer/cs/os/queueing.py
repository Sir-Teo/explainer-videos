"""Queues, simulated event by event (Part 31, chapter 12; the tail-latency frontier).

    r = mg1(lam=0.9, size=expo(1.0), n=200_000, discipline="fcfs")     # or "ps", "srpt"
    r["mean"], r["p99"], r["L"]              # mean and 99th-percentile response; time-average number in system
    path(lam, mu, T)                          # N(t) of an M/M/1 queue, for drawing its random walk
    multi(lam, size, c, policy)               # c cores: one central queue (c-FCFS), a queue per core (d-FCFS), or
                                              # processor sharing with a preemption quantum and its overhead

Formulas checked against: M/M/1 mean response 1/(mu - lam); Pollaczek-Khinchine for M/G/1 FCFS,
W = E[S] + lam E[S^2] / (2 (1 - rho)); processor sharing's E[T] = E[S] / (1 - rho), whatever the size distribution;
and Little's law L = lam W, which the simulation measures both ways.
"""
from __future__ import annotations

import heapq
import math
import random

import numpy as np


def expo(mean):
    return lambda rng: rng.expovariate(1.0 / mean)


def det(mean):
    return lambda rng: mean


def hyper(mean, scv):
    """A balanced two-phase hyperexponential with the given mean and squared coefficient of variation."""
    p = 0.5 * (1 + math.sqrt((scv - 1) / (scv + 1)))
    m1, m2 = mean / (2 * p), mean / (2 * (1 - p))
    return lambda rng: rng.expovariate(1 / m1) if rng.random() < p else rng.expovariate(1 / m2)


def bimodal(short, long_, p_long):
    return lambda rng: long_ if rng.random() < p_long else short


def pareto(mean, alpha=1.5, cap=None):
    xm = mean * (alpha - 1) / alpha

    def f(rng):
        x = xm / (1 - rng.random()) ** (1 / alpha)
        return min(x, cap) if cap else x
    return f


def pk(lam, es, es2):
    """Pollaczek-Khinchine: mean response time of M/G/1 FCFS."""
    rho = lam * es
    return es + lam * es2 / (2 * (1 - rho))


def mg1(lam: float, size, n: int = 200_000, discipline: str = "fcfs", seed: int = 1, warm: int = 2000) -> dict:
    """One server, Poisson arrivals at rate lam.  Returns response times (after a warm-up), their mean and
    percentiles, and L measured as the time-average number in the system."""
    rng = random.Random(seed)
    t = 0.0
    arr, sz = [], []
    for _ in range(n):
        t += rng.expovariate(lam)
        arr.append(t)
        sz.append(size(rng))
    T = _fcfs(arr, sz) if discipline == "fcfs" else _sharing(arr, sz, discipline)
    resp = np.array(T) - np.array(arr)
    span = max(T) - arr[0]
    L = resp.sum() / span        # the area under N(t), over the time
    r = resp[warm:]
    return {"mean": float(r.mean()), "p50": float(np.percentile(r, 50)), "p99": float(np.percentile(r, 99)),
            "p999": float(np.percentile(r, 99.9)), "L": float(L), "lam_hat": n / (arr[-1] - arr[0]),
            "W_all": float(resp.mean()), "rho": lam * float(np.mean(sz))}


def _fcfs(arr, sz):
    out, free = [], 0.0
    for a, s in zip(arr, sz):
        start = max(a, free)
        free = start + s
        out.append(free)
    return out


def _sharing(arr, sz, disc):
    """Processor sharing (every job at rate 1/N) or SRPT (the job with least remaining work), event by event."""
    n = len(arr)
    done = [0.0] * n
    rem = {}
    t = 0.0
    i = 0
    while i < n or rem:
        if not rem:
            t = arr[i]
            rem[i] = sz[i]
            i += 1
            continue
        nxt = arr[i] if i < n else math.inf
        if disc == "ps":
            k = len(rem)
            j, r = min(rem.items(), key=lambda kv: kv[1])
            fin = t + r * k
            if fin <= nxt:
                d = r
                for key in rem:
                    rem[key] -= d
                done[j] = fin
                del rem[j]
                t = fin
            else:
                d = (nxt - t) / k
                for key in rem:
                    rem[key] -= d
                t = nxt
                rem[i] = sz[i]
                i += 1
        else:  # srpt
            j, r = min(rem.items(), key=lambda kv: kv[1])
            fin = t + r
            if fin <= nxt:
                done[j] = fin
                del rem[j]
                t = fin
            else:
                rem[j] = r - (nxt - t)
                t = nxt
                rem[i] = sz[i]
                i += 1
    return done


def path(lam: float, mu: float, T: float, seed: int = 3) -> list[tuple[float, int]]:
    """The number in an M/M/1 system over [0, T]: (time, N) at every change."""
    rng = random.Random(seed)
    t, N, out = 0.0, 0, [(0.0, 0)]
    while t < T:
        rate = lam + (mu if N else 0.0)
        t += rng.expovariate(rate)
        N += 1 if rng.random() < lam / rate else -1
        out.append((t, N))
    return out


def multi(lam: float, size, c: int, policy: str = "cfcfs", n: int = 200_000, seed: int = 2, quantum: float = 5.0,
          overhead: float = 0.0, warm: int = 2000, short: float = 1.0) -> dict:
    """c servers.  ``cfcfs``: one shared FCFS queue; ``dfcfs``: each request joins a random core's own queue (as
    with receive-side scaling); ``ps``: a shared queue served in quanta (preempted after ``quantum``, back of the
    queue, ``overhead`` lost per preemption), as Shinjuku does with microsecond quanta.  ``short_p999`` is the
    99.9th percentile over requests of size at most ``short``: the ones a long request can block."""
    rng = random.Random(seed)
    t = 0.0
    arr, sz = [], []
    for _ in range(n):
        t += rng.expovariate(lam)
        arr.append(t)
        sz.append(size(rng))
    fin = [0.0] * n
    if policy == "dfcfs":
        free = [0.0] * c
        for k, (a, s) in enumerate(zip(arr, sz)):
            q = rng.randrange(c)
            start = max(a, free[q])
            free[q] = start + s
            fin[k] = free[q]
    elif policy == "cfcfs":
        cores = [0.0] * c
        heapq.heapify(cores)
        for k, (a, s) in enumerate(zip(arr, sz)):
            f = heapq.heappop(cores)
            start = max(a, f)
            fin[k] = start + s
            heapq.heappush(cores, fin[k])
    else:
        # event simulation: a FIFO of (job, remaining); c cores each run one quantum at a time
        from collections import deque
        q: deque = deque()
        ev: list = []          # (time, core)
        idle = list(range(c))
        i = 0
        now = 0.0
        rem = list(sz)
        running = {}
        while i < n or q or running:
            na = arr[i] if i < n else math.inf
            ne = ev[0][0] if ev else math.inf
            if na <= ne:
                now = na
                q.append(i)
                i += 1
            else:
                now, core = heapq.heappop(ev)
                j, ran = running.pop(core)
                rem[j] -= ran
                if rem[j] <= 1e-12:
                    fin[j] = now
                else:
                    q.append(j)
                idle.append(core)
            while idle and q:
                core = idle.pop()
                j = q.popleft()
                run = min(quantum, rem[j])
                cost = run + (overhead if rem[j] > quantum else 0.0)
                running[core] = (j, run)
                heapq.heappush(ev, (now + cost, core))
    resp = (np.array(fin) - np.array(arr))[warm:]
    s_ = np.array(sz)[warm:]
    sh, lo = resp[s_ <= short], resp[s_ > short]
    return {"mean": float(resp.mean()), "p50": float(np.percentile(resp, 50)), "p99": float(np.percentile(resp, 99)),
            "p999": float(np.percentile(resp, 99.9)), "short_p999": float(np.percentile(sh, 99.9)),
            "short_p99": float(np.percentile(sh, 99)), "long_mean": float(lo.mean()) if len(lo) else 0.0}
