"""Propositions as types, and other objects of the philosophy of mathematics, exactly.

    from explainer.philosophy.reasoner.types import parse_type, prove, type_of, show_term
    t = prove(parse_type("A -> B -> A"))       # a lambda term: the K combinator, \\x. \\y. x
    type_of(t)                                  # A -> (B -> A), checked
    prove(parse_type("((A -> B) -> A) -> A"))   # None: Peirce's law has no intuitionistic proof
    countermodel(parse_type("A | ~A"))          # the two-world Kripke model that refutes it

Types are tuples: ("var", "A"), ("->", a, b), ("&", a, b), ("|", a, b), ("bot",); ~A abbreviates A -> bot. Terms:
("v", x), ("lam", x, type, body), ("app", f, a), ("pair", a, b), ("fst", p), ("snd", p), ("inl", a, type),
("inr", b, type), ("case", s, x, l, y, r), ("abort", t, type). Also: normalization (a proof's detours removed by
running it), transport between two presentations of the numbers, and winding numbers of loops on a circle.
"""

from __future__ import annotations

import itertools
import re

BOT = ("bot",)

# ---------------------------------------------------------------------------
# Types
# ---------------------------------------------------------------------------
_TOK = re.compile(r"\s*(->|&|\||~|\(|\)|⊥|bot|[A-Z][A-Za-z0-9']*)")


def parse_type(s: str):
    toks = _TOK.findall(s)
    if "".join(toks).replace(" ", "") != s.replace(" ", ""):
        raise ValueError(f"cannot tokenize {s!r}")
    pos = [0]

    def peek():
        return toks[pos[0]] if pos[0] < len(toks) else None

    def eat():
        pos[0] += 1
        return toks[pos[0] - 1]

    def atom():
        t = eat()
        if t == "(":
            a = imp()
            eat()
            return a
        if t == "~":
            return ("->", atom(), BOT)
        if t in ("⊥", "bot"):
            return BOT
        return ("var", t)

    def conj():
        a = atom()
        while peek() == "&":
            eat()
            a = ("&", a, atom())
        return a

    def disj():
        a = conj()
        while peek() == "|":
            eat()
            a = ("|", a, conj())
        return a

    def imp():
        a = disj()
        if peek() == "->":
            eat()
            return ("->", a, imp())
        return a

    t = imp()
    if peek() is not None:
        raise ValueError(f"trailing {peek()}")
    return t


def show_type(t, tex: bool = False, top: bool = True) -> str:
    op = t[0]
    if op == "var":
        return t[1]
    if op == "bot":
        return r"\bot" if tex else "⊥"
    if op == "->" and t[2] == BOT:
        return (r"\lnot " if tex else "¬") + show_type(t[1], tex, False)
    sym = {"->": r" \to " if tex else " → ", "&": r" \wedge " if tex else " ∧ ", "|": r" \vee " if tex else " ∨ "}[op]
    s = show_type(t[1], tex, False) + sym + show_type(t[2], tex, op != "->")
    return s if top else f"({s})"


# ---------------------------------------------------------------------------
# Terms and type checking
# ---------------------------------------------------------------------------
def type_of(term, ctx=None):
    """The type of a term in a context (dict var -> type); raises TypeError if it is ill-typed."""
    ctx = ctx or {}
    op = term[0]
    if op == "v":
        if term[1] not in ctx:
            raise TypeError(f"unbound {term[1]}")
        return ctx[term[1]]
    if op == "lam":
        _, x, ty, body = term
        return ("->", ty, type_of(body, {**ctx, x: ty}))
    if op == "app":
        f, a = type_of(term[1], ctx), type_of(term[2], ctx)
        if f[0] != "->" or f[1] != a:
            raise TypeError(f"cannot apply {show_type(f)} to {show_type(a)}")
        return f[2]
    if op == "pair":
        return ("&", type_of(term[1], ctx), type_of(term[2], ctx))
    if op in ("fst", "snd"):
        p = type_of(term[1], ctx)
        if p[0] != "&":
            raise TypeError("projection from a non-pair")
        return p[1] if op == "fst" else p[2]
    if op == "inl":
        return ("|", type_of(term[1], ctx), term[2])
    if op == "inr":
        return ("|", term[2], type_of(term[1], ctx))
    if op == "case":
        _, s, x, l, y, r = term
        st = type_of(s, ctx)
        if st[0] != "|":
            raise TypeError("case on a non-sum")
        lt, rt = type_of(l, {**ctx, x: st[1]}), type_of(r, {**ctx, y: st[2]})
        if lt != rt:
            raise TypeError("case branches differ")
        return lt
    if op == "abort":
        if type_of(term[1], ctx) != BOT:
            raise TypeError("abort of a non-bottom")
        return term[2]
    raise ValueError(term)


def show_term(t) -> str:
    op = t[0]
    if op == "v":
        return t[1]
    if op == "lam":
        return f"λ{t[1]}. {show_term(t[3])}"
    if op == "app":
        f, a = show_term(t[1]), show_term(t[2])
        if t[1][0] in ("lam", "case"):
            f = f"({f})"
        if t[2][0] not in ("v", "pair"):
            a = f"({a})"
        return f"{f} {a}"
    if op == "pair":
        return f"⟨{show_term(t[1])}, {show_term(t[2])}⟩"
    if op in ("fst", "snd", "inl", "inr"):
        a = show_term(t[1])
        return f"{op} {a}" if t[1][0] in ("v", "pair") else f"{op} ({a})"
    if op == "case":
        return f"case {show_term(t[1])} of {t[2]} ⇒ {show_term(t[3])} | {t[4]} ⇒ {show_term(t[5])}"
    if op == "abort":
        return f"abort ({show_term(t[1])})"
    raise ValueError(t)


def rename(t, names: str = "xyzuvwpqrs"):
    """The same term with its bound variables renamed x, y, z, ... in the order they are bound."""
    supply = iter(names)
    def go(t, env):
        op = t[0]
        if op == "v":
            return ("v", env.get(t[1], t[1]))
        if op == "lam":
            n = next(supply)
            return ("lam", n, t[2], go(t[3], {**env, t[1]: n}))
        if op == "case":
            s = go(t[1], env)
            a = next(supply)
            l = go(t[3], {**env, t[2]: a})
            b = next(supply)
            return ("case", s, a, l, b, go(t[5], {**env, t[4]: b}))
        if op in ("inl", "inr", "abort"):
            return (op, go(t[1], env), t[2])
        return (op, *[go(a, env) for a in t[1:]])
    return go(t, {})


# ---------------------------------------------------------------------------
# Proof search: a proof is a program
# ---------------------------------------------------------------------------
def prove(goal, max_depth: int = 7):
    """Search for a closed term of the given type (an intuitionistic natural-deduction proof). Returns the term,
    or None if none is found within the depth bound."""
    names = (f"x{i}" for i in itertools.count())

    def spine(ty, target):
        """If ty = A1 -> ... -> An -> target, the list [A1..An]."""
        args = []
        while True:
            if ty == target:
                return args
            if ty[0] != "->":
                return None
            args.append(ty[1])
            ty = ty[2]

    def search(ctx, goal, depth, seen):
        key = (frozenset(t for _, t in ctx), goal)
        if depth < 0 or key in seen:
            return None
        seen = seen | {key}
        # introduction rules first, when they are invertible
        if goal[0] == "->":
            x = next(names)
            body = search(ctx + [(("v", x), goal[1])], goal[2], depth - 1, seen)
            return None if body is None else ("lam", x, goal[1], body)
        if goal[0] == "&":
            a = search(ctx, goal[1], depth - 1, seen)
            b = a and search(ctx, goal[2], depth - 1, seen)
            return None if b is None else ("pair", a, b)
        # decompose conjunctions in the context
        for i, (tm, ty) in enumerate(ctx):
            if ty[0] == "&":
                new = ctx[:i] + ctx[i + 1:] + [(("fst", tm), ty[1]), (("snd", tm), ty[2])]
                return search(new, goal, depth, seen - {key})
        for tm, ty in ctx:
            if ty == goal:
                return tm
        for tm, ty in ctx:
            if ty == BOT:
                return ("abort", tm, goal)
        # eliminate implications whose conclusion is the goal (or bottom)
        for target in (goal, BOT):
            for tm, ty in ctx:
                args = spine(ty, target)
                if args:
                    out = tm
                    for a in args:
                        sub = search(ctx, a, depth - 1, seen)
                        if sub is None:
                            break
                        out = ("app", out, sub)
                    else:
                        return out if target == goal else ("abort", out, goal)
        # case analysis on disjunctions
        for i, (tm, ty) in enumerate(ctx):
            if ty[0] == "|":
                rest = ctx[:i] + ctx[i + 1:]
                x, y = next(names), next(names)
                l = search(rest + [(("v", x), ty[1])], goal, depth - 1, seen)
                r = l and search(rest + [(("v", y), ty[2])], goal, depth - 1, seen)
                if r is not None:
                    return ("case", tm, x, l, y, r)
        if goal[0] == "|":
            a = search(ctx, goal[1], depth - 1, seen)
            if a is not None:
                return ("inl", a, goal[2])
            b = search(ctx, goal[2], depth - 1, seen)
            if b is not None:
                return ("inr", b, goal[1])
        return None

    return search([], goal, max_depth, frozenset())


# ---------------------------------------------------------------------------
# Kripke countermodels for intuitionistic logic (Part 5)
# ---------------------------------------------------------------------------
def _atoms(t):
    if t[0] == "var":
        return {t[1]}
    if t[0] == "bot":
        return set()
    return _atoms(t[1]) | _atoms(t[2])


def forces(w, t, up, val):
    op = t[0]
    if op == "var":
        return t[1] in val[w]
    if op == "bot":
        return False
    if op == "&":
        return forces(w, t[1], up, val) and forces(w, t[2], up, val)
    if op == "|":
        return forces(w, t[1], up, val) or forces(w, t[2], up, val)
    return all((not forces(v, t[1], up, val)) or forces(v, t[2], up, val) for v in up[w])


def countermodel(t, max_worlds: int = 3):
    """A rooted Kripke model (worlds 0..n-1, a tree order, monotone valuation) whose root does not force t."""
    atoms = sorted(_atoms(t))
    for n in range(1, max_worlds + 1):
        for parents in itertools.product(*[range(i) for i in range(1, n)]):
            par = (None,) + parents
            up = {w: {w} for w in range(n)}
            for w in range(n - 1, -1, -1):
                for v in range(n):
                    x = v
                    while x is not None:
                        if x == w:
                            up[w].add(v)
                        x = par[x]
            for bits in itertools.product((0, 1), repeat=n * len(atoms)):
                val = {w: {a for k, a in enumerate(atoms) if bits[w * len(atoms) + k]} for w in range(n)}
                if not all(val[w] <= val[v] for w in range(n) for v in up[w]):
                    continue
                if not forces(0, t, up, val):
                    return {"worlds": n, "parent": list(par), "val": {w: sorted(val[w]) for w in range(n)}}
    return None


EXAMPLES = [
    ("A -> B -> A", "K"),
    ("(A -> B -> C) -> (A -> B) -> A -> C", "S"),
    ("A & B -> B & A", "swap"),
    ("(A & B -> C) -> A -> B -> C", "curry"),
    ("(A -> C) -> (B -> C) -> A | B -> C", "cases"),
    ("A -> ~~A", "double negation in"),
    ("~~(A | ~A)", "excluded middle, doubly negated"),
    ("A | ~A", "excluded middle"),
    ("((A -> B) -> A) -> A", "Peirce's law"),
    ("~~A -> A", "double negation out"),
]


# ---------------------------------------------------------------------------
# Normalization: running a proof removes its detours
# ---------------------------------------------------------------------------
def _free(t) -> set:
    op = t[0]
    if op == "v":
        return {t[1]}
    if op == "lam":
        return _free(t[3]) - {t[1]}
    if op == "case":
        return _free(t[1]) | (_free(t[3]) - {t[2]}) | (_free(t[5]) - {t[4]})
    out = set()
    for x in t[1:]:
        if isinstance(x, tuple) and x and isinstance(x[0], str) and x[0] in _OPS:
            out |= _free(x)
    return out


_OPS = {"v", "lam", "app", "pair", "fst", "snd", "inl", "inr", "case", "abort"}
_fresh = (f"z{i}" for i in itertools.count())


def subst(t, x: str, s):
    """t with s put for the free occurrences of x (renaming bound variables when they would capture)."""
    op = t[0]
    if op == "v":
        return s if t[1] == x else t
    if op == "lam":
        y, ty, body = t[1], t[2], t[3]
        if y == x:
            return t
        if y in _free(s):
            z = next(_fresh)
            body, y = subst(body, y, ("v", z)), z
        return ("lam", y, ty, subst(body, x, s))
    if op == "case":
        sc, y, l, w, r = t[1:]
        l = l if y == x else subst(l, x, s)
        r = r if w == x else subst(r, x, s)
        return ("case", subst(sc, x, s), y, l, w, r)
    if op in ("inl", "inr", "abort"):
        return (op, subst(t[1], x, s), t[2])
    return (op, *[subst(a, x, s) for a in t[1:]])


def step(t):
    """One leftmost reduction step, or None if t is normal. Each step removes a detour: an introduction rule
    followed at once by the matching elimination."""
    op = t[0]
    if op == "app" and t[1][0] == "lam":
        return subst(t[1][3], t[1][1], t[2])
    if op in ("fst", "snd") and t[1][0] == "pair":
        return t[1][1] if op == "fst" else t[1][2]
    if op == "case" and t[1][0] in ("inl", "inr"):
        _, s, x, l, y, r = t
        return subst(l, x, s[1]) if s[0] == "inl" else subst(r, y, s[1])
    kids = list(t)
    for i, k in enumerate(kids[1:], 1):
        if isinstance(k, tuple) and k and isinstance(k[0], str) and k[0] in _OPS:
            r = step(k)
            if r is not None:
                kids[i] = r
                return tuple(kids)
    return None


def normalize(t, limit: int = 100) -> list:
    """The reduction sequence from t to its normal form (simply typed terms always reach one)."""
    seq = [t]
    while len(seq) <= limit:
        n = step(seq[-1])
        if n is None:
            return seq
        seq.append(n)
    raise RuntimeError("no normal form within the limit")


# ---------------------------------------------------------------------------
# Transport: two presentations of the natural numbers
# ---------------------------------------------------------------------------
def unary(n: int) -> str:
    return "S" * n + "0"


def binary(n: int) -> str:
    return format(n, "b")


def unary_to_binary(u: str) -> str:
    return binary(u.count("S"))


def binary_to_unary(b: str) -> str:
    return unary(int(b, 2))


def succ_unary(u: str) -> str:
    return "S" + u


def succ_binary(b: str) -> str:
    """Binary successor by carrying, without converting to an int."""
    bits = list(b)
    i = len(bits) - 1
    while i >= 0 and bits[i] == "1":
        bits[i] = "0"
        i -= 1
    if i < 0:
        return "1" + "".join(bits)
    bits[i] = "1"
    return "".join(bits)


def even_unary(u: str) -> bool:
    """Defined by recursion on the unary presentation: even(0), and even(S n) iff not even(n)."""
    v = True
    for ch in u[:-1]:
        v = not v
    return v


def transport_check(n: int = 64) -> dict:
    """The maps between the presentations are inverse and respect successor (an equivalence); so a property defined
    on one presentation transports to the other, where it can be computed differently (the last bit)."""
    inverse = all(binary_to_unary(unary_to_binary(unary(k))) == unary(k) for k in range(n))
    respects = all(unary_to_binary(succ_unary(unary(k))) == succ_binary(binary(k)) for k in range(n))
    agree = all(even_unary(binary_to_unary(binary(k))) == (binary(k)[-1] == "0") for k in range(n))
    return {"inverse": inverse, "respects_successor": respects, "even_is_last_bit_zero": agree, "checked": n}


# ---------------------------------------------------------------------------
# Loops on a circle: the fundamental group is the integers
# ---------------------------------------------------------------------------
def winding_number(angles) -> int:
    """For a closed path given by successive angles (radians, steps of less than pi), the net number of turns."""
    import math
    total = 0.0
    for a, b in zip(angles, angles[1:]):
        d = (b - a + math.pi) % (2 * math.pi) - math.pi
        total += d
    return round(total / (2 * math.pi))


def loop_path(turns: int, wobble: float = 0.0, samples: int = 200) -> list:
    import math
    return [2 * math.pi * turns * k / samples + wobble * math.sin(6 * math.pi * k / samples) for k in range(samples + 1)]
