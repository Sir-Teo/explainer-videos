"""Dominators, dominance frontiers, SSA construction and destruction (Part 13, chapters 5 and 6).

* :func:`dominators` is the iterative algorithm of Cooper, Harvey and Kennedy ("A simple, fast dominance algorithm",
  2001): immediate dominators by intersecting along the current tree, in reverse postorder, until nothing changes.
  It returns the idom map and the number of passes it took.
* :func:`frontiers` computes dominance frontiers the same paper's way: walk up from each join point's predecessors
  to its immediate dominator.
* :func:`to_ssa` is Cytron, Ferrante, Rosen, Wegman and Zadeck (1991): φ-functions at the iterated dominance
  frontier of every variable's definitions (pruned by liveness, so no dead φs), then renaming along the dominator
  tree.  Variables are the virtual registers assigned more than once or across blocks; temporaries already have
  one definition.
* :func:`from_ssa` replaces each φ by copies: ``x' = v`` at the end of each predecessor (critical edges split first)
  and ``x = x'`` where the φ was, which is always correct (no lost copies, no swap problem); the register
  allocator's move biasing removes most of the copies again.
"""
from __future__ import annotations

from explainer.cs.lang.compiler.ir import Block, Func, I, is_var, rpo


def dominators(f: Func):
    order = rpo(f)
    index = {l: i for i, l in enumerate(order)}
    preds = f.preds()
    entry = order[0]
    idom = {entry: entry}
    passes = 0
    changed = True

    def intersect(a, b):
        while a != b:
            while index[a] > index[b]:
                a = idom[a]
            while index[b] > index[a]:
                b = idom[b]
        return a
    while changed:
        passes += 1
        changed = False
        for b in order[1:]:
            ps = [p for p in preds[b] if p in idom]
            if not ps:
                continue
            new = ps[0]
            for p in ps[1:]:
                new = intersect(p, new)
            if idom.get(b) != new:
                idom[b] = new
                changed = True
    return idom, passes


def dom_tree(idom: dict) -> dict:
    kids = {b: [] for b in idom}
    for b, d in idom.items():
        if b != d:
            kids[d].append(b)
    return kids


def dominates(idom: dict, a: str, b: str) -> bool:
    while True:
        if a == b:
            return True
        if idom[b] == b:
            return False
        b = idom[b]


def frontiers(f: Func, idom: dict) -> dict:
    preds = f.preds()
    df = {b: set() for b in idom}
    for b in idom:
        ps = [p for p in preds[b] if p in idom]
        if len(ps) >= 2:
            for p in ps:
                r = p
                while r != idom[b]:
                    df[r].add(b)
                    r = idom[r]
    return df


# ---------------------------------------------------------------------------
# liveness on the non-SSA form, for pruning φs
# ---------------------------------------------------------------------------
def block_use_def(b: Block):
    use, defs = set(), set()
    for i in b.ins:
        for a in i.uses():
            if a not in defs:
                use.add(a)
        if i.dst:
            defs.add(i.dst)
    return use, defs


def live_in(f: Func) -> dict:
    ud = {b.label: block_use_def(b) for b in f.blocks}
    succ = {b.label: b.succs() for b in f.blocks}
    lin = {b.label: set() for b in f.blocks}
    lout = {b.label: set() for b in f.blocks}
    changed = True
    while changed:
        changed = False
        for b in reversed(f.blocks):
            l = b.label
            out = set().union(*(lin[s] for s in succ[l])) if succ[l] else set()
            inn = ud[l][0] | (out - ud[l][1])
            if inn != lin[l] or out != lout[l]:
                lin[l], lout[l] = inn, out
                changed = True
    return lin


def to_ssa(f: Func, stats: dict | None = None) -> Func:
    idom, _ = dominators(f)
    df = frontiers(f, idom)
    lab = f.labels()
    preds = f.preds()
    defsites: dict = {}
    for b in f.blocks:
        for i in b.ins:
            if i.dst:
                defsites.setdefault(i.dst, set()).add(b.label)
    for p in f.params:
        defsites.setdefault(p, set()).add(f.blocks[0].label)
    lin = live_in(f)
    # variables: defined in more than one place (or defined once and used in another block: harmless either way)
    ndefs: dict = {p: 1 for p in f.params}         # a parameter is defined on entry
    for b in f.blocks:
        for i in b.ins:
            if i.dst:
                ndefs[i.dst] = ndefs.get(i.dst, 0) + 1
    multi = {v for v, s in defsites.items() if len(s) > 1 or ndefs.get(v, 0) > 1}
    placed = 0
    for v in sorted(multi, key=str):
        work = sorted(defsites[v], key=str)
        has = set()
        while work:
            x = work.pop()
            for y in df[x]:
                if y not in has:
                    has.add(y)
                    if v in lin[y]:
                        lab[y].ins.insert(0, I("phi", v, [v] * len(preds[y]), list(preds[y])))
                        placed += 1
                    if y not in defsites[v]:
                        work.append(y)
    # renaming
    kids = dom_tree(idom)
    counter: dict = {}
    stacks: dict = {}

    def fresh(v):
        counter[v] = counter.get(v, 0) + 1
        n = f"{v}.{counter[v]}"
        stacks.setdefault(v, []).append(n)
        return n

    def top(v):
        st = stacks.get(v)
        return st[-1] if st else v

    new_params = []
    for p in f.params:
        new_params.append(fresh(p) if p in multi else p)
    import sys
    sys.setrecursionlimit(max(sys.getrecursionlimit(), 10000))

    def rename(l):
        pushed = []
        b = lab[l]
        for i in b.ins:
            if i.op != "phi":
                i.args = [top(a) if is_var(a) and a in multi else a for a in i.args]
            if i.dst and i.dst in multi:
                pushed.append(i.dst)
                i.dst = fresh(i.dst)
        for s in b.succs():
            for i in lab[s].ins:
                if i.op != "phi":
                    break
                for k, p in enumerate(i.k):
                    if p == l:
                        base = i.args[k]
                        i.args[k] = top(base) if is_var(base) and base in multi else base
        for c in kids.get(l, []):
            rename(c)
        for v in pushed:
            stacks[v].pop()

    # φ arguments still name the original variable until renamed: keep the original names for lookup
    for b in f.blocks:
        for i in b.ins:
            if i.op == "phi":
                i.orig = i.dst
    rename(f.blocks[0].label)
    # a φ argument along an edge where the variable was never defined: undefined, use 0
    for b in f.blocks:
        for i in b.ins:
            if i.op == "phi":
                i.args = [0 if (is_var(a) and a in multi) else a for a in i.args]
    f.params = new_params
    if stats is not None:
        stats["phis"] = placed
        stats["variables"] = len(multi)
    return f


def split_critical_edges(f: Func) -> int:
    preds = f.preds()
    n = 0
    new = []
    for b in list(f.blocks):
        succ = b.succs()
        if len(succ) < 2:
            continue
        t = b.term
        for s in succ:
            if len(preds[s]) < 2:
                continue
            n += 1
            mid = Block(f"{b.label}_{s}", [I("br", k=s)])
            new.append(mid)
            t.k = tuple(mid.label if x == s else x for x in t.k)
            for i in f.block(s).ins:
                if i.op == "phi":
                    i.k = [mid.label if p == b.label else p for p in i.k]
    f.blocks += new
    return n


def from_ssa(f: Func) -> Func:
    split_critical_edges(f)
    lab = f.labels()
    n = 0
    for b in f.blocks:
        phis = [i for i in b.ins if i.op == "phi"]
        if not phis:
            continue
        rest = [i for i in b.ins if i.op != "phi"]
        head = []
        for i in phis:
            n += 1
            t = f"{i.dst}'"
            for v, p in zip(i.args, i.k):
                pb = lab[p]
                pb.ins.insert(len(pb.ins) - 1, I("copy", t, [v]))
            head.append(I("copy", i.dst, [t]))
        b.ins = head + rest
    return f
