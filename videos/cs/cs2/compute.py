"""Precompute everything numerical in Part 2 of *Computer Science, Built* ("Proof and Counting").

    python -m videos.cs.cs2.compute              # everything missing (about half a minute)
    python -m videos.cs.cs2.compute --force puzzles

Results are cached in ``.cache/cs2/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Every count, search and
simulation here runs on this computer, and each is checked against the closed form or the theorem it illustrates.

Items:
    puzzles     sliding puzzles: breadth-first search over every position of the 2 x 3 and 3 x 3 puzzles (exactly half
                reachable, and exactly the half the parity invariant allows); the 3 x 3 distance histogram; a random
                walk on the 4 x 4 puzzle with its invariant at every move
    jugs        the water-jug puzzle (3 and 5 gallons): every reachable state, the shortest way to 4; which amounts
                other capacities reach (multiples of the gcd)
    tromino     an 8 x 8 board with one square removed, tiled by L-trominoes recursively: every piece, in order
    rationals   the positive rationals listed without repeats (Calkin-Wilf), and Cantor's pairing of N x N
    pascal      Pascal's triangle: the first rows, and 128 rows mod 2 (Sierpinski's triangle)
    monotone    Erdos-Szekeres: a sequence of 10 with its (increasing, decreasing) labels; the longest increasing
                subsequence of random permutations against sqrt(n)
    derange     derangements: D(n), D(n)/n! against 1/e; the hat-check problem simulated (fixed points against
                Poisson(1)); Euler's phi by inclusion-exclusion
    catalan     Catalan numbers; the five objects of size 3 in four guises (parentheses, binary trees, triangulations,
                lattice paths) matched by bijections; Stirling numbers of the second kind
    numbers     the extended Euclidean algorithm on 1071 and 462 (Bezout); Sunzi's remainder problem (CRT); Euclid's
                primes argument on 2 * 3 * 5 * 7 * 11 * 13 + 1
    chance      Monty Hall simulated; a medical test through Bayes; Markov, Chebyshev and the exact tail for 100
                coin flips; the birthday problem against the union bound
"""

from __future__ import annotations

import itertools
import math
from collections import Counter, deque
from fractions import Fraction

import numpy as np

from explainer.ai.cache import Cache

CACHE = Cache("cs2")
load = CACHE.load


# ---------------------------------------------------------------------------
# sliding puzzles
# ---------------------------------------------------------------------------
def neighbours(board: tuple, rows: int, cols: int):
    """Positions one slide away (0 is the blank)."""
    z = board.index(0)
    r, c = divmod(z, cols)
    for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        rr, cc = r + dr, c + dc
        if 0 <= rr < rows and 0 <= cc < cols:
            j = rr * cols + cc
            b = list(board)
            b[z], b[j] = b[j], b[z]
            yield tuple(b)


def parity(perm) -> int:
    """0 for an even permutation, 1 for odd (by counting cycles)."""
    perm = list(perm)
    seen, cycles = [False] * len(perm), 0
    for i in range(len(perm)):
        if not seen[i]:
            cycles += 1
            j = i
            while not seen[j]:
                seen[j] = True
                j = perm[j]
    return (len(perm) - cycles) % 2


def invariant(board: tuple, rows: int, cols: int) -> int:
    """Parity of the permutation of all squares (blank included, as the last square), plus the blank's taxicab
    distance from its home corner.  Every slide is a transposition and moves the blank one square, so this never
    changes."""
    n = rows * cols
    perm = [(v - 1) % n for v in board]  # tile v belongs at v - 1; the blank (0) at n - 1
    z = board.index(0)
    r, c = divmod(z, cols)
    return (parity(perm) + (rows - 1 - r) + (cols - 1 - c)) % 2


def bfs(start: tuple, rows: int, cols: int):
    dist = {start: 0}
    q = deque([start])
    while q:
        b = q.popleft()
        for nb in neighbours(b, rows, cols):
            if nb not in dist:
                dist[nb] = dist[b] + 1
                q.append(nb)
    return dist


def compute_puzzles() -> dict:
    out = {"sizes": []}
    for rows, cols in ((2, 2), (2, 3), (3, 3)):
        n = rows * cols
        solved = tuple(list(range(1, n)) + [0])
        dist = bfs(solved, rows, cols)
        total = math.factorial(n)
        # the reachable positions are exactly those with the solved position's invariant (0)
        assert len(dist) == total // 2
        assert all(invariant(b, rows, cols) == 0 for b in dist)
        if n <= 6:
            assert sum(1 for p in itertools.permutations(range(n)) if invariant(p, rows, cols) == 0) == total // 2
        hist = Counter(dist.values())
        far = [list(b) for b, d in dist.items() if d == max(hist)]
        out["sizes"].append({"rows": rows, "cols": cols, "total": total, "reachable": len(dist),
                             "max_dist": max(hist), "hist": [hist[k] for k in range(max(hist) + 1)],
                             "farthest": far[:4], "n_farthest": len(far)})
    # Loyd's position: 14 and 15 swapped
    loyd = tuple(list(range(1, 14)) + [15, 14, 0])
    out["loyd_invariant"] = invariant(loyd, 4, 4)
    assert out["loyd_invariant"] == 1
    # a random walk on the 4 x 4 board: the invariant at every move
    rng = np.random.default_rng(7)
    b = tuple(list(range(1, 16)) + [0])
    walk, prev = [list(b)], None
    for _ in range(40):
        opts = [nb for nb in neighbours(b, 4, 4) if nb != prev]
        prev, b = b, opts[rng.integers(len(opts))]
        walk.append(list(b))
    out["walk"] = walk
    out["walk_parity"] = [parity([(v - 1) % 16 for v in w]) for w in walk]
    out["walk_dist"] = [(3 - w.index(0) // 4) + (3 - w.index(0) % 4) for w in walk]
    assert all((p + d) % 2 == 0 for p, d in zip(out["walk_parity"], out["walk_dist"]))
    return out


# ---------------------------------------------------------------------------
# water jugs
# ---------------------------------------------------------------------------
def jug_moves(s, A, B):
    a, b = s
    pour = min(a, B - b)
    back = min(b, A - a)
    return [("fill A", (A, b)), ("fill B", (a, B)), ("empty A", (0, b)), ("empty B", (a, 0)),
            ("pour A into B", (a - pour, b + pour)), ("pour B into A", (a + back, b - back))]


def jugs(A, B):
    prev = {(0, 0): None}
    q = deque([(0, 0)])
    while q:
        s = q.popleft()
        for name, t in jug_moves(s, A, B):
            if t not in prev:
                prev[t] = (s, name)
                q.append(t)
    return prev


def compute_jugs() -> dict:
    A, B, goal = 3, 5, 4
    prev = jugs(A, B)
    target = min((s for s in prev if goal in s), key=lambda s: _depth(prev, s))
    path, s = [], target
    while prev[s] is not None:
        p, name = prev[s]
        path.append({"state": list(s), "move": name})
        s = p
    path = [{"state": [0, 0], "move": "start"}] + path[::-1]
    # every amount ever in a jug is a multiple of gcd(A, B), and every multiple up to B appears
    caps = []
    for a_, b_ in ((3, 5), (4, 6), (6, 9), (5, 7), (6, 10)):
        amounts = sorted({x for s in jugs(a_, b_) for x in s})
        g = math.gcd(a_, b_)
        assert amounts == list(range(0, b_ + 1, g))
        caps.append({"A": a_, "B": b_, "gcd": g, "amounts": amounts})
    return {"A": A, "B": B, "goal": goal, "states": sorted([list(s) for s in prev]), "path": path, "caps": caps}


def _depth(prev, s):
    d = 0
    while prev[s] is not None:
        s = prev[s][0]
        d += 1
    return d


# ---------------------------------------------------------------------------
# tromino tiling
# ---------------------------------------------------------------------------
def tromino(n: int, hole: tuple[int, int]) -> list[dict]:
    """Tile a 2^n x 2^n board missing ``hole`` with L-trominoes: the classic induction, as recursion.  Each piece
    is recorded with the level of the recursion that placed it."""
    pieces = []

    def go(r0, c0, size, hr, hc, level):
        if size == 1:
            return
        h = size // 2
        quads = [(r0, c0), (r0, c0 + h), (r0 + h, c0), (r0 + h, c0 + h)]
        centre = [(r0 + h - 1, c0 + h - 1), (r0 + h - 1, c0 + h), (r0 + h, c0 + h - 1), (r0 + h, c0 + h)]
        holes, piece = [], []
        for (qr, qc), cell in zip(quads, centre):
            if qr <= hr < qr + h and qc <= hc < qc + h:
                holes.append((hr, hc))
            else:
                holes.append(cell)
                piece.append(cell)
        pieces.append({"cells": [list(x) for x in piece], "level": level, "size": size})
        for (qr, qc), (xr, xc) in zip(quads, holes):
            go(qr, qc, h, xr, xc, level + 1)

    go(0, 0, 2 ** n, hole[0], hole[1], 0)
    cover = Counter(tuple(c) for p in pieces for c in p["cells"])
    assert len(pieces) == (4 ** n - 1) // 3 and all(v == 1 for v in cover.values()) and hole not in cover
    return pieces


def compute_tromino() -> dict:
    return {"n": 3, "hole": [5, 2], "pieces": tromino(3, (5, 2)), "small": tromino(2, (0, 3))}


# ---------------------------------------------------------------------------
# rationals and pairing
# ---------------------------------------------------------------------------
def compute_rationals() -> dict:
    q, cw = Fraction(1), []
    for _ in range(31):
        cw.append([q.numerator, q.denominator])
        q = 1 / (2 * math.floor(q) - q + 1)
    assert len({tuple(x) for x in cw}) == 31
    pair = [[(x + y) * (x + y + 1) // 2 + y for y in range(7)] for x in range(7)]  # Cantor's pairing
    assert sorted(v for r in pair for v in r)[:28] == list(range(28))
    return {"calkin_wilf": cw, "pairing": pair}


# ---------------------------------------------------------------------------
# Pascal's triangle
# ---------------------------------------------------------------------------
def compute_pascal() -> dict:
    rows = [[math.comb(n, k) for k in range(n + 1)] for n in range(11)]
    N = 128
    mod2 = np.zeros((N, 2 * N - 1), np.uint8)
    for n in range(N):
        for k in range(n + 1):
            mod2[n, N - 1 - n + 2 * k] = 1 if (math.comb(n, k) & 1) else 0
    # Lucas / Kummer: C(n, k) is odd exactly when k's binary digits are a subset of n's
    assert all(((math.comb(n, k) & 1) == 1) == ((k & n) == k) for n in range(N) for k in range(n + 1))
    odd = [sum(1 for k in range(n + 1) if k & n == k) for n in range(N)]
    assert all(odd[n] == 2 ** bin(n).count("1") for n in range(N))
    vander = [[math.comb(5, k) * math.comb(4, 3 - k) for k in range(4)], math.comb(9, 3)]
    assert sum(vander[0]) == vander[1]
    return {"rows": rows, "mod2": mod2, "odd": odd, "vandermonde": vander}


# ---------------------------------------------------------------------------
# Erdos-Szekeres
# ---------------------------------------------------------------------------
def lis_len(seq) -> int:
    import bisect

    tails = []
    for x in seq:
        i = bisect.bisect_left(tails, x)
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x
    return len(tails)


def labels(seq):
    inc, dec = [], []
    for k, x in enumerate(seq):
        inc.append(1 + max([inc[j] for j in range(k) if seq[j] < x], default=0))
        dec.append(1 + max([dec[j] for j in range(k) if seq[j] > x], default=0))
    return inc, dec


def compute_monotone() -> dict:
    seq = [6, 2, 9, 4, 10, 1, 7, 3, 8, 5]  # ten distinct numbers: some monotone run of 4 must exist
    inc, dec = labels(seq)
    assert len(set(zip(inc, dec))) == len(seq) and max(max(inc), max(dec)) >= 4
    tight = [3, 2, 1, 6, 5, 4, 9, 8, 7]  # nine numbers with no monotone run of 4
    ti, td = labels(tight)
    assert max(ti) == 3 and max(td) == 3
    rng = np.random.default_rng(2)
    rows = []
    for n in (10, 100, 1000, 10000, 100000):
        trials = 200 if n <= 10000 else 40
        vals = [lis_len(rng.permutation(n)) for _ in range(trials)]
        rows.append({"n": n, "mean": float(np.mean(vals)), "ratio": float(np.mean(vals) / math.sqrt(n)),
                     "min": int(min(vals))})
        assert min(vals) * max(1, 1) >= 1
    return {"seq": seq, "inc": inc, "dec": dec, "tight": tight, "tight_inc": ti, "tight_dec": td, "random": rows}


# ---------------------------------------------------------------------------
# inclusion-exclusion
# ---------------------------------------------------------------------------
def derangements(n: int) -> int:
    return sum((-1) ** k * math.comb(n, k) * math.factorial(n - k) for k in range(n + 1))


def compute_derange() -> dict:
    D = [derangements(n) for n in range(13)]
    assert D[:6] == [1, 0, 1, 2, 9, 44]
    assert all(D[n] == (n - 1) * (D[n - 1] + D[n - 2]) for n in range(2, 13))
    assert all(D[n] == sum(1 for p in itertools.permutations(range(n)) if all(p[i] != i for i in range(n)))
               for n in range(8))
    ratio = [D[n] / math.factorial(n) for n in range(13)]
    rng = np.random.default_rng(5)
    sims = []
    for n, trials in ((3, 100_000), (10, 100_000), (52, 100_000), (1000, 20_000)):
        perms = np.argsort(rng.random((trials, n)), axis=1)
        fixed = (perms == np.arange(n)).sum(axis=1)
        h = np.bincount(fixed, minlength=8)[:8] / trials
        sims.append({"n": n, "trials": trials, "mean": float(fixed.mean()), "none": float((fixed == 0).mean()),
                     "hist": h.tolist()})
    poisson = [math.exp(-1) / math.factorial(k) for k in range(8)]
    # 4 hats, the inclusion-exclusion terms: C(4,k) (4-k)!
    terms = [math.comb(4, k) * math.factorial(4 - k) for k in range(5)]
    # Euler's phi by inclusion-exclusion over the prime factors
    def phi(n):
        ps = [p for p in range(2, n + 1) if n % p == 0 and all(p % q for q in range(2, int(p ** 0.5) + 1))]
        tot = 0
        for r in range(len(ps) + 1):
            for sub in itertools.combinations(ps, r):
                tot += (-1) ** r * (n // math.prod(sub)) if sub else n
        return tot
    phis = [phi(n) for n in range(1, 61)]
    assert all(phis[n - 1] == sum(1 for k in range(1, n + 1) if math.gcd(k, n) == 1) for n in range(1, 61))
    surj = [[sum((-1) ** j * math.comb(k, j) * (k - j) ** n for j in range(k + 1)) for k in range(1, 6)]
            for n in range(1, 7)]
    return {"D": D, "ratio": ratio, "e_inv": math.exp(-1), "sims": sims, "poisson": poisson, "terms4": terms,
            "phi": phis, "surj": surj}


# ---------------------------------------------------------------------------
# Catalan numbers and their bijections
# ---------------------------------------------------------------------------
def dyck(n: int) -> list[str]:
    if n == 0:
        return [""]
    out = []
    for k in range(n):
        for a in dyck(k):
            for b in dyck(n - 1 - k):
                out.append("(" + a + ")" + b)
    return sorted(out, reverse=True)


def tree_of(w: str):
    """( A ) B  ->  node(left = tree(A), right = tree(B)); the empty word is the empty tree."""
    if not w:
        return None
    depth = 0
    for i, ch in enumerate(w):
        depth += 1 if ch == "(" else -1
        if depth == 0:
            return [tree_of(w[1:i]), tree_of(w[i + 1:])]
    raise ValueError(w)


def size(t) -> int:
    return 0 if t is None else 1 + size(t[0]) + size(t[1])


def triangles(t, i: int, j: int) -> list:
    """The triangulation of the polygon on vertices i..j that the binary tree t describes."""
    if t is None:
        return []
    k = i + size(t[0]) + 1
    return [[i, k, j]] + triangles(t[0], i, k) + triangles(t[1], k, j)


def compute_catalan() -> dict:
    cat = [math.comb(2 * n, n) // (n + 1) for n in range(13)]
    assert [len(dyck(n)) for n in range(9)] == cat[:9]
    assert all(cat[n + 1] == sum(cat[k] * cat[n - k] for k in range(n + 1)) for n in range(12))
    objs = []
    for w in dyck(3):
        t = tree_of(w)
        tri = triangles(t, 0, 4)
        assert len(tri) == 3
        path = [1 if ch == "(" else -1 for ch in w]
        objs.append({"word": w, "tree": t, "triangles": tri, "path": path})
    assert len({tuple(map(tuple, o["triangles"])) for o in objs}) == 5
    # Stirling numbers of the second kind: S(n, k) ways to split n things into k non-empty groups
    S = [[0] * 7 for _ in range(7)]
    S[0][0] = 1
    for n in range(1, 7):
        for k in range(1, n + 1):
            S[n][k] = k * S[n - 1][k] + S[n - 1][k - 1]
    bell = [sum(r) for r in S]
    assert bell[:7] == [1, 1, 2, 5, 15, 52, 203]
    fib_tilings = [1, 1]
    for _ in range(10):
        fib_tilings.append(fib_tilings[-1] + fib_tilings[-2])
    tilings4 = ["".join(t) for L in range(5) for t in itertools.product("|=", repeat=L)
                if sum(1 if c == "|" else 2 for c in t) == 4]
    assert len(tilings4) == fib_tilings[4]
    return {"catalan": cat, "objects": objs, "stirling": S, "bell": bell, "fib": fib_tilings, "tilings4": tilings4}


# ---------------------------------------------------------------------------
# number theory
# ---------------------------------------------------------------------------
def compute_numbers() -> dict:
    a, b = 1071, 462
    rows = []
    r0, r1, s0, s1, t0, t1 = a, b, 1, 0, 0, 1
    while r1:
        q = r0 // r1
        rows.append({"r": r0, "s": s0, "t": t0, "q": q})
        r0, r1, s0, s1, t0, t1 = r1, r0 - q * r1, s1, s0 - q * s1, t1, t0 - q * t1
    rows.append({"r": r0, "s": s0, "t": t0, "q": None})
    assert r0 == math.gcd(a, b) and s0 * a + t0 * b == r0
    # Sunzi Suanjing: x = 2 mod 3, 3 mod 5, 2 mod 7
    mods, res = [3, 5, 7], [2, 3, 2]
    sols = [x for x in range(105) if all(x % m == r for m, r in zip(mods, res))]
    assert sols == [23]
    # the Chinese remainder construction, term by term
    M = math.prod(mods)
    terms = []
    for m, r in zip(mods, res):
        Mi = M // m
        inv = pow(Mi, -1, m)
        terms.append({"m": m, "r": r, "Mi": Mi, "inv": inv, "term": r * Mi * inv})
    assert sum(t["term"] for t in terms) % M == 23
    prod = math.prod([2, 3, 5, 7, 11, 13]) + 1
    f = [p for p in range(2, prod) if prod % p == 0 and all(p % q for q in range(2, int(p ** 0.5) + 1))]
    assert prod == 30031 and f == [59, 509]
    euclid_numbers = []
    ps = [2, 3, 5, 7, 11, 13, 17]
    for k in range(1, len(ps) + 1):
        v = math.prod(ps[:k]) + 1
        fac, x, p = [], v, 2
        while p * p <= x:
            while x % p == 0:
                fac.append(p)
                x //= p
            p += 1
        if x > 1:
            fac.append(x)
        euclid_numbers.append({"primes": ps[:k], "value": v, "factors": fac})
    return {"a": a, "b": b, "bezout": rows, "mods": mods, "res": res, "solution": 23, "terms": terms, "M": M,
            "euclid": prod, "factors": f, "euclid_numbers": euclid_numbers}


# ---------------------------------------------------------------------------
# probability
# ---------------------------------------------------------------------------
def compute_chance() -> dict:
    rng = np.random.default_rng(11)
    T = 3000
    car = rng.integers(0, 3, T)
    pick = rng.integers(0, 3, T)
    stay = car == pick
    run_stay = np.cumsum(stay) / np.arange(1, T + 1)
    run_switch = np.cumsum(~stay) / np.arange(1, T + 1)
    # Bayes: prevalence 1%, sensitivity 99%, false positives 5%
    p, sens, fp = 0.01, 0.99, 0.05
    post = p * sens / (p * sens + (1 - p) * fp)
    per10000 = {"sick": 100, "sick_pos": 99, "well": 9900, "well_pos": 495}
    assert abs(per10000["sick_pos"] / (per10000["sick_pos"] + per10000["well_pos"]) - post) < 1e-12
    # 100 fair coins: P(X >= 75)
    exact = sum(math.comb(100, k) for k in range(75, 101)) / 2 ** 100
    markov = 50 / 75
    cheb = 25 / 25 ** 2  # P(|X - 50| >= 25) <= Var / 25^2
    # birthdays
    bday = []
    for k in (10, 20, 23, 30, 40, 50, 60):
        none = math.prod((365 - i) / 365 for i in range(k))
        bday.append({"k": k, "exact": 1 - none, "union": min(1.0, math.comb(k, 2) / 365)})
    return {"T": T, "stay": run_stay[::10].tolist(), "switch": run_switch[::10].tolist(),
            "stay_final": float(run_stay[-1]), "switch_final": float(run_switch[-1]), "posterior": post,
            "per10000": per10000, "coins": {"exact": exact, "markov": markov, "chebyshev": cheb}, "birthday": bday}


ITEMS = {
    "puzzles": compute_puzzles, "jugs": compute_jugs, "tromino": compute_tromino, "rationals": compute_rationals,
    "pascal": compute_pascal, "monotone": compute_monotone, "derange": compute_derange, "catalan": compute_catalan,
    "numbers": compute_numbers, "chance": compute_chance,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
