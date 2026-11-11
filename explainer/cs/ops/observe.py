"""Observability (Part 50): why averages lie; latency sketches with error guarantees (DDSketch, Masson, Rim and Lee
2019; an HDR-style log-linear histogram) against Part 46's KLL; distributed traces, their critical path, and head
against tail sampling; coordinated omission in load generators; open against closed load; and change-point
detection for performance regressions in CI."""

from __future__ import annotations

import math
import random

import numpy as np


# ---------------------------------------------------------------- sketches

class DDSketch:
    """Values in (gamma^(i-1), gamma^i] share bucket i, with gamma = (1 + alpha) / (1 - alpha).  Answering a quantile
    with 2 gamma^i / (gamma + 1) is within a relative error alpha of every value in the bucket."""

    def __init__(self, alpha: float = 0.01):
        if not 0 < alpha < 1:
            raise ValueError("relative error must lie in (0, 1)")
        self.alpha = alpha
        self.gamma = (1 + alpha) / (1 - alpha)
        self.lg = math.log(self.gamma)
        self.counts: dict[int, int] = {}
        self.n = 0

    def add(self, x: float) -> None:
        if not math.isfinite(x) or x <= 0:
            raise ValueError("this sketch models positive finite values")
        i = math.ceil(math.log(x) / self.lg)
        self.counts[i] = self.counts.get(i, 0) + 1
        self.n += 1

    def merge(self, other: "DDSketch") -> "DDSketch":
        if self.alpha != other.alpha:
            raise ValueError("merged sketches must use the same relative error")
        for i, c in other.counts.items():
            self.counts[i] = self.counts.get(i, 0) + c
        self.n += other.n
        return self

    def quantile(self, q: float) -> float:
        if not 0 <= q <= 1:
            raise ValueError("quantile must lie in [0, 1]")
        if not self.n:
            return float("nan")
        rank = q * (self.n - 1)
        seen = 0
        for i in sorted(self.counts):
            seen += self.counts[i]
            if seen > rank:
                return 2 * self.gamma ** i / (self.gamma + 1)
        return 2 * self.gamma ** max(self.counts) / (self.gamma + 1)

    @property
    def buckets(self) -> int:
        return len(self.counts)


class LogLinear:
    """An HDR-style histogram: each power of two split into 2^bits equal sub-buckets, so relative error is at most
    2^-bits (about two significant digits at bits = 7).  Values are in microseconds."""

    def __init__(self, bits: int = 7):
        self.bits = bits
        self.counts: dict[tuple[int, int], int] = {}
        self.n = 0

    def add(self, x: float) -> None:
        e = math.floor(math.log2(x))
        sub = int((x / 2 ** e - 1) * 2 ** self.bits)
        k = (e, sub)
        self.counts[k] = self.counts.get(k, 0) + 1
        self.n += 1

    def quantile(self, q: float) -> float:
        rank = q * (self.n - 1)
        seen = 0
        for (e, sub) in sorted(self.counts):
            seen += self.counts[(e, sub)]
            if seen > rank:
                return 2 ** e * (1 + (sub + 0.5) / 2 ** self.bits)
        return float("nan")

    @property
    def buckets(self) -> int:
        return len(self.counts)


def latencies(n: int = 200_000, seed: int = 0) -> np.ndarray:
    """Request latencies in milliseconds: lognormal around 20 ms for most requests, a slower mode for 5% (cache
    misses) and a heavy Pareto tail for 0.5% (pauses, retries)."""
    rng = np.random.default_rng(seed)
    x = rng.lognormal(math.log(20), 0.35, n)
    miss = rng.random(n) < 0.05
    x[miss] = rng.lognormal(math.log(120), 0.3, miss.sum())
    tail = rng.random(n) < 0.005
    x[tail] = 300 * (1 + rng.pareto(1.5, tail.sum()))
    return x


QS = (0.5, 0.9, 0.99, 0.999, 0.9999)


def sketch_experiment(n: int = 200_000, seed: int = 0) -> dict:
    from explainer.cs.data.columnar import KLL
    x = latencies(n, seed)
    true = {q: float(np.quantile(x, q, method="lower")) for q in QS}
    dd, hdr, kll = DDSketch(0.01), LogLinear(7), KLL(200, seed=seed)
    for v in x:
        dd.add(v)
        hdr.add(v * 1000)
        kll.add(v)
    rng = np.random.default_rng(seed + 1)
    sample = np.sort(rng.choice(x, 1000, replace=False))
    rows = []
    for q in QS:
        est = {"DDSketch": dd.quantile(q), "log-linear": hdr.quantile(q) / 1000, "KLL": kll.quantile(q),
               "sample of 1000": float(np.quantile(sample, q))}
        rows.append({"q": q, "true": true[q], **{k: v for k, v in est.items()},
                     **{"err " + k: abs(v - true[q]) / true[q] for k, v in est.items()}})
    hist, edges = np.histogram(np.log10(x), bins=60)
    return {"rows": rows, "n": n, "mean": float(x.mean()), "max": float(x.max()),
            "size": {"DDSketch": dd.buckets, "log-linear": hdr.buckets, "KLL": kll.size(),
                     "sample of 1000": 1000},
            "hist": {"counts": hist.tolist(), "log10_edges": edges.tolist()}}


def averages_lie(servers: int = 10, n: int = 20_000, seed: int = 0) -> dict:
    """Ten servers, one of them slow.  The mean hides the tail; averaging each server's p99 is not the fleet's p99;
    merging per-server sketches is exact to the sketch's error."""
    rng = np.random.default_rng(seed)
    per = []
    sk = DDSketch(0.01)
    for s in range(servers):
        x = latencies(n, seed + s)
        if s == 0:
            x = x * 4
        per.append(x)
        d = DDSketch(0.01)
        for v in x:
            d.add(v)
        sk.merge(d)
    allx = np.concatenate(per)
    p99s = [float(np.quantile(v, 0.99)) for v in per]
    _ = rng
    return {"mean": float(allx.mean()), "median": float(np.median(allx)), "p99": float(np.quantile(allx, 0.99)),
            "p999": float(np.quantile(allx, 0.999)), "mean_of_p99s": float(np.mean(p99s)), "p99s": p99s,
            "merged_sketch_p99": sk.quantile(0.99),
            "users_seeing_p99_in_100_requests": 1 - 0.99 ** 100}


# ---------------------------------------------------------------- traces

TREE = ("frontend", [("auth", []),
                     ("catalog", [("cache", []), ("db", [])]),
                     ("recommend", [("features", []), ("model", [])]),
                     ("render", [])])
PARALLEL = {"frontend": {"catalog", "recommend"}}          # these children run concurrently; others in sequence
MEAN_MS = {"frontend": 2, "auth": 3, "catalog": 2, "cache": 1, "db": 6, "recommend": 2, "features": 5, "model": 12,
           "render": 4}


def make_trace(rng: random.Random, start: float = 0.0, node=TREE, parent=None, spans=None, slow_p: float = 0.01,
               err_p: float = 0.002):
    """A synthetic trace: each span does some work of its own, calls its children (in sequence, or some in
    parallel), then finishes.  Rarely a span is slow (a pause) or fails."""
    if spans is None:
        spans = []
    name, kids = node
    sid = len(spans)
    span = {"id": sid, "parent": parent, "service": name, "start": start, "end": None, "error": False}
    spans.append(span)
    t = start + rng.expovariate(1 / (MEAN_MS[name] * 0.3))
    par = PARALLEL.get(name, set())
    group_end = t
    for k in kids:
        if k[0] in par:
            make_trace(rng, t, k, sid, spans, slow_p, err_p)
            group_end = max(group_end, spans[-1 - _size(k) + 1]["end"])
        else:
            t = max(t, group_end)
            make_trace(rng, t, k, sid, spans, slow_p, err_p)
            t = spans[-_size(k)]["end"]
            group_end = t
    t = max(t, group_end)
    own = rng.expovariate(1 / (MEAN_MS[name] * 0.7))
    if rng.random() < slow_p:
        own += 200
    span["end"] = t + own
    span["error"] = rng.random() < err_p
    return spans


def _size(node) -> int:
    return 1 + sum(_size(k) for k in node[1])


def critical_path(spans: list[dict]) -> list[tuple[int, float, float]]:
    """Walk back from the root's end: at each moment, the work that the end was waiting for.  Returns segments
    (span id, from, to) that tile the root's duration."""
    kids = {}
    for s in spans:
        if s["parent"] is not None:
            kids.setdefault(s["parent"], []).append(s)

    def walk(s, until):
        segs = []
        t = until
        for c in sorted(kids.get(s["id"], []), key=lambda c: -c["end"]):
            if c["end"] <= t and c["end"] > s["start"]:
                if c["end"] < t:
                    segs.append((s["id"], c["end"], t))
                segs += walk(c, c["end"])
                t = c["start"]
        if t > s["start"]:
            segs.append((s["id"], s["start"], t))
        return segs

    root = spans[0]
    return sorted(walk(root, root["end"]), key=lambda x: x[1])


def example_trace(seed: int = 3) -> dict:
    rng = random.Random(seed)
    spans = make_trace(rng, slow_p=0.0, err_p=0.0)
    cp = critical_path(spans)
    share = {}
    for sid, a, b in cp:
        share[spans[sid]["service"]] = share.get(spans[sid]["service"], 0) + (b - a)
    return {"spans": spans, "critical": cp, "share": share, "total": spans[0]["end"] - spans[0]["start"]}


def sampling(n: int = 50_000, head_rate: float = 0.01, seed: int = 0) -> dict:
    """Head sampling keeps a trace with probability ``head_rate``, decided at the first span.  Tail sampling waits
    until the trace ends, then keeps every error, every trace slower than 100 ms, and ``head_rate`` of the rest."""
    rng = random.Random(seed)
    head = {"kept": 0, "errors": 0, "slow": 0}
    tail = {"kept": 0, "errors": 0, "slow": 0}
    tot = {"errors": 0, "slow": 0}
    for _ in range(n):
        spans = make_trace(rng)
        err = any(s["error"] for s in spans)
        slow = spans[0]["end"] - spans[0]["start"] > 100
        tot["errors"] += err
        tot["slow"] += slow
        if rng.random() < head_rate:
            head["kept"] += 1
            head["errors"] += err
            head["slow"] += slow
        if err or slow or rng.random() < head_rate:
            tail["kept"] += 1
            tail["errors"] += err
            tail["slow"] += slow
    return {"n": n, "head_rate": head_rate, "total": tot, "head": head, "tail": tail}


# ---------------------------------------------------------------- coordinated omission

def coordinated_omission(seconds: float = 200.0, rate: float = 100.0, service_ms: float = 1.0,
                         stall_every_s: float = 40.0, stall_s: float = 4.0) -> dict:
    """A server answers in ``service_ms`` but freezes for ``stall_s`` every ``stall_every_s``.  A closed-loop load
    generator meant to send ``rate`` requests a second waits for each answer before sending the next, so during a
    stall it records one long sample instead of hundreds.  The true latency of each request is measured from when it
    should have been sent."""
    period = 1.0 / rate
    svc = service_ms / 1000

    def server_free_at(t):
        k = math.floor(t / stall_every_s)
        s0 = k * stall_every_s + (stall_every_s - stall_s)
        return s0 + stall_s if s0 <= t < s0 + stall_s else t

    closed, true = [], []
    t_next, busy_until = 0.0, 0.0
    # closed loop: one outstanding request; the next send waits for the reply
    t = 0.0
    while t < seconds:
        start = server_free_at(max(t, busy_until))
        done = start + svc
        closed.append(done - t)
        busy_until = done
        t = max(t + period, done)
    # open loop (or corrected): requests at their intended times, queueing behind the stall
    busy_until = 0.0
    k = 0
    while (t_next := k * period) < seconds:
        start = server_free_at(max(t_next, busy_until))
        done = start + svc
        true.append(done - t_next)
        busy_until = done
        k += 1

    def q(xs, p):
        return float(np.quantile(np.array(xs) * 1000, p))

    out = {}
    for name, xs in (("closed loop", closed), ("true", true)):
        out[name] = {"n": len(xs), "p50": q(xs, 0.5), "p90": q(xs, 0.9), "p99": q(xs, 0.99), "p999": q(xs, 0.999),
                     "max": max(xs) * 1000, "mean": float(np.mean(xs)) * 1000}
    out["stalled_share"] = stall_s / stall_every_s
    return out


def mva(N: int, D: float, Z: float) -> dict:
    """Exact mean-value analysis of a closed system: N users, think time Z, one queue of service demand D."""
    R = 0.0
    q = 0.0
    for n in range(1, N + 1):
        R = D * (1 + q)
        X = n / (R + Z)
        q = X * R
    return {"N": N, "R": R, "X": X}


def open_closed(D: float = 0.01, Z: float = 1.0, Ns=(10, 50, 80, 90, 95, 100, 110, 150)) -> list[dict]:
    """Closed load: response time is bounded because users wait.  Open load at the same throughput: M/M/1 with
    R = D / (1 - X D), which blows up as the load nears capacity."""
    rows = []
    for N in Ns:
        c = mva(N, D, Z)
        rho = c["X"] * D
        R_open = D / (1 - rho) if rho < 1 else float("inf")
        rows.append({"N": N, "throughput": c["X"], "util": rho, "closed_R": c["R"], "open_R": R_open})
    return rows


# ---------------------------------------------------------------- regressions in CI

def change_point(n: int = 80, at: int = 52, shift: float = 0.03, noise: float = 0.02, perms: int = 2000,
                 seed: int = 2) -> dict:
    """Benchmark times (relative to 1.0) for ``n`` commits, ``shift`` slower from commit ``at`` on, with
    multiplicative noise.  A naive alert fires whenever a run is 5% above the previous one; change-point detection
    finds the split that best separates two means, and a permutation test gives its p-value."""
    rng = np.random.default_rng(seed)
    x = 1.0 + noise * rng.standard_normal(n)
    x[at:] += shift
    naive = [i for i in range(1, n) if x[i] > 1.05 * x[i - 1]]

    def best(v):
        c = np.cumsum(v)
        tot = c[-1]
        m = len(v)
        bestk, bests = None, -1.0
        for k in range(5, m - 5):
            a, b = c[k - 1] / k, (tot - c[k - 1]) / (m - k)
            s = k * (m - k) / m * (a - b) ** 2
            if s > bests:
                bestk, bests = k, s
        return bestk, bests

    k, s = best(x)
    exceed = sum(1 for _ in range(perms) if best(rng.permutation(x))[1] >= s)
    return {"series": x.tolist(), "at": at, "shift": shift, "noise": noise, "found": int(k), "p": (exceed + 1) / (perms + 1),
            "before": float(x[:k].mean()), "after": float(x[k:].mean()), "naive_alerts": naive}
