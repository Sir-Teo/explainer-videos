"""Explicit-state model checking (Part 54, chapter 7; and the TLA+ chapter 12).

    m = peterson()                          # a guarded-command model: variables, initial states, commands, props
    K = build(m)                            # its Kripke structure: every reachable state, transitions, labels
    holds(K, ("AG", ("not", ("and", "cs0", "cs1"))))           # CTL by fixpoints
    response(K, "try0", "cs0", fairness=weak_fairness(m, ...))  # G(try0 -> F cs0): a fair lasso, or None

A **model** is a set of variables, initial states and guarded commands ``(action, guard, update)``, in the style of
Dijkstra's guarded commands and of TLA+ actions (Lamport, *Specifying Systems*, 2002).  :func:`build` explores it
breadth first into a **Kripke structure** (states, initial states, a transition relation, a labelling with atomic
propositions); a state with no enabled command is labelled ``deadlock`` and given a stuttering self-loop, so that
every path is infinite, as CTL and LTL semantics need.  Because the search is breadth first, the path it records to a
state is a shortest one, and so every counterexample reported here is a shortest one.

**CTL** (Clarke and Emerson 1981) is checked by the classical fixpoints: EX by predecessors, E[f U g] as a least
fixpoint, EG f as a greatest fixpoint, and AX, AF, AG, EF, A[f U g] from them by duality (Clarke, Emerson and Sistla
1986; Huth and Ryan, *Logic in Computer Science*, ch. 3; Baier and Katoen, *Principles of Model Checking*, ch. 6).

**LTL** response properties G(p -> F q) are checked as Baier and Katoen do for liveness (ch. 5): the property fails
exactly when some reachable p-state that is not a q-state starts an infinite *fair* path that avoids q for ever;
on a finite structure that path is a lasso into a strongly connected component of the q-avoiding states.  Fairness
is over sets of actions: **weak** (justice: an action continuously enabled from some point on is taken infinitely
often) and **strong** (compassion: an action enabled infinitely often is taken infinitely often); a component is
fair for a strong constraint it fails once the states that enable the action are removed and the rest re-examined
(Emerson and Lei 1987).

Models: Peterson (1981) and a broken variant that raises its flag too late; the dining philosophers (Dijkstra 1971),
naive and with a global fork order; Lamport's TCommit and TwoPhase specifications of two-phase commit (Gray and
Lamport, "Consensus on Transaction Commit", 2006), with a coordinator that commits on a timeout as the bug; and a
small abstract Raft election (Ongaro and Ousterhout 2014) for election safety.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field

STUTTER = "stutter"


# ------------------------------------------------------------------------------------------- models and structures

@dataclass
class Model:
    """Guarded commands over a tuple-valued state.  ``commands`` are ``(action, guard(s) -> bool, update(s) ->
    state)``; ``props`` map an atomic proposition to a predicate on states; ``show`` turns a state into a JSON-friendly
    dict for traces."""
    name: str
    vars: tuple
    init: list
    commands: list
    props: dict
    show_fn: object = None

    def show(self, s) -> dict:
        if self.show_fn is not None:
            return self.show_fn(s)
        return dict(zip(self.vars, s))

    def step(self, s):
        """The enabled commands of ``s`` and their successors, as (action, next state)."""
        return [(a, u(s)) for a, g, u in self.commands if g(s)]


@dataclass
class Kripke:
    model: Model
    states: list                  # id -> state
    index: dict                   # state -> id
    init: list                    # ids of initial states
    succ: list                    # id -> [(action, id)]
    labels: list                  # id -> frozenset of atomic propositions
    parent: list                  # id -> (parent id, action) on a shortest path from an initial state, or None
    depth: list                   # id -> length of that shortest path
    deadlocks: list = field(default_factory=list)
    _pred: list | None = None

    @property
    def n(self) -> int:
        return len(self.states)

    def edges(self) -> int:
        return sum(len(s) for s in self.succ)

    def pred(self) -> list:
        if self._pred is None:
            self._pred = [[] for _ in self.states]
            for i, out in enumerate(self.succ):
                for _, j in out:
                    self._pred[j].append(i)
        return self._pred

    def path_to(self, i) -> list:
        """Shortest path from an initial state to ``i``: [(action or None, id)], starting with (None, initial)."""
        out = []
        while self.parent[i] is not None:
            p, a = self.parent[i]
            out.append((a, i))
            i = p
        out.append((None, i))
        return out[::-1]

    def trace(self, path) -> list[dict]:
        """A path as JSON: one {"action", "state"} per step."""
        return [{"action": a, "state": self.model.show(self.states[i])} for a, i in path]


def build(m: Model, limit: int = 3_000_000) -> Kripke:
    """Breadth-first exploration of every reachable state of ``m``."""
    index, states, succ, labels, parent, depth = {}, [], [], [], [], []
    q = deque()
    for s in m.init:
        if s not in index:
            index[s] = len(states)
            states.append(s)
            parent.append(None)
            depth.append(0)
            q.append(s)
    init = list(range(len(states)))
    deadlocks = []
    while q:
        s = q.popleft()
        i = index[s]
        out = []
        for a, t in m.step(s):
            j = index.get(t)
            if j is None:
                j = index[t] = len(states)
                states.append(t)
                parent.append((i, a))
                depth.append(depth[i] + 1)
                q.append(t)
                if len(states) > limit:
                    raise RuntimeError("state space too large")
            out.append((a, j))
        lab = {p for p, f in m.props.items() if f(s)}
        if not out:
            out = [(STUTTER, i)]
            lab.add("deadlock")
            deadlocks.append(i)
        succ.append(out)
        labels.append(frozenset(lab))
    return Kripke(m, states, index, init, succ, labels, parent, depth, deadlocks)


# ------------------------------------------------------------------------------------------------------------- CTL

def show(f) -> str:
    """A formula in the usual notation."""
    if isinstance(f, str):
        return f
    op = f[0]
    if op == "not":
        return "¬" + _paren(f[1])
    if op in ("and", "or", "imp"):
        sym = {"and": " ∧ ", "or": " ∨ ", "imp": " → "}[op]
        return _paren(f[1]) + sym + _paren(f[2])
    if op in ("EU", "AU"):
        return f"{op[0]}[{show(f[1])} U {show(f[2])}]"
    return f"{op} " + _paren(f[1])


def _paren(f) -> str:
    s = show(f)
    return s if isinstance(f, str) or f[0] in ("not", "EX", "AX", "EF", "AF", "EG", "AG", "EU", "AU") else f"({s})"


def sat(K: Kripke, f) -> set:
    """The set of states satisfying the CTL formula ``f``: an atomic proposition (a string; "true" and "false"
    included) or a tuple ("not", f), ("and"/"or"/"imp", f, g), ("EX"/"AX"/"EF"/"AF"/"EG"/"AG", f),
    ("EU"/"AU", f, g)."""
    allst = set(range(K.n))
    if isinstance(f, str):
        if f == "true":
            return allst
        if f == "false":
            return set()
        return {i for i in range(K.n) if f in K.labels[i]}
    op = f[0]
    if op == "not":
        return allst - sat(K, f[1])
    if op == "and":
        return sat(K, f[1]) & sat(K, f[2])
    if op == "or":
        return sat(K, f[1]) | sat(K, f[2])
    if op == "imp":
        return (allst - sat(K, f[1])) | sat(K, f[2])
    if op == "EX":
        return ex(K, sat(K, f[1]))
    if op == "EU":
        return eu(K, sat(K, f[1]), sat(K, f[2]))
    if op == "EG":
        return eg(K, sat(K, f[1]))
    if op == "AX":
        return allst - ex(K, allst - sat(K, f[1]))
    if op == "EF":
        return eu(K, allst, sat(K, f[1]))
    if op == "AF":
        return allst - eg(K, allst - sat(K, f[1]))
    if op == "AG":
        return allst - eu(K, allst, allst - sat(K, f[1]))
    if op == "AU":                     # A[f U g] = ¬(E[¬g U (¬f ∧ ¬g)] ∨ EG ¬g)
        a, b = sat(K, f[1]), sat(K, f[2])
        ng = allst - b
        return allst - (eu(K, ng, ng - a) | eg(K, ng))
    raise ValueError(f"unknown operator {op}")


def ex(K: Kripke, Y: set) -> set:
    """EX: states with some successor in Y."""
    pred = K.pred()
    return {p for y in Y for p in pred[y]}


def eu(K: Kripke, F: set, G: set) -> set:
    """E[F U G], the least fixpoint Z = G ∪ (F ∩ EX Z): backward search from G through F."""
    pred = K.pred()
    Z = set(G)
    work = list(G)
    while work:
        y = work.pop()
        for p in pred[y]:
            if p not in Z and p in F:
                Z.add(p)
                work.append(p)
    return Z


def eg(K: Kripke, F: set) -> set:
    """EG F, the greatest fixpoint Z = F ∩ EX Z: repeatedly delete F-states with no successor left in Z."""
    pred = K.pred()
    Z = set(F)
    count = {i: sum(1 for _, j in K.succ[i] if j in Z) for i in Z}
    work = [i for i in Z if count[i] == 0]
    while work:
        i = work.pop()
        if i not in Z:
            continue
        Z.discard(i)
        for p in pred[i]:
            if p in Z:
                count[p] -= 1
                if count[p] == 0:
                    work.append(p)
    return Z


def holds(K: Kripke, f) -> bool:
    """K ⊨ f: every initial state satisfies f."""
    S = sat(K, f)
    return all(i in S for i in K.init)


def counterexample(K: Kripke, f) -> list | None:
    """For an invariant AG f that fails: a shortest path from an initial state to a state violating f."""
    S = sat(K, f)
    bad = [i for i in range(K.n) if i not in S]
    if not bad:
        return None
    return K.path_to(min(bad, key=lambda i: K.depth[i]))


# -------------------------------------------------------------------------------------- fairness and LTL liveness

def _enabled(K: Kripke, i: int, A) -> bool:
    return any(a in A for a, _ in K.succ[i])


def _sccs(nodes: set, succ_in) -> list[set]:
    """Tarjan's strongly connected components (iterative) of the graph on ``nodes``."""
    index, low, on, stack, out = {}, {}, set(), [], []
    counter = 0
    for root in nodes:
        if root in index:
            continue
        work = [(root, iter(succ_in(root)))]
        index[root] = low[root] = counter
        counter += 1
        stack.append(root)
        on.add(root)
        while work:
            v, it = work[-1]
            pushed = False
            for w in it:
                if w not in index:
                    index[w] = low[w] = counter
                    counter += 1
                    stack.append(w)
                    on.add(w)
                    work.append((w, iter(succ_in(w))))
                    pushed = True
                    break
                if w in on:
                    low[v] = min(low[v], index[w])
            if pushed:
                continue
            work.pop()
            if work:
                low[work[-1][0]] = min(low[work[-1][0]], low[v])
            if low[v] == index[v]:
                comp = set()
                while True:
                    w = stack.pop()
                    on.discard(w)
                    comp.add(w)
                    if w == v:
                        break
                out.append(comp)
    return out


def _fair_component(K: Kripke, nodes: set, fairness) -> set | None:
    """A strongly connected set of ``nodes`` with a cycle that can be traversed fairly, or None."""
    def succ_in(i):
        return [j for _, j in K.succ[i] if j in nodes]
    for C in _sccs(nodes, succ_in):
        if not any(j in C for i in C for _, j in K.succ[i]):
            continue                                   # a single state without a self-loop: no cycle
        ok, shrink = True, None
        for kind, A in fairness:
            taken = any(a in A and j in C for i in C for a, j in K.succ[i])
            if taken:
                continue
            en = {i for i in C if _enabled(K, i, A)}
            if kind == "weak":
                if len(en) == len(C):                  # continuously enabled, never taken: no sub-cycle helps
                    ok = False
                    break
            else:                                      # strong: must avoid every state enabling A
                if en:
                    ok, shrink = False, en
                    break
        if ok:
            return C
        if shrink is not None:
            sub = _fair_component(K, C - shrink, fairness)
            if sub is not None:
                return sub
    return None


def _bfs_within(K: Kripke, src: int, dst_pred, allowed: set) -> list:
    """Shortest path inside ``allowed`` from src to a state satisfying dst_pred: [(action, id)] without src."""
    if dst_pred(src):
        return []
    par = {src: None}
    q = deque([src])
    while q:
        i = q.popleft()
        for a, j in K.succ[i]:
            if j in allowed and j not in par:
                par[j] = (i, a)
                if dst_pred(j):
                    out = []
                    while par[j] is not None:
                        p, b = par[j]
                        out.append((b, j))
                        j = p
                    return out[::-1]
                q.append(j)
    raise ValueError("no path")


def fair_lasso(K: Kripke, starts, region: set, fairness=()) -> dict | None:
    """An infinite fair path that starts at one of ``starts`` and stays in ``region`` for ever, as a lasso
    {"start", "stem", "cycle"} of [(action, id)] steps (the cycle returns to the stem's last state), or None."""
    starts = [s for s in starts if s in region]
    par = {s: None for s in starts}
    q = deque(starts)
    while q:
        i = q.popleft()
        for a, j in K.succ[i]:
            if j in region and j not in par:
                par[j] = (i, a)
                q.append(j)
    C = _fair_component(K, set(par), list(fairness))
    if C is None:
        return None
    entry = next(i for i in par if i in C)            # par keeps BFS order: the first C-state found is nearest
    stem = []
    j = entry
    while par[j] is not None:
        p, a = par[j]
        stem.append((a, j))
        j = p
    start = j
    stem = stem[::-1]
    cycle, cur = [], entry
    for kind, A in fairness:
        edge = next(((i, a, j) for i in C for a, j in K.succ[i] if a in A and j in C), None)
        if edge is not None:
            u, a, v = edge
            cycle += _bfs_within(K, cur, lambda x, u=u: x == u, C) + [(a, v)]
            cur = v
        elif kind == "weak":
            seg = _bfs_within(K, cur, lambda x, A=A: not _enabled(K, x, A), C)
            cycle += seg
            cur = seg[-1][1] if seg else cur
    if not cycle and cur == entry:                     # still need one step round the cycle
        a, v = next((a, j) for a, j in K.succ[entry] if j in C)
        cycle.append((a, v))
        cur = v
    if cur != entry:
        cycle += _bfs_within(K, cur, lambda x: x == entry, C)
    return {"start": start, "stem": stem, "cycle": cycle}


def response(K: Kripke, trigger, goal, fairness=()) -> dict:
    """Check the LTL property G(trigger → F goal) (formulas as for :func:`sat`, evaluated state by state).  It fails
    exactly when a reachable (trigger ∧ ¬goal)-state starts a fair path that never meets goal."""
    G = sat(K, goal)
    region = set(range(K.n)) - G
    starts = sorted(sat(K, trigger) - G, key=lambda i: K.depth[i])
    lasso = fair_lasso(K, starts, region, fairness)
    out = {"property": f"G({show(trigger)} → F {show(goal)})", "holds": lasso is None,
           "fairness": [[k, sorted(A)] for k, A in fairness]}
    if lasso is not None:
        out["prefix"] = K.trace(K.path_to(lasso["start"]) + lasso["stem"])
        out["cycle"] = K.trace(lasso["cycle"])
        out["lasso"] = lasso
    return out


def check_lasso(K: Kripke, lasso: dict, region: set, fairness) -> bool:
    """Independent check of a lasso: every step is a transition, the cycle closes, it stays in the region, and each
    fairness constraint is met on the cycle (taken, or for weak fairness disabled somewhere, or for strong fairness
    disabled everywhere)."""
    cur = lasso["start"]
    for a, j in lasso["stem"] + lasso["cycle"]:
        if (a, j) not in K.succ[cur] or j not in region:
            return False
        cur = j
    entry = lasso["stem"][-1][1] if lasso["stem"] else lasso["start"]
    if cur != entry or not lasso["cycle"]:
        return False
    on = [entry] + [j for _, j in lasso["cycle"]]
    for kind, A in fairness:
        if any(a in A for a, _ in lasso["cycle"]):
            continue
        dis = [not _enabled(K, i, A) for i in on]
        if not (any(dis) if kind == "weak" else all(dis)):
            return False
    return True


def actions(m: Model, *prefixes) -> set:
    """The names of the commands of ``m`` starting with any of these prefixes."""
    return {a for a, _, _ in m.commands if a.startswith(prefixes)}


# ----------------------------------------------------------------------------------------------------- Peterson

PC = {0: "ncs", 1: "flag", 2: "wait", 3: "cs"}


def peterson(broken: bool = False, idle: bool = True) -> Model:
    """Peterson's algorithm for two processes as guarded commands over (pc0, pc1, flag0, flag1, turn).

    Process i:  ncs --req--> flag[i] := 1  --turn--> turn := j  --enter, when ¬flag[j] ∨ turn = i--> cs
    --exit--> flag[i] := 0, back to ncs.  ``idle`` lets a process stay in its non-critical section (a self-loop),
    as it may for ever.  ``broken``: the flag is raised *after* writing turn (the order of the first two steps
    swapped), which lets both processes in."""
    def put(s, **kw):
        s = list(s)
        for k, v in kw.items():
            s[VI[k]] = v
        return tuple(s)
    V = ("pc0", "pc1", "flag0", "flag1", "turn")
    VI = {v: i for i, v in enumerate(V)}
    cmds = []
    for i in (0, 1):
        j = 1 - i
        pc, fl, fj = f"pc{i}", f"flag{i}", f"flag{j}"
        p, g = VI[pc], VI[fj]
        if idle:
            cmds.append((f"idle{i}", lambda s, p=p: s[p] == 0, lambda s: s))
        if not broken:
            cmds.append((f"req{i}", lambda s, p=p: s[p] == 0, lambda s, pc=pc, fl=fl: put(s, **{pc: 1, fl: 1})))
            cmds.append((f"turn{i}", lambda s, p=p: s[p] == 1, lambda s, pc=pc, j=j: put(s, **{pc: 2, "turn": j})))
        else:
            cmds.append((f"req{i}", lambda s, p=p: s[p] == 0, lambda s, pc=pc, j=j: put(s, **{pc: 1, "turn": j})))
            cmds.append((f"turn{i}", lambda s, p=p: s[p] == 1, lambda s, pc=pc, fl=fl: put(s, **{pc: 2, fl: 1})))
        cmds.append((f"enter{i}", lambda s, p=p, g=g, i=i: s[p] == 2 and (s[g] == 0 or s[4] == i),
                     lambda s, pc=pc: put(s, **{pc: 3})))
        cmds.append((f"exit{i}", lambda s, p=p: s[p] == 3, lambda s, pc=pc, fl=fl: put(s, **{pc: 0, fl: 0})))
    props = {"cs0": lambda s: s[0] == 3, "cs1": lambda s: s[1] == 3,
             "try0": lambda s: s[0] in (1, 2), "try1": lambda s: s[1] in (1, 2),
             "ncs0": lambda s: s[0] == 0, "ncs1": lambda s: s[1] == 0}
    return Model("peterson-broken" if broken else "peterson", V, [(0, 0, 0, 0, 0)], cmds, props,
                 lambda s: {"pc0": PC[s[0]], "pc1": PC[s[1]], "flag0": s[2], "flag1": s[3], "turn": s[4]})


def process_fairness(m: Model, kind: str = "weak") -> list:
    """One fairness constraint per Peterson process, over its actions after the request (the non-critical
    section may last for ever; nothing else may stop)."""
    return [(kind, actions(m, f"turn{i}", f"enter{i}", f"exit{i}")) for i in (0, 1)]


MUTEX = ("AG", ("not", ("and", "cs0", "cs1")))


def peterson_results() -> dict:
    """Peterson checked: mutual exclusion (CTL), response with and without weak fairness (LTL, with the lasso
    that starves a process when there is no fairness), a few more CTL facts, the broken variant's shortest
    counterexample, and the verdicts of Part 33's interleaving checker on the same two algorithms."""
    m = peterson()
    K = build(m)
    ctl = [MUTEX, ("AG", ("imp", "try0", ("AF", "cs0"))), ("AG", ("imp", "try0", ("EF", "cs0"))),
           ("AG", ("EF", ("and", "ncs0", "ncs1"))), ("EF", "cs0"), ("AG", ("not", "deadlock"))]
    out = {"states": K.n, "edges": K.edges(),
           "ctl": [{"formula": show(f), "holds": holds(K, f)} for f in ctl],
           "response_unfair": _strip(response(K, "try0", "cs0")),
           "response_weak": [_strip(response(K, f"try{i}", f"cs{i}", process_fairness(m))) for i in (0, 1)]}
    mb = peterson(broken=True)
    Kb = build(mb)
    out["broken"] = {"states": Kb.n, "mutex": holds(Kb, MUTEX),
                     "counterexample": Kb.trace(counterexample(Kb, MUTEX[1]))}
    out["part33"] = part33_agreement()
    return out


def _strip(r: dict) -> dict:
    return {k: v for k, v in r.items() if k != "lasso"}


def part33_agreement() -> dict:
    """The same two algorithms on Part 33's checker (explainer/cs/conc/mc.py, sequential consistency): its
    ``peterson()``, and the flag-too-late variant written as a Part 33 program; the mutual-exclusion verdicts
    must agree with ours."""
    from explainer.cs.conc import mc
    r = mc.explore(mc.peterson(), "sc", invariant=mc.mutex)
    ths = []
    for i in (0, 1):
        j = 1 - i
        ths.append([("st", "turn", j), ("st", f"flag{i}", 1), ("label", "w"), ("ld", "f", f"flag{j}"),
                    ("beq", "f", 0, "in"), ("ld", "t", "turn"), ("beq", "t", j, "w"), ("label", "in"),
                    ("cs",), ("ncs",), ("st", f"flag{i}", 0)])
    rb = mc.explore(mc.Program({"flag0": 0, "flag1": 0, "turn": 0}, ths, ["P0", "P1"]), "sc", invariant=mc.mutex)
    ours = holds(build(peterson()), MUTEX)
    ours_b = holds(build(peterson(broken=True)), MUTEX)
    return {"part33_states": r.states, "part33_mutex": r.violation is None, "ours_mutex": ours,
            "broken_part33_states": rb.states, "broken_part33_mutex": rb.violation is None,
            "broken_ours_mutex": ours_b,
            "broken_part33_trace": rb.trace(rb.violation) if rb.violation is not None else None,
            "agree": (r.violation is None) == ours and (rb.violation is None) == ours_b}


# ----------------------------------------------------------------------------------------- dining philosophers

def forks(n: int, ordered: bool = False) -> list[tuple[int, int]]:
    """(first, second) fork of each philosopher: left (i) then right (i + 1 mod n); with ``ordered`` the last one
    takes the lower-numbered fork 0 first, so forks are always taken in increasing order (a global lock order)."""
    fs = [(i, (i + 1) % n) for i in range(n)]
    if ordered:
        fs[-1] = (fs[-1][1], fs[-1][0])
    return fs


def philosophers(n: int, ordered: bool = False) -> Model:
    """Each philosopher is thinking (0), holding its first fork (1) or eating with both (2); a fork is free when
    nobody holds it.  Commands: take1_i (pick up the first fork), take2_i (the second), release_i (put both down)."""
    fs = forks(n, ordered)

    def free(s, f):
        return not any((a == f and s[p] >= 1) or (b == f and s[p] == 2) for p, (a, b) in enumerate(fs))

    def put(s, i, v):
        return s[:i] + (v,) + s[i + 1:]
    cmds = []
    for i, (a, b) in enumerate(fs):
        cmds.append((f"take1_{i}", lambda s, i=i, a=a: s[i] == 0 and free(s, a), lambda s, i=i: put(s, i, 1)))
        cmds.append((f"take2_{i}", lambda s, i=i, b=b: s[i] == 1 and free(s, b), lambda s, i=i: put(s, i, 2)))
        cmds.append((f"release_{i}", lambda s, i=i: s[i] == 2, lambda s, i=i: put(s, i, 0)))
    props = {}
    for i in range(n):
        props[f"eat{i}"] = lambda s, i=i: s[i] == 2
        props[f"hungry{i}"] = lambda s, i=i: s[i] == 1
    names = ("think", "one fork", "eat")
    return Model(f"philosophers-{n}{'-ordered' if ordered else ''}", tuple(f"ph{i}" for i in range(n)),
                 [tuple([0] * n)], cmds, props, lambda s: {"phil": [names[x] for x in s]})


def philosopher_fairness(m: Model, n: int, kind: str = "weak") -> list:
    """Each philosopher, once hungry, keeps trying: fairness over its take2 and release (thinking may last)."""
    return [(kind, {f"take2_{i}", f"release_{i}"}) for i in range(n)]


def philosopher_results(ns=range(2, 9)) -> dict:
    """Reachable states and transitions for n = 2..8, naive and ordered: EF deadlock (CTL) and its shortest
    counterexample; and for the ordered version, starvation of philosopher 0 under weak fairness (a lasso) against
    its absence under strong fairness."""
    rows = []
    for n in ns:
        for ordered in (False, True):
            m = philosophers(n, ordered)
            K = build(m)
            row = {"n": n, "ordered": ordered, "states": K.n, "edges": K.edges(), "deadlocks": len(K.deadlocks),
                   "EF_deadlock": holds(K, ("EF", "deadlock")), "diameter": max(K.depth)}
            if K.deadlocks:
                path = K.path_to(min(K.deadlocks, key=lambda i: K.depth[i]))
                row["counterexample"] = [a for a, _ in path[1:]]
                row["counterexample_length"] = len(path) - 1
            rows.append(row)
    n = 3
    m = philosophers(n, ordered=True)
    K = build(m)
    weak = response(K, "hungry0", "eat0", philosopher_fairness(m, n, "weak"))
    strong = response(K, "hungry0", "eat0", philosopher_fairness(m, n, "strong"))
    return {"rows": rows, "starvation": {"n": n, "weak": _strip(weak), "strong": _strip(strong)}}


def philosophers_vs_part33(ns=(2, 3, 4)) -> list[dict]:
    """Deadlock verdicts against Part 33's philosophers (lock-based threads on its interleaving checker)."""
    from explainer.cs.conc import mc
    out = []
    for n in ns:
        for ordered in (False, True):
            r = mc.explore(mc.philosophers(n, ordered), "sc")
            K = build(philosophers(n, ordered))
            out.append({"n": n, "ordered": ordered, "part33_states": r.states, "part33_deadlock": bool(r.deadlocks),
                        "ours_states": K.n, "ours_deadlock": bool(K.deadlocks)})
    return out


# --------------------------------------------------------------------------------- two-phase commit, TLA+ style

RM = ("working", "prepared", "committed", "aborted")
TM = ("init", "committed", "aborted")
WORKING, PREPARED, COMMITTED, ABORTED = range(4)


def tcommit(n: int) -> Model:
    """Lamport's TCommit: the specification.  Each resource manager goes working → prepared, then commits if every
    one is prepared or committed, or aborts (from working or prepared) if nobody has committed."""
    def put(s, r, v):
        return s[:r] + (v,) + s[r + 1:]
    cmds = []
    for r in range(n):
        cmds.append((f"Prepare({r})", lambda s, r=r: s[r] == WORKING, lambda s, r=r: put(s, r, PREPARED)))
        cmds.append((f"Commit({r})", lambda s, r=r: s[r] == PREPARED and all(x in (PREPARED, COMMITTED) for x in s),
                     lambda s, r=r: put(s, r, COMMITTED)))
        cmds.append((f"Abort({r})", lambda s, r=r: s[r] in (WORKING, PREPARED) and COMMITTED not in s,
                     lambda s, r=r: put(s, r, ABORTED)))
    return Model(f"TCommit-{n}", tuple(f"rm{r}" for r in range(n)), [tuple([WORKING] * n)], cmds,
                 {"consistent": _consistent}, lambda s: {"rmState": [RM[x] for x in s]})


def _consistent(s) -> bool:
    """TCConsistent: no resource manager has committed while another has aborted."""
    rms = s if isinstance(s[0], int) else s[0]
    return not (COMMITTED in rms and ABORTED in rms)


def two_phase(n: int, bug: str | None = None) -> Model:
    """Lamport's TwoPhase: the protocol, with a transaction manager and messages.  The state is (rmState,
    tmState, tmPrepared, prepared messages, Commit sent, Abort sent); messages are never lost or removed, as in
    the TLA+ spec.  Actions: TMRcvPrepared(r), TMCommit (all prepared), TMAbort, RMPrepare(r), RMChooseToAbort(r),
    RMRcvCommitMsg(r), RMRcvAbortMsg(r).  ``bug="timeout-commit"``: the coordinator, tired of waiting, commits
    without hearing from everyone."""
    full = (1 << n) - 1

    def rmput(s, r, v):
        rm = s[0][:r] + (v,) + s[0][r + 1:]
        return (rm,) + s[1:]
    cmds = []
    for r in range(n):
        bit = 1 << r
        cmds.append((f"TMRcvPrepared({r})", lambda s, bit=bit: s[1] == 0 and s[3] & bit and not s[2] & bit,
                     lambda s, bit=bit: (s[0], s[1], s[2] | bit, s[3], s[4], s[5])))
    cmds.append(("TMCommit", lambda s: s[1] == 0 and s[2] == full, lambda s: (s[0], 1, s[2], s[3], True, s[5])))
    cmds.append(("TMAbort", lambda s: s[1] == 0, lambda s: (s[0], 2, s[2], s[3], s[4], True)))
    if bug == "timeout-commit":
        cmds.append(("TMTimeoutCommit", lambda s: s[1] == 0 and s[2] != full,
                     lambda s: (s[0], 1, s[2], s[3], True, s[5])))
    elif bug is not None:
        raise ValueError(bug)
    for r in range(n):
        bit = 1 << r
        cmds.append((f"RMPrepare({r})", lambda s, r=r: s[0][r] == WORKING,
                     lambda s, r=r, bit=bit: (lambda t: (t[0], t[1], t[2], t[3] | bit, t[4], t[5]))(
                         rmput(s, r, PREPARED))))
        cmds.append((f"RMChooseToAbort({r})", lambda s, r=r: s[0][r] == WORKING,
                     lambda s, r=r: rmput(s, r, ABORTED)))
        cmds.append((f"RMRcvCommitMsg({r})", lambda s, r=r: s[4] and s[0][r] != COMMITTED,
                     lambda s, r=r: rmput(s, r, COMMITTED)))
        cmds.append((f"RMRcvAbortMsg({r})", lambda s, r=r: s[5] and s[0][r] != ABORTED,
                     lambda s, r=r: rmput(s, r, ABORTED)))

    def showit(s):
        return {"rmState": [RM[x] for x in s[0]], "tmState": TM[s[1]],
                "tmPrepared": [r for r in range(n) if s[2] >> r & 1],
                "msgs": [f"Prepared({r})" for r in range(n) if s[3] >> r & 1] + (["Commit"] if s[4] else []) +
                (["Abort"] if s[5] else [])}
    init = ((WORKING,) * n, 0, 0, 0, False, False)
    return Model(f"TwoPhase-{n}{'-' + bug if bug else ''}", ("rmState", "tmState", "tmPrepared", "msgPrepared",
                 "msgCommit", "msgAbort"), [init], cmds, {"consistent": _consistent}, showit)


def refinement(n: int) -> dict:
    """TwoPhase implements TCommit: map each TwoPhase state to its rmState; the initial state maps to TCommit's,
    and every TwoPhase step maps to a TCommit step or to a stutter (the rmState unchanged).  This is the
    refinement mapping of the TLA+ proof, checked exhaustively."""
    K = build(two_phase(n))
    spec = tcommit(n)
    Ks = build(spec)
    ok_init = all(K.states[i][0] in {Ks.states[j] for j in Ks.init} for i in K.init)
    steps = stutters = bad = 0
    for i, out in enumerate(K.succ):
        a = K.states[i][0]
        for _, j in out:
            b = K.states[j][0]
            if a == b:
                stutters += 1
            elif b in {t for _, t in spec.step(a)}:
                steps += 1
            else:
                bad += 1
    image = {s[0] for s in K.states}
    return {"n": n, "init_ok": ok_init, "spec_steps": steps, "stutters": stutters, "bad": bad,
            "abstract_states_reached": len(image), "spec_states": Ks.n, "refines": ok_init and bad == 0}


def two_phase_results(ns=range(2, 6)) -> dict:
    """State counts of TCommit (3^n + 2^n - 1 in closed form) and TwoPhase for n = 2..5; the invariant
    TCConsistent on both; the refinement check; and the timeout-commit bug's shortest counterexample."""
    rows = []
    for n in ns:
        Kt = build(tcommit(n))
        K = build(two_phase(n))
        ref = refinement(n) if n <= 4 else None
        rows.append({"n": n, "tcommit_states": Kt.n, "tcommit_closed_form": 3 ** n + 2 ** n - 1,
                     "twophase_states": K.n, "twophase_edges": K.edges(),
                     "consistent": holds(K, ("AG", "consistent")) and holds(Kt, ("AG", "consistent")),
                     "diameter": max(K.depth), "refines": None if ref is None else ref["refines"]})
    Kb = build(two_phase(3, bug="timeout-commit"))
    cex = counterexample(Kb, "consistent")
    return {"rows": rows, "bug": {"n": 3, "states": Kb.n, "consistent": cex is None, "counterexample": Kb.trace(cex),
                                  "length": len(cex) - 1}}


# --------------------------------------------------------------------------------------------------- Raft-lite

FOLLOWER, CANDIDATE, LEADER = range(3)
ROLE = ("follower", "candidate", "leader")


def raft_lite(nodes: int = 3, max_term: int = 2, bug: str | None = None) -> Model:
    """An abstract Raft election (Ongaro and Ousterhout 2014, §5.2), logs left out.  State: per node (term, role,
    votedFor or -1), the set of vote grants sent (voter, candidate, term) — messages persist and may be counted
    late — and a history of (term, leader) elections.  Actions:

    * Timeout(i): a non-leader with term < max_term starts an election: term + 1, candidate, votes for itself;
    * Vote(j, i): j handles candidate i's request for i's current term t: a voter behind in term first moves to t
      (follower, no vote); it grants if it has not voted in t, or voted for i;
    * Win(i): a candidate counting grants for its current term from a majority becomes leader;
    * Learn(i, j): i sees j's higher term (any message carries it) and steps down to a follower of that term.

    ``bug="forget-vote"``: a voter grants without checking votedFor (as if it had forgotten its vote)."""
    N = nodes
    maj = N // 2 + 1

    def node(s, i):
        return s[0][i]

    def setn(s, i, v):
        ns = s[0][:i] + (v,) + s[0][i + 1:]
        return (ns,) + s[1:]
    cmds = []
    for i in range(N):
        cmds.append((f"Timeout({i})", lambda s, i=i: node(s, i)[1] != LEADER and node(s, i)[0] < max_term,
                     lambda s, i=i: (lambda t: (setn(s, i, (t, CANDIDATE, i))[0], s[1] | {(i, i, t)}, s[2]))(
                         node(s, i)[0] + 1)))
        for j in range(N):
            if j == i:
                continue

            def vguard(s, i=i, j=j):
                ti, ri, _ = node(s, i)
                tj, _, vj = node(s, j)
                if ri != CANDIDATE or tj > ti:
                    return False
                if tj < ti:
                    return True
                return bug == "forget-vote" or vj in (-1, i)

            def vupd(s, i=i, j=j):
                ti = node(s, i)[0]
                tj, rj, vj = node(s, j)
                if tj < ti:
                    rj = FOLLOWER
                return (setn(s, j, (ti, rj, i))[0], s[1] | {(j, i, ti)}, s[2])
            if bug not in (None, "forget-vote"):
                raise ValueError(bug)
            cmds.append((f"Vote({j},{i})", vguard, vupd))
            cmds.append((f"Learn({i},{j})", lambda s, i=i, j=j: node(s, j)[0] > node(s, i)[0],
                         lambda s, i=i, j=j: setn(s, i, (node(s, j)[0], FOLLOWER, -1))))

        def wguard(s, i=i):
            t, r, _ = node(s, i)
            return r == CANDIDATE and sum(1 for (v, c, tt) in s[1] if c == i and tt == t) >= maj
        cmds.append((f"Win({i})", wguard, lambda s, i=i: (setn(s, i, (node(s, i)[0], LEADER, node(s, i)[2]))[0],
                                                          s[1], s[2] | {(node(s, i)[0], i)})))

    def safe(s):
        terms = [t for t, _ in s[2]]
        return len(terms) == len(set(terms))

    def showit(s):
        return {"nodes": [{"term": t, "role": ROLE[r], "votedFor": None if v < 0 else v} for t, r, v in s[0]],
                "grants": sorted(list(g) for g in s[1]), "elected": sorted(list(e) for e in s[2])}
    init = (tuple((0, FOLLOWER, -1) for _ in range(N)), frozenset(), frozenset())
    return Model(f"raft-lite-{N}-{max_term}{'-' + bug if bug else ''}", ("nodes", "grants", "elected"), [init],
                 cmds, {"election_safety": safe,
                        "leader": lambda s: any(r == LEADER for _, r, _ in s[0])}, showit)


def raft_results(nodes: int = 3, max_term: int = 2) -> dict:
    """Election safety (at most one leader per term, over the whole history) checked exhaustively on the abstract
    model, and the forget-vote bug's shortest counterexample: two leaders in one term."""
    K = build(raft_lite(nodes, max_term))
    Kb = build(raft_lite(nodes, max_term, bug="forget-vote"))
    cex = counterexample(Kb, "election_safety")
    return {"nodes": nodes, "max_term": max_term, "states": K.n, "edges": K.edges(),
            "election_safety": holds(K, ("AG", "election_safety")), "EF_leader": holds(K, ("EF", "leader")),
            "diameter": max(K.depth),
            "bug": {"states": Kb.n, "election_safety": cex is None, "counterexample": Kb.trace(cex),
                    "length": len(cex) - 1}}


# ------------------------------------------------------------------------------------------- random structures

def random_model(n_states: int, seed: int, props=("p", "q"), max_out: int = 2) -> Model:
    """A small random model over states 0..n-1 (for checking the fixpoints against brute force)."""
    import random
    r = random.Random(seed)
    edges = {s: sorted({r.randrange(n_states) for _ in range(r.randint(0, max_out))}) for s in range(n_states)}
    lab = {p: {s for s in range(n_states) if r.random() < 0.5} for p in props}
    cmds = [(f"e{k}", lambda s, k=k: k < len(edges[s[0]]), lambda s, k=k: (edges[s[0]][k],)) for k in range(max_out)]
    return Model(f"random-{seed}", ("s",), [(s,) for s in range(n_states)], cmds,
                 {p: (lambda s, p=p: s[0] in lab[p]) for p in props})


def all_results() -> dict:
    return {"peterson": peterson_results(), "philosophers": philosopher_results(), "two_phase": two_phase_results(),
            "raft": raft_results()}

