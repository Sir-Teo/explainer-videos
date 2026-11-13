"""Sets and the infinite, exactly: hereditarily finite sets, Cantor's theorem, ordinals below ε₀, Goodstein's
sequences, and the free group behind Banach–Tarski.

    from explainer.philosophy.reasoner.sets import ackermann_decode, Ord, goodstein
    ackermann_decode(11)                    # {∅, {∅}, {{{∅}}}}... the set whose code is 11
    Ord.parse("w^2 + w*3 + 1") < Ord.omega_tower(3)
    goodstein(4, 6)                         # the first terms of Goodstein's sequence from 4

Hereditarily finite sets are frozensets of frozensets; Ackermann's bijection (1937) reads n in binary and takes the
set of the sets coded by its 1-bits. Ordinals below ε₀ are kept in Cantor normal form, ω^{a₁}·c₁ + ... + ω^{aₖ}·cₖ
with a₁ > ... > aₖ, the exponents themselves ordinals in normal form: so comparison, addition and multiplication are
exact. Everything is small enough to check by brute force; ``tests/philosophy/test_sets.py`` does.
"""

from __future__ import annotations

import itertools
from dataclasses import dataclass
from functools import lru_cache, total_ordering

EMPTY = frozenset()


# ---------------------------------------------------------------------------
# Hereditarily finite sets
# ---------------------------------------------------------------------------
@lru_cache(maxsize=None)
def ackermann_decode(n: int) -> frozenset:
    """The HF set with Ackermann code n: {decode(i) : the i-th bit of n is 1}."""
    return frozenset(ackermann_decode(i) for i in range(n.bit_length()) if n >> i & 1)


def ackermann_code(s: frozenset) -> int:
    return sum(1 << ackermann_code(x) for x in s)


def show_set(s: frozenset, tex: bool = False) -> str:
    """Braces all the way down, members in code order; ∅ for the empty set."""
    if not s:
        return r"\varnothing" if tex else "∅"
    inner = ", ".join(show_set(x, tex) for x in sorted(s, key=ackermann_code))
    return (r"\{" + inner + r"\}") if tex else "{" + inner + "}"


def rank(s: frozenset) -> int:
    """The least α with s ⊆ V_α: one more than the largest rank of a member."""
    return 1 + max((rank(x) for x in s), default=-1) if s else 0


def power(s: frozenset) -> frozenset:
    xs = list(s)
    return frozenset(frozenset(c) for r in range(len(xs) + 1) for c in itertools.combinations(xs, r))


def V(n: int) -> frozenset:
    """The cumulative hierarchy, finite stages: V_0 = ∅, V_{k+1} = 𝒫(V_k)."""
    v = EMPTY
    for _ in range(n):
        v = power(v)
    return v


def V_size(n: int) -> int:
    """|V_n| = 2 ↑↑ (n-1): 0, 1, 2, 4, 16, 65536, ..."""
    k = 0
    for _ in range(n):
        k = 2 ** k
    return k


def von_neumann(n: int) -> frozenset:
    """The finite ordinal n = {0, 1, ..., n-1}."""
    s = EMPTY
    for _ in range(n):
        s = s | {s}
    return s


def transitive(s: frozenset) -> bool:
    return all(x <= s for x in s)


# ---------------------------------------------------------------------------
# Cantor
# ---------------------------------------------------------------------------
def diagonal(rows):
    """Flip the diagonal of a table of 0/1 rows: the result differs from row i at place i."""
    return [1 - rows[i][i] for i in range(len(rows))]


def cantor_check(n: int) -> dict:
    """Every function f from an n-element set X to its power set misses D = {x ∈ X : x ∉ f(x)}. Checked for every
    one of the (2^n)^n functions."""
    X = list(range(n))
    subsets = [frozenset(c) for r in range(n + 1) for c in itertools.combinations(X, r)]
    count, missed = 0, 0
    for images in itertools.product(subsets, repeat=n):
        D = frozenset(x for x in X if x not in images[x])
        missed += D not in images
        count += 1
    return {"n": n, "functions": count, "subsets": len(subsets), "all_miss": missed == count}


def cantor_pair(x: int, y: int) -> int:
    """Cantor's pairing ℕ × ℕ → ℕ, along the diagonals: a bijection."""
    return (x + y) * (x + y + 1) // 2 + y


def cantor_unpair(z: int) -> tuple[int, int]:
    w = int(((8 * z + 1) ** 0.5 - 1) // 2)
    while (w + 1) * (w + 2) // 2 <= z:
        w += 1
    while w * (w + 1) // 2 > z:
        w -= 1
    y = z - w * (w + 1) // 2
    return w - y, y


def calkin_wilf(n: int) -> list[tuple[int, int]]:
    """The first n positive rationals in the Calkin–Wilf order (Newman's formula): each exactly once, in lowest
    terms."""
    out = []
    a, b = 1, 1
    for _ in range(n):
        out.append((a, b))
        # next = 1 / (2⌊q⌋ − q + 1)
        fl = a // b
        a, b = b, (2 * fl + 1) * b - a
    return out


# ---------------------------------------------------------------------------
# Ordinals below ε₀, in Cantor normal form
# ---------------------------------------------------------------------------
@total_ordering
@dataclass(frozen=True)
class Ord:
    """ω^{e₁}·c₁ + ... + ω^{eₖ}·cₖ with e₁ > ... > eₖ (each eᵢ an Ord) and cᵢ ≥ 1. Zero is the empty sum."""
    terms: tuple = ()

    @staticmethod
    def nat(n: int) -> "Ord":
        return Ord(((ZERO, n),)) if n else ZERO

    @staticmethod
    def omega_power(e: "Ord", c: int = 1) -> "Ord":
        return Ord(((e, c),))

    @staticmethod
    def omega_tower(k: int) -> "Ord":
        """ω^ω^...^ω with k omegas (k = 0 gives 1)."""
        o = Ord.nat(1)
        for _ in range(k):
            o = Ord.omega_power(o)
        return o

    def __lt__(self, other: "Ord") -> bool:
        for (e1, c1), (e2, c2) in zip(self.terms, other.terms):
            if e1 != e2:
                return e1 < e2
            if c1 != c2:
                return c1 < c2
        return len(self.terms) < len(other.terms)

    def is_zero(self) -> bool:
        return not self.terms

    def is_finite(self) -> bool:
        return all(e.is_zero() for e, _ in self.terms)

    def __add__(self, other: "Ord") -> "Ord":
        if other.is_zero():
            return self
        e0 = other.terms[0][0]
        keep = [t for t in self.terms if not t[0] < e0]
        if keep and keep[-1][0] == e0:
            keep[-1] = (e0, keep[-1][1] + other.terms[0][1])
            return Ord(tuple(keep) + other.terms[1:])
        return Ord(tuple(keep) + other.terms)

    def __mul__(self, other: "Ord") -> "Ord":
        if self.is_zero() or other.is_zero():
            return ZERO
        out = ZERO
        e1, c1 = self.terms[0]
        for e, c in other.terms:
            if e.is_zero():
                # (α)·c: the leading coefficient multiplies, the rest stays
                out = out + Ord(((e1, c1 * c),) + self.terms[1:])
            else:
                out = out + Ord(((e1 + e, c),))
        return out

    def tex(self) -> str:
        if self.is_zero():
            return "0"
        parts = []
        for e, c in self.terms:
            if e.is_zero():
                parts.append(str(c))
                continue
            base = r"\omega" if e == ONE else r"\omega^{" + e.tex() + "}"
            parts.append(base + (rf"\cdot {c}" if c > 1 else ""))
        return " + ".join(parts)

    def __repr__(self) -> str:
        return self.tex().replace(r"\omega", "w").replace(r"\cdot", "*").replace("{", "(").replace("}", ")")


ZERO = Ord(())
ONE = Ord(((ZERO, 1),))
OMEGA = Ord(((ONE, 1),))


# ---------------------------------------------------------------------------
# Goodstein's sequences (Goodstein 1944; Kirby and Paris 1982)
# ---------------------------------------------------------------------------
def hereditary(n: int, b: int) -> list:
    """n in hereditary base b: a list of (exponent-in-hereditary-base-b, coefficient), highest first."""
    out = []
    e = 0
    terms = []
    while n:
        n, d = divmod(n, b)
        if d:
            terms.append((e, d))
        e += 1
    for e, d in reversed(terms):
        out.append((hereditary(e, b), d))
    return out


def evaluate_hereditary(h: list, b: int) -> int:
    return sum(d * b ** evaluate_hereditary(e, b) for e, d in h)


def to_ordinal(h: list) -> Ord:
    """Replace the base by ω everywhere: the ordinal that Goodstein's proof attaches to a term."""
    o = ZERO
    for e, d in h:
        o = o + Ord.omega_power(to_ordinal(e), d)
    return o


def hereditary_tex(h: list, b: int) -> str:
    if not h:
        return "0"
    parts = []
    for e, d in h:
        if not e:
            parts.append(str(d))
            continue
        et = hereditary_tex(e, b)
        p = str(b) if et == "1" else f"{b}^{{{et}}}"
        parts.append((f"{d} \\cdot " if d > 1 else "") + p)
    return " + ".join(parts)


def goodstein(n: int, steps: int, cap: int = 10 ** 60) -> list[dict]:
    """Start at n in base 2. Each step: write the term in hereditary base b, replace b by b + 1 everywhere, subtract
    one. Records each term, its base, its hereditary form, and its ordinal (which strictly decreases)."""
    out = []
    b, m = 2, n
    for _ in range(steps):
        h = hereditary(m, b)
        out.append({"base": b, "value": m, "tex": hereditary_tex(h, b), "ordinal": to_ordinal(h)})
        if m == 0:
            break
        bumped = evaluate_hereditary(h, b + 1)
        m, b = bumped - 1, b + 1
        if m > cap:
            out.append({"base": b, "value": None, "tex": None, "ordinal": to_ordinal(hereditary(m, b))})
            break
    return out


# ---------------------------------------------------------------------------
# The free group on two generators (the heart of Banach–Tarski)
# ---------------------------------------------------------------------------
INV = {"a": "A", "A": "a", "b": "B", "B": "b"}   # A = a⁻¹, B = b⁻¹


def reduce_word(w: str) -> str:
    out = []
    for ch in w:
        if out and out[-1] == INV[ch]:
            out.pop()
        else:
            out.append(ch)
    return "".join(out)


def words(n: int) -> list[str]:
    """All reduced words of length at most n."""
    out = [""]
    frontier = [""]
    for _ in range(n):
        new = []
        for w in frontier:
            for ch in "aAbB":
                if not w or w[-1] != INV[ch]:
                    new.append(w + ch)
        out += new
        frontier = new
    return out


def paradoxical_check(n: int) -> dict:
    """F₂ = W(a) ∪ a·W(a⁻¹), and also F₂ = W(b) ∪ b·W(b⁻¹), where W(x) is the set of reduced words starting with x.
    So the four pieces W(a), W(a⁻¹), W(b), W(b⁻¹) (and {e}) split F₂ into two copies of itself. Checked on every word
    up to length n: w is in W(a), or a⁻¹w is in W(a⁻¹)."""
    ws = words(n)
    ok_a = all(w.startswith("a") or reduce_word("A" + w).startswith("A") for w in ws)
    ok_b = all(w.startswith("b") or reduce_word("B" + w).startswith("B") for w in ws)
    counts = {x: sum(1 for w in ws if w.startswith(x)) for x in "aAbB"}
    return {"n": n, "words": len(ws), "W(a) + aW(A)": ok_a, "W(b) + bW(B)": ok_b, "counts": counts}


# ---------------------------------------------------------------------------
# Forcing, as a picture: a generic path through the tree of finite conditions
# ---------------------------------------------------------------------------
def generic_real(ground: list[list[int]], length: int) -> dict:
    """Conditions are finite 0/1 strings; a real extends them. For each ground real r_k, the set D_k of conditions
    that disagree with r_k somewhere is dense: any condition can be extended into it. Meeting D_0, D_1, ... in turn
    builds a real that differs from every ground real: Cohen's idea, in Cantor's diagonal form."""
    c: list[int] = []
    met = []
    for k, r in enumerate(ground):
        if any(c[i] != r[i] for i in range(min(len(c), len(r)))):
            met.append(len(c))
            continue
        c = c + [1 - r[len(c)]]
        met.append(len(c))
    while len(c) < length:
        c.append(0)
    return {"generic": c, "met_at": met,
            "differs": all(any(c[i] != r[i] for i in range(min(len(c), len(r)))) for r in ground)}


# ---------------------------------------------------------------------------
# Coding mathematics in sets
# ---------------------------------------------------------------------------
def kuratowski(a: frozenset, b: frozenset) -> frozenset:
    """The ordered pair (a, b) = {{a}, {a, b}} (Kuratowski 1921)."""
    return frozenset({frozenset({a}), frozenset({a, b})})


def kuratowski_check(n: int = 16) -> dict:
    """(a, b) = (c, d) iff a = c and b = d, checked on every pair of the first n HF sets."""
    xs = [ackermann_decode(i) for i in range(n)]
    pairs = {}
    ok = True
    for a in xs:
        for b in xs:
            k = kuratowski(a, b)
            if k in pairs and pairs[k] != (a, b):
                ok = False
            pairs[k] = (a, b)
    return {"n": n, "pairs": len(pairs), "ok": ok and len(pairs) == n * n}


def zermelo_numeral(n: int) -> frozenset:
    """Zermelo's numerals (1908): 0 = ∅, n + 1 = {n}."""
    s = EMPTY
    for _ in range(n):
        s = frozenset({s})
    return s


# ---------------------------------------------------------------------------
# Zermelo (1913): every finite game of perfect information is determined
# ---------------------------------------------------------------------------
TTT_LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]


def _ttt_winner(b: str):
    for i, j, k in TTT_LINES:
        if b[i] != "." and b[i] == b[j] == b[k]:
            return b[i]
    return None


def tictactoe() -> dict:
    """Backward induction over every position of noughts and crosses reachable from the empty board: the value with
    best play (1 = X wins, 0 = draw, -1 = O wins), and the number of positions."""
    memo: dict[str, int] = {}

    def value(b: str) -> int:
        if b in memo:
            return memo[b]
        w = _ttt_winner(b)
        if w:
            v = 1 if w == "X" else -1
        elif "." not in b:
            v = 0
        else:
            turn = "X" if b.count("X") == b.count("O") else "O"
            vals = [value(b[:i] + turn + b[i + 1:]) for i in range(9) if b[i] == "."]
            v = max(vals) if turn == "X" else min(vals)
        memo[b] = v
        return v

    v = value("." * 9)
    return {"value": v, "positions": len(memo), "x_wins": sum(1 for x in memo.values() if x == 1),
            "o_wins": sum(1 for x in memo.values() if x == -1)}


# ---------------------------------------------------------------------------
# Hercules and the hydra (Kirby and Paris 1982)
# ---------------------------------------------------------------------------
def natural_sum(ords) -> Ord:
    """The Hessenberg natural sum: merge the Cantor normal forms, largest exponent first (commutative)."""
    terms: dict = {}
    for o in ords:
        for e, c in o.terms:
            terms[e] = terms.get(e, 0) + c
    return Ord(tuple(sorted(terms.items(), key=lambda t: t[0], reverse=True)))


def hydra_ordinal(t: tuple) -> Ord:
    """A hydra is a tree of nested tuples (a head is the empty tuple). Its ordinal: a head is 0; a node is the
    natural sum of ω^(ordinal of each child)."""
    return natural_sum([Ord.omega_power(hydra_ordinal(c)) for c in t]) if t else ZERO


def hydra_size(t: tuple) -> int:
    return 1 + sum(hydra_size(c) for c in t)


def _chop(t: tuple, n: int):
    """Chop the rightmost head of hydra t at step n (Kirby–Paris rule). Returns the new hydra."""
    # find the path to the rightmost leaf
    path = []
    node = t
    while node:
        path.append(len(node) - 1)
        node = node[-1]
    if len(path) == 1:                       # the head grows from the root: just remove it
        return t[:-1]

    def rebuild(tree, depth):
        i = path[depth]
        if depth == len(path) - 2:           # tree is the grandparent; tree[i] is the parent of the head
            parent = tree[i][:-1]            # remove the head
            return tree[:i] + (parent,) + (parent,) * n + tree[i + 1:]
        return tree[:i] + (rebuild(tree[i], depth + 1),) + tree[i + 1:]
    return rebuild(t, 0)


def hydra_battle(t: tuple, max_steps: int = 10 ** 6, record: int = 12) -> dict:
    """Hercules always chops the rightmost head; at step n the hydra regrows n copies. Returns the number of steps
    until the hydra dies (or None if it outlives max_steps), the first few hydras with their sizes and ordinals, and
    the peak size."""
    hist = []
    n = 0
    peak = hydra_size(t)
    while t:
        n += 1
        if len(hist) < record:
            hist.append({"step": n - 1, "size": hydra_size(t), "ordinal": hydra_ordinal(t), "tree": t})
        prev = hydra_ordinal(t)
        t = _chop(t, n)
        assert hydra_ordinal(t) < prev
        peak = max(peak, hydra_size(t))
        if n >= max_steps:
            return {"steps": None, "history": hist, "peak": peak}
    return {"steps": n, "history": hist, "peak": peak}


def hydra2_steps(k: int, cap: int = 10 ** 400) -> int | None:
    """The battle against the simplest growing hydra, a neck with k heads (ordinal ω^k), counted without drawing
    it: the root's children are kept as runs of necks with m heads (m = 0 is a bare head). Returns the number of
    steps, or None if it exceeds cap."""
    stack = [[k, 1]]
    n = 0
    while stack:
        m, c = stack[-1]
        if m == 0:                            # c bare heads: c steps
            n += c
            stack.pop()
        else:                                 # chop one head of the rightmost neck: n+1 necks with m-1 heads
            n += 1
            if c == 1:
                stack.pop()
            else:
                stack[-1][1] -= 1
            if stack and stack[-1][0] == m - 1:
                stack[-1][1] += n + 1
            else:
                stack.append([m - 1, n + 1])
        if n > cap:
            return None
    return n
