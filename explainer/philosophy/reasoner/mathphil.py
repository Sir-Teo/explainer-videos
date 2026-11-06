"""Objects of the philosophy of mathematics, built small enough to check (Part 9).

    from explainer.philosophy.reasoner import mathphil as M
    M.frege_numbers(4)          # 16 concepts fall into 5 numbers, 1-4-6-4-1, and successor runs 0 -> 1 -> ... -> 4
    M.abstraction_demands(5)    # Hume's principle, Basic Law V and the nuisance principle: objects needed vs had
    M.typical(M.ENGLISHMEN)     # Russell's typical Englishman, level by level
    M.automorphisms(4, rels)    # every symmetry of a small structure
    M.pi_digits(1000)           # Gibbons's spigot
    M.euler(M.POLYHEDRA["cube"])  # V - E + F
"""

from __future__ import annotations

import itertools
import math
from fractions import Fraction


# ---------------------------------------------------------------------------
# The Meno: doubling the square
# ---------------------------------------------------------------------------
def meno() -> list:
    """The boy's guesses for the side of a square of area 8 (twice the square of side 2), and the answer: the
    square on the diagonal, made of four half-squares."""
    return [{"side": "4", "area": 16}, {"side": "3", "area": 9}, {"side": "the diagonal", "area": 4 * 4 // 2}]


# ---------------------------------------------------------------------------
# Frege's numbers on a finite domain
# ---------------------------------------------------------------------------
def equinumerous(f, g) -> bool:
    """A one-to-one correspondence between f and g exists: search for one, pairing elements in order."""
    f, g = sorted(f), sorted(g)
    if len(f) != len(g):
        return False
    pairing = list(zip(f, g))
    return len({a for a, _ in pairing}) == len(f) and len({b for _, b in pairing}) == len(g)


def frege_numbers(n: int = 4) -> dict:
    """Concepts over a domain of n objects are its subsets. Hume's principle: the number of F is the number of G iff
    F and G are equinumerous; so each number is a class of concepts. Frege's successor relation: m follows k if
    some F and x under F have #F = m and #(F without x) = k."""
    dom = list(range(n))
    concepts = [frozenset(c) for r in range(n + 1) for c in itertools.combinations(dom, r)]
    classes = []
    for c in concepts:
        for cl in classes:
            if equinumerous(c, cl[0]):
                cl.append(c)
                break
        else:
            classes.append([c])
    idx = {c: i for i, cl in enumerate(classes) for c in cl}
    succ = sorted({(idx[f - {x}], idx[f]) for f in concepts for x in f})
    return {"concepts": len(concepts), "class_sizes": [len(cl) for cl in classes], "zero": idx[frozenset()],
            "successor": succ, "members": [len(cl[0]) for cl in classes]}


def abstraction_demands(nmax: int = 5) -> list:
    """An abstraction principle gives one object for each class of concepts. On a domain of n objects it can hold
    only if the classes are no more than n. Counted here by enumerating every concept:
      Hume's principle:   classes by size                      (n + 1 of them)
      Basic Law V:        classes by identity: every extension  (2^n)
      nuisance principle: classes by finite difference          (1, on a finite domain)"""
    out = []
    for n in range(1, nmax + 1):
        concepts = [frozenset(c) for r in range(n + 1) for c in itertools.combinations(range(n), r)]
        hp = len({len(c) for c in concepts})
        blv = len(set(concepts))
        nuis = 1  # every two concepts on a finite domain differ in finitely many objects
        out.append({"n": n, "HP": hp, "BLV": blv, "NP": nuis})
    return out


def hp_model_on_naturals(limit: int = 6) -> dict:
    """Hume's principle holds on the domain {0, 1, 2, ...}: let #F be 0 if F is infinite, and |F| + 1 if finite.
    Checked on finite concepts up to the limit, plus the infinite ones (which all get 0)."""
    def num(f):
        return 0 if f is None else len(f) + 1
    finite = [frozenset(c) for r in range(limit) for c in itertools.combinations(range(limit), r)]
    ok = all((num(f) == num(g)) == (len(f) == len(g)) for f in finite for g in finite)
    return {"ok": ok, "rule": "#F = 0 if F is infinite, else |F| + 1", "checked": len(finite)}


def frege_ladder(n: int = 4) -> list:
    """Frege's numbers counting themselves: 0 = #[x: x != x], and n + 1 = #[x: x is one of 0, ..., n]."""
    return [{"n": k, "concept": list(range(k))} for k in range(n + 1)]


# ---------------------------------------------------------------------------
# Bombelli: an imaginary detour to a real answer
# ---------------------------------------------------------------------------
def cmul(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def bombelli() -> dict:
    """x^3 = 15x + 4. Cardano: x = cbrt(2 + sqrt(-121)) + cbrt(2 - sqrt(-121)). Bombelli (1572): (2 + i)^3 =
    2 + 11i, so the cube roots are 2 + i and 2 - i, and x = 4."""
    p, q = 15, 4
    disc = Fraction(q, 2) ** 2 - Fraction(p, 3) ** 3
    cube = cmul(cmul((2, 1), (2, 1)), (2, 1))
    cube_bar = cmul(cmul((2, -1), (2, -1)), (2, -1))
    x = (2 + 2, 1 - 1)
    return {"disc": str(disc), "cube": cube, "cube_bar": cube_bar, "x": x[0], "check": x[0] ** 3 == p * x[0] + q,
            "real_roots": sorted(round(r, 6) for r in (4, -2 + math.sqrt(3), -2 - math.sqrt(3)))}


# ---------------------------------------------------------------------------
# The digits of pi (Gibbons's unbounded spigot) and Brouwer's weak counterexamples
# ---------------------------------------------------------------------------
def pi_digits(count: int) -> str:
    q, r, t, k, n, l = 1, 0, 1, 1, 3, 3
    out = []
    while len(out) < count:
        if 4 * q + r - t < n * t:
            out.append(str(n))
            q, r, n = 10 * q, 10 * (r - n * t), (10 * (3 * q + r)) // t - 10 * n
        else:
            q, r, t, k, n, l = q * k, (2 * q + r) * l, t * l, k + 1, (q * (7 * k + 2) + r * l) // (t * l), l + 2
    return "".join(out)


def first_run(digits: str, pattern: str):
    """The decimal place (1 = the first digit after the point) where pattern first begins, or None."""
    i = digits.find(pattern, 1)
    return None if i < 0 else i


def brouwer_real(digits: str, pattern: str, n: int) -> Fraction:
    """Brouwer's real r, to n places: r_n = (-1/2)^k if the pattern first begins at place k <= n, else (-1/2)^n.
    r is positive if k is even, negative if odd, zero if the pattern never occurs; nobody needs to know which to
    compute r to any precision, but to say whether r < 0, r = 0 or r > 0 one must know where the pattern is."""
    k = first_run(digits[: n + len(pattern)], pattern)
    e = k if k is not None and k <= n else n
    return Fraction(-1, 2) ** e


def goldbach_checked(upto: int = 100_000) -> dict:
    """Every even number from 4 to the limit is a sum of two primes (Goldbach's conjecture, checked); the fewest
    ways, and the largest even number with a given smallest prime."""
    sieve = bytearray([1]) * (upto + 1)
    sieve[0] = sieve[1] = 0
    for i in range(2, int(upto ** 0.5) + 1):
        if sieve[i]:
            sieve[i * i::i] = bytearray(len(sieve[i * i::i]))
    worst = (0, 0)
    for n in range(4, upto + 1, 2):
        p = next((p for p in range(2, n // 2 + 1) if sieve[p] and sieve[n - p]), None)
        if p is None:
            return {"upto": upto, "counterexample": n}
        if p > worst[1]:
            worst = (n, p)
    return {"upto": upto, "counterexample": None, "hardest": worst}


# ---------------------------------------------------------------------------
# Predicativity: Russell's typical Englishman
# ---------------------------------------------------------------------------
ENGLISHMEN = {  # seven people, four traits
    "Alfred": {"drinks tea": 1, "likes cricket": 1, "owns a dog": 0, "plays chess": 1},
    "Bertrand": {"drinks tea": 1, "likes cricket": 0, "owns a dog": 1, "plays chess": 1},
    "Charles": {"drinks tea": 1, "likes cricket": 1, "owns a dog": 1, "plays chess": 0},
    "Dora": {"drinks tea": 0, "likes cricket": 1, "owns a dog": 1, "plays chess": 1},
    "Edith": {"drinks tea": 1, "likes cricket": 1, "owns a dog": 1, "plays chess": 1},
    "Frank": {"drinks tea": 1, "likes cricket": 1, "owns a dog": 0, "plays chess": 0},
    "Grace": {"drinks tea": 0, "likes cricket": 0, "owns a dog": 1, "plays chess": 1},
}


def typical(people: dict = ENGLISHMEN, levels: int = 3) -> list:
    """'A typical Englishman has every property that a majority of Englishmen have.' Level 0: the given traits.
    Level k+1 adds 'typical at level k' and its negation. The typical ones at each level, and finally with every
    property whatever (every subset), when nobody is typical: for each x, 'not x' is a majority property."""
    names = list(people)
    props = {t: frozenset(p for p in names if people[p][t]) for t in next(iter(people.values()))}
    props.update({f"not {t}": frozenset(names) - s for t, s in list(props.items())})
    half = len(names) / 2
    out = []
    for lev in range(levels):
        majority = [t for t, s in props.items() if len(s) > half]
        typ = frozenset(p for p in names if all(p in props[t] for t in majority))
        out.append({"level": lev, "majority": majority, "typical": sorted(typ, key=names.index)})
        props[f"typical{lev}"] = typ
        props[f"untypical{lev}"] = frozenset(names) - typ
    every = [frozenset(c) for r in range(len(names) + 1) for c in itertools.combinations(names, r)]
    maj = [s for s in every if len(s) > half]
    out.append({"level": "all", "majority": len(maj), "typical": [p for p in names if all(p in s for s in maj)]})
    return out


# ---------------------------------------------------------------------------
# Structuralism: automorphisms of small structures
# ---------------------------------------------------------------------------
def automorphisms(n: int, relations) -> list:
    """Every permutation of 0..n-1 that maps each relation (a set of tuples) onto itself."""
    rels = [set(map(tuple, r)) for r in relations]
    return [p for p in itertools.permutations(range(n))
            if all({tuple(p[x] for x in t) for t in rel} == rel for rel in rels)]


def fixed_points(autos) -> list:
    """The elements every automorphism fixes: those the structure alone can tell apart from all the rest."""
    n = len(autos[0])
    return [x for x in range(n) if all(p[x] == x for p in autos)]


def roots_of_unity() -> dict:
    """{1, i, -1, -i} as i^0..i^3 under multiplication: i^j * i^k = i^(j+k mod 4). Swapping i and -i preserves it."""
    mult = {(a, b, (a + b) % 4) for a in range(4) for b in range(4)}
    autos = automorphisms(4, [mult])
    return {"autos": autos, "fixed": fixed_points(autos), "names": ["1", "i", "-1", "-i"]}


def edges_rel(edges) -> set:
    return {(a, b) for a, b in edges} | {(b, a) for a, b in edges}


GRAPHS = {
    "two points": (2, []),
    "two points, joined": (2, [(0, 1)]),
    "a path of three": (3, [(0, 1), (1, 2)]),
    "a triangle with a tail": (4, [(0, 1), (1, 2), (2, 0), (2, 3)]),
    "an asymmetric graph": (6, [(0, 1), (1, 2), (2, 3), (3, 4), (2, 4), (4, 5)]),
}


def graph_symmetries() -> dict:
    out = {}
    for name, (n, edges) in GRAPHS.items():
        autos = automorphisms(n, [edges_rel(edges)])
        out[name] = {"n": n, "edges": edges, "autos": len(autos), "fixed": fixed_points(autos),
                     "weakly_discernible": n == 2 and bool(edges)}
    return out


# ---------------------------------------------------------------------------
# Indispensability: prime periods (Baker's cicadas)
# ---------------------------------------------------------------------------
def cicada_overlap(cycle: int, predators=range(2, 10)) -> Fraction:
    """How often, per year, an emergence coincides with a peak of a predator whose period is p: 1 / lcm(cycle, p),
    summed over predator periods."""
    return sum((Fraction(1, math.lcm(cycle, p)) for p in predators), Fraction(0))


def cicadas(lo: int = 10, hi: int = 20) -> list:
    return [{"cycle": c, "overlap": float(cicada_overlap(c)), "prime": all(c % d for d in range(2, c))}
            for c in range(lo, hi + 1)]


# ---------------------------------------------------------------------------
# Field: numbers as representations of a structure of points
# ---------------------------------------------------------------------------
LINE_POINTS = {"a": 0, "b": 1, "c": 2, "d": 4, "e": 5}  # hidden positions on a line


def nominal_facts(pos: dict = LINE_POINTS) -> dict:
    """Only betweenness and congruence of segments: no numbers."""
    names = sorted(pos)
    bet = {(x, y, z) for x, y, z in itertools.permutations(names, 3)
           if min(pos[x], pos[z]) < pos[y] < max(pos[x], pos[z])}
    segs = list(itertools.combinations(names, 2))
    cong = {(s, t) for s in segs for t in segs if s < t and abs(pos[s[0]] - pos[s[1]]) == abs(pos[t[0]] - pos[t[1]])}
    return {"names": names, "bet": bet, "cong": cong, "segs": segs}


def representations(facts: dict, lo: int = -12, hi: int = 12, origin: str = "a") -> list:
    """Every integer coordinate assignment in [lo, hi], with the origin point at 0, that makes exactly the given
    betweenness and congruence facts true. Here every answer is x -> s x for a nonzero s: once a unit and a direction
    are chosen, the numbers are fixed. The representation and uniqueness theorems, in miniature."""
    names = facts["names"]
    rest = [n for n in names if n != origin]
    out = []
    for vals in itertools.product(range(lo, hi + 1), repeat=len(rest)):
        if 0 in vals or len(set(vals)) < len(vals):
            continue
        pos = {origin: 0, **dict(zip(rest, vals))}
        f = nominal_facts(pos)
        if f["bet"] == facts["bet"] and f["cong"] == facts["cong"]:
            out.append(pos)
    return out


# ---------------------------------------------------------------------------
# Lakatos: V - E + F
# ---------------------------------------------------------------------------
def _frame():
    """Lakatos's picture frame: a square ring, each of its four faces (top, bottom, outside, inside) cut in four."""
    o = [(0, 0), (3, 0), (3, 3), (0, 3)]
    i = [(1, 1), (2, 1), (2, 2), (1, 2)]
    v = {}
    for h in (0, 1):
        for k in range(4):
            v[("o", k, h)] = (*o[k], h)
            v[("i", k, h)] = (*i[k], h)
    faces = []
    for k in range(4):
        n = (k + 1) % 4
        for h in (0, 1):
            faces.append([("o", k, h), ("o", n, h), ("i", n, h), ("i", k, h)])
        faces.append([("o", k, 0), ("o", n, 0), ("o", n, 1), ("o", k, 1)])
        faces.append([("i", k, 0), ("i", n, 0), ("i", n, 1), ("i", k, 1)])
    return faces


POLYHEDRA = {
    "tetrahedron": [[0, 1, 2], [0, 1, 3], [0, 2, 3], [1, 2, 3]],
    "cube": [[0, 1, 2, 3], [4, 5, 6, 7], [0, 1, 5, 4], [1, 2, 6, 5], [2, 3, 7, 6], [3, 0, 4, 7]],
    "octahedron": [[0, 2, 4], [0, 4, 3], [0, 3, 5], [0, 5, 2], [1, 2, 4], [1, 4, 3], [1, 3, 5], [1, 5, 2]],
    "twin tetrahedra": [[0, 1, 2], [0, 1, 3], [0, 2, 3], [1, 2, 3], [0, 4, 5], [0, 4, 6], [0, 5, 6], [4, 5, 6]],
    "picture frame": _frame(),
}


def euler(faces) -> dict:
    vs = {v for f in faces for v in f}
    es = {frozenset((f[k], f[(k + 1) % len(f)])) for f in faces for k in range(len(f))}
    return {"V": len(vs), "E": len(es), "F": len(faces), "chi": len(vs) - len(es) + len(faces)}


URCHIN = {"V": 12, "E": 30, "F": 12, "chi": -6}  # Kepler's small stellated dodecahedron, faces read as pentagrams


# ---------------------------------------------------------------------------
# Practice: pictures that prove, and pictures that lie
# ---------------------------------------------------------------------------
def odd_squares(n: int = 6) -> list:
    """1 + 3 + ... + (2k - 1) = k^2: each odd number is an L-shaped layer around the last square."""
    return [(k, sum(2 * j - 1 for j in range(1, k + 1))) for k in range(1, n + 1)]


def gauss_pairs(n: int = 10) -> dict:
    return {"n": n, "sum": sum(range(1, n + 1)), "pairs": n // 2, "pair_sum": n + 1, "formula": n * (n + 1) // 2}


def missing_square() -> dict:
    """Paul Curry's puzzle (1953). Pieces: triangles 8 by 3 and 5 by 2, and two L-shapes of 7 and 8 squares.
    Arranged in a '13 by 5 triangle' (area 32.5), they leave a hole of one square in the second arrangement. The
    slopes 3/8 and 2/5 differ, so neither figure is a triangle: one sags by half a square, the other bulges."""
    s1, s2, big = Fraction(3, 8), Fraction(2, 5), Fraction(5, 13)
    pieces = Fraction(8 * 3, 2) + Fraction(5 * 2, 2) + 7 + 8
    return {"slopes": [str(s1), str(s2), str(big)], "equal": s1 == s2 == big, "pieces": str(pieces),
            "triangle": str(Fraction(13 * 5, 2)), "figure1": str(pieces), "figure2": str(pieces + 1)}


# ---------------------------------------------------------------------------
# What a checked proof shows: a misformalized theorem
# ---------------------------------------------------------------------------
def is_prime(n: int) -> bool:
    return n > 1 and all(n % d for d in range(2, int(n ** 0.5) + 1))


def euclid_statements(upto: int = 30) -> dict:
    """'There are infinitely many primes', stated two ways and checked for n up to the limit. The bad statement,
    'for every n there is a prime', is true with the witness 2 every time: a checker certifies what was written."""
    bad = [(n, 2) for n in range(upto) if is_prime(2)]
    good = [(n, next(p for p in range(n + 1, 2 * n + 3) if is_prime(p))) for n in range(upto)]
    return {"bad": bad, "good": good}
