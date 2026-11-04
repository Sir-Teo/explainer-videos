"""Precompute everything numerical in Part 9 of *Computer Science, Built* ("The Memory Hierarchy").

    python -m videos.cs.cs9.compute              # everything missing
    python -m videos.cs.cs9.compute --force staircase

Results are cached in ``.cache/cs9/<name>.json``; scenes call ``load(name)``.  The cache simulator and the trace
analyses are ``explainer/cs/pebble/cache.py`` (checked against brute force in tests/test_cs9_cache.py).  The
measurements of this machine compile small C programs with the system compiler; their numbers belong to whatever
computer runs this file, and the scenes say which one (from /proc/cpuinfo).

Items:
    machine     this computer: CPU name, cache sizes (lscpu), clock
    staircase   the pointer-chasing latency staircase: nanoseconds per dependent load, working sets 4 KB to 512 MB
    bandwidth   sequential read bandwidth against working-set size
    matmul      matrix multiply in C from n = 256 to 2048: i-j-k, i-k-j, tiled, against a tuned BLAS (numpy), in
                GFLOP/s; the misses of each order simulated on a small cache (n = 64), fully associative and 8-way
    trace       the Job's first chapter as a memory trace: the scatter, reuse distances, the miss-ratio curve
    policies    LRU, tree pseudo-LRU, FIFO, random and Belady's optimum on that trace, by cache size
    threec      compulsory, capacity and conflict misses by size and associativity
    scans       all thirty novels: every table scan, and its exact LRU misses at every cache size, against keeping
                the front of the table
    scancost    cycles per scanned table entry on Part 8's core with this machine's latencies at 885 MHz: the
                table in L1, in L2, beyond; with and without a stride prefetcher
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import tempfile
import time
from pathlib import Path

import numpy as np

from explainer.ai.cache import Cache

CACHE = Cache("cs9")
load = CACHE.load


def _run_c(src: str, args=(), opt="-O2") -> str:
    with tempfile.TemporaryDirectory() as d:
        c, exe = Path(d) / "m.c", Path(d) / "m"
        c.write_text(src)
        subprocess.run(["gcc", opt, "-march=native", "-o", str(exe), str(c), "-lm"], check=True)
        out = subprocess.run([str(exe), *map(str, args)], check=True, capture_output=True, text=True)
        return out.stdout


def compute_machine() -> dict:
    name = "unknown"
    try:
        for line in Path("/proc/cpuinfo").read_text().splitlines():
            if line.startswith("model name"):
                name = line.split(":", 1)[1].strip()
                break
    except OSError:
        pass
    caches = {}
    try:
        out = subprocess.run(["lscpu"], capture_output=True, text=True).stdout
        for key in ("L1d", "L2", "L3"):
            m = re.search(rf"^{key} cache:\s+(.+)$", out, re.M)
            if m:
                caches[key] = m.group(1).strip()
    except OSError:
        pass
    ghz = None
    m = re.search(r"@ ([\d.]+)GHz", name)
    if m:
        ghz = float(m.group(1))
    return {"cpu": name, "caches": caches, "ghz": ghz, "cores": os.cpu_count()}


CHASE = r"""
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>
static double now(void) { struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t); return t.tv_sec + t.tv_nsec * 1e-9; }
static uint64_t s = 88172645463325252ull;
static uint64_t rnd(void) { s ^= s << 13; s ^= s >> 7; s ^= s << 17; return s; }
int main(int argc, char **argv) {
    /* a random cyclic permutation of the cache lines of a working set; each load's address is the last load's
       value, so the loads cannot overlap: the time per step is the latency of wherever the line lives */
    size_t bytes = strtoull(argv[1], 0, 10), line = 64, n = bytes / line;
    char *buf = aligned_alloc(4096, bytes);
    size_t *order = malloc(n * sizeof(size_t));
    for (size_t i = 0; i < n; i++) order[i] = i;
    for (size_t i = n - 1; i > 0; i--) { size_t j = rnd() % (i + 1); size_t t = order[i]; order[i] = order[j]; order[j] = t; }
    for (size_t i = 0; i < n; i++) *(void **)(buf + order[i] * line) = buf + order[(i + 1) % n] * line;
    void **p = (void **)(buf + order[0] * line);
    size_t steps = 20000000;
    for (size_t i = 0; i < n * 2 && i < steps; i++) p = (void **)*p;   /* warm up */
    double best = 1e9;
    for (int r = 0; r < 3; r++) {
        double t0 = now();
        for (size_t i = 0; i < steps; i++) p = (void **)*p;
        double t = (now() - t0) / steps;
        if (t < best) best = t;
    }
    printf("%.4f %p\n", best * 1e9, (void *)p);
    return 0;
}
"""


def compute_staircase() -> dict:
    sizes = [1 << k for k in range(12, 30)]  # 4 KB .. 512 MB
    out = []
    for b in sizes:
        ns = float(_run_c(CHASE, [b]).split()[0])
        out.append({"bytes": b, "ns": ns})
    mach = compute_machine()
    return {"points": out, "machine": mach}


BANDWIDTH = r"""
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>
static double now(void) { struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t); return t.tv_sec + t.tv_nsec * 1e-9; }
int main(int argc, char **argv) {
    size_t bytes = strtoull(argv[1], 0, 10), n = bytes / 8;
    uint64_t *a = aligned_alloc(4096, bytes);
    for (size_t i = 0; i < n; i++) a[i] = i;
    size_t total = 0; uint64_t sum = 0;
    double best = 0;
    size_t reps = (1ull << 31) / bytes + 1;
    for (int r = 0; r < 5; r++) {
        double t0 = now();
        for (size_t k = 0; k < reps; k++) { uint64_t s0 = 0, s1 = 0, s2 = 0, s3 = 0;
            for (size_t i = 0; i < n; i += 4) { s0 += a[i]; s1 += a[i + 1]; s2 += a[i + 2]; s3 += a[i + 3]; }
            sum += s0 + s1 + s2 + s3; }
        double gbs = (double)bytes * reps / (now() - t0) / 1e9;
        if (gbs > best) best = gbs;
    }
    printf("%.3f %llu\n", best, (unsigned long long)sum);
    return 0;
}
"""


def compute_bandwidth() -> dict:
    sizes = [1 << k for k in range(13, 30, 2)]
    out = []
    for b in sizes:
        out.append({"bytes": b, "gbs": float(_run_c(BANDWIDTH, [b]).split()[0])})
    return {"points": out}


MATMUL = r"""
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
static double now(void) { struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t); return t.tv_sec + t.tv_nsec * 1e-9; }
static int N;
static double *A, *B, *C;
#define a(i, j) A[(size_t)(i) * N + (j)]
#define b(i, j) B[(size_t)(i) * N + (j)]
#define c(i, j) C[(size_t)(i) * N + (j)]
static void ijk(void) { for (int i = 0; i < N; i++) for (int j = 0; j < N; j++) { double s = 0;
    for (int k = 0; k < N; k++) s += a(i, k) * b(k, j); c(i, j) = s; } }
static void ikj(void) { memset(C, 0, sizeof(double) * N * N); for (int i = 0; i < N; i++) for (int k = 0; k < N; k++) {
    double x = a(i, k); for (int j = 0; j < N; j++) c(i, j) += x * b(k, j); } }
static void tiled(int T) { memset(C, 0, sizeof(double) * N * N);
    for (int ii = 0; ii < N; ii += T) for (int kk = 0; kk < N; kk += T) for (int jj = 0; jj < N; jj += T)
        for (int i = ii; i < ii + T; i++) for (int k = kk; k < kk + T; k++) { double x = a(i, k);
            for (int j = jj; j < jj + T; j++) c(i, j) += x * b(k, j); } }
int main(int argc, char **argv) {
    N = atoi(argv[1]); int with_ijk = atoi(argv[2]);
    A = aligned_alloc(64, sizeof(double) * N * N); B = aligned_alloc(64, sizeof(double) * N * N);
    C = aligned_alloc(64, sizeof(double) * N * N);
    for (int i = 0; i < N; i++) for (int j = 0; j < N; j++) { a(i, j) = (i * 7 + j) % 13; b(i, j) = (i + j * 3) % 11; }
    double t;
    if (with_ijk) { t = now(); ijk(); printf("ijk %.4f %.0f\n", now() - t, c(17, 23)); }
    t = now(); ikj(); printf("ikj %.4f %.0f\n", now() - t, c(17, 23));
    t = now(); tiled(128); printf("tiled %.4f %.0f\n", now() - t, c(17, 23));
    return 0;
}
"""


def _matmul_trace(n: int, order: str, T: int = 8) -> list[int]:
    """The byte addresses of every A, B, C element touched by a matrix multiply (doubles, row major; A at 0, B
    after it, C after B), for the cache simulator."""
    A, B, C = 0, 8 * n * n, 16 * n * n
    out = []
    if order == "ijk":
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    out += [A + 8 * (i * n + k), B + 8 * (k * n + j)]
                out.append(C + 8 * (i * n + j))
    elif order == "ikj":
        for i in range(n):
            for k in range(n):
                out.append(A + 8 * (i * n + k))
                for j in range(n):
                    out += [B + 8 * (k * n + j), C + 8 * (i * n + j)]
    else:
        for ii in range(0, n, T):
            for kk in range(0, n, T):
                for jj in range(0, n, T):
                    for i in range(ii, ii + T):
                        for k in range(kk, kk + T):
                            out.append(A + 8 * (i * n + k))
                            for j in range(jj, jj + T):
                                out += [B + 8 * (k * n + j), C + 8 * (i * n + j)]
    return out


def compute_matmul() -> dict:
    from explainer.cs.pebble.cache import SetAssoc

    sizes = (256, 512, 1024, 2048)
    times: dict[str, dict[str, float]] = {}
    for n in sizes:
        out = _run_c(MATMUL, [n, int(n <= 1024)])
        for line in out.strip().splitlines():
            name, t, _ = line.split()
            times.setdefault(name, {})[str(n)] = float(t)
        a = np.random.default_rng(0).random((n, n))
        b = np.random.default_rng(1).random((n, n))
        a @ b
        t0 = time.time()
        a @ b
        times.setdefault("blas", {})[str(n)] = time.time() - t0
    gflops = {k: {n: 2 * int(n) ** 3 / t / 1e9 for n, t in v.items()} for k, v in times.items()}
    n = 64
    sim = {}
    for order in ("ijk", "ikj", "tiled"):
        tr = _matmul_trace(n, order, T=8)
        row = {"accesses": len(tr)}
        for name, ways in (("full", 128), ("8-way", 8)):
            c = SetAssoc(8 * 1024, line=64, ways=ways)
            row[name] = sum(not c.access(a) for a in tr)
        sim[order] = row
    return {"sizes": list(sizes), "times": times, "gflops": gflops,
            "sim": {"n": n, "cache_bytes": 8 * 1024, "tile": 8, "rows": sim}, "machine": compute_machine()}


ITEMS = {"machine": compute_machine, "staircase": compute_staircase, "bandwidth": compute_bandwidth,
         "matmul": compute_matmul}



# ---------------------------------------------------------------------------
# the Job's table scans over the whole corpus, and their misses under LRU, exactly
# ---------------------------------------------------------------------------
def scan_ends(text: bytes) -> np.ndarray:
    """For every word of the text, the index of the last table entry the Job's scan reads (the word's own entry, or
    the last entry when the word is new and appended).  The table holds 12-byte entries in order of first use."""
    from explainer.cs.pebble import programs as P

    index: dict[bytes, int] = {}
    ends = np.empty(len(P.job_words(text)), np.int64)
    for t, w in enumerate(P.job_words(text)):
        i = index.get(w)
        if i is None:
            i = len(index)
            index[w] = i
        ends[t] = i
    return ends


def lru_scan_misses(ends_lines: np.ndarray, capacity: int) -> tuple[int, int]:
    """Misses of a fully associative LRU cache of ``capacity`` lines on a sequence of prefix scans (scan t reads
    lines 0 .. e_t).  Between the previous access to line l (by the latest earlier scan reaching l, ending at e') and
    this one, exactly e' + 1 distinct lines are touched (this scan's lines below l and that scan's lines from l on),
    so the access hits iff e' < capacity.  The latest scan reaching each line is read off a stack of earlier ends,
    increasing from the top: O(1) amortized per scan.  Returns (accesses, misses), in lines."""
    stack: list[int] = []  # ends of earlier scans, most recent on top, strictly increasing downwards
    accesses = misses = 0
    for e in ends_lines:
        e = int(e)
        accesses += e + 1
        # lines reached by an earlier scan with end < capacity hit; others miss (or are first touches)
        m = -1  # the largest earlier end below capacity, among the scans that are latest for some line
        for s in reversed(stack):
            if s < capacity:
                m = s
            else:
                break
        hits = min(e, m) + 1 if m >= 0 else 0
        misses += e + 1 - hits
        while stack and stack[-1] <= e:
            stack.pop()
        stack.append(e)
    return accesses, misses


# ---------------------------------------------------------------------------
# the Job's memory trace
# ---------------------------------------------------------------------------
def chapter_trace():
    from explainer.cs.pebble import assemble
    from explainer.cs.pebble import programs as P
    from explainer.cs.pebble.cache import memtrace
    from videos.cs.cs8.compute import chapter_tape

    return memtrace(assemble(P.JOB_V0).image, tape=chapter_tape())


def compute_trace() -> dict:
    from explainer.cs.pebble.cache import miss_curve, stack_distances

    t = chapter_trace()
    lines = t.addr // 64
    d = stack_distances(lines)
    # a picture: every access as (time, address), thinned evenly
    k = max(1, len(t) // 6000)
    scatter = {"step": t.step[::k].tolist(), "addr": t.addr[::k].tolist(), "store": t.store[::k].tolist()}
    regions = {"table": [65536, 65536 + 12 * 4000], "pool": [524288, 524288 + 8 * 4000], "code": [0, 600]}
    caps = [1 << k for k in range(0, 15)]  # lines: 64 B .. 1 MB
    curve = miss_curve(d, caps)
    hist = np.bincount(np.clip(d[d >= 0], 0, 4095) // 16, minlength=256)[:256].tolist()
    return {"accesses": len(t), "instructions": t.instructions, "loads": int((~t.store).sum()),
            "stores": int(t.store.sum()), "distinct_lines": int(len(np.unique(lines))), "scatter": scatter,
            "regions": regions, "capacities_lines": caps, "miss_curve": curve, "first_touch": int((d < 0).sum()),
            "reuse_hist16": hist, "reuse_median": float(np.median(d[d >= 0]))}


def compute_policies() -> dict:
    from explainer.cs.pebble.cache import SetAssoc, belady

    t = chapter_trace()
    lines = (t.addr // 64).tolist()
    out = {}
    for kb in (1, 2, 4, 8):
        row = {}
        for pol in ("lru", "plru", "fifo", "random"):
            c = SetAssoc(kb * 1024, line=64, ways=8, policy=pol)
            row[pol] = sum(not c.access(a) for a in t.addr.tolist()) / len(lines)
        row["opt (fully associative)"] = belady(lines, kb * 1024 // 64) / len(lines)
        c = SetAssoc(kb * 1024, line=64, ways=kb * 1024 // 64)
        row["lru (fully associative)"] = sum(not c.access(a) for a in t.addr.tolist()) / len(lines)
        out[str(kb)] = row
    return {"rows": out, "accesses": len(lines)}


def compute_threec() -> dict:
    from explainer.cs.pebble.cache import three_c

    t = chapter_trace()
    lines = t.addr // 64
    out = []
    for kb in (1, 2, 4, 8, 16):
        for ways in (1, 2, 8):
            sets = kb * 1024 // 64 // ways
            r = three_c(lines, sets=sets, ways=ways)
            out.append({"kb": kb, "ways": ways, **r})
    return {"rows": out}


def compute_scans() -> dict:
    """The Job over all thirty novels: every table scan, and the LRU misses of the table at every cache size; and
    the misses if the cache simply kept the front of the table (close to Belady's optimum on these scans)."""
    import videos.ai.ai1.compute as A
    from explainer.cs.pebble import programs as P
    from videos.cs.cs6.compute import novels

    books = novels()
    full = P.job_tape("\n".join(books[n] for n in A.BOOKS))
    ends = scan_ends(full)
    e_lines = (ends * 12 + 11) // 64
    caps_kb = [4, 8, 16, 32, 64, 128, 256, 512, 1024]
    rows = []
    total = int((e_lines + 1).sum())
    for kb in caps_kb:
        c = kb * 1024 // 64
        acc, mis = lru_scan_misses(e_lines, c)
        keep_front = int(np.maximum(0, e_lines + 1 - c).sum()) + min(c, int(e_lines.max()) + 1)
        rows.append({"kb": kb, "lru": mis / acc, "keep_front": keep_front / acc, "misses": mis})
    lengths = np.bincount(np.minimum(ends // 256, 255), minlength=256).tolist()
    return {"words": len(ends), "table_entries": int(ends.max()) + 1, "table_kb": (int(ends.max()) + 1) * 12 / 1024,
            "line_reads": total, "rows": rows, "scan_hist256": lengths, "mean_scan": float(ends.mean() + 1)}


ITEMS.update({"trace": compute_trace, "policies": compute_policies, "threec": compute_threec,
              "scans": compute_scans})


# ---------------------------------------------------------------------------
# the price of a missed line, measured on Part 8's core with a realistic hierarchy
# ---------------------------------------------------------------------------
MHZ = 884.9557522123894  # Part 7's clock, kept by the ledger


def pebble_hierarchy(prefetch: str | None = "stride", mhz: float = MHZ):
    """L1 32 KB 8-way, L2 1 MB 16-way, a 4 MB third level, then DRAM: this machine's measured latencies
    (load("staircase")) converted to cycles of Pebble's 885 MHz clock."""
    from explainer.cs.pebble.cache import Hierarchy, SetAssoc

    st = load("staircase")["points"]

    def ns(kb):
        return min(st, key=lambda p: abs(p["bytes"] - kb * 1024))["ns"]

    cyc = [max(1, int(np.ceil(ns(k) * mhz / 1000))) for k in (16, 512, 2048, 65536)]
    l1, l2, l3, dram = cyc
    return Hierarchy([SetAssoc(32 << 10, ways=8, hit=l1, name="L1"),
                      SetAssoc(1 << 20, ways=16, hit=l2 - l1, name="L2"),
                      SetAssoc(4 << 20, ways=16, hit=l3 - l2, name="L3")], dram=dram - l3, prefetch=prefetch), cyc


SCAN_BENCH = """
        li   s0, 65536        # the table
        li   s1, {n}           # entries
        li   a1, {target}      # the length looked for
        li   s2, {reps}
rep:    mv   t0, s0
        li   a2, 0
scan:   beq  a2, s1, done
        lw   t1, 4(t0)
        bne  t1, a1, next
        addi a3, a3, 1        # (a match: the Job would compare letters here)
next:   addi t0, t0, 12
        addi a2, a2, 1
        j    scan
done:   addi s2, s2, -1
        bnez s2, rep
        halt
"""


def compute_scancost() -> dict:
    """Cycles per scanned table entry on the out-of-order core when the table lives in L1, in L2, or beyond, with
    the word lengths in the corpus's table order."""
    import videos.ai.ai1.compute as A
    from explainer.cs.pebble import assemble
    from explainer.cs.pebble import predict as PR
    from explainer.cs.pebble import programs as P
    from explainer.cs.pebble.ooo import OutOfOrder
    from videos.cs.cs6.compute import novels

    books = novels()
    full = P.job_tape("\n".join(books[n] for n in A.BOOKS))
    seen: dict[bytes, int] = {}
    for w in P.job_words(full):
        if w not in seen:
            seen[w] = len(w)
    lengths = list(seen.values())
    rows = []
    for n in (1000, 40000, 120000):
        img = None
        res = {}
        for name in ("ideal", "hierarchy", "no prefetch"):
            cyc = {}
            for reps in (1, 3):  # the difference is two warm passes: compulsory misses cancel
                prog = assemble(SCAN_BENCH.format(n=n, target=6, reps=reps))
                img = bytearray(prog.image)
                img.extend(bytes(65536 + 12 * n + 64 - len(img)))
                for i in range(n):
                    o = 65536 + 12 * i
                    img[o + 4:o + 8] = lengths[i % len(lengths)].to_bytes(4, "little")
                kw = {} if name == "ideal" else {
                    "cache": pebble_hierarchy(None if name == "no prefetch" else "stride")[0]}
                cyc[reps] = OutOfOrder(bytes(img), predictor=PR.Tournament(), mem_size=1 << 21, **kw).run().cycles
            res[name] = {"per_entry": (cyc[3] - cyc[1]) / (2 * n), "cold_pass": cyc[1] / n}
        rows.append({"entries": n, "kb": 12 * n / 1024, **res})
    return {"rows": rows, "latencies": pebble_hierarchy()[1], "mhz": MHZ}


ITEMS["scancost"] = compute_scancost


# ---------------------------------------------------------------------------
# the Job's line accesses at sampled points of the corpus run, through a three-level hierarchy
# ---------------------------------------------------------------------------
TABLE, POOL = 65536, 524288


def corpus_words() -> list[bytes]:
    import videos.ai.ai1.compute as A
    from explainer.cs.pebble import programs as P
    from videos.cs.cs6.compute import novels

    books = novels()
    return P.job_words(P.job_tape("\n".join(books[n] for n in A.BOOKS)))


def window_events(words: list[bytes], start: int, count: int):
    """The cache lines the Job reads for words ``start`` .. ``start + count``: each table entry scanned (its line),
    and, for each entry of the word's length, the pool line of its first letter (and the next letters while they
    match).  Returns (lines, is_pool) in program order, with the table state as it is at ``start``."""
    index: dict[bytes, int] = {}
    offs: list[int] = []
    lens: list[int] = []
    off = 0
    for w in words[:start]:
        if w not in index:
            index[w] = len(offs)
            offs.append(off)
            lens.append(len(w))
            off += len(w)
    lines: list[int] = []
    pool: list[bool] = []
    for w in words[start:start + count]:
        i = index.get(w)
        end = len(offs) if i is None else i  # the scan reads entries 0 .. end (end itself only if found)
        L = len(w)
        last = -1
        for e in range(min(end + 1, len(offs))):
            ln = (TABLE + 12 * e + 4) // 64
            if ln != last:
                lines.append(ln)
                pool.append(False)
                last = ln
            if lens[e] == L:
                o = offs[e]
                lines.append((POOL + o) // 64)
                pool.append(True)
        if i is None:
            index[w] = len(offs)
            offs.append(off)
            lens.append(L)
            off += L
    return np.array(lines, np.int64), np.array(pool, bool)


def compute_job_memory() -> dict:
    """Misses of table and pool reads in L1 / L2 / L3 at four points of the corpus run (each window warmed by the
    words before it), from which ledger row 3 is projected."""
    from explainer.cs.pebble.cache import SetAssoc

    words = corpus_words()
    n = len(words)
    out = []
    for frac in (0.1, 0.35, 0.6, 0.85):
        start = int(n * frac)
        warm, count = 300, 1500
        lines, pool = window_events(words, start - warm, warm + count)
        levels = [SetAssoc(32 << 10, ways=8), SetAssoc(1 << 20, ways=16), SetAssoc(4 << 20, ways=16)]
        # the warm-up: the events of the first ``warm`` words
        wl, _ = window_events(words, start - warm, warm)
        cut = len(wl)
        stats = {k: {"accesses": 0, "L1": 0, "L2": 0, "L3": 0} for k in ("table", "pool")}
        for j, (ln, ip) in enumerate(zip(lines.tolist(), pool.tolist())):
            a = ln * 64
            lvl = 0
            for lv in levels:
                if lv.access(a):
                    break
                lvl += 1
            if j >= cut:
                st = stats["pool" if ip else "table"]
                st["accesses"] += 1
                for k, name in enumerate(("L1", "L2", "L3")):
                    if lvl > k:
                        st[name] += 1
        out.append({"frac": frac, "word": start, "events": int(len(lines) - cut), **stats})
    return {"windows": out, "words": n}


POOL_BENCH = """
        li   s0, 65536        # the table: every entry has the looked-for length, pointing somewhere in the pool
        li   s1, {n}
        li   a1, 6
        li   s2, {reps}
        li   a3, 524288        # the word being looked up, at the end of the pool: never equal
rep:    mv   t0, s0
        li   a2, 0
scan:   beq  a2, s1, done
        lw   t1, 4(t0)
        bne  t1, a1, next
        lw   t2, 0(t0)        # its letters
        lbu  a4, 0(t2)
        lbu  a5, 0(a3)
        bne  a4, a5, next     # the first letter differs
next:   addi t0, t0, 12
        addi a2, a2, 1
        j    scan
done:   addi s2, s2, -1
        bnez s2, rep
        halt
"""


def compute_poolcost() -> dict:
    """Cycles per same-length entry when its letters live in L1, L2 or beyond (random pool lines)."""
    from explainer.cs.pebble import assemble
    from explainer.cs.pebble import predict as PR
    from explainer.cs.pebble.ooo import OutOfOrder

    rng = np.random.default_rng(2)
    rows = []
    density = 1697048776 / 15020950949  # same-length entries among those scanned, over the corpus (Part 6's counts)
    for n, pool_kb in ((1000, 8), (20000, 512), (20000, 3072)):
        res = {}
        same_n = 0
        for name in ("ideal", "hierarchy"):
            cyc = {}
            for reps in (1, 3):
                rng = np.random.default_rng(2)
                prog = assemble(POOL_BENCH.format(n=n, reps=reps))
                size = 524288 + pool_kb * 1024 + 4096
                img = bytearray(prog.image)
                img.extend(bytes(size - len(img)))
                img[524288] = ord("z")
                same_n = 0
                for i in range(n):
                    o = 65536 + 12 * i
                    p = 524288 + 64 + int(rng.integers(0, pool_kb * 1024 // 64 - 1)) * 64
                    img[o:o + 4] = p.to_bytes(4, "little")
                    same = rng.random() < density
                    same_n += same
                    img[o + 4:o + 8] = (6 if same else 5).to_bytes(4, "little")
                    img[p] = ord("a") + int(rng.integers(0, 25))
                kw = {} if name == "ideal" else {"cache": pebble_hierarchy()[0]}
                cyc[reps] = OutOfOrder(bytes(img), predictor=PR.Tournament(), mem_size=1 << 22, **kw).run().cycles
            res[name] = {"per_entry": (cyc[3] - cyc[1]) / (2 * n)}
        extra = (res["hierarchy"]["per_entry"] - res["ideal"]["per_entry"]) * n / max(same_n, 1)
        rows.append({"entries": n, "pool_kb": pool_kb, "same_length": same_n, "extra_per_same": extra, **res})
    return {"rows": rows, "density": density}


ITEMS.update({"job_memory": compute_job_memory, "poolcost": compute_poolcost})


def _steady(src_fn, fill, mem, cache_fn, n):
    """Cycles per entry of two warm passes (three passes minus one), so compulsory misses cancel."""
    from explainer.cs.pebble import assemble
    from explainer.cs.pebble import predict as PR
    from explainer.cs.pebble.ooo import OutOfOrder

    cyc = {}
    for reps in (1, 3):
        prog = assemble(src_fn(reps))
        img = bytearray(prog.image)
        img.extend(bytes(mem - len(img)))
        fill(img)
        cyc[reps] = OutOfOrder(bytes(img), predictor=PR.Tournament(), mem_size=1 << 22, cache=cache_fn()).run().cycles
    return (cyc[3] - cyc[1]) / (2 * n)


def compute_job() -> dict:
    """Ledger row 3: the Job with this machine's memory hierarchy at Pebble's clock.  The extra cycles per scanned
    entry and per same-length entry (their letters read from the pool) are measured on the core in steady state,
    with the table and the pool in L2 as they are over the corpus, and weighted by the fraction of those reads that
    miss L1 in the sampled windows.  The same at this machine's own clock shows the memory wall as a ratio."""
    import videos.ai.ai1.compute as A
    from explainer.cs.pebble import programs as P
    from videos.cs.cs6.compute import load as load6
    from videos.cs.cs6.compute import novels
    from videos.cs.cs8.compute import load as load8

    books = novels()
    full = P.job_tape("\n".join(books[n] for n in A.BOOKS))
    seen: dict[bytes, int] = {}
    for w in P.job_words(full):
        if w not in seen:
            seen[w] = len(w)
    lengths = list(seen.values())
    f = load6("job")["corpus"]["features"]
    density = f["same_length"] / f["scanned"]
    win = load("job_memory")["windows"]
    m_table = sum(w["table"]["L1"] for w in win) / sum(w["table"]["accesses"] for w in win)
    m_pool = sum(w["pool"]["L1"] for w in win) / sum(w["pool"]["accesses"] for w in win)
    n = 20000
    rng = np.random.default_rng(2)
    same = rng.random(n) < density
    ptrs = 524288 + 64 + rng.integers(0, 512 * 1024 // 64 - 1, n) * 64

    def fill_scan(img):
        for i in range(n):
            o = 65536 + 12 * i
            img[o + 4:o + 8] = lengths[i % len(lengths)].to_bytes(4, "little")

    def fill_pool(img):
        img[524288] = ord("z")
        for i in range(n):
            o = 65536 + 12 * i
            img[o:o + 4] = int(ptrs[i]).to_bytes(4, "little")
            img[o + 4:o + 8] = (6 if same[i] else 5).to_bytes(4, "little")
            img[int(ptrs[i])] = ord("a") + i % 25

    out = {}
    for name, mhz in (("pebble", MHZ), ("this machine", load("machine")["ghz"] * 1000)):
        row = {"mhz": mhz, "latencies": pebble_hierarchy(mhz=mhz)[1]}
        for pf in ("stride", None):
            key = "prefetch" if pf else "no prefetch"
            scan = {c: _steady(lambda r: SCAN_BENCH.format(n=n, target=6, reps=r), fill_scan, 65536 + 12 * n + 64,
                               (lambda: None) if c == "ideal" else (lambda: pebble_hierarchy(pf, mhz)[0]), n)
                    for c in ("ideal", "real")}
            pool = {c: _steady(lambda r: POOL_BENCH.format(n=n, reps=r), fill_pool, 524288 + 512 * 1024 + 4096,
                               (lambda: None) if c == "ideal" else (lambda: pebble_hierarchy(pf, mhz)[0]), n)
                    for c in ("ideal", "real")}
            e_scan = scan["real"] - scan["ideal"]
            e_pool = (pool["real"] - pool["ideal"] - e_scan) * n / max(int(same.sum()), 1)
            # the benchmarks miss L1 on every line; over the corpus a fraction m of these reads do
            extra = e_scan * f["scanned"] * m_table + max(e_pool, 0) * f["same_length"] * m_pool
            row[key] = {"scan_extra_per_entry": e_scan, "pool_extra_per_same": e_pool, "extra_cycles": extra}
        out[name] = row
    led = json.loads((Cache("cs8").dir / "ledger.json").read_text())[:3]
    base = led[2]
    cycles = base["cycles"] + out["pebble"]["prefetch"]["extra_cycles"]
    seconds = cycles / (MHZ * 1e6)
    led.append({"part": 9, "label": r"real caches", "seconds": seconds, "cycles": cycles, "clock_mhz": MHZ})
    CACHE.dir.mkdir(parents=True, exist_ok=True)
    (CACHE.dir / "ledger.json").write_text(json.dumps(led, indent=1))
    return {"clocks": out, "m_table": m_table, "m_pool": m_pool, "density": density, "ledger": led,
            "row2": base, "change": cycles / base["cycles"] - 1,
            "no_prefetch_change": out["pebble"]["no prefetch"]["extra_cycles"] / base["cycles"]}


ITEMS["job"] = compute_job


# ---------------------------------------------------------------------------
# cache-oblivious transpose; the red-blue pebble bound; DRAM row buffers; learned and adaptive replacement
# ---------------------------------------------------------------------------
def _transpose_trace(n: int, how: str, b: int = 8) -> list[int]:
    """Addresses of B = A^T (doubles, row major; A at 0, B after it)."""
    A, Bb = 0, 8 * n * n
    out: list[int] = []

    def cell(i, j):
        out.append(A + 8 * (i * n + j))
        out.append(Bb + 8 * (j * n + i))

    if how == "naive":
        for i in range(n):
            for j in range(n):
                cell(i, j)
    elif how == "blocked":
        for ii in range(0, n, b):
            for jj in range(0, n, b):
                for i in range(ii, ii + b):
                    for j in range(jj, jj + b):
                        cell(i, j)
    else:  # recursive: split the larger dimension until a block is 4 x 4 (no size known to the algorithm)
        def rec(i0, i1, j0, j1):
            if (i1 - i0) * (j1 - j0) <= 16:
                for i in range(i0, i1):
                    for j in range(j0, j1):
                        cell(i, j)
            elif i1 - i0 >= j1 - j0:
                m = (i0 + i1) // 2
                rec(i0, m, j0, j1)
                rec(m, i1, j0, j1)
            else:
                m = (j0 + j1) // 2
                rec(i0, i1, j0, m)
                rec(i0, i1, m, j1)
        rec(0, n, 0, n)
    return out


def compute_oblivious() -> dict:
    from explainer.cs.pebble.cache import miss_curve, stack_distances

    n = 256
    caps_kb = [1, 2, 4, 8, 16, 32, 64]
    rows = {}
    for how, b in (("naive", 0), ("blocked", 32), ("recursive", 0)):
        tr = np.array(_transpose_trace(n, how, b=b or 8)) // 64
        d = stack_distances(tr)
        rows[how] = miss_curve(d, [k * 1024 // 64 for k in caps_kb])
    return {"n": n, "caps_kb": caps_kb, "rows": rows, "accesses": 2 * n * n, "ideal": 2 * n * n * 8 // 64}


def compute_pebbles() -> dict:
    """Words moved between a fast memory of M words and slow memory by tiled matrix multiplies, against the red-blue
    pebble lower bound 2 n^3 / sqrt(M) - 2M (Hong and Kung 1981; the constant from Smith et al. 2019)."""
    from explainer.cs.pebble.cache import miss_curve, stack_distances

    n = 64
    M_words = 1024  # an 8 KB fast memory of doubles
    lines_cap = M_words * 8 // 64
    bound = 2 * n ** 3 / np.sqrt(M_words) - 2 * M_words
    rows = []
    for order, T in (("ijk", 0), ("ikj", 0), ("tiled", 4), ("tiled", 8), ("tiled", 16)):
        tr = np.array(_matmul_trace(n, order, T=T or 8)) // 64
        d = stack_distances(tr)
        words = miss_curve(d, [lines_cap])[0] * len(tr) * 8
        rows.append({"order": order, "T": T, "words": words})
    return {"n": n, "M": M_words, "bound": bound, "rows": rows, "flops": 2 * n ** 3}


def compute_dram() -> dict:
    """Row-buffer hits of an open-page DRAM (8 banks, 8 KB rows, the bank chosen by the bits above the row offset) on
    sequential, strided and random line streams."""
    rng = np.random.default_rng(3)
    streams = {
        "sequential": np.arange(0, 64 * 50000, 64),
        "stride 4 KB": np.arange(0, 4096 * 50000, 4096) % (1 << 30),
        "random": rng.integers(0, 1 << 30, 50000) // 64 * 64,
    }
    rows = {}
    for name, addrs in streams.items():
        open_row = {}
        hits = 0
        for a in addrs.tolist():
            row = a >> 13
            bank = row % 8
            if open_row.get(bank) == row:
                hits += 1
            open_row[bank] = row
        rows[name] = hits / len(addrs)
    return {"rows": rows, "tRCD_ns": 14, "tCAS_ns": 14, "tRP_ns": 14}


def compute_frontier() -> dict:
    """Replacement on the Job's scans, scaled down (the first words of the corpus, an 8 KB cache): LRU, bimodal
    insertion (Qureshi et al. 2007: insert at the LRU end, at the MRU end once in 32), random, and Belady's optimum."""
    from explainer.cs.pebble.cache import belady

    words = corpus_words()[:6000]
    lines, _ = window_events(words, 0, len(words))
    cap = 128
    seq = lines.tolist()

    def lru_like(insert_mru):
        rnd = np.random.default_rng(4)
        from collections import OrderedDict
        c = OrderedDict()
        miss = 0
        for ln in seq:
            if ln in c:
                c.move_to_end(ln)
                continue
            miss += 1
            if len(c) >= cap:
                c.popitem(last=False)
            c[ln] = True
            if not insert_mru(rnd):
                c.move_to_end(ln, last=False)
        return miss / len(seq)

    def random_policy():
        rnd = np.random.default_rng(5)
        c, pos = [], {}
        miss = 0
        for ln in seq:
            if ln in pos:
                continue
            miss += 1
            if len(c) >= cap:
                k = int(rnd.integers(len(c)))
                del pos[c[k]]
                c[k] = ln
                pos[ln] = k
            else:
                pos[ln] = len(c)
                c.append(ln)
        return miss / len(seq)

    res = {"lru": lru_like(lambda r: True), "bip": lru_like(lambda r: r.random() < 1 / 32),
           "random": random_policy(), "opt": belady(seq, cap) / len(seq)}
    return {"words": len(words), "accesses": len(seq), "cache_lines": cap, "rows": res}


ITEMS.update({"oblivious": compute_oblivious, "pebbles": compute_pebbles, "dram": compute_dram,
              "frontier": compute_frontier})

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
