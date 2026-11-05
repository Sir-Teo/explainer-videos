"""Precompute everything numerical in Part 16 of *Computer Science, Built* ("Counting Steps").

    python -m videos.cs.cs16.compute              # everything missing
    python -m videos.cs.cs16.compute --force quick

Results are cached in ``.cache/cs16/<name>.json``; scenes call ``load(name)``.  The instruments are
``explainer/cs/algo/sorts.py`` (every sort and selection algorithm, counting its comparisons) and
``explainer/cs/algo/job.py`` (the Job v1, sort then count, in the Pebble language, with the exact model of its
instruction count and a C program that counts the same events on all thirty novels); tested in
tests/test_cs16_sorts.py.  Items that time code (``ram``, ``linear``, ``practice``) run on this machine.

Items:
    hook       the ledger so far; the Job v0's cost per byte as the text grows
    ram        unit cost and its pitfall: repeated squaring of a Python integer, timed
    growth     the growth-rate ladder; Stirling's formula against log n!
    insertion  inversions and comparisons of insertion sort against n(n − 1)/4
    merge      merge sort's recursion tree; comparisons against n lg n
    master     the three cases, with level-by-level costs; Akra–Bazzi
    lower      a decision tree for n = 3; the bound log2 n! against merge insertion and binary insertion
    heap       heapify's linear build; heapsort's comparisons
    quick      quicksort against 2n ln n; pivot rules on sorted input
    concentration  10,000 runs of quicksort: the histogram and its tails
    linear     counting and radix sort against comparison sorts, timed in C on this machine
    select     quickselect and median of medians
    gf         Fibonacci and Catalan from generating functions; asymptotics from the singularity
    amortized  the dynamic array: copies per append, the potential, growth factors 2 and 1.5
    practice   Python's sort on presorted data; replacement selection; Timsort's invariant
    job        the Job v1 on Pebble, its instruction model, all thirty novels: ledger row 7
    frontier   smoothed analysis of quicksort's worst case; integer sorting and fine-grained complexity
"""

from __future__ import annotations

import json
import math
import random
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

import numpy as np

from explainer.ai.cache import Cache

CACHE = Cache("cs16")
load = CACHE.load


def _full_text():
    import videos.ai.ai1.compute as A
    from explainer.cs.pebble import programs as PR
    from videos.cs.cs6.compute import novels
    books = novels()
    return PR.job_tape("\n".join(books[n] for n in A.BOOKS))


def compute_hook() -> dict:
    from explainer.cs.pebble import programs as PR
    led = json.loads((Cache("cs15").dir / "ledger.json").read_text())
    full = _full_text()
    rows = []
    for L in (10_000, 30_000, 100_000, 300_000, 1_000_000, 3_000_000):
        f = PR.job_features(full[:L])
        rows.append({"bytes": L, "cycles": PR.job_cycles(f), "per_byte": PR.job_cycles(f) / L,
                     "distinct": f["distinct"], "words": f["words"]})
        print(rows[-1])
    c6 = json.loads((Cache("cs6").dir / "job.json").read_text())["corpus"]
    rows.append({"bytes": c6["features"]["bytes"], "cycles": c6["cycles"], "per_byte": c6["per_byte"],
                 "distinct": c6["features"]["distinct"], "words": c6["features"]["words"]})
    return {"ledger": led, "growth": rows}


def compute_ram() -> dict:
    rows = []
    x = 3
    for k in range(1, 22):
        t0 = time.perf_counter()
        y = x * x
        dt = time.perf_counter() - t0
        x = y
        rows.append({"step": k, "bits": x.bit_length(), "seconds": dt})
    return {"rows": rows, "python": shutil.which("python3.12") or "python3"}


def compute_growth() -> dict:
    fns = {"lg n": lambda n: math.log2(n), "n": lambda n: n, "n lg n": lambda n: n * math.log2(n),
           "n^2": lambda n: n ** 2, "n^3": lambda n: n ** 3, "2^n": lambda n: 2.0 ** n if n < 1000 else float("inf")}
    ns = [2 ** k for k in range(1, 31)]
    table = {k: [f(n) for n in ns] for k, f in fns.items()}
    stir = []
    for n in (1, 2, 5, 10, 20, 50, 100, 1000):
        exact = math.lgamma(n + 1)
        approx = n * math.log(n) - n + 0.5 * math.log(2 * math.pi * n)
        stir.append({"n": n, "ln_fact": exact, "stirling": approx, "rel_err": (exact - approx) / exact if exact else 0})
    # one-nanosecond steps: the largest n solvable in a second, a day, a year
    budget = {}
    for name, f in fns.items():
        out = {}
        for label, secs in (("second", 1.0), ("day", 86400.0), ("year", 3.15e7)):
            steps = secs * 1e9
            lo, hi = 1, 2
            while f(hi) <= steps and hi < 10 ** 18:
                hi *= 2
            while lo < hi - 1:
                m = (lo + hi) // 2
                if f(m) <= steps:
                    lo = m
                else:
                    hi = m
            out[label] = lo
        budget[name] = out
    return {"ns": ns, "table": {k: [min(v, 1e300) for v in vs] for k, vs in table.items()}, "stirling": stir,
            "budget": budget}


def compute_insertion() -> dict:
    from explainer.cs.algo import sorts as S
    rng = random.Random(16)
    rows = []
    for n in (10, 20, 50, 100, 200, 500, 1000):
        inv, cmp = [], []
        for _ in range(200 if n <= 200 else 40):
            xs = [rng.random() for _ in range(n)]
            inv.append(S.inversions(xs))
            cmp.append(S.insertion_sort(xs)[1]["cmp"])
        rows.append({"n": n, "inv": sum(inv) / len(inv), "cmp": sum(cmp) / len(cmp), "formula": n * (n - 1) / 4})
    ex = [5, 2, 4, 6, 1, 3]
    steps = []
    a = list(ex)
    for i in range(1, len(a)):
        x = a[i]
        j = i - 1
        while j >= 0 and a[j] > x:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = x
        steps.append(list(a))
    return {"rows": rows, "example": ex, "steps": steps,
            "sorted": S.insertion_sort(list(range(1000)))[1]["cmp"],
            "reversed": S.insertion_sort(list(range(1000, 0, -1)))[1]["cmp"]}


def compute_merge() -> dict:
    from explainer.cs.algo import sorts as S
    rng = random.Random(16)
    rows = []
    for k in range(4, 17):
        n = 2 ** k
        xs = [rng.random() for _ in range(n)]
        c = S.merge_sort(xs)[1]["cmp"]
        rows.append({"n": n, "cmp": c, "nlgn": n * k, "worst": n * k - n + 1})
    out, st = S.merge_sort([rng.random() for _ in range(16)])
    return {"rows": rows, "levels16": st["levels"], "lower": [S.lower_bound(2 ** k) for k in range(4, 17)]}


def compute_master() -> dict:
    def levels(a, b, f, n=1024):
        out, m, cnt = [], n, 1
        while m >= 1:
            out.append(cnt * f(m))
            m /= b
            cnt *= a
        return out
    cases = [
        {"name": "binary search", "rec": r"T(n) = T(n/2) + 1", "a": 1, "b": 2, "f": "1", "case": 2,
         "sol": r"\Theta(\log n)", "levels": levels(1, 2, lambda m: 1)},
        {"name": "merge sort", "rec": r"T(n) = 2T(n/2) + n", "a": 2, "b": 2, "f": "n", "case": 2,
         "sol": r"\Theta(n \log n)", "levels": levels(2, 2, lambda m: m)},
        {"name": "Karatsuba", "rec": r"T(n) = 3T(n/2) + n", "a": 3, "b": 2, "f": "n", "case": 1,
         "sol": r"\Theta(n^{\log_2 3}) = \Theta(n^{1.585})", "levels": levels(3, 2, lambda m: m)},
        {"name": "Strassen", "rec": r"T(n) = 7T(n/2) + n^2", "a": 7, "b": 2, "f": "n^2", "case": 1,
         "sol": r"\Theta(n^{\log_2 7}) = \Theta(n^{2.807})", "levels": levels(7, 2, lambda m: m * m)},
        {"name": "a heavy combine", "rec": r"T(n) = 2T(n/2) + n^2", "a": 2, "b": 2, "f": "n^2", "case": 3,
         "sol": r"\Theta(n^2)", "levels": levels(2, 2, lambda m: m * m)},
    ]
    # Akra–Bazzi: T(n) = T(n/3) + T(2n/3) + n, solved numerically
    memo = {}

    def T(n):
        if n <= 1:
            return 1.0
        k = int(n)
        if k in memo:
            return memo[k]
        v = T(n / 3) + T(2 * n / 3) + n
        memo[k] = v
        return v
    ab = [{"n": n, "T": T(n), "ratio": T(n) / (n * math.log2(n))} for n in (10, 100, 1000, 10 ** 4, 10 ** 5, 10 ** 6)]
    return {"cases": cases, "akra_bazzi": ab}


def compute_lower() -> dict:
    from explainer.cs.algo import sorts as S
    tree = S.decision_tree(lambda xs: S.insertion_sort(xs), 3)
    known = {1: 0, 2: 1, 3: 3, 4: 5, 5: 7, 6: 10, 7: 13, 8: 16, 9: 19, 10: 22, 11: 26, 12: 30}
    rows = []
    for n in range(1, 13):
        r = {"n": n, "bound": S.lower_bound(n), "fj": S.ford_johnson_formula(n),
             "binary": sum(math.ceil(math.log2(k)) for k in range(1, n + 1)),
             "merge": n * math.ceil(math.log2(n)) - 2 ** math.ceil(math.log2(n)) + 1 if n > 1 else 0,
             "optimal": known[n]}
        if n <= 8:
            r["fj_checked"] = S.worst_case(S.ford_johnson, n)
        rows.append(r)
        print(r)
    big = []
    for n in (10, 100, 1000, 10 ** 4, 10 ** 5, 10 ** 6):
        lb = math.lgamma(n + 1) / math.log(2)
        big.append({"n": n, "log2fact": lb, "nlgn": n * math.log2(n), "stirling": n * math.log2(n) - n * math.log2(math.e)})
    return {"tree": {"".join(map(str, p)): [[a, b, r] for a, b, r in log] for p, log in tree.items()},
            "rows": rows, "big": big}


def compute_heap() -> dict:
    from explainer.cs.algo import sorts as S
    rng = random.Random(16)
    rows = []
    for k in range(6, 17, 2):
        n = 2 ** k
        xs = [rng.random() for _ in range(n)]
        _, st = S.heapsort(xs)
        rows.append({"n": n, "build": st["build"], "total": st["cmp"], "nlgn": n * k})
    sums = [sum(h / 2 ** h for h in range(1, H + 1)) for H in range(1, 21)]
    return {"rows": rows, "sum_h": sums}


def compute_quick() -> dict:
    from explainer.cs.algo import sorts as S
    rng = random.Random(16)
    rows = []
    for n in (100, 300, 1000, 3000, 10000):
        cs = [S.quicksort([rng.random() for _ in range(n)], "random", rng)[1]["cmp"] for _ in range(60 if n <= 1000 else 15)]
        rows.append({"n": n, "mean": sum(cs) / len(cs), "exact": S.quicksort_expected(n),
                     "approx": 2 * n * math.log(n), "nlgn": n * math.log2(n)})
        print(rows[-1])
    n = 2000
    sorted_in = list(range(n))
    rand_in = [rng.random() for _ in range(n)]
    pivots = {}
    for rule in ("first", "median3", "random"):
        pivots[rule] = {"sorted": S.quicksort(sorted_in, rule, random.Random(1))[1]["cmp"],
                        "random": S.quicksort(rand_in, rule, random.Random(1))[1]["cmp"]}
    return {"rows": rows, "pivots": pivots, "pivot_n": n, "constant": 2 / math.log2(math.e)}


def compute_concentration() -> dict:
    from explainer.cs.algo import sorts as S
    rng = random.Random(1616)
    n, R = 1000, 10000
    base = [rng.random() for _ in range(n)]
    cs = []
    for r in range(R):
        cs.append(S.quicksort(base, "random", random.Random(r))[1]["cmp"])
    a = np.array(cs, dtype=float)
    mu, sd = float(a.mean()), float(a.std())
    hist, edges = np.histogram(a, bins=40)
    tails = {k: float(np.mean(a > mu + k * sd)) for k in (1, 2, 3, 4)}
    return {"n": n, "runs": R, "mean": mu, "sd": sd, "sd_over_n": sd / n, "exact_mean": S.quicksort_expected(n),
            "theory_sd_over_n": math.sqrt(7 - 2 * math.pi ** 2 / 3), "hist": hist.tolist(), "edges": edges.tolist(),
            "tails": tails, "max": float(a.max()), "min": float(a.min()), "worst": n * (n - 1) / 2}


LINEAR_C = r"""
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>
static double now(void){ struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t); return t.tv_sec + t.tv_nsec / 1e9; }
static int cmp(const void *a, const void *b){ uint32_t x = *(const uint32_t*)a, y = *(const uint32_t*)b; return (x > y) - (x < y); }
static void radix(uint32_t *a, uint32_t *t, size_t n){
  for (int s = 0; s < 32; s += 8) {
    size_t c[257] = {0};
    for (size_t i = 0; i < n; i++) c[((a[i] >> s) & 255) + 1]++;
    for (int k = 0; k < 256; k++) c[k + 1] += c[k];
    for (size_t i = 0; i < n; i++) t[c[(a[i] >> s) & 255]++] = a[i];
    memcpy(a, t, n * sizeof *a);
  }
}
static void counting(uint32_t *a, size_t n, uint32_t k){
  size_t *c = calloc(k, sizeof *c);
  for (size_t i = 0; i < n; i++) c[a[i]]++;
  size_t o = 0; for (uint32_t v = 0; v < k; v++) for (size_t j = 0; j < c[v]; j++) a[o++] = v;
  free(c);
}
int main(int argc, char **argv){
  size_t n = (size_t)atol(argv[1]);
  uint32_t *a = malloc(n * 4), *b = malloc(n * 4), *t = malloc(n * 4);
  uint64_t s = 88172645463325252ULL;
  for (size_t i = 0; i < n; i++) { s ^= s << 13; s ^= s >> 7; s ^= s << 17; a[i] = (uint32_t)s; }
  memcpy(b, a, n * 4); double t0 = now(); qsort(b, n, 4, cmp); double tq = now() - t0;
  memcpy(t, b, n * 4);
  memcpy(b, a, n * 4); t0 = now(); radix(b, t + 0, n); double tr = now() - t0;
  for (size_t i = 1; i < n; i++) if (b[i - 1] > b[i]) { printf("radix wrong\n"); return 1; }
  for (size_t i = 0; i < n; i++) b[i] = a[i] & 65535;
  t0 = now(); counting(b, n, 65536); double tc = now() - t0;
  printf("%.6f %.6f %.6f\n", tq, tr, tc);
}
"""

LINEAR_CPP = r"""
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <vector>
int main(int argc, char **argv){
  size_t n = (size_t)atol(argv[1]);
  std::vector<uint32_t> a(n);
  uint64_t s = 88172645463325252ULL;
  for (auto &x : a) { s ^= s << 13; s ^= s >> 7; s ^= s << 17; x = (uint32_t)s; }
  auto t0 = std::chrono::steady_clock::now(); std::sort(a.begin(), a.end());
  double t = std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count();
  printf("%.6f\n", t);
}
"""


def compute_linear() -> dict:
    rows = []
    with tempfile.TemporaryDirectory() as d:
        Path(d, "l.c").write_text(LINEAR_C)
        Path(d, "l.cpp").write_text(LINEAR_CPP)
        subprocess.run(["gcc", "-O2", "-o", "l", "l.c"], cwd=d, check=True)
        subprocess.run(["g++", "-O2", "-o", "lp", "l.cpp"], cwd=d, check=True)
        for n in (10 ** 5, 10 ** 6, 10 ** 7):
            best = None
            for _ in range(3):
                q, r, c = map(float, subprocess.run(["./l", str(n)], cwd=d, capture_output=True, text=True,
                                                    check=True).stdout.split())
                sp = float(subprocess.run(["./lp", str(n)], cwd=d, capture_output=True, text=True, check=True).stdout)
                cur = {"n": n, "qsort": q, "std_sort": sp, "radix": r, "counting": c}
                best = cur if best is None else {k: min(best[k], cur[k]) for k in cur}
            rows.append(best)
            print(best)
    return {"rows": rows, "gcc": subprocess.run(["gcc", "--version"], capture_output=True, text=True).stdout.splitlines()[0]}


def compute_select() -> dict:
    from explainer.cs.algo import sorts as S
    rng = random.Random(16)
    rows = []
    for n in (101, 1001, 10001, 100001):
        xs = [rng.random() for _ in range(n)]
        k = n // 2
        qs = [S.quickselect(xs, k, random.Random(r))[1]["cmp"] for r in range(20)]
        mv, st = S.median_of_medians(xs, k)
        assert mv == sorted(xs)[k]
        rows.append({"n": n, "quick": sum(qs) / len(qs), "mom": st["cmp"], "sort": n * math.log2(n)})
        print(rows[-1])
    return {"rows": rows, "quick_theory": 2 + 2 * math.log(2)}


def compute_gf() -> dict:
    from math import comb, sqrt
    phi = (1 + sqrt(5)) / 2
    fib = [0, 1]
    for _ in range(60):
        fib.append(fib[-1] + fib[-2])
    binet = [round((phi ** n - (-1 / phi) ** n) / sqrt(5)) for n in range(len(fib))]
    cat = [1]
    for n in range(1, 61):
        cat.append(sum(cat[i] * cat[n - 1 - i] for i in range(n)))
    closed = [comb(2 * n, n) // (n + 1) for n in range(61)]
    asym = [{"n": n, "ratio": cat[n] / (4 ** n / (math.sqrt(math.pi) * n ** 1.5))} for n in (1, 2, 5, 10, 20, 40, 60)]
    return {"fib": fib[:21], "fib_ok": fib == binet, "catalan": cat[:13], "catalan_ok": cat == closed,
            "asym": asym, "phi": phi}


def compute_amortized() -> dict:
    from explainer.cs.algo import sorts as S
    seq = []
    cap, size = 1, 0
    for i in range(1, 65):
        cost = 1
        if size == cap:
            cost += size
            cap *= 2
        size += 1
        seq.append({"i": i, "cost": cost, "cap": cap, "phi": 2 * size - cap})
    return {"seq": seq, "two": S.dynamic_array(10 ** 6, 2.0), "one_half": S.dynamic_array(10 ** 6, 1.5),
            "golden": (1 + math.sqrt(5)) / 2}


def compute_practice() -> dict:
    from explainer.cs.algo import sorts as S
    rng = random.Random(16)
    n = 100_000
    data = {"random": [rng.random() for _ in range(n)], "sorted": list(range(n)), "reversed": list(range(n, 0, -1)),
            "ten runs": sum((sorted(rng.random() for _ in range(n // 10)) for _ in range(10)), []),
            "sorted, 1% shuffled": None}
    s = list(range(n))
    for _ in range(n // 100):
        i, j = rng.randrange(n), rng.randrange(n)
        s[i], s[j] = s[j], s[i]
    data["sorted, 1% shuffled"] = s
    rows = []
    for name, xs in data.items():
        rows.append({"input": name, "timsort": S.timsort_cmp(xs), "merge": S.merge_sort(xs)[1]["cmp"],
                     "nlgn": n * math.log2(n)})
        print(rows[-1])
    runs = S.replacement_selection([rng.random() for _ in range(200_000)], 1000)
    return {"rows": rows, "n": n, "rs_runs": len(runs), "rs_mean": sum(runs[1:-1]) / max(len(runs) - 2, 1),
            "rs_m": 1000, "rs_records": 200_000}


def compute_job() -> dict:
    """Ledger row 7: the Job v1 compiled from the Pebble language.  Instructions for the thirty novels from the exact
    model fitted on passages; cycles at the IPC measured on Part 8's core."""
    from explainer.cs.algo import job as J
    from explainer.cs.pebble import programs as PR
    from videos.cs.cs8.compute import core
    from videos.cs.cs13.compute import _tapes
    c = J.compile_job()
    samples = []
    for t in _tapes(40, 100, 3000, seed=16):
        m = J.run(c, t)
        assert bytes(m.output) == PR.job_reference(t)
        samples.append((J.features(t), m.steps))
    model = J.fit(samples[:30])
    held = [{"bytes": f["bytes"], "steps": s, "predicted": J.predict(model, f)} for f, s in samples[30:]]
    held_err = max(abs(h["predicted"] - h["steps"]) / h["steps"] for h in held)
    full = _full_text()
    ff, out = J.features_native(full)
    assert out == PR.job_reference(full)
    instr = J.predict(model, ff)
    # IPC on the out-of-order core, on the passages that priced rows 3 and 5
    cyc = ins = 0
    for t in _tapes(6, 1200, 2600)[:3]:
        q = core(c.program.image, t)
        assert bytes(q.output) == PR.job_reference(t)
        cyc += q.cycles
        ins += q.committed
    ipc = ins / cyc
    led = json.loads((Cache("cs15").dir / "ledger.json").read_text())[:7]
    row5 = led[5]
    cycles = instr / ipc
    seconds = cycles / (row5["clock_mhz"] * 1e6)
    led.append({"part": 16, "label": r"sort, then count", "seconds": seconds, "cycles": cycles,
                "clock_mhz": row5["clock_mhz"], "instructions": instr, "ipc": ipc})
    CACHE.dir.mkdir(parents=True, exist_ok=True)
    (CACHE.dir / "ledger.json").write_text(json.dumps(led, indent=1))
    c6 = json.loads((Cache("cs6").dir / "job.json").read_text())["corpus"]["features"]
    return {"model": model, "held": held, "held_err": held_err, "train_err": model["max_rel_err"],
            "features": ff, "instructions": instr, "ipc": ipc, "seconds": seconds, "ledger": led,
            "v0": {"scanned": c6["scanned"], "same_length": c6["same_length"], "words": c6["words"],
                   "distinct": c6["distinct"]},
            "speedup_vs_row5": row5["seconds"] / seconds, "speedup_vs_row4": led[4]["seconds"] / seconds,
            "source": J.JOB_SORT.strip().splitlines()}


def compute_frontier() -> dict:
    from explainer.cs.algo import sorts as S
    n = 2000
    rows = []
    for sigma in (0.0, 1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2, 0.1, 0.3, 1.0):
        cs = []
        for r in range(10):
            rng = random.Random(r)
            xs = [i / n + rng.gauss(0, sigma) for i in range(n)]
            cs.append(S.quicksort(xs, "first", random.Random(0))[1]["cmp"])
        rows.append({"sigma": sigma, "cmp": sum(cs) / len(cs)})
        print(rows[-1])
    return {"n": n, "rows": rows, "worst": n * (n - 1) / 2, "average": S.quicksort_expected(n)}


ITEMS = {
    "hook": compute_hook, "ram": compute_ram, "growth": compute_growth, "insertion": compute_insertion,
    "merge": compute_merge, "master": compute_master, "lower": compute_lower, "heap": compute_heap,
    "quick": compute_quick, "concentration": compute_concentration, "linear": compute_linear,
    "select": compute_select, "gf": compute_gf, "amortized": compute_amortized, "practice": compute_practice,
    "job": compute_job, "frontier": compute_frontier,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
