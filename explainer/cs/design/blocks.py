"""Building blocks of system design (Part 48): Maglev hashing (Eisenbud et al. 2016) against a hash ring, measuring
disruption when a backend leaves; caches (LRU, LFU, a simplified W-TinyLFU with Count-Min admission) on Zipf traffic
against Che's approximation; cache stampedes with and without probabilistic early expiration (Vattani et al. 2015);
and rate limiters: a token bucket's conformance, and the sliding-window counter's error."""

from __future__ import annotations

import bisect
import hashlib
import math
import random
from collections import OrderedDict, defaultdict

import numpy as np


def h64(s: str, salt: str = "") -> int:
    return int.from_bytes(hashlib.blake2b((salt + s).encode(), digest_size=8).digest(), "big")


# ---------------------------------------------------------------- load balancing

def maglev_table(backends, M=65537):
    """Each backend gets a permutation of table slots (offset, skip from two hashes); backends take turns claiming
    their next preferred free slot until the table is full.  Every backend ends up with M/N slots, +-1."""
    N = len(backends)
    offset = [h64(b, "o") % M for b in backends]
    skip = [h64(b, "s") % (M - 1) + 1 for b in backends]
    nxt = [0] * N
    table = [-1] * M
    filled = 0
    while True:
        for i in range(N):
            c = (offset[i] + nxt[i] * skip[i]) % M
            while table[c] >= 0:
                nxt[i] += 1
                c = (offset[i] + nxt[i] * skip[i]) % M
            table[c] = i
            nxt[i] += 1
            filled += 1
            if filled == M:
                return table


def ring(backends, vnodes=100):
    pts = sorted((h64(f"{b}#{v}"), i) for i, b in enumerate(backends) for v in range(vnodes))
    return [p for p, _ in pts], [i for _, i in pts]


def ring_lookup(r, key):
    keys, owners = r
    k = h64(key)
    j = bisect.bisect(keys, k) % len(keys)
    return owners[j]


def disruption(n_backends=20, keys=50_000, M=65537, vnodes=100):
    """Remove one backend: the share of keys that move that were not on the removed backend (pure disruption), and
    the load spread, for Maglev and a ring with virtual nodes."""
    names = [f"b{i}" for i in range(n_backends)]
    names2 = names[:5] + names[6:]
    ks = [f"key{i}" for i in range(keys)]
    t1, t2 = maglev_table(names, M), maglev_table(names2, M)
    m1 = [names[t1[h64(k) % M]] for k in ks]
    m2 = [names2[t2[h64(k) % M]] for k in ks]
    r1, r2 = ring(names, vnodes), ring(names2, vnodes)
    g1 = [names[ring_lookup(r1, k)] for k in ks]
    g2 = [names2[ring_lookup(r2, k)] for k in ks]

    def stats(a, b):
        moved_other = sum(1 for x, y in zip(a, b) if x != y and x != "b5") / keys
        loads = defaultdict(int)
        for y in b:
            loads[y] += 1
        v = list(loads.values())
        return {"moved_needlessly": moved_other, "max_over_mean": max(v) / (keys / len(v))}
    return {"maglev": stats(m1, m2), "ring": stats(g1, g2), "removed_share": 1 / n_backends,
            "slots_per_backend": {"min": min(np.bincount(t1)), "max": max(np.bincount(t1))}}


# ---------------------------------------------------------------- caches

def zipf_trace(n=200_000, items=100_000, s=0.9, seed=0):
    rng = np.random.default_rng(seed)
    w = 1 / np.arange(1, items + 1) ** s
    p = w / w.sum()
    return rng.choice(items, size=n, p=p), p


def lru_hits(trace, size):
    c = OrderedDict()
    hits = 0
    for x in trace:
        if x in c:
            hits += 1
            c.move_to_end(x)
        else:
            c[x] = 1
            if len(c) > size:
                c.popitem(last=False)
    return hits / len(trace)


def lfu_hits(trace, size):
    """In-cache LFU (counts forgotten on eviction)."""
    import heapq
    cnt, heap, hits, t = {}, [], 0, 0
    for x in trace:
        t += 1
        if x in cnt:
            hits += 1
            cnt[x] += 1
            heapq.heappush(heap, (cnt[x], t, x))
        else:
            if len(cnt) >= size:
                while True:
                    f, _, y = heapq.heappop(heap)
                    if y in cnt and cnt[y] == f:
                        del cnt[y]
                        break
            cnt[x] = 1
            heapq.heappush(heap, (1, t, x))
    return hits / len(trace)


class CountMin:
    def __init__(self, w=4096, d=4, seed=1):
        self.w, self.d = w, d
        self.t = np.zeros((d, w), dtype=np.int32)
        self.salts = [seed * 1000 + i for i in range(d)]
        self.adds = 0

    def idx(self, x):
        return [hash((s, int(x))) % self.w for s in self.salts]

    def add(self, x):
        for r, j in enumerate(self.idx(x)):
            self.t[r, j] += 1
        self.adds += 1
        if self.adds >= 10 * self.w:          # aging: halve every counter periodically
            self.t //= 2
            self.adds = 0

    def est(self, x):
        return min(self.t[r, j] for r, j in enumerate(self.idx(x)))


def tinylfu_hits(trace, size, window_frac=0.01):
    """W-TinyLFU, simplified: a small LRU window admits every item; an item evicted from the window enters the main
    LRU only if the Count-Min sketch says it is more frequent than the main cache's victim."""
    wsize = max(1, int(size * window_frac))
    msize = size - wsize
    win, main = OrderedDict(), OrderedDict()
    cm = CountMin(w=max(1024, 4 * size))
    hits = 0
    for x in trace:
        cm.add(x)
        if x in win:
            hits += 1
            win.move_to_end(x)
            continue
        if x in main:
            hits += 1
            main.move_to_end(x)
            continue
        win[x] = 1
        if len(win) > wsize:
            cand, _ = win.popitem(last=False)
            if len(main) < msize:
                main[cand] = 1
            else:
                victim = next(iter(main))
                if cm.est(cand) > cm.est(victim):
                    main.popitem(last=False)
                    main[cand] = 1
    return hits / len(trace)


def che(p, size):
    """Che's approximation for LRU under independent references: find the characteristic time T with
    sum_i (1 - exp(-p_i T)) = size; the hit rate is sum_i p_i (1 - exp(-p_i T))."""
    lo, hi = 0.0, 1.0
    while np.sum(1 - np.exp(-p * hi)) < size:
        hi *= 2
    for _ in range(80):
        mid = (lo + hi) / 2
        if np.sum(1 - np.exp(-p * mid)) < size:
            lo = mid
        else:
            hi = mid
    T = (lo + hi) / 2
    return float(np.sum(p * (1 - np.exp(-p * T))))


def cache_experiment(sizes=(100, 300, 1000, 3000, 10000), n=200_000, items=100_000, s=0.9):
    trace, p = zipf_trace(n, items, s)
    tr = trace.tolist()
    rows = []
    for c in sizes:
        rows.append({"size": c, "lru": lru_hits(tr, c), "lfu": lfu_hits(tr, c), "tinylfu": tinylfu_hits(tr, c),
                     "che": che(p, c), "optimal_static": float(np.sort(p)[::-1][:c].sum())})
    return {"items": items, "requests": n, "zipf_s": s, "rows": rows}


def scan_resistance(size=1000, n=100_000, items=50_000, seed=2):
    """Zipf traffic interrupted by a one-off scan of 20,000 cold items (a batch job reading everything).  The textbook
    story is that LRU flushes its hot set and TinyLFU refuses the scan; with this trace and cache size the drops
    are almost entirely the scan's own misses, for both policies, which the Caching scene says."""
    trace, _ = zipf_trace(n, items, 0.9, seed)
    tr = trace.tolist()
    scan = list(range(items, items + 20_000))
    mixed = tr[:n // 2] + scan + tr[n // 2:]
    return {"lru": lru_hits(mixed, size), "tinylfu": tinylfu_hits(mixed, size),
            "lru_clean": lru_hits(tr, size), "tinylfu_clean": tinylfu_hits(tr, size)}


# ---------------------------------------------------------------- stampedes

def stampede(rate=200.0, ttl=60.0, recompute=2.0, beta=1.0, horizon=300.0, seed=3, early=False):
    """One hot key requested `rate` times a second, cached for ttl seconds, taking `recompute` seconds to rebuild.
    Without protection, every request that misses while the value is being rebuilt also rebuilds it.  With XFetch
    (Vattani, Chierichetti and Lowenstein 2015), each request recomputes early with probability rising as expiry
    nears: if now - recompute * beta * ln(U) >= expiry."""
    rng = random.Random(seed)
    t, expiry = 0.0, ttl
    rebuild_done = None          # when the current (unprotected) rebuild finishes
    starts = []
    misses = 0
    while t < horizon:
        t += rng.expovariate(rate)
        if rebuild_done is not None and t >= rebuild_done:
            expiry, rebuild_done = rebuild_done + ttl, None
        if t < expiry:
            if early and rebuild_done is None and t - recompute * beta * math.log(1 - rng.random()) >= expiry:
                starts.append(t)                 # one request refreshes early; everyone else still hits
                rebuild_done = t + recompute
                expiry = rebuild_done            # the old value stays valid until the new one lands
            continue
        misses += 1                              # expired: this request rebuilds the value itself
        starts.append(t)
        if rebuild_done is None:
            rebuild_done = t + recompute
    peak = 0
    for i in range(len(starts)):
        j = bisect.bisect(starts, starts[i] + 1.0)
        peak = max(peak, j - i)
    return {"early": early, "recomputations": len(starts), "misses": misses, "peak_per_second": peak,
            "expiries": int(horizon // (ttl + recompute))}


# ---------------------------------------------------------------- rate limiting

def token_bucket(arrivals, rate, burst):
    """Allow a request if a token is available; tokens refill at `rate` per second up to `burst`.  Any allowed
    sequence satisfies A(t, t + s) <= burst + rate * s, the (sigma, rho) envelope."""
    tokens, last, out = burst, arrivals[0] if arrivals else 0.0, []
    for t in arrivals:
        tokens = min(burst, tokens + (t - last) * rate)
        last = t
        if tokens >= 1:
            tokens -= 1
            out.append(t)
    return out


def envelope_ok(allowed, rate, burst):
    worst = 0.0
    j = 0
    for i, t in enumerate(allowed):
        while allowed[j] < t - 10.0:
            j += 1
        for k in range(j, i + 1):
            s = t - allowed[k]
            worst = max(worst, (i - k + 1) - (burst + rate * s))
    return worst <= 1e-9, worst


def limiter_experiment(seed=4, limit=100, window=60.0, horizon=600.0):
    """Bursty traffic: the token bucket's admitted counts stay within its envelope; the fixed window admits up to
    twice the limit across a boundary; the sliding-window counter (weighted previous window) against an exact
    sliding log: its error."""
    rng = random.Random(seed)
    arr = []
    t = 0.0
    while t < horizon:
        rate = 4.0 if int(t / 30) % 3 == 0 else 0.8
        t += rng.expovariate(rate)
        arr.append(t)
    tb = token_bucket(arr, rate=limit / window, burst=20)
    ok, worst = envelope_ok(tb, limit / window, 20)
    # fixed windows
    fixed, counts = [], defaultdict(int)
    for x in arr:
        w = int(x // window)
        if counts[w] < limit:
            counts[w] += 1
            fixed.append(x)
    worst_fixed = max(sum(1 for y in fixed if x - window < y <= x) for x in fixed)
    # the sliding-window counter's estimate of requests in the last window against the exact count (all requests)
    errs = []
    prev_c = cur_c = cur_w = 0
    j = 0
    for i, x in enumerate(arr):
        while arr[j] <= x - window:
            j += 1
        exact = i - j + 1
        w = int(x // window)
        if w != cur_w:
            prev_c = cur_c if w == cur_w + 1 else 0
            cur_c, cur_w = 0, w
        cur_c += 1
        frac = (x % window) / window
        est = prev_c * (1 - frac) + cur_c
        errs.append((est - exact) / max(1, exact))
    errs = np.array(errs)
    return {"requests": len(arr), "bucket_allowed": len(tb), "bucket_envelope_ok": ok,
            "fixed_allowed": len(fixed), "fixed_worst_window": worst_fixed, "limit": limit,
            "sliding_mean_rel_error": float(np.mean(np.abs(errs))), "sliding_max_rel_error": float(np.max(np.abs(errs)))}
