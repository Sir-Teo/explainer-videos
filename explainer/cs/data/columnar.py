"""Columnar storage (Part 46): Parquet-style encodings (plain, dictionary, run-length/bit-packing hybrid, delta) on
the novels' words; row groups with min/max statistics and the row groups a filter can skip; Dremel's repetition and
definition levels for nested records; and the cost of distributed joins with skew."""

from __future__ import annotations

import gzip
import math
import random
import struct
from collections import Counter


def plain_strings(xs):
    return b"".join(struct.pack("<I", len(x.encode())) + x.encode() for x in xs)


def bitpack(vals, width):
    acc, nbits, out = 0, 0, bytearray()
    for v in vals:
        acc |= v << nbits
        nbits += width
        while nbits >= 8:
            out.append(acc & 0xFF)
            acc >>= 8
            nbits -= 8
    if nbits:
        out.append(acc)
    return bytes(out)


def rle_hybrid(vals, width):
    """Runs of 8 or more equal values become (count, value); everything else is bit-packed, as in Parquet's
    RLE/bit-packing hybrid.  Returns encoded size in bytes (headers as varints, approximately one byte)."""
    size, i, n = 0, 0, len(vals)
    lit = []
    while i < n:
        j = i
        while j < n and vals[j] == vals[i]:
            j += 1
        if j - i >= 8:
            if lit:
                size += 1 + math.ceil(len(lit) * width / 8)
                lit = []
            size += 1 + math.ceil(width / 8)
        else:
            lit += vals[i:j]
        i = j
    if lit:
        size += 1 + math.ceil(len(lit) * width / 8)
    return size


def delta_ints(vals):
    """Delta encoding of an integer column: store differences, bit-packed at the width of the largest one."""
    if not vals:
        return 0
    d = [b - a for a, b in zip(vals, vals[1:])]
    lo = min(d) if d else 0
    width = max(1, max((x - lo).bit_length() for x in d)) if d else 1
    return 8 + math.ceil(len(d) * width / 8)


def encode_words(words):
    """Sizes of one column of words under each encoding, with and without a general-purpose compressor after."""
    plain = plain_strings(words)
    vocab = {w: i for i, (w, _) in enumerate(Counter(words).most_common())}
    idx = [vocab[w] for w in words]
    width = max(1, (len(vocab) - 1).bit_length())
    dict_page = plain_strings(list(vocab))
    packed = bitpack(idx, width)
    rle = rle_hybrid(idx, width)
    srt = sorted(idx)
    rle_sorted = rle_hybrid(srt, width)
    return {"values": len(words), "distinct": len(vocab), "index_bits": width,
            "plain": len(plain), "plain_gzip": len(gzip.compress(plain, 6)),
            "dictionary": len(dict_page) + len(packed), "dictionary_gzip": len(dict_page) + len(
                gzip.compress(packed, 6)),
            "dict_rle": len(dict_page) + rle, "dict_rle_sorted": len(dict_page) + rle_sorted,
            "row_text_gzip": len(gzip.compress(" ".join(words).encode(), 6))}


def int_column(n=100_000, seed=0):
    """A timestamp column (increasing, small gaps): plain 8 bytes each against delta-encoded."""
    rng = random.Random(seed)
    t, vals = 1_700_000_000_000, []
    for _ in range(n):
        t += rng.randrange(0, 2000)
        vals.append(t)
    return {"values": n, "plain": 8 * n, "delta": delta_ints(vals)}


def pushdown(n=1_000_000, group=100_000, seed=1, lo=420_000, hi=430_000, sorted_=True):
    """Row groups with min/max statistics: a filter lo <= x < hi reads only groups whose range overlaps.  On a
    column sorted (or clustered) by x, almost all groups are skipped; on a random one, none are."""
    rng = random.Random(seed)
    xs = list(range(n)) if sorted_ else [rng.randrange(n) for _ in range(n)]
    groups = [xs[i:i + group] for i in range(0, n, group)]
    read = sum(1 for g in groups if min(g) < hi and max(g) >= lo)
    return {"groups": len(groups), "read": read, "sorted": sorted_}


# ---------------------------------------------------------------- Dremel

def dremel(records, path):
    """Repetition and definition levels for a repeated/optional path through nested records (Melnik et al. 2010).
    Records are nested dicts/lists; `path` is a list of (field, kind) with kind in required, optional, repeated.
    Returns (value, r, d) triples.  r: at which repeated level in the path this value repeats (0 = new record);
    d: how many optional or repeated fields along the path are actually present."""
    out = []

    def walk(node, depth, r, d):
        if depth == len(path):
            out.append((node, r, d))
            return
        field, kind = path[depth]
        child = node.get(field) if isinstance(node, dict) else None
        rep_level = sum(1 for _, k in path[:depth + 1] if k == "repeated")
        if kind == "repeated":
            items = child or []
            if not items:
                out.append((None, r, d))
                return
            for j, it in enumerate(items):
                walk(it, depth + 1, r if j == 0 else rep_level, d + 1)
        elif kind == "optional":
            if child is None:
                out.append((None, r, d))
            else:
                walk(child, depth + 1, r, d + 1)
        else:
            walk(child, depth + 1, r, d)
    for rec in records:
        walk(rec, 0, 0, 0)
    return out


def dremel_example():
    """Two books with chapters, each with repeated keywords; one chapter has none, one book has no chapters."""
    books = [
        {"title": "Moby-Dick", "chapters": [{"name": "Loomings", "keywords": ["sea", "whale"]},
                                            {"name": "The Carpet-Bag", "keywords": ["inn"]},
                                            {"name": "The Spouter-Inn", "keywords": []}]},
        {"title": "Notes", "chapters": []},
        {"title": "Emma", "chapters": [{"name": "Chapter I", "keywords": ["Highbury"]}]},
    ]
    path = [("chapters", "repeated"), ("keywords", "repeated")]
    trip = dremel(books, path)
    return {"records": books, "column": "chapters.keywords", "max_r": 2, "max_d": 2, "levels": trip}


def reassemble(levels, max_d=2):
    """Rebuild the nested lists of the column from its levels alone (the reader's side)."""
    recs = []
    for v, r, d in levels:
        if r == 0:
            recs.append([])
        if d == 0:
            continue
        if r <= 1:
            recs[-1].append([])
        if d == max_d:
            recs[-1][-1].append(v)
    return recs


# ---------------------------------------------------------------- distributed joins

def join_cost(big_rows=1e9, small_rows=1e6, row_bytes=100, workers=100):
    """Bytes moved over the network.  Broadcast: send the small table to every worker.  Shuffle hash join: send
    every row of both tables to the worker that owns its key's hash (all but 1/workers of them move)."""
    broadcast = small_rows * row_bytes * workers
    shuffle = (big_rows + small_rows) * row_bytes * (1 - 1 / workers)
    # broadcast = shuffle:  S N = (B + S)(1 - 1/N)  =>  S* = B (N - 1) / (N^2 - N + 1)
    crossover = big_rows * (workers - 1) / (workers * workers - workers + 1)
    return {"broadcast_bytes": broadcast, "shuffle_bytes": shuffle, "small_rows": small_rows, "big_rows": big_rows,
            "crossover_small_rows": crossover, "workers": workers}


def skew(workers=16, rows=200_000, hot_share=0.2, salt=8, seed=2):
    """Rows hashed to workers by key; one key holds hot_share of the rows.  The slowest worker sets the time.
    Salting splits the hot key over `salt` sub-keys (the small side is replicated to match)."""
    rng = random.Random(seed)
    keys = ["hot" if rng.random() < hot_share else f"k{rng.randrange(50_000)}" for _ in range(rows)]

    def loads(ks):
        c = [0] * workers
        for k in ks:
            c[hash(k) % workers] += 1
        return c
    plain = loads(keys)
    salted = loads([(k + f"#{rng.randrange(salt)}") if k == "hot" else k for k in keys])
    return {"workers": workers, "ideal": rows / workers, "max_plain": max(plain), "max_salted": max(salted),
            "slowdown_plain": max(plain) / (rows / workers), "slowdown_salted": max(salted) / (rows / workers)}


# ---------------------------------------------------------------- quantile sketches

class KLL:
    """A simplified KLL sketch (Karnin, Lang and Liberty 2016): levels of buffers; a full level is sorted and every
    other item (a random half) is promoted with double weight.  Space grows with the log of the stream."""

    def __init__(self, k=200, seed=0):
        self.k = k
        self.levels = [[]]
        self.rng = random.Random(seed)

    def cap(self, h):
        return max(2, int(self.k * (2 / 3) ** (len(self.levels) - 1 - h)))

    def add(self, x):
        self.levels[0].append(x)
        h = 0
        while len(self.levels[h]) >= self.cap(h):
            buf = sorted(self.levels[h])
            off = self.rng.randrange(2)
            if h + 1 == len(self.levels):
                self.levels.append([])
            self.levels[h + 1] += buf[off::2]
            self.levels[h] = []
            h += 1
            if h >= len(self.levels):
                break

    def size(self):
        return sum(len(b) for b in self.levels)

    def quantile(self, q):
        items = sorted((x, 2 ** h) for h, b in enumerate(self.levels) for x in b)
        total = sum(w for _, w in items)
        acc = 0
        for x, w in items:
            acc += w
            if acc >= q * total:
                return x
        return items[-1][0]


def quantile_experiment(n=200_000, ks=(50, 200, 800), seed=3):
    """Latencies (lognormal with a heavy tail): estimated p50, p99 and p99.9 from sketches of several sizes against
    the exact values, with the rank error of each estimate."""
    rng = random.Random(seed)
    xs = [rng.lognormvariate(3, 0.6) * (10 if rng.random() < 0.01 else 1) for _ in range(n)]
    srt = sorted(xs)

    def rank(v):
        import bisect
        return bisect.bisect_left(srt, v) / n
    exact = {q: srt[int(q * n)] for q in (0.5, 0.99, 0.999)}
    rows = []
    for k in ks:
        sk = KLL(k, seed)
        for x in xs:
            sk.add(x)
        est = {q: sk.quantile(q) for q in exact}
        rows.append({"k": k, "stored": sk.size(), "estimates": est,
                     "rank_error": {q: abs(rank(est[q]) - q) for q in exact}})
    return {"n": n, "exact": exact, "rows": rows}


# ---------------------------------------------------------------- lakehouse commits

def optimistic_commits(writers=(1, 2, 4, 8, 16), commits_each=50, work=1.0, commit_time=0.05, seed=4,
                       disjoint=False):
    """Writers to one table on object storage, as in Iceberg or Delta: each reads the current snapshot, works, and
    tries to swap the table's pointer from that snapshot to its new one (compare-and-swap).  If another commit won
    in between, it retries; with disjoint=True, non-conflicting appends are rebased instead of redone."""
    rng = random.Random(seed)
    out = []
    for w in writers:
        version = 0
        t = 0.0
        events = []
        for i in range(w):
            events.append((rng.uniform(0, work), i, 0, 0))   # (finish time, writer, base version, done)
        done = [0] * w
        retries = 0
        import heapq
        heapq.heapify(events)
        while events:
            ft, i, base, _ = heapq.heappop(events)
            t = ft
            if base == version or disjoint:
                version += 1
                done[i] += 1
                if done[i] < commits_each:
                    heapq.heappush(events, (t + commit_time + rng.expovariate(1 / work), i, version, 0))
            else:
                retries += 1
                heapq.heappush(events, (t + commit_time + rng.expovariate(1 / work), i, version, 0))
        out.append({"writers": w, "commits": w * commits_each, "retries": retries,
                    "retry_per_commit": retries / (w * commits_each), "time": t,
                    "throughput": w * commits_each / t})
    return out
