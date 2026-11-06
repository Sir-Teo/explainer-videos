"""Join algorithms on pages, with every page read and written counted (Part 35), to set against the textbook
formulas.

Relations are lists of pages, each a list of (key, payload) tuples; ``B`` pages of memory.  Each algorithm returns
(the joined pairs, I/O counts):

* ``block_nested_loops``: hold B - 2 pages of R; scan all of S for each block.  M + ceil(M / (B - 2)) N.
* ``index_nested_loops``: for each R tuple, probe a hash index on S (one page for the bucket).  M + |R| (1 + pages
  of matches).
* ``sort_merge``: external merge sort of each input (runs of B pages, then (B - 1)-way merges), then one merging
  scan.  2 M (passes) + 2 N (passes) + M + N.
* ``grace_hash``: partition both inputs into B - 1 buckets on disk, then join bucket by bucket in memory.
  3 (M + N), when each bucket of R fits in memory.
"""
from __future__ import annotations

import heapq
import math
import random


def make(n: int, page_rows: int, keys: int, seed: int) -> list[list]:
    rng = random.Random(seed)
    rows = [(rng.randrange(keys), i) for i in range(n)]
    return [rows[i:i + page_rows] for i in range(0, n, page_rows)]


class IO:
    def __init__(self):
        self.reads = 0
        self.writes = 0

    @property
    def total(self):
        return self.reads + self.writes


def block_nested_loops(R, S, B):
    io = IO()
    out = []
    blk = max(1, B - 2)
    for i in range(0, len(R), blk):
        chunk = R[i:i + blk]
        io.reads += len(chunk)
        table: dict = {}
        for page in chunk:
            for k, v in page:
                table.setdefault(k, []).append(v)
        for page in S:
            io.reads += 1
            for k, w in page:
                for v in table.get(k, ()):
                    out.append((v, w))
    return out, io


def index_nested_loops(R, S, B, page_rows):
    io = IO()
    index: dict = {}
    for page in S:                                    # the index already exists: building it is not charged
        for k, w in page:
            index.setdefault(k, []).append(w)
    out = []
    for page in R:
        io.reads += 1
        for k, v in page:
            ms = index.get(k, [])
            io.reads += 1 + (math.ceil(len(ms) / page_rows) if ms else 0)
            out.extend((v, w) for w in ms)
    return out, io


def _external_sort(P, B, io, page_rows):
    runs = []
    for i in range(0, len(P), B):                     # pass 0: sorted runs of B pages
        chunk = [t for page in P[i:i + B] for t in page]
        io.reads += len(P[i:i + B])
        chunk.sort()
        run = [chunk[j:j + page_rows] for j in range(0, len(chunk), page_rows)]
        io.writes += len(run)
        runs.append(run)
    passes = 1
    while len(runs) > 1:                              # (B - 1)-way merges
        nxt = []
        for i in range(0, len(runs), B - 1):
            group = runs[i:i + B - 1]
            io.reads += sum(len(r) for r in group)
            merged = list(heapq.merge(*[[t for page in r for t in page] for r in group]))
            run = [merged[j:j + page_rows] for j in range(0, len(merged), page_rows)]
            io.writes += len(run)
            nxt.append(run)
        runs = nxt
        passes += 1
    return (runs[0] if runs else []), passes


def sort_merge(R, S, B, page_rows):
    io = IO()
    Rs, pr = _external_sort(R, B, io, page_rows)
    Ss, ps = _external_sort(S, B, io, page_rows)
    io.reads += len(Rs) + len(Ss)                     # the merging scan
    a = [t for page in Rs for t in page]
    b = [t for page in Ss for t in page]
    out, j = [], 0
    for k, v in a:
        while j < len(b) and b[j][0] < k:
            j += 1
        jj = j
        while jj < len(b) and b[jj][0] == k:
            out.append((v, b[jj][1]))
            jj += 1
    return out, io, (pr, ps)


def grace_hash(R, S, B, page_rows):
    io = IO()
    nb = B - 1

    def part(P):
        buckets = [[] for _ in range(nb)]
        for page in P:
            io.reads += 1
            for t in page:
                buckets[hash(("p", t[0])) % nb].append(t)
        pages = []
        for bk in buckets:
            bp = [bk[j:j + page_rows] for j in range(0, len(bk), page_rows)]
            io.writes += len(bp)
            pages.append(bp)
        return pages
    Rp, Sp = part(R), part(S)
    out = []
    fits = True
    for rb, sb in zip(Rp, Sp):
        io.reads += len(rb) + len(sb)
        fits = fits and len(rb) <= B - 2
        table: dict = {}
        for page in rb:
            for k, v in page:
                table.setdefault(k, []).append(v)
        for page in sb:
            for k, w in page:
                for v in table.get(k, ()):
                    out.append((v, w))
    return out, io, fits


def formulas(M, N, B, R_tuples, page_rows, match_pages=1):
    def sort_cost(P):
        runs = math.ceil(P / B)
        passes = 1 + (math.ceil(math.log(runs, B - 1)) if runs > 1 else 0)
        return 2 * P * passes
    return {"block nested loops": M + math.ceil(M / (B - 2)) * N,
            "index nested loops": M + R_tuples * (1 + match_pages),
            "sort-merge": sort_cost(M) + sort_cost(N) + M + N,
            "grace hash": 3 * (M + N)}


def compare(n_r=20_000, n_s=10_000, page_rows=50, B=20, keys=5_000, seed=0) -> dict:
    R = make(n_r, page_rows, keys, seed)
    S = make(n_s, page_rows, keys, seed + 1)
    M, N = len(R), len(S)
    truth = sorted(block_nested_loops(R, S, B)[0])
    res = {}
    o, io = block_nested_loops(R, S, B)
    res["block nested loops"] = io.total
    o, io = index_nested_loops(R, S, B, page_rows)
    assert sorted(o) == truth
    res["index nested loops"] = io.total
    o, io, passes = sort_merge(R, S, B, page_rows)
    assert sorted(o) == truth
    res["sort-merge"] = io.total
    o, io, fits = grace_hash(R, S, B, page_rows)
    assert sorted(o) == truth
    res["grace hash"] = io.total
    avg = n_s / keys
    f = formulas(M, N, B, n_r, page_rows, match_pages=math.ceil(avg / page_rows))
    return {"M": M, "N": N, "B": B, "measured": res, "formula": f, "matches": len(truth), "sort_passes": passes,
            "buckets_fit": fits}
