"""Precompute everything numerical in Part 10 of *Computer Science, Built* ("Parallel Machines").

    python -m videos.cs.cs10.compute              # everything missing
    python -m videos.cs.cs10.compute --force split

Results are cached in ``.cache/cs10/<name>.json``; scenes call ``load(name)``.  The models are
``explainer/cs/pebble/coherence.py`` (MESI, the store-buffering litmus test) and ``explainer/cs/pebble/parallel.py``
(work and span, schedules, scans, sorting networks, networks), checked in tests/test_cs10_parallel.py.  The
measurements compile small C programs with pthreads; their numbers belong to whatever computer runs this file.

Items:
    trends      fifty years of microprocessors (Karl Rupp's compilation, CC BY 4.0): transistors, clock, power, cores
    threads     this machine: how much throughput 1 .. 4 threads of pure arithmetic get
    split       the Job on p Pebble cores: shards counted in private tables, then merged (serially, as a tree, or
                partitioned by key); cycles from Part 8's model of the core; ledger row 4
    mesi        a scripted MESI sequence for the animation, and coherence traffic of shared against private counters
    falseshare  four counters in one cache line against four lines, measured: atomic increments, 1 .. 4 threads
    litmus      the store-buffering test: simulated (SC, TSO) and run on this machine, with and without a fence
    atomics     four threads incrementing one counter: plain (lost updates), fetch-and-add, CAS, a lock, a spinlock
    jobc        the Job in C on this machine: scalar against AVX2, 1 .. 4 threads; the output checked
    gpu         SIMT divergence: warps of 32 of the Job's word lookups, as they come and sorted by scan length
    workspan    a small computation's DAG and greedy schedules; Brent's bound against greedy on random DAGs; the
                parallel Job's work and span
    stealing    randomized work stealing on a fork-join tree against T1/p + T_inf
    scan        Hillis-Steele and Blelloch scans step by step; the adder's carries as a scan; stream compaction
    sortnet     bitonic and odd-even merge networks; the 0-1 principle checked exhaustively for n <= 10
    amdahl      Amdahl and Gustafson curves, and the Job's strong scaling against them
    topology    ring, mesh, torus, hypercube, tree: degree, diameter and bisection width found by exhaustive search
    top500      supercomputer milestones (cited)
    frontier    the load-buffering test and out-of-thin-air values; dark silicon under post-Dennard scaling
    pieces      the Build problem: 64 pieces taken greedily by 4 cores, then the partitioned merge
"""

from __future__ import annotations

import json
import subprocess
import tempfile
import time
import urllib.request
from pathlib import Path

import numpy as np

from explainer.ai.cache import Cache
from explainer.cs.pebble import coherence as Co
from explainer.cs.pebble import parallel as Pa
from explainer.cs.pebble import programs as P

CACHE = Cache("cs10")
load = CACHE.load
MHZ = 884.9557522123894  # Part 7's clock, kept by the ledger


def _run_c(src: str, args=(), opt="-O2", repeat=1) -> list[str]:
    with tempfile.TemporaryDirectory() as d:
        c, exe = Path(d) / "m.c", Path(d) / "m"
        c.write_text(src)
        subprocess.run(["gcc", opt, "-march=native", "-pthread", "-o", str(exe), str(c), "-lm"], check=True)
        return [subprocess.run([str(exe), *map(str, args)], check=True, capture_output=True, text=True).stdout
                for _ in range(repeat)]


# ---------------------------------------------------------------------------
# fifty years of microprocessors
# ---------------------------------------------------------------------------
RUPP = "https://raw.githubusercontent.com/karlrupp/microprocessor-trend-data/master/50yrs/{}.dat"


def compute_trends() -> dict:
    out = {}
    d = CACHE.dir / "rupp"
    d.mkdir(parents=True, exist_ok=True)
    for name in ("transistors", "frequency", "watts", "specint", "cores"):
        f = d / f"{name}.dat"
        if not f.exists():
            f.write_bytes(urllib.request.urlopen(RUPP.format(name), timeout=60).read())
        pts = []
        for line in f.read_text().splitlines():
            parts = line.split()
            if len(parts) >= 2 and not line.startswith("#"):
                pts.append([float(parts[0]), float(parts[1])])
        out[name] = sorted(pts)
    # the clock's growth before and after 2005 (least squares on log10)
    fr = np.array(out["frequency"])
    rates = {}
    for lo, hi in ((1985, 2004), (2006, 2021)):
        m = (fr[:, 0] >= lo) & (fr[:, 0] <= hi)
        k = np.polyfit(fr[m, 0], np.log10(fr[m, 1]), 1)[0]
        rates[f"{lo}-{hi}"] = 10 ** k - 1
    return {"series": out, "clock_growth": rates, "source": "Karl Rupp, Microprocessor Trend Data (CC BY 4.0), "
            "after Horowitz, Labonte, Shacham, Olukotun, Hammond and Batten"}


# ---------------------------------------------------------------------------
# this machine's threads
# ---------------------------------------------------------------------------
SPIN = r"""
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
static void *work(void *a) { unsigned long x = (unsigned long)a + 1;
  for (long i = 0; i < 400000000L; i++) x = x * 6364136223846793005UL + 1442695040888963407UL; return (void *)x; }
static double now(void) { struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t); return t.tv_sec + 1e-9 * t.tv_nsec; }
int main(int argc, char **argv) { int n = atoi(argv[1]); pthread_t t[64]; double t0 = now();
  for (long k = 0; k < n; k++) pthread_create(&t[k], 0, work, (void *)k);
  for (int k = 0; k < n; k++) pthread_join(t[k], 0);
  printf("%.4f\n", now() - t0); return 0; }
"""


def compute_threads() -> dict:
    """Each thread does the same arithmetic; throughput = threads x one thread's time / the time taken."""
    from videos.cs.cs9.compute import compute_machine

    rows = []
    for n in (1, 2, 3, 4):
        t = min(float(s) for s in _run_c(SPIN, [n], repeat=3))
        rows.append({"threads": n, "seconds": t})
    for r in rows:
        r["throughput"] = r["threads"] * rows[0]["seconds"] / r["seconds"]
    return {"rows": rows, "machine": compute_machine()}


# ---------------------------------------------------------------------------
# the Job on p Pebble cores
# ---------------------------------------------------------------------------
FEATURES = ("bytes", "letters", "caps", "words", "distinct", "scanned", "same_length", "matched")


def _coef() -> dict:
    return json.loads((Cache("cs8").dir / "job.json").read_text())["coef"]


def corpus_tape() -> bytes:
    import videos.ai.ai1.compute as A
    from videos.cs.cs6.compute import novels

    books = novels()
    return P.job_tape("\n".join(books[n] for n in A.BOOKS))


def shards(tape: bytes, p: int) -> list[bytes]:
    """Cut the text into p pieces of nearly equal bytes, at word boundaries."""
    out, s, n = [], 0, len(tape)
    for k in range(1, p + 1):
        e = n if k == p else n * k // p
        while e < n and (65 <= tape[e] <= 90 or 97 <= tape[e] <= 122):
            e += 1
        out.append(tape[s:e])
        s = e
    return out


def table_of(tape: bytes) -> dict[bytes, int]:
    c: dict[bytes, int] = {}
    for w in P.job_words(tape):
        c[w] = c.get(w, 0) + 1
    return c


def merge_features(dst: dict, src: dict) -> tuple[dict, dict]:
    """The work of looking up every entry of ``src`` (in its table order) in the table ``dst`` by the Job's scan,
    adding its count or appending it: the same events :func:`programs.job_features` counts for words, with no text
    to read.  Returns the merged table and the features."""
    index: dict[bytes, int] = {}
    by_len: dict[int, int] = {}
    rank: dict[bytes, int] = {}
    prefix: dict[tuple, int] = {}
    lcp: dict[bytes, int] = {}

    def insert(w):
        n, acc = len(w), 0
        for k in range(1, n + 1):
            key = (n, w[:k])
            acc += prefix.get(key, 0)
            prefix[key] = prefix.get(key, 0) + 1
        lcp[w] = acc
        rank[w] = by_len.get(n, 0)
        index[w] = len(index)
        by_len[n] = by_len.get(n, 0) + 1
        return acc

    for w in dst:
        insert(w)
    sc = same = mt = new = 0
    for w in src:
        i = index.get(w)
        if i is None:
            sc += len(index)
            same += by_len.get(len(w), 0)
            mt += insert(w)
            new += 1
        else:
            sc += i + 1
            same += rank[w] + 1
            mt += lcp[w] + len(w)
    out = dict(dst)
    for w, c in src.items():
        out[w] = out.get(w, 0) + c
    f = {"bytes": 0, "letters": 0, "caps": 0, "words": len(src), "distinct": new, "scanned": sc, "same_length": same,
         "matched": mt}
    return out, f


def _cycles(f: dict, coef: dict, const=True) -> float:
    return (coef["const"] if const else 0.0) + sum(coef[k] * f[k] for k in FEATURES)


def word_hash(w: bytes, p: int) -> int:
    """Which core merges word w: the sum of its letters, mod p (a hash function in miniature: Part 17)."""
    return sum(w) % p


def compute_split() -> dict:
    coef = _coef()
    full = corpus_tape()
    f1 = P.job_features(full)
    one = _cycles(f1, coef)
    rows = []
    for p in (1, 2, 4, 8, 16, 32):
        sh = shards(full, p)
        fs = [P.job_features(x) for x in sh]
        cyc = [_cycles(x, coef) for x in fs]
        tabs = [table_of(x) for x in sh]
        row = {"p": p, "shard_cycles": cyc, "shard_distinct": [x["distinct"] for x in fs],
               "shard_words": [x["words"] for x in fs], "shard_scanned": [x["scanned"] for x in fs]}
        if p > 1:
            m, ser = tabs[0], 0.0
            for t in tabs[1:]:
                m, f = merge_features(m, t)
                ser += _cycles(f, coef, const=False)
            level, tree, tree_levels = tabs, 0.0, []
            while len(level) > 1:
                nxt, costs = [], []
                for a, b in zip(level[::2], level[1::2]):
                    mm, f = merge_features(a, b)
                    nxt.append(mm)
                    costs.append(_cycles(f, coef, const=False))
                tree += max(costs)
                tree_levels.append(costs)
                level = nxt
            part = []
            for k in range(p):
                mk, c = {}, 0.0
                for t in tabs:
                    mk, f = merge_features(mk, {w: n for w, n in t.items() if word_hash(w, p) == k})
                    c += _cycles(f, coef, const=False)
                part.append(c)
            row.update({"serial_merge": ser, "tree_merge": tree, "tree_levels": tree_levels, "part_merge": part,
                        "bytes": [len(x) for x in sh]})
        else:
            row.update({"serial_merge": 0.0, "tree_merge": 0.0, "part_merge": [0.0]})
        mx = max(cyc)
        row["seconds"] = {k: (mx + v) / (MHZ * 1e6) for k, v in (
            ("serial", row["serial_merge"]), ("tree", row["tree_merge"]), ("partitioned", max(row["part_merge"])))}
        row["work_seconds"] = (sum(cyc) + sum(row["part_merge"])) / (MHZ * 1e6)
        row["speedup"] = {k: one / (MHZ * 1e6) / v for k, v in row["seconds"].items()}
        rows.append(row)
        print(p, {k: round(v, 2) for k, v in row["seconds"].items()})
    four = next(r for r in rows if r["p"] == 4)
    ledger = json.loads((Cache("cs9").dir / "ledger.json").read_text())[:4]
    secs = four["seconds"]["partitioned"]
    ledger.append({"part": 10, "label": r"four cores", "seconds": secs, "cycles": secs * MHZ * 1e6,
                   "clock_mhz": MHZ, "cores": 4})
    CACHE.dir.mkdir(parents=True, exist_ok=True)
    (CACHE.dir / "ledger.json").write_text(json.dumps(ledger, indent=1))
    return {"one": {"cycles": one, "seconds": one / (MHZ * 1e6), "distinct": f1["distinct"], "words": f1["words"],
                    "bytes": f1["bytes"],
                    "scanned": f1["scanned"]}, "rows": rows, "ledger": ledger, "note": "row 3's real-memory cost "
            "(+0.05%) is not added: each core's table is smaller still"}


# ---------------------------------------------------------------------------
# coherence
# ---------------------------------------------------------------------------
def compute_mesi() -> dict:
    m = Co.MESI(cores=4)
    script = [(0, "read"), (1, "read"), (0, "write"), (2, "read"), (3, "write"), (3, "write"), (1, "read"),
              (2, "write")]
    steps = []
    for core, op in script:
        ev = m.access(core, 0, write=op == "write", value=len(steps) + 1)
        steps.append({"core": core, "op": op, "event": ev, "states": [m.state(c, 0) for c in range(4)]})
        m.check()
    # two counters, one per core, written alternately: in one line, and in two lines
    out = {"script": steps}
    for name, addrs in (("same line", (0, 8)), ("own lines", (0, 64))):
        mm = Co.MESI(cores=2)
        for t in range(1000):
            c = t % 2
            mm.access(c, addrs[c], write=True, value=t)
        out[name] = dict(mm.stats)
    return out


FALSE_SHARING = r"""
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#define N 50000000L
static int stride; static long *ctr;
static void *work(void *a) { long *c = ctr + (long)a * stride;
  for (long i = 0; i < N; i++) __atomic_fetch_add(c, 1, __ATOMIC_RELAXED); return 0; }
static double now(void) { struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t); return t.tv_sec + 1e-9 * t.tv_nsec; }
int main(int argc, char **argv) { int n = atoi(argv[1]); stride = atoi(argv[2]);
  ctr = aligned_alloc(4096, 4096 * 8); for (int i = 0; i < 4096; i++) ctr[i] = 0;
  pthread_t t[64]; double t0 = now();
  for (long k = 0; k < n; k++) pthread_create(&t[k], 0, work, (void *)k);
  for (int k = 0; k < n; k++) pthread_join(t[k], 0);
  printf("%.3f\n", (now() - t0) * 1e9 / N); return 0; }
"""


def compute_falseshare() -> dict:
    """Nanoseconds per increment per thread: thread k increments counter k, the counters 8 bytes apart (one line) or
    64 bytes apart (a line each)."""
    rows = []
    for n in (1, 2, 3, 4):
        r = {"threads": n}
        for name, stride in (("same", 1), ("padded", 8)):
            r[name] = min(float(s) for s in _run_c(FALSE_SHARING, [n, stride], repeat=3))
        rows.append(r)
    return {"rows": rows}


LITMUS = r"""
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdatomic.h>
#ifdef FENCE
#define F() __asm__ __volatile__("mfence" ::: "memory")
#else
#define F() __asm__ __volatile__("" ::: "memory")
#endif
static volatile int x, y, r0, r1;
static atomic_long go0, go1, done0, done1;
static long iters;
static void *t0(void *a) { for (long i = 1; i <= iters; i++) {
  while (atomic_load_explicit(&go0, memory_order_acquire) != i); x = 1; F(); r0 = y;
  atomic_store_explicit(&done0, i, memory_order_release); } return 0; }
static void *t1(void *a) { for (long i = 1; i <= iters; i++) {
  while (atomic_load_explicit(&go1, memory_order_acquire) != i); y = 1; F(); r1 = x;
  atomic_store_explicit(&done1, i, memory_order_release); } return 0; }
int main(int argc, char **argv) {
  iters = atol(argv[1]); long c[4] = {0};
  pthread_t a, b; pthread_create(&a, 0, t0, 0); pthread_create(&b, 0, t1, 0);
  for (long i = 1; i <= iters; i++) {
    x = 0; y = 0; atomic_thread_fence(memory_order_seq_cst);
    atomic_store_explicit(&go0, i, memory_order_release); atomic_store_explicit(&go1, i, memory_order_release);
    while (atomic_load_explicit(&done0, memory_order_acquire) != i || atomic_load_explicit(&done1, memory_order_acquire) != i);
    c[2 * r0 + r1]++; }
  pthread_join(a, 0); pthread_join(b, 0);
  printf("%ld %ld %ld %ld\n", c[0], c[1], c[2], c[3]); return 0; }
"""


def compute_litmus() -> dict:
    n = 1_000_000
    out = {"simulated": {m: Co.litmus_sb(m, trials=200_000) for m in ("sc", "tso")}, "trials": n}
    for name, opt in (("plain", []), ("mfence", ["-DFENCE"])):
        with tempfile.TemporaryDirectory() as d:
            c, exe = Path(d) / "m.c", Path(d) / "m"
            c.write_text(LITMUS)
            subprocess.run(["gcc", "-O2", "-pthread", *opt, "-o", str(exe), str(c)], check=True)
            v = list(map(int, subprocess.run([str(exe), str(n)], check=True, capture_output=True,
                                             text=True).stdout.split()))
        out[name] = {"r0=0, r1=0": v[0], "r0=0, r1=1": v[1], "r0=1, r1=0": v[2], "r0=1, r1=1": v[3]}
    return out


ATOMICS = r"""
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#define N 10000000L
static volatile long plain; static long atom, cas, locked, tas_count; static volatile int tas_lock;
static pthread_mutex_t mu = PTHREAD_MUTEX_INITIALIZER; static int mode;
static void *work(void *a) {
  for (long i = 0; i < N; i++) switch (mode) {
    case 0: plain = plain + 1; break;
    case 1: __atomic_fetch_add(&atom, 1, __ATOMIC_SEQ_CST); break;
    case 2: { long v = __atomic_load_n(&cas, __ATOMIC_RELAXED);
              while (!__atomic_compare_exchange_n(&cas, &v, v + 1, 1, __ATOMIC_SEQ_CST, __ATOMIC_RELAXED)); } break;
    case 3: pthread_mutex_lock(&mu); locked++; pthread_mutex_unlock(&mu); break;
    case 4: while (__atomic_test_and_set((void *)&tas_lock, __ATOMIC_ACQUIRE)); tas_count++;
            __atomic_clear((void *)&tas_lock, __ATOMIC_RELEASE); break; }
  return 0; }
static double now(void) { struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t); return t.tv_sec + 1e-9 * t.tv_nsec; }
int main(int argc, char **argv) { int n = atoi(argv[1]); mode = atoi(argv[2]); pthread_t t[64]; double t0 = now();
  for (long k = 0; k < n; k++) pthread_create(&t[k], 0, work, 0);
  for (int k = 0; k < n; k++) pthread_join(t[k], 0);
  long v[] = {plain, atom, cas, locked, tas_count};
  printf("%ld %.3f\n", v[mode], (now() - t0) * 1e9 / (N * n)); return 0; }
"""


def compute_atomics() -> dict:
    names = ["plain", "fetch-and-add", "compare-and-swap loop", "mutex", "test-and-set spinlock"]
    rows = []
    for mode, name in enumerate(names):
        r = {"name": name}
        for n in (1, 4):
            runs = [s.split() for s in _run_c(ATOMICS, [n, mode], repeat=3)]
            r[f"t{n}"] = {"count": [int(x[0]) for x in runs], "ns": min(float(x[1]) for x in runs),
                          "expected": 10_000_000 * n}
        rows.append(r)
    return {"rows": rows}


# ---------------------------------------------------------------------------
# the Job in C: SIMD and threads, on this machine
# ---------------------------------------------------------------------------
JOB_C = r"""
// The Job in C: the same linear-scan table as Pebble's program (find the word by scanning from the start, compare
// length then letters).  SIMD=1 compares 32 lengths at once (AVX2), the lengths kept in their own array.  T threads:
// each counts a shard of the text in a private table; then thread k merges the entries whose letter sum is k mod T.
#include <immintrin.h>
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
typedef struct { unsigned char *len; unsigned *off; long *cnt; char *pool; long n, used; } Table;
static int SIMD;
static void tinit(Table *t) { long cap = 1 << 17; t->n = 0; t->used = 0; t->len = aligned_alloc(64, cap + 64);
  memset(t->len, 0, cap + 64); t->off = malloc(4 * cap); t->cnt = malloc(8 * cap); t->pool = malloc(1 << 24); }
static long find(Table *t, const char *w, int L) {
  long n = t->n, i = 0;
  if (SIMD) { __m256i key = _mm256_set1_epi8((char)L);
    for (; i < n; i += 32) {
      unsigned m = (unsigned)_mm256_movemask_epi8(_mm256_cmpeq_epi8(_mm256_load_si256((__m256i *)(t->len + i)), key));
      while (m) { long j = i + __builtin_ctz(m); if (j >= n) return -1;
        if (!memcmp(t->pool + t->off[j], w, L)) return j; m &= m - 1; } }
    return -1; }
  for (; i < n; i++) if (t->len[i] == L && !memcmp(t->pool + t->off[i], w, L)) return i;
  return -1; }
static void add(Table *t, const char *w, int L, long c) {
  long j = find(t, w, L); if (j >= 0) { t->cnt[j] += c; return; }
  j = t->n++; t->len[j] = L; t->off[j] = t->used; memcpy(t->pool + t->used, w, L); t->used += L; t->cnt[j] = c; }
static char *text; static long tlen; static int T; static Table tabs[64], parts[64]; static long cut[65];
static void *count(void *a) {
  long k = (long)a; Table *t = &tabs[k]; tinit(t); char w[256]; int L = 0;
  for (long i = cut[k]; i < cut[k + 1]; i++) { char c = text[i]; if (c >= 'A' && c <= 'Z') c += 32;
    if (c >= 'a' && c <= 'z') { if (L < 255) w[L++] = c; } else if (L) { add(t, w, L, 1); L = 0; } }
  if (L) add(t, w, L, 1);
  return 0; }
static int hash(const char *w, int L) { int s = 0; for (int i = 0; i < L; i++) s += (unsigned char)w[i]; return s % T; }
static void *merge(void *a) { long k = (long)a; Table *p = &parts[k]; tinit(p);
  for (int s = 0; s < T; s++) { Table *t = &tabs[s]; for (long j = 0; j < t->n; j++)
    if (hash(t->pool + t->off[j], t->len[j]) == k) add(p, t->pool + t->off[j], t->len[j], t->cnt[j]); }
  return 0; }
static double now(void) { struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t); return t.tv_sec + 1e-9 * t.tv_nsec; }
int main(int argc, char **argv) {
  T = atoi(argv[2]); SIMD = atoi(argv[3]);
  FILE *f = fopen(argv[1], "rb"); fseek(f, 0, SEEK_END); tlen = ftell(f); fseek(f, 0, SEEK_SET);
  text = malloc(tlen); if (fread(text, 1, tlen, f) != (size_t)tlen) return 1; fclose(f);
  for (int k = 0; k <= T; k++) { long e = k == T ? tlen : tlen * k / T;
    while (k && k < T && e < tlen && ((text[e] >= 'a' && text[e] <= 'z') || (text[e] >= 'A' && text[e] <= 'Z'))) e++;
    cut[k] = e; }
  pthread_t th[64]; double t0 = now();
  for (long k = 0; k < T; k++) pthread_create(&th[k], 0, count, (void *)k);
  for (int k = 0; k < T; k++) pthread_join(th[k], 0);
  double t1 = now();
  if (T > 1) { for (long k = 0; k < T; k++) pthread_create(&th[k], 0, merge, (void *)k);
    for (int k = 0; k < T; k++) pthread_join(th[k], 0); } else parts[0] = tabs[0];
  double t2 = now();
  printf("%.4f %.4f\n", t1 - t0, t2 - t1);
  for (int r = 0; r < 20; r++) { long best = 0; int bk = -1; long bj = -1;
    for (int k = 0; k < T; k++) for (long j = 0; j < parts[k].n; j++) if (parts[k].cnt[j] > best) { best = parts[k].cnt[j]; bk = k; bj = j; }
    if (bk < 0) break;
    printf("%.*s %ld\n", parts[bk].len[bj], parts[bk].pool + parts[bk].off[bj], best); parts[bk].cnt[bj] = -best; }
  return 0; }
"""


def compute_jobc() -> dict:
    full = corpus_tape()
    counts = table_of(full)
    want = sorted(counts.items(), key=lambda kv: -kv[1])[:20]
    rows = []
    with tempfile.TemporaryDirectory() as d:
        src, exe, txt = Path(d) / "job.c", Path(d) / "job", Path(d) / "corpus.txt"
        src.write_text(JOB_C)
        txt.write_bytes(full)
        subprocess.run(["gcc", "-O2", "-march=native", "-pthread", "-o", str(exe), str(src)], check=True)
        for T in (1, 2, 4):
            for simd in (0, 1):
                best = None
                for _ in range(2):
                    out = subprocess.run([str(exe), str(txt), str(T), str(simd)], check=True, capture_output=True,
                                         text=True).stdout.splitlines()
                    count_s, merge_s = map(float, out[0].split())
                    got = [(l.split()[0].encode(), int(l.split()[1])) for l in out[1:]]
                    assert {w: c for w, c in got} == dict(want), "the C Job's top twenty differ"
                    if best is None or count_s + merge_s < best[0] + best[1]:
                        best = (count_s, merge_s)
                rows.append({"threads": T, "simd": bool(simd), "count": best[0], "merge": best[1],
                             "seconds": best[0] + best[1]})
                print(rows[-1])
    return {"rows": rows, "top": [[w.decode(), c] for w, c in want]}


# ---------------------------------------------------------------------------
# GPUs: divergence
# ---------------------------------------------------------------------------
def compute_gpu() -> dict:
    from videos.cs.cs9.compute import scan_ends

    full = corpus_tape()
    ends = scan_ends(full) + 1  # entries each lookup reads
    w = 32
    n = len(ends) // w * w
    e = ends[:n].reshape(-1, w)
    eff = float(e.sum() / (e.max(axis=1).sum() * w))
    srt = np.sort(ends[:n]).reshape(-1, w)
    eff_sorted = float(srt.sum() / (srt.max(axis=1).sum() * w))
    k = len(e) // 2
    example = e[k].tolist()
    return {"warp": w, "efficiency": eff, "efficiency_sorted": eff_sorted, "example": example,
            "example_index": int(k), "lookups": int(n)}


# ---------------------------------------------------------------------------
# work and span, Brent, stealing
# ---------------------------------------------------------------------------
def _small_dag() -> Pa.Dag:
    """A 14-node computation drawn in the chapter (a sum tree beside a chain)."""
    preds = [[], [], [], [], [0, 1], [2, 3], [4, 5], [], [7], [8], [9], [10], [6, 11], [12]]
    return Pa.Dag(len(preds), preds)


def _optimal(d: Pa.Dag, p: int) -> int:
    """The shortest schedule of a small unit-cost DAG on p processors, by search over the sets of finished nodes
    (running fewer than p ready nodes in a step never helps more than running p, but both are tried)."""
    import itertools
    from functools import lru_cache

    full = (1 << d.n) - 1

    @lru_cache(None)
    def best(done: int) -> int:
        if done == full:
            return 0
        ready = [v for v in range(d.n) if not done >> v & 1 and all(done >> u & 1 for u in d.preds[v])]
        k = min(p, len(ready))
        return 1 + min(best(done | sum(1 << v for v in c)) for c in itertools.combinations(ready, k))

    return best(0)


def compute_workspan() -> dict:
    d = _small_dag()
    small = {"preds": d.preds, "work": d.work(), "span": d.span(), "path": d.critical_path(),
             "schedules": {p: Pa.greedy(d, p)["steps"] for p in (1, 2, 3)}, "optimal": {p: _optimal(d, p)
                                                                                     for p in (2, 3)}}
    rows = []
    for seed in range(40):
        g = Pa.Dag.random(2000, width=24, fan=3, seed=seed)
        t1, tinf = g.work(), g.span()
        for p in (1, 2, 4, 8, 16, 32, 64):
            m = Pa.greedy(g, p)["makespan"]
            rows.append({"seed": seed, "p": p, "makespan": m, "t1": t1, "tinf": tinf})
    worst = {}
    for p in (1, 2, 4, 8, 16, 32, 64):
        rs = [r for r in rows if r["p"] == p]
        worst[p] = {"ratio_to_bound": max(r["makespan"] / (r["t1"] / p + r["tinf"]) for r in rs),
                    "ratio_to_lower": max(r["makespan"] / max(r["t1"] / p, r["tinf"]) for r in rs)}
    one = rows[0]["t1"], rows[0]["tinf"]
    ex = [{"p": r["p"], "makespan": r["makespan"]} for r in rows if r["seed"] == 0]
    # the parallel Job: work and span (in seconds), from split
    sp = load("split")
    job = []
    for r in sp["rows"]:
        job.append({"p": r["p"], "work": r["work_seconds"], "span": r["seconds"]["partitioned"]})
    return {"small": small, "random": {"t1": one[0], "tinf": one[1], "example": ex, "worst": worst}, "job": job}


def compute_stealing() -> dict:
    d = Pa.fork_join_tree(11)
    t1, tinf = d.work(), d.span()
    rows = []
    for p in (1, 2, 4, 8, 16, 32, 64):
        runs = [Pa.steal(d, p, seed=s) for s in range(10)]
        rows.append({"p": p, "makespan": float(np.mean([r["makespan"] for r in runs])),
                     "worst": max(r["makespan"] for r in runs), "steals": float(np.mean([r["steals"] for r in runs])),
                     "attempts": float(np.mean([r["attempts"] for r in runs])), "bound": t1 / p + tinf})
    return {"t1": t1, "tinf": tinf, "rows": rows}


# ---------------------------------------------------------------------------
# scans
# ---------------------------------------------------------------------------
def compute_scan() -> dict:
    xs = [3, 1, 4, 1, 5, 9, 2, 6]
    hs = Pa.hillis_steele(xs)
    bl = Pa.blelloch(xs)
    ops = [{"n": 1 << k, "hillis_steele": Pa.hillis_steele([1] * (1 << k))["ops"],
            "blelloch": Pa.blelloch([1] * (1 << k))["ops"], "serial": (1 << k) - 1, "steps_hs": k, "steps_bl": 2 * k}
           for k in range(1, 21)]
    # the adder's carries as a scan (Part 4): (g, p) pairs under (g2, p2) o (g1, p1) = (g2 | p2 & g1, p2 & p1)
    a, b = 0b01101011, 0b00111001
    gp = [((a >> i) & (b >> i) & 1, ((a >> i) ^ (b >> i)) & 1) for i in range(8)]
    pref = Pa.hillis_steele(gp, op=lambda lo, hi: (hi[0] | (hi[1] & lo[0]), hi[1] & lo[1]))["result"]
    carries = [g for g, _ in pref]
    s = sum((((a >> i) ^ (b >> i) ^ (carries[i - 1] if i else 0)) & 1) << i for i in range(8)) + (carries[7] << 8)
    assert s == a + b
    # stream compaction: keep the words of seven letters or more
    words = "it is a truth universally acknowledged that a single man in possession of a good fortune".split()
    flags = [int(len(w) >= 7) for w in words]
    pos = list(np.cumsum([0] + flags[:-1]))
    kept = [w for w, f in zip(words, flags) if f]
    return {"xs": xs, "hillis_steele": hs["levels"], "blelloch_up": bl["up"], "blelloch_down": bl["down"],
            "ops": ops, "adder": {"a": a, "b": b, "gp": gp, "prefix": pref, "sum": s},
            "compact": {"words": words, "flags": flags, "positions": [int(x) for x in pos], "kept": kept}}


# ---------------------------------------------------------------------------
# sorting networks
# ---------------------------------------------------------------------------
def _batcher(n: int) -> list:
    """Batcher's odd-even merge sort for any n: build it for the next power of two and drop every comparator that
    touches a wire >= n (those wires would carry +infinity, so such comparators never move anything)."""
    m = 1
    while m < n:
        m *= 2
    return [(i, j) for i, j in Pa.odd_even_merge(m) if j < n]


def compute_sortnet() -> dict:
    rows = []
    for n in range(2, 11):
        r = {"n": n, "inputs_01": 2 ** n, "permutations": int(np.prod(range(1, n + 1)))}
        for name, net in (("insertion", Pa.insertion(n)), ("transposition", Pa.transposition(n)),
                          ("batcher", _batcher(n))):
            t = time.time()
            ok, _ = Pa.sorts_all_01(net, n)
            r[name] = {"size": len(net), "depth": len(Pa.layers(net)), "sorts": ok, "seconds": time.time() - t}
        if n <= 8:
            r["checked_by_permutations"] = Pa.sorts_all_perms(_batcher(n), n)
        r["best_size"], r["best_depth"] = Pa.BEST_SIZE[n], Pa.BEST_DEPTH[n]
        rows.append(r)
    bit = Pa.bitonic(8)
    broken = [c for k, c in enumerate(_batcher(8)) if k != 11]
    ok, bad = Pa.sorts_all_01(broken, 8)
    big = {}
    for n in (16, 32, 64, 1024):
        big[n] = {"bitonic_size": len(Pa.bitonic(n)), "bitonic_depth": len(Pa.layers(Pa.bitonic(n))),
                  "oem_size": len(Pa.odd_even_merge(n)), "oem_depth": len(Pa.layers(Pa.odd_even_merge(n)))}
    return {"rows": rows, "bitonic8": {"net": bit, "layers": Pa.layers(bit)},
            "batcher8": {"net": _batcher(8), "layers": Pa.layers(_batcher(8))},
            "broken": {"removed": list(_batcher(8)[11]), "sorts": ok, "input": bad, "output": Pa.apply(broken, bad)},
            "big": big}


# ---------------------------------------------------------------------------
# Amdahl and Gustafson; networks; supercomputers
# ---------------------------------------------------------------------------
def compute_amdahl() -> dict:
    ps = [1, 2, 4, 8, 16, 32, 64, 128, 256, 1024]
    curves = {}
    for s in (0.01, 0.05, 0.1, 0.25):
        curves[str(s)] = {"amdahl": [1 / (s + (1 - s) / p) for p in ps], "gustafson": [s + (1 - s) * p for p in ps]}
    sp = load("split")
    job = [{"p": r["p"], **r["speedup"]} for r in sp["rows"]]
    return {"ps": ps, "curves": curves, "job": job}


def compute_topology() -> dict:
    nets = {"ring": Pa.ring(16), "2-D mesh": Pa.mesh(4), "2-D torus": Pa.mesh(4, wrap=True),
            "hypercube": Pa.hypercube(4), "complete": Pa.complete(16)}
    rows = []
    for name, g in nets.items():
        t = time.time()
        bis = Pa.bisection(g, 16)
        links = sum(len(v) for v in g.values()) // 2
        rows.append({"name": name, "n": 16, "links": links, "degree": max(len(v) for v in g.values()),
                     "diameter": Pa.diameter(g), "bisection": bis, "seconds": time.time() - t})
    tr = Pa.tree(8)
    rows.append({"name": "tree", "n": 8, "links": sum(len(v) for v in tr.values()) // 2, "degree": 3,
                 "diameter": Pa.diameter(tr, nodes=list(range(8))), "bisection": Pa.bisection(tr, 8)})
    # formulas for N = 1024 processors
    N = 1024
    formulas = {"ring": {"links": N, "diameter": N // 2, "bisection": 2},
                "2-D mesh": {"links": 2 * 32 * 31, "diameter": 2 * 31, "bisection": 32},
                "2-D torus": {"links": 2 * N, "diameter": 32, "bisection": 64},
                "hypercube": {"links": N * 10 // 2, "diameter": 10, "bisection": N // 2},
                "fat tree": {"links": None, "diameter": 2 * 10, "bisection": N // 2},
                "complete": {"links": N * (N - 1) // 2, "diameter": 1, "bisection": (N // 2) ** 2}}
    return {"rows": rows, "N": N, "formulas": formulas}


def compute_top500() -> dict:
    """Milestones, as published (Top500 lists, Rmax on LINPACK; the Cray-1 at its peak)."""
    return {"milestones": [
        {"year": 1976, "name": "Cray-1", "flops": 160e6, "note": "peak; vector registers"},
        {"year": 1985, "name": "Cray-2", "flops": 1.9e9, "note": "peak"},
        {"year": 1997, "name": "ASCI Red", "flops": 1.068e12, "note": "the first teraflop (Top500)"},
        {"year": 2008, "name": "Roadrunner", "flops": 1.026e15, "note": "the first petaflop"},
        {"year": 2022, "name": "Frontier", "flops": 1.102e18, "note": "the first exaflop"},
        {"year": 2024, "name": "El Capitan", "flops": 1.742e18, "note": "Top500, November 2024"},
    ], "frontier_power_mw": 21.1, "frontier_cores": 8_699_904}


# ---------------------------------------------------------------------------
# the Frontier: load buffering and thin air; dark silicon
# ---------------------------------------------------------------------------
def _lb_outcomes(reorder: bool) -> set:
    """Load buffering: thread 0: r1 = x; y = r1.   thread 1: r2 = y; x = r2.   Enumerate every interleaving (and, if
    ``reorder``, every interleaving where each thread's store may go before its load, as a weak model permits when
    the store does not depend on the load: here it does, so the store writes whatever value r is *at that moment*,
    taken as an unconstrained guess v that must be confirmed by the load).  Values from {0, 1, 42}."""
    out = set()
    import itertools as it

    for guess in ((0, 0), (1, 1), (42, 42), (0, 42), (42, 0)) if reorder else ((None, None),):
        ops0 = [("ld", "x", "r1"), ("st", "y", "r1")]
        ops1 = [("ld", "y", "r2"), ("st", "x", "r2")]
        orders0 = [ops0, ops0[::-1]] if reorder else [ops0]
        orders1 = [ops1, ops1[::-1]] if reorder else [ops1]
        for o0 in orders0:
            for o1 in orders1:
                for pick in it.combinations(range(4), 2):
                    seq, a, b = [], 0, 0
                    for k in range(4):
                        if k in pick:
                            seq.append(o0[a]); a += 1
                        else:
                            seq.append(o1[b]); b += 1
                    mem = {"x": 0, "y": 0}
                    reg = {"r1": guess[0], "r2": guess[1]} if reorder else {}
                    early = {"r1": o0[0][0] == "st", "r2": o1[0][0] == "st"}
                    ok = True
                    for op, var, r in seq:
                        if op == "ld":
                            v = mem[var]
                            if early[r] and reorder and reg[r] != v:
                                ok = False  # the speculated value was not confirmed
                            reg[r] = v
                        else:
                            mem[var] = reg.get(r, 0) if reg.get(r) is not None else 0
                    if ok:
                        out.add((reg["r1"], reg["r2"]))
    return out


def compute_frontier() -> dict:
    sc = sorted(_lb_outcomes(False))
    weak = sorted(_lb_outcomes(True))
    # dark silicon: each generation doubles transistors in the same area; post-Dennard, the switching energy per
    # transistor falls only by ~1/1.4 per generation (voltage nearly flat) instead of 1/2, at a fixed power budget
    gens = list(range(0, 9))
    lit = [min(1.0, 1.4 ** g / 2 ** g) for g in gens]  # the fraction that can switch at full speed
    return {"lb": {"sc": sc, "speculative": weak}, "dark": {"generations": gens, "lit": lit},
            "esmaeilzadeh": "at 8 nm, more than 50% of a chip dark (Esmaeilzadeh et al., ISCA 2011)"}


ITEMS = {
    "trends": compute_trends, "threads": compute_threads, "split": compute_split, "mesi": compute_mesi,
    "falseshare": compute_falseshare, "litmus": compute_litmus, "atomics": compute_atomics, "jobc": compute_jobc,
    "gpu": compute_gpu, "workspan": compute_workspan, "stealing": compute_stealing, "scan": compute_scan,
    "sortnet": compute_sortnet, "amdahl": compute_amdahl, "topology": compute_topology, "top500": compute_top500,
    "frontier": compute_frontier,
}

def compute_pieces() -> dict:
    """The Build problem's answer: cut the text into 64 pieces, each counted in its own table; 4 cores take pieces
    greedily (an idle core takes the next one, which for independent tasks is what work stealing does), then the
    partitioned merge of all 64 tables."""
    import heapq

    coef = _coef()
    full = corpus_tape()
    sh = shards(full, 64)
    cyc = [_cycles(P.job_features(x), coef) for x in sh]
    tabs = [table_of(x) for x in sh]
    free = [(0.0, k) for k in range(4)]
    heapq.heapify(free)
    for c in cyc:
        t, k = heapq.heappop(free)
        heapq.heappush(free, (t + c, k))
    count = max(t for t, _ in free)
    part = []
    for k in range(4):
        mk, c = {}, 0.0
        for t in tabs:
            mk, f = merge_features(mk, {w: n for w, n in t.items() if word_hash(w, 4) == k})
            c += _cycles(f, coef, const=False)
        part.append(c)
    four = next(r for r in load("split")["rows"] if r["p"] == 4)
    return {"pieces": 64, "count_seconds": count / (MHZ * 1e6), "ideal_seconds": sum(cyc) / 4 / (MHZ * 1e6),
            "merge_seconds": max(part) / (MHZ * 1e6), "total_seconds": (count + max(part)) / (MHZ * 1e6),
            "four_shards_seconds": four["seconds"]["partitioned"]}


ITEMS["pieces"] = compute_pieces


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
