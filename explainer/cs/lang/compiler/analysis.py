"""Analyses for Part 13's chapters 7 and 12: monotone dataflow frameworks with their iteration traces, and the
chordality of SSA interference graphs.

* :func:`solve` is Kildall's (1973) worklist algorithm for a monotone framework on a lattice of sets: a direction,
  a meet (union for "may" problems, intersection for "must" problems), and per-block transfer functions
  ``out = gen ∪ (in − kill)``.  It records every update, so the scenes can show the facts flowing round the CFG
  until they reach the least fixed point (the Knaster–Tarski theorem says it exists; Kleene's iteration from ⊥
  says this is how to get there).
* :func:`liveness`, :func:`reaching`, :func:`available` instantiate it.
* :func:`interference_ssa` builds the interference graph of a strict SSA function (two values interfere when one is
  live where the other is defined); :func:`is_chordal` checks it with maximum cardinality search and a perfect
  elimination ordering (Tarjan and Yannakakis 1984); :func:`color_peo` colours along that ordering, which is optimal
  on a chordal graph (Hack, Grund and Goos 2006: every strict-SSA interference graph is chordal).
"""
from __future__ import annotations

from explainer.cs.lang.compiler.ir import Func, is_var


def solve(f: Func, gen: dict, kill: dict, direction: str = "forward", meet: str = "union", universe=None,
          entry_value=frozenset()):
    labels = [b.label for b in f.blocks]
    succ = {b.label: b.succs() for b in f.blocks}
    pred = f.preds()
    top = frozenset(universe) if meet == "intersect" else frozenset()
    IN = {l: top for l in labels}
    OUT = {l: top for l in labels}
    if direction == "forward":
        IN[labels[0]] = frozenset(entry_value)
    trace = []
    work = list(labels) if direction == "forward" else list(reversed(labels))
    rounds = 0
    while work:
        rounds += 1
        l = work.pop(0)
        if direction == "forward":
            ps = pred[l]
            if l == labels[0]:
                inn = frozenset(entry_value)
            elif not ps:
                inn = frozenset()
            elif meet == "union":
                inn = frozenset().union(*(OUT[p] for p in ps))
            else:
                inn = frozenset.intersection(*(OUT[p] for p in ps))
            out = frozenset(gen[l]) | (inn - kill[l])
            changed = out != OUT[l] or inn != IN[l]
            IN[l], OUT[l] = inn, out
            if changed:
                trace.append((l, inn, out))
                for s in succ[l]:
                    if s not in work:
                        work.append(s)
        else:
            ss = succ[l]
            if not ss:
                out = frozenset()
            elif meet == "union":
                out = frozenset().union(*(IN[s] for s in ss))
            else:
                out = frozenset.intersection(*(IN[s] for s in ss))
            inn = frozenset(gen[l]) | (out - kill[l])
            changed = out != OUT[l] or inn != IN[l]
            IN[l], OUT[l] = inn, out
            if changed:
                trace.append((l, inn, out))
                for p in pred[l]:
                    if p not in work:
                        work.append(p)
    return IN, OUT, trace, rounds


def liveness(f: Func):
    gen, kill = {}, {}
    for b in f.blocks:
        use, d = set(), set()
        for i in b.ins:
            for a in i.uses():
                if a not in d:
                    use.add(a)
            if i.dst:
                d.add(i.dst)
        gen[b.label], kill[b.label] = use, d
    return solve(f, gen, kill, "backward", "union")


def reaching(f: Func):
    """Definitions are (block, index, variable)."""
    defs_of: dict = {}
    sites = []
    for b in f.blocks:
        for k, i in enumerate(b.ins):
            if i.dst:
                s = (b.label, k, i.dst)
                sites.append(s)
                defs_of.setdefault(i.dst, set()).add(s)
    gen, kill = {}, {}
    for b in f.blocks:
        g, kl = {}, set()
        for k, i in enumerate(b.ins):
            if i.dst:
                g[i.dst] = (b.label, k, i.dst)
                kl |= defs_of[i.dst]
        gen[b.label] = set(g.values())
        kill[b.label] = kl - set(g.values())
    return solve(f, gen, kill, "forward", "union")


def _expr(i):
    if i.op == "bin":
        return (i.k, tuple(i.args))
    return None


def available(f: Func):
    exprs = set()
    for b in f.blocks:
        for i in b.ins:
            e = _expr(i)
            if e:
                exprs.add(e)
    gen, kill = {}, {}
    for b in f.blocks:
        g, kl = set(), set()
        for i in b.ins:
            e = _expr(i)
            if e:
                g.add(e)
            if i.dst:
                dead = {x for x in exprs if i.dst in x[1]}
                g -= dead
                kl |= dead
        gen[b.label], kill[b.label] = g, kl
    return solve(f, gen, kill, "forward", "intersect", universe=exprs)


# ---------------------------------------------------------------------------
# interference graphs and chordality
# ---------------------------------------------------------------------------
def interference_ssa(f: Func) -> dict:
    """Interference among virtual registers by instruction-level liveness (φ uses live at the end of the matching
    predecessor, φ definitions at the top of their block)."""
    lab = f.labels()
    succ = {b.label: b.succs() for b in f.blocks}
    phi_uses = {b.label: set() for b in f.blocks}     # values used by φs along the edge out of this block
    for b in f.blocks:
        for i in b.ins:
            if i.op == "phi":
                for v, p in zip(i.args, i.k):
                    if is_var(v):
                        phi_uses[p].add(v)
    lin = {b.label: set() for b in f.blocks}
    lout = {b.label: set() for b in f.blocks}
    changed = True
    while changed:
        changed = False
        for b in reversed(f.blocks):
            out = set(phi_uses[b.label])
            for s in succ[b.label]:
                out |= {v for v in lin[s]}
            live = set(out)
            for i in reversed(b.ins):
                if i.dst:
                    live.discard(i.dst)
                if i.op != "phi":
                    live |= set(i.uses())
            phidefs = {i.dst for i in b.ins if i.op == "phi"}
            inn = live | phidefs if False else live
            if inn != lin[b.label] or out != lout[b.label]:
                lin[b.label], lout[b.label] = inn, out
                changed = True
    adj: dict = {}
    for p in f.params:
        adj.setdefault(p, set())
    for b in f.blocks:
        live = set(lout[b.label])
        for i in reversed(b.ins):
            if i.op == "phi":
                continue
            if i.dst:
                adj.setdefault(i.dst, set())
                for l in live:
                    if l != i.dst:
                        adj[i.dst].add(l)
                        adj.setdefault(l, set()).add(i.dst)
                live.discard(i.dst)
            for a in i.uses():
                adj.setdefault(a, set())
                live.add(a)
        phidefs = [i.dst for i in b.ins if i.op == "phi"]
        for d in phidefs:
            adj.setdefault(d, set())
            for l in live | set(phidefs):
                if l != d:
                    adj[d].add(l)
                    adj.setdefault(l, set()).add(d)
    if f.params:
        live = set(lin[f.blocks[0].label]) | set(f.params)
        for p in f.params:
            for l in live:
                if l != p:
                    adj[p].add(l)
                    adj.setdefault(l, set()).add(p)
    return adj


def mcs(adj: dict) -> list:
    """Maximum cardinality search: an ordering whose reverse is a perfect elimination ordering iff chordal."""
    weight = {v: 0 for v in adj}
    order, done = [], set()
    while len(order) < len(adj):
        v = max((u for u in adj if u not in done), key=lambda u: (weight[u], str(u)))
        order.append(v)
        done.add(v)
        for u in adj[v]:
            if u not in done:
                weight[u] += 1
    return order


def is_chordal(adj: dict):
    order = mcs(adj)
    pos = {v: i for i, v in enumerate(order)}
    for v in order:
        earlier = [u for u in adj[v] if pos[u] < pos[v]]
        if not earlier:
            continue
        parent = max(earlier, key=lambda u: pos[u])
        need = set(earlier) - {parent}
        if not need <= adj[parent]:
            return False, order, (v, parent, sorted(need - adj[parent], key=str)[:3])
    return True, order, None


def color_peo(adj: dict, order=None) -> dict:
    order = order or mcs(adj)
    col = {}
    for v in order:
        used = {col[u] for u in adj[v] if u in col}
        c = 0
        while c in used:
            c += 1
        col[v] = c
    return col


def max_clique_chordal(adj: dict) -> int:
    order = mcs(adj)
    pos = {v: i for i, v in enumerate(order)}
    return max((1 + sum(1 for u in adj[v] if pos[u] < pos[v]) for v in order), default=0)


def find_hole(adj: dict, limit: int = 8):
    """A chordless cycle of length >= 4 (a witness that the graph is not chordal), by search on small graphs."""
    nodes = sorted(adj, key=str)
    import itertools
    for n in range(4, limit + 1):
        for start in nodes:
            stack = [(start, [start])]
            while stack:
                v, path = stack.pop()
                if len(path) == n:
                    if start in adj[v]:
                        ok = all(path[j] not in adj[path[k]] for j in range(n) for k in range(j + 2, n)
                                 if not (j == 0 and k == n - 1))
                        if ok:
                            return path
                    continue
                for u in adj[v]:
                    if u not in path and str(u) > str(start):
                        stack.append((u, path + [u]))
    return None


# ---------------------------------------------------------------------------
# list scheduling (chapter 13) on final assembly, inside basic blocks
# ---------------------------------------------------------------------------
def schedule_asm(asm: str) -> tuple[str, int]:
    """Reorder instructions inside each basic block of assembly text to separate loads from their uses (Pebble's
    pipeline stalls one cycle on a load-use pair).  Dependences: register RAW, WAR, WAW; memory accesses keep their
    order with stores and device accesses; branches, calls and labels end blocks.  Returns the text and the number
    of load-use pairs separated."""
    import re
    lines = asm.splitlines()
    out, block = [], []
    fixed = 0

    def regs(ins):
        op, *rest = ins.split(None, 1)
        args = [a.strip() for a in rest[0].split(",")] if rest else []
        m = re.compile(r"(-?\w+)\((\w+)\)")
        if op in ("lw", "lbu", "lb"):
            mm = m.fullmatch(args[1])
            return op, {args[0]}, {mm.group(2)}
        if op in ("sw", "sb"):
            mm = m.fullmatch(args[1])
            return op, set(), {args[0], mm.group(2)}
        if op in ("mv",):
            return op, {args[0]}, {args[1]}
        if op in ("li", "la"):
            return op, {args[0]}, set()
        if len(args) == 3:
            srcs = {a for a in args[1:] if not re.fullmatch(r"-?\d+", a)}
            return op, {args[0]}, srcs
        return op, set(), set()

    def flush():
        nonlocal fixed, block
        n = len(block)
        if n < 3:
            out.extend(block)
            block = []
            return
        info = [regs(x.strip()) for x in block]
        deps = {k: set() for k in range(n)}
        for j in range(n):
            oj, dj, uj = info[j]
            memj = oj in ("lw", "lbu", "lb", "sw", "sb")
            for k in range(j):
                ok, dk, uk = info[k]
                memk = ok in ("lw", "lbu", "lb", "sw", "sb")
                if (dk & uj) or (dk & dj) or (uk & dj) or (memj and memk and (oj in ("sw", "sb") or ok in ("sw", "sb"))):
                    deps[j].add(k)
                if "sp" in dj or "sp" in dk:
                    deps[j].add(k)
        before = sum(1 for k in range(n - 1) if info[k][0] in ("lw", "lbu", "lb") and info[k][1] & info[k + 1][2])
        # greedy: at each step take a ready instruction that does not use the previous load's result
        done, order = set(), []
        while len(order) < n:
            ready = [j for j in range(n) if j not in done and deps[j] <= done]
            last = info[order[-1]] if order else None
            good = [j for j in ready if not (last and last[0] in ("lw", "lbu", "lb") and last[1] & info[j][2])]
            # prefer loads early (they feed later instructions), then original order
            pick = min(good or ready, key=lambda j: (0 if info[j][0] in ("lw", "lbu", "lb") else 1, j))
            order.append(pick)
            done.add(pick)
        after = sum(1 for a, b in zip(order, order[1:]) if info[a][0] in ("lw", "lbu", "lb") and info[a][1] &
                    info[b][2])
        fixed += before - after
        out.extend(block[j] for j in order)
        block = []
    for ln in lines:
        s = ln.strip()
        if not s or s.endswith(":") or s.startswith(".") or ":" in s.split()[0]:
            flush()
            out.append(ln)
            continue
        op = s.split()[0]
        if op in ("j", "jal", "call", "ret", "halt", "beq", "bne", "blt", "bge", "bltu", "bgeu", "beqz", "bnez",
                  "jr", "jalr") or "sp, sp" in s:
            flush()
            out.append(ln)
            continue
        block.append(ln)
    flush()
    return "\n".join(out), fixed
