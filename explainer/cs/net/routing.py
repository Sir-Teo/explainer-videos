"""Routing (Part 36): distance vector as distributed Bellman-Ford, with count-to-infinity, split horizon and
poisoned reverse; link state as flooding plus Dijkstra, with the transient loops of reconvergence.

A network is {node: {neighbour: cost}} (symmetric).

    dv_run(net, rounds, mode, table=None, infinity=16)   synchronous rounds: every node sends its vector to every
        neighbour, then all recompute d(x, y) = min over neighbours v of c(x, v) + d_v(y).  mode "plain", "split"
        (split horizon: never advertise a route back to the neighbour it goes through) or "poison" (advertise it
        back as infinity).  Returns the tables after each round and when it converged
    dv_fail(net, a, b, ...)   converge, cut the link a-b, and run again: the count to infinity
    ls_flood(net, origin)     LSA copies sent when one node floods its link state (each node forwards a new LSA once)
    spf(net, src)             Dijkstra: (distance, next hop) to every node
    ls_reconverge(net, a, b, delays)   after the link a-b fails, node i recomputes its table at time delays[i];
        between the first and the last recomputation, forwarding can loop: returns, at each instant, the
        destinations whose forwarding path loops
"""
from __future__ import annotations

import heapq


def neighbours(net: dict, x) -> dict:
    return net[x]


def dv_run(net: dict, rounds: int = 60, mode: str = "plain", table: dict | None = None, infinity: int = 16,
           dests=None) -> dict:
    nodes = sorted(net)
    dests = dests or nodes
    if table is None:
        table = {x: {y: ((0, x) if x == y else (infinity, None)) for y in dests} for x in nodes}
    history = [{x: dict(t) for x, t in table.items()}]
    converged = None
    for r in range(1, rounds + 1):
        # every node advertises its vector to each neighbour (as that neighbour would hear it)
        adverts = {}
        for x in nodes:
            for v in net[x]:
                vec = {}
                for y in dests:
                    d, hop = table[x][y]
                    if hop == v and y != x and mode == "split":
                        continue
                    if hop == v and y != x and mode == "poison":
                        d = infinity
                    vec[y] = d
                adverts[(x, v)] = vec
        new = {}
        for x in nodes:
            new[x] = {}
            for y in dests:
                if y == x:
                    new[x][y] = (0, x)
                    continue
                best = (infinity, None)
                for v, c in sorted(net[x].items()):
                    d = adverts[(v, x)].get(y, infinity)
                    cand = min(infinity, c + d)
                    if cand < best[0]:
                        best = (cand, v)
                new[x][y] = best if best[0] < infinity else (infinity, None)
        changed = new != table
        table = new
        history.append({x: dict(t) for x, t in table.items()})
        if not changed:
            converged = r - 1
            break
    return {"table": table, "history": history, "converged": converged, "rounds": len(history) - 1}


def dv_fail(net: dict, a, b, mode: str = "plain", infinity: int = 16, dests=None) -> dict:
    first = dv_run(net, mode=mode, infinity=infinity, dests=dests)
    cut = {x: {v: c for v, c in nb.items() if {x, v} != {a, b}} for x, nb in net.items()}
    second = dv_run(cut, mode=mode, table=first["table"], infinity=infinity, dests=dests, rounds=200)
    return {"before": first, "after": second, "net": cut}


def ls_flood(net: dict, origin) -> dict:
    """Reliable flooding: the origin sends its LSA on every link; a node receiving a new LSA forwards it on every
    link except the one it came on; duplicates are dropped."""
    seen = {origin}
    queue = [(origin, None)]
    sent = 0
    hops = {origin: 0}
    while queue:
        nxt = []
        for x, came in queue:
            for v in net[x]:
                if v == came:
                    continue
                sent += 1
                if v not in seen:
                    seen.add(v)
                    hops[v] = hops[x] + 1
                    nxt.append((v, x))
        queue = nxt
    return {"sent": sent, "reached": len(seen), "max_hops": max(hops.values())}


def spf(net: dict, src) -> dict:
    dist = {src: 0}
    first = {src: src}
    pq = [(0, src, src)]
    done = set()
    while pq:
        d, x, f = heapq.heappop(pq)
        if x in done:
            continue
        done.add(x)
        first[x] = f
        for v, c in sorted(net[x].items()):
            nd = d + c
            if v not in dist or nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v, v if x == src else f))
    return {y: (dist[y], first[y]) for y in dist}


def forward_path(tables: dict, src, dst, limit: int = 64):
    path = [src]
    x = src
    for _ in range(limit):
        if x == dst:
            return path, "delivered"
        entry = tables[x].get(dst)
        if entry is None or entry[1] is None:
            return path, "dropped"
        x = entry[1]
        if x in path:
            return path + [x], "loop"
        path.append(x)
    return path, "loop"


def ls_reconverge(net: dict, a, b, delays: dict) -> dict:
    old = {x: spf(net, x) for x in net}
    cut = {x: {v: c for v, c in nb.items() if {x, v} != {a, b}} for x, nb in net.items()}
    new = {x: spf(cut, x) for x in cut}
    times = sorted(set(delays.values()))
    timeline = []
    for t in [0.0] + times:
        tables = {x: (new[x] if delays[x] <= t else old[x]) for x in net}
        # a node still using the dead link drops the packet: model that as a next hop of None
        for x in tables:
            tables[x] = {y: (d, h) if not ({x, h} == {a, b}) else (d, None) for y, (d, h) in tables[x].items()}
        loops, drops = [], []
        for s in net:
            for d in net:
                if s == d:
                    continue
                path, how = forward_path(tables, s, d)
                if how == "loop":
                    loops.append((s, d, path))
                elif how == "dropped":
                    drops.append((s, d))
        timeline.append({"t": t, "loops": loops, "drops": len(drops)})
    return {"timeline": timeline, "old": old, "new": new}
