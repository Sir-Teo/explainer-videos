"""Propositional logic, exactly: formulas, truth tables, normal forms, SAT, and the elenchus.

    from explainer.philosophy.reasoner.prop import parse, truth_table, satisfiable, mus_mcs
    f = parse("(p -> q) & p -> q")
    tautology(f)                                   # True
    claims = {"omnipotent": parse("o"), ...}
    mus_mcs(claims, background)                    # the minimal inconsistent sets and the minimal ways out

Formulas are nested tuples, so they hash, compare and print without classes:

    ("var", "p")  ("top",)  ("bot",)  ("not", A)  ("and", A, B)  ("or", A, B)  ("imp", A, B)  ("iff", A, B)

Every algorithm here is small enough to check against brute force, and ``tests/philosophy/test_prop.py`` does.
"""

from __future__ import annotations

import itertools
import random
import re
from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# Formulas
# ---------------------------------------------------------------------------
TOP, BOT = ("top",), ("bot",)


def Var(name: str):
    return ("var", name)


def Not(a):
    return ("not", a)


def And(*xs):
    return _fold("and", xs, TOP)


def Or(*xs):
    return _fold("or", xs, BOT)


def Imp(a, b):
    return ("imp", a, b)


def Iff(a, b):
    return ("iff", a, b)


def _fold(op, xs, unit):
    xs = list(xs)
    if not xs:
        return unit
    out = xs[0]
    for x in xs[1:]:
        out = (op, out, x)
    return out


_TOKEN = re.compile(r"\s*(<->|<=>|->|=>|↔|→|¬|~|!|∧|&|∨|\||\(|\)|⊤|⊥|[A-Za-z_][A-Za-z0-9_']*)")
_BIN = {"<->": "iff", "<=>": "iff", "↔": "iff", "->": "imp", "=>": "imp", "→": "imp", "∧": "and", "&": "and",
        "∨": "or", "|": "or"}
_PREC = {"iff": 1, "imp": 2, "or": 3, "and": 4}


def parse(s: str):
    """Parse ``(p -> q) & ~r`` (or the same with ¬ ∧ ∨ → ↔). Precedence: ¬ > ∧ > ∨ > → > ↔; → and ↔ associate to
    the right, ∧ and ∨ to the left. ``⊤``/``top`` and ``⊥``/``bot`` are the constants."""
    toks, pos = [], 0
    s = s.strip()
    while pos < len(s):
        m = _TOKEN.match(s, pos)
        if not m or m.end() == pos:
            raise ValueError(f"cannot parse {s!r} at {pos}: {s[pos:pos + 10]!r}")
        toks.append(m.group(1))
        pos = m.end()
        while pos < len(s) and s[pos].isspace():
            pos += 1
    i = 0

    def peek():
        return toks[i] if i < len(toks) else None

    def atom():
        nonlocal i
        t = peek()
        if t is None:
            raise ValueError(f"unexpected end of {s!r}")
        i += 1
        if t in ("¬", "~", "!"):
            return ("not", atom())
        if t == "(":
            e = expr(0)
            if peek() != ")":
                raise ValueError(f"missing ) in {s!r}")
            i += 1
            return e
        if t in ("⊤", "top"):
            return TOP
        if t in ("⊥", "bot"):
            return BOT
        if t in _BIN or t == ")":
            raise ValueError(f"unexpected {t!r} in {s!r}")
        return ("var", t)

    def expr(min_prec):
        nonlocal i
        left = atom()
        while peek() in _BIN and _PREC[_BIN[peek()]] >= min_prec:
            op = _BIN[peek()]
            i += 1
            right_assoc = op in ("imp", "iff")
            right = expr(_PREC[op] if right_assoc else _PREC[op] + 1)
            left = (op, left, right)
        return left

    e = expr(0)
    if i != len(toks):
        raise ValueError(f"trailing {toks[i:]} in {s!r}")
    return e


def atoms(f) -> list[str]:
    """The variables of ``f`` in order of first appearance."""
    out: list[str] = []

    def go(g):
        if g[0] == "var":
            if g[1] not in out:
                out.append(g[1])
        else:
            for a in g[1:]:
                go(a)

    go(f)
    return out


def atoms_of(fs) -> list[str]:
    out: list[str] = []
    for f in fs:
        for a in atoms(f):
            if a not in out:
                out.append(a)
    return out


def evaluate(f, v: dict) -> bool:
    op = f[0]
    if op == "var":
        return bool(v[f[1]])
    if op == "top":
        return True
    if op == "bot":
        return False
    if op == "not":
        return not evaluate(f[1], v)
    a, b = evaluate(f[1], v), evaluate(f[2], v)
    if op == "and":
        return a and b
    if op == "or":
        return a or b
    if op == "imp":
        return (not a) or b
    if op == "iff":
        return a == b
    raise ValueError(op)


SYM = {"not": "¬", "and": "∧", "or": "∨", "imp": "→", "iff": "↔"}
TEX = {"not": r"\lnot ", "and": r"\land", "or": r"\lor", "imp": r"\to", "iff": r"\leftrightarrow"}


def show(f, tex: bool = False, top: bool = True) -> str:
    """``f`` as text (¬ ∧ ∨ → ↔) or as TeX, with only the brackets precedence needs."""
    sym = TEX if tex else SYM
    op = f[0]
    if op == "var":
        name = f[1]
        if tex:
            m = re.fullmatch(r"([A-Za-z]+)(\d+)", name)
            if m:
                return rf"{m.group(1)}_{{{m.group(2)}}}"
            return name if len(name) == 1 else rf"\mathit{{{name}}}"
        return name
    if op == "top":
        return r"\top" if tex else "⊤"
    if op == "bot":
        return r"\bot" if tex else "⊥"
    if op == "not":
        inner = show(f[1], tex, False)
        return sym["not"] + (f"({inner})" if f[1][0] in _PREC else inner)
    a, b = f[1], f[2]

    def side(g, right):
        s = show(g, tex, False)
        if g[0] in _PREC:
            pg, pf = _PREC[g[0]], _PREC[op]
            if pg < pf or (pg == pf and (right if op in ("and", "or") else not right)):
                return f"({s})"
        return s

    s = f"{side(a, False)} {sym[op]} {side(b, True)}"
    return s


def subformulas(f) -> list:
    """Every subformula of ``f``, children before parents, each once (the columns of a full truth table)."""
    out: list = []

    def go(g):
        for a in g[1:] if g[0] not in ("var",) else ():
            if isinstance(a, tuple):
                go(a)
        if g not in out:
            out.append(g)

    go(f)
    return out


def valuations(names):
    """All 2^n valuations, in the order truth tables list them (first variable slowest, True first)."""
    for bits in itertools.product((True, False), repeat=len(names)):
        yield dict(zip(names, bits))


def truth_table(f, names=None, columns=None):
    """Rows of a truth table: ``(valuation, [value of each column])``; columns default to the subformulas."""
    names = names or atoms(f)
    cols = columns or [g for g in subformulas(f) if g[0] != "var"]
    return [(v, [evaluate(c, v) for c in cols]) for v in valuations(names)], cols


def tautology(f) -> bool:
    return all(evaluate(f, v) for v in valuations(atoms(f)))


def satisfiable_bf(fs) -> dict | None:
    """Brute force: a valuation satisfying every formula in ``fs``, or None."""
    names = atoms_of(fs)
    for v in valuations(names):
        if all(evaluate(f, v) for f in fs):
            return v
    return None


def entails(premises, conclusion) -> tuple[bool, dict | None]:
    """Does ``premises ⊨ conclusion``? Returns (verdict, a countermodel when it fails)."""
    names = atoms_of(list(premises) + [conclusion])
    for v in valuations(names):
        if all(evaluate(p, v) for p in premises) and not evaluate(conclusion, v):
            return False, v
    return True, None


def truth_function(f, names) -> tuple[bool, ...]:
    return tuple(evaluate(f, v) for v in valuations(names))


# ---------------------------------------------------------------------------
# Post's functional completeness
# ---------------------------------------------------------------------------
def _post_classes(table: tuple[bool, ...], n: int) -> dict[str, bool]:
    """Which of Post's five clones a truth function (listed in ``valuations`` order) belongs to."""
    rows = list(itertools.product((True, False), repeat=n))
    val = dict(zip(rows, table))
    t0 = val[tuple([False] * n)] is False
    t1 = val[tuple([True] * n)] is True
    sd = all(val[tuple(not x for x in r)] == (not val[r]) for r in rows)
    mono = all(not (all(a <= b for a, b in zip(r, s)) and val[r] > val[s]) for r in rows for s in rows)
    # affine: f = c ⊕ (xor of some subset); test every subset
    aff = False
    for c in (False, True):
        for S in itertools.product((False, True), repeat=n):
            if all(val[r] == (c ^ (sum(x for x, s in zip(r, S) if s) % 2 == 1)) for r in rows):
                aff = True
                break
        if aff:
            break
    return {"T0": t0, "T1": t1, "self-dual": sd, "monotone": mono, "affine": aff}


CONNECTIVES = {
    "¬": (1, lambda a: not a), "∧": (2, lambda a, b: a and b), "∨": (2, lambda a, b: a or b),
    "→": (2, lambda a, b: (not a) or b), "↔": (2, lambda a, b: a == b), "⊕": (2, lambda a, b: a != b),
    "↑": (2, lambda a, b: not (a and b)), "↓": (2, lambda a, b: not (a or b)),
    "⊤": (0, lambda: True), "⊥": (0, lambda: False),
}


def post_complete(conns) -> tuple[bool, dict]:
    """Post (1941): a set of connectives is functionally complete iff for each of the five clones some connective
    lies outside it. Returns (complete?, {clone: [connectives outside it]})."""
    escape = {k: [] for k in ("T0", "T1", "self-dual", "monotone", "affine")}
    for c in conns:
        n, fn = CONNECTIVES[c]
        table = tuple(fn(*r) for r in itertools.product((True, False), repeat=n))
        cls = _post_classes(table, n)
        for k, inside in cls.items():
            if not inside:
                escape[k].append(c)
    return all(escape.values()), escape


# ---------------------------------------------------------------------------
# Normal forms and clauses (DIMACS-style integers: variable i is i, its negation -i)
# ---------------------------------------------------------------------------
def nnf(f):
    op = f[0]
    if op in ("var", "top", "bot"):
        return f
    if op == "imp":
        return nnf(("or", ("not", f[1]), f[2]))
    if op == "iff":
        return nnf(("and", ("imp", f[1], f[2]), ("imp", f[2], f[1])))
    if op in ("and", "or"):
        return (op, nnf(f[1]), nnf(f[2]))
    g = f[1]  # not
    if g[0] == "var":
        return f
    if g[0] == "top":
        return BOT
    if g[0] == "bot":
        return TOP
    if g[0] == "not":
        return nnf(g[1])
    if g[0] == "and":
        return ("or", nnf(("not", g[1])), nnf(("not", g[2])))
    if g[0] == "or":
        return ("and", nnf(("not", g[1])), nnf(("not", g[2])))
    return nnf(("not", nnf(g)))


def cnf_clauses(f, names) -> list[frozenset]:
    """CNF by distribution (exponential in the worst case; fine for small formulas): clauses as frozensets of
    signed integers, variable ``names[i]`` being ``i + 1``. Tautologous clauses are dropped."""
    idx = {n: i + 1 for i, n in enumerate(names)}

    def go(g):
        op = g[0]
        if op == "top":
            return []
        if op == "bot":
            return [frozenset()]
        if op == "var":
            return [frozenset([idx[g[1]]])]
        if op == "not":
            return [frozenset([-idx[g[1][1]]])]
        if op == "and":
            return go(g[1]) + go(g[2])
        a, b = go(g[1]), go(g[2])
        return [x | y for x in a for y in b]

    out = []
    for c in go(nnf(f)):
        if not any(-l in c for l in c) and c not in out:
            out.append(c)
    return out


def tseitin(f, names: list[str]) -> tuple[list[frozenset], list[str]]:
    """Tseitin's transformation (1968): an equisatisfiable CNF linear in the size of ``f``. ``names`` is extended
    with one fresh variable per connective (``_t1``, ``_t2``, ...); returns (clauses, names)."""
    names = list(names)
    idx = {n: i + 1 for i, n in enumerate(names)}
    clauses: list[frozenset] = []

    def lit(g) -> int:
        op = g[0]
        if op == "var":
            if g[1] not in idx:
                names.append(g[1])
                idx[g[1]] = len(names)
            return idx[g[1]]
        if op == "not":
            return -lit(g[1])
        names.append(f"_t{len(names) + 1}")
        x = len(names)
        idx[names[-1]] = x
        if op == "top":
            clauses.append(frozenset([x]))
            return x
        if op == "bot":
            clauses.append(frozenset([-x]))
            return x
        a, b = lit(g[1]), lit(g[2])
        if op == "and":
            clauses.extend([frozenset([-x, a]), frozenset([-x, b]), frozenset([x, -a, -b])])
        elif op == "or":
            clauses.extend([frozenset([-x, a, b]), frozenset([x, -a]), frozenset([x, -b])])
        elif op == "imp":
            clauses.extend([frozenset([-x, -a, b]), frozenset([x, a]), frozenset([x, -b])])
        elif op == "iff":
            clauses.extend([frozenset([-x, -a, b]), frozenset([-x, a, -b]), frozenset([x, a, b]),
                            frozenset([x, -a, -b])])
        return x

    clauses.append(frozenset([lit(f)]))
    return clauses, names


# ---------------------------------------------------------------------------
# SAT: DPLL (with a recorded tree) and CDCL (with learned clauses), on integer clauses
# ---------------------------------------------------------------------------
def _simplify(clauses, lit):
    out = []
    for c in clauses:
        if lit in c:
            continue
        if -lit in c:
            c = c - {-lit}
        out.append(c)
    return out


@dataclass
class DPLLNode:
    decision: int | None
    forced: list[int]
    end: str  # "conflict", "sat", "split"
    children: list[int] = field(default_factory=list)
    parent: int | None = None


def dpll(clauses, n_vars: int, record: bool = False, choose=None):
    """DPLL (Davis, Putnam 1960; Davis, Logemann, Loveland 1962): unit propagation, pure literals off, branch on the
    lowest unassigned variable (or ``choose(clauses, assigned)``), True first. Returns (model dict var->bool or
    None, stats) where stats has ``decisions``, ``propagations``, ``conflicts`` and, if ``record``, ``nodes``
    (the search tree in creation order)."""
    stats = {"decisions": 0, "propagations": 0, "conflicts": 0, "nodes": []}

    def go(cl, assign, parent, decision):
        cl = list(cl)
        forced = []
        while True:
            if any(len(c) == 0 for c in cl):
                stats["conflicts"] += 1
                if record:
                    k = len(stats["nodes"])
                    stats["nodes"].append(DPLLNode(decision, forced, "conflict", parent=parent))
                    if parent is not None:
                        stats["nodes"][parent].children.append(k)
                return None
            units = [next(iter(c)) for c in cl if len(c) == 1]
            if not units:
                break
            u = units[0]
            forced.append(u)
            stats["propagations"] += 1
            assign = {**assign, abs(u): u > 0}
            cl = _simplify(cl, u)
        k = None
        if record:
            k = len(stats["nodes"])
            stats["nodes"].append(DPLLNode(decision, forced, "sat" if not cl else "split", parent=parent))
            if parent is not None:
                stats["nodes"][parent].children.append(k)
        if not cl:
            return assign
        free = sorted({abs(l) for c in cl for l in c})
        v = choose(cl, assign) if choose else free[0]
        for val in (v, -v):
            stats["decisions"] += 1
            r = go(_simplify(cl, val), {**assign, v: val > 0}, k, val)
            if r is not None:
                return r
        return None

    model = go([frozenset(c) for c in clauses], {}, None, None)
    if model is not None:
        for v in range(1, n_vars + 1):
            model.setdefault(v, True)
    return model, stats


def cdcl(clauses, n_vars: int, record: bool = False, max_conflicts: int = 10**7):
    """Conflict-driven clause learning (Marques-Silva and Sakallah 1996): watched-free but exact; first-UIP
    learning, non-chronological backjumping, VSIDS-like activity. Returns (model or None, stats) with
    ``decisions``, ``propagations``, ``conflicts``, ``learned`` (the clauses learned, in order) and, if
    ``record``, ``events`` (decide / propagate / conflict / learn / backjump)."""
    clauses = [list(c) for c in clauses]
    stats = {"decisions": 0, "propagations": 0, "conflicts": 0, "learned": [], "events": []}
    if any(len(c) == 0 for c in clauses):
        return None, stats
    assign: dict[int, bool] = {}
    level: dict[int, int] = {}
    reason: dict[int, int | None] = {}
    trail: list[int] = []
    activity = {v: 0.0 for v in range(1, n_vars + 1)}
    for c in clauses:
        for l in c:
            activity[abs(l)] += 1.0
    bump = 1.0

    def value(l):
        v = assign.get(abs(l))
        return None if v is None else (v if l > 0 else not v)

    def propagate(dl):
        changed = True
        while changed:
            changed = False
            for ci, c in enumerate(clauses):
                vals = [value(l) for l in c]
                if any(x is True for x in vals):
                    continue
                open_ = [l for l, x in zip(c, vals) if x is None]
                if not open_:
                    return ci
                if len(open_) == 1:
                    u = open_[0]
                    assign[abs(u)] = u > 0
                    level[abs(u)] = dl
                    reason[abs(u)] = ci
                    trail.append(u)
                    stats["propagations"] += 1
                    if record:
                        stats["events"].append(("propagate", u, ci, dl))
                    changed = True
        return None

    dl = 0
    conflict = propagate(0)
    if conflict is not None:
        return None, stats
    while True:
        free = [v for v in range(1, n_vars + 1) if v not in assign]
        if not free:
            return {v: assign[v] for v in range(1, n_vars + 1)}, stats
        v = max(free, key=lambda x: (activity[x], -x))
        dl += 1
        stats["decisions"] += 1
        assign[v], level[v], reason[v] = True, dl, None
        trail.append(v)
        if record:
            stats["events"].append(("decide", v, None, dl))
        while True:
            conflict = propagate(dl)
            if conflict is None:
                break
            stats["conflicts"] += 1
            if record:
                stats["events"].append(("conflict", None, conflict, dl))
            if stats["conflicts"] > max_conflicts:
                raise RuntimeError("conflict budget exceeded")
            if dl == 0:
                return None, stats
            # first-UIP analysis
            learnt = set(clauses[conflict])
            while True:
                at_dl = [l for l in learnt if level.get(abs(l)) == dl]
                if len(at_dl) <= 1:
                    break
                last = next(l for l in reversed(trail) if -l in learnt and level[abs(l)] == dl and reason[abs(l)] is not None)
                r = clauses[reason[abs(last)]]
                learnt = (learnt - {-last}) | {x for x in r if x != last}
            learnt_l = sorted(learnt, key=lambda l: (-level.get(abs(l), 0), abs(l)))
            for l in learnt_l:
                activity[abs(l)] += bump
            bump *= 1.05
            back = max([level[abs(l)] for l in learnt_l if level[abs(l)] != dl], default=0)
            clauses.append(learnt_l)
            stats["learned"].append(tuple(learnt_l))
            if record:
                stats["events"].append(("learn", tuple(learnt_l), len(clauses) - 1, back))
            # backjump
            while trail and level[abs(trail[-1])] > back:
                u = trail.pop()
                del assign[abs(u)], level[abs(u)], reason[abs(u)]
            dl = back
            if record:
                stats["events"].append(("backjump", None, None, back))


def solve(fs, names=None) -> dict | None:
    """Satisfy a list of formulas (Tseitin + CDCL). Returns a valuation of their atoms, or None."""
    names = list(names or atoms_of(fs))
    big = And(*fs) if fs else TOP
    cl, allnames = tseitin(big, names)
    model, _ = cdcl(cl, len(allnames))
    if model is None:
        return None
    return {n: model[i + 1] for i, n in enumerate(names)}


def satisfiable(fs) -> bool:
    return solve(list(fs)) is not None


# ---------------------------------------------------------------------------
# Resolution
# ---------------------------------------------------------------------------
def resolve(a: frozenset, b: frozenset):
    """All resolvents of two clauses (one per clashing pair), tautologies dropped."""
    out = []
    for l in a:
        if -l in b:
            r = (a - {l}) | (b - {-l})
            if not any(-x in r for x in r):
                out.append(frozenset(r))
    return out


def resolution_refute(clauses, limit: int = 200000) -> dict:
    """Resolution (Robinson 1965) by the given-clause loop: take the shortest waiting clause, drop it if a kept clause
    subsumes it, else keep it and resolve it with every kept clause. Stops at the empty clause or when nothing new
    comes. Returns {"refuted", "derived" (resolvents generated), "kept", "proof": [(clause, parent_a, parent_b)]}."""
    import heapq

    parents: dict[frozenset, tuple] = {}
    waiting: list = []
    tick = 0
    for c in clauses:
        c = frozenset(c)
        if c not in parents:
            parents[c] = (None, None)
            heapq.heappush(waiting, (len(c), tick, c))
            tick += 1
    kept: list[frozenset] = []
    derived = 0

    def proof_of(empty):
        proof = []

        def back(c):
            pa, pb = parents[c]
            if pa is None:
                return
            back(pa)
            back(pb)
            if (c, pa, pb) not in proof:
                proof.append((c, pa, pb))

        back(empty)
        return proof

    while waiting:
        _, _, g = heapq.heappop(waiting)
        if any(k <= g for k in kept):
            continue
        kept = [k for k in kept if not g <= k]
        kept.append(g)
        for k in list(kept):
            for r in resolve(g, k):
                derived += 1
                if r in parents:
                    continue
                parents[r] = (g, k)
                if not r:
                    return {"refuted": True, "derived": derived, "kept": len(kept), "proof": proof_of(r)}
                if not any(x <= r for x in kept):
                    heapq.heappush(waiting, (len(r), tick, r))
                    tick += 1
                if derived > limit:
                    return {"refuted": False, "derived": derived, "kept": len(kept), "proof": [], "gave_up": True}
    return {"refuted": False, "derived": derived, "kept": len(kept), "proof": []}


# ---------------------------------------------------------------------------
# Families of formulas
# ---------------------------------------------------------------------------
def pigeonhole(n: int) -> tuple[list[frozenset], int]:
    """PHP(n+1, n): n+1 pigeons in n holes, one per hole. Variable p_{i,j} (pigeon i in hole j) is i*n + j + 1.
    Unsatisfiable; Haken (1985): every resolution refutation has size exponential in n."""
    var = lambda i, j: i * n + j + 1  # noqa: E731
    cl = [frozenset(var(i, j) for j in range(n)) for i in range(n + 1)]
    for j in range(n):
        for i in range(n + 1):
            for k in range(i + 1, n + 1):
                cl.append(frozenset([-var(i, j), -var(k, j)]))
    return cl, (n + 1) * n


def random_ksat(n: int, m: int, k: int = 3, rng: random.Random | None = None) -> list[frozenset]:
    rng = rng or random.Random(0)
    out = []
    for _ in range(m):
        vs = rng.sample(range(1, n + 1), k)
        out.append(frozenset(v if rng.random() < 0.5 else -v for v in vs))
    return out


# ---------------------------------------------------------------------------
# The elenchus: minimal unsatisfiable subsets and minimal correction sets
# ---------------------------------------------------------------------------
def mus_mcs(claims: dict, background=()) -> dict:
    """Socrates' method, exactly. ``claims`` maps a name to a formula; ``background`` are formulas held fixed
    (definitions, logic). Enumerates every subset (claims are few: a Price List has 3-8), and returns

    * ``consistent``: whether all the claims together are satisfiable with the background;
    * ``mus``: the minimal unsatisfiable subsets (each a sorted tuple of names);
    * ``mcs``: the minimal correction sets, the minimal sets of claims whose rejection restores consistency:
      the possible *positions*, each named by what it gives up;
    * ``mss``: their complements, the maximal satisfiable subsets (what each position keeps).

    Hitting-set duality (Reiter 1987; Liffiton and Sakallah 2008) holds: the MCSs are exactly the minimal hitting
    sets of the MUSs; ``hitting_sets`` checks it independently."""
    names = list(claims)
    bg = list(background)
    sat_cache: dict[frozenset, bool] = {}

    def sat(S):
        S = frozenset(S)
        if S not in sat_cache:
            sat_cache[S] = satisfiable_bf(bg + [claims[x] for x in S]) is not None if len(
                atoms_of(bg + [claims[x] for x in S])) <= 16 else satisfiable(bg + [claims[x] for x in S])
        return sat_cache[S]

    subsets = [frozenset(c) for r in range(len(names) + 1) for c in itertools.combinations(names, r)]
    uns = [S for S in subsets if not sat(S)]
    mus = [S for S in uns if all(sat(S - {x}) for x in S)]
    satis = [S for S in subsets if sat(S)]
    mss = [S for S in satis if all(not sat(S | {x}) for x in names if x not in S)]
    full = frozenset(names)
    mcs = [full - S for S in mss]
    key = lambda S: (len(S), sorted(names.index(x) for x in S))  # noqa: E731
    return {
        "consistent": sat(full),
        "mus": [tuple(sorted(S, key=names.index)) for S in sorted(mus, key=key)],
        "mcs": [tuple(sorted(S, key=names.index)) for S in sorted(mcs, key=key)],
        "mss": [tuple(sorted(S, key=names.index)) for S in sorted(mss, key=lambda S: key(full - S))],
    }


def hitting_sets(family) -> list[tuple]:
    """The minimal hitting sets of a family of sets (brute force over the union)."""
    universe = sorted({x for S in family for x in S}, key=str)
    hits = []
    for r in range(len(universe) + 1):
        for c in itertools.combinations(universe, r):
            cs = set(c)
            if all(cs & set(S) for S in family) and not any(set(h) <= cs for h in hits):
                hits.append(c)
    return hits


# ---------------------------------------------------------------------------
# Natural deduction, Fitch style
# ---------------------------------------------------------------------------
RULES = ("premise", "assume", "reit", "andI", "andE", "orI", "orE", "impI", "impE", "notI", "notE", "botE",
         "dne", "iffI", "iffE")


def check_fitch(lines, premises=None, goal=None) -> tuple[bool, str]:
    """Check a Fitch-style natural deduction proof.

    ``lines`` is a list of ``(depth, formula_text, rule, refs)``: ``depth`` the number of open subproofs, ``rule`` in
    ``RULES``, ``refs`` the line numbers (1-based) it cites; a subproof is cited as a pair ``(start, end)``.
    Rules: andI (a, b), andE (a), orI (a), orE (disjunction, (s1,e1), (s2,e2)), impI ((s,e)), impE (imp, ant),
    notI ((s,e) ending in ⊥), notE (a, ¬a) gives ⊥, botE (⊥), dne (¬¬a), iffI ((s1,e1),(s2,e2)), iffE (iff, side),
    reit (an accessible line). Returns (ok, message)."""
    parsed = [(d, parse(t), r, refs) for d, t, r, refs in lines]
    # scope: for each line, the chain of subproofs it lives in (start indices)
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

    def accessible(i, j):  # line j is usable at line i: earlier, and its subproofs are still open at i
        return j < i and all(s in scope[i] for s in scope[j])

    def subproof(i, se):
        s, e = se[0] - 1, se[1] - 1
        if not (0 <= s <= e < i) or parsed[s][2] != "assume":
            return None
        # e must be in the subproof opened at s, at the same or deeper level, and the subproof closed by line i
        if s not in scope[e] or s in scope[i]:
            return None
        if not all(x in scope[i] for x in scope[s][:-1]):
            return None
        return parsed[s][1], parsed[e][1]

    for i, (d, f, r, refs) in enumerate(parsed):
        ok = False
        R = [x - 1 if isinstance(x, int) else x for x in refs]
        ints = [x for x in R if isinstance(x, int)]
        if any(not accessible(i, j) for j in ints):
            return False, f"line {i + 1}: cites a line that is not accessible"
        g = lambda k: parsed[R[k]][1]  # noqa: E731
        try:
            if r == "premise":
                ok = d == 0 and (premises is None or f in [parse(p) for p in premises])
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
                dis = g(0)
                a = subproof(i, refs[1])
                b = subproof(i, refs[2])
                ok = (dis[0] == "or" and a and b and {a[0], b[0]} == {dis[1], dis[2]} and a[1] == f and b[1] == f)
            elif r == "impI":
                a = subproof(i, refs[0])
                ok = bool(a) and f == ("imp", a[0], a[1])
            elif r == "impE":
                ok = g(0)[0] == "imp" and g(0)[1] == g(1) and g(0)[2] == f
            elif r == "notI":
                a = subproof(i, refs[0])
                ok = bool(a) and a[1] == BOT and f == ("not", a[0])
            elif r == "notE":
                ok = f == BOT and (g(1) == ("not", g(0)) or g(0) == ("not", g(1)))
            elif r == "botE":
                ok = g(0) == BOT
            elif r == "dne":
                ok = g(0) == ("not", ("not", f))
            elif r == "iffI":
                a, b = subproof(i, refs[0]), subproof(i, refs[1])
                ok = bool(a and b) and f[0] == "iff" and a == (f[1], f[2]) and b == (f[2], f[1])
            elif r == "iffE":
                ok = g(0)[0] == "iff" and ((g(1) == g(0)[1] and f == g(0)[2]) or (g(1) == g(0)[2] and f == g(0)[1]))
        except (IndexError, TypeError):
            ok = False
        if not ok:
            return False, f"line {i + 1}: {r} does not justify {show(f)}"
    if goal is not None:
        last = parsed[-1]
        if last[0] != 0 or last[1] != parse(goal):
            return False, "the proof does not end with the goal at depth 0"
    return True, "valid"
