"""Monochord's mathematics of rhythm and scale (Part 33 of *Music, Built*).

    euclid(k, n)                 Bjorklund's algorithm: k onsets spread as evenly as possible over n pulses
    named_euclidean()            Toussaint's catalogue of traditional rhythms that are Euclidean (up to rotation)
    is_rotation(a, b)            whether two rhythms are rotations of each other
    convergents(x)               continued-fraction convergents of x
    mos_sizes(generator)         sizes at which a stack of the generator has two step sizes (moments of symmetry)
    oddity(onsets, n)            Arom's rhythmic oddity: no two onsets split the cycle into equal halves
    homometric_pairs(k, n)       rhythms with the same interval content that are not rotations or reflections
    tilings(A, n)                every B with A + B = Z_n (each pulse covered exactly once), by exact cover
    is_periodic(S, n)            whether S is invariant under some nonzero shift
    VUZA_A, VUZA_B               a Vuza canon at period 72, found by search and verified
    prosody_counts(n)            Pingala's count of rhythms of short and long syllables of total length n (Fibonacci)
    de_bruijn(k, n)              a de Bruijn sequence; ``yamatarajabhanasalagam`` checked against it
    plain_bob_minimus()          the 24 changes of Plain Bob Minimus on four bells
    vals and commas              a temperament as a linear map on prime exponents; commas in its kernel
    best_edos(limit)             equal divisions of the octave ranked by their error on 3/2 and 5/4
    bohlen_pierce()              the 13-step division of the 3:1 'tritave'
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, permutations
from math import gcd, log2

import numpy as np


# ------------------------------------------------------------------------------------------------- Euclid
def euclid(k: int, n: int) -> list[int]:
    """Bjorklund's algorithm (2003): distribute k ones among n slots as evenly as possible, by Euclid's
    remainder process on sequences.  Returns a list of 0s and 1s starting with an onset."""
    if k <= 0:
        return [0] * n
    if k >= n:
        return [1] * n
    a = [[1] for _ in range(k)]
    b = [[0] for _ in range(n - k)]
    while len(b) > 1:
        m = min(len(a), len(b))
        a, b = [a[i] + b[i] for i in range(m)], (a[m:] if len(a) > m else b[m:])
    out = [x for s in a + b for x in s]
    return out


def euclid_steps(k: int, n: int) -> list:
    """The stages of Bjorklund's process, for drawing: each a list of groups (strings of x and .)."""
    a = [["x"] for _ in range(k)]
    b = [["."] for _ in range(n - k)]
    stages = [["".join(s) for s in a + b]]
    while len(b) > 1:
        m = min(len(a), len(b))
        a, b = [a[i] + b[i] for i in range(m)], (a[m:] if len(a) > m else b[m:])
        stages.append(["".join(s) for s in a + b])
    return stages


def onsets(pattern) -> list[int]:
    return [i for i, x in enumerate(pattern) if x]


def pattern_of(onsets_, n: int) -> list[int]:
    s = set(onsets_)
    return [1 if i in s else 0 for i in range(n)]


def is_rotation(a, b) -> bool:
    a, b = list(a), list(b)
    return len(a) == len(b) and any(a[i:] + a[:i] == b for i in range(len(a)))


def steps(pattern) -> list[int]:
    """Inter-onset intervals round the cycle."""
    o = onsets(pattern)
    n = len(pattern)
    return [(o[(i + 1) % len(o)] - o[i]) % n or n for i in range(len(o))]


# Toussaint (2005), "The Euclidean algorithm generates traditional musical rhythms": a selection, each written as a
# timeline of x (onset) and . (rest), as usually played; every one is a rotation of euclid(k, n).
NAMED = [
    (3, 8, "x..x..x.", "tresillo (Cuba), and much else"),
    (5, 8, "x.xx.xx.", "cinquillo (Cuba)"),
    (2, 5, "x.x..", "khafif-e-ramal (Persia)"),
    (3, 7, "x.x.x..", "ruchenitza (Bulgaria)"),
    (4, 9, "x.x.x.x..", "aksak (Turkey)"),
    (5, 12, "x..x.x..x.x.", "a timeline of the Venda (South Africa)"),
    (7, 12, "x.x.xx.x.x.x", "the standard bell pattern (West Africa)"),
    (5, 16, "x..x..x...x..x..", "bossa nova (Brazil)"),
    (7, 16, "x..x.x.x..x.x.x.", "a samba pattern (Brazil)"),
]


def parse(s: str) -> list[int]:
    return [1 if c == "x" else 0 for c in s]


def named_euclidean() -> list[dict]:
    out = []
    for k, n, s, name in NAMED:
        p = parse(s)
        out.append({"k": k, "n": n, "pattern": s, "name": name, "euclid": "".join("x" if x else "." for x in euclid(k, n)),
                    "rotation": is_rotation(p, euclid(k, n)), "steps": steps(p)})
    return out


# ------------------------------------------------------------------------------------------------- scales
def convergents(x: float, terms: int = 8) -> list[Fraction]:
    a, out = [], []
    y = x
    for _ in range(terms):
        q = int(np.floor(y))
        a.append(q)
        if abs(y - q) < 1e-12:
            break
        y = 1.0 / (y - q)
    for i in range(1, len(a) + 1):
        f = Fraction(a[i - 1])
        for q in reversed(a[: i - 1]):
            f = q + 1 / f
        out.append(f)
    return out


def mos_sizes(generator: float = log2(1.5), limit: int = 60) -> list[int]:
    """Sizes n at which n stacked generators (mod the octave) leave exactly two step sizes."""
    out = []
    for n in range(2, limit + 1):
        pts = np.sort((np.arange(n) * generator) % 1.0)
        g = np.diff(np.concatenate([pts, [pts[0] + 1]]))
        if len(np.unique(np.round(g, 9))) == 2:
            out.append(n)
    return out


# ------------------------------------------------------------------------------------------------- oddity, homometry
def oddity(ons, n: int) -> bool:
    """Arom's rhythmic oddity property (n even): no two onsets are exactly half the cycle apart."""
    s = set(ons)
    return all((x + n // 2) % n not in s for x in s)


def interval_content(ons, n: int) -> tuple:
    v = [0] * (n // 2 + 1)
    for a, b in combinations(sorted(ons), 2):
        d = (b - a) % n
        v[min(d, n - d)] += 1
    return tuple(v[1:])


def _dihedral_canon(ons, n: int) -> tuple:
    forms = []
    for s in (list(ons), [(-x) % n for x in ons]):
        for t in range(n):
            forms.append(tuple(sorted((x + t) % n for x in s)))
    return min(forms)


def homometric_pairs(k: int, n: int) -> list[tuple]:
    """Classes of k-onset rhythms in n pulses (up to rotation and reflection) sharing interval content with another."""
    by = {}
    for c in combinations(range(n), k):
        if c[0] != 0:
            continue
        key = _dihedral_canon(c, n)
        by.setdefault(interval_content(c, n), set()).add(key)
    return [tuple(sorted(v)) for v in by.values() if len(v) > 1]


# ------------------------------------------------------------------------------------------------- tiling canons
def is_periodic(S, n: int) -> bool:
    S = set(x % n for x in S)
    return any(all((x + p) % n in S for x in S) for p in range(1, n) if n % p == 0)


def is_tiling(A, B, n: int) -> bool:
    seen = [0] * n
    for a in A:
        for b in B:
            seen[(a + b) % n] += 1
    return all(x == 1 for x in seen)


def tilings(A, n: int, limit: int = 100000) -> list[list[int]]:
    """Every B containing 0 with A + B = Z_n exactly once over, by exact-cover backtracking."""
    A = sorted(x % n for x in A)
    out, cover, B = [], [False] * n, []

    def go():
        if len(out) >= limit:
            return
        try:
            c = cover.index(False)
        except ValueError:
            out.append(sorted(B))
            return
        for a in A:
            t = (c - a) % n
            cells = [(x + t) % n for x in A]
            if all(not cover[y] for y in cells):
                for y in cells:
                    cover[y] = True
                B.append(t)
                go()
                B.pop()
                for y in cells:
                    cover[y] = False

    go()
    return out


VUZA_N = 72
VUZA_A = (0, 8, 16, 18, 26, 34)                                     # = {0, 8, 16} + {0, 18}
VUZA_B = (0, 1, 5, 24, 25, 29, 30, 36, 49, 53, 60, 66)


def vuza_check() -> dict:
    return {"tiles": is_tiling(VUZA_A, VUZA_B, VUZA_N), "A_periodic": is_periodic(VUZA_A, VUZA_N),
            "B_periodic": is_periodic(VUZA_B, VUZA_N)}


# ------------------------------------------------------------------------------------------------- prosody
def prosody_counts(n: int) -> list[int]:
    """Rhythms of short (1) and long (2) syllables with total length m, for m = 1 ... n (Pingala; Virahanka)."""
    c = [1, 1]
    for m in range(2, n + 1):
        c.append(c[-1] + c[-2])
    return c[1:n + 1]


def prosody_rhythms(m: int) -> list[str]:
    out = []

    def go(s, left):
        if left == 0:
            out.append(s)
            return
        go(s + "S", left - 1)
        if left >= 2:
            go(s + "L", left - 2)

    go("", m)
    return out


YAMATA = ["ya", "mā", "tā", "rā", "ja", "bhā", "na", "sa", "la", "gā"]
YAMATA_BITS = [0, 1, 1, 1, 0, 1, 0, 0, 0, 1]                        # 0 light (short), 1 heavy (long)


def windows(bits, k: int) -> list[tuple]:
    return [tuple(bits[i:i + k]) for i in range(len(bits) - k + 1)]


def de_bruijn(k: int, n: int) -> list[int]:
    """A de Bruijn sequence B(k, n) (cyclic), by the standard Lyndon-word construction."""
    a = [0] * k * n
    seq = []

    def db(t, p):
        if t > n:
            if n % p == 0:
                seq.extend(a[1:p + 1])
        else:
            a[t] = a[t - p]
            db(t + 1, p)
            for j in range(a[t - p] + 1, k):
                a[t] = j
                db(t + 1, t)

    db(1, 1)
    return seq


# ------------------------------------------------------------------------------------------------- change ringing
def apply_place(row: tuple, places: str) -> tuple:
    """One change: 'x' swaps every pair; otherwise the listed places (1-based) stay and the rest swap in pairs."""
    r = list(row)
    n = len(r)
    keep = set() if places == "x" else {int(c) - 1 for c in places}
    i = 0
    while i < n:
        if i in keep:
            i += 1
            continue
        if i + 1 < n and i + 1 not in keep:
            r[i], r[i + 1] = r[i + 1], r[i]
            i += 2
        else:
            i += 1
    return tuple(r)


def plain_hunt(n: int = 4) -> list[tuple]:
    row = tuple(range(1, n + 1))
    rows = [row]
    pn = ["x", "1" + str(n)] if n % 2 == 0 else ["1", str(n)]
    for i in range(2 * n - 1):
        row = apply_place(row, pn[i % 2])
        rows.append(row)
    return rows


def plain_bob_minimus() -> list[tuple]:
    """Plain Bob Minimus: x 14 x 14 x 14 x 12, three times: 24 changes, every order of four bells once."""
    lead = ["x", "14", "x", "14", "x", "14", "x", "12"]
    row = (1, 2, 3, 4)
    rows = [row]
    for _ in range(3):
        for p in lead:
            row = apply_place(row, p)
            rows.append(row)
    return rows


# ------------------------------------------------------------------------------------------------- temperaments
PRIMES = (2, 3, 5)


def monzo(r: Fraction) -> tuple:
    """Prime exponents of a 5-limit ratio."""
    out = []
    num, den = r.numerator, r.denominator
    for p in PRIMES:
        e = 0
        while num % p == 0:
            num //= p
            e += 1
        while den % p == 0:
            den //= p
            e -= 1
        out.append(e)
    if num != 1 or den != 1:
        raise ValueError("not 5-limit")
    return tuple(out)


def patent_val(n: int) -> tuple:
    """The equal division's nearest step counts for 2, 3 and 5."""
    return tuple(int(round(n * log2(p))) for p in PRIMES)


def tempers_out(val, ratio: Fraction) -> bool:
    return sum(v * e for v, e in zip(val, monzo(ratio))) == 0


def edo_error(n: int) -> dict:
    fifth = 1200 * round(n * log2(1.5)) / n - 1200 * log2(1.5)
    third = 1200 * round(n * log2(1.25)) / n - 1200 * log2(1.25)
    return {"n": n, "fifth": fifth, "third": third, "worst": max(abs(fifth), abs(third))}


def best_edos(limit: int = 60) -> list[dict]:
    """Equal divisions that approximate both 3/2 and 5/4 better (in worst-case cents) than every smaller division."""
    rec, best = [], 1e9
    for n in range(5, limit + 1):
        e = edo_error(n)
        if e["worst"] < best - 1e-9:
            best = e["worst"]
            rec.append(e)
    return rec


# ------------------------------------------------------------------------------------------------- Bohlen–Pierce
def bohlen_pierce() -> dict:
    step = 1200 * log2(3) / 13
    targets = {"9/7": 9 / 7, "7/5": 7 / 5, "5/3": 5 / 3, "9/5": 9 / 5, "7/3": 7 / 3, "3/1": 3.0}
    out = {}
    for name, r in targets.items():
        c = 1200 * log2(r)
        k = round(c / step)
        out[name] = {"steps": k, "error": k * step - c}
    return {"step_cents": step, "tritave_cents": 1200 * log2(3), "ratios": out}
