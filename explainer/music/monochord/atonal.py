"""Twelve tones (Part 29): pitch-class sets, their classes and interval vectors, Z-relations, the hexachord theorem,
twelve-tone rows with their forty-eight forms, all-interval rows, combinatoriality, and what a row looks like in a score.

Pitch classes are integers mod 12.  Transposition T_n adds n; inversion I_n maps x to n - x.  A *set class* is a set up
to transposition and inversion; its *prime form* is the most compact, left-packed representative (Rahn's ordering).  No
manim.
"""

from __future__ import annotations

from itertools import combinations, permutations
from math import comb

import numpy as np

N = 12


# ---------------------------------------------------------------------------------------------------------- sets
def norm(pcs) -> tuple[int, ...]:
    return tuple(sorted({int(p) % N for p in pcs}))


def transpose(pcs, n: int) -> tuple[int, ...]:
    return norm(p + n for p in pcs)


def invert(pcs, n: int = 0) -> tuple[int, ...]:
    return norm(n - p for p in pcs)


def normal_order(pcs) -> tuple[int, ...]:
    """The rotation of the set spanning the smallest interval, ties broken by packing to the left (Rahn)."""
    s = norm(pcs)
    if not s:
        return ()
    rots = [s[i:] + tuple(x + N for x in s[:i]) for i in range(len(s))]

    def key(r):
        return tuple(r[-1 - k] - r[0] for k in range(len(r)))           # outer span first, then inner spans from the right
    return tuple(x % N for x in min(rots, key=key))


def prime_form(pcs) -> tuple[int, ...]:
    """The set class's representative: the more compact of the normal orders of the set and its inversion, from 0."""
    s = norm(pcs)
    if not s:
        return ()
    cands = []
    for t in (s, invert(s)):
        no = normal_order(t)
        cands.append(tuple((x - no[0]) % N for x in no))

    def key(r):
        return tuple(r[-1 - k] for k in range(len(r)))
    return min(cands, key=key)


def interval_vector(pcs) -> tuple[int, ...]:
    """How many pairs of the set lie each interval class (1 to 6) apart."""
    v = [0] * 6
    for a, b in combinations(norm(pcs), 2):
        d = (b - a) % N
        v[min(d, N - d) - 1] += 1
    return tuple(v)


def set_classes() -> dict:
    """Every set class (up to transposition and inversion), found by brute force over the 4,096 sets."""
    out: dict = {}
    for m in range(1 << N):
        s = tuple(i for i in range(N) if m >> i & 1)
        out.setdefault(prime_form(s), 0)
        out[prime_form(s)] += 1
    return out


def burnside_ti(n: int = N) -> int:
    """The number of set classes under the dihedral group of order 24, by Burnside's lemma: the average number of
    subsets each of the 24 operations leaves alone."""
    total = 0
    for k in range(n):                                                    # transpositions: 2^gcd(k, n)
        total += 2 ** np.gcd(k, n)
    for k in range(n):                                                    # inversions x -> k - x
        fixed_points = sum(1 for x in range(n) if (k - x) % n == x)
        cycles = fixed_points + (n - fixed_points) // 2
        total += 2 ** cycles
    return int(total // (2 * n))


def z_pairs() -> list[tuple]:
    """Pairs of different set classes with the same interval vector: Forte's Z-related sets."""
    by_vec: dict = {}
    for pf in set_classes():
        by_vec.setdefault((len(pf), interval_vector(pf)), []).append(pf)
    return [tuple(v) for v in by_vec.values() if len(v) > 1]


def complement(pcs) -> tuple[int, ...]:
    s = set(norm(pcs))
    return tuple(x for x in range(N) if x not in s)


def hexachord_theorem() -> dict:
    """Babbitt's hexachord theorem, checked on all 924 six-note sets: a hexachord and its complement have the same
    interval vector."""
    checked = 0
    ok = True
    same_class = 0
    for s in combinations(range(N), 6):
        checked += 1
        c = complement(s)
        ok &= interval_vector(s) == interval_vector(c)
        same_class += prime_form(s) == prime_form(c)
    return {"checked": checked, "holds": bool(ok), "complement_same_class": same_class}


def ic_count_with_complement(pcs) -> list[int]:
    """For a k-set S and its complement C in Z12: IV(C) - IV(S) = (12 - 2k) times (1,1,1,1,1,1/2), the general form
    of the theorem (zero when k = 6)."""
    s = norm(pcs)
    a, b = interval_vector(s), interval_vector(complement(s))
    return [bb - aa for aa, bb in zip(a, b)]


# ----------------------------------------------------------------------------------------------------------- rows
def is_row(row) -> bool:
    return sorted(int(p) % N for p in row) == list(range(N))


def forms(row) -> dict:
    """The 48 forms of a row: P_n, I_n, R_n, RI_n, named by their first note (for P and I)."""
    p0 = [(p - row[0]) % N for p in row]
    i0 = [(-p) % N for p in p0]
    out = {}
    for n in range(N):
        P = [(x + n) % N for x in p0]
        I = [(x + n) % N for x in i0]
        out[f"P{n}"] = P
        out[f"I{n}"] = I
        out[f"R{n}"] = P[::-1]
        out[f"RI{n}"] = I[::-1]
    return out


def distinct_forms(row) -> int:
    return len({tuple(v) for v in forms(row).values()})


def intervals(row) -> list[int]:
    return [(b - a) % N for a, b in zip(row, row[1:])]


def is_all_interval(row) -> bool:
    return sorted(intervals(row)) == list(range(1, N))


def all_interval_rows() -> list[tuple[int, ...]]:
    """Every row starting on 0 whose eleven successive intervals are all different (each of 1 to 11 once), by depth-first
    search."""
    out = []
    row = [0]
    used_p = {0}
    used_i = set()

    def go():
        if len(row) == N:
            out.append(tuple(row))
            return
        for i in range(1, N):
            if i in used_i:
                continue
            p = (row[-1] + i) % N
            if p in used_p:
                continue
            row.append(p)
            used_p.add(p)
            used_i.add(i)
            go()
            row.pop()
            used_p.discard(p)
            used_i.discard(i)
    go()
    return out


def combinatorial(hexachord) -> dict:
    """Which operations map a hexachord onto its complement (so that a row and that form of it, sounded together, make
    two aggregates): P (transposition), I (inversion), R and RI follow from them."""
    h = set(norm(hexachord))
    c = set(complement(h))
    t = [n for n in range(N) if set(transpose(h, n)) == c]
    i = [n for n in range(N) if set(invert(h, n)) == c]
    return {"T": t, "I": i, "all": bool(t) and bool(i)}


def all_combinatorial_hexachords() -> list[tuple[int, ...]]:
    """Set classes of hexachords that map onto their complements under some transposition and some inversion (Babbitt's
    all-combinatorial hexachords; there are six)."""
    out = []
    for pf in set_classes():
        if len(pf) == 6 and combinatorial(pf)["all"]:
            out.append(pf)
    return sorted(out)


def matrix(row) -> list[list[int]]:
    """The 12 by 12 row matrix: P forms across, I forms down."""
    p0 = [(p - row[0]) % N for p in row]
    i0 = [(-p) % N for p in p0]
    return [[(row[0] + i0[r] + p0[c]) % N for c in range(N)] for r in range(N)]


def row_of(notes, k: int = 12) -> list[int]:
    """The first k distinct pitch classes in a line of (key number, onset, duration) notes, in order."""
    out = []
    for p, _, _ in sorted(notes, key=lambda n: n[1]):
        pc = int(p) % N
        if pc not in out:
            out.append(pc)
        if len(out) == k:
            break
    return out


def find_form(segment, row) -> list[str]:
    """Which of the row's 48 forms begin with the given pitch-class segment."""
    seg = [int(x) % N for x in segment]
    return [name for name, f in forms(row).items() if f[: len(seg)] == seg]


def tune_row(intervals_seq, start: int = 0) -> list[int]:
    """A row grown from a melody's intervals: follow each interval in turn (up, or else down), skipping any that would
    repeat a pitch class, then fill the remaining pitch classes by the smallest available step."""
    row = [start % N]
    for iv in intervals_seq:
        for cand in ((row[-1] + iv) % N, (row[-1] - iv) % N):
            if cand not in row and iv % N:
                row.append(cand)
                break
        if len(row) == N:
            return row
    while len(row) < N:
        rest = [x for x in range(N) if x not in row]
        row.append(min(rest, key=lambda x: (min((x - row[-1]) % N, (row[-1] - x) % N), x)))
    return row


def random_rows(n: int, rng) -> list[list[int]]:
    return [list(rng.permutation(N)) for _ in range(n)]


def homometric(a, b) -> bool:
    """Two sets are homometric when they have the same interval content (the crystallographers' word for the same
    Patterson function) but are not related by transposition or inversion."""
    return interval_vector(a) == interval_vector(b) and prime_form(a) != prime_form(b)


def chance_distinct(k: int) -> float:
    """The share of k-note sets of pitch classes (out of comb(12, k)) whose set class is its own complement's class."""
    if k != 6:
        return 0.0
    return hexachord_theorem()["complement_same_class"] / comb(N, 6)
