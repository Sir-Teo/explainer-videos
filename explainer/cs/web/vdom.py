"""UI frameworks (Part 42): a virtual-DOM reconciler with the heuristics React uses (a different type replaces the
subtree; children are matched by position, or by key), the true tree edit distance (Zhang and Shasha, 1989) for
comparison, and fine-grained reactivity as a dependency graph of signals."""

from __future__ import annotations

import time
from dataclasses import dataclass, field


@dataclass
class V:
    tag: str
    key: object = None
    text: str = ""
    kids: list = field(default_factory=list)


def size(v):
    return 1 + sum(size(k) for k in v.kids)


def reconcile(old, new, ops, keyed=True):
    """Append DOM operations to ops; returns nothing.  Operations: create (counts nodes), remove, move, text."""
    if old is None:
        ops.append(("create", new.tag, size(new)))
        return
    if old.tag != new.tag:
        ops.append(("remove", old.tag, size(old)))
        ops.append(("create", new.tag, size(new)))
        return
    if old.text != new.text:
        ops.append(("text", new.tag, 1))
    if keyed and all(k.key is not None for k in new.kids) and all(k.key is not None for k in old.kids):
        old_by_key = {k.key: (i, k) for i, k in enumerate(old.kids)}
        last = -1
        for k in new.kids:
            if k.key in old_by_key:
                i, ok = old_by_key.pop(k.key)
                if i < last:
                    ops.append(("move", k.tag, 1))
                else:
                    last = i
                reconcile(ok, k, ops, keyed)
            else:
                ops.append(("create", k.tag, size(k)))
        for i, ok in old_by_key.values():
            ops.append(("remove", ok.tag, size(ok)))
    else:
        for i in range(max(len(old.kids), len(new.kids))):
            if i >= len(new.kids):
                ops.append(("remove", old.kids[i].tag, size(old.kids[i])))
            elif i >= len(old.kids):
                ops.append(("create", new.kids[i].tag, size(new.kids[i])))
            else:
                reconcile(old.kids[i], new.kids[i], ops, keyed)


def row(i, name):
    return V("li", key=i, kids=[V("span", text=name), V("input", text="")])


def cost(ops):
    """Nodes touched: created and removed count every node in the subtree; moves and text edits count one."""
    return sum(n for _, _, n in ops)


def list_experiment(n=100):
    names = [f"item {i}" for i in range(n)]
    base = V("ul", kids=[row(i, names[i]) for i in range(n)])
    cases = {
        "prepend": V("ul", kids=[row(-1, "new")] + [row(i, names[i]) for i in range(n)]),
        "append": V("ul", kids=[row(i, names[i]) for i in range(n)] + [row(n, "new")]),
        "remove first": V("ul", kids=[row(i, names[i]) for i in range(1, n)]),
        "reverse": V("ul", kids=[row(i, names[i]) for i in reversed(range(n))]),
        "swap two": V("ul", kids=[row(i, names[i]) for i in [n - 1] + list(range(1, n - 1)) + [0]]),
    }
    out = {}
    for name, new in cases.items():
        k, u = [], []
        reconcile(base, new, k, keyed=True)
        reconcile(base, new, u, keyed=False)
        # unkeyed: positional matching edits every row's text; and an input's state now belongs to the wrong row
        wrong = 0
        for i in range(min(len(base.kids), len(new.kids))):
            if base.kids[i].key != new.kids[i].key:
                wrong += 1
        lis = lis_moves([c.key for c in base.kids], [c.key for c in new.kids])
        out[name] = {"lis_moves": lis, "keyed": cost(k), "unkeyed": cost(u), "keyed_ops": len(k), "unkeyed_ops": len(u),
                     "state_misplaced": wrong}
    return out


def lis_moves(old_keys, new_keys):
    """The fewest moves for a keyed list: keep a longest increasing subsequence of old positions in place and move
    the rest (Inferno and Vue 3 do this; React's single pass keeps only a greedy increasing run)."""
    import bisect
    pos = {k: i for i, k in enumerate(old_keys)}
    seq = [pos[k] for k in new_keys if k in pos]
    tails = []
    for x in seq:
        j = bisect.bisect_left(tails, x)
        tails[j:j + 1] = [x]
    return len(seq) - len(tails)


# ---------------------------------------------------------------- tree edit distance

def _postorder(v):
    nodes, lmd = [], []

    def go(x):
        first = None
        for c in x.kids:
            f = go(c)
            first = f if first is None else first
        nodes.append(x)
        me = len(nodes) - 1
        lmd.append(first if first is not None else me)
        return lmd[me]
    go(v)
    return nodes, lmd


def tree_edit_distance(a, b):
    """Zhang–Shasha: unit costs for insert, delete and relabel (label = tag + text).  O(n^2 m^2) worst case here; the
    best known general algorithms are about cubic."""
    na, la = _postorder(a)
    nb, lb = _postorder(b)

    def keyroots(lmd):
        seen, kr = set(), []
        for i in range(len(lmd) - 1, -1, -1):
            if lmd[i] not in seen:
                seen.add(lmd[i])
                kr.append(i)
        return sorted(kr)
    td = [[0] * len(nb) for _ in na]
    for i in keyroots(la):
        for j in keyroots(lb):
            m, n = i - la[i] + 2, j - lb[j] + 2
            fd = [[0] * n for _ in range(m)]
            ioff, joff = la[i] - 1, lb[j] - 1
            for x in range(1, m):
                fd[x][0] = fd[x - 1][0] + 1
            for y in range(1, n):
                fd[0][y] = fd[0][y - 1] + 1
            for x in range(1, m):
                for y in range(1, n):
                    xi, yj = x + ioff, y + joff
                    if la[xi] == la[i] and lb[yj] == lb[j]:
                        rel = 0 if (na[xi].tag, na[xi].text) == (nb[yj].tag, nb[yj].text) else 1
                        fd[x][y] = min(fd[x - 1][y] + 1, fd[x][y - 1] + 1, fd[x - 1][y - 1] + rel)
                        td[xi][yj] = fd[x][y]
                    else:
                        p, q = la[xi] - 1 - ioff, lb[yj] - 1 - joff
                        fd[x][y] = min(fd[x - 1][y] + 1, fd[x][y - 1] + 1, fd[p][q] + td[xi][yj])
    return td[-1][-1]


def diff_timing(sizes=(10, 20, 40, 80, 160)):
    """Time the heuristic reconciler against exact tree edit distance on lists of n rows with one row changed."""
    out = []
    for n in sizes:
        a = V("ul", kids=[row(i, f"item {i}") for i in range(n)])
        b = V("ul", kids=[row(i, f"item {i}" if i != n // 2 else "changed") for i in range(n)])
        t0 = time.perf_counter()
        ops = []
        reconcile(a, b, ops)
        t1 = time.perf_counter()
        d = tree_edit_distance(a, b)
        t2 = time.perf_counter()
        out.append({"n": n, "nodes": size(a), "heuristic_ms": (t1 - t0) * 1e3, "exact_ms": (t2 - t1) * 1e3,
                    "heuristic_ops": cost(ops), "distance": d})
    return out


# ---------------------------------------------------------------- signals

class Graph:
    """Signals, computed values and effects: reading registers a dependency; writing marks dependents stale and
    re-runs only effects downstream of the change (push to invalidate, pull to recompute)."""

    def __init__(self):
        self.deps = {}          # node -> set of nodes it reads
        self.fn = {}
        self.val = {}
        self.runs = {}
        self.reading = []

    def signal(self, name, v):
        self.val[name] = v
        self.deps[name] = set()

    def computed(self, name, fn):
        self.fn[name] = fn
        self.deps[name] = set()
        self._eval(name)

    def get(self, name):
        if self.reading:
            self.deps[self.reading[-1]].add(name)
        return self.val[name]

    def _eval(self, name):
        self.deps[name] = set()
        self.reading.append(name)
        self.val[name] = self.fn[name](self.get)
        self.reading.pop()
        self.runs[name] = self.runs.get(name, 0) + 1

    def set(self, name, v):
        self.val[name] = v
        dirty = self._downstream(name)
        order = [n for n in self._topo() if n in dirty]
        for n in order:
            self._eval(n)
        return order

    def _downstream(self, name):
        out, stack = set(), [name]
        while stack:
            x = stack.pop()
            for n, ds in self.deps.items():
                if x in ds and n not in out:
                    out.add(n)
                    stack.append(n)
        return out

    def _topo(self):
        seen, order = set(), []

        def go(n):
            if n in seen:
                return
            seen.add(n)
            for d in self.deps[n]:
                go(d)
            order.append(n)
        for n in self.deps:
            go(n)
        return order


def signals_demo():
    g = Graph()
    g.signal("first", "Ada")
    g.signal("last", "Lovelace")
    g.signal("count", 0)
    g.computed("full", lambda get: get("first") + " " + get("last"))
    g.computed("greeting", lambda get: "Hello, " + get("full"))
    g.computed("badge", lambda get: f"{get('count')} new")
    g.computed("header", lambda get: get("greeting") + " | " + get("badge"))
    reran = {"count": g.set("count", 3), "last": g.set("last", "King")}
    return {"reran": reran, "values": {k: g.val[k] for k in ("full", "greeting", "badge", "header")},
            "deps": {k: sorted(v) for k, v in g.deps.items() if v}}
