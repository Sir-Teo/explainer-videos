"""Transformations (Part 31): the twenty-four triads, the T/I group and the PLR group acting on them, their duality,
shortest paths, cycles, the Tonnetz, and voice-leading distance.

A triad is (root, quality) with quality "M" or "m"; as a set of pitch classes, C major is {0, 4, 7}.  P (parallel) swaps
C major and C minor; R (relative) C major and A minor; L (leading-tone exchange) C major and E minor.  Each is an
involution that keeps two notes and moves one, by a semitone (L, P) or a whole tone (R).  No manim.
"""

from __future__ import annotations

from collections import deque
from itertools import product

TRIADS = [(r, q) for q in ("M", "m") for r in range(12)]
NAMES = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]


def pcs(t) -> frozenset:
    r, q = t
    return frozenset({r % 12, (r + (4 if q == "M" else 3)) % 12, (r + 7) % 12})


def name(t) -> str:
    r, q = t
    return NAMES[r] + ("" if q == "M" else "m")


def from_set(s) -> tuple:
    s = frozenset(x % 12 for x in s)
    return next(t for t in TRIADS if pcs(t) == s)


def P(t):
    r, q = t
    return (r, "m" if q == "M" else "M")


def R(t):
    r, q = t
    return ((r + 9) % 12, "m") if q == "M" else ((r + 3) % 12, "M")


def L(t):
    r, q = t
    return ((r + 4) % 12, "m") if q == "M" else ((r + 8) % 12, "M")


OPS = {"P": P, "L": L, "R": R}


def T(n):
    return lambda t: from_set({x + n for x in pcs(t)})


def I(n):
    return lambda t: from_set({n - x for x in pcs(t)})


def as_perm(f) -> tuple:
    return tuple(TRIADS.index(f(t)) for t in TRIADS)


def compose(a: tuple, b: tuple) -> tuple:
    """a after b, as permutations of the 24 triad indices."""
    return tuple(a[b[i]] for i in range(len(b)))


def closure(gens) -> set:
    ident = tuple(range(24))
    group = {ident}
    frontier = [ident]
    while frontier:
        nxt = []
        for g in frontier:
            for h in gens:
                k = compose(h, g)
                if k not in group:
                    group.add(k)
                    nxt.append(k)
        frontier = nxt
    return group


def plr_group() -> set:
    return closure([as_perm(P), as_perm(L), as_perm(R)])


def ti_group() -> set:
    return closure([as_perm(T(1)), as_perm(I(0))])


def commute(G, H) -> bool:
    return all(compose(g, h) == compose(h, g) for g in G for h in H)


def is_simply_transitive(G) -> bool:
    """Each triad reaches every triad by exactly one element of the group."""
    for i in range(24):
        images = [g[i] for g in G]
        if sorted(images) != list(range(24)):
            return False
    return True


def shortest_paths(start=(0, "M"), ops=("P", "L", "R")) -> dict:
    """Breadth-first search: the shortest word in P, L and R from ``start`` to every triad."""
    dist = {start: ""}
    q = deque([start])
    while q:
        t = q.popleft()
        for k in ops:
            u = OPS[k](t)
            if u not in dist:
                dist[u] = dist[t] + k
                q.append(u)
    return dist


def apply(word: str, t):
    """Apply a word of operations left to right (the musicians' convention: 'LP' means L, then P)."""
    for k in word:
        t = OPS[k](t)
    return t


def cycle(word: str, start=(0, "M")) -> list:
    """The chain of triads made by repeating ``word``'s operations one at a time until it returns to ``start``."""
    out = [start]
    t = start
    i = 0
    while True:
        t = OPS[word[i % len(word)]](t)
        i += 1
        if t == start and i % len(word) == 0:
            return out
        out.append(t)


def voice_leading(a, b) -> int:
    """The smallest total number of semitones the three voices move from triad a to triad b."""
    A, B = sorted(pcs(a)), sorted(pcs(b))
    best = 99
    for perm in ((0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0)):
        d = sum(min((B[perm[i]] - A[i]) % 12, (A[i] - B[perm[i]]) % 12) for i in range(3))
        best = min(best, d)
    return best


def common_tones(a, b) -> int:
    return len(pcs(a) & pcs(b))


def tonnetz_xy(pc: int) -> tuple:
    """A pitch class's place on the Tonnetz: fifths to the right, major thirds up (coordinates mod the torus)."""
    for x, y in product(range(12), range(3)):
        if (7 * x + 4 * y) % 12 == pc and x < 4:
            return x, y
    raise ValueError(pc)


def name_move(a, b, max_len: int = 4) -> str:
    """The shortest PLR word taking triad a to b."""
    best = shortest_paths(a)
    return best[b]


def harmonize(melody_pcs, start=(0, "M"), end=None) -> list:
    """A walk on the Tonnetz that fits a melody: at each step stay, or take one or two P, L or R steps, to a triad
    containing the melody note; prefer staying, then single steps, then the fewest semitones of voice-leading; dynamic
    programming over all triads."""
    INF = 10 ** 9
    steps = {s: shortest_paths(s) for s in TRIADS}
    cost = {t: (0 if (t == start and melody_pcs[0] in pcs(t)) else INF) for t in TRIADS}
    if all(v == INF for v in cost.values()):
        cost = {t: (0 if melody_pcs[0] in pcs(t) else INF) for t in TRIADS}
    back = []
    for m in melody_pcs[1:]:
        new, ptr = {}, {}
        for t in TRIADS:
            if m not in pcs(t):
                new[t] = INF
                continue
            best, arg = INF, None
            for s in TRIADS:
                if cost[s] >= INF:
                    continue
                k = len(steps[s][t])
                if k > 2:
                    continue
                c = 0 if k == 0 else 3 * k + voice_leading(s, t)
                if cost[s] + c < best:
                    best, arg = cost[s] + c, s
            new[t], ptr[t] = best, arg
        back.append(ptr)
        cost = new
    t = end if (end is not None and cost.get(end, INF) < INF) else min(cost, key=cost.get)
    path = [t]
    for ptr in reversed(back):
        t = ptr[t]
        path.append(t)
    return path[::-1]


def distance_histogram(start=(0, "M")) -> dict:
    """How many triads lie at each PLR distance from ``start`` (the Tonnetz's spheres)."""
    c: dict = {}
    for w in shortest_paths(start).values():
        c[len(w)] = c.get(len(w), 0) + 1
    return dict(sorted(c.items()))


def systems(word: str) -> list:
    """The orbits of the cycle generated by ``word``: four hexatonic systems for 'PL', three octatonic for 'PR'."""
    seen, out = set(), []
    for t in TRIADS:
        if t in seen:
            continue
        orb = cycle(word, t)
        out.append(orb)
        seen.update(orb)
    return out


def hamiltonian_cycles(ops=("P", "L", "R")) -> int:
    """The number of Hamiltonian cycles of the PLR graph (each cycle counted once, whatever its start or direction)."""
    start = TRIADS[0]
    n = len(TRIADS)
    count = 0
    path = [start]
    seen = {start}

    def nb(t):
        return [OPS[k](t) for k in ops]

    def go(t):
        nonlocal count
        if len(path) == n:
            if start in nb(t):
                count += 1
            return
        for u in nb(t):
            if u not in seen:
                seen.add(u)
                path.append(u)
                go(u)
                path.pop()
                seen.discard(u)

    go(start)
    return count // 2


def order(word: str) -> int:
    """The order of the group element ``word`` (applied left to right): the least k with word^k the identity."""
    k = 1
    while True:
        if all(apply(word * k, t) == t for t in TRIADS):
            return k
        k += 1


def weitzmann(aug_root: int) -> list:
    """Weitzmann's region: the six triads one semitone from an augmented triad (three major, three minor)."""
    aug = {aug_root % 12, (aug_root + 4) % 12, (aug_root + 8) % 12}
    out = []
    for t in TRIADS:
        s = pcs(t)
        if len(s & aug) == 2:
            out.append(t)
    return out


# ------------------------------------------------------------------------------------------------ seventh chords
def seventh(kind: str, root: int) -> frozenset:
    """A dominant seventh ('7': root, major third, fifth, minor seventh) or half-diminished seventh ('o': root, minor
    third, diminished fifth, minor seventh)."""
    iv = (0, 4, 7, 10) if kind == "7" else (0, 3, 6, 10)
    return frozenset((root + i) % 12 for i in iv)


SEVENTHS = [(k, r) for k in ("7", "o") for r in range(12)]


def voice_leading4(a: frozenset, b: frozenset) -> int:
    """The smallest total semitones four voices move from chord a to chord b."""
    from itertools import permutations
    A, B = sorted(a), sorted(b)
    return min(sum(min((B[p[i]] - A[i]) % 12, (A[i] - B[p[i]]) % 12) for i in range(4)) for p in permutations(range(4)))


def seventh_neighbours(src=("7", 0)) -> list:
    """The dominant and half-diminished sevenths within two semitones of voice leading of ``src``: (chord, semitones,
    common tones)."""
    a = seventh(*src)
    out = []
    for c in SEVENTHS:
        if c == src:
            continue
        d = voice_leading4(a, seventh(*c))
        if d <= 2:
            out.append((c, d, len(a & seventh(*c))))
    return out
