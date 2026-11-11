"""Abstract interpretation (Part 54): the interval domain over the language of hoare.py, read here over mathematical
integers (no wrap-around), with join, meet, widening and narrowing, and a structured fixpoint iteration that records
every loop iteration for the animation of the lattice and the widening jump.

    Interval domain                    an interval is (lo, hi) with lo <= hi, bounds ints or -inf/+inf; None is bottom;
                                       join (hull), meet (intersection), widen (an unstable bound jumps to infinity),
                                       narrow (only an infinite bound may come back)
    abstract eval and filter           interval arithmetic for + - * unary - >> 1, and refinement of a state by a
                                       condition (x < e, e < x, ==, !=, &&, ||, !, ==>)
    analyze(prog, widen=True)          per loop: every iteration's head state, phase ascending / narrowing; the final
                                       state before every line; each assert proved or not
    concrete_states(prog, env)         the states a concrete run passes through at each line, for the soundness test
    EXAMPLES / relational_gap()        x counting to 100 (101 iterations without widening, 2 with it, narrowed back to
                                       [0, 100]); i counting to 10 with j = 2 i, where plain iteration never stops
                                       (j's bound climbs forever) and widening gives j in [0, +inf]: the relation is
                                       what intervals cannot hold

A program point's abstract state maps each variable to an interval (a missing variable is unconstrained); the state
None is unreachable.  Each concrete set of states is abstracted by its box of intervals: the Galois connection between
sets of integer vectors and boxes.  Relational domains keep what boxes lose: octagons (Mine 2006) bound +-x +-y, so
they hold i + j = 10 but not j = 2 i; linear equalities (Karr 1976) and convex polyhedra (Cousot and Halbwachs 1978)
hold j = 2 i exactly.

After Cousot and Cousot, "Abstract interpretation: a unified lattice model for static analysis of programs by
construction or approximation of fixpoints" (POPL 1977); Moller and Schwartzbach, *Static Program Analysis* (2024),
ch. 5-6; Rival and Yi, *Introduction to Static Analysis* (2020).
"""

from __future__ import annotations

import math

from explainer.cs.verify import hoare as H

INF = math.inf
TOP = (-INF, INF)


# ------------------------------------------------------------------------------------------- the interval lattice

def interval(lo, hi):
    return None if lo > hi else (lo, hi)


def join(a, b):
    if a is None:
        return b
    if b is None:
        return a
    return (min(a[0], b[0]), max(a[1], b[1]))


def meet(a, b):
    if a is None or b is None:
        return None
    return interval(max(a[0], b[0]), min(a[1], b[1]))


def leq(a, b) -> bool:
    """a is contained in b."""
    return a is None or (b is not None and b[0] <= a[0] and a[1] <= b[1])


def widen(a, b):
    """Standard interval widening: keep a bound that is stable, send one that grew to infinity."""
    if a is None:
        return b
    if b is None:
        return a
    return (a[0] if b[0] >= a[0] else -INF, a[1] if b[1] <= a[1] else INF)


def narrow(a, b):
    """Standard narrowing: only an infinite bound of a may be replaced by b's."""
    if a is None or b is None:
        return None
    return interval(b[0] if a[0] == -INF else a[0], b[1] if a[1] == INF else a[1])


def fmt(iv):
    """JSON form: [lo, hi] with '-inf' / '+inf', or None for bottom."""
    if iv is None:
        return None
    return ["-inf" if iv[0] == -INF else iv[0], "+inf" if iv[1] == INF else iv[1]]


# ------------------------------------------------------------------------------------------- abstract states

def s_join(s, t):
    if s is None:
        return None if t is None else dict(t)
    if t is None:
        return dict(s)
    return {x: join(s[x], t[x]) for x in s if x in t}          # missing = top


def s_leq(s, t) -> bool:
    if s is None:
        return True
    if t is None:
        return False
    return all(leq(s.get(x, TOP), t[x]) for x in t)


def s_pointwise(f, s, t):
    keys = set(s) & set(t)
    out = {x: f(s[x], t[x]) for x in keys}
    return None if any(v is None for v in out.values()) else out


def s_widen(s, t):
    if s is None:
        return t
    if t is None:
        return s
    return s_pointwise(widen, s, t)


def s_narrow(s, t):
    if s is None or t is None:
        return None
    return s_pointwise(narrow, s, t)


def s_fmt(s):
    return None if s is None else {x: fmt(s[x]) for x in sorted(s)}


# ------------------------------------------------------------------------------------------- transfer functions

def _half(b):
    return b if b in (INF, -INF) else b // 2


def _mul(a, b):
    def m(x, y):
        return 0 if x == 0 or y == 0 else x * y
    ps = [m(x, y) for x in a for y in b]
    return (min(ps), max(ps))


def aeval(e, s):
    """The interval of a term in abstract state s (not None)."""
    op = e[0]
    if op == "var":
        return s.get(e[1], TOP)
    if op == "const":
        return (e[1], e[1])
    a = aeval(e[1], s)
    if op == "neg":
        return (-a[1], -a[0])
    if op == "ashr":
        return (_half(a[0]), _half(a[1]))
    if op == "lshr":
        return (_half(a[0]), _half(a[1])) if a[0] >= 0 else (0, INF)
    b = aeval(e[2], s)
    if op == "add":
        return (a[0] + b[0], a[1] + b[1])
    if op == "sub":
        return (a[0] - b[1], a[1] - b[0])
    if op == "mul":
        return _mul(a, b)
    raise TypeError(op)


_FLIP = {"lt": "gt", "le": "ge", "gt": "lt", "ge": "le", "eq": "eq", "ne": "ne"}
_NEG = {"lt": "ge", "le": "gt", "gt": "le", "ge": "lt", "eq": "ne", "ne": "eq"}


def _restrict(x, op, b):
    """Values of x consistent with x op y for some y in b."""
    if op == "lt":
        return meet(x, (-INF, b[1] - 1))
    if op == "le":
        return meet(x, (-INF, b[1]))
    if op == "gt":
        return meet(x, (b[0] + 1, INF))
    if op == "ge":
        return meet(x, (b[0], INF))
    if op == "eq":
        return meet(x, b)
    if b[0] == b[1] and x is not None:                         # ne: shave a matching endpoint
        if x[0] == b[0]:
            return interval(x[0] + 1, x[1])
        if x[1] == b[0]:
            return interval(x[0], x[1] - 1)
    return x


def afilter(s, c):
    """The abstract state s refined by the condition c (None if c cannot hold)."""
    if s is None:
        return None
    op = c[0]
    if op == "true":
        return s
    if op == "false":
        return None
    if op == "and":
        return afilter(afilter(s, c[1]), c[2])
    if op == "or":
        return s_join(afilter(s, c[1]), afilter(s, c[2]))
    if op == "implies":
        return afilter(s, ("or", ("not", c[1]), c[2]))
    if op == "not":
        d = c[1]
        if d[0] in _NEG:
            return afilter(s, (_NEG[d[0]], d[1], d[2]))
        return afilter(s, {"true": H.FALSE, "false": H.TRUE}.get(d[0]) or
                       {"and": lambda: ("or", ("not", d[1]), ("not", d[2])),
                        "or": lambda: ("and", ("not", d[1]), ("not", d[2])),
                        "implies": lambda: ("and", d[1], ("not", d[2])),
                        "not": lambda: d[1]}[d[0]]())
    a, b = aeval(c[1], s), aeval(c[2], s)
    if _restrict(a, op, b) is None:
        return None
    s = dict(s)
    if c[1][0] == "var":
        s[c[1][1]] = _restrict(a, op, b)
    if c[2][0] == "var":
        b2 = _restrict(aeval(c[2], s), _FLIP[op], aeval(c[1], s))
        if b2 is None:
            return None
        s[c[2][1]] = b2
    return s


# ------------------------------------------------------------------------------------------- the analysis

class _Analysis:
    def __init__(self, prog, widen_on, max_iter, narrow_steps):
        self.prog = prog
        self.widen_on = widen_on
        self.max_iter = max_iter
        self.narrow_steps = narrow_steps
        self.ids = H.line_numbers(prog["body"])
        self.points = {}                                     # line -> state before it (last visit)
        self.heads = {}                                      # loop line -> head state
        self.trace = []
        self.loops = {}
        self.asserts = {}

    def block(self, stmts, s, record):
        for st in stmts:
            s = self.stmt(st, s, record)
        return s

    def stmt(self, st, s, record):
        line = self.ids[id(st)]
        if record:
            self.points[line] = s
        if s is None:
            if st[0] == "while" and record:
                self.heads[line] = None
            return None
        k = st[0]
        if k == "assign":
            s = dict(s)
            s[st[1]] = aeval(st[2], s)
            return s
        if k == "havoc":
            s = dict(s)
            s[st[1]] = TOP
            return s
        if k == "assume":
            return afilter(s, st[1])
        if k == "assert":
            if record:
                self.asserts[line] = afilter(s, H.neg(st[1])) is None
            return afilter(s, st[1])
        if k == "if":
            return s_join(self.block(st[2], afilter(s, st[1]), record),
                          self.block(st[3], afilter(s, H.neg(st[1])), record))
        if k == "while":
            return self.loop(st, line, s, record)
        raise ValueError(k)

    def loop(self, st, line, entry, record):
        c, body = st[1], st[3]

        def F(head):
            return s_join(entry, self.block(body, afilter(head, c), False))

        head = dict(entry)
        ascending, narrowing = 0, 0
        widening, converged = self.widen_on, True
        self.trace.append({"loop": line, "iteration": 0, "phase": "entry", "head": s_fmt(head)})
        while True:
            ascending += 1
            if not widening and ascending > self.max_iter:
                widening, converged = True, False           # give up on plain iteration: widen, to stay sound
            new = F(head)
            nxt = s_widen(head, new) if widening else s_join(head, new)
            self.trace.append({"loop": line, "iteration": ascending, "phase": "ascending",
                               "computed": s_fmt(new), "head": s_fmt(nxt), "widened": nxt != s_join(head, new)})
            if s_leq(nxt, head):
                break
            head = nxt
        if widening:
            for _ in range(self.narrow_steps):
                narrowing += 1
                nxt = s_narrow(head, F(head))
                self.trace.append({"loop": line, "iteration": ascending + narrowing, "phase": "narrowing",
                                   "head": s_fmt(nxt)})
                if nxt == head:
                    break
                head = nxt
        if record:
            self.heads[line] = head
            self.block(body, afilter(head, c), True)
            self.loops[line] = {"line": line, "ascending": ascending, "narrowing": narrowing,
                                "converged_without_widening": converged if not self.widen_on else None,
                                "head": s_fmt(head)}
        return afilter(head, H.neg(c))


def analyze(prog, widen: bool = True, max_iter: int = 1000, narrow_steps: int = 5, init=None) -> dict:
    """Interval analysis of a program from the initial abstract state ``init`` (default: every variable
    unconstrained; the precondition is applied as an assumption).  Without widening, a loop whose plain Kleene
    iteration has not stabilized after ``max_iter`` rounds (an infinite ascending chain) is widened from then on, to
    stay sound and finite, and reports converged_without_widening = False.  Returns {name, widen, loops: per loop the number of
    ascending and narrowing iterations and the final head, trace: every iteration's head per loop, points: the state
    before each line, exit, asserts: line -> proved}."""
    a = _Analysis(prog, widen, max_iter, narrow_steps)
    s = afilter(dict(init or {}), prog["pre"])
    exit_state = a.block(prog["body"], s, True)
    lines = H.listing(prog)
    return {"name": prog["name"], "widen": widen,
            "loops": [a.loops[k] for k in sorted(a.loops)],
            "trace": a.trace,
            "points": [{"line": r["line"], "code": r["code"], "state": s_fmt(a.points.get(r["line"]))}
                       for r in lines if r["line"] in a.points],
            "heads": {k: s_fmt(v) for k, v in a.heads.items()},
            "exit": s_fmt(exit_state),
            "asserts": [{"line": k, "code": next(r["code"] for r in lines if r["line"] == k), "proved": v}
                        for k, v in sorted(a.asserts.items())],
            "_raw": {"points": a.points, "heads": a.heads, "exit": exit_state}}


def contains(state, env) -> bool:
    """Is the concrete environment inside the abstract state (a missing variable is unconstrained)?"""
    if state is None:
        return False
    return all(state[x][0] <= v <= state[x][1] for x, v in env.items() if x in state)


def concrete_states(prog, env, fuel: int = 100_000, choose=None) -> dict:
    """Run the program on mathematical integers; returns {'points': line -> [envs before it], 'heads': loop line ->
    [envs at its tests], 'exit': final env or None if an assume blocked}."""
    ids = H.line_numbers(prog["body"])
    pts, heads = {}, {}

    def visit(st, e, where):
        (heads if where == "head" else pts).setdefault(ids[id(st)], []).append(dict(e))
    if not H.evaluate(prog["pre"], env, None):
        raise H.Blocked("precondition")
    try:
        final = H.run(prog["body"], env, None, choose=choose, fuel=fuel, visit=visit)
    except H.Blocked:
        final = None
    return {"points": pts, "heads": heads, "exit": final}


# ------------------------------------------------------------------------------------------- the examples

def counter_program():
    return H.program("count to 100", [H.assign("x", "0"), H.while_("x < 100", "true", [H.assign("x", "x + 1")]),
                                      H.assert_("x == 100")])


def bounded_program():
    return H.program("count to an input n in [0, 50]",
                     [H.assign("i", "0"), H.while_("i < n", "true", [H.assign("i", "i + 1")]),
                      H.assert_("i <= 50")], pre="0 <= n && n <= 50")


def two_counter_program():
    return H.program("i counts up, j = 2 i",
                     [H.assign("i", "0"), H.assign("j", "0"),
                      H.while_("i < 10", "true", [H.assign("i", "i + 1"), H.assign("j", "j + 2")]),
                      H.assert_("j == 20")])


EXAMPLES = {"counter": counter_program, "bounded": bounded_program, "two": two_counter_program}


def relational_gap(max_iter: int = 60) -> dict:
    """What intervals cannot say.  At the head of the two-counter loop the reachable states are the 11 points of the
    line j = 2 i.  Without widening, i stops at [0, 10] but j's upper bound climbs by 2 every round, forever (the guard
    bounds i, and nothing ties j to i): an infinite ascending chain.  With widening, j becomes [0, +inf], and narrowing
    cannot bring it back, since nothing in the loop bounds j; so assert j == 20 is not proved."""
    prog = two_counter_program()
    reach = concrete_states(prog, {})
    loop_line = next(r["line"] for r in H.listing(prog) if r["kind"] == "while")
    states = sorted({(e["i"], e["j"]) for e in reach["heads"][loop_line]})
    plain = analyze(prog, widen=False, max_iter=max_iter)
    climb = [{"iteration": t["iteration"], "i": t["head"]["i"], "j": t["head"]["j"]}
             for t in plain["trace"] if t["loop"] == loop_line and t["phase"] in ("entry", "ascending")
             and t["iteration"] <= max_iter]
    wid = analyze(prog, widen=True)
    return {"reachable": [list(p) for p in states],
            "relation": "j == 2 * i",
            "no_widen_climb": climb,
            "no_widen_converged": plain["loops"][0]["converged_without_widening"],
            "widen_head": wid["heads"][loop_line],
            "widen_before_assert": next(p["state"] for p in wid["points"] if p["code"].startswith("assert")),
            "assert_proved": wid["asserts"][0]["proved"],
            "relational_head": {"i": [0, 10], "j": [0, 20], "relation": "j == 2 * i"},
            "note": ("intervals keep one range per variable and lose the relation j = 2 i, so they cannot prove "
                     "j == 20 at exit; octagons (+-x +-y <= c) cannot express it either, linear equalities (Karr "
                     "1976) and polyhedra (Cousot and Halbwachs 1978) hold j = 2 i, which with i = 10 at exit "
                     "gives j = 20")}


def examples() -> dict:
    """Every example analyzed with and without widening (raw Python states dropped), plus the relational gap.  Note
    that ``exit`` is the state after the last line; after an assert it assumes the assertion held."""
    out = {}
    for k, f in EXAMPLES.items():
        for w in (False, True):
            r = analyze(f(), widen=w, max_iter=200)
            r.pop("_raw")
            out[f"{k}_{'widen' if w else 'no_widen'}"] = r
    out["relational_gap"] = relational_gap()
    return out
