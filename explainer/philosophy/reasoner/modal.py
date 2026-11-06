"""Modal logic, small and exact: Kripke models, validity on frames checked exhaustively, frame correspondence, a
modal model finder, bisimulation and minimization, tense operators, and explicit-state model checking (CTL with
counterexample traces) for the Part 4 lecture.

    from explainer.philosophy.reasoner.modal import parse, Model, holds, valid_on_frame, all_frames
    f = parse("[]p -> p")                         # the axiom T
    sum(valid_on_frame(f, F) for F in all_frames(3))       # 64 of 512: exactly the reflexive frames

Formulas are tuples: ("var", name), ("top",), ("bot",), ("not", A), ("and", A, B), ("or", A, B), ("imp", A, B),
("iff", A, B), ("box", A), ("dia", A), and for tense logic ("G", A), ("F", A), ("H", A), ("P", A) (future and past,
over the relation and its converse). Text syntax: [] or □ for box, <> or ◇ for diamond, ~ & | -> <->, and the
letters G F H P before a formula for the tense operators.
"""

from __future__ import annotations

import itertools
import re
from collections import deque
from dataclasses import dataclass, field

_TOK = re.compile(r"\s*(\[\]|<>|□|◇|<->|->|↔|→|¬|~|∧|&|∨|\||\(|\)|⊤|⊥|[A-Za-z_][A-Za-z0-9_']*)")
_BIN = {"<->": "iff", "↔": "iff", "->": "imp", "→": "imp", "∧": "and", "&": "and", "∨": "or", "|": "or"}
_PREC = {"iff": 1, "imp": 2, "or": 3, "and": 4}
_UN = {"[]": "box", "□": "box", "<>": "dia", "◇": "dia", "~": "not", "¬": "not"}
TENSE = {"G", "F", "H", "P"}


def parse(s: str):
    toks = _TOK.findall(s)
    if "".join(toks).replace(" ", "") != s.replace(" ", ""):
        raise ValueError(f"cannot tokenize {s!r}")
    pos = [0]

    def peek():
        return toks[pos[0]] if pos[0] < len(toks) else None

    def eat(t=None):
        x = peek()
        if t is not None and x != t:
            raise ValueError(f"expected {t}, got {x} in {s!r}")
        pos[0] += 1
        return x

    def unary():
        t = peek()
        if t in _UN:
            eat()
            return (_UN[t], unary())
        if t in TENSE and pos[0] + 1 < len(toks) and toks[pos[0] + 1] not in _BIN and toks[pos[0] + 1] != ")":
            eat()
            return (t, unary())
        if t == "(":
            eat()
            f = expr(0)
            eat(")")
            return f
        if t in ("⊤", "top"):
            eat()
            return ("top",)
        if t in ("⊥", "bot"):
            eat()
            return ("bot",)
        eat()
        return ("var", t)

    def expr(min_prec):
        left = unary()
        while peek() in _BIN and _PREC[_BIN[peek()]] >= min_prec:
            op = _BIN[eat()]
            right = expr(_PREC[op] if op in ("imp", "iff") else _PREC[op] + 1)
            left = (op, left, right)
        return left

    f = expr(0)
    if peek() is not None:
        raise ValueError(f"trailing {peek()} in {s!r}")
    return f


def show(f, tex: bool = False) -> str:
    sym = {"not": r"\lnot " if tex else "¬", "box": r"\Box " if tex else "□", "dia": r"\Diamond " if tex else "◇",
           "and": r"\land" if tex else "∧", "or": r"\lor" if tex else "∨", "imp": r"\to" if tex else "→",
           "iff": r"\leftrightarrow" if tex else "↔"}

    def go(g, top=True):
        op = g[0]
        if op == "var":
            return g[1]
        if op == "top":
            return r"\top" if tex else "⊤"
        if op == "bot":
            return r"\bot" if tex else "⊥"
        if op in ("not", "box", "dia") or op in TENSE:
            inner = go(g[1], False)
            s_ = sym.get(op, (rf"\mathsf{{{op}}}\," if tex else op + " "))
            return s_ + (f"({inner})" if g[1][0] in _PREC else inner)
        a, b = go(g[1], False), go(g[2], False)
        if g[1][0] in _PREC and _PREC[g[1][0]] <= _PREC[op]:
            a = f"({a})"
        if g[2][0] in _PREC and _PREC[g[2][0]] < _PREC[op] + (0 if op in ("imp", "iff") else 1):
            b = f"({b})"
        out = f"{a} {sym[op]} {b}"
        return out

    return go(f)


def atoms(f) -> list:
    out = set()

    def go(g):
        if g[0] == "var":
            out.add(g[1])
        elif g[0] not in ("top", "bot"):
            for a in g[1:]:
                go(a)
    go(f)
    return sorted(out)


# ---------------------------------------------------------------------------
# Frames and models
# ---------------------------------------------------------------------------
@dataclass
class Model:
    worlds: list
    R: set
    V: dict = field(default_factory=dict)        # atom -> set of worlds where it is true

    def succ(self, w):
        return [v for v in self.worlds if (w, v) in self.R]

    def pred(self, w):
        return [v for v in self.worlds if (v, w) in self.R]


def holds(f, M: Model, w) -> bool:
    op = f[0]
    if op == "var":
        return w in M.V.get(f[1], set())
    if op == "top":
        return True
    if op == "bot":
        return False
    if op == "not":
        return not holds(f[1], M, w)
    if op == "and":
        return holds(f[1], M, w) and holds(f[2], M, w)
    if op == "or":
        return holds(f[1], M, w) or holds(f[2], M, w)
    if op == "imp":
        return (not holds(f[1], M, w)) or holds(f[2], M, w)
    if op == "iff":
        return holds(f[1], M, w) == holds(f[2], M, w)
    if op in ("box", "G"):
        return all(holds(f[1], M, v) for v in M.succ(w))
    if op in ("dia", "F"):
        return any(holds(f[1], M, v) for v in M.succ(w))
    if op == "H":
        return all(holds(f[1], M, v) for v in M.pred(w))
    if op == "P":
        return any(holds(f[1], M, v) for v in M.pred(w))
    raise ValueError(op)


def truth_set(f, M: Model) -> set:
    return {w for w in M.worlds if holds(f, M, w)}


def all_frames(n: int):
    """Every relation on worlds 0..n-1, as a set of pairs (2^(n*n) of them)."""
    pairs = list(itertools.product(range(n), repeat=2))
    for bits in itertools.product((False, True), repeat=len(pairs)):
        yield {p for p, b in zip(pairs, bits) if b}


def valuations(n: int, names):
    subsets = [frozenset(c) for k in range(n + 1) for c in itertools.combinations(range(n), k)]
    for choice in itertools.product(subsets, repeat=len(names)):
        yield dict(zip(names, choice))


def valid_on_frame(f, R, n: int | None = None) -> bool:
    """Is f true at every world of the frame (W, R) under every valuation?"""
    n = n if n is not None else (1 + max([max(p) for p in R], default=-1))
    W = list(range(n))
    names = atoms(f)
    for V in valuations(n, names):
        M = Model(W, R, V)
        if not all(holds(f, M, w) for w in W):
            return False
    return True


def frame_countermodel(f, R, n: int):
    """A valuation and world refuting f on the frame, or None."""
    W = list(range(n))
    for V in valuations(n, atoms(f)):
        M = Model(W, R, V)
        for w in W:
            if not holds(f, M, w):
                return {k: sorted(v) for k, v in V.items()}, w
    return None


# frame conditions
def reflexive(R, n):
    return all((w, w) in R for w in range(n))


def symmetric(R, n):
    return all((v, u) in R for u, v in R)


def transitive(R, n):
    return all((u, x) in R for u, v in R for w, x in R if v == w)


def euclidean(R, n):
    return all((v, x) in R for u, v in R for w, x in R if u == w)


def serial(R, n):
    return all(any((w, v) in R for v in range(n)) for w in range(n))


def irreflexive(R, n):
    return all((w, w) not in R for w in range(n))


def converse_wellfounded(R, n):
    """No infinite R-chain w0 R w1 R w2 ...: on a finite frame, no cycle (R restricted to n worlds is acyclic)."""
    color = {}

    def dfs(u):
        color[u] = 1
        for a, b in R:
            if a == u:
                if color.get(b) == 1:
                    return False
                if color.get(b) is None and not dfs(b):
                    return False
        color[u] = 2
        return True
    return all(color.get(w) == 2 or dfs(w) for w in range(n))


AXIOMS = {
    "K": ("[](p -> q) -> ([]p -> []q)", None),
    "T": ("[]p -> p", reflexive),
    "D": ("[]p -> <>p", serial),
    "B": ("p -> []<>p", symmetric),
    "4": ("[]p -> [][]p", transitive),
    "5": ("<>p -> []<>p", euclidean),
    "L": ("[]([]p -> p) -> []p", lambda R, n: transitive(R, n) and converse_wellfounded(R, n)),
}


def correspondence(name: str, n: int) -> dict:
    """Check an axiom against its frame condition on every frame with n worlds: counts and any mismatch."""
    f = parse(AXIOMS[name][0])
    cond = AXIOMS[name][1]
    valid = agree = 0
    mismatch = None
    total = 0
    for R in all_frames(n):
        total += 1
        v = valid_on_frame(f, R, n)
        valid += v
        c = cond(R, n) if cond else True
        if v == c:
            agree += 1
        elif mismatch is None:
            mismatch = sorted(R)
    return {"axiom": name, "formula": AXIOMS[name][0], "worlds": n, "frames": total, "valid": valid,
            "agree": agree, "mismatch": mismatch}


# ---------------------------------------------------------------------------
# Model finding (satisfiability in a class of frames)
# ---------------------------------------------------------------------------
def find_model(fs, max_worlds: int = 3, frame_ok=None):
    """A smallest model (worlds 0..n-1, world 0 the one where all of fs hold) whose frame passes frame_ok."""
    names = sorted({a for f in fs for a in atoms(f)})
    for n in range(1, max_worlds + 1):
        for R in all_frames(n):
            if frame_ok and not frame_ok(R, n):
                continue
            for V in valuations(n, names):
                M = Model(list(range(n)), R, V)
                if all(holds(f, M, 0) for f in fs):
                    return M
    return None


# ---------------------------------------------------------------------------
# Bisimulation
# ---------------------------------------------------------------------------
def bisimulation(M1: Model, M2: Model, props=None) -> set:
    """The largest bisimulation between two finite models (pairs (u, v)), by refinement."""
    props = props if props is not None else sorted(set(M1.V) | set(M2.V))
    Z = {(u, v) for u in M1.worlds for v in M2.worlds
         if all((u in M1.V.get(p, set())) == (v in M2.V.get(p, set())) for p in props)}
    changed = True
    while changed:
        changed = False
        for u, v in list(Z):
            forth = all(any((u2, v2) in Z for v2 in M2.succ(v)) for u2 in M1.succ(u))
            back = all(any((u2, v2) in Z for u2 in M1.succ(u)) for v2 in M2.succ(v))
            if not (forth and back):
                Z.discard((u, v))
                changed = True
    return Z


def minimize(M: Model, props=None):
    """The bisimulation quotient: blocks of bisimilar worlds, and the smallest model equivalent to M."""
    Z = bisimulation(M, M, props)
    blocks: list[list] = []
    for w in M.worlds:
        for b in blocks:
            if (w, b[0]) in Z:
                b.append(w)
                break
        else:
            blocks.append([w])
    idx = {w: i for i, b in enumerate(blocks) for w in b}
    R = {(idx[u], idx[v]) for u, v in M.R}
    V = {p: {idx[w] for w in ws} for p, ws in M.V.items()}
    return blocks, Model(list(range(len(blocks))), R, V)


# ---------------------------------------------------------------------------
# Explicit-state model checking
# ---------------------------------------------------------------------------
@dataclass
class System:
    """A transition system: states (hashable), initial states, successor function, and a labelling."""
    init: list
    step: object                      # state -> list of (action, next_state)
    label: object                     # state -> set of atomic propositions

    def explore(self, limit: int = 100000):
        """Breadth-first reachable states, with each one's parent (for traces)."""
        parent = {s: None for s in self.init}
        order = list(self.init)
        q = deque(self.init)
        while q and len(parent) < limit:
            s = q.popleft()
            for act, t in self.step(s):
                if t not in parent:
                    parent[t] = (s, act)
                    order.append(t)
                    q.append(t)
        return order, parent

    def check_invariant(self, good):
        """Is good(s) true in every reachable state? If not, a shortest trace to a bad state."""
        order, parent = self.explore()
        for s in order:
            if not good(s):
                trace = [s]
                while parent[trace[-1]] is not None:
                    trace.append(parent[trace[-1]][0])
                return False, list(reversed(trace)), len(order)
        return True, None, len(order)

    def graph(self):
        order, _ = self.explore()
        edges = {(s, t) for s in order for _, t in self.step(s)}
        return order, edges


def ctl_eu(states, edges, phi, psi) -> set:
    """E[phi U psi]: least fixed point."""
    Z = set(psi)
    pred = {}
    for s, t in edges:
        pred.setdefault(t, []).append(s)
    q = deque(Z)
    while q:
        t = q.popleft()
        for s in pred.get(t, []):
            if s not in Z and s in phi:
                Z.add(s)
                q.append(s)
    return Z


def ctl_eg(states, edges, phi) -> set:
    """EG phi: greatest fixed point (states with an infinite path staying in phi)."""
    Z = set(phi)
    succ = {}
    for s, t in edges:
        succ.setdefault(s, []).append(t)
    changed = True
    while changed:
        changed = False
        for s in list(Z):
            if not any(t in Z for t in succ.get(s, [])):
                Z.discard(s)
                changed = True
    return Z


def ctl_ex(states, edges, phi) -> set:
    return {s for s, t in edges if t in phi}


# ---------------------------------------------------------------------------
# Peterson's mutual exclusion (1981), and a broken variant
# ---------------------------------------------------------------------------
# A state is (pc0, pc1, flag0, flag1, turn). Each process i runs:
#   0 idle -> 1: flag[i] = True -> 2: turn = 1 - i -> 3: wait until not flag[1-i] or turn == i -> 4: critical
#   -> 0: flag[i] = False
# The broken variant swaps lines 1 and 2 (turn is set before the flag): mutual exclusion fails.
PETERSON_PC = {0: "idle", 1: "set flag", 2: "give turn", 3: "wait", 4: "critical"}


def peterson(broken: bool = False) -> System:
    def step(s):
        pc, flag, turn = [s[0], s[1]], [s[2], s[3]], s[4]
        out = []
        for i in (0, 1):
            j = 1 - i
            p2, f2, t2 = list(pc), list(flag), turn
            c = pc[i]
            if c == 0:
                p2[i] = 1
            elif c == 1:
                if broken:
                    t2 = j
                else:
                    f2[i] = True
                p2[i] = 2
            elif c == 2:
                if broken:
                    f2[i] = True
                else:
                    t2 = j
                p2[i] = 3
            elif c == 3:
                if not flag[j] or turn == i:
                    p2[i] = 4
                else:
                    continue                       # blocked: no move for this process
            elif c == 4:
                p2[i] = 0
                f2[i] = False
            out.append((f"P{i}: {PETERSON_PC[c]}", (p2[0], p2[1], f2[0], f2[1], t2)))
        return out

    def label(s):
        out = set()
        for i in (0, 1):
            if s[i] == 4:
                out.add(f"crit{i}")
            if s[i] in (1, 2, 3):
                out.add(f"try{i}")
        return out

    return System([(0, 0, False, False, 0)], step, label)


def mutual_exclusion(sys_: System):
    """Check AG not(crit0 and crit1); return (holds, shortest counterexample trace, reachable states)."""
    return sys_.check_invariant(lambda s: not (s[0] == 4 and s[1] == 4))


def deadlock_free(sys_: System):
    states, edges = sys_.graph()
    succ = {s for s, _ in edges}
    dead = [s for s in states if s not in succ]
    return not dead, dead


def _sccs(nodes: set, succ: dict) -> list:
    """Tarjan's strongly connected components of the subgraph on ``nodes``."""
    index, low, on, stack, out = {}, {}, set(), [], []
    counter = [0]

    def visit(v):
        index[v] = low[v] = counter[0]
        counter[0] += 1
        stack.append(v)
        on.add(v)
        for w in succ.get(v, ()):
            if w not in nodes:
                continue
            if w not in index:
                visit(w)
                low[v] = min(low[v], low[w])
            elif w in on:
                low[v] = min(low[v], index[w])
        if low[v] == index[v]:
            comp = set()
            while True:
                w = stack.pop()
                on.discard(w)
                comp.add(w)
                if w == v:
                    break
            out.append(comp)

    import sys
    old = sys.getrecursionlimit()
    sys.setrecursionlimit(max(old, 10000))
    for v in nodes:
        if v not in index:
            visit(v)
    sys.setrecursionlimit(old)
    return out


def fair_eg(sys_: System, phi, procs=("P0", "P1")) -> set:
    """States with an infinite path that stays in phi and is strongly fair to every process (a process enabled
    infinitely often moves infinitely often). Actions are labelled 'Pi: ...'. Emerson-Lei style SCC refinement."""
    states, _ = sys_.explore()
    moves = {s: sys_.step(s) for s in states}
    succ = {s: [t for _, t in moves[s]] for s in states}
    enabled = {s: {a.split(":")[0] for a, _ in moves[s]} for s in states}
    good = {s for s in states if phi(s)}

    def fair_core(C):
        """The states of C that lie on a fair cycle inside C."""
        work = [C]
        found = set()
        while work:
            X = work.pop()
            for comp in _sccs(X, succ):
                internal = [(s, a) for s in comp for a, t in moves[s] if t in comp]
                if not internal:
                    continue
                bad = set()
                for p in procs:
                    if any(a.startswith(p) for _, a in internal):
                        continue
                    bad |= {s for s in comp if p in enabled[s]}
                if not bad:
                    found |= comp
                elif comp - bad:
                    work.append(comp - bad)
        return found

    core = fair_core(good)
    # backward reachability to the fair core, inside good
    Z = set(core)
    pred: dict = {}
    for s in states:
        for t in succ[s]:
            pred.setdefault(t, []).append(s)
    q = deque(Z)
    while q:
        t = q.popleft()
        for s in pred.get(t, []):
            if s in good and s not in Z:
                Z.add(s)
                q.append(s)
    return Z


# ---------------------------------------------------------------------------
# Prefixed tableaux for K (and T, by making every world see itself)
# ---------------------------------------------------------------------------
def _neg(f):
    return f[1] if f[0] == "not" else ("not", f)


def tableau(f, reflexive_: bool = False, max_worlds: int = 12):
    """Is f valid in K (or T)? A prefixed tableau for the negation of f: returns (valid, steps, countermodel).
    Steps are (rule, world, formula_text, branch_id) in the order applied; the countermodel (from the first open,
    saturated branch) is a Model, with world 0 refuting f."""
    steps = []
    counter = [0]

    def expand(todo, facts, R, worlds, bid):
        # facts: set of (w, formula); todo: list of (w, formula) not yet processed
        todo = list(todo)
        while todo:
            w, g = todo.pop(0)
            if (w, _neg(g)) in facts or g == ("bot",) or (g[0] == "not" and g[1] == ("top",)):
                steps.append(("close", w, show(g), bid))
                return None
            if (w, g) in facts and g[0] != "box":
                continue
            facts = facts | {(w, g)}
            op = g[0]
            neg = op == "not"
            h = g[1] if neg else None
            if op in ("var", "top", "bot") or (neg and h[0] in ("var", "top", "bot")):
                continue
            if neg and h[0] == "not":
                todo.append((w, h[1]))
                steps.append(("not-not", w, show(g), bid))
            elif op == "and" or (neg and h[0] in ("or", "imp")):
                a, b = (g[1], g[2]) if op == "and" else ((_neg(h[1]), _neg(h[2])) if h[0] == "or"
                                                           else (h[1], _neg(h[2])))
                todo += [(w, a), (w, b)]
                steps.append(("alpha", w, show(g), bid))
            elif op in ("or", "imp") or (neg and h[0] == "and"):
                a, b = ((g[1], g[2]) if op == "or" else (_neg(g[1]), g[2])) if not neg else (_neg(h[1]), _neg(h[2]))
                steps.append(("beta", w, show(g), bid))
                counter[0] += 1
                left = expand(todo + [(w, a)], facts, R, worlds, bid)
                if left is not None:
                    return left
                return expand(todo + [(w, b)], facts, R, worlds, counter[0])
            elif op == "iff" or (neg and h[0] == "iff"):
                x, y = (g[1], g[2]) if not neg else (h[1], h[2])
                pos_ = [(w, x), (w, y)] if not neg else [(w, x), (w, _neg(y))]
                negs = [(w, _neg(x)), (w, _neg(y))] if not neg else [(w, _neg(x)), (w, y)]
                steps.append(("beta", w, show(g), bid))
                counter[0] += 1
                left = expand(todo + pos_, facts, R, worlds, bid)
                if left is not None:
                    return left
                return expand(todo + negs, facts, R, worlds, counter[0])
            elif op == "box" or (neg and h[0] == "dia"):
                body = g[1] if op == "box" else _neg(h[1])
                facts = facts | {(w, ("box", body))}
                for (u, v) in R:
                    if u == w:
                        todo.append((v, body))
                steps.append(("nu", w, show(g), bid))
            elif op == "dia" or (neg and h[0] == "box"):
                body = g[1] if op == "dia" else _neg(h[1])
                if len(worlds) >= max_worlds:
                    raise RuntimeError("too many worlds")
                v = len(worlds)
                worlds = worlds + [v]
                R = R | {(w, v)} | ({(v, v)} if reflexive_ else set())
                todo.append((v, body))
                for (u, b) in facts:
                    if b[0] == "box" and (u == w or (reflexive_ and u == v)):
                        todo.append((v, b[1]))
                steps.append(("pi", w, show(g) + f"  ->  w{v}", bid))
            else:
                raise ValueError(g)
        V = {}
        for (w, g) in facts:
            if g[0] == "var":
                V.setdefault(g[1], set()).add(w)
        return Model(worlds, R, V)

    R0 = {(0, 0)} if reflexive_ else set()
    start = [(0, ("not", f))]
    if reflexive_:
        pass
    M = expand(start, frozenset(), R0, [0], 0)
    if M is not None:
        assert not holds(f, M, 0)
    return M is None, steps, M
