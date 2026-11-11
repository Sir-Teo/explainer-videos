"""Keys and the Job as a service (Part 48): UUIDv4 collision odds by the birthday bound; Snowflake-style and UUIDv7
time-ordered IDs; B-tree page splits and pages touched for random against time-ordered keys; Z-order (Morton) and
Hilbert curves, their locality, and the key ranges a map rectangle needs; estimation worksheets; and a load test of
"upload a book, get its top words" with and without a cache."""

from __future__ import annotations

import math
import random
import uuid


# ---------------------------------------------------------------- unique IDs

def birthday(bits=122, ns=(1e9, 1e12, 1e15, 2.71e18)):
    """P(any collision) ~ 1 - exp(-n(n-1) / 2^(bits+1)); UUIDv4 has 122 random bits."""
    if bits < 1 or any(n < 0 for n in ns):
        raise ValueError("need positive random bits and nonnegative ID counts")
    return [{"n": n, "p": -math.expm1(-(n * max(0, n - 1)) / 2 ** (bits + 1))} for n in ns]


def snowflake(ts_ms: int, machine: int, seq: int, epoch=1288834974657):
    """41 bits of milliseconds since an epoch, 10 bits of machine, 12 bits of sequence (Twitter, 2010)."""
    if not (0 <= ts_ms - epoch < 1 << 41 and 0 <= machine < 1 << 10 and 0 <= seq < 1 << 12):
        raise ValueError("timestamp, machine, and sequence must fit their Snowflake fields")
    return ((ts_ms - epoch) << 22) | (machine << 12) | seq


def uuid7(ts_ms: int, rng: random.Random):
    if not 0 <= ts_ms < 1 << 48:
        raise ValueError("UUIDv7 timestamp must fit 48 bits")
    rand = rng.getrandbits(74)
    v = (ts_ms << 80) | (0x7 << 76) | ((rand >> 62) << 64) | (0b10 << 62) | (rand & ((1 << 62) - 1))
    return uuid.UUID(int=v)


def btree_inserts(n=200_000, page=100, seed=0, ordered=False):
    """Insert keys into a B+ tree's leaf level (sorted pages of `page` keys, split in half when full): random keys
    split pages all over the tree and leave them partly full (about 69% here, near the ln 2 of theory); time-ordered keys only touch the rightmost page."""
    import bisect
    rng = random.Random(seed)
    firsts = [0]               # first key of each page
    pages = [[]]
    splits = 0
    touched = set()
    recent = set()
    for i in range(n):
        k = i if ordered else rng.getrandbits(62)
        j = max(0, bisect.bisect(firsts, k) - 1)
        touched.add(id(pages[j]))
        bisect.insort(pages[j], k)
        if i >= n - 10_000:
            recent.add(j if ordered else firsts[j])
        if len(pages[j]) > page:
            # appending at the right edge: start a new page with just the new key (what real engines do);
            # otherwise split the page in half
            half = page if (ordered and j == len(pages) - 1) else len(pages[j]) // 2
            new = pages[j][half:]
            pages[j] = pages[j][:half]
            pages.insert(j + 1, new)
            firsts.insert(j + 1, new[0])
            splits += 1
        if j == 0 and pages[0]:
            firsts[0] = min(firsts[0], pages[0][0])
    fill = n / (len(pages) * page)
    return {"ordered": ordered, "pages": len(pages), "splits": splits, "fill": fill,
            "pages_touched_last_10000": len(recent)}


def id_examples():
    rng = random.Random(1)
    ts = 1_793_000_000_000
    sf = [snowflake(ts, 7, 0), snowflake(ts, 7, 1), snowflake(ts + 1, 7, 0)]   # two in one ms, one in the next
    u7 = [str(uuid7(ts + k, rng)) for k in range(3)]
    u4 = [str(uuid.UUID(int=rng.getrandbits(128), version=4)) for _ in range(3)]
    return {"snowflake": sf, "snowflake_bin": [format(x, "064b") for x in sf], "uuid7": u7, "uuid4": u4,
            "sorted_uuid7": u7 == sorted(u7)}


# ---------------------------------------------------------------- space-filling curves

def morton(x, y, bits=8):
    z = 0
    for i in range(bits):
        z |= ((x >> i) & 1) << (2 * i) | ((y >> i) & 1) << (2 * i + 1)
    return z


def hilbert(x, y, bits=8):
    """Distance along the Hilbert curve of order `bits` (the classic rotate-and-flip algorithm)."""
    n = 1 << bits
    d = 0
    s = n >> 1
    while s:
        rx = 1 if x & s else 0
        ry = 1 if y & s else 0
        d += s * s * ((3 * rx) ^ ry)
        if ry == 0:
            if rx == 1:
                x, y = s - 1 - x, s - 1 - y
            x, y = y, x
        s >>= 1
    return d


def curve_points(bits=3):
    n = 1 << bits
    pts = [(x, y) for x in range(n) for y in range(n)]
    return {"morton": sorted(pts, key=lambda p: morton(*p, bits)), "hilbert": sorted(pts, key=lambda p: hilbert(*p, bits))}


def locality(bits=8, samples=20_000, seed=2):
    """For random pairs of neighbouring cells: how far apart they are along each curve (median and 99th
    percentile), and for random 16x16 query rectangles, how many contiguous key ranges cover them."""
    rng = random.Random(seed)
    n = 1 << bits
    out = {}
    for name, f in (("z-order", morton), ("hilbert", hilbert)):
        ds = []
        for _ in range(samples):
            x, y = rng.randrange(n - 1), rng.randrange(n - 1)
            dx, dy = (1, 0) if rng.random() < 0.5 else (0, 1)
            ds.append(abs(f(x, y, bits) - f(x + dx, y + dy, bits)))
        ds.sort()
        ranges = []
        for _ in range(300):
            x0, y0 = rng.randrange(n - 16), rng.randrange(n - 16)
            keys = sorted(f(x, y, bits) for x in range(x0, x0 + 16) for y in range(y0, y0 + 16))
            ranges.append(1 + sum(1 for a, b in zip(keys, keys[1:]) if b != a + 1))
        out[name] = {"median_gap": ds[len(ds) // 2], "p99_gap": ds[int(0.99 * len(ds))],
                     "mean_ranges_16x16": sum(ranges) / len(ranges), "max_ranges": max(ranges)}
    return out


def geohash(lat, lon, chars=7):
    """Base-32 geohash: interleave longitude and latitude bisection bits (Z-order on the globe)."""
    alphabet = "0123456789bcdefghjkmnpqrstuvwxyz"
    lat_r, lon_r = [-90.0, 90.0], [-180.0, 180.0]
    bits, even, out, ch = 0, True, [], 0
    while len(out) < chars:
        r, v = (lon_r, lon) if even else (lat_r, lat)
        mid = (r[0] + r[1]) / 2
        if v >= mid:
            ch = ch * 2 + 1
            r[0] = mid
        else:
            ch *= 2
            r[1] = mid
        even = not even
        bits += 1
        if bits == 5:
            out.append(alphabet[ch])
            bits, ch = 0, 0
    return "".join(out)


# ---------------------------------------------------------------- estimation

def napkin(dau=10_000_000, actions_per_user=20, peak=3.0, read_write=10, obj_bytes=2_000, years=5, replicas=3):
    """A worksheet: daily active users to queries per second, peak, writes, storage and bandwidth."""
    per_day = dau * actions_per_user
    qps = per_day / 86_400
    writes = per_day / (read_write + 1)
    storage = writes * obj_bytes * 365 * years * replicas
    return {"dau": dau, "requests_per_day": per_day, "avg_qps": qps, "peak_qps": qps * peak,
            "writes_per_day": writes, "write_qps": writes / 86_400, "storage_bytes": storage,
            "read_bandwidth_Bps": qps * peak * obj_bytes * read_write / (read_write + 1), "years": years,
            "replicas": replicas}


# ---------------------------------------------------------------- the Job as a service

def job_service(qps_list=(5, 10, 20, 40, 60, 80, 95), servers=8, work_s=0.08, cache_size=0, seed=3, n=30_000,
                books=3000):
    """Requests "top words of book b", b drawn by Zipf popularity from `books` uploaded books, each costing work_s
    seconds of one server (exponential), served by `servers` workers from one queue; with an LRU cache of
    cache_size results, a hit costs 1 ms.  Returns hit rate, p50 and p99 of response time against offered load."""
    from collections import OrderedDict
    rng = random.Random(seed)
    w = [1 / (k + 1) for k in range(books)]
    rows = []
    for qps in qps_list:
        t = 0.0
        free = [0.0] * servers
        cache = OrderedDict()
        lat, hits = [], 0
        for _ in range(n):
            t += rng.expovariate(qps)
            b = rng.choices(range(books), weights=w)[0]
            if cache_size and b in cache:
                cache.move_to_end(b)
                hits += 1
                lat.append(0.001)
                continue
            cost = rng.expovariate(1 / work_s)
            k = min(range(servers), key=lambda i: free[i])
            start = max(t, free[k])
            free[k] = start + cost
            lat.append(free[k] - t)
            if cache_size:
                cache[b] = 1
                if len(cache) > cache_size:
                    cache.popitem(last=False)
        lat.sort()
        rows.append({"qps": qps, "utilization": qps * work_s * (1 - hits / n) / servers, "hit_rate": hits / n,
                     "p50_ms": 1000 * lat[n // 2], "p99_ms": 1000 * lat[int(0.99 * n)]})
    return {"servers": servers, "work_ms": work_s * 1000, "cache_size": cache_size, "books": books, "rows": rows}


# ---------------------------------------------------------------- learned indexes

def learned_index(keys, eps=64):
    """A piecewise-linear model of position against key with maximum error eps (the shrinking-cone greedy of the
    PGM-index, Ferragina and Vinciguerra 2020): each segment predicts a key's position to within eps, so a lookup is
    one model evaluation plus a binary search over 2 eps + 1 slots."""
    segs = []
    i, n = 0, len(keys)
    while i < n:
        x0, y0 = keys[i], i
        lo, hi = -math.inf, math.inf
        j = i + 1
        while j < n:
            dx = keys[j] - x0
            if dx == 0:
                j += 1
                continue
            s_lo, s_hi = (j - eps - y0) / dx, (j + eps - y0) / dx
            nlo, nhi = max(lo, s_lo), min(hi, s_hi)
            if nlo > nhi:
                break
            lo, hi = nlo, nhi
            j += 1
        slope = (lo + hi) / 2 if lo > -math.inf else 0.0
        segs.append((x0, y0, slope))
        i = j
    return segs


def learned_experiment(n=1_000_000, seed=4, eps_list=(8, 32, 128, 512)):
    """Keys: event timestamps with bursty gaps.  Segments needed and bytes, against a B+ tree's inner nodes, and
    the comparisons per lookup."""
    rng = random.Random(seed)
    t, keys = 0, []
    for k in range(n):
        t += rng.expovariate(1.0) * (50 if (k // 10_000) % 7 == 0 else 1)
        keys.append(t)
    rows = []
    for eps in eps_list:
        segs = learned_index(keys, eps)
        rows.append({"eps": eps, "segments": len(segs), "bytes": 24 * len(segs),
                     "search_steps": math.ceil(math.log2(2 * eps + 1))})
    fan = 256
    level, inner, depth = math.ceil(n / fan), 0, 0      # leaves hold the keys; count the nodes above them
    while level > 1:
        level = math.ceil(level / fan)
        inner += level
        depth += 1
    return {"keys": n, "rows": rows, "btree_leaves": math.ceil(n / fan), "btree_inner_nodes": inner,
            "btree_inner_bytes": inner * fan * 16, "btree_inner_levels": depth,
            "btree_steps": (depth + 1) * 8}
