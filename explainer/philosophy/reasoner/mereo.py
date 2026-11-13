"""Ontology, built: what there is (Part 20).

* Quine's criterion on small models: the Geach--Kaplan sentence, which quantifies over pluralities, checked by brute
  force on admiration graphs.
* Resemblance nominalism on property tables: maximal resemblance classes against property extensions (Goodman's
  imperfect community and companionship difficulties).
* Finite mereology: every partial order on up to six elements, up to isomorphism, tested axiom by axiom (weak and
  strong supplementation, unrestricted fusion); the finite models of classical extensional mereology are exactly the
  Boolean algebras with the bottom removed, so they have 2^k - 1 elements.
* The special composition question counted on a grid of simples (nihilism, contact, universalism), Putnam's three
  individuals (3 objects, or 7), and gunk as endless bisection.
* Grounding as a strict partial order: irreflexivity, asymmetry, transitivity, fundamental facts and levels.
"""

from __future__ import annotations

import itertools
from functools import lru_cache

import numpy as np


# ---------------------------------------------------------------------------
# Plural quantification: the Geach--Kaplan sentence
# ---------------------------------------------------------------------------
def geach_kaplan(n: int, admires: set[tuple[int, int]]) -> dict:
    """`Some critics admire only one another': there is a nonempty plurality X such that whenever x is among X and
    x admires y, then y is among X and y is not x. Checked over every nonempty subset; returns the witnesses."""
    wit = []
    for k in range(1, n + 1):
        for X in itertools.combinations(range(n), k):
            S = set(X)
            if all((y in S and y != x) for x in S for (a, y) in admires if a == x):
                wit.append(sorted(S))
    return {"true": bool(wit), "witnesses": wit, "subsets_checked": 2 ** n - 1}


def geach_kaplan_demo() -> dict:
    """Three admiration graphs on five critics: one where the sentence holds, one where it fails, one where only the
    whole community witnesses it."""
    graphs = {
        "a closed circle": (5, {(0, 1), (1, 0), (2, 3), (3, 4), (4, 0)}),
        "everyone admires a self-admirer": (5, {(0, 1), (1, 2), (2, 2), (3, 2), (4, 3)}),
        "a ring": (5, {(i, (i + 1) % 5) for i in range(5)}),
    }
    out = {}
    for name, (n, A) in graphs.items():
        r = geach_kaplan(n, A)
        out[name] = {"edges": sorted(A), "true": r["true"], "witnesses": r["witnesses"][:4],
                     "n_witnesses": len(r["witnesses"]), "checked": r["subsets_checked"]}
    return out


# ---------------------------------------------------------------------------
# Resemblance nominalism
# ---------------------------------------------------------------------------
def resemblance_classes(objects: dict[str, set[str]]) -> dict:
    """Two objects resemble iff they share a property. A resemblance class is a maximal set of pairwise resembling
    objects (a maximal clique). The nominalist hopes these are exactly the property extensions."""
    names = list(objects)
    res = {(a, b) for a in names for b in names if a != b and objects[a] & objects[b]}
    cliques = []
    for k in range(len(names), 0, -1):
        for C in itertools.combinations(names, k):
            if all((a, b) in res for a, b in itertools.combinations(C, 2)) and not any(
                    set(C) < set(D) for D in cliques):
                cliques.append(C)
    props = sorted({p for s in objects.values() for p in s})
    ext = {p: tuple(n for n in names if p in objects[n]) for p in props}
    cl = [tuple(c) for c in cliques if len(c) > 1]
    spurious = [c for c in cl if c not in ext.values()]
    missing = {p: e for p, e in ext.items() if e not in cl}
    return {"objects": {k: sorted(v) for k, v in objects.items()}, "classes": cl, "extensions": ext,
            "spurious": spurious, "missing": missing}


def goodman_demo() -> dict:
    """Imperfect community: a, b, c pairwise share a property but no property is common to all three. Companionship:
    every F is G, so the F's are never a maximal resemblance class."""
    imperfect = {"a": {"F", "G"}, "b": {"G", "H"}, "c": {"F", "H"}}
    companion = {"d": {"F", "G"}, "e": {"F", "G"}, "f": {"G"}}
    return {"imperfect": resemblance_classes(imperfect), "companionship": resemblance_classes(companion)}


# ---------------------------------------------------------------------------
# Finite mereology
# ---------------------------------------------------------------------------
class Poset:
    """A finite partial order: ``le[i][j]`` means i is part of j (reflexive, antisymmetric, transitive)."""

    def __init__(self, n: int, le):
        self.n = n
        self.le = [list(r) for r in le]

    def part(self, x, y) -> bool:
        return self.le[x][y]

    def proper(self, x, y) -> bool:
        return x != y and self.le[x][y]

    def overlap(self, x, y) -> bool:
        return any(self.le[z][x] and self.le[z][y] for z in range(self.n))

    # -- axioms -------------------------------------------------------------
    def wsp(self) -> bool:
        """Weak supplementation: if x is a proper part of y, some part of y does not overlap x."""
        return all(any(self.le[z][y] and not self.overlap(z, x) for z in range(self.n))
                   for x in range(self.n) for y in range(self.n) if self.proper(x, y))

    def ssp(self) -> bool:
        """Strong supplementation: if y is not part of x, some part of y does not overlap x."""
        return all(any(self.le[z][y] and not self.overlap(z, x) for z in range(self.n))
                   for x in range(self.n) for y in range(self.n) if not self.le[y][x])

    def fusion(self, S) -> list[int]:
        """The fusions of S: z such that for every w, w overlaps z iff w overlaps some member of S."""
        return [z for z in range(self.n) if all(self.overlap(w, z) == any(self.overlap(w, s) for s in S)
                                                for w in range(self.n))]

    def uf(self) -> bool:
        """Unrestricted fusion: every nonempty subset has a fusion."""
        return all(self.fusion(S) for k in range(1, self.n + 1) for S in itertools.combinations(range(self.n), k))

    def extensional(self) -> bool:
        """Composite objects with the same proper parts are identical."""
        pp = [frozenset(z for z in range(self.n) if self.proper(z, x)) for x in range(self.n)]
        return all(not (pp[x] and pp[x] == pp[y]) for x in range(self.n) for y in range(x + 1, self.n))

    def atoms(self) -> list[int]:
        return [x for x in range(self.n) if not any(self.proper(z, x) for z in range(self.n))]

    def hasse(self) -> list[tuple[int, int]]:
        return [(x, y) for x in range(self.n) for y in range(self.n) if self.proper(x, y) and not any(
            self.proper(x, z) and self.proper(z, y) for z in range(self.n))]

    def profile(self) -> dict:
        return {"wsp": self.wsp(), "ssp": self.ssp(), "uf": self.uf(), "ext": self.extensional()}


def _natural_posets(n: int):
    """Every partial order on 0..n-1 whose order relation respects the natural order (i < j whenever i is a proper
    part of j). Every finite poset is isomorphic to one of these (take a linear extension)."""
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    for mask in range(1 << len(pairs)):
        lt = [[False] * n for _ in range(n)]
        for b, (i, j) in enumerate(pairs):
            if mask >> b & 1:
                lt[i][j] = True
        ok = True
        for i, j in pairs:
            if lt[i][j]:
                for k in range(j + 1, n):
                    if lt[j][k] and not lt[i][k]:
                        ok = False
                        break
            if not ok:
                break
        if ok:
            yield lt


def _canon(n: int, lt) -> tuple:
    best = None
    for p in itertools.permutations(range(n)):
        key = tuple(lt[p[i]][p[j]] for i in range(n) for j in range(n))
        if best is None or key < best:
            best = key
    return best


@lru_cache(maxsize=None)
def posets_up_to_iso(n: int) -> list[Poset]:
    seen, out = set(), []
    for lt in _natural_posets(n):
        k = _canon(n, lt)
        if k in seen:
            continue
        seen.add(k)
        out.append(Poset(n, [[i == j or lt[i][j] for j in range(n)] for i in range(n)]))
    return out


def mereology_census(max_n: int = 6) -> dict:
    """For each size, how many posets (up to isomorphism) satisfy each axiom, and which satisfy classical extensional
    mereology (partial order + strong supplementation + unrestricted fusion)."""
    rows = []
    for n in range(1, max_n + 1):
        ps = posets_up_to_iso(n)
        prof = [p.profile() for p in ps]
        cem = [p for p, f in zip(ps, prof) if f["ssp"] and f["uf"]]
        rows.append({"n": n, "posets": len(ps), "wsp": sum(f["wsp"] for f in prof),
                     "ssp": sum(f["ssp"] for f in prof), "uf": sum(f["uf"] for f in prof), "cem": len(cem),
                     "cem_hasse": [p.hasse() for p in cem], "cem_atoms": [len(p.atoms()) for p in cem]})
    return {"rows": rows}


def boolean_minus_bottom(k: int) -> Poset:
    """The nonempty subsets of k atoms, ordered by inclusion: the model of CEM with k atoms."""
    subs = [frozenset(s) for r in range(1, k + 1) for s in itertools.combinations(range(k), r)]
    return Poset(len(subs), [[a <= b for b in subs] for a in subs])


def boolean_check(k_max: int = 4) -> dict:
    out = {}
    for k in range(1, k_max + 1):
        P = boolean_minus_bottom(k)
        out[k] = {"size": P.n, **P.profile(), "atoms": len(P.atoms())}
    return out


def counterexamples() -> dict:
    """Two classic failures. (1) Two wholes built from the same two parts: weak supplementation holds, strong fails, so
    extensionality fails. (2) A single proper part: a whole with only one proper part violates weak supplementation."""
    # a=0, b=1, x=2, y=3; a, b < x and a, b < y
    le = [[i == j for j in range(4)] for i in range(4)]
    for p in (0, 1):
        for w in (2, 3):
            le[p][w] = True
    twin = Poset(4, le)
    le2 = [[True, True], [False, True]]
    lonely = Poset(2, le2)
    return {"twin": {**twin.profile(), "hasse": twin.hasse()}, "lonely": {**lonely.profile(), "hasse": lonely.hasse()}}


# ---------------------------------------------------------------------------
# The special composition question, counted
# ---------------------------------------------------------------------------
def grid_graph(rows: int, cols: int):
    cells = [(r, c) for r in range(rows) for c in range(cols)]
    idx = {c: i for i, c in enumerate(cells)}
    adj = {i: set() for i in range(len(cells))}
    for (r, c), i in idx.items():
        for dr, dc in ((0, 1), (1, 0)):
            j = idx.get((r + dr, c + dc))
            if j is not None:
                adj[i].add(j)
                adj[j].add(i)
    return cells, adj


def _connected(S, adj) -> bool:
    S = set(S)
    start = next(iter(S))
    seen, stack = {start}, [start]
    while stack:
        v = stack.pop()
        for w in adj[v] & S:
            if w not in seen:
                seen.add(w)
                stack.append(w)
    return seen == S


def composition_counts(rows: int = 2, cols: int = 3) -> dict:
    """How many objects are there, on each answer to van Inwagen's question, among rows x cols blocks? Nihilism: only
    the simples. Contact: every connected group composes something. Universalism: every nonempty group does.
    ``scattered_example`` is the first group that is not connected, or None when every group is (one or two blocks
    in a row)."""
    cells, adj = grid_graph(rows, cols)
    n = len(cells)
    subsets = [S for k in range(1, n + 1) for S in itertools.combinations(range(n), k)]
    contact = [S for S in subsets if _connected(S, adj)]
    by_size = {k: sum(1 for S in contact if len(S) == k) for k in range(1, n + 1)}
    return {"rows": rows, "cols": cols, "simples": n, "nihilism": n, "contact": len(contact),
            "universalism": 2 ** n - 1, "contact_by_size": by_size,
            "scattered_example": next((list(S) for S in subsets if not _connected(S, adj)), None)}


def putnam_world(k: int = 3) -> dict:
    """Putnam's cookie cutter: a world of k individuals. `How many objects?' Carnap: k. A Polish logician who accepts
    every mereological sum: 2^k - 1."""
    sums = [list(s) for r in range(1, k + 1) for s in itertools.combinations(range(k), r)]
    return {"k": k, "carnap": k, "polish": 2 ** k - 1, "sums": sums}


def gunk(depth: int = 6) -> dict:
    """Bisect [0, 1] again and again: the dyadic intervals. At every finite depth there are atoms (the smallest
    intervals), but each has a proper part one level down; the limit structure is atomless (gunk)."""
    levels = [[(i / 2 ** d, (i + 1) / 2 ** d) for i in range(2 ** d)] for d in range(depth + 1)]
    parts_total = [2 ** (d + 1) - 1 for d in range(depth + 1)]
    return {"levels": levels, "parts_total": parts_total, "atoms_at_depth": [2 ** d for d in range(depth + 1)]}


# ---------------------------------------------------------------------------
# Grounding
# ---------------------------------------------------------------------------
GROUNDING = {
    # fact: list of facts that (together) immediately ground it
    "electron 1 is charged": [],
    "electron 2 is charged": [],
    "the particles are arranged tablewise": [],
    "Socrates exists": [],
    "snow is white": [],
    "the table exists": ["the particles are arranged tablewise"],
    "the table is solid": ["the table exists", "the particles are arranged tablewise"],
    "Socrates' singleton exists": ["Socrates exists"],
    "Socrates exists or Zeus exists": ["Socrates exists"],
    "'snow is white' is true": ["snow is white"],
    "something is charged": ["electron 1 is charged"],
    "something is charged and the table exists": ["something is charged", "the table exists"],
}


def grounding_check(G: dict | None = None) -> dict:
    """Close the immediate-grounding graph under transitivity; check irreflexivity and asymmetry (a strict partial
    order), find the fundamental (ungrounded) facts, and assign each fact a level: the length of its longest grounding
    chain down to the fundamental."""
    G = G or GROUNDING
    facts = list(G)
    below = {f: set() for f in facts}

    def down(f, seen=()):
        out = set()
        for g in G[f]:
            if g in seen:
                return None
            sub = down(g, seen + (f,))
            if sub is None:
                return None
            out |= {g} | sub
        return out

    cyclic = False
    for f in facts:
        d = down(f)
        if d is None:
            cyclic = True
            break
        below[f] = d
    irreflexive = not cyclic and all(f not in below[f] for f in facts)
    asymmetric = not cyclic and all(not (g in below[f] and f in below[g]) for f in facts for g in facts)
    transitive = not cyclic and all(below[h] <= below[f] for f in facts for h in below[f])

    @lru_cache(maxsize=None)
    def level(f):
        return 0 if not G[f] else 1 + max(level(g) for g in G[f])

    levels = {f: level(f) for f in facts} if not cyclic else {}
    return {"facts": facts, "edges": [(g, f) for f in facts for g in G[f]], "irreflexive": irreflexive,
            "asymmetric": asymmetric, "transitive": transitive, "fundamental": [f for f in facts if not G[f]],
            "levels": levels, "cyclic": cyclic}


def grounding_cycle_demo() -> dict:
    """Add `the table exists' as a ground of the particles' arrangement, and the order breaks."""
    G = dict(GROUNDING)
    G["the particles are arranged tablewise"] = ["the table exists"]
    return grounding_check(G)


def descent(n: int = 8) -> dict:
    """An infinite descending grounding chain, truncated: each level's facts grounded in the next level's. Every
    finite truncation has a bottom; the chain itself has none."""
    chain = [f"level {i}" for i in range(n)]
    return {"chain": chain, "bottom_in_truncation": chain[-1]}


def summary() -> dict:
    c = mereology_census(5)
    return {"posets": [r["posets"] for r in c["rows"]], "cem": [r["cem"] for r in c["rows"]]}


if __name__ == "__main__":  # pragma: no cover
    import json
    print(json.dumps(summary(), indent=1))
    print(np.__name__)


# ---------------------------------------------------------------------------
# Fine's truth-functional logic of ground
# ---------------------------------------------------------------------------
def _true(f, v) -> bool:
    if isinstance(f, str):
        return v[f]
    op = f[0]
    if op == "not":
        return not _true(f[1], v)
    if op == "and":
        return _true(f[1], v) and _true(f[2], v)
    return _true(f[1], v) or _true(f[2], v)


def show_f(f) -> str:
    if isinstance(f, str):
        return f
    op = f[0]
    if op == "not":
        inner = show_f(f[1])
        return r"\lnot " + (inner if isinstance(f[1], str) or f[1][0] == "not" else "(" + inner + ")")
    sym = r" \land " if op == "and" else r" \lor "
    parts = []
    for x in (f[1], f[2]):
        s = show_f(x)
        if not isinstance(x, str) and x[0] in ("and", "or") and x[0] != op:
            s = "(" + s + ")"
        parts.append(s)
    return sym.join(parts)


def immediate_grounds(f, v) -> list[list]:
    """Fine (2012): the full immediate grounds of a true truth-functional formula. A true disjunct grounds a
    disjunction; both conjuncts together ground a conjunction; a double negation is grounded in what it negates; a
    negated conjunction in either false conjunct's negation; a negated disjunction in both negations together.
    Literals (atoms and negated atoms) are fundamental: they have no grounds."""
    assert _true(f, v)
    if isinstance(f, str):
        return []
    op = f[0]
    if op == "and":
        return [[f[1], f[2]]]
    if op == "or":
        return [[x] for x in (f[1], f[2]) if _true(x, v)]
    g = f[1]
    if isinstance(g, str):
        return []
    if g[0] == "not":
        return [[g[1]]]
    if g[0] == "and":
        return [[("not", x)] for x in (g[1], g[2]) if not _true(x, v)]
    return [[("not", g[1]), ("not", g[2])]]


def ground_tree(f, v) -> dict:
    """Unfold the immediate grounds down to the literals: every node is a true formula with its alternative full
    grounds; the leaves are the fundamental facts."""
    nodes, edges = [], []

    def walk(g, depth):
        i = len(nodes)
        nodes.append({"f": show_f(g), "depth": depth, "literal": not immediate_grounds(g, v)})
        for k, alt in enumerate(immediate_grounds(g, v)):
            for h in alt:
                j = walk(h, depth + 1)
                edges.append((j, i, k))
        return i

    walk(f, 0)
    leaves = sorted({n["f"] for n in nodes if n["literal"]})
    return {"nodes": nodes, "edges": edges, "fundamental": leaves}


def ground_demo() -> dict:
    v = {"p": True, "q": True, "r": False}
    f1 = ("or", ("and", "p", "q"), ("not", "r"))
    f2 = ("not", ("and", "r", ("not", "p")))
    f3 = ("or", "p", "p")
    return {"valuation": v, "f1": {"formula": show_f(f1), **ground_tree(f1, v)},
            "f2": {"formula": show_f(f2), **ground_tree(f2, v)},
            "f3": {"formula": show_f(f3), "grounds": [[show_f(x) for x in alt] for alt in immediate_grounds(f3, v)]}}
