"""Service-level instruments for Part 39: load balancing as a queueing system (the supermarket model), availability
arithmetic with correlated failures, and failure detection by timeouts and by phi accrual."""

from __future__ import annotations

import heapq
import math
import random

import numpy as np


# ---------------------------------------------------------------- the supermarket model

def balance(policy: str, servers: int = 100, load: float = 0.9, jobs: int = 100_000, seed: int = 0):
    """Poisson arrivals at rate ``load * servers``, exponential service of mean 1 at each FCFS server.  Policies:
    "random", "round robin", "two choices" (the shorter of two random queues), "shortest queue" (all).  Returns
    the mean and the 99th percentile of the response time, in units of the mean service time."""
    rng = random.Random(seed)
    nrng = np.random.default_rng(seed)
    q = np.zeros(servers, dtype=np.int64)
    free = [0.0] * servers
    done: list = []
    t = 0.0
    resp = []
    rr = 0
    lam = load * servers
    for _ in range(jobs):
        t += rng.expovariate(lam)
        while done and done[0][0] <= t:
            _, s = heapq.heappop(done)
            q[s] -= 1
        if policy == "random":
            s = rng.randrange(servers)
        elif policy == "round robin":
            s = rr
            rr = (rr + 1) % servers
        elif policy == "two choices":
            a, b = rng.randrange(servers), rng.randrange(servers)
            s = a if q[a] <= q[b] else b
        else:
            m = q.min()
            cand = np.flatnonzero(q == m)
            s = int(cand[nrng.integers(len(cand))])
        start = max(t, free[s])
        fin = start + rng.expovariate(1.0)
        free[s] = fin
        q[s] += 1
        heapq.heappush(done, (fin, s))
        resp.append(fin - t)
    r = np.array(resp[jobs // 10:])
    return {"policy": policy, "load": load, "mean": float(r.mean()), "p99": float(np.percentile(r, 99))}


def balance_table(loads=(0.5, 0.7, 0.8, 0.9, 0.95), policies=("random", "round robin", "two choices",
                                                               "shortest queue"), servers: int = 100,
                  jobs: int = 100_000):
    return [balance(p, servers, rho, jobs, seed=int(rho * 100)) for rho in loads for p in policies]


# ---------------------------------------------------------------- availability

def nines(a: float) -> float:
    return -math.log10(1 - a) if a < 1 else float("inf")


def availability(component: float = 0.999, deps=(1, 5, 10, 30, 100), replicas=(1, 2, 3), rack_down: float = 0.0005,
                 machine_down: float = 0.001, trials: int = 2_000_000, seed: int = 0):
    """Series: a request that needs ``n`` components each up a fraction ``component`` of the time.  Parallel:
    ``k`` replicas, any one suffices.  Correlation: machines fail independently a fraction ``machine_down`` of the
    time and their rack a fraction ``rack_down``; three replicas in one rack against three racks, by Monte Carlo."""
    series = [{"deps": n, "up": component ** n} for n in deps]
    par = [{"replicas": k, "up": 1 - (1 - component) ** k} for k in replicas]
    rng = np.random.default_rng(seed)
    rack = rng.random((trials, 3)) < rack_down
    mach = rng.random((trials, 3)) < machine_down
    same = rack[:, 0][:, None] | mach
    spread = rack | mach
    corr = {"same_rack": 1 - float(same.all(axis=1).mean()), "three_racks": 1 - float(spread.all(axis=1).mean()),
            "independent_formula": 1 - (rack_down + machine_down - rack_down * machine_down) ** 3,
            "same_rack_formula": 1 - (rack_down + (1 - rack_down) * machine_down ** 3)}
    return {"series": series, "parallel": par, "corr": corr, "component": component}


# ---------------------------------------------------------------- failure detection

def heartbeat_delays(n: int, rng: random.Random, base_ms: float = 5.0, calm: float = 0.3, noisy: float = 1.1,
                     period: int = 6000, pause_rate: float = 0.0001, pause_ms=(300.0, 2500.0)):
    """One-way delays: lognormal around ``base_ms``, with the network alternating every ``period`` heartbeats
    between calm (log-sd ``calm``) and congested (``noisy``) spells; plus, with probability ``pause_rate`` per
    heartbeat, a pause (a garbage collection) that delays this heartbeat and the ones queued behind it."""
    out = []
    hold = 0.0
    for k in range(n):
        sg = calm if (k // period) % 2 == 0 else noisy
        d = base_ms * math.exp(rng.gauss(0, sg))
        if rng.random() < pause_rate:
            hold = max(hold, rng.uniform(*pause_ms))
        out.append(d + hold)
        hold = max(0.0, hold - 100.0)
    return out


def detector(timeouts_ms=(150, 200, 300, 500, 1000, 2000, 3000), phis=(1, 2, 4, 8, 12), interval_ms: float = 100.0,
             hours: float = 10.0, seed: int = 0, window: int = 1000):
    """A process sends a heartbeat every ``interval_ms``.  A fixed timeout suspects it when no heartbeat has
    arrived for ``timeout`` ms; phi accrual (Hayashibara et al. 2004) suspects when phi = -log10 P(gap this long)
    under a normal fit of recent gaps exceeds a threshold.  For each setting: false suspicions per hour while the
    process is alive, and the mean time to detect a real crash."""
    rng = random.Random(seed)
    n = int(hours * 3600 * 1000 / interval_ms)
    arr = [k * interval_ms + d for k, d in enumerate(heartbeat_delays(n, rng))]
    arr.sort()
    gaps = np.diff(np.array(arr))
    fixed = []
    for T in timeouts_ms:
        fp = int((gaps > T).sum())
        # crash at a uniform moment: detection = time from crash to (last arrival + T)
        det = T - interval_ms / 2 + 2.0
        fixed.append({"timeout_ms": T, "false_per_hour": fp / hours, "detect_ms": det})
    acc = []
    cs = np.concatenate([[0.0], np.cumsum(gaps)])
    cs2 = np.concatenate([[0.0], np.cumsum(gaps ** 2)])
    idx = np.arange(len(gaps))
    lo = np.maximum(0, idx - window)
    cnt = idx - lo
    ok = cnt >= 30
    mu = (cs[idx] - cs[lo])[ok] / cnt[ok]
    var = (cs2[idx] - cs2[lo])[ok] / cnt[ok] - mu ** 2
    sd = np.maximum(np.sqrt(np.maximum(var, 0)), 0.1 * mu)
    x = gaps[ok]
    for th in phis:
        limit = mu + _norm_isf(10 ** (-th)) * sd
        acc.append({"phi": th, "false_per_hour": int((x > limit).sum()) / hours,
                    "detect_ms": float(np.mean(limit)) - interval_ms / 2 + 2.0})
    return {"fixed": fixed, "accrual": acc, "interval_ms": interval_ms, "hours": hours}


def _norm_isf(p: float) -> float:
    """Inverse survival function of the standard normal, by bisection."""
    lo, hi = -10.0, 40.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if 0.5 * math.erfc(mid / math.sqrt(2)) > p:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


# ---------------------------------------------------------------- tails through a call graph

def call_chain(depths=(1, 3, 10), median_ms: float = 10.0, sigma: float = 0.8, trials: int = 200_000, seed: int = 0):
    """A request passes through ``k`` services in sequence, each taking a lognormal time.  The end-to-end median
    and 99th percentile against the sum of the services' 99th percentiles (what a naive latency budget adds up)."""
    rng = np.random.default_rng(seed)
    out = []
    for k in depths:
        x = median_ms * np.exp(rng.normal(0, sigma, size=(trials, k)))
        tot = x.sum(axis=1)
        p99_each = float(np.percentile(x[:, 0], 99))
        out.append({"depth": k, "p50": float(np.median(tot)), "p99": float(np.percentile(tot, 99)),
                    "sum_of_p99": p99_each * k, "p99_each": p99_each})
    return out


def retry_amplification(layers=(1, 2, 3, 4), retries: int = 3, fail: float = 1.0):
    """When the bottom service fails every request, a stack of ``L`` layers that each retry ``retries`` times
    sends (retries + 1)^L attempts to the bottom for every user request; with a retry budget of 10% per layer,
    at most 1.1^L."""
    return [{"layers": L, "attempts": (retries + 1) ** L, "budgeted": 1.1 ** L} for L in layers]
