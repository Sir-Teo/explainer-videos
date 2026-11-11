"""Checking a history for isolation anomalies, after Elle (Kingsbury and Alvaro 2020), for Part 39.

Transactions append unique values to lists and read whole lists.  Because every value is unique and lists only
grow, each read reveals exactly which writes it saw and in what order, so the dependency graph between
transactions (write-write, write-read, read-write) can be inferred from the history alone, and any cycle is a
proof that no serial order explains what the clients observed."""

from __future__ import annotations

import random
from collections import defaultdict


def run_store(mode: str = "serializable", txns: int = 2000, keys: int = 5, max_lag: int = 8, seed: int = 0):
    """Execute random list-append transactions.  ``serializable``: one copy, one transaction at a time.
    ``stale replica``: appends go to the primary at once, but each transaction reads a snapshot from a replica
    up to ``max_lag`` transactions behind (plus its own appends), as with asynchronous followers."""
    rng = random.Random(seed)
    state = {k: [] for k in range(keys)}
    snaps = [{k: [] for k in range(keys)}]
    hist = []
    nxt = 1
    for t in range(txns):
        if mode == "serializable":
            view = {k: list(v) for k, v in state.items()}
        else:
            view = {k: list(v) for k, v in snaps[max(0, len(snaps) - 1 - rng.randint(0, max_lag))].items()}
        ops = []
        for _ in range(rng.randint(1, 3)):
            k = rng.randrange(keys)
            if rng.random() < 0.5:
                ops.append(("r", k, tuple(view[k])))
            else:
                v = nxt
                nxt += 1
                view[k].append(v)
                state[k].append(v)
                ops.append(("a", k, v))
        hist.append(ops)
        snaps.append({k: list(v) for k, v in state.items()})
    return {"history": hist, "final": {k: tuple(v) for k, v in state.items()}}


def infer_graph(history, final):
    """Edges T -> U labelled ww (U appended right after T's value), wr (T's value is the last U saw), rw (T read a
    prefix that U's value extends)."""
    writer = {}
    for t, ops in enumerate(history):
        for op in ops:
            if op[0] == "a":
                writer[op[2]] = t
    edges = defaultdict(set)
    for k, lst in final.items():
        for a, b in zip(lst, lst[1:]):
            if writer[a] != writer[b]:
                edges[(writer[a], writer[b])].add("ww")
    for t, ops in enumerate(history):
        own = {op[2] for op in ops if op[0] == "a"}
        for op in ops:
            if op[0] != "r":
                continue
            _, k, seen = op
            ext = [v for v in seen if v not in own]
            if ext:
                w = writer[ext[-1]]
                if w != t:
                    edges[(w, t)].add("wr")
            lst = final[k]
            p = len(ext)
            if p < len(lst):
                u = writer[lst[p]]
                if u != t:
                    edges[(t, u)].add("rw")
    return edges


def _sccs(nodes, adj):
    index, low, on, st, out = {}, {}, set(), [], []
    counter = [0]

    def strong(v):
        stack = [(v, iter(adj[v]))]
        index[v] = low[v] = counter[0]
        counter[0] += 1
        st.append(v)
        on.add(v)
        while stack:
            u, it = stack[-1]
            for w in it:
                if w not in index:
                    index[w] = low[w] = counter[0]
                    counter[0] += 1
                    st.append(w)
                    on.add(w)
                    stack.append((w, iter(adj[w])))
                    break
                if w in on:
                    low[u] = min(low[u], index[w])
            else:
                stack.pop()
                if stack:
                    low[stack[-1][0]] = min(low[stack[-1][0]], low[u])
                if low[u] == index[u]:
                    comp = []
                    while True:
                        w = st.pop()
                        on.discard(w)
                        comp.append(w)
                        if w == u:
                            break
                    out.append(comp)
    for v in nodes:
        if v not in index:
            strong(v)
    return out


def _short_cycle(comp, adj):
    cs = set(comp)
    best = None
    for s in sorted(comp)[:50]:
        prev = {s: None}
        q = [s]
        found = None
        while q and found is None:
            nq = []
            for u in q:
                for w in adj[u]:
                    if w not in cs:
                        continue
                    if w == s:
                        found = u
                        break
                    if w not in prev:
                        prev[w] = u
                        nq.append(w)
                if found is not None:
                    break
            q = nq
        if found is not None:
            path = [found]
            while path[-1] != s:
                path.append(prev[path[-1]])
            path.reverse()
            if best is None or len(path) < len(best):
                best = path
    return best


def check(history, final):
    edges = infer_graph(history, final)
    adj = defaultdict(list)
    for (a, b) in edges:
        adj[a].append(b)
    nodes = list(range(len(history)))
    comps = [c for c in _sccs(nodes, adj) if len(c) > 1]
    cyc = _short_cycle(max(comps, key=len), adj) if comps else None
    example = None
    if cyc:
        example = [{"txn": a, "to": b, "kinds": sorted(edges[(a, b)]), "ops": history[a]}
                   for a, b in zip(cyc, cyc[1:] + cyc[:1])]
    counts = defaultdict(int)
    for kinds in edges.values():
        for k in kinds:
            counts[k] += 1
    return {"txns": len(history), "edges": dict(counts), "cyclic_components": len(comps),
            "txns_in_cycles": sum(len(c) for c in comps), "example": example}


def campaign(txns: int = 2000, seed: int = 0):
    out = {}
    for mode in ("serializable", "stale replica"):
        r = run_store(mode, txns=txns, seed=seed)
        out[mode] = check(r["history"], r["final"])
    return out
