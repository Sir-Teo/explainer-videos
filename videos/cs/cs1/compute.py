"""Precompute everything numerical in Part 1 of *Computer Science, Built* ("What Is a Computation?").

    python -m videos.cs.cs1.compute              # everything missing (about a minute)
    python -m videos.cs.cs1.compute --force beavers

Results are cached in ``.cache/cs1/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Every machine here runs on
this computer; the dates and the proofs about busy beavers are the published ones, cited on screen.

Items:
    pebbles     Euclid with two piles of pebbles: take the smaller pile from the larger until they are equal
    euclid      Euclid's algorithm on 1071 and 462, step by step, as squares cut from a rectangle; the number of steps
                for every pair up to 233 (a heatmap), the worst case at consecutive Fibonacci numbers, Lamé's bound
    difference  the method of finite differences on Babbage's demonstration polynomial x^2 + x + 41: the table, built
                by additions alone, and which values are prime
    bernoulli   the Bernoulli numbers B_0..B_10 (exact), from the recurrence Lovelace's Note G programs
    adder       a Turing machine adding in unary, 111+11, every configuration
    palindrome  palindromes on one tape and on two (every configuration on 0110 and 1001001), and the steps against
                the input's length: one tape (~n^2/2), two tapes (~3n), and two tapes simulated on one (Sipser)
    universal   the universal machine U (3 tapes, our own design) running <M> for the 2-state busy beaver, every
                configuration; U's steps against M's for the 2-, 3- and 4-state champions
    lam         lambda calculus: PLUS 2 3 reduced in normal order, every term and redex; the step counts of a few
                more sums, products and powers
    counters    a three-counter machine adding 3 + 4 (every step, for the bowls of pebbles); the same program compiled
                to two counters (Minsky): its length, and its steps on a few inputs
    rule110     Rule 110 from a single live cell: 300 generations
    life        Conway's Game of Life: Gosper's glider gun, 150 generations
    machines    how many machines there are with n states (2 symbols), and the first few descriptions <M>
    diagonal    the halting table: the first 2-state machines (rows) on inputs 1^j (columns), run for 10,000 steps
    beavers2    every 2-state, 2-symbol machine (20,736) from a blank tape: which halt, and when
    beavers     the busy-beaver champions for 2, 3 and 4 states (every configuration); the 5-state champion run for
                all 47,176,870 steps (a downsampled space-time picture, its first steps in full, its ones over time)
    pebble      Pebble-32 (Part 6's machine) running Euclid on 1071 and 462: the program and its trace
"""

from __future__ import annotations

import math
from fractions import Fraction

import numpy as np

from explainer.ai.cache import Cache
from explainer.cs import lam
from explainer.cs.turing import BLANK, CHAMPIONS, HALT, TM, run, run_fast, spacetime
from videos.cs.cs1.machines import (ADD3, PALINDROME, PALINDROME2, UNARY_ADD, UTM, compile_two_counters, elementary,
                                    encode, godel, life, run_universal, single_tape_cost, ungodel)

CACHE = Cache("cs1")
load = CACHE.load


def hist_json(res, tapes: int, lo: list[int], hi: list[int]) -> list[dict]:
    """A recorded run, each configuration as JSON: state, heads, tape windows, the rule applied (index)."""
    out = []
    for st, hs, tps, rule in res.history:
        out.append({"state": st, "heads": list(hs), "rule": rule,
                    "tapes": ["".join(tps[t].get(k, BLANK) for k in range(lo[t], hi[t] + 1)) for t in range(tapes)]})
    return out


def compute_pebbles() -> dict:
    a, b = 24, 18
    steps = [(a, b)]
    while a != b:
        if a > b:
            a -= b
        else:
            b -= a
        steps.append((a, b))
    return {"start": [24, 18], "steps": steps, "gcd": a}


def euclid_steps(a: int, b: int) -> int:
    n = 0
    while b:
        a, b = b, a % b
        n += 1
    return n


def compute_euclid() -> dict:
    a, b = 1071, 462
    trace = []
    while b:
        q, r = divmod(a, b)
        trace.append({"a": a, "b": b, "q": q, "r": r})
        a, b = b, r
    N = 233
    grid = np.zeros((N + 1, N + 1), np.int16)
    for x in range(1, N + 1):
        for y in range(1, N + 1):
            grid[x, y] = euclid_steps(max(x, y), min(x, y))
    fib = [1, 1]
    while fib[-1] < 10**6:
        fib.append(fib[-1] + fib[-2])
    worst = []  # for each number of steps k, the smallest pair needing k steps (Lamé: consecutive Fibonacci numbers)
    for k in range(1, 14):
        worst.append({"k": k, "pair": [fib[k + 1], fib[k]], "steps": euclid_steps(fib[k + 1], fib[k])})
    # Lamé (1844): steps <= 5 x (decimal digits of the smaller number); check it on the whole grid
    lame_ok = all(euclid_steps(max(x, y), min(x, y)) <= 5 * len(str(min(x, y)))
                  for x in range(1, N + 1) for y in range(1, N + 1))
    assert lame_ok
    return {"trace": trace, "gcd": a, "grid": grid[1:, 1:], "N": N, "worst": worst, "max_steps": int(grid.max()),
            "argmax": [int(v) for v in np.unravel_index(int(grid.argmax()), grid.shape)]}


def compute_difference() -> dict:
    p = [x * x + x + 41 for x in range(0, 42)]
    d1 = [p[i + 1] - p[i] for i in range(len(p) - 1)]
    d2 = [d1[i + 1] - d1[i] for i in range(len(d1) - 1)]
    assert set(d2) == {2}

    def prime(n):
        return n > 1 and all(n % k for k in range(2, int(n ** 0.5) + 1))

    return {"values": p, "d1": d1, "d2": d2, "prime": [prime(v) for v in p],
            "first_composite": next(x for x, v in enumerate(p) if not prime(v))}


def compute_bernoulli() -> dict:
    B = [Fraction(1)]
    for m in range(1, 11):
        B.append(-sum(math.comb(m + 1, k) * B[k] for k in range(m)) / (m + 1))
    return {"B": [[f.numerator, f.denominator] for f in B]}


def compute_adder() -> dict:
    r = run(UNARY_ADD, "111+11", record=True)
    return {"rules": UNARY_ADD.table_text(), "history": hist_json(r, 1, [-1], [7]), "steps": r.steps,
            "result": r.tape(0, 0, 5), "lo": -1}


def compute_palindrome() -> dict:
    out = {"rules1": PALINDROME.table_text(), "rules2": [(st, *rd, *wr, *mv, nx) for st, rd, wr, mv, nx in
                                                         PALINDROME2.rules]}
    for w in ("0110", "1001001"):
        r = run(PALINDROME, w, record=True)
        out[f"run1_{w}"] = hist_json(r, 1, [-1], [len(w)])
        r2 = run(PALINDROME2, (w, ""), record=True)
        out[f"run2_{w}"] = hist_json(r2, 2, [-1, -1], [len(w), len(w)])
    long = "011010011101110010110110"  # 24 symbols, then checked to be a palindrome
    long = long[:12] + long[:12][::-1]
    r = run(PALINDROME, long, record=True)
    out["st_long"] = spacetime(r, -1, len(long))
    out["long"] = long
    out["long_steps"] = r.steps
    rng = np.random.default_rng(1)
    ns = list(range(1, 61))
    one, two, sim = [], [], []
    for n in ns:
        half = "".join(rng.choice(["0", "1"], n // 2))
        w = half + ("1" if n % 2 else "") + half[::-1]
        assert w == w[::-1] and len(w) == n
        r1 = run(PALINDROME, w, max_steps=10**6)
        r2 = run(PALINDROME2, (w, ""), max_steps=10**6)
        assert r1.state == r2.state == "accept"
        c = single_tape_cost(PALINDROME2, (w, ""))
        one.append(r1.steps)
        two.append(r2.steps)
        sim.append(c["moves"])
    # every input up to length 10 against Python
    for n in range(0, 11):
        for k in range(2 ** n):
            w = format(k, f"0{n}b") if n else ""
            want = "accept" if w == w[::-1] else "reject"
            assert run(PALINDROME, w).state == want and run(PALINDROME2, (w, "")).state == want
    a, b = np.polyfit(np.array(ns, float), np.array(one, float) / np.array(ns, float), 1)
    return {**out, "n": ns, "one": one, "two": two, "sim": sim, "fit_one": [float(a), float(b)]}


def compute_universal() -> dict:
    m = TM.parse(CHAMPIONS[2][0])
    enc = encode(m)
    r = run_universal(m, record=True)
    L = len(enc) + 2
    hist = hist_json(r, 3, [0, -3, 0], [L - 1, 2, 4])
    # where M's steps fall in U's run: the steps at which U executes a "write"
    writes = [i for i, h in enumerate(hist) if h["state"] == "write"]
    rows = []
    for n in (2, 3, 4):
        mm = TM.parse(CHAMPIONS[n][0])
        u = run_universal(mm)
        d = run(mm)
        assert u.halted and u.tape(1) == d.tape(0)
        rows.append({"n": n, "m_steps": d.steps, "u_steps": u.steps, "len": len(encode(mm))})
    states = sorted({x for rr in UTM.rules for x in (rr[0], rr[4])})
    return {"encoding": enc, "history": hist, "writes": writes, "u_steps": r.steps, "rows": rows,
            "u_rules": len(UTM.rules), "u_states": len([s for s in states if s not in HALT]),
            "rules": [[st, "".join(rd), "".join(wr), "".join(mv), nx] for st, rd, wr, mv, nx in UTM.rules]}


def compute_lam() -> dict:
    t = lam.parse(f"({lam.PLUS}) ({lam.show(lam.church(2))}) ({lam.show(lam.church(3))})")
    steps = lam.normalize(t)
    assert lam.unchurch(steps[-1].term) == 5
    seq = [{"text": lam.show(s.term), "tex": lam.tex(s.term, redex=s.redex), "redex": list(s.redex or [])}
           for s in steps]
    counts = []
    for op, f in (("PLUS", lambda a, b: a + b), ("TIMES", lambda a, b: a * b), ("POW", lambda a, b: a ** b)):
        for a_, b_ in ((2, 3), (3, 3), (2, 5)):
            term = lam.parse(f"({getattr(lam, op)}) ({lam.show(lam.church(a_))}) ({lam.show(lam.church(b_))})")
            ss = lam.normalize(term, max_steps=100_000)
            assert lam.unchurch(ss[-1].term) == f(a_, b_)
            counts.append({"op": op, "a": a_, "b": b_, "value": f(a_, b_), "steps": len(ss) - 1})
    return {"plus23": seq, "counts": counts}


def compute_counters() -> dict:
    r = ADD3.run([3, 4], record=True)
    two = compile_two_counters(ADD3)
    runs = []
    for a_, b_ in ((1, 1), (2, 1), (3, 4), (5, 5)):
        g = godel([a_, b_, 0])
        rr = two.run([g, 0])
        assert ungodel(rr["regs"][0], 3) == ADD3.run([a_, b_])["regs"] and rr["regs"][1] == 0
        runs.append({"a": a_, "b": b_, "godel_in": g, "godel_out": rr["regs"][0], "steps": rr["steps"],
                     "three_steps": ADD3.run([a_, b_])["steps"]})
    # the size of A over the run of 3 + 4 (sampled), for the picture of a counter that swells and shrinks
    rr = two.run([godel([3, 4, 0]), 0], record=True)
    hA = np.array([h[1][0] for h in rr["history"]], np.int64)
    hB = np.array([h[1][1] for h in rr["history"]], np.int64)
    idx = np.linspace(0, len(hA) - 1, 2000).astype(int)
    return {"prog3": [list(i) for i in ADD3.prog], "history3": [[pc, list(rg)] for pc, rg in r["history"]],
            "result3": r["regs"], "two_len": len(two.prog), "runs": runs, "A": hA[idx], "B": hB[idx],
            "two_steps": int(len(hA))}


def compute_rule110() -> dict:
    return {"grid": elementary(110, 600, 300)}


def compute_life() -> dict:
    return {"frames": life(40, 64, 150)}


def compute_machines() -> dict:
    counts = [{"n": n, "count": (4 * n + 4) ** (2 * n)} for n in range(1, 7)]
    examples = []
    for n in (2, 3, 4, 5):
        examples.append({"n": n, "table": CHAMPIONS[n][0], "encoding": encode(TM.parse(CHAMPIONS[n][0]))})
    return {"counts": counts, "examples": examples}


def all_two_state():
    """Every 2-state, 2-symbol machine with the halting transitions allowed (12^4 = 20,736), in a fixed order."""
    acts = [f"{w}{m}{n}" for n in "ABZ" for m in "RL" for w in "01"]
    for a0 in acts:
        for a1 in acts:
            for b0 in acts:
                for b1 in acts:
                    yield f"{a0}{a1}_{b0}{b1}"


def compute_diagonal() -> dict:
    """Rows: machines spread through the enumeration (every 2,591st, a prime stride), keeping those whose rows differ;
    columns: the inputs 1^j.  An entry is the number of steps to halt, or None if still running at 10,000 steps."""
    machines = list(all_two_state())
    rows, seen = [], set()
    for k in range(0, len(machines), 2591):
        m = TM.parse(machines[k])
        res = []
        for j in range(8):
            r = run(m, "1" * j, max_steps=10_000)
            res.append(r.steps if r.halted else None)
        sig = tuple(-1 if v is None else v for v in res)
        if sig in seen or all(v is None for v in res) and any(all(x is None for x in rr["results"]) for rr in rows):
            continue
        seen.add(sig)
        rows.append({"index": k, "table": machines[k], "results": res})
        if len(rows) == 8:
            break
    return {"rows": rows, "inputs": ["1" * j for j in range(8)], "limit": 10_000, "total": len(machines)}


def compute_beavers2() -> dict:
    halts, ones, total = [], [], 0
    for t in all_two_state():
        total += 1
        r = run(TM.parse(t), max_steps=1000)
        if r.halted and r.state in HALT:
            halts.append(r.steps)
            ones.append(r.ones())
    halts, ones = np.array(halts), np.array(ones)
    assert halts.max() == 6
    return {"total": total, "halting": int(len(halts)), "hist": np.bincount(halts, minlength=7).tolist(),
            "max_steps": int(halts.max()), "max_ones": int(ones.max())}


def compute_beavers() -> dict:
    out = {}
    for n in (2, 3, 4):
        t, S, ones, who, year = CHAMPIONS[n]
        r = run(TM.parse(t), max_steps=1000, record=True)
        assert r.steps == S and r.ones() == ones
        lo = min(h[1][0] for h in r.history) - 1
        hi = max(h[1][0] for h in r.history) + 1
        out[f"st{n}"] = spacetime(r, lo, hi)
        out[f"info{n}"] = {"table": t, "steps": S, "ones": ones, "who": who, "year": year, "lo": lo, "hi": hi}
    t, S, ones, who, year = CHAMPIONS[5]
    m = TM.parse(t)
    rows = 1600
    every = S // rows
    f = run_fast(m, S + 10, size=1 << 15, snap_every=every, n_snaps=rows)
    assert f["steps"] == S and f["ones"] == ones
    lo, hi = f["lo"], f["hi"]
    size = 1 << 15
    snaps = f["snaps"][:, size // 2 + lo: size // 2 + hi + 1]
    pool = 8
    w = snaps.shape[1] // pool * pool
    pooled = snaps[:, :w].reshape(len(snaps), -1, pool).mean(axis=2)
    ones_t = snaps.sum(axis=1)
    early = run_fast(m, 4000, size=1 << 12, snap_every=1, n_snaps=4000)
    e_lo, e_hi = int(early["snap_bounds"][:, 0].min()), int(early["snap_bounds"][:, 1].max())
    es = early["snaps"][:, (1 << 11) + e_lo: (1 << 11) + e_hi + 1]
    out["st5"] = (pooled * 255).astype(np.uint8)
    out["heads5"] = f["snap_heads"]
    out["ones5"] = ones_t
    out["early5"] = es
    out["early_heads5"] = early["snap_heads"] - e_lo
    out["info5"] = {"table": t, "steps": S, "ones": ones, "who": who, "year": year, "lo": lo, "hi": hi,
                    "every": every, "pool": pool, "cells": hi - lo + 1}
    return out


EUCLID_ASM = """
        li   a0, 1071
        li   a1, 462
loop:   beqz a1, done        # b = 0? stop
mod:    bltu a0, a1, swap    # a < b? swap
        sub  a0, a0, a1      # a = a - b
        j    mod
swap:   mv   t0, a0          # a, b = b, a
        mv   a0, a1
        mv   a1, t0
        j    loop
done:   halt                 # a0 = gcd
"""


def compute_pebble() -> dict:
    from explainer.cs.pebble import assemble, run as prun

    p = assemble(EUCLID_ASM)
    m = prun(p, trace=True, mem_size=4096)
    assert m.regs[3] == math.gcd(1071, 462)
    # the register file after every step
    regs = [0] * 16
    regs[2] = 4096
    trace = []
    lines = {addr: ln for addr, ln in p.source_lines.items()}
    for s in m.log:
        if s.reg:
            regs[s.reg[0]] = s.reg[1]
        trace.append({"pc": s.pc, "line": lines[s.pc], "a0": regs[3], "a1": regs[4], "t0": regs[9],
                      "taken": s.taken})
    return {"source": EUCLID_ASM.strip("\n").split("\n"), "listing": [[a, w, src] for a, w, src in p.listing],
            "trace": trace, "steps": m.steps, "result": m.regs[3]}


# ---------------------------------------------------------------------------
# The Frontier chapter (videos/cs/SYLLABUS.md 1.1): BB(6), Antihydra, and where provability ends
# ---------------------------------------------------------------------------
ANTIHYDRA = "1RB1RA_0LC1LE_1LD1LC_1LA0LB_1LF1RE_---0RA"  # mxdys, 28 June 2024 (wiki.bbchallenge.org/wiki/Antihydra)
# BB(6) records, (year, who, the bound on the number of steps S(6), as on-screen TeX); wiki.bbchallenge.org/wiki/BB(6)
BB6_RECORDS = [
    (1964, r"Green", r"436"),
    (1990, r"Marxen and Buntrock", r"13{,}122{,}572{,}797"),
    (2010, r"Kropitz", r"3.8 \times 10^{21132}"),
    (2022, r"Kropitz", r"10 \uparrow\uparrow 15"),
    (2025, r"mxdys", r"10 \uparrow\uparrow 10 \uparrow\uparrow 10 \uparrow\uparrow 8"),
]
# the smallest known machine whose halting ZFC cannot settle (if ZFC is consistent); wiki.bbchallenge.org,
# "Independence from ZFC": the later entries are not yet formally verified
ZFC_RECORDS = [(2016, 7910, r"Yedidia and Aaronson"), (2023, 745, r"Riebel"), (2024, 636, r"Ridenour"),
               (2025, 432, r"Wade")]


def compute_frontier() -> dict:
    """Antihydra run as a Turing machine on our simulator, and as its Collatz-like rule (Racheline): h = 8, c = 0;
    each step c += 2 if h is even, else c -= 1, then h += floor(h / 2); the machine halts iff c reaches -1."""
    m = TM.parse(ANTIHYDRA)
    big = run_fast(m, 10 ** 8, size=1 << 20)
    assert not big["halted"]
    early = run_fast(m, 6000, size=1 << 12, snap_every=1, n_snaps=6000)
    e_lo, e_hi = int(early["snap_bounds"][:, 0].min()), int(early["snap_bounds"][:, 1].max())
    es = early["snaps"][:, (1 << 11) + e_lo: (1 << 11) + e_hi + 1]
    h, c, even, n = 8, 0, 0, 10 ** 6
    first, path, frac = [], [], []
    for i in range(n):
        if i < 16:
            first.append((h, h & 1, c))
        if h & 1:
            c -= 1
        else:
            c += 2
            even += 1
        h += h >> 1
        assert c >= 0
        if (i + 1) % 1000 == 0:
            path.append(c)
            frac.append(even / (i + 1))
    phi = (1 + 5 ** 0.5) / 2
    return {"table": ANTIHYDRA, "tm_steps": big["steps"], "tm_cells": big["hi"] - big["lo"] + 1,
            "tm_ones": big["ones"], "early": es, "early_heads": early["snap_heads"] - e_lo,
            "first": first, "iterations": n, "c_path": path, "even_frac": frac, "c_final": c,
            "even_final": even / n, "h_bits": h.bit_length(),
            "q": 1 / phi, "log10_p": -(c + 1) * float(np.log10(phi)),
            "bb6": BB6_RECORDS, "zfc": ZFC_RECORDS}


ITEMS = {
    "pebbles": compute_pebbles, "euclid": compute_euclid, "difference": compute_difference,
    "bernoulli": compute_bernoulli, "adder": compute_adder, "palindrome": compute_palindrome,
    "universal": compute_universal, "lam": compute_lam, "counters": compute_counters, "rule110": compute_rule110,
    "life": compute_life, "machines": compute_machines, "diagonal": compute_diagonal, "beavers2": compute_beavers2,
    "beavers": compute_beavers, "pebble": compute_pebble, "frontier": compute_frontier,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
