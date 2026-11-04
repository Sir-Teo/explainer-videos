"""Precompute everything numerical in Part 4 of *Computer Science, Built* ("Arithmetic").

    python -m videos.cs.cs4.compute              # everything missing (a few minutes)
    python -m videos.cs.cs4.compute --force adders

Results are cached in ``.cache/cs4/<name>.json``; scenes call ``load(name)``.  Every circuit is a netlist from
``explainer/cs/pebble/blocks.py``, checked against Python's integers (exhaustively where the inputs are few, on
random and worst-case patterns otherwise) and timed with ``Circuit.settle`` (unit gate delays).

Items:
    clock      integers on a 4-bit clock (unsigned and two's complement), and the overflow stories of the hook
    adders     ripple, carry-skip, carry-select, Brent-Kung, Sklansky, Kogge-Stone: gates, depth, and the measured
               settling time, for n = 4 ... 64
    prefix     the prefix networks on 16 positions, level by level, with their size, depth and largest fan-out
    mult       array against Wallace and Dadda tree multipliers, n = 4 ... 16; Booth radix-4 recoding of an example
    divide     restoring division traced; radix-4 SRT with its quotient-digit table; the same table with five cells
               emptied (a toy FDIV bug), run on random divisions; Newton-Raphson and Goldschmidt convergence
    alu        Pebble's ALU: gates by part, depth, settling time; verified exhaustively at 8 bits, on random vectors
               at 32
    floats     a toy 6-bit float format (every value), float32 fields, ulp and spacing, the formats table
    error      cancellation in (1 - cos x)/x^2; naive, pairwise and Kahan summation in float32; the Patriot clock
    wilkinson  the roots of prod (x - k), k = 1..20, as the x^19 coefficient moves by 2^-23 (60-digit arithmetic)
    functions  CORDIC iterations; a Remez minimax polynomial for e^x against Taylor's
"""

from __future__ import annotations

import math
import struct

import numpy as np

from explainer.ai.cache import Cache
from explainer.cs.pebble import blocks as B
from explainer.cs.pebble.hdl import simulate

CACHE = Cache("cs4")
load = CACHE.load


# ---------------------------------------------------------------------------
# the clock
# ---------------------------------------------------------------------------
def compute_clock() -> dict:
    n = 4
    rows = []
    for u in range(1 << n):
        s = u - (1 << n) if u >> (n - 1) else u
        rows.append({"bits": format(u, f"0{n}b"), "u": u, "s": s})
    # overflow in 4 bits: 5 + 4 = 9 unsigned, but -7 signed
    return {
        "n": n, "rows": rows,
        "int32_max": 2 ** 31 - 1,
        "days_2_31_cs": 2 ** 31 / 100 / 86400,         # a centisecond counter in a signed 32-bit integer
        "point_three": repr(0.1 + 0.2),
        "neg_examples": [{"x": x, "bits": format(x & 0xFF, "08b"), "inv": format(~x & 0xFF, "08b"),
                          "neg": format(-x & 0xFF, "08b")} for x in (1, 6, 100, -128)],
    }


# ---------------------------------------------------------------------------
# adders
# ---------------------------------------------------------------------------
DESIGNS = ("ripple", "carry-skip", "carry-select", "brent-kung", "sklansky", "kogge-stone")


def adder(n: int, kind: str):
    if kind == "ripple":
        return B.ripple_adder(n)
    if kind == "carry-skip":
        return B.carry_skip_adder(n, max(2, round(math.sqrt(n / 2))))
    if kind == "carry-select":
        return B.carry_select_adder(n)
    return B.prefix_adder(n, kind)


def adder_vectors(n: int, rng, count: int = 6000):
    """Random patterns, mostly-propagating patterns (b close to not a) and the worst cases by construction: a
    carry generated at bit j and propagated to the top, for every j."""
    hi = 1 << n
    a = rng.integers(0, hi, count, dtype=np.uint64) if n < 64 else rng.integers(0, 1 << 63, count, dtype=np.uint64)
    flips = np.zeros(count, np.uint64)
    for _ in range(3):
        flips |= np.uint64(1) << rng.integers(0, n, count).astype(np.uint64)
    mask = np.uint64(hi - 1) if n < 64 else np.uint64(0xFFFF_FFFF_FFFF_FFFF)
    b = np.where(rng.random(count) < 0.7, (~a ^ flips) & mask, rng.integers(0, 1 << min(n, 63), count, dtype=np.uint64))
    cin = rng.integers(0, 2, count, dtype=np.uint64)
    full = (1 << n) - 1
    wa = [full] * n + [full]
    wb = [1 << j for j in range(n)] + [0]
    wc = [0] * n + [1]
    a = np.concatenate([a, np.array(wa, dtype=np.uint64)])
    b = np.concatenate([b, np.array(wb, dtype=np.uint64)])
    cin = np.concatenate([cin, np.array(wc, dtype=np.uint64)])
    return a, b, cin


def compute_adders() -> dict:
    rng = np.random.default_rng(4)
    table = []
    for n in (4, 8, 16, 32, 64):
        a, b, cin = adder_vectors(n, rng)
        ai, bi, ci = (x.astype(object) for x in (a, b, cin))
        for kind in DESIGNS:
            c = adder(n, kind)
            r = simulate(c, {"a": a, "b": b, "cin": cin})
            got = r["s"].astype(object) + (r["cout"].astype(object) << n)
            assert all(got == ai + bi + ci), (n, kind)
            st = c.settle({"a": a.astype(np.int64) if n < 64 else a.view(np.int64), "b": b.astype(np.int64)
                           if n < 64 else b.view(np.int64), "cin": cin.astype(np.int64)})
            table.append({"n": n, "kind": kind, "gates": c.size(), "depth": c.depth(), "settle": int(st.max()),
                          "vectors": len(a)})
    # exhaustive check of every design at 8 bits
    p = np.arange(1 << 17, dtype=np.int64)
    a8, b8, c8 = p & 0xFF, (p >> 8) & 0xFF, p >> 16
    for kind in DESIGNS:
        r = simulate(adder(8, kind), {"a": a8, "b": b8, "cin": c8})
        assert np.array_equal(r["s"].astype(np.int64) + (r["cout"].astype(np.int64) << 8), a8 + b8 + c8)
    # the ripple carry, wire by wire, for one 8-bit addition: when each carry settles
    c = B.ripple_adder(8)
    x, y = 0b01111111, 0b00000001
    times = carry_times(c, x, y, 0)
    return {"rows": table, "exhaustive8": 1 << 17, "ripple_example": {"a": x, "b": y, "carry_times": times}}


def carry_times(c, a: int, b: int, cin: int) -> list[int]:
    """The settling time of each sum bit of an adder for one input pattern."""
    out = []
    for i in range(len(c.outputs["s"])):
        sub = type(c)(c.name, c.kinds, c.args, c.inputs, {"s": [c.outputs["s"][i]]})
        out.append(int(sub.settle({"a": np.array([a]), "b": np.array([b]), "cin": np.array([cin])})[0]))
    return out


# ---------------------------------------------------------------------------
# prefix networks
# ---------------------------------------------------------------------------
def compute_prefix() -> dict:
    out = {}
    for kind in B.PREFIX:
        lv = B.prefix_levels(16, kind)
        # fan-out: the gates one node drives at one level (its own next value, and every combine that reads it)
        fo = 1 + max(max(sum(1 for _, j in level if j == k) for k in range(16)) for level in lv)
        out[kind] = {"levels": lv, "nodes": sum(len(level) for level in lv), "depth": len(lv), "fanout": fo}
    return out


# ---------------------------------------------------------------------------
# multipliers
# ---------------------------------------------------------------------------
def booth4(b: int, n: int) -> list[int]:
    """Radix-4 Booth digits of the n-bit two's complement number b, least significant first: each in -2..2."""
    bits = [0] + [(b >> i) & 1 for i in range(n)] + [(b >> (n - 1)) & 1] * 2
    return [bits[i] + bits[i + 1] - 2 * bits[i + 2] for i in range(0, n, 2)]


def compute_mult() -> dict:
    rng = np.random.default_rng(5)
    rows = []
    for n in (4, 6, 8, 12, 16):
        if 2 * n <= 16:
            p = np.arange(1 << (2 * n), dtype=np.int64)
            a, b = p & ((1 << n) - 1), p >> n
        else:
            a = rng.integers(0, 1 << n, 20000)
            b = rng.integers(0, 1 << n, 20000)
            a[:2], b[:2] = (1 << n) - 1, (1 << n) - 1
        for kind in ("array", "wallace", "dadda"):
            c = B.array_multiplier(n) if kind == "array" else B.tree_multiplier(n, kind)
            r = simulate(c, {"a": a, "b": b})
            assert np.array_equal(r["p"].astype(np.int64), a * b), (n, kind)
            st = c.settle({"a": a[:4000], "b": b[:4000]})
            rows.append({"n": n, "kind": kind, "gates": c.size(), "depth": c.depth(), "settle": int(st.max()),
                         "stages": getattr(c, "stages", None), "exhaustive": bool(2 * n <= 16),
                         "full_adders": None})
    ex = 0b01110110  # 118
    digits = booth4(ex, 8)
    assert sum(d * 4 ** i for i, d in enumerate(digits)) == ex
    # the column heights of an 8x8 tree multiplier, level by level (Wallace)
    heights = [[min(k + 1, 15 - k, 8) for k in range(15)]]
    return {"rows": rows, "booth": {"b": ex, "digits": digits}, "heights8": heights}


# ---------------------------------------------------------------------------
# division
# ---------------------------------------------------------------------------
SRT_F = 24
PL, PH = -48, 48  # the table's rows: the estimate of 4w, in steps of 1/8
BAD_COLS = (17, 20, 23, 26, 29)  # divisor columns 1.0001, 1.0100, 1.0111, 1.1010, 1.1101 (the Pentium's five)


def restoring(x: int, d: int, n: int = 8) -> list[dict]:
    """Restoring division of n-bit x by d, one quotient bit per step: shift, try subtracting, keep or restore."""
    r, steps = 0, []
    for i in reversed(range(n)):
        r = (r << 1) | ((x >> i) & 1)
        t = r - d
        q = int(t >= 0)
        steps.append({"bit": i, "r": r, "try": t, "q": q})
        if q:
            r = t
    return steps


def srt_table() -> dict:
    """For each cell (estimate of 4w to 1/8, divisor to 1/16): a quotient digit q in -2..2 that keeps the next
    remainder 4w - q d within +-(2/3) d for every point of the cell inside |4w| <= (8/3) d."""
    tab = {}
    us = np.linspace(0, 1, 13)[:-1] + 1e-9
    for di in range(16, 32):
        for pi in range(PL, PH):
            P = np.array([((pi + u) / 8, (di + v) / 16) for u in us for v in us])
            P = P[np.abs(P[:, 0]) <= 8 / 3 * P[:, 1]]
            if len(P) == 0:
                continue
            valid = [q for q in (-2, -1, 0, 1, 2) if np.all(np.abs(P[:, 0] - q * P[:, 1]) <= 2 / 3 * P[:, 1] + 1e-12)]
            assert valid, (pi, di)
            mid = (pi + 0.5) / 8 / ((di + 0.5) / 16)
            tab[(pi, di)] = min(valid, key=lambda q: abs(q - mid))
    return tab


def srt_array(tab: dict) -> np.ndarray:
    T = np.zeros((PH - PL, 16), np.int64)
    for pi in range(PL, PH):
        for di in range(16, 32):
            T[pi - PL, di - 16] = tab.get((pi, di), 2 if pi >= 0 else -2)
    return T


def srt_divide(X, D, T, steps=14, record=False):
    """Radix-4 SRT on x, d in [1, 2) with SRT_F fraction bits (integer arrays).  w0 = x / 4; each step
    p = 4 w, q = T[p estimate, d estimate], w = p - q d.  Returns the quotient digits' value, scaled by 4^steps."""
    F = SRT_F
    W = X.copy()
    Dd = D << 2
    Q = np.zeros_like(X)
    di = (D >> (F - 4)) - 16
    cells = []
    for _ in range(steps):
        p = 4 * W
        pi = p >> (F - 1)
        q = np.where(pi >= PH, 2, np.where(pi < PL, -2, T[np.clip(pi - PL, 0, PH - PL - 1), di]))
        if record:
            cells.append(pi.copy())
        W = p - q * Dd
        Q = 4 * Q + q
    return Q, cells


def compute_divide() -> dict:
    F = SRT_F
    rng = np.random.default_rng(6)
    tab = srt_table()
    T = srt_array(tab)
    # which cells do random divisions visit?
    N = 400_000
    X = rng.integers(1 << F, 1 << (F + 1), N)
    D = rng.integers(1 << F, 1 << (F + 1), N)
    Q, cells = srt_divide(X, D, T, record=True)
    steps = 14
    qv = 4 * Q / 4.0 ** steps
    good_err = float(np.max(np.abs(qv - X / D) / (X / D)))
    C = np.array(cells)
    di = (D >> (F - 4)) - 16
    visited = set()
    for k in range(steps):
        visited |= set(zip(C[k].tolist(), (di + 16).tolist()))
    # the toy bug: in five divisor columns, the highest cell random divisions ever visit is emptied (q = 0)
    top = {}
    for col in BAD_COLS:
        Xc = rng.integers(1 << F, 1 << (F + 1), 1_000_000)
        Dc = rng.integers(col << (F - 4), (col + 1) << (F - 4), 1_000_000)
        _, cc = srt_divide(Xc, Dc, T, record=True)
        top[col] = int(np.array(cc).max())
    bad_tab = dict(tab)
    for col, pi in top.items():
        bad_tab[(pi, col)] = 0
    Tb = srt_array(bad_tab)
    M = 2_000_000
    X = rng.integers(1 << F, 1 << (F + 1), M)
    D = rng.integers(1 << F, 1 << (F + 1), M)
    Qg, _ = srt_divide(X, D, T)
    Qb, _ = srt_divide(X, D, Tb)
    wrong = Qg != Qb
    qb = 4 * Qb / 4.0 ** steps
    rel = np.abs(qb - X / D) / (X / D)
    worst = int(np.argmax(np.where(wrong, rel, 0)))
    # Newton-Raphson for 1/d, and Goldschmidt
    d = 1.7
    y, nr = 0.75, []  # a rough first guess from a small table
    for k in range(6):
        nr.append({"k": k, "y": y, "err": abs(y - 1 / d)})
        y = y * (2 - d * y)
    g, (num, den) = [], (1.0, d)
    for k in range(6):
        g.append({"k": k, "q": num, "err": abs(num - 1 / d)})
        f = 2 - den
        num, den = num * f, den * f
    return {
        "restoring": {"x": 200, "d": 13, "steps": restoring(200, 13), "q": 200 // 13, "r": 200 % 13},
        "table": [[pi, di, q] for (pi, di), q in sorted(tab.items())], "cells": len(tab),
        "visited": len(visited), "never": len(tab) - len(visited & set(tab)),
        "good_max_rel_err": good_err, "steps": steps,
        "bad_cells": [[top[c], c] for c in BAD_COLS],
        "bad_divisions": M, "bad_wrong": int(wrong.sum()), "bad_max_rel": float(rel[wrong].max()) if wrong.any() else 0,
        "bad_example": {"x": int(X[worst]) / 2 ** F, "d": int(D[worst]) / 2 ** F, "got": float(qb[worst]),
                        "true": float(X[worst] / D[worst])},
        "pentium": {"x": 4195835, "d": 3145727, "true": 4195835 / 3145727, "pentium": 1.333739068902037589},
        "newton": nr, "goldschmidt": g, "nr_d": d,
    }


# ---------------------------------------------------------------------------
# Pebble's ALU
# ---------------------------------------------------------------------------
def compute_alu() -> dict:
    rng = np.random.default_rng(7)
    p = np.arange(1 << 20, dtype=np.int64)
    a, b, op = p & 0xFF, (p >> 8) & 0xFF, p >> 16
    keep = op < len(B.ALU_OPS)
    a, b, op = a[keep], b[keep], op[keep]
    c8 = B.alu(8)
    r = simulate(c8, {"a": a, "b": b, "op": op})
    assert np.array_equal(r["y"].astype(np.int64), B.alu_spec(a, b, op, 8))
    n8 = int(keep.sum())
    rows = []
    for adder in ("ripple", "kogge-stone"):
        c = B.alu(32, adder)
        V = 20000
        A = rng.integers(0, 1 << 32, V, dtype=np.int64)
        Bv = rng.integers(0, 1 << 32, V, dtype=np.int64)
        Bv[: V // 4] = rng.integers(0, 32, V // 4)  # small shift amounts, and small numbers
        OP = rng.integers(0, len(B.ALU_OPS), V)
        A[:20], Bv[:20], OP[:20] = 0xFFFF_FFFF, 1, B.ALU_OPS.index("add")  # the longest carry
        A[20:40], Bv[20:40], OP[20:40] = 0, 1, B.ALU_OPS.index("sub")       # and the longest borrow
        rr = simulate(c, {"a": A, "b": Bv, "op": OP})
        assert np.array_equal(rr["y"].astype(np.int64), B.alu_spec(A, Bv, OP, 32)), adder
        st = c.settle({"a": A[:3000], "b": Bv[:3000], "op": OP[:3000]})
        nand = c.to_nand()
        rows.append({"adder": adder, "gates": c.size(), "counts": c.counts(), "depth": c.depth(),
                     "settle": int(st.max()), "nands": nand.size(), "vectors": V})
    return {"rows": rows, "ops": list(B.ALU_OPS), "exhaustive8": n8, "gates8": c8.size()}


# ---------------------------------------------------------------------------
# floating point
# ---------------------------------------------------------------------------
def minifloat_values(e_bits=3, m_bits=2):
    bias = (1 << (e_bits - 1)) - 1
    vals = []
    for e in range(1 << e_bits):
        for m in range(1 << m_bits):
            if e == (1 << e_bits) - 1:
                continue  # infinities and NaNs
            if e == 0:
                v = m / (1 << m_bits) * 2.0 ** (1 - bias)
                kind = "sub"
            else:
                v = (1 + m / (1 << m_bits)) * 2.0 ** (e - bias)
                kind = "normal"
            vals.append({"e": e, "m": m, "v": v, "kind": kind})
    return vals, bias


def f32_fields(x: float) -> dict:
    u = struct.unpack(">I", struct.pack(">f", x))[0]
    s, e, m = u >> 31, (u >> 23) & 0xFF, u & 0x7FFFFF
    exact = struct.unpack(">f", struct.pack(">I", u))[0]
    from decimal import Decimal
    return {"x": x, "bits": format(u, "032b"), "s": s, "e": e, "m": m, "stored": repr(exact),
            "exact": str(Decimal(exact))}


def compute_floats() -> dict:
    vals, bias = minifloat_values()
    fmts = []
    for name, e, m in (("binary64", 11, 52), ("binary32", 8, 23), ("binary16", 5, 10), ("bfloat16", 8, 7),
                       ("FP8 E5M2", 5, 2), ("FP8 E4M3", 4, 3)):
        bias_ = (1 << (e - 1)) - 1
        emax = (1 << e) - 2 - bias_
        mx = (2 - 2.0 ** -m) * 2.0 ** emax
        if name == "FP8 E4M3":  # OCP E4M3 keeps only one NaN pattern, so its largest exponent is usable: 448
            mx = 448.0
        fmts.append({"name": name, "e": e, "m": m, "bits": 1 + e + m, "max": mx, "min_normal": 2.0 ** (1 - bias_),
                     "min_sub": 2.0 ** (1 - bias_ - m), "eps": 2.0 ** -m, "digits": m * math.log10(2) + math.log10(2)})
    # spacing of float32 between 1 and 16: ulp(x)
    xs = np.float32(2.0) ** np.arange(-3, 5, dtype=np.float32)
    ulps = [{"x": float(x), "ulp": float(np.spacing(np.float32(x)))} for x in xs]
    return {
        "mini": {"values": vals, "bias": bias, "e_bits": 3, "m_bits": 2},
        "formats": fmts,
        "f32": [f32_fields(x) for x in (0.1, -6.25, 1.0)],
        "ulps": ulps,
        "eps32": float(np.finfo(np.float32).eps), "eps64": float(np.finfo(np.float64).eps),
        "big": float(np.float32(2 ** 24) + np.float32(1)),  # 16777217 is not a float32: it rounds to 16777216
    }


# ---------------------------------------------------------------------------
# error analysis
# ---------------------------------------------------------------------------
def compute_error() -> dict:
    xs = 10.0 ** -np.arange(1, 9, 0.25)
    naive = (1 - np.cos(xs)) / xs ** 2
    stable = 2 * np.sin(xs / 2) ** 2 / xs ** 2
    cancel = [{"x": float(x), "naive": float(a), "stable": float(s)} for x, a, s in zip(xs, naive, stable)]
    rng = np.random.default_rng(8)
    sums = []
    for logn in range(2, 7):
        n = 10 ** logn
        v = rng.random(n).astype(np.float32)
        exact = math.fsum(v.astype(np.float64).tolist())
        s = np.float32(0)
        s = np.cumsum(v, dtype=np.float32)[-1]  # sequential float32 accumulation
        kahan = kahan32(v)
        pair = float(np.sum(v, dtype=np.float32))  # numpy sums pairwise
        sums.append({"n": n, "exact": exact, "naive": float(s), "pairwise": pair, "kahan": kahan,
                     "err_naive": abs(float(s) - exact) / exact, "err_pair": abs(pair - exact) / exact,
                     "err_kahan": abs(kahan - exact) / exact})
    # the Patriot: 0.1 s chopped to 23 fraction bits of a 24-bit register
    tenth = math.floor(0.1 * 2 ** 23) / 2 ** 23
    per_tick = 0.1 - tenth
    hours = 100
    drift = per_tick * hours * 3600 * 10
    return {"cancel": cancel, "sums": sums, "u32": 2.0 ** -24,
            "patriot": {"tenth": tenth, "per_tick": per_tick, "hours": hours, "drift": drift, "scud": 1676,
                        "miss_m": drift * 1676},
            "ariane": {"limit": 32767, "year": 1996}}


def kahan32(v: np.ndarray) -> float:
    """Kahan's compensated summation, every operation rounded to float32."""
    s = np.float32(0)
    c = np.float32(0)
    for x in v.tolist():
        y = np.float32(np.float32(x) - c)
        t = np.float32(s + y)
        c = np.float32(np.float32(t - s) - y)
        s = t
    return float(s)


# ---------------------------------------------------------------------------
# Wilkinson's polynomial
# ---------------------------------------------------------------------------
def compute_wilkinson() -> dict:
    import mpmath as mp

    mp.mp.dps = 60
    coef = [mp.mpf(1)]
    for k in range(1, 21):
        new = [mp.mpf(0)] * (len(coef) + 1)
        for i, a in enumerate(coef):
            new[i] += a
            new[i + 1] -= a * k
        coef = new
    frames = []
    prev = None
    for t in np.linspace(0, 1, 41):
        c2 = list(coef)
        c2[1] -= mp.mpf(t) * mp.mpf(2) ** -23
        r = [complex(z) for z in mp.polyroots(c2, maxsteps=800, extraprec=600)]
        if prev is None:
            r.sort(key=lambda z: z.real)
        else:  # follow each root from the previous frame
            order = []
            left = list(r)
            for z0 in prev:
                j = min(range(len(left)), key=lambda j: abs(left[j] - z0))
                order.append(left.pop(j))
            r = order
        prev = r
        frames.append([[z.real, z.imag] for z in r])
    cond = []  # how sensitive each root is: |d root / d a19| = k^19 / prod_{j != k} |k - j|
    for k in range(1, 21):
        den = 1.0
        for j in range(1, 21):
            if j != k:
                den *= abs(k - j)
        cond.append(k ** 19 / den)
    return {"frames": frames, "delta": 2.0 ** -23, "a19": -210, "cond": cond}


# ---------------------------------------------------------------------------
# elementary functions
# ---------------------------------------------------------------------------
def remez_exp(deg=4, a=-math.log(2) / 2, b=math.log(2) / 2, iters=12):
    """The minimax polynomial for e^x on [a, b] (Remez exchange): its coefficients and the equioscillating error."""
    n = deg + 2
    x = (a + b) / 2 + (b - a) / 2 * np.cos(np.pi * np.arange(n)[::-1] / (n - 1))
    for _ in range(iters):
        A = np.zeros((n, n))
        for i in range(n):
            A[i, :deg + 1] = x[i] ** np.arange(deg + 1)
            A[i, deg + 1] = (-1) ** i
        sol = np.linalg.solve(A, np.exp(x))
        c, E = sol[:deg + 1], sol[deg + 1]
        grid = np.linspace(a, b, 20001)
        err = np.exp(grid) - np.polyval(c[::-1], grid)
        # new reference: the extrema of the error, one per sign change
        idx = [0]
        for i in range(1, len(grid) - 1):
            if (err[i] - err[i - 1]) * (err[i + 1] - err[i]) <= 0:
                idx.append(i)
        idx.append(len(grid) - 1)
        cand = sorted(idx, key=lambda i: -abs(err[i]))
        pts = []
        for i in sorted(set(cand[: 3 * n])):
            if not pts or np.sign(err[i]) != np.sign(err[pts[-1]]):
                pts.append(i)
            elif abs(err[i]) > abs(err[pts[-1]]):
                pts[-1] = i
        if len(pts) >= n:
            x = grid[pts[:n]]
    grid = np.linspace(a, b, 401)
    err_mm = np.exp(grid) - np.polyval(c[::-1], grid)
    taylor = sum(grid ** k / math.factorial(k) for k in range(deg + 1))
    err_t = np.exp(grid) - taylor
    return {"coef": c.tolist(), "E": float(abs(E)), "x": grid.tolist(), "err_minimax": err_mm.tolist(),
            "err_taylor": err_t.tolist(), "max_minimax": float(np.abs(err_mm).max()),
            "max_taylor": float(np.abs(err_t).max()), "a": a, "b": b, "deg": deg}


def compute_functions() -> dict:
    theta = 1.0  # radians
    K = 1.0
    x, y, z = 1.0, 0.0, theta
    steps = []
    for i in range(16):
        K /= math.sqrt(1 + 2.0 ** (-2 * i))
        d = 1 if z >= 0 else -1
        steps.append({"i": i, "d": d, "atan": math.atan(2.0 ** -i), "x": x, "y": y, "z": z})
        x, y = x - d * y * 2.0 ** -i, y + d * x * 2.0 ** -i
        z -= d * math.atan(2.0 ** -i)
    return {"cordic": {"theta": theta, "steps": steps, "K": K, "cos": x * K, "sin": y * K,
                       "true": [math.cos(theta), math.sin(theta)]},
            "remez": remez_exp()}


# ---------------------------------------------------------------------------
# The Frontier chapter (videos/cs/SYLLABUS.md 1.1): fast multiplication and correctly rounded functions,
# measured on this machine
# ---------------------------------------------------------------------------
def _cpu_name() -> str:
    try:
        for ln in open("/proc/cpuinfo"):
            if ln.startswith("model name"):
                return ln.split(":", 1)[1].strip()
    except OSError:
        pass
    import platform
    return platform.processor() or platform.machine()


def compute_frontier() -> dict:
    import decimal
    import random
    import time

    import mpmath

    def best(f, reps=3):
        b = 9e9
        for _ in range(reps):
            t = time.perf_counter()
            f()
            b = min(b, time.perf_counter() - t)
        return b

    rnd = random.Random(1)
    mul = []
    for d in (1000, 3000, 10_000, 30_000, 100_000, 300_000, 1_000_000):
        bits = int(d * 3.3219)
        a, b = rnd.getrandbits(bits) | 1, rnd.getrandbits(bits) | 1
        ti = best(lambda: a * b)
        ctx = decimal.Context(prec=2 * d + 10, Emax=decimal.MAX_EMAX, Emin=decimal.MIN_EMIN)
        da = decimal.Decimal("".join(rnd.choice("123456789") for _ in range(d)))
        db = decimal.Decimal("".join(rnd.choice("123456789") for _ in range(d)))
        td = best(lambda: ctx.multiply(da, db))
        mul.append({"digits": d, "int": ti, "decimal": td})
    lx = np.log([m["digits"] for m in mul[2:]])
    slope_int = float(np.polyfit(lx, np.log([m["int"] for m in mul[2:]]), 1)[0])
    slope_dec = float(np.polyfit(lx, np.log([m["decimal"] for m in mul[2:]]), 1)[0])
    # float32 exp: NumPy's against the correctly rounded value (float64 exp, rounded once, checked by mpmath)
    rng = np.random.default_rng(0)
    n = 10_000_000
    x = rng.uniform(-87, 88, n).astype(np.float32)
    got = np.exp(x)
    ref = np.exp(x.astype(np.float64)).astype(np.float32)
    ulps = np.abs(got.view(np.int32).astype(np.int64) - ref.view(np.int32).astype(np.int64))
    bad = np.nonzero(ulps)[0]
    mpmath.mp.prec = 200
    sample = bad[:: max(1, len(bad) // 200)][:200]
    agree = sum(np.float32(float(mpmath.exp(mpmath.mpf(float(x[i]))))) == ref[i] for i in sample)
    return {"cpu": _cpu_name(), "numpy": np.__version__, "mul": mul, "slope_int": slope_int, "slope_dec": slope_dec,
            "ratio_1m": mul[-1]["int"] / mul[-1]["decimal"],
            "exp_n": n, "exp_bad": int(len(bad)), "exp_frac": float(len(bad) / n),
            "exp_ulps": {str(k): int((ulps == k).sum()) for k in range(int(ulps.max()) + 1)},
            "exp_max_ulp": int(ulps.max()), "exp_checked": int(len(sample)), "exp_agree": int(agree)}


def compute_hardround() -> dict:
    """The float32 input whose e^x lies nearest a rounding midpoint (the research problem's answer).  Every float32
    in [-87.33, 88.72] is screened in float64 (error below 2^-28 of a float32 ulp), and the 200 nearest candidates are
    re-measured at 300 bits with mpmath."""
    import mpmath

    lo, hi = np.float32(-87.33), np.float32(88.72)
    ranges = [(0, int(hi.view(np.int32)) + 1, np.uint32), (int(np.float32(-0.0).view(np.uint32)),
                                                          int(lo.view(np.uint32)) + 1, np.uint32)]
    cand, total = [], 0
    for a0, b0, dt in ranges:
        for a in range(a0, b0, 50_000_000):
            u = np.arange(a, min(b0, a + 50_000_000), dtype=dt)
            x = u.view(np.float32).astype(np.float64)
            m, _ = np.frexp(np.exp(x))
            s = m * 2.0 ** 24
            dist = np.abs(s - np.floor(s) - 0.5)
            k = np.argpartition(dist, 40)[:40]
            cand.extend(zip(dist[k].tolist(), x[k].tolist()))
            total += len(u)
    cand.sort()
    mpmath.mp.prec = 300
    exact = []
    for _, x in cand[:200]:
        m, _ = mpmath.frexp(mpmath.exp(mpmath.mpf(x)))
        s = m * 2 ** 24
        exact.append((float(abs(s - mpmath.floor(s) - mpmath.mpf(0.5))), x))
    exact.sort()
    return {"inputs": total, "worst": [{"x": float(np.float32(x)), "distance_ulp": dd,
                                        "bits": 24 + float(-np.log2(dd))} for dd, x in exact[:5]]}


ITEMS = {
    "clock": compute_clock, "adders": compute_adders, "prefix": compute_prefix, "mult": compute_mult,
    "divide": compute_divide, "alu": compute_alu, "floats": compute_floats, "error": compute_error,
    "wilkinson": compute_wilkinson, "functions": compute_functions, "frontier": compute_frontier,
    "hardround": compute_hardround,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
