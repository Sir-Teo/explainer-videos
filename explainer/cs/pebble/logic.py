"""Two-level logic minimization: Quine–McCluskey with don't-cares, and sums of products built as gates.

Part 3 introduced the method on screen; Part 5 used it for state machines; Part 6 uses it for Pebble's control
unit, where the unused opcodes are the don't-cares.

    terms = min_cover(on={1, 3, 5}, dc={7}, n=3)      # [(value, mask)], mask bits = variables eliminated
    wire = sop(circuit, terms, variables)
"""

from __future__ import annotations

import itertools

from .hdl import Circuit


def prime_implicants(on: set[int], dc: set[int], n: int) -> set[tuple[int, int]]:
    """Merge terms that differ in one variable, round after round; the terms never merged are the primes."""
    terms = {(m, 0) for m in on | dc}
    primes = set()
    while terms:
        nxt, used = set(), set()
        by_mask: dict[int, list] = {}
        for t in terms:
            by_mask.setdefault(t[1], []).append(t)
        for group in by_mask.values():
            for (v1, m1), (v2, m2) in itertools.combinations(sorted(group), 2):
                if bin(v1 ^ v2).count("1") == 1:
                    nxt.add((v1 & v2, m1 | (v1 ^ v2)))
                    used.add((v1, m1))
                    used.add((v2, m2))
        primes |= terms - used
        terms = nxt
    return primes


def covers(t: tuple[int, int], m: int) -> bool:
    v, mask = t
    return (m & ~mask) == (v & ~mask)


def min_cover(on: set[int], dc: set[int], n: int) -> list[tuple[int, int]]:
    """A small sum of products: essential primes first, then greedily the prime that covers the most remaining
    minterms (ties: the one with fewer literals)."""
    if not on:
        return []
    primes = sorted(prime_implicants(set(on), set(dc), n), key=lambda t: (-bin(t[1]).count("1"), t))
    left, chosen = set(on), []
    while left:
        ess = [p for p in primes if any(sum(covers(q, m) for q in primes) == 1 and covers(p, m) for m in left)]
        pick = ess[0] if ess else max(primes, key=lambda p: (sum(covers(p, m) for m in left), bin(p[1]).count("1")))
        chosen.append(pick)
        left = {m for m in left if not covers(pick, m)}
    return chosen


def literals(terms: list[tuple[int, int]], n: int) -> int:
    return sum(n - bin(mask).count("1") for _, mask in terms)


class Literals:
    """Each variable and its complement, made once and shared by every product term."""

    def __init__(self, c: Circuit, variables: list[int]):
        self.c, self.var, self.neg = c, variables, {}

    def __call__(self, i: int, val: int) -> int:
        if val:
            return self.var[i]
        if i not in self.neg:
            self.neg[i] = self.c.not_(self.var[i])
        return self.neg[i]


def sop(c: Circuit, terms: list[tuple[int, int]], lits: Literals, products: dict | None = None) -> int:
    """The sum of products as AND and OR trees.  ``products`` shares identical product terms between outputs (as a
    PLA's AND plane does)."""
    from .blocks import tree

    n = len(lits.var)
    if not terms:
        return c.const(0)
    outs = []
    for v, mask in terms:
        key = (v & ~mask, mask)
        if products is not None and key in products:
            outs.append(products[key])
            continue
        ls = [lits(i, (v >> i) & 1) for i in range(n) if not (mask >> i) & 1]
        t = tree(c, c.and_, ls) if ls else c.const(1)
        if products is not None:
            products[key] = t
        outs.append(t)
    return tree(c, c.or_, outs)
