"""First-order logic, small and exact: formulas, finite structures, Tarski satisfaction, a model finder, and a
tableau prover that returns a countermodel when the proof fails.

    from explainer.philosophy.reasoner.fol import parse, Structure, holds, find_model, prove
    f = parse("forall x exists y L(x, y)")
    M = Structure(range(3), {"L": {(0, 1), (1, 2), (2, 0)}})
    holds(f, M)                                   # True
    prove([parse("forall x (H(x) -> A(x))")], parse("forall x ((exists y (Hd(x,y) & H(y))) -> exists y (Hd(x,y) & A(y)))"))

Formulas are tuples:

    ("P", name, (t1, ..., tn))      ("=", t1, t2)       ("not", A)   ("and", A, B)  ("or", A, B)  ("imp", A, B)
    ("iff", A, B)   ("all", x, A)   ("ex", x, A)        ("top",) ("bot",)

Terms are variables or constants (strings) or function applications ("f", name, (t1, ...)). In the parser, a name
bound by a quantifier is a variable; any other lower-case name is a constant; Capitalized names applied to
arguments are predicates; lower-case names applied to arguments are functions.
"""

from __future__ import annotations

import itertools
import re
from dataclasses import dataclass, field

_TOK = re.compile(r"\s*(forall|exists|∀|∃|<->|->|↔|→|¬|~|∧|&|∨|\||\(|\)|,|=|⊤|⊥|[A-Za-z_][A-Za-z0-9_']*)")
_BIN = {"<->": "iff", "↔": "iff", "->": "imp", "→": "imp", "∧": "and", "&": "and", "∨": "or", "|": "or"}
_PREC = {"iff": 1, "imp": 2, "or": 3, "and": 4}


def parse(s: str):
    toks, pos = [], 0
    s = s.strip()
    while pos < len(s):
        m = _TOK.match(s, pos)
        if not m:
            raise ValueError(f"cannot parse {s!r} at {pos}")
        toks.append(m.group(1))
        pos = m.end()
        while pos < len(s) and s[pos].isspace():
            pos += 1
    i = 0

    def peek(k=0):
        return toks[i + k] if i + k < len(toks) else None

    def eat(t=None):
        nonlocal i
        x = toks[i]
        if t is not None and x != t:
            raise ValueError(f"expected {t!r}, got {x!r} in {s!r}")
        i += 1
        return x

    def term(bound):
        name = eat()
        if peek() == "(":
            eat("(")
            args = [term(bound)]
            while peek() == ",":
                eat(",")
                args.append(term(bound))
            eat(")")
            return ("f", name, tuple(args))
        return name

    def atom(bound):
        t = peek()
        if t in ("¬", "~"):
            eat()
            return ("not", atom(bound))
        if t in ("forall", "∀", "exists", "∃"):
            eat()
            v = eat()
            body = atom(bound | {v}) if peek() != "(" else atom(bound | {v})
            return ("all" if t in ("forall", "∀") else "ex", v, body)
        if t == "(":
            eat("(")
            e = expr(0, bound)
            eat(")")
            return e
        if t == "⊤":
            eat()
            return ("top",)
        if t == "⊥":
            eat()
            return ("bot",)
        # predicate application or equation
        name = t
        if name[0].isupper():
            eat()
            args = []
            if peek() == "(":
                eat("(")
                args = [term(bound)]
                while peek() == ",":
                    eat(",")
                    args.append(term(bound))
                eat(")")
            return ("P", name, tuple(args))
        left = term(bound)
        eat("=")
        right = term(bound)
        return ("=", left, right)

    def expr(min_prec, bound):
        nonlocal i
        left = atom(bound)
        while peek() in _BIN and _PREC[_BIN[peek()]] >= min_prec:
            op = _BIN[eat()]
            right = expr(_PREC[op] if op in ("imp", "iff") else _PREC[op] + 1, bound)
            left = (op, left, right)
        return left

    e = expr(0, frozenset())
    if i != len(toks):
        raise ValueError(f"trailing {toks[i:]} in {s!r}")
    return e


def free_vars(f, bound=frozenset()) -> set:
    op = f[0]
    if op == "P":
        return {v for a in f[2] for v in _term_vars(a)} - bound
    if op == "=":
        return (_term_vars(f[1]) | _term_vars(f[2])) - bound
    if op in ("top", "bot"):
        return set()
    if op == "not":
        return free_vars(f[1], bound)
    if op in ("all", "ex"):
        return free_vars(f[2], bound | {f[1]})
    return free_vars(f[1], bound) | free_vars(f[2], bound)


VARS = re.compile(r"^[u-z][0-9']*$")   # x, y, z, u, v, w (with digits or primes) are variables


def _term_vars(t) -> set:
    if isinstance(t, str):
        return {t} if VARS.match(t) else set()
    return {v for a in t[2] for v in _term_vars(a)}


def show(f, tex: bool = False) -> str:
    sym = {"not": r"\lnot " if tex else "¬", "and": r"\land" if tex else "∧", "or": r"\lor" if tex else "∨",
           "imp": r"\to" if tex else "→", "iff": r"\leftrightarrow" if tex else "↔",
           "all": r"\forall " if tex else "∀", "ex": r"\exists " if tex else "∃"}

    def name(n):
        # in TeX, a multi-letter name (romeo, mother) is upright; a one-letter one (x, a) stays italic
        if tex and len(n) > 1 and not VARS.match(n):
            return rf"\mathrm{{{n}}}"
        return n

    def T(t):
        if isinstance(t, str):
            return name(t)
        return f"{name(t[1])}({', '.join(T(a) for a in t[2])})"

    def go(g, top=True):
        op = g[0]
        if op == "P":
            name = rf"\mathrm{{{g[1]}}}" if tex else g[1]
            return name + (f"({', '.join(T(a) for a in g[2])})" if g[2] else "")
        if op == "=":
            return f"{T(g[1])} = {T(g[2])}"
        if op in ("top", "bot"):
            return (r"\top" if op == "top" else r"\bot") if tex else ("⊤" if op == "top" else "⊥")
        if op == "not":
            inner = go(g[1], False)
            return sym["not"] + (f"({inner})" if g[1][0] in _PREC else inner)
        if op in ("all", "ex"):
            body = go(g[2], False)
            if g[2][0] in _PREC:
                body = f"({body})"
            return f"{sym[op]}{g[1]}\\, {body}" if tex else f"{sym[op]}{g[1]} {body}"
        a, b = go(g[1], False), go(g[2], False)
        if g[1][0] in _PREC and _PREC[g[1][0]] <= _PREC[op]:
            a = f"({a})"
        if g[2][0] in _PREC and _PREC[g[2][0]] < _PREC[op] + (0 if op in ("imp", "iff") else 1):
            b = f"({b})"
        return f"{a} {sym[op]} {b}"

    return go(f)


# ---------------------------------------------------------------------------
# Structures and satisfaction
# ---------------------------------------------------------------------------
@dataclass
class Structure:
    domain: list
    preds: dict = field(default_factory=dict)       # name -> set of tuples
    funcs: dict = field(default_factory=dict)       # name -> dict tuple -> element
    consts: dict = field(default_factory=dict)      # name -> element

    def __post_init__(self):
        self.domain = list(self.domain)


def value(t, M: Structure, g: dict):
    if isinstance(t, str):
        if t in g:
            return g[t]
        if t in M.consts:
            return M.consts[t]
        raise KeyError(f"unassigned term {t}")
    return M.funcs[t[1]][tuple(value(a, M, g) for a in t[2])]


def holds(f, M: Structure, g: dict | None = None, trace: list | None = None) -> bool:
    """Tarski's satisfaction relation M, g |= f. If ``trace`` is a list, each quantifier's evaluation appends
    (formula, assignment, value) so a scene can replay it."""
    g = g or {}
    op = f[0]
    if op == "P":
        r = tuple(value(a, M, g) for a in f[2]) in M.preds.get(f[1], set())
    elif op == "=":
        r = value(f[1], M, g) == value(f[2], M, g)
    elif op == "top":
        r = True
    elif op == "bot":
        r = False
    elif op == "not":
        r = not holds(f[1], M, g, trace)
    elif op == "and":
        r = holds(f[1], M, g, trace) and holds(f[2], M, g, trace)
    elif op == "or":
        r = holds(f[1], M, g, trace) or holds(f[2], M, g, trace)
    elif op == "imp":
        r = (not holds(f[1], M, g, trace)) or holds(f[2], M, g, trace)
    elif op == "iff":
        r = holds(f[1], M, g, trace) == holds(f[2], M, g, trace)
    elif op == "all":
        r = all(holds(f[2], M, {**g, f[1]: d}, trace) for d in M.domain)
    elif op == "ex":
        r = any(holds(f[2], M, {**g, f[1]: d}, trace) for d in M.domain)
    else:
        raise ValueError(op)
    if trace is not None and op in ("all", "ex"):
        trace.append((f, dict(g), r))
    return r


def signature(fs) -> dict:
    """{predicate name: arity}, constants, and functions used by the formulas."""
    preds, consts, funcs = {}, set(), {}

    def T(t, bound):
        if isinstance(t, str):
            if t not in bound and not VARS.match(t):
                consts.add(t)
        else:
            funcs[t[1]] = len(t[2])
            for a in t[2]:
                T(a, bound)

    def go(f, bound):
        op = f[0]
        if op == "P":
            preds[f[1]] = len(f[2])
            for a in f[2]:
                T(a, bound)
        elif op == "=":
            T(f[1], bound)
            T(f[2], bound)
        elif op == "not":
            go(f[1], bound)
        elif op in ("all", "ex"):
            go(f[2], bound | {f[1]})
        elif op in _PREC:
            go(f[1], bound)
            go(f[2], bound)

    for f in fs:
        go(f, frozenset())
    return {"preds": preds, "consts": sorted(consts), "funcs": funcs}


def all_structures(sig: dict, n: int):
    """Every structure on {0, ..., n-1} for a signature without functions (constants allowed)."""
    dom = list(range(n))
    names = sorted(sig["preds"])
    tuples = {p: list(itertools.product(dom, repeat=sig["preds"][p])) for p in names}
    choices = [list(itertools.product((False, True), repeat=len(tuples[p]))) for p in names]
    for consts in itertools.product(dom, repeat=len(sig["consts"])):
        cmap = dict(zip(sig["consts"], consts))
        for combo in itertools.product(*choices):
            preds = {p: {t for t, b in zip(tuples[p], bits) if b} for p, bits in zip(names, combo)}
            yield Structure(dom, preds, {}, cmap)


def find_model(fs, max_size: int = 4, min_size: int = 1):
    """A smallest finite structure satisfying all of ``fs`` (no functions), or None up to ``max_size``."""
    sig = signature(fs)
    if sig["funcs"]:
        raise ValueError("find_model handles predicates and constants only")
    for n in range(min_size, max_size + 1):
        for M in all_structures(sig, n):
            if all(holds(f, M) for f in fs):
                return M
    return None


def countermodel(premises, conclusion, max_size: int = 4):
    return find_model(list(premises) + [("not", conclusion)], max_size)


# ---------------------------------------------------------------------------
# Tableaux
# ---------------------------------------------------------------------------
def subst(f, v, t):
    op = f[0]

    def T(x):
        if isinstance(x, str):
            return t if x == v else x
        return ("f", x[1], tuple(T(a) for a in x[2]))

    if op == "P":
        return ("P", f[1], tuple(T(a) for a in f[2]))
    if op == "=":
        return ("=", T(f[1]), T(f[2]))
    if op in ("top", "bot"):
        return f
    if op == "not":
        return ("not", subst(f[1], v, t))
    if op in ("all", "ex"):
        return f if f[1] == v else (op, f[1], subst(f[2], v, t))
    return (op, subst(f[1], v, t), subst(f[2], v, t))


@dataclass
class TableauResult:
    closed: bool
    steps: list           # (rule, formula shown, branch id) in the order applied
    branches: int
    countermodel: Structure | None = None
    gave_up: bool = False  # an open branch hit the term bound and its atoms are not a model


def prove(premises, conclusion, max_terms: int = 6, max_steps: int = 4000) -> TableauResult:
    """A signed ground tableau (Smullyan): start from the premises and the negated conclusion, decompose, and close
    a branch when it holds a formula and its negation. Universal (gamma) formulas are instantiated with every
    ground term on the branch, new parameters are introduced for existentials (delta). If a branch is exhausted
    without closing, its atoms define a countermodel (Hintikka set), returned with the result. Equality is
    treated as an uninterpreted predicate; functions are not supported (constants are)."""
    start = list(premises) + [("not", conclusion)]
    steps: list = []
    fresh = itertools.count()
    nb = [0]

    def neg(f):
        return f[1] if f[0] == "not" else ("not", f)

    def consts_of(branch):
        cs = set()
        for f in branch:
            cs |= _consts(f)
        return sorted(cs)

    def expand(branch, used_gamma, depth):
        if len(steps) > max_steps:
            raise RuntimeError("tableau step budget exceeded")
        lits = set(branch)
        for f in branch:
            if neg(f) in lits or f == ("bot",) or f == ("not", ("top",)):
                steps.append(("close", f, depth))
                return True, None
        # alpha rules first, then beta, delta, gamma
        for f in branch:
            op = f[0]
            if op == "and" and not {f[1], f[2]} <= lits:
                steps.append(("and", f, depth))
                return expand(branch + [x for x in (f[1], f[2]) if x not in lits], used_gamma, depth)
            if op == "not" and f[1][0] == "not" and f[1][1] not in lits:
                steps.append(("not-not", f, depth))
                return expand(branch + [f[1][1]], used_gamma, depth)
            if op == "not" and f[1][0] == "or" and not {neg(f[1][1]), neg(f[1][2])} <= lits:
                steps.append(("not-or", f, depth))
                return expand(branch + [x for x in (neg(f[1][1]), neg(f[1][2])) if x not in lits], used_gamma, depth)
            if op == "not" and f[1][0] == "imp" and not {f[1][1], neg(f[1][2])} <= lits:
                steps.append(("not-imp", f, depth))
                return expand(branch + [x for x in (f[1][1], neg(f[1][2])) if x not in lits], used_gamma, depth)
            if op == "iff" and not ({f[1], f[2]} <= lits or {neg(f[1]), neg(f[2])} <= lits):
                pass
        for f in branch:
            op = f[0]
            pair = None
            if op == "or":
                pair = (f[1], f[2])
            elif op == "imp":
                pair = (neg(f[1]), f[2])
            elif op == "not" and f[1][0] == "and":
                pair = (neg(f[1][1]), neg(f[1][2]))
            elif op == "iff":
                pair = (("and", f[1], f[2]), ("and", neg(f[1]), neg(f[2])))
            elif op == "not" and f[1][0] == "iff":
                pair = (("and", f[1][1], neg(f[1][2])), ("and", neg(f[1][1]), f[1][2]))
            if pair and not any(p in lits for p in pair):
                steps.append(("split", f, depth))
                nb[0] += 1
                l_ok, l_m = expand(branch + [pair[0]], used_gamma, depth + 1)
                if not l_ok:
                    return False, l_m
                r_ok, r_m = expand(branch + [pair[1]], used_gamma, depth + 1)
                return r_ok, r_m
        for f in branch:
            if f[0] == "ex" or (f[0] == "not" and f[1][0] == "all"):
                v, body = (f[1], f[2]) if f[0] == "ex" else (f[1][1], ("not", f[1][2]))
                # already witnessed?
                if any(subst(body, v, c) in lits for c in consts_of(branch)):
                    continue
                taken = set(consts_of(branch))
                c = f"a{next(fresh)}"
                while c in taken:
                    c = f"a{next(fresh)}"
                steps.append(("new " + c, f, depth))
                return expand(branch + [subst(body, v, c)], used_gamma, depth)
        cs = consts_of(branch)
        if not cs:  # the domain is never empty: start it with one fresh element
            c = f"a{next(fresh)}"
            cs = [c]
        if len(cs) > max_terms:
            return False, _hintikka(branch, cs)
        for f in branch:
            if f[0] == "all" or (f[0] == "not" and f[1][0] == "ex"):
                v, body = (f[1], f[2]) if f[0] == "all" else (f[1][1], ("not", f[1][2]))
                for c in cs:
                    inst = subst(body, v, c)
                    if (f, c) not in used_gamma and inst not in lits:
                        steps.append(("every: " + c, f, depth))
                        return expand(branch + [inst], used_gamma | {(f, c)}, depth)
        return False, _hintikka(branch, cs)

    ok, model = expand(start, frozenset(), 0)
    if ok:
        return TableauResult(True, steps, nb[0] + 1)
    if model is not None and all(holds(f, model) for f in start):
        return TableauResult(False, steps, nb[0] + 1, model)
    return TableauResult(False, steps, nb[0] + 1, None, gave_up=True)


def _consts(f) -> set:
    op = f[0]
    if op == "P":
        return {a for a in f[2] if isinstance(a, str) and not VARS.match(a)}
    if op == "=":
        return {a for a in (f[1], f[2]) if isinstance(a, str) and not VARS.match(a)}
    if op == "not":
        return _consts(f[1])
    if op in ("all", "ex"):
        return {c for c in _consts(f[2]) if c != f[1]}
    if op in _PREC:
        return _consts(f[1]) | _consts(f[2])
    return set()


def _hintikka(branch, cs) -> Structure:
    """The model an open branch describes: its constants are the domain, its positive atoms are true."""
    preds: dict = {}
    for f in branch:
        if f[0] == "P":
            preds.setdefault(f[1], set()).add(tuple(f[2]))
    return Structure(list(cs), preds, {}, {c: c for c in cs})


# ---------------------------------------------------------------------------
# Natural deduction, checked
# ---------------------------------------------------------------------------
def _terms(f) -> set:
    """Every term occurring in a formula (subterms included)."""
    out: set = set()

    def T(t):
        out.add(t)
        if not isinstance(t, str):
            for a in t[2]:
                T(a)

    def go(g):
        op = g[0]
        if op == "P":
            for a in g[2]:
                T(a)
        elif op == "=":
            T(g[1])
            T(g[2])
        elif op == "not":
            go(g[1])
        elif op in ("all", "ex"):
            go(g[2])
        elif op in _PREC:
            go(g[1])
            go(g[2])

    go(f)
    return out


def _bound(f) -> set:
    op = f[0]
    if op == "not":
        return _bound(f[1])
    if op in ("all", "ex"):
        return {f[1]} | _bound(f[2])
    if op in _PREC:
        return _bound(f[1]) | _bound(f[2])
    return set()


def _instance_of(body, x, f) -> bool:
    """Is ``f`` the result of putting some term, free for ``x``, in place of ``x`` in ``body``?"""
    if x not in free_vars(body):
        return f == body
    for t in _terms(f):
        if _term_vars(t) & _bound(body):
            continue                         # the term would be captured: not free for x
        if subst(body, x, t) == f:
            return True
    return False


def check_fitch(lines, premises=None, goal=None) -> tuple[bool, str]:
    """Check a Fitch-style natural deduction proof in first-order logic.

    ``lines`` as for :func:`prop.check_fitch`: ``(depth, formula_text, rule, refs)``, refs 1-based, a subproof cited
    as ``(start, end)``. The propositional rules of ``prop.check_fitch``, and for the quantifiers:
    allE (∀xφ ⊢ φ[t/x], t free for x), exI (φ[t/x] ⊢ ∃xφ), allI (φ[a/x] ⊢ ∀xφ, where the constant a occurs in no
    premise, no open assumption, and not in ∀xφ), exE (∃xφ, and a subproof from φ[a/x] to ψ ⊢ ψ, where a is new:
    not in ∃xφ, ψ, the premises or any assumption still open), and eqI (t = t). Returns (ok, message)."""
    parsed = [(d, parse(t), r, refs) for d, t, r, refs in lines]
    prem_fs = [parse(p) for p in premises] if premises is not None else [f for d, f, r, _ in parsed if r == "premise"]
    open_starts: list[int] = []
    scope: list[tuple[int, ...]] = []
    for i, (d, f, r, refs) in enumerate(parsed):
        if r == "assume":
            while len(open_starts) >= d:
                open_starts.pop()
            open_starts.append(i)
        else:
            while len(open_starts) > d:
                open_starts.pop()
        if len(open_starts) != d:
            return False, f"line {i + 1}: depth {d} without an assumption opening it"
        scope.append(tuple(open_starts))

    def accessible(i, j):
        return j < i and all(s in scope[i] for s in scope[j])

    def subproof(i, se):
        s, e = se[0] - 1, se[1] - 1
        if not (0 <= s <= e < i) or parsed[s][2] != "assume":
            return None
        if s not in scope[e] or s in scope[i]:
            return None
        if not all(x in scope[i] for x in scope[s][:-1]):
            return None
        return parsed[s][1], parsed[e][1]

    def fresh(c, i, *fs):
        """The constant c occurs in no premise, no assumption open at line i, and none of fs."""
        if VARS.match(c):
            return False
        open_assumptions = [parsed[s][1] for s in scope[i]]
        return all(c not in _consts(g) for g in [*prem_fs, *open_assumptions, *fs])

    for i, (d, f, r, refs) in enumerate(parsed):
        ok, why = False, ""
        R = [x - 1 if isinstance(x, int) else x for x in refs]
        ints = [x for x in R if isinstance(x, int)]
        if any(not accessible(i, j) for j in ints):
            return False, f"line {i + 1}: cites a line that is not accessible"
        g = lambda k: parsed[R[k]][1]  # noqa: E731
        try:
            if r == "premise":
                ok = d == 0 and f in prem_fs
            elif r == "assume":
                ok = True
            elif r == "reit":
                ok = g(0) == f
            elif r == "andI":
                ok = f == ("and", g(0), g(1))
            elif r == "andE":
                ok = g(0)[0] == "and" and f in (g(0)[1], g(0)[2])
            elif r == "orI":
                ok = f[0] == "or" and g(0) in (f[1], f[2])
            elif r == "orE":
                dis, a, b = g(0), subproof(i, refs[1]), subproof(i, refs[2])
                ok = (dis[0] == "or" and a and b and {a[0], b[0]} == {dis[1], dis[2]} and a[1] == f and b[1] == f)
            elif r == "impI":
                a = subproof(i, refs[0])
                ok = bool(a) and f == ("imp", a[0], a[1])
            elif r == "impE":
                ok = g(0)[0] == "imp" and g(0)[1] == g(1) and g(0)[2] == f
            elif r == "notI":
                a = subproof(i, refs[0])
                ok = bool(a) and a[1] == ("bot",) and f == ("not", a[0])
            elif r == "notE":
                ok = f == ("bot",) and (g(1) == ("not", g(0)) or g(0) == ("not", g(1)))
            elif r == "botE":
                ok = g(0) == ("bot",)
            elif r == "dne":
                ok = g(0) == ("not", ("not", f))
            elif r == "allE":
                ok = g(0)[0] == "all" and _instance_of(g(0)[2], g(0)[1], f)
            elif r == "exI":
                ok = f[0] == "ex" and _instance_of(f[2], f[1], g(0))
            elif r == "eqI":
                ok = f[0] == "=" and f[1] == f[2]
            elif r == "allI":
                ok = False
                if f[0] == "all":
                    x, body = f[1], f[2]
                    cands = [c for c in _consts(g(0)) if subst(body, x, c) == g(0)]
                    if x not in free_vars(body):
                        ok, why = g(0) == body, ""
                    elif not cands:
                        why = "it is not an instance"
                    else:
                        ok = any(fresh(c, i, f) for c in cands)
                        if not ok:
                            why = f"{cands[0]} is not arbitrary: it occurs in a premise or an open assumption"
            elif r == "exE":
                ex = g(0)
                a = subproof(i, refs[1])
                ok = False
                if ex[0] == "ex" and a and a[1] == f:
                    x, body = ex[1], ex[2]
                    cands = [c for c in _consts(a[0]) if subst(body, x, c) == a[0]]
                    ok = any(fresh(c, i, ex, f) for c in cands)
                    if not ok and cands:
                        why = f"{cands[0]} is not new"
        except (IndexError, TypeError):
            ok = False
        if not ok:
            return False, f"line {i + 1}: {r} does not justify {show(f)}" + (f" ({why})" if why else "")
    if goal is not None:
        last = parsed[-1]
        if last[0] != 0 or last[1] != parse(goal):
            return False, "the proof does not end with the goal at depth 0"
    return True, "valid"


# ---------------------------------------------------------------------------
# Unification and resolution (Robinson 1965)
# ---------------------------------------------------------------------------
def _walk(t, s):
    while isinstance(t, str) and t in s:
        t = s[t]
    return t


def _occurs(v, t, s) -> bool:
    t = _walk(t, s)
    if isinstance(t, str):
        return t == v
    return any(_occurs(v, a, s) for a in t[2])


def resolve_term(t, s):
    """Apply a substitution (a triangular one, as unify builds it) fully to a term."""
    t = _walk(t, s)
    if isinstance(t, str):
        return t
    return ("f", t[1], tuple(resolve_term(a, s) for a in t[2]))


def unify(a, b, s=None, trace=None):
    """A most general unifier of two terms or atoms (variables match VARS), extending ``s``; None if there is none.
    With ``trace`` a list, each binding is appended as (variable, term) in the order it was made; a failed occurs
    check appends ("occurs", variable, term)."""
    s = dict(s or {})
    stack = [(a, b)]
    while stack:
        x, y = stack.pop()
        if isinstance(x, tuple) and x and x[0] == "P":
            if not (isinstance(y, tuple) and y[0] == "P" and x[1] == y[1] and len(x[2]) == len(y[2])):
                return None
            stack.extend(reversed(list(zip(x[2], y[2]))))
            continue
        x, y = _walk(x, s), _walk(y, s)
        if x == y:
            continue
        if isinstance(x, str) and VARS.match(x):
            if _occurs(x, y, s):
                if trace is not None:
                    trace.append(("occurs", x, resolve_term(y, s)))
                return None
            s[x] = y
            if trace is not None:
                trace.append((x, y))
        elif isinstance(y, str) and VARS.match(y):
            stack.append((y, x))
        elif isinstance(x, tuple) and isinstance(y, tuple) and x[1] == y[1] and len(x[2]) == len(y[2]):
            stack.extend(reversed(list(zip(x[2], y[2]))))
        else:
            return None
    return s


def _sub_atom(atom, s):
    return ("P", atom[1], tuple(resolve_term(a, s) for a in atom[2]))


def _rename(clause, k):
    """Fresh variables for a clause: x becomes x_k."""
    def T(t):
        if isinstance(t, str):
            return f"{t}{k}" if VARS.match(t) else t
        return ("f", t[1], tuple(T(a) for a in t[2]))
    return frozenset((sg, ("P", at[1], tuple(T(a) for a in at[2]))) for sg, at in clause)


def parse_clause(s: str) -> frozenset:
    """'~L(x, y) | L(z, x)' -> frozenset of (positive?, atom). Free lower-case names u-z are variables."""
    lits = []
    for part in s.split("|"):
        part = part.strip()
        neg = part.startswith("~") or part.startswith("¬")
        f = parse(part.lstrip("~¬").strip())
        lits.append((not neg, f))
    return frozenset(lits)


def show_clause(c) -> str:
    if not c:
        return "□"
    return " ∨ ".join(("" if sg else "¬") + show(at) for sg, at in sorted(c, key=lambda l: (show(l[1]), l[0])))


def resolution(clauses, max_steps: int = 2000):
    """Refute a set of first-order clauses by binary resolution with factoring (given-clause loop, shortest
    clauses first). Returns (refuted, derivation): derivation lists (clause, parent_i, parent_j, unifier) for every
    derived clause, numbered after the input clauses; the empty clause last when refuted."""
    kept = [frozenset(c) for c in clauses]
    info = [None] * len(kept)
    seen = {c for c in kept}
    derived = []
    usable: list[int] = []
    queue = list(range(len(kept)))
    k = 0
    while queue and k < max_steps:
        queue.sort(key=lambda i: (len(kept[i]), i))
        gi = queue.pop(0)
        given = kept[gi]
        for ui in usable + [gi]:
            other = _rename(kept[ui], k + 1)
            k += 1
            for sg1, a1 in given:
                for sg2, a2 in other:
                    if sg1 == sg2:
                        continue
                    s = unify(a1, a2)
                    if s is None:
                        continue
                    res = frozenset((sg, _sub_atom(at, s)) for sg, at in (given - {(sg1, a1)}) | (other - {(sg2, a2)}))
                    if any((not sg, at) in res for sg, at in res):
                        continue                      # a tautology
                    key = _canon(res)
                    if key in seen:
                        continue
                    seen.add(key)
                    kept.append(res)
                    info.append((gi, ui, {v: resolve_term(t, s) for v, t in s.items()}))
                    derived.append(len(kept) - 1)
                    queue.append(len(kept) - 1)
                    if not res:
                        return True, [(kept[i], *info[i]) for i in derived]
        usable.append(gi)
    return False, [(kept[i], *info[i]) for i in derived]


def _canon(c) -> frozenset:
    """A clause with its variables renamed in order of appearance, so variants count as the same clause."""
    names: dict = {}

    def T(t):
        if isinstance(t, str):
            if VARS.match(t):
                names.setdefault(t, f"v{len(names)}")
                return names[t]
            return t
        return ("f", t[1], tuple(T(a) for a in t[2]))
    out = []
    for sg, at in sorted(c, key=lambda l: (l[0], show(l[1]))):
        out.append((sg, ("P", at[1], tuple(T(a) for a in at[2]))))
    return frozenset(out)


def resolution_proof(clauses, derivation):
    """The part of a refutation that the empty clause depends on: [(number, clause, parents, unifier)], input
    clauses first (numbered 1..), then each needed resolvent, renumbered in order; variables renamed x, y, z, ..."""
    n = len(clauses)
    allc = [frozenset(c) for c in clauses] + [d[0] for d in derivation]
    parents = {n + i: (d[1], d[2]) for i, d in enumerate(derivation)}
    unif = {n + i: d[3] for i, d in enumerate(derivation)}
    need, stack = set(), [len(allc) - 1]
    while stack:
        i = stack.pop()
        if i in need:
            continue
        need.add(i)
        if i in parents:
            stack.extend(parents[i])
    order = sorted(need)
    num = {i: k + 1 for k, i in enumerate(order)}

    def pretty(c):
        names: dict = {}
        letters = iter("xyzuvw")

        def T(t):
            if isinstance(t, str):
                if VARS.match(t):
                    if t not in names:
                        names[t] = next(letters)
                    return names[t]
                return t
            return ("f", t[1], tuple(T(a) for a in t[2]))
        return frozenset((sg, ("P", at[1], tuple(T(a) for a in at[2]))) for sg, at in c)

    out = []
    for i in order:
        ps = tuple(num[p] for p in parents[i]) if i in parents else ()
        u = {}
        if i in unif:
            for v, t in unif[i].items():
                tt = resolve_term(t, {})
                if not (isinstance(tt, str) and VARS.match(tt)):
                    u[re.sub(r"\d+$", "", v)] = show(("P", "_", (tt,)))[2:-1]
        out.append((num[i], show_clause(pretty(allc[i])), ps, u))
    return out
