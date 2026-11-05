"""Propositions as types (Curry–Howard), for Part 14.

* :func:`prove` searches for a program of a given type in the simply typed λ-calculus with pairs, sums and an empty
  type, which is the same thing as a proof in intuitionistic propositional logic.  The search uses invertible rules
  first, decomposes hypotheses, chains forward through implications, and refuses to revisit a (context, goal)
  pair, so it always terminates (every formula it meets is a subformula of the question).
* :func:`classical` checks a formula with truth tables.
* :func:`countermodel` finds a Kripke model (at most three worlds) in which the formula fails, which proves that
  *no* program has that type: excluded middle, double-negation elimination and Peirce's law are classically true
  and have no program.
"""
from __future__ import annotations

import itertools
import re


def atom(a):
    return ("atom", a)


def imp(a, b):
    return ("imp", a, b)


BOT = ("bot",)


def neg(a):
    return imp(a, BOT)


def parse(s: str):
    toks = re.findall(r"->|→|[&∧|∨~¬()]|False|⊥|[A-Z]", s)
    pos = 0

    def peek():
        return toks[pos] if pos < len(toks) else None

    def take():
        nonlocal pos
        pos += 1
        return toks[pos - 1]

    def p_imp():
        a = p_or()
        if peek() in ("->", "→"):
            take()
            return imp(a, p_imp())
        return a

    def p_or():
        a = p_and()
        while peek() in ("|", "∨"):
            take()
            a = ("or", a, p_and())
        return a

    def p_and():
        a = p_not()
        while peek() in ("&", "∧"):
            take()
            a = ("and", a, p_not())
        return a

    def p_not():
        if peek() in ("~", "¬"):
            take()
            return neg(p_not())
        t = take()
        if t == "(":
            a = p_imp()
            take()
            return a
        if t in ("False", "⊥"):
            return BOT
        return atom(t)

    f = p_imp()
    assert pos == len(toks), s
    return f


def show(f, prec=0) -> str:
    k = f[0]
    if k == "atom":
        return f[1]
    if k == "bot":
        return "⊥"
    if k == "imp" and f[2] == BOT:
        return "¬" + show(f[1], 4)
    if k == "imp":
        s = f"{show(f[1], 1)} → {show(f[2], 0)}"
        return f"({s})" if prec >= 1 else s
    if k == "and":
        s = f"{show(f[1], 3)} ∧ {show(f[2], 3)}"
        return f"({s})" if prec >= 3 else s
    s = f"{show(f[1], 2)} ∨ {show(f[2], 2)}"
    return f"({s})" if prec >= 2 else s


def tex(f, prec=0) -> str:
    k = f[0]
    if k == "atom":
        return f[1]
    if k == "bot":
        return r"\bot"
    if k == "imp" and f[2] == BOT:
        return r"\neg " + tex(f[1], 4)
    if k == "imp":
        s = rf"{tex(f[1], 1)} \to {tex(f[2], 0)}"
        return f"({s})" if prec >= 1 else s
    if k == "and":
        s = rf"{tex(f[1], 3)} \land {tex(f[2], 3)}"
        return f"({s})" if prec >= 3 else s
    s = rf"{tex(f[1], 2)} \lor {tex(f[2], 2)}"
    return f"({s})" if prec >= 2 else s


def atoms(f) -> set:
    if f[0] == "atom":
        return {f[1]}
    if f[0] == "bot":
        return set()
    return atoms(f[1]) | atoms(f[2])


# -- truth tables ----------------------------------------------------------------------------------------------
def holds(f, v) -> bool:
    k = f[0]
    if k == "atom":
        return v[f[1]]
    if k == "bot":
        return False
    if k == "imp":
        return (not holds(f[1], v)) or holds(f[2], v)
    if k == "and":
        return holds(f[1], v) and holds(f[2], v)
    return holds(f[1], v) or holds(f[2], v)


def classical(f) -> bool:
    names = sorted(atoms(f))
    return all(holds(f, dict(zip(names, bits))) for bits in itertools.product((False, True), repeat=len(names)))


# -- proof search = program synthesis --------------------------------------------------------------------------
class _Names:
    def __init__(self):
        self.k = 0

    def fresh(self):
        n = "xyzuvwpqrs"[self.k % 10] + ("" if self.k < 10 else str(self.k // 10))
        self.k += 1
        return n


def prove(goal, max_nodes=200000):
    """A λ-term (as a string) of type ``goal``, or None if there is none."""
    names = _Names()
    budget = [max_nodes]

    def add(ctx, x, A):
        """Add hypothesis x : A, splitting conjunctions."""
        out = list(ctx)
        work = [(x, A)]
        while work:
            t, B = work.pop()
            if any(B == C for _, C in out):
                continue
            out.append((t, B))
            if B[0] == "and":
                work.append((f"fst {_p(t)}", B[1]))
                work.append((f"snd {_p(t)}", B[2]))
        return tuple(out)

    def search(ctx, goal, seen):
        budget[0] -= 1
        if budget[0] < 0:
            return None
        key = (frozenset(B for _, B in ctx), goal)
        if key in seen:
            return None
        seen = seen | {key}
        for t, B in ctx:                       # an assumption of exactly this type
            if B == goal:
                return t
        for t, B in ctx:                       # ex falso
            if B == BOT:
                return f"absurd {_p(t)}"
        if goal[0] == "imp":                   # invertible right rules
            x = names.fresh()
            b = search(add(ctx, x, goal[1]), goal[2], seen)
            return None if b is None else f"λ{x}. {b}"
        if goal[0] == "and":
            a = search(ctx, goal[1], seen)
            if a is None:
                return None
            b = search(ctx, goal[2], seen)
            return None if b is None else f"({a}, {b})"
        for t, B in ctx:                       # invertible left rule: case on a disjunction
            if B[0] == "or":
                rest = tuple(h for h in ctx if h[0] != t)
                y, z = names.fresh(), names.fresh()
                l = search(add(rest, y, B[1]), goal, seen)
                if l is None:
                    continue
                r = search(add(rest, z, B[2]), goal, seen)
                if r is None:
                    continue
                return f"case {t} of inl {y} ⇒ {l} | inr {z} ⇒ {r}"
        for t, B in ctx:                       # use an implication: prove its premises, then its conclusion
            prem, C = [], B
            while C[0] == "imp":
                prem.append(C[1])
                C = C[2]
                if C == goal or C[0] in ("and", "or", "bot"):
                    args = []
                    for P in prem:
                        a = search(ctx, P, seen)
                        if a is None:
                            break
                        args.append(a)
                    else:
                        app = t + "".join(f" {_p(a)}" for a in args)
                        if C == goal:
                            return app
                        res = search(add(ctx, f"({app})", C), goal, seen)
                        if res is not None:
                            return res
        if goal[0] == "or":                    # choose a side
            a = search(ctx, goal[1], seen)
            if a is not None:
                return f"inl {_p(a)}"
            b = search(ctx, goal[2], seen)
            if b is not None:
                return f"inr {_p(b)}"
        return None

    return search((), goal, frozenset())


def _p(t: str) -> str:
    return t if re.fullmatch(r"[\w']+", t) or (t.startswith("(") and t.endswith(")") and _balanced(t[1:-1])) \
        else f"({t})"


def _balanced(s):
    d = 0
    for c in s:
        d += c == "("
        d -= c == ")"
        if d < 0:
            return False
    return d == 0


# -- Kripke countermodels --------------------------------------------------------------------------------------
def _posets(n):
    """Reflexive transitive antisymmetric orders on 0..n-1 with 0 below everything."""
    pairs = [(i, j) for i in range(n) for j in range(n) if i != j]
    for bits in itertools.product((0, 1), repeat=len(pairs)):
        le = {(i, i) for i in range(n)} | {p for p, b in zip(pairs, bits) if b}
        if any((j, i) in le for (i, j) in le if i != j):
            continue
        if any((i, k) not in le for (i, j) in le for (j2, k) in le if j == j2):
            continue
        if all((0, j) in le for j in range(n)):
            yield le


def forces(le, val, w, f, n):
    k = f[0]
    if k == "atom":
        return w in val[f[1]]
    if k == "bot":
        return False
    if k == "and":
        return forces(le, val, w, f[1], n) and forces(le, val, w, f[2], n)
    if k == "or":
        return forces(le, val, w, f[1], n) or forces(le, val, w, f[2], n)
    return all(not forces(le, val, v, f[1], n) or forces(le, val, v, f[2], n) for v in range(n) if (w, v) in le)


def countermodel(f, max_worlds=3):
    """A Kripke model whose root does not force f: (worlds, order, valuation), or None."""
    names = sorted(atoms(f))
    for n in range(1, max_worlds + 1):
        for le in _posets(n):
            ups = [frozenset(s) for r in range(n + 1) for s in itertools.combinations(range(n), r)
                   if all(v in s for u in s for v in range(n) if (u, v) in le)]
            for choice in itertools.product(ups, repeat=len(names)):
                val = dict(zip(names, choice))
                if not forces(le, val, 0, f, n):
                    return {"worlds": n, "order": sorted(p for p in le if p[0] != p[1]),
                            "valuation": {a: sorted(s) for a, s in val.items()}}
    return None


EXAMPLES = [
    ("identity", "A -> A"),
    ("K", "A -> B -> A"),
    ("composition", "(A -> B) -> (B -> C) -> A -> C"),
    ("S", "(A -> B -> C) -> (A -> B) -> A -> C"),
    ("swap", "A & B -> B & A"),
    ("currying", "(A & B -> C) -> A -> B -> C"),
    ("cases", "(A -> C) -> (B -> C) -> A | B -> C"),
    ("commute or", "A | B -> B | A"),
    ("double negation intro", "A -> ~~A"),
    ("contraposition", "(A -> B) -> ~B -> ~A"),
    ("not not excluded middle", "~~(A | ~A)"),
    ("excluded middle", "A | ~A"),
    ("double negation elim", "~~A -> A"),
    ("Peirce's law", "((A -> B) -> A) -> A"),
    ("de Morgan (the hard half)", "~(A & B) -> ~A | ~B"),
]


def table():
    rows = []
    for name, s in EXAMPLES:
        f = parse(s)
        p = prove(f)
        cm = None if p is not None else countermodel(f)
        rows.append({"name": name, "formula": show(f), "tex": tex(f), "classical": classical(f), "program": p,
                     "countermodel": cm})
    return rows
