"""Semantics (Part 58), computed.  One small call-by-value language with recursion (PCF-like: integers, booleans,
functions, fix) given three operational semantics that must agree: small-step reduction, a big-step evaluator, and a
CEK machine (Felleisen and Friedman 1986).  The Kleene chain of the factorial functional; normalization by
evaluation for the untyped lambda calculus on Church numerals; free theorems (Wadler 1989) checked by property
tests; strong bisimilarity by partition refinement (Kanellakis and Smolka 1983; Paige and Tarjan 1987), with the
classic pair that has the same traces but is not bisimilar; and three effects as monads.  After Winskel, *The
Formal Semantics of Programming Languages*, and Harper, *Practical Foundations for Programming Languages*."""

from __future__ import annotations

import random
from dataclasses import dataclass

# ---------------------------------------------------------------- the language
# terms: ("int", n) ("bool", b) ("var", x) ("lam", x, body) ("app", f, a) ("fix", f, x, body)  [fix f(x) = body]
#        ("if", c, t, e) ("op", o, a, b) with o in + - * < =


def show(t) -> str:
    k = t[0]
    if k == "int":
        return str(t[1])
    if k == "bool":
        return "true" if t[1] else "false"
    if k == "var":
        return t[1]
    if k == "lam":
        return f"(fun {t[1]} -> {show(t[2])})"
    if k == "fix":
        return f"(fix {t[1]} {t[2]} -> {show(t[3])})"
    if k == "app":
        return f"({show(t[1])} {show(t[2])})"
    if k == "if":
        return f"(if {show(t[1])} then {show(t[2])} else {show(t[3])})"
    if k == "op":
        return f"({show(t[2])} {t[1]} {show(t[3])})"
    if k == "clo":
        return "<closure>"
    raise ValueError(k)


def _prim(o, a, b):
    return {"+": lambda: a + b, "-": lambda: a - b, "*": lambda: a * b, "<": lambda: a < b,
            "=": lambda: a == b}[o]()


def is_value(t) -> bool:
    return t[0] in ("int", "bool", "lam", "fix")


def free_vars(t):
    k = t[0]
    if k in ("int", "bool"):
        return set()
    if k == "var":
        return {t[1]}
    if k == "lam":
        return free_vars(t[2]) - {t[1]}
    if k == "fix":
        return free_vars(t[3]) - {t[1], t[2]}
    children = t[1:] if k in ("app", "if") else t[2:] if k == "op" else None
    if children is None:
        raise ValueError(k)
    return set().union(*(free_vars(c) for c in children))


def _fresh(name, used):
    i = 0
    while f"{name}_{i}" in used:
        i += 1
    return f"{name}_{i}"


def subst(t, x, v):
    """Capture-avoiding substitution, including open function values."""
    k = t[0]
    if k in ("int", "bool"):
        return t
    if k == "var":
        return v if t[1] == x else t
    if k == "lam":
        name, body = t[1:]
        if name == x or x not in free_vars(body):
            return t
        if name in free_vars(v):
            fresh = _fresh(name, free_vars(body) | free_vars(v) | {x})
            body, name = subst(body, name, ("var", fresh)), fresh
        return ("lam", name, subst(body, x, v))
    if k == "fix":
        names, body = list(t[1:3]), t[3]
        if x in names or x not in free_vars(body):
            return t
        for name in dict.fromkeys(names):
            if name in free_vars(v):
                fresh = _fresh(name, free_vars(body) | free_vars(v) | set(names) | {x})
                body = subst(body, name, ("var", fresh))
                names = [fresh if n == name else n for n in names]
        return ("fix", *names, subst(body, x, v))
    if k == "app":
        return ("app", subst(t[1], x, v), subst(t[2], x, v))
    if k == "if":
        return ("if", subst(t[1], x, v), subst(t[2], x, v), subst(t[3], x, v))
    if k == "op":
        return ("op", t[1], subst(t[2], x, v), subst(t[3], x, v))
    raise ValueError(k)


def step(t):
    """One small step (call by value, left to right), or None if t is a value or stuck."""
    k = t[0]
    if k == "app":
        f, a = t[1], t[2]
        if not is_value(f):
            s = step(f)
            return None if s is None else ("app", s, a)
        if not is_value(a):
            s = step(a)
            return None if s is None else ("app", f, s)
        if f[0] == "lam":
            return subst(f[2], f[1], a)
        if f[0] == "fix":
            return subst(subst(f[3], f[1], f), f[2], a)
        return None
    if k == "if":
        c = t[1]
        if not is_value(c):
            s = step(c)
            return None if s is None else ("if", s, t[2], t[3])
        return t[2] if c[1] else t[3]
    if k == "op":
        a, b = t[2], t[3]
        if not is_value(a):
            s = step(a)
            return None if s is None else ("op", t[1], s, b)
        if not is_value(b):
            s = step(b)
            return None if s is None else ("op", t[1], a, s)
        r = _prim(t[1], a[1], b[1])
        return ("bool", r) if isinstance(r, bool) else ("int", r)
    return None


def small(t, limit: int = 200_000):
    trace = [t]
    n = 0
    while not is_value(t):
        s = step(t)
        if s is None:
            raise RuntimeError("stuck")
        t = s
        n += 1
        if len(trace) < 40:
            trace.append(t)
        if n > limit:
            raise RuntimeError("no value within the limit")
    return t, n, trace


def _val(v):
    """A comparable view of a value: integers and booleans as themselves, functions as 'fun'."""
    if v[0] in ("int", "bool"):
        return v[1]
    return "fun"


def big(t, env=None):
    """Big-step evaluation with environments; functions become closures."""
    env = env or {}
    k = t[0]
    if k in ("int", "bool"):
        return t
    if k == "var":
        return env[t[1]]
    if k == "lam":
        return ("clo", t[1], t[2], env, None)
    if k == "fix":
        return ("clo", t[2], t[3], env, t[1])
    if k == "app":
        f = big(t[1], env)
        a = big(t[2], env)
        _, x, body, cenv, self_name = f
        e2 = dict(cenv)
        if self_name:
            e2[self_name] = f
        e2[x] = a
        return big(body, e2)
    if k == "if":
        return big(t[2], env) if big(t[1], env)[1] else big(t[3], env)
    if k == "op":
        a, b = big(t[2], env), big(t[3], env)
        r = _prim(t[1], a[1], b[1])
        return ("bool", r) if isinstance(r, bool) else ("int", r)
    raise ValueError(k)


def cek(t, limit: int = 2_000_000):
    """The CEK machine: a Control term, an Environment, and a continuation K as an explicit stack."""
    C, E, K = t, {}, []
    steps = 0
    while True:
        steps += 1
        if steps > limit:
            raise RuntimeError("limit")
        k = C[0]
        if k != "VAL":
            if k in ("int", "bool"):
                C = ("VAL", C)
            elif k == "var":
                C = ("VAL", E[C[1]])
            elif k == "lam":
                C = ("VAL", ("clo", C[1], C[2], E, None))
            elif k == "fix":
                C = ("VAL", ("clo", C[2], C[3], E, C[1]))
            elif k == "app":
                K.append(("arg", C[2], E))
                C = C[1]
            elif k == "if":
                K.append(("if", C[2], C[3], E))
                C = C[1]
            elif k == "op":
                K.append(("opr", C[1], C[3], E))
                C = C[2]
            continue
        v = C[1]
        if not K:
            return v, steps
        fr = K.pop()
        if fr[0] == "arg":
            K.append(("fun", v))
            C, E = fr[1], fr[2]
        elif fr[0] == "fun":
            _, x, body, cenv, self_name = fr[1]
            E = dict(cenv)
            if self_name:
                E[self_name] = fr[1]
            E[x] = v
            C = body
        elif fr[0] == "if":
            C, E = (fr[1] if v[1] else fr[2]), fr[3]
        elif fr[0] == "opr":
            K.append(("opl", fr[1], v))
            C, E = fr[2], fr[3]
        elif fr[0] == "opl":
            r = _prim(fr[1], fr[2][1], v[1])
            C = ("VAL", ("bool", r) if isinstance(r, bool) else ("int", r))


# ---------------------------------------------------------------- random programs

def random_program(rng: random.Random, depth: int = 4):
    """A closed, terminating integer program: arithmetic, conditionals, lambdas applied to arguments, and a bounded
    recursion fix f n -> if n < 1 then e else f (n - 1) + e' applied to a small number."""
    def expr(d, vars_):
        r = rng.random()
        if d == 0 or r < 0.2:
            if vars_ and rng.random() < 0.5:
                return ("var", rng.choice(vars_))
            return ("int", rng.randint(0, 9))
        if r < 0.45:
            return ("op", rng.choice("+-*"), expr(d - 1, vars_), expr(d - 1, vars_))
        if r < 0.6:
            return ("if", ("op", rng.choice("<="), expr(d - 1, vars_), expr(d - 1, vars_)), expr(d - 1, vars_),
                    expr(d - 1, vars_))
        if r < 0.8:
            x = f"x{d}{rng.randint(0, 9)}"
            return ("app", ("lam", x, expr(d - 1, vars_ + [x])), expr(d - 1, vars_))
        f, n = f"f{d}", f"n{d}"
        body = ("if", ("op", "<", ("var", n), ("int", 1)), expr(d - 1, vars_ + [n]),
                ("op", "+", ("app", ("var", f), ("op", "-", ("var", n), ("int", 1))), expr(d - 1, vars_ + [n])))
        return ("app", ("fix", f, n, body), ("int", rng.randint(0, 6)))
    return expr(depth, [])


def agreement(n: int = 300, seed: int = 0) -> dict:
    rng = random.Random(seed)
    agree, steps_s, steps_c, sizes = 0, [], [], []
    example = None
    for i in range(n):
        p = random_program(rng)
        v1, ns, trace = small(p)
        v2 = big(p)
        v3, nc = cek(p)
        if _val(v1) == _val(v2) == _val(v3):
            agree += 1
        steps_s.append(ns)
        steps_c.append(nc)
        sizes.append(len(show(p)))
        if example is None and 6 <= ns <= 14 and len(show(p)) < 90:
            example = {"program": show(p), "trace": [show(t) for t in trace], "value": _val(v1)}
    return {"n": n, "agree": agree, "mean_small_steps": sum(steps_s) / n, "mean_cek_steps": sum(steps_c) / n,
            "example": example}


FACT = ("fix", "fact", "n", ("if", ("op", "=", ("var", "n"), ("int", 0)), ("int", 1),
                              ("op", "*", ("var", "n"), ("app", ("var", "fact"), ("op", "-", ("var", "n"),
                                                                                    ("int", 1))))))


def fact_trace(n: int = 3) -> dict:
    v, steps, trace = small(("app", FACT, ("int", n)))
    return {"n": n, "value": v[1], "steps": steps, "trace": [show(t) for t in trace]}


# ---------------------------------------------------------------- Kleene's chain

def kleene(k_max: int = 7, domain: int = 8) -> list[dict]:
    """F(f)(n) = 1 if n = 0 else n * f(n - 1).  Starting from the everywhere-undefined function, the iterates F^k(bot)
    are defined on 0..k-1 and agree with factorial there: an increasing chain whose least upper bound is factorial,
    the least fixed point of F."""
    rows = []
    f = {}
    for k in range(k_max + 1):
        rows.append({"k": k, "defined": {str(n): f[n] for n in sorted(f)},
                     "table": [f.get(n) for n in range(domain)]})
        g = {}
        for n in range(domain):
            if n == 0:
                g[n] = 1
            elif (n - 1) in f:
                g[n] = n * f[n - 1]
        f = g
    return rows


# ---------------------------------------------------------------- normalization by evaluation

@dataclass(frozen=True)
class Lam:
    body: object


@dataclass(frozen=True)
class App:
    f: object
    a: object


@dataclass(frozen=True)
class Var:
    i: int                      # de Bruijn index


def church(n: int):
    body = Var(0)
    for _ in range(n):
        body = App(Var(1), body)
    return Lam(Lam(body))


PLUS = Lam(Lam(Lam(Lam(App(App(Var(3), Var(1)), App(App(Var(2), Var(1)), Var(0)))))))
TIMES = Lam(Lam(Lam(App(Var(2), App(Var(1), Var(0))))))
EXP = Lam(Lam(App(Var(0), Var(1))))


def nbe(t):
    """Evaluate into Python closures (the semantic domain), then read back a normal form."""
    class N:                    # neutral: a variable at a de Bruijn level applied to arguments
        def __init__(self, lvl, args=()):
            self.lvl, self.args = lvl, args

    def ev(t, env):
        if isinstance(t, Var):
            return env[t.i]
        if isinstance(t, Lam):
            return lambda v, t=t, env=env: ev(t.body, [v] + env)
        f, a = ev(t.f, env), ev(t.a, env)
        return f(a) if callable(f) else N(f.lvl, f.args + (a,))

    def rb(v, depth):
        if callable(v):
            return Lam(rb(v(N(depth)), depth + 1))
        out = Var(depth - v.lvl - 1)
        for a in v.args:
            out = App(out, rb(a, depth))
        return out

    return rb(ev(t, []), 0)


def beta_steps(t, limit: int = 100_000):
    """Normal-order reduction to normal form, counting steps (for comparison with NbE)."""
    def shift(t, d, c=0):
        if isinstance(t, Var):
            return Var(t.i + d) if t.i >= c else t
        if isinstance(t, Lam):
            return Lam(shift(t.body, d, c + 1))
        return App(shift(t.f, d, c), shift(t.a, d, c))

    def sub(t, j, s):
        if isinstance(t, Var):
            return s if t.i == j else t
        if isinstance(t, Lam):
            return Lam(sub(t.body, j + 1, shift(s, 1)))
        return App(sub(t.f, j, s), sub(t.a, j, s))

    def red(t):
        if isinstance(t, App):
            if isinstance(t.f, Lam):
                return shift(sub(t.f.body, 0, shift(t.a, 1)), -1)
            r = red(t.f)
            if r is not None:
                return App(r, t.a)
            r = red(t.a)
            return None if r is None else App(t.f, r)
        if isinstance(t, Lam):
            r = red(t.body)
            return None if r is None else Lam(r)
        return None
    n = 0
    while True:
        r = red(t)
        if r is None:
            return t, n
        t = r
        n += 1
        if n > limit:
            raise RuntimeError("limit")


def church_value(t) -> int | None:
    if isinstance(t, Lam) and isinstance(t.body, Lam):
        b, n = t.body.body, 0
        while isinstance(b, App) and b.f == Var(1):
            b, n = b.a, n + 1
        return n if b == Var(0) else None
    return None


def nbe_experiment() -> list[dict]:
    rows = []
    for name, term, expect in (("2 + 3", App(App(PLUS, church(2)), church(3)), 5),
                               ("2 x 3", App(App(TIMES, church(2)), church(3)), 6),
                               ("3 x 4", App(App(TIMES, church(3)), church(4)), 12),
                               ("2 ^ 3", App(App(EXP, church(2)), church(3)), 8),
                               ("3 ^ 3", App(App(EXP, church(3)), church(3)), 27)):
        nf = nbe(term)
        nf2, steps = beta_steps(term)
        rows.append({"term": name, "nbe": church_value(nf), "beta": church_value(nf2), "beta_steps": steps,
                     "expected": expect, "same_normal_form": nf == nf2})
    return rows


# ---------------------------------------------------------------- free theorems

def free_theorems(trials: int = 2000, seed: int = 0) -> dict:
    """Any function r : [a] -> [a] commutes with map (r . map f = map f . r); any sort parametric in its comparison
    commutes with map f for monotone f.  Checked on random lists and functions, and the non-monotone counterexample
    found."""
    rng = random.Random(seed)
    rearrangements = {"reverse": lambda xs: xs[::-1], "take 3": lambda xs: xs[:3],
                      "every other": lambda xs: xs[::2], "rotate": lambda xs: xs[1:] + xs[:1]}
    out = {}
    for name, r in rearrangements.items():
        ok = 0
        for _ in range(trials):
            xs = [rng.randint(-20, 20) for _ in range(rng.randint(0, 8))]
            a, b = rng.randint(-3, 3), rng.randint(-5, 5)
            f = lambda x, a=a, b=b: a * x * x + b  # noqa: E731
            ok += r([f(x) for x in xs]) == [f(x) for x in r(xs)]
        out[name] = ok / trials
    mono, counter = 0, None
    for _ in range(trials):
        xs = [rng.randint(-20, 20) for _ in range(rng.randint(0, 8))]
        f = lambda x: 2 * x + 1  # noqa: E731
        mono += sorted(f(x) for x in xs) == [f(x) for x in sorted(xs)]
        g = lambda x: x * x  # noqa: E731
        if counter is None and sorted(g(x) for x in xs) != [g(x) for x in sorted(xs)]:
            counter = {"xs": xs, "sort_then_map": [g(x) for x in sorted(xs)], "map_then_sort": sorted(g(x) for x in xs)}
    return {"rearrangements": out, "sort_monotone": mono / trials, "sort_counterexample": counter}


# ---------------------------------------------------------------- bisimulation

def bisimilar(lts: dict, p, q) -> dict:
    """Strong bisimilarity by naive partition refinement: split blocks until every state in a block can reach the
    same set of blocks by each action.  lts: state -> list of (action, state)."""
    states = sorted(lts)
    block = {s: 0 for s in states}
    rounds = 0
    while True:
        rounds += 1
        sig = {s: (block[s], frozenset((a, block[t]) for a, t in lts[s])) for s in states}
        ids = {}
        new = {s: ids.setdefault(sig[s], len(ids)) for s in states}
        if len(set(new.values())) == len(set(block.values())):
            break
        block = new
    return {"bisimilar": block[p] == block[q], "blocks": len(set(block.values())), "rounds": rounds,
            "partition": {s: block[s] for s in states}}


def traces(lts, s, depth=3):
    out = {()}
    if depth == 0:
        return out
    for a, t in lts[s]:
        out |= {(a,) + tr for tr in traces(lts, t, depth - 1)}
    return out


def bisim_examples() -> dict:
    """a.(b + c) against a.b + a.c (Milner): the same traces, but after the first a the second machine has already
    chosen; an observer who wants to choose c after a can tell them apart."""
    L = {"P": [("a", "P1")], "P1": [("b", "P2"), ("c", "P3")], "P2": [], "P3": [],
         "Q": [("a", "Q1"), ("a", "Q2")], "Q1": [("b", "Q3")], "Q2": [("c", "Q4")], "Q3": [], "Q4": []}
    r = bisimilar(L, "P", "Q")
    same_traces = traces(L, "P") == traces(L, "Q")
    V = {"V1": [("coin", "V2")], "V2": [("tea", "V1"), ("coffee", "V1")],
         "W1": [("coin", "W2")], "W2": [("tea", "W3"), ("coffee", "W3")], "W3": [("coin", "W2")]}
    r2 = bisimilar(V, "V1", "W1")
    return {"choice": {"lts": L, "same_traces": same_traces, **r,
                       "formula": "<a>(<b>true and <c>true)"},
            "vending": {"lts": V, **r2}}


# ---------------------------------------------------------------- effects as monads

def monads() -> dict:
    """One small program, safe division of a by b then adding a counter, run in three monads: Maybe (exceptions),
    State (a counter threaded through), and List (nondeterministic choice of b)."""
    def bind_maybe(m, k):
        return None if m is None else k(m)

    def div(a, b):
        return None if b == 0 else a // b

    maybe = {str(b): bind_maybe(div(12, b), lambda q: q + 1) for b in (0, 3, 4)}

    def tick(s):
        return (None, s + 1)

    def bind_state(m, k):
        return lambda s: (lambda r: k(r[0])(r[1]))(m(s))

    prog = bind_state(lambda s: tick(s), lambda _: bind_state(lambda s: tick(s), lambda _: lambda s: (s * 10, s)))
    state = prog(0)
    lst = [q for b in (1, 2, 3, 4) for q in ([12 // b] if b else [])]
    return {"maybe": maybe, "state": {"result": state[0], "final_state": state[1]}, "list": lst}
