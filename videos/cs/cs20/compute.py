"""Precompute everything numerical in Part 20 of *Computer Science, Built* ("Randomness as a Resource").

    python -m videos.cs.cs20.compute              # everything missing
    python -m videos.cs.cs20.compute --force job

Results are cached in ``.cache/cs20/<name>.json``; scenes call ``load(name)``.  The instruments are
``explainer/cs/algo/randomized.py`` (Freivalds, Schwartz-Zippel and the Tutte matrix, Karger and Karger-Stein,
Fermat and Miller-Rabin, random-walk SAT, balls into bins, Bloom filters, reservoir sampling, Misra-Gries, Count-Min,
HyperLogLog, KMV, the AMS sketch, MinHash and LSH, Moser-Tardos, conditional expectations, RANDU) and
``explainer/cs/algo/job3.py`` (the Job v3: Count-Min and a heap, in the Pebble language), tested in
tests/test_cs20_randomized.py.  ``job`` emulates every instruction of the Job v3 on the thirty novels (about a
quarter of an hour) and writes ledger row 9.

Items:
    hook       the Job in kilobytes: memory and answers of rows 8 and 9
    freivalds  checking a matrix product: error per round, time against multiplying
    pit        Schwartz-Zippel; perfect matchings by the Tutte matrix; fingerprints
    karger     contraction on a two-cluster graph: success rate against 2/(n(n-1)); Karger-Stein
    primes     Fermat liars and Carmichael numbers; Miller-Rabin's worst liar rate; big primes timed
    walks      2-SAT by random walk against n^2; Schoening's 3-SAT walk against (4/3)^n
    bins       maximum load with one and two choices
    bloom      Bloom filters on the novels' vocabulary against (1 - e^{-kn/m})^k
    stream     reservoir sampling's uniformity; Misra-Gries; Count-Min against its guarantee
    job        the Job v3 on the emulator: ledger row 9
    sweep      the same algorithm in C: sketch sizes and hash seeds swept
    hll        HyperLogLog and KMV on the novels: error against 1.04/sqrt(m)
    ams        the AMS F2 sketch: median of means
    minhash    MinHash and LSH: near-duplicate paragraphs in the novels
    probmethod Ramsey's bound; Moser-Tardos resampling
    derand     MAX-CUT by conditional expectations; RANDU's planes; generators
"""

from __future__ import annotations

import json
import math
import random
import subprocess
import tempfile
import time
from collections import Counter
from pathlib import Path

import numpy as np

from explainer.ai.cache import Cache

CACHE = Cache("cs20")
load = CACHE.load


def _full_text():
    from videos.cs.cs16.compute import _full_text as f
    return f()


def _best(f, reps=3):
    best, out = math.inf, None
    for _ in range(reps):
        t0 = time.perf_counter()
        out = f()
        best = min(best, time.perf_counter() - t0)
    return best, out


SWEEP_C = r"""
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
/* The Job v3's algorithm (Count-Min, conservative or plain update, K candidates) for many sketch sizes and hash
   seeds.  argv: file d w K conservative mult.  Prints the twenty reported words with their estimates. */
#define P 16777213L
int main(int argc, char **argv) {
  FILE *f = fopen(argv[1], "rb"); fseek(f, 0, SEEK_END); long sz = ftell(f); fseek(f, 0, SEEK_SET);
  unsigned char *t = malloc(sz); if (fread(t, 1, sz, f) != (size_t)sz) return 1; fclose(f);
  int d = atoi(argv[2]), w = atoi(argv[3]), K = atoi(argv[4]), cons = atoi(argv[5]); long mult = atol(argv[6]);
  long *cm = calloc((size_t)d * w, sizeof(long));
  char cw[64][40]; int cl[64]; long ce[64]; int nc = 0;
  char word[80]; int n = 0; long h = 0;
  for (long i = 0; i <= sz; i++) {
    int c = i < sz ? t[i] : -1;
    if (c >= 'A' && c <= 'Z') c += 32;
    if (c >= 'a' && c <= 'z') { if (n < 72) word[n] = c; n++; h = (mult * h + c) % P; continue; }
    if (n == 0) continue;
    long g = 1 + (h / w) % (w - 1), idx[8], m = -1;
    for (int r = 0; r < d; r++) { idx[r] = r * (long)w + (h + r * g) % w; if (m < 0 || cm[idx[r]] < m) m = cm[idx[r]]; }
    for (int r = 0; r < d; r++) { if (!cons || cm[idx[r]] == m) cm[idx[r]]++; }
    m = cm[idx[0]]; for (int r = 1; r < d; r++) if (cm[idx[r]] < m) m = cm[idx[r]];
    int mi = 0; for (int e = 1; e < nc; e++) if (ce[e] < ce[mi]) mi = e;
    if (n <= 32 && (nc < K || m > ce[mi])) {
      int e = -1; for (int q = 0; q < nc; q++) if (cl[q] == n && !memcmp(cw[q], word, n)) { e = q; break; }
      if (e >= 0) ce[e] = m;
      else { e = nc < K ? nc++ : mi; memcpy(cw[e], word, n); cl[e] = n; ce[e] = m; }
    }
    n = 0; h = 0;
  }
  for (int e = 0; e < nc; e++) printf("%.*s\n", cl[e], cw[e]);
  printf("--\n");
  for (int s = 0; s < 20 && s < nc; s++) {
    int b = 0; for (int e = 1; e < nc; e++) if (ce[e] > ce[b]) b = e;
    printf("%.*s %ld\n", cl[b], cw[b], ce[b]); ce[b] = -1;
  }
  return 0;
}
"""


def _sweep(full: bytes, configs, seeds) -> list:
    from explainer.cs.pebble import programs as PR
    exact_words = PR.job_words(full)
    counts = Counter(exact_words)
    rows = []
    with tempfile.TemporaryDirectory() as d:
        Path(d, "s.c").write_text(SWEEP_C)
        subprocess.run(["gcc", "-O2", "-o", "s", "s.c"], cwd=d, check=True)
        Path(d, "t").write_bytes(full)
        for dd, w, k, cons in configs:
            res = []
            for s in seeds:
                out = subprocess.run(["./s", "t", str(dd), str(w), str(k), str(int(cons)), str(33 + 2 * s)], cwd=d,
                                     capture_output=True, check=True).stdout
                cands, rest = out.split(b"--\n")
                cands = set(cands.split())
                rep = [ln.rsplit(b" ", 1) for ln in rest.strip().split(b"\n")]
                true_top = [w_ for w_, _ in sorted(counts.items(), key=lambda kv: -kv[1])[:20]]
                got = [w_ for w_, _ in rep]
                errs = [(int(e) - counts[w_]) / counts[w_] for w_, e in rep]
                res.append({"seed": s, "covered": set(true_top) <= cands,
                            "exact": all(int(e) == counts[w_] for w_, e in rep) and set(got) == set(true_top),
                            "overlap": len(set(got) & set(true_top)), "max_err": max(errs),
                            "intruder": [(w_.decode(), int(e), counts[w_]) for w_, e in rep if w_ not in true_top]})
            rows.append({"d": dd, "w": w, "k": k, "conservative": cons, "kb": dd * w * 4 / 1024,
                         "exact_share": sum(r["exact"] for r in res) / len(res),
                         "mean_overlap": sum(r["overlap"] for r in res) / len(res),
                         "worst_overlap": min(r["overlap"] for r in res),
                         "mean_max_err": sum(r["max_err"] for r in res) / len(res),
                         "example_intruder": next((r["intruder"][0] for r in res if r["intruder"]), None),
                         "covered_share": sum(r["covered"] for r in res) / len(res),
                         "exact_seeds": [r["seed"] for r in res if r["exact"]]})
            print(rows[-1])
    return rows


def compute_job() -> dict:
    """Ledger row 9: the Job v3 compiled from the Pebble language, every instruction emulated on the thirty novels;
    cycles at the IPC measured on Part 8's core (as rows 3, 5, 7 and 8 were priced), plus every miss that Part 9's
    hierarchy sees, each charged its full latency."""
    from explainer.cs.algo import job3 as J
    from explainer.cs.pebble import programs as PR
    from explainer.cs.pebble.emu import Machine
    from videos.cs.cs8.compute import core
    from videos.cs.cs9.compute import pebble_hierarchy
    from videos.cs.cs13.compute import _tapes
    c = J.compile_job()
    full = _full_text()
    # every instruction, on the emulator
    t0 = time.perf_counter()
    m = J.run(c, full, max_steps=4_000_000_000)
    emu_s = time.perf_counter() - t0
    out = bytes(m.output)
    ref, est = J.reference(full)
    assert out == ref, "the emulator and the Python reference disagree"
    exact = PR.job_reference(full)
    instr = m.steps
    print("steps", instr, "emulated in", emu_s)
    # IPC on the out-of-order core, on passages of 1-3 kB
    cyc = ins = 0
    for t in _tapes(6, 1200, 2600)[:3]:
        q = core(c.program.image, t)
        assert bytes(q.output) == J.reference(t)[0]
        cyc += q.cycles
        ins += q.committed
    ipc = ins / cyc
    # the memory hierarchy: every load and store of a long passage, through Part 9's caches
    hier, lat = pebble_hierarchy()

    class Traced(Machine):
        def load(self, addr, size, signed_=False):
            if addr < 0x80000000:
                traced["acc"] += 1
                traced["lines"].add(addr // 64)
                traced["stall"] += hier.access(addr) - lat[0]
            return super().load(addr, size, signed_)

        def store(self, addr, size, value):
            if addr < 0x80000000:
                traced["acc"] += 1
                traced["lines"].add(addr // 64)
                traced["stall"] += hier.access(addr, write=True) - lat[0]
            return super().store(addr, size, value)
    traced = {"acc": 0, "lines": set(), "stall": 0}
    passage = full[3_000_000:3_150_000]
    tm = Traced(image=c.program.image, tape=passage)
    tm.run(400_000_000)
    lines = traced["lines"]
    sets = Counter(ln % 64 for ln in lines)          # L1: 32 KB, 8 ways, 64-byte lines: 64 sets
    # every line is touched in the first few hundred words and never evicted, so the corpus pays the same misses
    stall = traced["stall"]
    fp = J.footprint(c)
    led = json.loads((Cache("cs17").dir / "ledger.json").read_text())[:9]
    row8 = led[8]
    cycles = instr / ipc + stall
    seconds = cycles / (row8["clock_mhz"] * 1e6)
    # memory: the v2 keeps every distinct word; the v3 keeps the sketch and 32 candidates
    j17 = json.loads((Cache("cs17").dir / "job.json").read_text())
    vocab = Counter(PR.job_words(full))
    v2_bytes = sum(len(w) for w in vocab) + 4 * j17["final_cap"] + 16 * len(vocab)
    v3_bytes = fp["bytes"]
    led.append({"part": 20, "label": r"Count-Min and a heap", "seconds": seconds, "cycles": cycles,
                "clock_mhz": row8["clock_mhz"], "instructions": instr, "ipc": ipc, "stall_cycles": stall,
                "memory_bytes": v3_bytes})
    led[8]["memory_bytes"] = v2_bytes
    CACHE.dir.mkdir(parents=True, exist_ok=True)
    (CACHE.dir / "ledger.json").write_text(json.dumps(led, indent=1))
    rep = [ln.rsplit(b" ", 1) for ln in out.strip().split(b"\n")]
    n_words = len(PR.job_words(full))
    return {"instructions": instr, "per_byte": instr / len(full), "emulated_s": emu_s, "ipc": ipc,
            "seconds": seconds, "cycles": cycles, "stall_cycles": stall, "stall_share": stall / cycles,
            "traced_accesses": traced["acc"], "traced_lines": len(lines), "max_lines_per_set": max(sets.values()),
            "passage_bytes": len(passage), "latencies": lat,
            "output": out.decode(), "exact": out == exact, "report": [[w.decode(), int(e)] for w, e in rep],
            "footprint": fp["bytes"], "globals": {k: v[1] for k, v in fp["globals"].items()},
            "v2_bytes": v2_bytes, "v3_bytes": v3_bytes, "memory_ratio": v2_bytes / v3_bytes,
            "vocab": len(vocab), "words": n_words, "ledger": led,
            "slower_than_row8": seconds / row8["seconds"], "row8_seconds": row8["seconds"],
            "cm_bound": math.e * n_words / 1021, "cm_delta": math.exp(-4),
            "source": J.JOB_SKETCH.strip().splitlines()}


def compute_sweep() -> dict:
    """The Job v3's algorithm in C, for seven sketch shapes and twenty hash functions each (seed 0 is the
    program's)."""
    full = _full_text()
    rows = _sweep(full, [(4, 1021, 32, True), (4, 1021, 32, False), (4, 509, 32, True), (2, 1021, 32, True),
                         (4, 2039, 32, True), (4, 4093, 32, True), (3, 1021, 32, True)], range(20))
    return {"rows": rows, "seeds": 20}


def _vocab_counts():
    from explainer.cs.pebble import programs as PR
    return Counter(PR.job_words(_full_text()))


def compute_lasvegas() -> dict:
    """Las Vegas: randomized quicksort is always right, and its time is random; Monte Carlo: a fixed time, and the
    answer is random.  Comparisons over many runs; amplification of a one-sided error."""
    from explainer.cs.algo.sorts import quicksort
    rng = random.Random(20)
    n = 2000
    a = list(range(n))
    runs = [quicksort(a, "random", rng)[1]["cmp"] for _ in range(400)]
    mean = sum(runs) / len(runs)
    sd = (sum((r - mean) ** 2 for r in runs) / len(runs)) ** 0.5
    expect = 2 * (n + 1) * sum(1 / k for k in range(1, n + 1)) - 4 * n
    hist, edges = np.histogram(runs, bins=24)
    amp = [{"rounds": k, "error": 0.5 ** k} for k in (1, 2, 5, 10, 20, 40)]
    return {"n": n, "runs": len(runs), "mean": mean, "sd": sd, "expected": expect, "min": min(runs), "max": max(runs),
            "worst": n * (n - 1) / 2, "hist": hist.tolist(), "edges": edges.tolist(), "amplify": amp}


def compute_freivalds() -> dict:
    from explainer.cs.algo import randomized as R
    rng = np.random.default_rng(1977)
    n = 2000
    A = rng.integers(-9, 10, (n, n)).astype(np.float64)
    B = rng.integers(-9, 10, (n, n)).astype(np.float64)
    t_mul, C = _best(lambda: A @ B)
    r = rng.integers(0, 2, n).astype(np.float64)
    t_chk, _ = _best(lambda: np.array_equal(A @ (B @ r), C @ r))
    # one wrong entry: a round passes exactly when that column's coin is 0
    C1 = C.copy()
    C1[123, 456] += 1
    trials = 4000
    small = rng.integers(-9, 10, (200, 200)).astype(np.float64), rng.integers(-9, 10, (200, 200)).astype(np.float64)
    Cs = small[0] @ small[1]
    W1 = Cs.copy()
    W1[12, 45] += 1
    W2 = Cs + rng.integers(0, 2, Cs.shape)            # many wrong entries
    pass1 = sum(R.freivalds(*small, W1, 1, rng) for _ in range(trials)) / trials
    pass2 = sum(R.freivalds(*small, W2, 1, rng) for _ in range(trials)) / trials
    pass_k = [{"rounds": k, "measured": sum(R.freivalds(*small, W1, k, rng) for _ in range(trials)) / trials,
               "bound": 0.5 ** k} for k in (1, 2, 3, 4, 6)]
    caught = not R.freivalds(A, B, C1, 30, rng)
    flops_mul = 2 * n ** 3
    flops_chk = 3 * 2 * n ** 2
    return {"n": n, "t_mul": t_mul, "t_check": t_chk, "ratio": t_mul / t_chk, "pass_one_wrong": pass1,
            "pass_many_wrong": pass2, "rounds": pass_k, "caught_30": caught, "trials": trials,
            "flops_mul": flops_mul, "flops_check": flops_chk}


def compute_pit() -> dict:
    """Schwartz-Zippel on a false identity; the Tutte matrix against Edmonds' algorithm; a fingerprint of the
    corpus."""
    import networkx as nx

    from explainer.cs.algo import randomized as R
    rng = random.Random(1979)
    # claim: (x - y)(y - z)(z - x) = x^2 z - x^2 y + y^2 x - y^2 z + z^2 y - z^2 x  ... with one sign wrong
    true = lambda x, y, z: (x - y) * (y - z) * (z - x)                       # noqa: E731
    claim = lambda x, y, z: x * x * z - x * x * y + y * y * x - y * y * z + z * z * y + z * z * x  # noqa: E731
    sz = []
    for S in (2, 4, 10, 30, 100, 1000):
        tr = 20000
        agree = sum(R.schwartz_zippel_trial(true, claim, 3, S, rng) for _ in range(tr)) / tr
        sz.append({"S": S, "agree": agree, "bound": min(1.0, 3 / S)})
    # Vandermonde: det V(x_1..x_n) = prod_{i<j} (x_j - x_i), checked at random points mod p
    p = 2_147_483_647
    vn = 8
    ok = 0
    for _ in range(50):
        xs = [rng.randrange(p) for _ in range(vn)]
        V = [[pow(x, k, p) for k in range(vn)] for x in xs]
        prod = 1
        for i in range(vn):
            for j in range(i + 1, vn):
                prod = prod * (xs[j] - xs[i]) % p
        ok += R.det_mod(V, p) == prod
    vander_terms = math.factorial(vn)
    # perfect matchings: Tutte's determinant against Edmonds' blossoms
    rows = []
    for n in (40, 60, 80, 100):
        pr = 1.15 * math.log(n) / n                            # near the threshold: about half have one
        agree = 0
        have = 0
        t_t = t_e = 0.0
        G_ = 12
        for g in range(G_):
            es = [(u, v) for u in range(n) for v in range(u + 1, n) if rng.random() < pr]
            t0 = time.perf_counter()
            a = R.tutte_has_perfect_matching(n, es, rng)
            t_t += time.perf_counter() - t0
            G = nx.Graph()
            G.add_nodes_from(range(n))
            G.add_edges_from(es)
            t0 = time.perf_counter()
            b = len(nx.max_weight_matching(G, maxcardinality=True)) == n // 2
            t_e += time.perf_counter() - t0
            agree += a == b
            have += b
        rows.append({"n": n, "graphs": G_, "agree": agree, "with_pm": have, "t_tutte": t_t / G_, "t_edmonds": t_e / G_})
        print(rows[-1])
    # fingerprints: two copies of the corpus, one byte apart
    full = _full_text()
    other = bytearray(full)
    other[12_345_678] ^= 1
    q = R.random_prime(61, rng)
    t_fp, fa = _best(lambda: R.fingerprint(full, q), 1)
    fb = R.fingerprint(bytes(other), q)
    bits = 8 * len(full)
    primes_61 = 2 ** 60 / (61 * math.log(2))                      # primes in [2^60, 2^61)
    bad = bits / 60                                               # prime factors >= 2^60 of a number below 2^bits
    return {"sz": sz, "degree": 3, "vandermonde": {"n": vn, "trials": 50, "ok": ok, "terms": vander_terms},
            "tutte": rows, "fp_prime": q, "fp_a": fa, "fp_b": fb, "fp_differ": fa != fb, "fp_seconds": t_fp,
            "bytes": len(full), "fp_false_bound": bad / primes_61, "bad_primes": bad, "primes_61": primes_61}


def compute_karger() -> dict:
    from explainer.cs.algo import randomized as R
    rng = random.Random(1993)
    # two dense clusters joined by three edges
    n = 16
    while True:          # two dense clusters, every vertex of degree at least 4 inside its own: the bridges are the
        es = [(u, v) for g in (0, 8) for u in range(g, g + 8) for v in range(u + 1, g + 8) if rng.random() < 0.7]
        deg = Counter(x for e in es for x in e)
        if min(deg[v] for v in range(n)) >= 4:          # only minimum cut
            break
    es += [(0, 8), (3, 11), (6, 13)]
    true_cut = 3
    trials = 20000
    cuts = Counter(R.karger(n, es, rng) for _ in range(trials))
    succ = cuts[true_cut] / trials
    bound = 2 / (n * (n - 1))
    # the cycle: C(n, 2) minimum cuts, each found with probability exactly 1/C(n, 2)
    cn = 10
    cyc = [(i, (i + 1) % cn) for i in range(cn)]
    found = Counter()
    for _ in range(20000):
        _, groups = R.karger_trace(cn, cyc, rng)
        found[tuple(min(groups, key=lambda g: (0 not in g, g)))] += 1
    # traces for drawing: the first seeds that succeed and fail
    def trace(want):
        for sd in range(1000):
            mg, gr = R.karger_trace(n, es, random.Random(sd))
            side = set(gr[0])
            c = sum((u in side) != (v in side) for u, v in es)
            if (c == true_cut) == want:
                return mg, gr, c
    merges, groups, _ = trace(True)
    fail_merges, fail_groups, fail_cut = trace(False)
    # Karger-Stein against repeated Karger on a larger graph
    m = 48
    es2 = [(u, v) for g in (0, 24) for u in range(g, g + 24) for v in range(u + 1, g + 24) if rng.random() < 0.35]
    es2 += [(1, 30), (10, 40), (20, 25), (5, 47)]
    deg = Counter()
    for u, v in es2:
        deg[u] += 1
        deg[v] += 1
    true2 = min(4, min(deg.values()))
    tk, tks = 0.0, 0.0
    sk = sks = 0
    R_ = 200
    for _ in range(R_):
        t0 = time.perf_counter()
        sk += R.karger(m, es2, rng) == true2
        tk += time.perf_counter() - t0
    for _ in range(40):
        t0 = time.perf_counter()
        sks += R.karger_stein(m, es2, rng) == true2
        tks += time.perf_counter() - t0
    return {"n": n, "edges": es, "m": len(es), "true_cut": true_cut, "trials": trials, "success": succ,
            "bound": bound, "cuts": {str(k): v for k, v in sorted(cuts.items())}, "cycle_n": cn,
            "cycle_mincuts": len(found), "cycle_expected": math.comb(cn, 2),
            "cycle_min_share": min(found.values()) / 20000, "cycle_max_share": max(found.values()) / 20000,
            "trace": merges, "groups": groups, "fail_trace": fail_merges,
            "fail_groups": fail_groups, "fail_cut": fail_cut, "ks_n": m, "ks_m": len(es2), "ks_true": true2,
            "karger_success": sk / R_, "karger_s": tk / R_, "ks_success": sks / 40, "ks_s": tks / 40}


def compute_primes() -> dict:
    from explainer.cs.algo import randomized as R
    cm = R.carmichaels(1_000_000)
    n = 561
    fermat = sum(R.fermat_liar(a, n) for a in range(1, n))
    strong = sum(R.mr_liar(a, n) for a in range(1, n))
    coprime = sum(math.gcd(a, n) == 1 for a in range(1, n))
    worst, at = 0.0, 0
    for c in range(9, 20000, 2):
        if R.miller_rabin(c, 20, random.Random(c)):
            continue
        lr = sum(R.mr_liar(a, c) for a in range(1, c)) / (c - 1)
        if lr > worst:
            worst, at = lr, c
    rng = random.Random(30)
    times = []
    for bits in (256, 512, 1024, 2048):
        t0 = time.perf_counter()
        reps = 3 if bits < 2048 else 1
        for _ in range(reps):
            R.random_prime(bits, rng)
        times.append({"bits": bits, "seconds": (time.perf_counter() - t0) / reps,
                      "candidates": round(bits * math.log(2) / 2)})
        print(times[-1])
    p = R.random_prime(1024, rng)
    t_round, _ = _best(lambda: R.mr_liar(rng.randrange(2, p - 1), p), 5)
    return {"carmichael_count": len(cm), "carmichaels": cm[:12], "n": n, "fermat_liars": fermat,
            "strong_liars": strong, "coprime": coprime, "factors": [3, 11, 17], "worst_rate": worst, "worst_n": at,
            "times": times, "round_1024": t_round, "trial_division_bits": 512}


def compute_walks() -> dict:
    from explainer.cs.algo import randomized as R
    rng = random.Random(1991)
    two = []
    for n in (20, 40, 80, 160, 320):
        flips = []
        for _ in range(12):
            cl = R.random_2sat(n, 2 * n, rng)
            flips.append(R.walk_sat(n, cl, rng, 100 * n * n))
        two.append({"n": n, "mean": sum(flips) / len(flips), "max": max(flips), "bound": 2 * n * n})
        print(two[-1])
    # Schoening on random 3-SAT at the threshold with exactly one satisfying assignment (checked by brute force):
    # the walk must find that one point.  Restarts of 3n flips until success, against (4/3)^n
    three = []
    for n in (8, 10, 12, 14, 16, 18, 20):
        m = round(4.26 * n)
        inst = []
        xs = np.arange(1 << n)
        while len(inst) < 6:
            cl = [tuple((v, rng.random() < 0.5) for v in rng.sample(range(n), 3)) for _ in range(m)]
            sat = np.ones(1 << n, dtype=bool)
            for c in cl:
                sat &= np.logical_or.reduce([((xs >> v) & 1).astype(bool) == s for v, s in c])
            if int(sat.sum()) == 1:
                inst.append(cl)
        restarts = []
        for cl in inst:
            for _ in range(8):
                f = R.walk_sat(n, cl, rng, 10 ** 8, k_restart=3 * n)
                restarts.append(f // (3 * n) + 1)
        three.append({"n": n, "m": m, "mean_restarts": sum(restarts) / len(restarts), "schoening": (4 / 3) ** n,
                      "brute": 2 ** n})
        print(three[-1])
    return {"two": two, "three": three}


def compute_bins() -> dict:
    from explainer.cs.algo import randomized as R
    rng = np.random.default_rng(1999)
    rows = []
    for n in (10 ** 3, 10 ** 4, 10 ** 5, 10 ** 6):
        one = [R.max_load(n, 1, rng) for _ in range(5)]
        two = [R.max_load(n, 2, rng) for _ in range(3 if n < 10 ** 6 else 1)]
        rows.append({"n": n, "one": max(one), "one_mean": sum(one) / len(one), "two": max(two),
                     "theory_one": math.log(n) / math.log(math.log(n)), "theory_two": math.log(math.log(n)) / math.log(2)})
        print(rows[-1])
    n = 10 ** 6
    h1 = np.bincount(np.bincount(rng.integers(0, n, n), minlength=n)).tolist()
    load = np.zeros(n, dtype=np.int32)
    for row in rng.integers(0, n, (n, 2)):
        b = row[0] if load[row[0]] <= load[row[1]] else row[1]
        load[b] += 1
    h2 = np.bincount(load).tolist()
    # a small animation: 24 balls into 12 bins, each with its two choices
    small = rng.integers(0, 12, (24, 2)).tolist()
    return {"rows": rows, "hist_one": h1, "hist_two": h2, "small": small}


def compute_bloom() -> dict:
    from explainer.cs.algo import randomized as R
    vocab = list(_vocab_counts())
    n = len(vocab)
    rng = random.Random(1970)
    probes = []
    vs = set(vocab)
    while len(probes) < 100_000:
        w = "".join(rng.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(rng.randint(4, 9))).encode()
        if w not in vs:
            probes.append(w)
    rows = []
    for bpw in (4, 8, 10, 16):
        m = bpw * n
        for k in (1, 2, 3, 4, 6, 7, 8, 11, 12):
            if bpw != 10 and k not in (1, 3, round(bpw * math.log(2)), 8):
                continue
            b = R.Bloom(m, k)
            for w in vocab:
                b.add(w)
            fp = sum(w in b for w in probes) / len(probes)
            rows.append({"bits_per_word": bpw, "k": k, "measured": fp, "theory": R.bloom_theory(n, m, k),
                         "fill": float(b.bits.mean())})
            print(rows[-1])
    assert all(w in b for w in vocab)
    # a tiny one to draw: 32 bits, 3 hashes, six words
    tiny = R.Bloom(32, 3)
    words = [b"whale", b"sea", b"ship", b"captain", b"harpoon", b"queequeg"]
    idx = {w.decode(): tiny._idx(w) for w in words}
    for w in words:
        tiny.add(w)
    queries = {w: (tiny._idx(w.encode()), w.encode() in tiny) for w in ("ocean", "dog", "boat", "rope", "sail", "deck",
                                                                       "mast", "oar")}
    return {"n": n, "probes": len(probes), "rows": rows, "tiny_idx": idx, "tiny_queries": queries,
            "kb_10": 10 * n / 8 / 1024, "vocab_bytes": sum(len(w) for w in vocab)}


def compute_stream() -> dict:
    from explainer.cs.algo import randomized as R
    from explainer.cs.pebble import programs as PR
    rng = random.Random(1985)
    counts = [0] * 100
    trials = 50_000
    for _ in range(trials):
        for x in R.reservoir(range(100), 5, rng):
            counts[x] += 1
    expect = trials * 5 / 100
    words = PR.job_words(_full_text())
    N = len(words)
    sample = [w.decode() for w in R.reservoir(words, 8, rng)]
    c = Counter(words)
    top = [w for w, _ in c.most_common(20)]
    mg = R.misra_gries(words, 100)
    mg_rows = [{"word": w.decode(), "true": c[w], "mg": mg.get(w, 0)} for w in top]
    # plain Count-Min, vectorized: every word's estimate against the e N / w guarantee
    keys = list(c)
    true = np.array([c[w] for w in keys], dtype=np.int64)
    hs = []
    for w in keys:
        h = 0
        for ch in w:
            h = (33 * h + ch) % 16777213
        hs.append(h)
    hs = np.array(hs, dtype=np.int64)
    out = {}
    for d, w in ((4, 1021), (4, 4093), (2, 1021)):
        g = 1 + (hs // w) % (w - 1)
        est = np.full(len(keys), np.iinfo(np.int64).max)
        for r in range(d):
            idx = (hs + r * g) % w
            row = np.bincount(idx, weights=true, minlength=w).astype(np.int64)
            est = np.minimum(est, row[idx])
        err = est - true
        bound = math.e * N / w
        out[f"{d}x{w}"] = {"d": d, "w": w, "bound": bound, "over_bound": float(np.mean(err > bound)),
                           "delta": math.exp(-d), "mean_err": float(err.mean()), "median_err": float(np.median(err)),
                           "exact_share": float(np.mean(err == 0)),
                           "top_err": [int(err[keys.index(t)]) for t in top]}
        print(f"{d}x{w}", out[f"{d}x{w}"]["over_bound"], out[f"{d}x{w}"]["mean_err"])
    return {"trials": trials, "k": 5, "of": 100, "counts_min": min(counts), "counts_max": max(counts),
            "expect": expect, "counts": counts, "N": N, "sample": sample, "mg_k": 100, "mg_bound": N / 100,
            "mg": mg_rows, "mg_kept": len(mg), "cm": out, "distinct": len(c)}


def compute_hll() -> dict:
    from explainer.cs.algo import randomized as R
    from explainer.cs.pebble import programs as PR
    words = PR.job_words(_full_text())
    distinct = len(set(words))
    vocab = list(set(words))
    rows = []
    for b in (4, 6, 8, 10, 12, 14):
        errs, kerrs = [], []
        for seed in range(30):
            h = R._h64(vocab, seed)
            errs.append(R.hyperloglog(h, b) / distinct - 1)
            if seed < 10:
                kerrs.append(R.kmv(h, 1 << b) / distinct - 1)
        m = 1 << b
        rows.append({"b": b, "m": m, "bytes": m * 6 / 8, "rmse": float(np.sqrt(np.mean(np.square(errs)))),
                     "theory": 1.04 / math.sqrt(m), "kmv_rmse": float(np.sqrt(np.mean(np.square(kerrs)))),
                     "kmv_theory": 1 / math.sqrt(m - 2), "kmv_bytes": m * 8})
        print(rows[-1])
    # the stream itself: hashing the whole corpus once (repeats do not change the registers)
    t0 = time.perf_counter()
    hw = R._h64(words, 0)
    t_hash = time.perf_counter() - t0
    est = R.hyperloglog(hw, 12)
    # five-word phrases: millions of distinct items, the same 3 KB of registers
    K = 5
    sh = [b" ".join(words[i:i + K]) for i in range(0, len(words) - K + 1)]
    true_sh = len(set(sh))
    est_sh = R.hyperloglog(R._h64(sh, 0), 12)
    # the registers for drawing, at m = 64
    h = R._h64(vocab, 0)
    idx = (h >> np.uint64(58)).astype(np.int64)
    reg = np.zeros(64, dtype=np.int64)
    rest = h << np.uint64(6)
    lz = np.array([64 - int(x).bit_length() if x else 58 for x in rest.tolist()])
    np.maximum.at(reg, idx, np.minimum(lz + 1, 59))
    return {"distinct": distinct, "words": len(words), "rows": rows, "est_corpus": est, "t_hash": t_hash,
            "shingles": len(sh), "true_shingles": true_sh, "est_shingles": est_sh, "registers64": reg.tolist()}


def compute_ams() -> dict:
    from explainer.cs.algo import randomized as R
    c = _vocab_counts()
    f2 = sum(v * v for v in c.values())
    rng = np.random.default_rng(1996)
    rows = []
    for k in (4, 16, 64, 256):
        errs = []
        for _ in range(40):
            errs.append(R.ams_f2(None, c, k, 1, rng) / f2 - 1)
        med = []
        for _ in range(40):
            med.append(R.ams_f2(None, c, k, 9, rng) / f2 - 1)
        rows.append({"k": k, "rmse_mean": float(np.sqrt(np.mean(np.square(errs)))), "theory": math.sqrt(2 / k),
                     "worst_mean": float(np.max(np.abs(errs))), "worst_median9": float(np.max(np.abs(med)))})
        print(rows[-1])
    one = [R.ams_f2(None, c, 1, 1, rng) / f2 for _ in range(400)]
    return {"f2": f2, "distinct": len(c), "words": sum(c.values()), "rows": rows, "single": one,
            "single_mean": float(np.mean(one)), "the": c[b"the"] ** 2 / f2}


def compute_minhash() -> dict:
    """Near-duplicate paragraphs among the thirty novels: 5-word shingles, 100 MinHashes, 20 bands of 5."""
    import videos.ai.ai1.compute as A
    from videos.cs.cs6.compute import novels
    import re
    from collections import defaultdict
    books = novels()
    paras = []
    for bk in A.BOOKS:
        for p in books[bk].split("\n"):
            w = re.findall(r"[a-z]+", p.lower())
            if len(w) >= 40:
                paras.append((bk, w, p))
    K, NP, p_ = 5, 100, (1 << 31) - 1

    def shingle_ids(w):
        import zlib
        return [zlib.crc32(" ".join(w[i:i + K]).encode()) & 0x7fffffff for i in range(len(w) - K + 1)]
    ids, bounds = [], [0]
    for _, w, _ in paras:
        ids += shingle_ids(w)
        bounds.append(len(ids))
    x = np.array(ids, dtype=np.int64)
    rng = np.random.default_rng(1998)
    a, b = rng.integers(1, p_, NP), rng.integers(0, p_, NP)
    starts = np.array(bounds[:-1])
    t0 = time.perf_counter()
    sig = np.zeros((len(paras), NP), dtype=np.int64)
    for k in range(NP):
        sig[:, k] = np.minimum.reduceat((a[k] * x + b[k]) % p_, starts)
    t_sig = time.perf_counter() - t0

    def bands(sig, R_, B_):
        cand = set()
        for band in range(B_):
            d = defaultdict(list)
            for i, row in enumerate(map(tuple, sig[:, band * R_:(band + 1) * R_])):
                d[row].append(i)
            for v in d.values():
                for i in range(len(v)):
                    for j in range(i + 1, len(v)):
                        cand.add((v[i], v[j]))
        return cand
    t0 = time.perf_counter()
    cand = bands(sig, 5, 20)
    t_band = time.perf_counter() - t0

    def sh(i):
        return set(x[bounds[i]:bounds[i + 1]].tolist())
    found = sorted(((len(sh(i) & sh(j)) / len(sh(i) | sh(j)), i, j) for i, j in cand), reverse=True)
    # ground truth: every pair that shares a phrase, by an inverted index
    inv = defaultdict(list)
    for i in range(len(paras)):
        for s in sh(i):
            inv[s].append(i)
    pc = Counter()
    for v in inv.values():
        if 1 < len(v) <= 60:
            for i in range(len(v)):
                for j in range(i + 1, len(v)):
                    pc[(v[i], v[j])] += 1
    size = [len(sh(i)) for i in range(len(paras))]
    truth = sorted(((cnt / (size[i] + size[j] - cnt), i, j) for (i, j), cnt in pc.items()), reverse=True)
    truth = [t for t in truth if t[0] >= 0.2]
    pairs = [{"j": J, "a": A.BOOKS[paras[i][0]] if isinstance(A.BOOKS, dict) else str(paras[i][0]),
              "b": A.BOOKS[paras[j][0]] if isinstance(A.BOOKS, dict) else str(paras[j][0]),
              "text_a": paras[i][2][:160], "text_b": paras[j][2][:160], "found": (i, j) in cand}
             for J, i, j in truth]
    # planted near-duplicates: a paragraph and an edited copy, at every similarity, against 1 - (1 - s^5)^20
    prng = random.Random(5)
    planted = []
    for _ in range(600):
        i = prng.randrange(len(paras))
        w = list(paras[i][1])
        rate = prng.uniform(0.0, 0.25)
        w2 = [prng.choice(w) if prng.random() < rate else t for t in w]
        s1, s2 = set(shingle_ids(w)), set(shingle_ids(w2))
        J = len(s1 & s2) / len(s1 | s2)
        xs1, xs2 = np.array(sorted(s1)), np.array(sorted(s2))
        g1 = np.min((a[:, None] * xs1[None, :] + b[:, None]) % p_, axis=1)
        g2 = np.min((a[:, None] * xs2[None, :] + b[:, None]) % p_, axis=1)
        hit = any(np.array_equal(g1[k * 5:(k + 1) * 5], g2[k * 5:(k + 1) * 5]) for k in range(20))
        planted.append((J, hit, float(np.mean(g1 == g2))))
    curve = []
    for lo in np.arange(0, 1.0, 0.1):
        pts = [h for J, h, _ in planted if lo <= J < lo + 0.1]
        if pts:
            mid = lo + 0.05
            curve.append({"lo": float(lo), "n": len(pts), "hit": sum(pts) / len(pts),
                          "theory": 1 - (1 - mid ** 5) ** 20})
    est_err = float(np.sqrt(np.mean([(e - J) ** 2 for J, _, e in planted])))
    n = len(paras)
    return {"paragraphs": n, "shingles": len(x), "pairs": n * (n - 1) // 2, "candidates": len(cand),
            "t_sig": t_sig, "t_band": t_band, "found": [[J, paras[i][2][:120], paras[j][2][:120]] for J, i, j in found],
            "truth": pairs, "truth_count": len(truth), "recall": sum(p["found"] for p in pairs if p["j"] >= 0.5),
            "truth_05": sum(p["j"] >= 0.5 for p in pairs), "curve": curve, "est_rmse": est_err,
            "est_theory": 1 / math.sqrt(NP) / 2}


def compute_probmethod() -> dict:
    from explainer.cs.algo import randomized as R
    ram = []
    for k in range(3, 21):
        n = k
        while R.ramsey_expected(n + 1, k) < 1:
            n += 1
        ram.append({"k": k, "n": n, "floor": math.floor(2 ** (k / 2))})
    known = {3: 6, 4: 18}
    rng = random.Random(1947)
    # K_17 has a colouring with no monochromatic K_4 (the Paley graph); random colourings find many
    n = 17
    quads = [q for q in __import__("itertools").combinations(range(n), 4)]
    mono = []
    for _ in range(200):
        col = {(u, v): rng.random() < 0.5 for u in range(n) for v in range(u + 1, n)}
        cnt = 0
        for q in quads:
            es = [col[(q[i], q[j])] for i in range(4) for j in range(i + 1, 4)]
            cnt += all(es) or not any(es)
        mono.append(cnt)
    qr = {(x * x) % 17 for x in range(1, 17)}
    paley = 0
    for q in quads:
        es = [((q[j] - q[i]) % 17) in qr for i in range(4) for j in range(i + 1, 4)]
        paley += all(es) or not any(es)
    # Moser-Tardos: dense 10-SAT, each clause sharing variables with a few hundred others (inside the LLL condition)
    mt = []
    for nv in (2000, 8000, 32000):
        k = 10
        m = 5 * nv // 2
        cl = [tuple((v, rng.random() < 0.5) for v in rng.sample(range(nv), k)) for _ in range(m)]
        occ = Counter(v for c in cl for v, _ in c)
        dmax = max(sum(occ[v] - 1 for v, _ in c) for c in cl)
        x0 = [rng.random() < 0.5 for _ in range(nv)]
        bad0 = sum(1 for c in cl if not any(x0[v] == s for v, s in c))
        steps, x = R.moser_tardos(nv, cl, rng)
        assert all(any(x[v] == s for v, s in c) for c in cl)
        mt.append({"n": nv, "m": m, "k": k, "d": dmax, "lll": math.e * (dmax + 1) * 2 ** -k, "resamplings": steps,
                   "bound": m / dmax, "initial_bad": bad0})
        print(mt[-1])
    return {"ramsey": ram, "known": known, "k4_mean": sum(mono) / len(mono), "k4_min": min(mono),
            "k4_expected": math.comb(17, 4) * 2 ** -5, "paley": paley, "mt": mt}


def compute_derand() -> dict:
    from explainer.cs.algo import randomized as R
    rng = random.Random(1964)
    n = 60
    es = [(u, v) for u in range(n) for v in range(u + 1, n) if rng.random() < 0.15]
    cut, side = R.maxcut_conditional(n, es)
    rand = []
    for _ in range(2000):
        s = [rng.random() < 0.5 for _ in range(n)]
        rand.append(sum(1 for u, v in es if s[u] != s[v]))
    xs = R.randu(1, 3 * 4000)
    tri = [[xs[3 * i] / 2 ** 31, xs[3 * i + 1] / 2 ** 31, xs[3 * i + 2] / 2 ** 31] for i in range(4000)]
    # the planes: 9x - 6y + z is an integer for every triple; count the distinct integers
    planes = sorted({round(9 * a - 6 * b + c) for a, b, c in tri})
    mt = np.random.Generator(np.random.MT19937(1)).random((4000, 3)).tolist()
    return {"n": n, "m": len(es), "cut": cut, "half": len(es) / 2, "rand_mean": sum(rand) / len(rand),
            "rand_max": max(rand), "rand_min": min(rand), "randu": tri, "planes": planes, "mt": mt}


ITEMS = {
    "lasvegas": compute_lasvegas,
    "freivalds": compute_freivalds,
    "pit": compute_pit,
    "karger": compute_karger,
    "primes": compute_primes,
    "walks": compute_walks,
    "bins": compute_bins,
    "bloom": compute_bloom,
    "stream": compute_stream,
    "job": compute_job,
    "sweep": compute_sweep,
    "hll": compute_hll,
    "ams": compute_ams,
    "minhash": compute_minhash,
    "probmethod": compute_probmethod,
    "derand": compute_derand,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
