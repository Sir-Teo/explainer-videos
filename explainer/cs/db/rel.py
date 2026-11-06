"""Relations and relational algebra (Part 35), and the theory of functional dependencies.

A relation is a set of tuples over named attributes.  Codd's operators each take relations and return one, so they
compose:

    sigma(R, pred)        selection: the tuples that satisfy pred
    pi(R, cols)           projection: some attributes, duplicates removed
    join(R, S, on)        natural or equi-join
    union, minus          set operations on relations with the same attributes
    rho(R, {old: new})    renaming
    product(R, S)         Cartesian product
    group(R, keys, aggs)  grouping with COUNT, SUM, MIN, MAX (an extension Codd did not have)

Functional dependencies (Armstrong 1974): ``closure(attrs, fds)``, ``keys``, ``is_bcnf``, ``bcnf_decompose``,
``synthesize_3nf``, and a check that a decomposition is lossless.
"""
from __future__ import annotations

import itertools
from dataclasses import dataclass, field


@dataclass
class Relation:
    cols: tuple[str, ...]
    rows: list[tuple] = field(default_factory=list)
    name: str = ""

    def __post_init__(self):
        self.cols = tuple(self.cols)

    def idx(self, c: str) -> int:
        if c in self.cols:
            return self.cols.index(c)
        for k, cc in enumerate(self.cols):            # "R.a" matches "a"
            if cc.split(".")[-1] == c:
                return k
        raise KeyError(c)

    def dicts(self):
        return [dict(zip(self.cols, r)) for r in self.rows]

    def __len__(self):
        return len(self.rows)

    def distinct(self) -> Relation:
        seen, out = set(), []
        for r in self.rows:
            if r not in seen:
                seen.add(r)
                out.append(r)
        return Relation(self.cols, out, self.name)

    def sorted(self, key=None) -> Relation:
        return Relation(self.cols, sorted(self.rows, key=key), self.name)

    def same(self, other: Relation) -> bool:
        """Equal as sets of tuples (attributes in the same order)."""
        return set(self.rows) == set(other.rows) and self.cols == other.cols


def table(cols, rows, name="") -> Relation:
    return Relation(tuple(cols), [tuple(r) for r in rows], name)


# ---- the algebra ----------------------------------------------------------------------------------------------
def sigma(R: Relation, pred) -> Relation:
    """``pred`` takes a dict of attribute -> value."""
    return Relation(R.cols, [r for r in R.rows if pred(dict(zip(R.cols, r)))], R.name)


def pi(R: Relation, cols) -> Relation:
    ix = [R.idx(c) for c in cols]
    return Relation(tuple(cols), [tuple(r[i] for i in ix) for r in R.rows]).distinct()


def rho(R: Relation, names: dict) -> Relation:
    return Relation(tuple(names.get(c, c) for c in R.cols), list(R.rows), R.name)


def product(R: Relation, S: Relation) -> Relation:
    return Relation(R.cols + S.cols, [r + s for r in R.rows for s in S.rows])


def join(R: Relation, S: Relation, on: list[tuple[str, str]] | None = None) -> Relation:
    """Equi-join on pairs (R attribute, S attribute); with ``on`` None, the natural join on shared names (the shared
    attributes appear once)."""
    if on is None:
        shared = [c for c in R.cols if c in S.cols]
        on = [(c, c) for c in shared]
        keep = [i for i, c in enumerate(S.cols) if c not in shared]
        cols = R.cols + tuple(S.cols[i] for i in keep)
    else:
        keep = list(range(len(S.cols)))
        cols = R.cols + S.cols
    ri = [R.idx(a) for a, _ in on]
    si = [S.idx(b) for _, b in on]
    h: dict = {}
    for s in S.rows:
        h.setdefault(tuple(s[i] for i in si), []).append(s)
    out = []
    for r in R.rows:
        for s in h.get(tuple(r[i] for i in ri), ()):
            out.append(r + tuple(s[i] for i in keep))
    return Relation(cols, out)


def union(R: Relation, S: Relation) -> Relation:
    assert R.cols == S.cols
    return Relation(R.cols, R.rows + S.rows).distinct()


def minus(R: Relation, S: Relation) -> Relation:
    assert R.cols == S.cols
    ss = set(S.rows)
    return Relation(R.cols, [r for r in R.rows if r not in ss]).distinct()


def group(R: Relation, keys, aggs) -> Relation:
    """``aggs``: [(name, "count"|"sum"|"min"|"max", attribute or None)]."""
    ki = [R.idx(k) for k in keys]
    acc: dict = {}
    for r in R.rows:
        acc.setdefault(tuple(r[i] for i in ki), []).append(r)
    out = []
    for k, rs in acc.items():
        vals = []
        for _, fn, a in aggs:
            if fn == "count":
                vals.append(len(rs))
            else:
                col = [r[R.idx(a)] for r in rs]
                vals.append({"sum": sum, "min": min, "max": max}[fn](col))
        out.append(k + tuple(vals))
    return Relation(tuple(keys) + tuple(n for n, _, _ in aggs), out)


# ---- functional dependencies -----------------------------------------------------------------------------------
FD = tuple[frozenset, frozenset]


def fd(lhs: str, rhs: str) -> FD:
    """fd("AB", "C"): attributes are single letters, or space-separated names."""
    def s(x):
        return frozenset(x.split()) if " " in x else frozenset(x)
    return s(lhs), s(rhs)


def closure(attrs, fds: list[FD]) -> frozenset:
    """X+ : every attribute determined by X, by Armstrong's axioms (computed by the usual fixpoint)."""
    x = set(attrs)
    changed = True
    while changed:
        changed = False
        for l, r in fds:
            if l <= x and not r <= x:
                x |= r
                changed = True
    return frozenset(x)


def keys(attrs, fds: list[FD]) -> list[frozenset]:
    """The candidate keys: minimal sets whose closure is everything."""
    attrs = frozenset(attrs)
    out = []
    for k in range(1, len(attrs) + 1):
        for c in itertools.combinations(sorted(attrs), k):
            c = frozenset(c)
            if any(o <= c for o in out):
                continue
            if closure(c, fds) >= attrs:
                out.append(c)
    return out


def project_fds(attrs, fds: list[FD]) -> list[FD]:
    """The dependencies that hold on a subset of the attributes (by closures of its subsets)."""
    attrs = frozenset(attrs)
    out = []
    for k in range(1, len(attrs)):
        for c in itertools.combinations(sorted(attrs), k):
            c = frozenset(c)
            r = (closure(c, fds) & attrs) - c
            if r:
                out.append((c, r))
    return out


def bcnf_violation(attrs, fds: list[FD]):
    """A dependency X -> Y on these attributes with X not a superkey, or None."""
    attrs = frozenset(attrs)
    for l, r in project_fds(attrs, fds):
        if not closure(l, fds) >= attrs:
            return l, r
    return None


def is_bcnf(attrs, fds) -> bool:
    return bcnf_violation(attrs, fds) is None


def bcnf_decompose(attrs, fds: list[FD]) -> list[frozenset]:
    """Split on a violating X -> Y into X ∪ Y and attrs − (Y − X), recursively: always lossless, not always
    dependency-preserving."""
    attrs = frozenset(attrs)
    v = bcnf_violation(attrs, fds)
    if v is None:
        return [attrs]
    l, r = v
    r = (closure(l, fds) & attrs) - l
    return bcnf_decompose(l | r, fds) + bcnf_decompose(attrs - r, fds)


def minimal_cover(fds: list[FD]) -> list[FD]:
    out = [(l, frozenset([a])) for l, r in fds for a in r]
    changed = True
    while changed:                                  # drop extraneous left-hand attributes
        changed = False
        for i, (l, r) in enumerate(out):
            for a in sorted(l):
                if len(l) > 1 and r <= closure(l - {a}, out):
                    out[i] = (l - {a}, r)
                    changed = True
                    break
    res = []
    for i, f in enumerate(out):                     # drop redundant dependencies
        rest = res + out[i + 1:]
        if not f[1] <= closure(f[0], rest):
            res.append(f)
    return list(dict.fromkeys(res))


def synthesize_3nf(attrs, fds: list[FD]) -> list[frozenset]:
    """Bernstein's synthesis: one relation per dependency of a minimal cover, plus a key if none contains one:
    lossless and dependency-preserving."""
    cover = minimal_cover(fds)
    rels = []
    for l, r in cover:
        s = l | r
        if not any(s <= x for x in rels):
            rels = [x for x in rels if not x <= s] + [s]
    ks = keys(attrs, fds)
    if not any(k <= x for x in rels for k in ks):
        rels.append(ks[0])
    return rels


def lossless(attrs, parts: list[frozenset], fds: list[FD]) -> bool:
    """The chase test: start with one row per part, distinguished where the part has the attribute; apply the
    dependencies; lossless iff some row becomes all distinguished."""
    attrs = sorted(attrs)
    rows = [{a: ("d" if a in p else ("s", i)) for a in attrs} for i, p in enumerate(parts)]
    changed = True
    while changed:
        changed = False
        for l, r in fds:
            for x, y in itertools.combinations(rows, 2):
                if all(x[a] == y[a] for a in l):
                    for a in r:
                        if x[a] != y[a]:
                            v = "d" if "d" in (x[a], y[a]) else min(x[a], y[a])
                            x[a] = y[a] = v
                            changed = True
    return any(all(r[a] == "d" for a in attrs) for r in rows)
