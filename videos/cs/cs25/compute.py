"""Precompute everything numerical in Part 25 of *Computer Science, Built* ("Undecidable").

    python -m videos.cs.cs25.compute              # everything missing
    python -m videos.cs.cs25.compute --force pcp

Results are cached in ``.cache/cs25/<name>.json``; scenes call ``load(name)``.  The instrument is
``explainer/cs/algo/computability.py`` (tested in tests/test_cs25_computability.py).

Items:
    quines    a Python quine and a Pebble-language quine, run on the emulator, output checked against source
    pcp       Sipser's example; the TM-to-PCP reduction on a small machine; the hardest small instances found
    tiles     Jeandel and Rao's 11 tiles: rectangles found, every small torus refuted
    hilbert   Pell equations by brute force and by continued fractions
    fractran  Conway's PRIMEGAME producing primes
    collatz   trajectories and records below a million
    godel     Gödel numbers of three formulas, encoded as prime powers and decoded back
    kolmo     compressed sizes of random, textual and structured data
    omega     lower bounds on the halting probability of random 3-state machines, against the step budget
    hat       the 2023 monotile's outline
"""

from __future__ import annotations

import random
import time

import numpy as np

from explainer.ai.cache import Cache
from explainer.cs.algo import computability as C

CACHE = Cache("cs25")
load = CACHE.load


def compute_quines() -> dict:
    import contextlib
    import io
    from explainer.cs.lang.compiler import driver as Dr
    q = C.python_quine()
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec(q, {})
    src = C.pebble_quine()
    comp = Dr.compile_program(src, 2)
    r = Dr.run(comp, b"")
    out = bytes(r.output).decode()
    assert out == src
    lines = src.splitlines()
    return {"python": q, "python_ok": buf.getvalue() == q, "pebble_len": len(src), "pebble_lines": len(lines),
            "pebble_ok": out == src, "pebble_steps": int(getattr(r, "steps", 0)),
            "pebble_head": lines[:14], "pebble_data": lines[14:18], "pebble_tail": lines[-16:],
            "data_lines": sum(1 for ln in lines if ln.strip().startswith("d["))}


def compute_pcp() -> dict:
    sip = [("b", "ca"), ("a", "ab"), ("ca", "a"), ("abc", "c")]
    seq, nodes = C.pcp_solve(sip, 10)
    rules = {("q", "1"): ("p", "1", "R"), ("p", "0"): ("a", "0", "R"), ("q", "0"): ("r", "0", "R"),
             ("p", "1"): ("r", "1", "R"), ("q", "_"): ("r", "_", "R"), ("p", "_"): ("r", "_", "R")}
    D = C.tm_to_mpcp(rules, "q", "a", "10", "01")
    s2, n2 = C.pcp_solve(D, 60, first=0)
    hist = C.run_tm_history(rules, "q", "a", "10")
    top = "".join(D[i][0] for i in s2)
    assert top.startswith(hist)
    # the hardest random 3-domino instances over {0,1} with words of length <= 3
    rng = random.Random(25)
    words = ["0", "1", "00", "01", "10", "11", "000", "001", "010", "011", "100", "101", "110", "111"]
    best = []
    tried = 0
    t0 = time.time()
    while time.time() - t0 < 120 and tried < 20000:
        inst = [(rng.choice(words), rng.choice(words)) for _ in range(3)]
        tried += 1
        s, nn = C.pcp_solve(inst, 60, max_nodes=20000)
        if s is not None:
            best.append((len(s), inst, s, nn))
    best.sort(key=lambda x: -x[0])
    hard = [{"len": b[0], "dominoes": b[1], "match": b[2], "nodes": b[3]} for b in best[:5]]
    lens = [b[0] for b in best]
    return {"sipser": sip, "sipser_match": seq, "sipser_nodes": nodes, "tm_dominoes": D, "tm_match": s2,
            "tm_nodes": n2, "history": hist, "tm_top": top, "hard": hard, "tried": tried, "solved": len(best),
            "len_hist": {str(k): lens.count(k) for k in sorted(set(lens))}}


def compute_tiles() -> dict:
    T = C.JEANDEL_RAO
    rects = []
    for n in (4, 8, 12, 16, 20):
        t0 = time.time()
        g, nodes, _ = C.wang_tile(T, n, n, limit=50_000_000)
        rects.append({"n": n, "found": g is not None, "nodes": nodes, "seconds": time.time() - t0,
                      "grid": g if n in (8, 12) else None})
    tori = []
    for n in range(1, 9):
        for m in range(1, 9):
            g, nodes, done = C.wang_tile(T, n, m, limit=3_000_000, periodic=True)
            tori.append({"n": n, "m": m, "found": g is not None, "complete": done, "nodes": nodes})
    # a set that tiles periodically, for contrast: two tiles alternating
    P = [(0, 1, 1, 0), (1, 0, 0, 1)]
    gp, _, _ = C.wang_tile(P, 4, 4, periodic=True)
    return {"tiles": T, "rects": rects, "tori": tori, "refuted": sum(1 for t in tori if not t["found"] and t["complete"]),
            "periodic_example": P, "periodic_grid": gp}


def compute_hilbert() -> dict:
    rows = []
    for D in (2, 3, 5, 7, 13, 29, 61, 109, 181, 991):
        t0 = time.time()
        x, y = C.pell(D)
        tc = time.time() - t0
        rows.append({"D": D, "x": str(x), "y": str(y), "digits": len(str(x)), "cf_seconds": tc})
    # brute force: try y = 1, 2, ... until D y^2 + 1 is a square
    import math
    brute = []
    for D in (13, 29, 61):
        t0 = time.time()
        y = 1
        found = None
        while time.time() - t0 < 20:
            v = D * y * y + 1
            r = math.isqrt(v)
            if r * r == v:
                found = (r, y)
                break
            y += 1
        brute.append({"D": D, "found": found is not None, "tried": y, "seconds": time.time() - t0})
    return {"rows": rows, "brute": brute}


def compute_fractran() -> dict:
    t0 = time.time()
    out = C.fractran(C.PRIMEGAME, 2, 3_000_000)
    return {"primes": [p for _, p in out], "steps": [s for s, _ in out], "seconds": time.time() - t0}


def compute_collatz() -> dict:
    N = 1_000_000
    L = np.zeros(N, dtype=np.int32)
    best, best_n, peak_best, peak_n = 0, 1, 1, 1
    records = []
    for n in range(2, N):
        m, s, pk = n, 0, n
        while m >= n:
            m = m // 2 if m % 2 == 0 else 3 * m + 1
            pk = max(pk, m)
            s += 1
        L[n] = s + L[m]
        if L[n] > best:
            best, best_n = int(L[n]), n
            records.append((n, best))
        if pk > peak_best:
            peak_best, peak_n = pk, n
    traj = []
    m = 27
    while m != 1:
        traj.append(m)
        m = m // 2 if m % 2 == 0 else 3 * m + 1
    traj.append(1)
    return {"N": N, "longest_n": best_n, "longest": best, "records": records, "peak_n": peak_n, "peak": peak_best,
            "traj27": traj, "verified_to": "beyond 2^68 (Barina, 2020)"}


def compute_kolmo() -> dict:
    from videos.cs.cs16.compute import _full_text
    n = 100_000
    rng = random.Random(5)
    samples = {
        "random bytes": bytes(rng.getrandbits(8) for _ in range(n)),
        "English text": _full_text()[1_000_000:1_000_000 + n],
        "digits of pi": C.pi_digits(n).encode(),
        "Thue-Morse": C.thue_morse(n).encode(),
        "0101...": ("01" * (n // 2)).encode(),
        "all zeros": b"0" * n,
    }
    rows = []
    for name, data in samples.items():
        r = C.complexity_proxies(data)
        rows.append({"name": name, **r, "best": min(r["zlib"], r["bz2"], r["lzma"])})
    # counting: how many n-bit strings compress by k bits?
    import inspect
    src = inspect.getsource(C.pi_digits)
    return {"rows": rows, "n": n, "pi_program_bytes": len(src.encode()), "pi_program_lines": len(src.splitlines())}


def compute_godel() -> dict:
    """Godel numbering: symbol codes, a formula as a product of prime powers, and its decoding."""
    codes = {"0": 1, "S": 2, "=": 3, "+": 4, "(": 5, ")": 6, "¬": 7, "∀": 8, "x": 9, "→": 10}
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]
    out = []
    for f in ["0=0", "S0=S0", "∀x(x+0=x)"]:
        g = 1
        for p_, ch in zip(primes, f):
            g *= p_ ** codes[ch]
        # decode by factoring out each prime in turn
        dec, h = [], g
        for p_ in primes:
            e = 0
            while h % p_ == 0:
                h //= p_
                e += 1
            if e == 0:
                break
            dec.append(e)
        inv = {v: k for k, v in codes.items()}
        assert "".join(inv[e] for e in dec) == f
        out.append({"formula": f, "codes": [codes[c] for c in f], "number": str(g), "digits": len(str(g))})
    return {"codes": codes, "rows": out}


def compute_omega() -> dict:
    """Random 3-state, 2-symbol machines (each transition uniform over write x move x {A, B, C, halt}); the
    fraction seen to halt within t steps is a lower bound on this model's halting probability, rising with t and
    never certified."""
    from explainer.cs import turing as T
    rng = random.Random(3)
    N = 5000
    budgets = [1, 2, 4, 8, 16, 32, 64, 128, 512, 2000]
    halt_at = []
    states = "ABC"
    for _ in range(N):
        rules = []
        for s in states:
            for sym in "01":
                w = rng.choice("01")
                mv = rng.choice("LR")
                nx = rng.choice("ABCZ")
                rules.append((s, sym, w, mv, nx))
        text = "_".join("".join(f"{w}{mv}{nx}" for (st, sy, w, mv, nx) in rules[2 * i:2 * i + 2]) for i in range(3))
        tm = T.TM.parse(text)
        r = T.run(tm, max_steps=budgets[-1])
        halt_at.append(r.steps if r.halted else None)
    rows = [{"t": t, "fraction": sum(1 for h in halt_at if h is not None and h <= t) / N} for t in budgets]
    longest = max(h for h in halt_at if h is not None)
    return {"N": N, "rows": rows, "longest": longest}


def compute_hat() -> dict:
    P = C.hat_polygon()
    return {"P": P.tolist(), "area": C.shoelace(P), "kites": 8}


ITEMS = {k[8:]: v for k, v in globals().items() if k.startswith("compute_")}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
