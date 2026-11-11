"""Case studies (Part 49): a URL shortener's ID space; a news feed's fan-out on write against on read over a
power-law follower graph, and the hybrid; a crawler's politeness-limited throughput and Bloom-filter dedup; ride-hail
dispatch, greedy against batched assignment; adaptive bitrate (buffer-based against MPC) with rebuffering; a
double-entry ledger with idempotent payments; operational transformation's convergence, and its failure without
transformation; and the Job at a million books a day."""

from __future__ import annotations

import hashlib
import math
import random

import numpy as np


# ---------------------------------------------------------------- URL shortener

def shortener(ns=(1e6, 1e9, 1e12), alphabet=62):
    if alphabet < 2 or any(n < 1 for n in ns):
        raise ValueError("need at least two symbols and positive link counts")
    rows = []
    for n in ns:
        L, capacity = 1, alphabet
        while capacity < n:
            L += 1
            capacity *= alphabet
        rows.append({"links": n, "length": L, "space": alphabet ** L})
    # truncated hashes: collisions among m links with k base62 characters
    coll = []
    for k in (6, 7, 8):
        space = alphabet ** k
        for m in (1e6, 1e8):
            coll.append({"chars": k, "links": m, "expected_collisions": m * m / (2 * space)})
    return {"rows": rows, "collisions": coll}


def base62(n):
    if not isinstance(n, int) or n < 0:
        raise ValueError("base62 IDs must be nonnegative integers")
    a = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    s = ""
    while True:
        n, r = divmod(n, 62)
        s = a[r] + s
        if n == 0:
            return s


# ---------------------------------------------------------------- news feed

def follower_graph(users=100_000, alpha=2.1, seed=0, cap=None):
    """Follower counts from a power law (a few celebrities with millions, most with dozens), scaled to the user
    count; followee counts are the column sums of the same graph, so both fan-outs are consistent."""
    rng = np.random.default_rng(seed)
    f = np.floor((rng.pareto(alpha - 1, users) + 1) * 20).astype(np.int64)
    f = np.minimum(f, cap or users - 1)
    return f


def feed_cost(users=100_000, posts_per_user_day=0.5, reads_per_user_day=20, threshold=None, seed=0):
    """Fan-out on write: each post is written into every follower's timeline (cost = followers).  Fan-out on read:
    each timeline read gathers from every followee (cost = followees, about the mean follower count).  The hybrid
    pushes posts of users under the threshold and pulls the rest at read time."""
    f = follower_graph(users, seed=seed)
    mean_followees = f.mean()
    posts = posts_per_user_day * users
    reads = reads_per_user_day * users
    write_all = posts_per_user_day * f.sum()
    read_all = reads * mean_followees
    out = {"users": users, "max_followers": int(f.max()), "median_followers": float(np.median(f)),
           "mean_followers": float(mean_followees), "push_writes": float(write_all), "pull_reads": float(read_all)}
    rows = []
    for th in (threshold,) if threshold is not None else (100, 1_000, 10_000, 10 ** 9):
        celeb = f >= th
        push = posts_per_user_day * f[~celeb].sum()
        # reads must pull from the celebrities each user follows: on average followees * share of edges to celebs
        share = f[celeb].sum() / f.sum()
        pull = reads * mean_followees * share
        rows.append({"threshold": th, "celebrities": int(celeb.sum()), "push_writes": float(push),
                     "pull_reads": float(pull), "total": float(push + pull),
                     "max_fanout_per_post": int(f[~celeb].max()) if (~celeb).any() else 0})
    out["hybrid"] = rows
    out["posts"] = posts
    out["reads"] = reads
    return out


def celebrity_post(f_max, rate_per_server=50_000):
    return {"followers": f_max, "seconds_on_one_server": f_max / rate_per_server}


# ---------------------------------------------------------------- crawler

def crawler(pages=1e9, days=30, hosts=10_000_000, delay_s=1.0, page_kb=100, workers_per_machine=500,
            fetch_ms=500):
    rate = pages / (days * 86400)
    concurrent = rate * fetch_ms / 1000
    machines = concurrent / workers_per_machine
    bandwidth = rate * page_kb * 1000 * 8 / 1e9
    per_host_max = 1 / delay_s
    bloom_bits = -pages * math.log(0.01) / (math.log(2) ** 2)
    return {"pages": pages, "days": days, "pages_per_second": rate, "concurrent_fetches": concurrent,
            "machines": machines, "gbit_per_s": bandwidth, "polite_host_rate": per_host_max,
            "hosts_needed_busy": rate / per_host_max, "bloom_bytes_1pct": bloom_bits / 8,
            "bloom_bits_per_url": bloom_bits / pages}


def bloom_check(n=200_000, bits_per=9.6, seed=1):
    m = int(n * bits_per)
    k = max(1, round(bits_per * math.log(2)))
    arr = np.zeros(m, dtype=bool)

    def idx(s):
        h = hashlib.blake2b(s.encode(), digest_size=16).digest()
        a, b = int.from_bytes(h[:8], "big"), int.from_bytes(h[8:], "big")
        return [(a + i * b) % m for i in range(k)]
    for i in range(n):
        arr[idx(f"https://site{i % 997}.example/page{i}")] = True
    fp = sum(1 for i in range(20_000) if all(arr[j] for j in idx(f"https://new{i}.example/x")))
    return {"urls": n, "bits_per_url": bits_per, "hashes": k, "false_positive": fp / 20_000,
            "theory": (1 - math.exp(-k * n / m)) ** k}


# ---------------------------------------------------------------- ride-hailing dispatch

def dispatch(riders=60, drivers=70, rounds=200, seed=2, size=10.0):
    """Riders and drivers at random points in a city; greedy assigns each rider, in arrival order, its nearest free
    driver; batched matching collects riders for a short window and solves the assignment problem (Hungarian
    algorithm, Part 18).  Mean and worst pickup distance."""
    from scipy.optimize import linear_sum_assignment
    rng = np.random.default_rng(seed)
    g, b, gw, bw = [], [], [], []
    for _ in range(rounds):
        R = rng.uniform(0, size, (riders, 2))
        D = rng.uniform(0, size, (drivers, 2))
        C = np.sqrt(((R[:, None, :] - D[None, :, :]) ** 2).sum(-1))
        free = np.ones(drivers, bool)
        dist = []
        for i in range(riders):
            j = np.argmin(np.where(free, C[i], np.inf))
            free[j] = False
            dist.append(C[i, j])
        r, c = linear_sum_assignment(C)
        g.append(np.mean(dist))
        gw.append(np.max(dist))
        b.append(C[r, c].mean())
        bw.append(C[r, c].max())
    return {"riders": riders, "drivers": drivers, "greedy_mean": float(np.mean(g)), "batched_mean": float(np.mean(b)),
            "greedy_worst": float(np.mean(gw)), "batched_worst": float(np.mean(bw)), "city_km": size}


# ---------------------------------------------------------------- adaptive bitrate

LADDER = [0.3, 0.75, 1.2, 1.85, 2.85, 4.3]     # Mbit/s, a typical encoding ladder (illustrative)


def throughput_trace(seconds=600, seed=3):
    """A Markov-modulated bandwidth trace: good, fair and poor states with noise (Mbit/s per second)."""
    rng = random.Random(seed)
    means = {"good": 5.0, "fair": 2.2, "poor": 0.7}
    state, out = "good", []
    for _ in range(seconds):
        if rng.random() < 0.03:
            state = rng.choice([s for s in means if s != state])
        out.append(max(0.1, rng.gauss(means[state], means[state] * 0.25)))
    return out


def abr(policy, trace, seg=2.0, max_buf=30.0, horizon=5, startup=2):
    """Play segments of `seg` seconds.  Buffer-based (Huang et al. 2014): choose the bitrate from the buffer level
    alone, linearly between a reservoir and a cushion.  Rate-based: the highest bitrate under the harmonic mean of the
    last five throughputs.  MPC (Yin et al. 2015): choose the next bitrate maximizing quality minus rebuffering and
    switching penalties over a lookahead of `horizon` segments, using the harmonic-mean prediction discounted by the
    recent worst error (RobustMPC)."""
    t, buf, played, rebuf, switches, last = 0.0, 0.0, 0, 0.0, 0, None
    history, quality, errors = [], [], []
    n_seg = int(len(trace) * 0.9 / seg)
    tl = []
    for s in range(n_seg):
        hm = len(history[-5:]) / sum(1 / x for x in history[-5:]) if history else 1.0
        if policy == "mpc" and errors:              # RobustMPC: discount by the recent worst prediction error
            hm = hm / (1 + max(errors[-5:]))
        predicted = hm
        if policy == "buffer":
            res, cush = 5.0, 20.0
            frac = min(1.0, max(0.0, (buf - res) / (cush - res)))
            q = int(frac * (len(LADDER) - 1))
        elif policy == "rate":
            q = max([i for i, r in enumerate(LADDER) if r <= hm] or [0])
        else:
            best, q = -1e9, 0
            for first in range(len(LADDER)):
                b, score, prev = buf, 0.0, last if last is not None else first
                for k in range(horizon):
                    r = LADDER[first]
                    dl = r * seg / max(hm, 0.1)
                    stall = max(0.0, dl - b)
                    b = max(0.0, b - dl) + seg
                    score += r - 4.3 * stall - abs(r - LADDER[prev])     # Yin et al.'s QoE, Mbit/s
                    prev = first
                if score > best:
                    best, q = score, first
        r = LADDER[q]
        size = r * seg
        dl, got = 0.0, 0.0
        while got < size:
            bw = trace[min(int(t + dl), len(trace) - 1)]
            step = min(1.0, (size - got) / bw)
            got += bw * step
            dl += step
        history.append(size / dl)
        errors.append(max(0.0, (predicted - size / dl) / (size / dl)))
        if s >= startup:
            stall = max(0.0, dl - buf)
            rebuf += stall
        buf = max(0.0, buf - dl) + seg
        if buf > max_buf:
            t += buf - max_buf
            buf = max_buf
        t += dl
        if last is not None and q != last:
            switches += 1
        last = q
        quality.append(r)
        tl.append((t, buf, r))
        played += 1
    return {"policy": policy, "mean_bitrate": sum(quality) / len(quality), "rebuffer_s": rebuf,
            "switches": switches, "segments": played, "timeline": tl[::3]}


def abr_experiment(seeds=(3, 4, 5, 6, 7)):
    out = {p: {"mean_bitrate": 0.0, "rebuffer_s": 0.0, "switches": 0.0} for p in ("rate", "buffer", "mpc")}
    tl = {}
    for s in seeds:
        tr = throughput_trace(seed=s)
        for p in out:
            r = abr(p, tr)
            for k in ("mean_bitrate", "rebuffer_s", "switches"):
                out[p][k] += r[k] / len(seeds)
            if s == seeds[0]:
                tl[p] = r["timeline"]
    tr = throughput_trace(seed=seeds[0])
    return {"policies": out, "timelines": tl, "trace": tr[::3], "ladder": LADDER}


# ---------------------------------------------------------------- payments

def ledger(n=5000, fail=0.05, retry=0.3, seed=4, idempotent=True):
    """Payments move money between accounts as balanced journal entries (debits = credits).  The client times out
    on some requests and retries; with idempotency keys the retry returns the first result.  Checks the invariant
    sum(balances) = 0 and the number of double charges."""
    rng = random.Random(seed)
    bal = {"customer": 0, "merchant": 0, "fees": 0, "bank": 0}
    entries, seen, double = [], {}, 0
    for i in range(n):
        amount = rng.randrange(100, 10_000)
        key = f"pay-{i}"
        attempts = 1 + (1 if rng.random() < retry else 0)
        for _ in range(attempts):
            if idempotent and key in seen:
                continue
            if rng.random() < fail:
                continue                       # declined: nothing posted
            fee = amount * 3 // 100
            lines = [("customer", -amount), ("merchant", amount - fee), ("fees", fee)]
            assert sum(v for _, v in lines) == 0
            for a, v in lines:
                bal[a] += v
            if key in seen:
                double += 1
            seen[key] = True
            entries.append((key, lines))
    return {"payments": n, "entries": len(entries), "double_charges": double, "sum": sum(bal.values()),
            "balances": bal, "idempotent": idempotent}


# ---------------------------------------------------------------- operational transformation

def transform(op, other, prio):
    """Transform op = (kind, pos, ch) against a concurrent `other` already applied (Ellis and Gibbs style, with the
    tie broken by site priority)."""
    k, p, c = op
    ko, po, _ = other
    if ko == "ins":
        if po < p or (po == p and (prio or k == "del")):   # a delete at the same index targets the old character
            p += 1
    else:
        if po < p:
            p -= 1
        elif po == p and k == "del":
            return None            # both deleted the same character
    return (k, p, c)


def apply(s, op):
    if op is None:
        return s
    k, p, c = op
    if k == "ins":
        return s[:p] + c + s[p:]
    return s[:p] + s[p + 1:] if p < len(s) else s


def ot_experiment(trials=5000, seed=5, start="the cat sat"):
    """Two sites each apply one random operation concurrently, then receive the other's: with transformation both
    end equal (TP1); applying the remote operation unchanged diverges."""
    rng = random.Random(seed)
    ok_t = ok_n = 0
    example = None
    for _ in range(trials):
        def rnd():
            if not start or rng.random() < 0.6:
                return ("ins", rng.randrange(len(start) + 1), rng.choice("xyz"))
            return ("del", rng.randrange(len(start)), "")
        a, b = rnd(), rnd()
        sa = apply(apply(start, a), transform(b, a, False))
        sb = apply(apply(start, b), transform(a, b, True))
        ok_t += sa == sb
        na, nb = apply(apply(start, a), b), apply(apply(start, b), a)
        ok_n += na == nb
        if na != nb and example is None and a[0] == b[0] == "ins":
            example = {"start": start, "a": a, "b": b, "naive": [na, nb], "transformed": [sa, sb]}
    return {"trials": trials, "converged_transformed": ok_t / trials, "converged_naive": ok_n / trials,
            "example": example}


# ---------------------------------------------------------------- metrics cardinality

def cardinality(labels=(("service", 50), ("endpoint", 40), ("status", 6), ("region", 8), ("pod", 200))):
    """Time series = product of label cardinalities; adding a user-id label multiplies it by the users."""
    rows, n = [], 1
    for name, c in labels:
        n *= c
        rows.append({"label": name, "values": c, "series": n})
    return {"rows": rows, "with_user_id": n * 1_000_000}


# ---------------------------------------------------------------- the Job at a million books a day

def job_million(books_per_day=1_000_000, read_ratio=20, work_s=0.08, cache_hit=0.6, servers=None,
                cost_per_server_hour=0.096, seed=6):
    """Uploads count a new book; reads ask for a known book's top words (cached with the given hit rate).  Size the
    workers for 60% utilization at a peak of three times the mean, then simulate an hour at the peak."""
    from explainer.cs.design.keys import job_service  # noqa: F401
    up = books_per_day / 86400
    rd = up * read_ratio
    peak = 3 * (up + rd * (1 - cache_hit))
    work_per_s = peak * work_s
    servers = servers or math.ceil(work_per_s / 0.6)
    rng = random.Random(seed)
    t, free, lat = 0.0, [0.0] * servers, []
    for _ in range(60_000):
        t += rng.expovariate(peak)
        k = min(range(servers), key=lambda i: free[i])
        start = max(t, free[k])
        free[k] = start + rng.expovariate(1 / work_s)
        lat.append(free[k] - t)
    lat.sort()
    monthly = servers * cost_per_server_hour * 24 * 30
    return {"uploads_per_s": up, "reads_per_s": rd, "peak_work_rps": peak, "servers": servers,
            "p50_ms": 1000 * lat[len(lat) // 2], "p99_ms": 1000 * lat[int(0.99 * len(lat))],
            "monthly_dollars": monthly, "dollars_per_book": monthly / (books_per_day * 30),
            "storage_tb_per_year": books_per_day * 365 * 600_000 / 1e12, "cache_hit": cache_hit}
