"""The early moderns and Kant, made computable (Part 10).

    from explainer.philosophy.reasoner import modern as Mo
    g = Mo.ethics_graph()              # Spinoza, Ethics I: 8 definitions, 7 axioms, 36 propositions, and who cites whom
    Mo.longest_chain(g)                # the deepest line of argument, from a definition to a proposition
    Mo.unused(g)                       # axioms and definitions no demonstration cites
    Mo.continued_fraction(Fraction(355, 113)), Mo.sqrt_cf(2, 12)   # Leibniz: finite and infinite analysis
    Mo.descartes_normal()              # the method of normals, La Géométrie (1637)
    Mo.spherical_excess(...)           # Gauss's triangle, and why it could not test Kant

The citations of Ethics I are those printed in R. H. M. Elwes's English translation (1883), read off its
demonstrations (corollaries and scholia excluded) by `parse_ethics` below, with the few citations made in words
("the third axiom", "the last Prop.", "the preceding one") resolved. One citation the Latin makes and Elwes drops is
kept apart: Proposition 11's first demonstration cites Axiom 7.
"""

from __future__ import annotations

import math
import re
from fractions import Fraction

# ---------------------------------------------------------------------------
# Spinoza, Ethics I
# ---------------------------------------------------------------------------
DEFINITIONS = {
    1: "self-caused", 2: "finite after its kind", 3: "substance", 4: "attribute", 5: "mode", 6: "God",
    7: "free; necessary", 8: "eternity",
}
AXIOMS = {
    1: "everything is in itself or in another", 2: "what is not conceived through another is conceived through itself",
    3: "a determinate cause necessitates its effect", 4: "knowing an effect involves knowing its cause",
    5: "what has nothing in common cannot be understood through the other", 6: "a true idea agrees with its object",
    7: "if a thing can be conceived as not existing, its essence does not involve existence",
}
PROPOSITIONS = {
    1: "substance is prior to its modifications", 2: "substances with different attributes share nothing",
    3: "what shares nothing cannot cause the other", 4: "things differ by attributes or by modifications",
    5: "no two substances share an attribute", 6: "no substance produces another",
    7: "existence belongs to the nature of substance", 8: "every substance is infinite",
    9: "more reality, more attributes", 10: "each attribute is conceived through itself",
    11: "God necessarily exists", 12: "no attribute implies that substance is divisible",
    13: "absolutely infinite substance is indivisible", 14: "besides God, no substance",
    15: "whatever is, is in God", 16: "infinitely many things follow from God's nature",
    17: "God acts from the laws of his nature alone", 18: "God is the immanent cause of all things",
    19: "God and his attributes are eternal", 20: "God's existence and essence are one",
    21: "what follows from an attribute's absolute nature is infinite and eternal",
    22: "so too what follows from an attribute so modified", 23: "every infinite mode follows from an attribute",
    24: "the essence of things God produces does not involve existence",
    25: "God causes the essence and the existence of things", 26: "what is determined to act, God so determined",
    27: "what God determines cannot undetermine itself", 28: "every finite thing is caused by another finite thing",
    29: "nothing in nature is contingent", 30: "intellect must comprehend God's attributes",
    31: "intellect belongs to nature natured", 32: "will is not a free cause, but a necessary one",
    33: "things could not have been produced otherwise", 34: "God's power is his essence",
    35: "whatever is in God's power necessarily exists", 36: "nothing exists from which no effect follows",
}
# what each demonstration cites, in Elwes's translation (computed by parse_ethics from Project Gutenberg #3800)
CITES = {
    1: "D3 D5", 2: "D3", 3: "A4 A5", 4: "A1 A4 D3 D5", 5: "D3 D6 P1 P4", 6: "P2 P3", 7: "P6", 8: "D2 P5 P7",
    9: "D4", 10: "D3 D4", 11: "A1 D6 P2 P7", 12: "D4 P2 P5 P6 P7 P8 P10", 13: "P5 P7 P11", 14: "D6 P5 P11",
    15: "A1 D3 D5 P14", 16: "D6", 17: "P15 P16", 18: "P14 P15 P16", 19: "D4 D6 D8 P7 P11", 20: "D8 P19",
    21: "D2 P11 P20", 22: "P21", 23: "D5 D8 P15 P21 P22", 24: "D1", 25: "A4 P15", 26: "P16 P25", 27: "A3",
    28: "A1 D3 D5 P21 P24 P26", 29: "P11 P15 P16 P24 P26 P27", 30: "A6 P14 P15", 31: "D5 D6 P15",
    32: "D7 P23 P28", 33: "P11 P14 P16 P29", 34: "P11 P16", 35: "P34", 36: "P16 P25 P34",
}
LATIN_ONLY = {11: ["A7"]}   # 'Ergo (per Axiom. 7) ejus essentia non involvit existentiam'


def _roman(s: str) -> int:
    vals = {"i": 1, "v": 5, "x": 10, "l": 50}
    s = s.lower()
    return sum(-vals[a] if i + 1 < len(s) and vals[s[i + 1]] > vals[a] else vals[a] for i, a in enumerate(s))


def parse_ethics(text: str) -> dict:
    """Read the citations in the demonstrations of Ethics I from Elwes's text (Project Gutenberg #3800)."""
    lines = text.splitlines()
    start = next(i for i, ln in enumerate(lines) if ln.startswith("PROP. I. "))
    end = next(i for i, ln in enumerate(lines) if ln.startswith("APPENDIX"))
    props, cur, mode = {}, None, None
    for ln in lines[start:end]:
        m = re.match(r"PROP\. ([IVXL]+)\.\s*(.*)", ln)
        if m:
            cur = _roman(m.group(1))
            props[cur] = {"stmt": [m.group(2)], "proof": []}
            mode = "stmt"
            continue
        if cur is None:
            continue
        if re.match(r"(Proof|Another proof)", ln):
            mode = "proof"
        elif re.match(r"(Corollary|Coroll\. ?[IVX]*\.?--|Note|Explanation)", ln):
            mode = "other"
        if mode in ("stmt", "proof"):
            props[cur][mode].append(ln)
    out = {}
    for n, p in props.items():
        body = re.sub(r"\s+", " ", " ".join(p["proof"]) or " ".join(p["stmt"]))
        found, kind = set(), None
        for m in re.finditer(r"(Deff?\.|Ax\.|Axiom\.?|Axioms|Props?\.?|Coroll?\.|Schol\.?|Note|Part)|\b([ivxl]+)\b\.?",
                             body):
            if m.group(1):
                w = m.group(1).lower()
                kind = "D" if w.startswith("def") else "A" if w.startswith("ax") else "P" if w.startswith("prop") \
                    else None
            elif kind:
                found.add(f"{kind}{_roman(m.group(2))}")
        if "the third axiom" in body:
            found.add("A3")
        if "the preceding one" in body or "the last Prop" in body:
            found.add(f"P{n - 1}")
        out[n] = " ".join(sorted(found, key=lambda s: (s[0], int(s[1:]))))
    return out


def ethics_graph(latin: bool = False) -> dict:
    """Nodes D1..D8, A1..A7, P1..P36; an edge X -> Pn when the demonstration of Pn cites X."""
    nodes = [f"D{i}" for i in DEFINITIONS] + [f"A{i}" for i in AXIOMS] + [f"P{i}" for i in PROPOSITIONS]
    edges = []
    for n, cs in CITES.items():
        for c in cs.split():
            edges.append((c, f"P{n}"))
        if latin:
            for c in LATIN_ONLY.get(n, []):
                edges.append((c, f"P{n}"))
    return {"nodes": nodes, "edges": edges}


def _order(g: dict) -> list:
    """A topological order (Kahn's algorithm); raises if there is a cycle."""
    indeg = {v: 0 for v in g["nodes"]}
    out = {v: [] for v in g["nodes"]}
    for a, b in g["edges"]:
        indeg[b] += 1
        out[a].append(b)
    ready = [v for v in g["nodes"] if indeg[v] == 0]
    order = []
    while ready:
        v = ready.pop(0)
        order.append(v)
        for w in out[v]:
            indeg[w] -= 1
            if indeg[w] == 0:
                ready.append(w)
    if len(order) != len(g["nodes"]):
        raise ValueError("the citations are circular")
    return order


def forward_only(g: dict) -> bool:
    """Every proposition cites only earlier propositions: the order of the book is a topological order."""
    return all(not (a.startswith("P") and int(a[1:]) >= int(b[1:])) for a, b in g["edges"])


def depth(g: dict) -> dict:
    """The length of the longest chain of citations ending at each node (definitions and axioms have depth 0)."""
    d = {v: 0 for v in g["nodes"]}
    preds = {v: [] for v in g["nodes"]}
    for a, b in g["edges"]:
        preds[b].append(a)
    for v in _order(g):
        if preds[v]:
            d[v] = 1 + max(d[p] for p in preds[v])
    return d


def longest_chain(g: dict) -> list:
    d = depth(g)
    preds = {v: [] for v in g["nodes"]}
    for a, b in g["edges"]:
        preds[b].append(a)
    v = max(g["nodes"], key=lambda x: (d[x], -g["nodes"].index(x)))
    chain = [v]
    while preds[v]:
        v = max(preds[v], key=lambda x: (d[x], -g["nodes"].index(x)))
        chain.append(v)
    return chain[::-1]


def unused(g: dict) -> list:
    cited = {a for a, _ in g["edges"]}
    return [v for v in g["nodes"] if not v.startswith("P") and v not in cited]


def most_cited(g: dict, k: int = 5) -> list:
    count = {}
    for a, _ in g["edges"]:
        count[a] = count.get(a, 0) + 1
    return sorted(count.items(), key=lambda kv: (-kv[1], kv[0]))[:k]


def ancestors(g: dict, v: str) -> set:
    preds = {x: [] for x in g["nodes"]}
    for a, b in g["edges"]:
        preds[b].append(a)
    seen, stack = set(), [v]
    while stack:
        x = stack.pop()
        for p in preds[x]:
            if p not in seen:
                seen.add(p)
                stack.append(p)
    return seen


# ---------------------------------------------------------------------------
# Leibniz: finite and infinite analysis
# ---------------------------------------------------------------------------
def continued_fraction(q: Fraction) -> list:
    """Euclid's algorithm: the analysis of a ratio always ends."""
    out = []
    a, b = q.numerator, q.denominator
    while b:
        out.append(a // b)
        a, b = b, a - (a // b) * b
    return out


def sqrt_cf(n: int, terms: int = 12) -> list:
    """The continued fraction of sqrt(n), exactly (integer arithmetic): it never ends, but repeats."""
    a0 = math.isqrt(n)
    if a0 * a0 == n:
        return [a0]
    m, d, a = 0, 1, a0
    out = [a0]
    while len(out) < terms:
        m = d * a - m
        d = (n - m * m) // d
        a = (a0 + m) // d
        out.append(a)
    return out


def convergents(cf: list) -> list:
    h0, h1, k0, k1 = 1, cf[0], 0, 1
    out = [Fraction(h1, k1)]
    for a in cf[1:]:
        h0, h1 = h1, a * h1 + h0
        k0, k1 = k1, a * k1 + k0
        out.append(Fraction(h1, k1))
    return out


# ---------------------------------------------------------------------------
# Descartes: the method of normals (La Géométrie, Book II)
# ---------------------------------------------------------------------------
def descartes_normal(a: Fraction = Fraction(1)) -> dict:
    """The normal to y = x^2 at (a, a^2). Descartes: find the circle, centred on the y-axis at (0, k), that meets the
    curve at P twice over. Substituting x^2 = y into x^2 + (y - k)^2 = r^2 gives y^2 + (1 - 2k) y + k^2 - r^2 = 0,
    which must have y = a^2 as a double root: so its two roots sum to 2a^2, that is 2k - 1 = 2a^2."""
    import sympy as sp
    y, k, r2 = sp.symbols("y k r2")
    quad = sp.expand(y + (y - k) ** 2 - r2)
    target = sp.expand((y - sp.Rational(a.numerator, a.denominator) ** 2) ** 2)
    sol = sp.solve(sp.Poly(quad - target, y).coeffs(), [k, r2], dict=True)[0]
    kk = sol[k]
    # the line from the centre (0, k) to P is the normal: check it is perpendicular to the tangent (slope 2a)
    A = sp.Rational(a.numerator, a.denominator)
    slope_normal = (A ** 2 - kk) / A
    return {"quadratic": str(sp.collect(quad, y)), "k": str(kk), "r2": str(sol[r2]),
            "perpendicular": bool(sp.simplify(slope_normal * 2 * A + 1) == 0)}


# ---------------------------------------------------------------------------
# Hume: the missing shade of blue
# ---------------------------------------------------------------------------
def blue_shades(n: int = 11, missing: int = 6) -> dict:
    """n shades from light to dark blue, evenly spaced in lightness; one is left out."""
    light, dark = (205, 225, 255), (10, 30, 120)
    shades = []
    for i in range(n):
        t = i / (n - 1)
        rgb = tuple(round(light[j] + (dark[j] - light[j]) * t) for j in range(3))
        shades.append("#%02X%02X%02X" % rgb)
    return {"shades": shades, "missing": missing}


def habits(sequence: str) -> list:
    """A Humean learner: after each observation of a cause, how strong is the expectation of the usual effect?
    (the fraction of past cases with the effect, after a first case; no reason, only custom)."""
    out, seen, with_effect = [], 0, 0
    for ch in sequence:
        seen += 1
        with_effect += ch == "1"
        out.append(with_effect / seen)
    return out


def rival_rules(data: list, horizon: int = 12) -> list:
    """Rules that agree with every observation so far and disagree about tomorrow."""
    n = len(data)
    rules = [("always", lambda t: 1), (f"until day {n}", lambda t: 1 if t < n else 0),
             (f"until day {n + 2}", lambda t: 1 if t < n + 2 else 0), ("on even days after", lambda t: 1 if t < n
                                                                       else int(t % 2 == 0))]
    out = []
    for name, f in rules:
        ok = all(f(t) == v for t, v in enumerate(data))
        out.append({"rule": name, "fits": ok, "tomorrow": f(n), "forecast": [f(t) for t in range(n, horizon)]})
    return out


# ---------------------------------------------------------------------------
# Kant: the grid, and what became of his examples
# ---------------------------------------------------------------------------
GRID = [
    ("all bachelors are unmarried", "analytic", "a priori", "Kant; everyone"),
    ("all bodies are extended", "analytic", "a priori", "Kant's own example"),
    ("some bodies are heavy", "synthetic", "a posteriori", "Kant's own example"),
    ("7 + 5 = 12", "synthetic", "a priori", "Kant; Frege: analytic (Part 9)"),
    ("a triangle's angles sum to 180°", "synthetic", "a priori", "Kant; after 1915: a posteriori, and false"),
    ("every event has a cause", "synthetic", "a priori", "Kant: the second analogy"),
    ("water is H$_2$O", "synthetic", "a posteriori", "Kripke: yet necessary (Part 22)"),
]


def spherical_excess(a_km: float, b_km: float, c_km: float, radius_km: float = 6371.0) -> dict:
    """A triangle's angles on a sphere sum to 180 degrees plus area / R^2 (in radians): Heron's formula for the
    (nearly flat) area, converted to arcseconds."""
    s = (a_km + b_km + c_km) / 2
    area = math.sqrt(s * (s - a_km) * (s - b_km) * (s - c_km))
    excess = area / radius_km ** 2
    return {"area_km2": area, "excess_arcsec": math.degrees(excess) * 3600}


GAUSS_TRIANGLE = {"Brocken-Hohehagen": 69.2, "Hohehagen-Inselsberg": 85.0, "Inselsberg-Brocken": 105.97}


def octant() -> dict:
    """The triangle with one vertex at the north pole and two on the equator, 90 degrees apart: three right angles."""
    return {"angles": [90, 90, 90], "sum": 270, "excess_deg": 90, "area_fraction_of_sphere": Fraction(1, 8)}


# ---------------------------------------------------------------------------
# Leibniz's optics: nature takes the easiest path (Fermat 1662; Leibniz 1682)
# ---------------------------------------------------------------------------
def least_time(a=(0.0, 1.0), b=(2.0, -1.0), v1: float = 1.0, v2: float = 0.75, iters: int = 200) -> dict:
    """Light goes from a (above the surface y = 0, speed v1) to b (below, speed v2). Among all crossing points x on
    the surface, find the one of least travel time (ternary search, the time is convex in x), and check Snell's law:
    sin(i) / v1 = sin(r) / v2 there."""
    def t(x):
        return math.hypot(x - a[0], a[1]) / v1 + math.hypot(b[0] - x, b[1]) / v2
    lo, hi = a[0], b[0]
    for _ in range(iters):
        m1, m2 = lo + (hi - lo) / 3, hi - (hi - lo) / 3
        if t(m1) < t(m2):
            hi = m2
        else:
            lo = m1
    x = (lo + hi) / 2
    sin_i = (x - a[0]) / math.hypot(x - a[0], a[1])
    sin_r = (b[0] - x) / math.hypot(b[0] - x, b[1])
    samples = [(round(a[0] + (b[0] - a[0]) * k / 20, 3), t(a[0] + (b[0] - a[0]) * k / 20)) for k in range(21)]
    return {"x": x, "time": t(x), "sin_i_over_v1": sin_i / v1, "sin_r_over_v2": sin_r / v2, "samples": samples,
            "straight_time": t(a[0] + (b[0] - a[0]) * a[1] / (a[1] - b[1]))}


def light_bending() -> dict:
    """Starlight grazing the sun: general relativity predicts a deflection of 4GM/(c^2 R), twice the 'Newtonian'
    value 2GM/(c^2 R) (Soldner 1801); Eddington's eclipse expedition of 1919 found the larger one."""
    G, M, c, R = 6.674e-11, 1.989e30, 2.998e8, 6.957e8
    rad_to_arcsec = 180 / math.pi * 3600
    gr = 4 * G * M / (c * c * R) * rad_to_arcsec
    return {"einstein": gr, "newton": gr / 2, "sobral_1919": 1.98, "principe_1919": 1.61}


# ---------------------------------------------------------------------------
# Kant's incongruent counterparts (1768): a hand and its mirror image
# ---------------------------------------------------------------------------
HAND = [(0, 0), (1, 0), (2, 0), (0, 1), (0, 2), (0, 3)]   # an L of six cells: a flat 'hand'


def _normal(cells):
    mx, my = min(x for x, _ in cells), min(y for _, y in cells)
    return frozenset((x - mx, y - my) for x, y in cells)


def chirality(cells=HAND) -> dict:
    """Try all four rotations of a plane shape against its mirror image (reflection in a vertical line). In the
    plane, no rotation works when the shape is chiral; a turn through the third dimension (flipping it over) does."""
    mirror = _normal([(-x, y) for x, y in cells])
    rots, cur = [], list(cells)
    for k in range(4):
        rots.append(_normal(cur))
        cur = [(-y, x) for x, y in cur]
    return {"rotations_match": [r == mirror for r in rots], "flip_matches": _normal([(-x, y) for x, y in cells]) ==
            mirror, "cells": cells}
