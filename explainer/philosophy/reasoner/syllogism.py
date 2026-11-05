"""Aristotle's syllogistic, exactly: categorical propositions, the 256 moods, Venn-region models, and Leibniz's
characteristic numbers (1679).

    from explainer.philosophy.reasoner.syllogism import all_moods, valid, leibniz_valid
    [m for m in all_moods() if valid(m)]                       # the 15 Boolean-valid moods
    [m for m in all_moods() if valid(m, existential=True)]     # the 24 traditional ones

A mood is (figure, "XYZ"): X the major premise, Y the minor premise, Z the conclusion, each of A (all), E (no),
I (some), O (some ... not). Terms: S (subject of the conclusion), P (its predicate), M (the middle term).

    figure 1: M-P, S-M |- S-P      figure 2: P-M, S-M |- S-P
    figure 3: M-P, M-S |- S-P      figure 4: P-M, M-S |- S-P

A model says which of the eight regions of the three-circle Venn diagram are inhabited (2^8 = 256 models).
"""

from __future__ import annotations

import itertools
from math import gcd

TERMS = ("S", "M", "P")
FIGURES = {1: (("M", "P"), ("S", "M")), 2: (("P", "M"), ("S", "M")),
           3: (("M", "P"), ("M", "S")), 4: (("P", "M"), ("M", "S"))}
NAMES = {
    (1, "AAA"): "Barbara", (1, "EAE"): "Celarent", (1, "AII"): "Darii", (1, "EIO"): "Ferio",
    (1, "AAI"): "Barbari", (1, "EAO"): "Celaront",
    (2, "EAE"): "Cesare", (2, "AEE"): "Camestres", (2, "EIO"): "Festino", (2, "AOO"): "Baroco",
    (2, "EAO"): "Cesaro", (2, "AEO"): "Camestros",
    (3, "AAI"): "Darapti", (3, "IAI"): "Disamis", (3, "AII"): "Datisi", (3, "EAO"): "Felapton",
    (3, "OAO"): "Bocardo", (3, "EIO"): "Ferison",
    (4, "AAI"): "Bramantip", (4, "AEE"): "Camenes", (4, "IAI"): "Dimaris", (4, "EAO"): "Fesapo",
    (4, "EIO"): "Fresison", (4, "AEO"): "Camenos",
}
REGIONS = list(itertools.product((True, False), repeat=3))  # membership in (S, M, P)


def all_moods():
    return [(f, "".join(t)) for f in (1, 2, 3, 4) for t in itertools.product("AEIO", repeat=3)]


def holds(kind: str, x: str, y: str, model) -> bool:
    """``model``: the set of inhabited regions (tuples of membership in S, M, P)."""
    ix, iy = TERMS.index(x), TERMS.index(y)
    xy = any(r[ix] and r[iy] for r in model)
    x_not_y = any(r[ix] and not r[iy] for r in model)
    return {"A": not x_not_y, "E": not xy, "I": xy, "O": x_not_y}[kind]


def models(existential: bool = False):
    for bits in itertools.product((False, True), repeat=8):
        m = frozenset(r for r, b in zip(REGIONS, bits) if b)
        if existential and not all(any(r[i] for r in m) for i in range(3)):
            continue
        yield m


def premises(mood):
    f, k = mood
    (a1, b1), (a2, b2) = FIGURES[f]
    return [(k[0], a1, b1), (k[1], a2, b2)], (k[2], "S", "P")


def countermodel(mood, existential: bool = False):
    prem, concl = premises(mood)
    for m in models(existential):
        if all(holds(k, x, y, m) for k, x, y in prem) and not holds(*concl, m):
            return m
    return None


def valid(mood, existential: bool = False) -> bool:
    return countermodel(mood, existential) is None


# ---------------------------------------------------------------------------
# Leibniz, "Elementa calculi" and the characteristic numbers (April 1679)
# ---------------------------------------------------------------------------
def leibniz_holds(kind: str, x, y) -> bool:
    """Each term is a pair (+, -) of coprime positive integers. Leibniz's rules (as reconstructed by Łukasiewicz
    1951): All x is y iff +y divides +x and -y divides -x; No x is y iff +x and -y, or -x and +y, share a factor;
    Some x is y iff not 'no'; some x is not y iff not 'all'."""
    (xp, xm), (yp, ym) = x, y
    a = xp % yp == 0 and xm % ym == 0
    e = gcd(xp, ym) > 1 or gcd(xm, yp) > 1
    return {"A": a, "E": e, "I": not e, "O": not a}[kind]


def leibniz_pairs(primes=(2, 3, 5)):
    """Every term number built from distinct ``primes``: each prime goes to +, to -, or to neither."""
    out = []
    for assign in itertools.product((0, 1, 2), repeat=len(primes)):
        p = m = 1
        for q, a in zip(primes, assign):
            if a == 1:
                p *= q
            elif a == 2:
                m *= q
        out.append((p, m))
    return out


def leibniz_countermodel(mood, primes=(2, 3, 5)):
    prem, concl = premises(mood)
    pairs = leibniz_pairs(primes)
    for s, mm, p in itertools.product(pairs, repeat=3):
        val = {"S": s, "M": mm, "P": p}
        if all(leibniz_holds(k, val[x], val[y]) for k, x, y in prem) and not leibniz_holds(concl[0], val["S"], val["P"]):
            return val
    return None


def describe(kind: str, x: str, y: str, names=None) -> str:
    n = names or {"S": "S", "M": "M", "P": "P"}
    return {"A": f"All {n[x]} are {n[y]}", "E": f"No {n[x]} are {n[y]}", "I": f"Some {n[x]} are {n[y]}",
            "O": f"Some {n[x]} are not {n[y]}"}[kind]
