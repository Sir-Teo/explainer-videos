"""Research method (Part 61), computed.  Measurement bias (Mytkowicz, Diwan, Hauswirth and Sweeney 2009) reproduced
on this machine: the same C program, compiled once, timed with environment blocks of growing size and with its
object files linked in different orders; rigorous timing (Georges, Buytaert and Eeckhout 2007): repeated runs,
bootstrap confidence intervals, and why speedups are averaged geometrically; small cases of open conjectures
checked by computer; and the open problems the series met, with their records."""

from __future__ import annotations

import subprocess
import tempfile
import time
from pathlib import Path

import numpy as np

KERNEL = r"""
#include <stdint.h>
extern uint32_t mix(uint32_t h, uint32_t c);
uint64_t count(const unsigned char *s, long n) {
    uint32_t h = 2166136261u; uint64_t words = 0, acc = 0; int in = 0;
    for (long i = 0; i < n; i++) {
        unsigned c = s[i] | 32;
        if (c >= 'a' && c <= 'z') { h = mix(h, c); in = 1; }
        else if (in) { acc += h & 1023; words++; h = 2166136261u; in = 0; }
    }
    return acc + words;
}
"""
MIX = r"""
#include <stdint.h>
uint32_t mix(uint32_t h, uint32_t c) { return (h ^ c) * 16777619u; }
"""
MAIN = r"""
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>
extern uint64_t count(const unsigned char *s, long n);
int main(int argc, char **argv) {
    long n = 1 << 24; unsigned char *buf = malloc(n);
    uint32_t x = 12345;
    for (long i = 0; i < n; i++) { x = x * 1103515245u + 12345u; buf[i] = (x >> 16) % 7 ? 'a' + (x >> 20) % 26 : ' '; }
    struct timespec t0, t1; uint64_t r = 0;
    clock_gettime(CLOCK_MONOTONIC, &t0);
    for (int k = 0; k < 4; k++) r += count(buf, n);
    clock_gettime(CLOCK_MONOTONIC, &t1);
    printf("%.6f %llu\n", (t1.tv_sec - t0.tv_sec) + 1e-9 * (t1.tv_nsec - t0.tv_nsec), (unsigned long long) r);
    return 0;
}
"""


def _build(d: Path, order: tuple[str, ...]) -> Path:
    for name, src in (("kernel.c", KERNEL), ("mix.c", MIX), ("main.c", MAIN)):
        (d / name).write_text(src)
    objs = []
    for name in ("kernel", "mix", "main"):
        subprocess.run(["gcc", "-O2", "-c", f"{name}.c", "-o", f"{name}.o"], cwd=d, check=True)
        objs.append(f"{name}.o")
    exe = d / ("job_" + "_".join(order))
    subprocess.run(["gcc", "-O2", *[f"{o}.o" for o in order], "-o", exe.name], cwd=d, check=True)
    return exe


def _time(exe: Path, env_bytes: int = 0) -> float:
    env = {"PATH": "/usr/bin:/bin", "PAD": "x" * env_bytes}
    out = subprocess.run([str(exe)], env=env, capture_output=True, text=True, check=True).stdout.split()
    return float(out[0])


def measurement_bias(env_sizes=range(0, 4097, 128), orders=(("kernel", "mix", "main"), ("main", "mix", "kernel"),
                                                           ("mix", "main", "kernel")), reps: int = 5) -> dict:
    """The same program timed with the environment padded by 0 to 4,096 bytes (which shifts the initial stack), and
    with three link orders.  Each point is the median of ``reps`` runs, interleaved so that slow drift of the
    machine is spread across all settings."""
    with tempfile.TemporaryDirectory() as td:
        d = Path(td)
        exes = {"+".join(o): _build(d, o) for o in orders}
        base = exes["+".join(orders[0])]
        env_rows = {e: [] for e in env_sizes}
        for r in range(reps):
            for e in env_sizes:
                env_rows[e].append(_time(base, e))
        link_rows = {k: [] for k in exes}
        for r in range(reps * 3):
            for k, exe in exes.items():
                link_rows[k].append(_time(exe, 0))
    env = [{"bytes": e, "median": float(np.median(v)), "min": float(min(v))} for e, v in env_rows.items()]
    med = [r["median"] for r in env]
    link = [{"order": k, "median": float(np.median(v)), "min": float(min(v)), "runs": v} for k, v in link_rows.items()]
    return {"env": env, "env_spread": (max(med) - min(med)) / min(med), "link": link,
            "link_spread": (max(r["median"] for r in link) - min(r["median"] for r in link)) /
            min(r["median"] for r in link), "reps": reps}


def bootstrap(xs, stat=np.median, B: int = 10_000, alpha: float = 0.05, seed: int = 0):
    rng = np.random.default_rng(seed)
    xs = np.asarray(xs)
    boots = np.array([stat(rng.choice(xs, len(xs))) for _ in range(B)])
    return float(np.quantile(boots, alpha / 2)), float(np.quantile(boots, 1 - alpha / 2))


def job_timing(runs: int = 30) -> dict:
    """The Job in plain Python on the thirty novels (Counter over regular-expression words), timed ``runs`` times:
    the distribution, its mean and median with bootstrap 95% intervals, and how the interval narrows with runs."""
    import re
    from collections import Counter
    from videos.cs.cs6.compute import novels
    text = " ".join(novels().values()).lower()
    word = re.compile(r"[a-z]+")
    times = []
    for _ in range(runs):
        t0 = time.perf_counter()
        Counter(word.findall(text)).most_common(20)
        times.append(time.perf_counter() - t0)
    widths = []
    for k in (3, 5, 10, 20, runs):
        lo, hi = bootstrap(times[:k], np.mean, B=4000)
        widths.append({"runs": k, "lo": lo, "hi": hi, "mean": float(np.mean(times[:k]))})
    return {"times": times, "mean": float(np.mean(times)), "median": float(np.median(times)),
            "ci_mean": bootstrap(times, np.mean), "ci_median": bootstrap(times, np.median), "narrowing": widths,
            "bytes": len(text)}


def speedup_means() -> dict:
    """Why speedups are averaged geometrically: program A is 2x faster on one benchmark and 2x slower on another.
    The arithmetic mean of the ratios says A is faster whichever way round you divide; the geometric mean says they
    tie, either way round (Fleming and Wallace 1986)."""
    a = np.array([1.0, 4.0])
    b = np.array([2.0, 2.0])
    r1, r2 = b / a, a / b
    return {"times_a": a.tolist(), "times_b": b.tolist(), "ratios_b_over_a": r1.tolist(),
            "arith_b_over_a": float(r1.mean()), "arith_a_over_b": float(r2.mean()),
            "geo_b_over_a": float(np.exp(np.log(r1).mean())), "geo_a_over_b": float(np.exp(np.log(r2).mean()))}


# ---------------------------------------------------------------- conjectures checked by computer

def goldbach(limit: int = 2_000_000) -> dict:
    """Every even number from 4 to ``limit`` is a sum of two primes (checked), with the even numbers that need the
    largest smallest prime.  Oliveira e Silva, Herzog and Pardi (2014) verified it to 4 x 10^18."""
    sieve = np.ones(limit + 1, bool)
    sieve[:2] = False
    for p in range(2, int(limit ** 0.5) + 1):
        if sieve[p]:
            sieve[p * p::p] = False
    primes = np.flatnonzero(sieve)
    need = np.zeros(limit + 1, np.int32)
    remaining = np.arange(4, limit + 1, 2)
    for p in primes:
        if len(remaining) == 0:
            break
        ok = sieve[remaining - p] if p < remaining.min() else None
        if ok is None:
            mask = remaining - p >= 2
            ok = np.zeros(len(remaining), bool)
            ok[mask] = sieve[remaining[mask] - p]
        need[remaining[ok]] = p
        remaining = remaining[~ok]
    evens = np.arange(4, limit + 1, 2)
    worst = evens[np.argmax(need[evens])]
    records = []
    best = 0
    for e in evens:
        if need[e] > best:
            best = int(need[e])
            records.append({"n": int(e), "p": best})
    return {"limit": limit, "all_hold": bool(np.all(need[evens] > 0)), "worst": int(worst), "worst_p": int(need[worst]),
            "records": records}


def collatz(limit: int = 1_000_000) -> dict:
    """Every start below ``limit`` reaches 1 (checked); the record stopping times.  Verified far beyond this by
    distributed search (to about 2^68 by 2020)."""
    steps = np.zeros(limit, np.int32)
    records = []
    best = -1
    for n in range(1, limit):
        x, s = n, 0
        while x >= n and x != 1:
            x = x // 2 if x % 2 == 0 else 3 * x + 1
            s += 1
        total = s + (steps[x] if x < n else 0)
        steps[n] = total
        if total > best:
            best = int(total)
            records.append({"n": n, "steps": best})
    return {"limit": limit, "all_reach_one": True, "records": records[-12:], "max_steps": best}


# ---------------------------------------------------------------- the open problems

OPEN = [
    {"problem": "P versus NP", "since": 1971, "record": "open; no superpolynomial lower bound for any NP problem",
     "parts": [26]},
    {"problem": "one-way functions exist?", "since": 1976, "record": "open; implies P != NP", "parts": [29, 30]},
    {"problem": "the exponent of matrix multiplication", "since": 1969,
     "record": "omega < 2.372 (2024); omega >= 2", "parts": [19, 52]},
    {"problem": "BB(6)", "since": 1962, "record": "BB(5) = 47,176,870, proved in 2024; BB(6) open", "parts": [25]},
    {"problem": "dynamic optimality of splay trees", "since": 1985,
     "record": "open; Tango trees are O(log log n)-competitive (2004)", "parts": [17]},
    {"problem": "the unique games conjecture", "since": 2002, "record": "open; the 2-to-2 theorem (2018)",
     "parts": [23, 56]},
    {"problem": "derandomization: BPP = P?", "since": 1980, "record": "open; PRIMES is in P (2004)", "parts": [20, 27]},
    {"problem": "circuit lower bounds", "since": 1949,
     "record": "no explicit function is known to need more than about 3.1 n gates (2022)", "parts": [3, 26]},
    {"problem": "a memory model for C", "since": 2011, "record": "open: the out-of-thin-air problem", "parts": [33]},
    {"problem": "practical quantum advantage", "since": 1994, "record": "open; error correction below threshold "
     "(2024)", "parts": [53]},
    {"problem": "verified software at scale", "since": 1969, "record": "seL4 (2009) and CompCert exist; scale open",
     "parts": [54]},
]


def open_problems() -> list[dict]:
    return OPEN
