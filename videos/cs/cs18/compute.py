"""Precompute everything numerical in Part 18 of *Computer Science, Built* ("Graphs").

    python -m videos.cs.cs18.compute              # everything missing
    python -m videos.cs.cs18.compute --force astar

Results are cached in ``.cache/cs18/<name>.json``; scenes call ``load(name)``.  The instrument is
``explainer/cs/algo/graphs.py`` (traversals, components, shortest paths with A*, landmarks and contraction
hierarchies, spanning trees, flows, matchings, Held-Karp and PageRank, each counting its work), tested in
tests/test_cs18_graphs.py.  Items that time code (``representation``, ``hard``) run on this machine.

Items:
    euler          Königsberg's degrees; an Euler circuit found by Hierholzer's algorithm
    representation adjacency matrix against adjacency lists: memory and the time to visit every edge
    bfs            a maze explored in layers; bipartite or not
    dfs            discovery and finish times and edge classes on a small directed graph
    topo           a build's dependency graph sorted two ways
    scc            Tarjan's components on a small graph; a random web's bow tie; 2-SAT
    dijkstra       the wavefront over a city grid; settled vertices and relaxations
    bellman        negative edges; arbitrage as a negative cycle in -log rates
    allpairs       Floyd-Warshall and Johnson on the same graph
    astar          Dijkstra, bidirectional, A*, landmarks and contraction hierarchies on one city
    mst            Kruskal, Prim and Borůvka on random points
    flow           Edmonds-Karp step by step; the bad case for DFS augmenting paths; the min cut
    matching       Gale-Shapley proposals and stability; the Hungarian algorithm
    hard           Euler tours in linear time against Held-Karp's 2^n n^2, timed
    pagerank       power iteration on a synthetic web: convergence and the top pages
    planar         Euler's formula on a planar map; greedy colouring
"""

from __future__ import annotations

import json
import math
import random
import time
from collections import Counter

import numpy as np

from explainer.ai.cache import Cache

CACHE = Cache("cs18")
load = CACHE.load


def compute_euler() -> dict:
    from explainer.cs.algo import graphs as G
    # Königsberg: four land masses, seven bridges
    k = {"A": ["B", "B", "C", "C", "D"], "B": ["A", "A", "D"], "C": ["A", "A", "D"], "D": ["A", "B", "C"]}
    deg = {u: len(v) for u, v in k.items()}
    # an envelope with a roof (the house of Nikolaus) has two odd vertices: a path but no circuit; add one edge
    house = {0: [1, 2, 4], 1: [0, 2, 3, 4], 2: [0, 1, 3, 4], 3: [1, 2], 4: [0, 1, 2]}
    # a graph with all even degrees: the circuit
    g = {0: [1, 3, 4, 5], 1: [0, 2], 2: [1, 3], 3: [0, 2, 4, 5], 4: [0, 3], 5: [0, 3]}
    circ = G.euler_circuit(g)
    return {"konigsberg_degrees": deg, "konigsberg_circuit": G.euler_circuit(k), "house_degrees":
            {u: len(v) for u, v in house.items()}, "graph": {str(u): v for u, v in g.items()}, "circuit": circ}


def compute_representation() -> dict:
    rows = []
    for n, deg in ((1000, 5), (10000, 5), (3000, 1000)):
        rng = random.Random(n)
        m = n * deg // 2
        edges = set()
        while len(edges) < m:
            a, b = rng.randrange(n), rng.randrange(n)
            if a != b:
                edges.add((min(a, b), max(a, b)))
        lists = [[] for _ in range(n)]
        for a, b in edges:
            lists[a].append(b)
            lists[b].append(a)
        t0 = time.perf_counter()
        c = 0
        for u in range(n):
            for v in lists[u]:
                c += 1
        t_list = time.perf_counter() - t0
        mat = np.zeros((n, n), dtype=bool)
        for a, b in edges:
            mat[a, b] = mat[b, a] = True
        t0 = time.perf_counter()
        c2 = 0
        for u in range(min(n, 2000)):
            c2 += int(np.count_nonzero(mat[u]))
        t_mat = (time.perf_counter() - t0) * n / min(n, 2000)
        rows.append({"n": n, "m": m, "list_bytes": 8 * 2 * m + 8 * n, "matrix_bytes": n * n // 8,
                     "list_s": t_list, "matrix_s": t_mat, "visited": c})
        print(rows[-1])
    return {"rows": rows}


def maze(w, h, rng, loops=0.08):
    """A perfect maze by randomized DFS, then a few extra openings so there are cycles."""
    cells = [(x, y) for x in range(w) for y in range(h)]
    adj = {c: [] for c in cells}
    seen = {(0, 0)}
    st = [(0, 0)]
    while st:
        x, y = st[-1]
        nb = [(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
              if 0 <= x + dx < w and 0 <= y + dy < h and (x + dx, y + dy) not in seen]
        if not nb:
            st.pop()
            continue
        n = rng.choice(nb)
        adj[(x, y)].append(n)
        adj[n].append((x, y))
        seen.add(n)
        st.append(n)
    for c in cells:
        x, y = c
        for n in ((x + 1, y), (x, y + 1)):
            if n in adj and n not in adj[c] and rng.random() < loops:
                adj[c].append(n)
                adj[n].append(c)
    return adj


def compute_bfs() -> dict:
    from explainer.cs.algo import graphs as G
    rng = random.Random(18)
    w, h = 24, 14
    adj = maze(w, h, rng)
    dist, parent, layers = G.bfs(adj, (0, 0))
    goal = (w - 1, h - 1)
    path = [goal]
    while parent[path[-1]] is not None:
        path.append(parent[path[-1]])
    walls = []
    for x in range(w):
        for y in range(h):
            if x + 1 < w and (x + 1, y) not in adj[(x, y)]:
                walls.append([x + 0.5, y - 0.5, x + 0.5, y + 0.5])
            if y + 1 < h and (x, y + 1) not in adj[(x, y)]:
                walls.append([x - 0.5, y + 0.5, x + 0.5, y + 0.5])
    grid_bip = isinstance(G.bipartite(adj), dict)
    tri = G.bipartite({0: [1, 2], 1: [0, 2], 2: [0, 1]})
    return {"w": w, "h": h, "dist": {f"{x},{y}": d for (x, y), d in dist.items()}, "layers": len(layers),
            "path": [list(p) for p in path[::-1]], "walls": walls, "maze_bipartite": grid_bip, "triangle": tri[1]}


def compute_dfs() -> dict:
    from explainer.cs.algo import graphs as G
    g = {"a": ["b", "e", "d"], "b": ["c", "e"], "c": ["a"], "d": ["e"], "e": ["c", "f"], "f": [], "g": ["f", "h"],
         "h": ["g"]}
    d, f, cls = G.dfs(g)
    return {"graph": g, "d": d, "f": f, "classes": {f"{u}->{v}": c for (u, v), c in cls.items()}}


def compute_topo() -> dict:
    from explainer.cs.algo import graphs as G
    dag = {"lexer.c": ["lexer.o"], "parser.c": ["parser.o"], "ast.h": ["lexer.o", "parser.o", "codegen.o"],
           "codegen.c": ["codegen.o"], "lexer.o": ["pebblec"], "parser.o": ["pebblec"], "codegen.o": ["pebblec"],
           "pebblec": ["tests"], "tests": []}
    k = G.topo_kahn(dag)
    dd = G.topo_dfs(dag)
    cyc = dict(dag)
    cyc["tests"] = ["ast.h"]
    return {"dag": dag, "kahn": k, "dfs": dd, "cycle_result": G.topo_kahn(cyc)}


def compute_scc() -> dict:
    from explainer.cs.algo import graphs as G
    g = {1: [2], 2: [3, 4], 3: [1], 4: [5], 5: [6], 6: [4], 7: [6, 8], 8: [7]}
    comps = G.tarjan_scc(g)
    # a random web with some reciprocal links: the bow tie (Broder et al. 2000)
    rng = random.Random(7)
    n = 20000
    web = G.random_web(n, 3, rng)
    for u in range(n):
        if rng.random() < 0.25 and web[u]:
            v = rng.choice(web[u])
            web[v].append(u)
    sc = G.tarjan_scc(web)
    big = max(sc, key=len)
    core = set(big)
    s0 = next(iter(core))
    fwd = {s0}
    st = [s0]
    while st:
        u = st.pop()
        for v in web[u]:
            if v not in fwd:
                fwd.add(v)
                st.append(v)
    rev = {u: [] for u in web}
    for u in web:
        for v in web[u]:
            rev[v].append(u)
    bwd = {s0}
    st = [s0]
    while st:
        u = st.pop()
        for v in rev[u]:
            if v not in bwd:
                bwd.add(v)
                st.append(v)
    out_ = len(fwd - core)
    in_ = len(bwd - core)
    sat = G.two_sat(3, [(1, 2), (-1, 3), (-2, -3), (2, 3)])
    unsat = G.two_sat(2, [(1, 2), (1, -2), (-1, 2), (-1, -2)])
    return {"graph": {str(u): v for u, v in g.items()}, "comps": comps, "web_n": n, "core": len(core),
            "in": in_, "out": out_, "other": n - len(core) - in_ - out_, "sizes": Counter(len(c) for c in sc).most_common(5),
            "sat": sat, "unsat": unsat}


def _city(w=60, h=40, seed=18):
    from explainer.cs.algo import graphs as G
    rng = random.Random(seed)
    return G.grid_city(w, h, rng)


def compute_dijkstra() -> dict:
    from explainer.cs.algo import graphs as G
    adj, pos = _city()
    s = (5, 20)
    order = G.order_settled(adj, s)
    dist, parent, settled, relax = G.dijkstra(adj, s)
    m = sum(len(v) for v in adj.values())
    return {"pos": {f"{x},{y}": p for (x, y), p in pos.items()}, "order": [[list(u), d] for u, d in order],
            "edges": [[list(u), list(v)] for u in adj for v, _ in adj[u] if u < v], "n": len(adj), "m": m // 2,
            "settled": settled, "relax": relax, "source": list(s)}


def compute_bellman() -> dict:
    from explainer.cs.algo import graphs as G
    # illustrative exchange rates (not market data), with one cycle that gains
    rates = {("USD", "EUR"): 0.920, ("EUR", "USD"): 1.084, ("USD", "JPY"): 150.2, ("JPY", "USD"): 1 / 150.9,
             ("EUR", "JPY"): 164.4, ("JPY", "EUR"): 1 / 164.6, ("USD", "GBP"): 0.786, ("GBP", "USD"): 1.268,
             ("EUR", "GBP"): 0.853, ("GBP", "EUR"): 1.170, ("GBP", "JPY"): 190.8, ("JPY", "GBP"): 1 / 191.4}
    adj = {c: [] for c in {a for a, _ in rates}}
    for (a, b), r in rates.items():
        adj[a].append((b, -math.log(r)))
    dist, cyc = G.bellman_ford(adj, "USD")
    gain = 1.0
    if cyc:
        for a, b in zip(cyc, cyc[1:] + cyc[:1]):
            gain *= rates[(a, b)]
    return {"rates": {f"{a}>{b}": r for (a, b), r in rates.items()}, "cycle": cyc, "gain": gain}


def compute_allpairs() -> dict:
    from explainer.cs.algo import graphs as G
    rng = random.Random(9)
    n = 150
    # negative edges but no negative cycle: w = c + p(u) - p(v) with c >= 0 and random potentials p
    pot = [rng.randint(0, 30) for _ in range(n)]
    adj = {i: [] for i in range(n)}
    for _ in range(6 * n):
        a, b = rng.randrange(n), rng.randrange(n)
        if a != b:
            adj[a].append((b, rng.randint(0, 20) + pot[a] - pot[b]))
    edges = [(u, v, w) for u in adj for v, w in adj[u]]
    t0 = time.perf_counter()
    fw = G.floyd_warshall(n, edges)
    t_fw = time.perf_counter() - t0
    neg = any(fw[i][i] < 0 for i in range(n))
    if neg:
        for u in adj:
            adj[u] = [(v, abs(w)) for v, w in adj[u]]
        edges = [(u, v, w) for u in adj for v, w in adj[u]]
        fw = G.floyd_warshall(n, edges)
    t0 = time.perf_counter()
    J, minw = G.johnson(adj)
    t_j = time.perf_counter() - t0
    agree = all(abs(J[u].get(v, math.inf) - fw[u][v]) < 1e-9 for u in range(n) for v in range(n) if fw[u][v] < math.inf)
    return {"n": n, "m": len(edges), "fw_s": t_fw, "johnson_s": t_j, "agree": agree, "negative_edges":
            sum(1 for _, _, w in edges if w < 0), "min_reweighted": minw, "fw_ops": n ** 3}


def compute_astar() -> dict:
    from explainer.cs.algo import graphs as G
    adj, pos = _city(80, 60, seed=3)
    rng = random.Random(4)
    t0 = time.perf_counter()
    ch = G.CH(adj)
    ch_s = time.perf_counter() - t0
    corners = [(0, 0), (79, 0), (0, 59), (79, 59)]
    qs = [((rng.randrange(80), rng.randrange(60)), (rng.randrange(80), rng.randrange(60))) for _ in range(40)]
    tot = Counter()
    for s, t in qs:
        d, _, n_d, _ = G.dijkstra(adj, s, t)
        _, n_b = G.bidijkstra(adj, adj, s, t)
        # admissible: straight-line distance at the fastest speed (arterials, 0.35 per unit)
        da, _, n_a, _ = G.dijkstra(adj, s, t, h=lambda v, t=t: 0.35 * math.dist(pos[v], pos[t]))
        assert abs(da[t] - d[t]) < 1e-9
        hh = G.alt_heuristic(adj, adj, corners, t)
        _, _, n_l, _ = G.dijkstra(adj, s, t, h=hh)
        dl, _, n_l2, _ = G.dijkstra(adj, s, t, h=hh)
        assert abs(dl[t] - d[t]) < 1e-9
        dc, n_c = ch.query(s, t)
        assert abs(dc - d[t]) < 1e-9
        tot.update({"dijkstra": n_d, "bidirectional": n_b, "astar": n_a, "alt": n_l, "ch": n_c})
    # one query, for the picture: the settled sets
    s, t = (8, 30), (72, 32)
    pics = {}
    for name, h in (("dijkstra", None), ("astar", lambda v: 0.35 * math.dist(pos[v], pos[t]))):
        dist, parent, _, _ = G.dijkstra(adj, s, t, h=h)
        pics[name] = [list(u) for u in parent]
    # a diagonal query, where the straight line is a poor guide: A* against landmarks, and the hierarchy
    s2, t2 = (6, 8), (72, 52)
    for name, h in (("astar2", lambda v: 0.35 * math.dist(pos[v], pos[t2])),
                    ("alt2", G.alt_heuristic(adj, adj, corners, t2))):
        dist, parent, _, _ = G.dijkstra(adj, s2, t2, h=h)
        pics[name] = [list(u) for u in parent]
    dc, _ = ch.query(s2, t2)
    assert abs(dc - G.dijkstra(adj, s2, t2)[0][t2]) < 1e-9
    pics["ch_s"] = [list(u) for u in ch.last_settled[0]]
    pics["ch_t"] = [list(u) for u in ch.last_settled[1]]
    pics["s2"], pics["t2"] = list(s2), list(t2)
    return {"n": len(adj), "queries": len(qs), "avg": {k: v / len(qs) for k, v in tot.items()},
            "ch_build_s": ch_s, "shortcuts": ch.shortcuts, "pics": pics, "s": list(s), "t": list(t),
            "pos": {f"{x},{y}": p for (x, y), p in pos.items()}}


def compute_mst() -> dict:
    from explainer.cs.algo import graphs as G
    rng = random.Random(12)
    n = 120
    pts = [(rng.uniform(-6, 6), rng.uniform(-3.2, 3.2)) for _ in range(n)]
    edges = [(math.dist(pts[i], pts[j]), i, j) for i in range(n) for j in range(i + 1, n)]
    adj = {i: [] for i in range(n)}
    for w, i, j in edges:
        adj[i].append((j, w))
        adj[j].append((i, w))
    k, tree = G.kruskal(n, edges)
    p, _ = G.prim(n, adj)
    b, _, rounds = G.boruvka(n, edges)
    return {"pts": pts, "tree": [[u, v] for u, v, _ in tree], "kruskal": k, "prim": p, "boruvka": b,
            "rounds": rounds, "n": n, "m": len(edges)}


def compute_flow() -> dict:
    from explainer.cs.algo import graphs as G
    cap = {"s": {"a": 10, "b": 10}, "a": {"b": 2, "c": 4, "d": 8}, "b": {"d": 9}, "c": {"t": 10},
           "d": {"c": 6, "t": 10}}
    f, paths, side = G.edmonds_karp(cap, "s", "t")
    cut = [[u, v, c] for u in side for v, c in cap.get(u, {}).items() if v not in side]
    bad = {"s": {"a": 1000, "b": 1000}, "a": {"b": 1, "t": 1000}, "b": {"t": 1000}}
    # the unlucky choice: always an augmenting path through the middle edge, forwards then backwards
    res = {("s", "a"): 1000, ("s", "b"): 1000, ("a", "b"): 1, ("b", "a"): 0, ("a", "t"): 1000, ("b", "t"): 1000}
    aug = 0
    while True:
        for path in (("s", "a", "b", "t"), ("s", "b", "a", "t")):
            if all(res[e] > 0 for e in zip(path, path[1:])):
                break
        else:
            break
        bneck = min(res[e] for e in zip(path, path[1:]))
        for u, v in zip(path, path[1:]):
            res[(u, v)] -= bneck
            res[(v, u)] = res.get((v, u), 0) + bneck
        aug += 1
    ek = len(G.edmonds_karp(bad, "s", "t")[1])
    # a larger random network: augmentations against the bound O(VE)
    rng = random.Random(3)
    n = 60
    big = {i: {} for i in range(n)}
    for _ in range(400):
        a, b = rng.sample(range(n), 2)
        big[a][b] = rng.randint(1, 50)
    fb, pb, _ = G.edmonds_karp(big, 0, n - 1)
    return {"cap": cap, "flow": f, "paths": paths, "side": sorted(side), "cut": cut, "bad_ff": aug, "bad_ek": ek,
            "big_n": n, "big_m": 400, "big_flow": fb, "big_aug": len(pb)}


def compute_matching() -> dict:
    from explainer.cs.algo import graphs as G
    rows = []
    for n in (10, 100, 1000):
        props = []
        for r in range(5):
            rng = random.Random(100 * n + r)
            P = [rng.sample(range(n), n) for _ in range(n)]
            R = [rng.sample(range(n), n) for _ in range(n)]
            m, pr = G.gale_shapley(P, R)
            if n <= 100:
                assert G.is_stable(m, P, R)
            props.append(pr)
        H = sum(1 / k for k in range(1, n + 1))
        rows.append({"n": n, "proposals": sum(props) / len(props), "nHn": n * H, "worst": n * n})
        print(rows[-1])
    # a small example to animate
    for seed in range(200):           # a small example in which the two sides' optimal matchings differ
        rng = random.Random(seed)
        n = 4
        P = [rng.sample(range(n), n) for _ in range(n)]
        R = [rng.sample(range(n), n) for _ in range(n)]
        m, pr = G.gale_shapley(P, R)
        mR, prR = G.gale_shapley(R, P)
        if {r: p for p, r in mR.items()} != m and pr >= 6:
            break
    rng = random.Random(6)
    cost = [[rng.randint(1, 99) for _ in range(60)] for _ in range(60)]
    t0 = time.perf_counter()
    total, assign = G.hungarian(cost)
    t_h = time.perf_counter() - t0
    return {"rows": rows, "P": P, "R": R, "match": {str(k): v for k, v in m.items()}, "proposals": pr,
            "match_r": {str(k): v for k, v in mR.items()}, "hungarian_n": 60, "hungarian_total": total,
            "hungarian_s": t_h, "greedy_total": _greedy_assign(cost)}


def _greedy_assign(cost):
    n = len(cost)
    used, total = set(), 0
    for i in range(n):
        j = min((j for j in range(n) if j not in used), key=lambda j: cost[i][j])
        used.add(j)
        total += cost[i][j]
    return total


def compute_hard() -> dict:
    from explainer.cs.algo import graphs as G
    rows = []
    for n in range(6, 17, 2):
        rng = random.Random(n)
        pts = [(rng.random(), rng.random()) for _ in range(n)]
        D = [[math.dist(a, b) for b in pts] for a in pts]
        best = math.inf
        for _ in range(3):                  # best of three: the machine is shared
            t0 = time.perf_counter()
            G.held_karp(D)
            best = min(best, time.perf_counter() - t0)
        rows.append({"n": n, "held_karp_s": best, "brute": math.factorial(n - 1) / 2,
                     "hk_ops": 2 ** n * n * n})
        print(rows[-1])
    # Euler: a big even-degree graph (a torus grid), circuit in linear time
    w = 300
    g = {(x, y): [((x + 1) % w, y), ((x - 1) % w, y), (x, (y + 1) % w), (x, (y - 1) % w)] for x in range(w) for y in
         range(w)}
    t_e = math.inf
    for _ in range(3):
        t0 = time.perf_counter()
        c = G.euler_circuit(g)
        t_e = min(t_e, time.perf_counter() - t0)
    # Hamilton's icosian game: the dodecahedron, drawn flat (outer pentagon, a ring of ten, inner pentagon)
    edges = [(i, (i + 1) % 5) for i in range(5)] + [(i, 5 + 2 * i) for i in range(5)]
    edges += [(5 + j, 5 + (j + 1) % 10) for j in range(10)] + [(15 + i, 6 + 2 * i) for i in range(5)]
    edges += [(15 + i, 15 + (i + 1) % 5) for i in range(5)]
    adj = {v: set() for v in range(20)}
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    assert all(len(x) == 3 for x in adj.values()) and len(edges) == 30
    cycles = []

    def walk(path, seen):
        if len(path) == 20:
            if 0 in adj[path[-1]]:
                cycles.append(list(path))
            return
        for v in sorted(adj[path[-1]]):
            if v not in seen:
                seen.add(v)
                path.append(v)
                walk(path, seen)
                path.pop()
                seen.discard(v)
    walk([0], {0})
    distinct = {frozenset(frozenset((c[i], c[(i + 1) % 20])) for i in range(20)) for c in cycles}
    return {"rows": rows, "euler_edges": len(c) - 1, "euler_s": t_e, "dodeca_edges": edges,
            "dodeca_cycle": cycles[0], "dodeca_cycles": len(distinct)}


def compute_pagerank() -> dict:
    from explainer.cs.algo import graphs as G
    rng = random.Random(15)
    n = 20000
    web = G.random_web(n, 4, rng)
    r, res = G.pagerank(web)
    indeg = Counter(v for u in web for v in web[u])
    top = sorted(r, key=lambda u: -r[u])[:10]
    top_in = sorted(indeg, key=lambda u: -indeg[u])[:10]
    small = G.random_web(12, 2, random.Random(2))
    rs, _ = G.pagerank(small)
    return {"n": n, "m": sum(len(v) for v in web.values()), "residuals": res, "top": [[u, r[u], indeg[u]] for u in top],
            "overlap_top10": len(set(top) & set(top_in)), "small": {str(u): v for u, v in small.items()},
            "small_rank": {str(u): v for u, v in rs.items()}}


def compute_planar() -> dict:
    from explainer.cs.algo import graphs as G
    rng = random.Random(21)
    # a triangulated grid: planar by construction
    w, h = 9, 6
    V = [(x, y) for x in range(w) for y in range(h)]
    E = set()
    for x in range(w):
        for y in range(h):
            if x + 1 < w:
                E.add(((x, y), (x + 1, y)))
            if y + 1 < h:
                E.add(((x, y), (x, y + 1)))
            if x + 1 < w and y + 1 < h:
                E.add(((x, y), (x + 1, y + 1)) if rng.random() < 0.5 else ((x + 1, y), (x, y + 1)))
    F = 2 * (w - 1) * (h - 1) + 1          # the triangles, plus the outer face
    adj = {v: [] for v in V}
    for a, b in E:
        adj[a].append(b)
        adj[b].append(a)
    col = G.greedy_colouring(adj)
    order = sorted(V, key=lambda v: -len(adj[v]))
    col2 = G.greedy_colouring(adj, order)
    four = G.colour_k(adj, 4)
    assert four and all(four[u] != four[v] for u in adj for v in adj[u])
    three = G.colour_k(adj, 3)
    return {"V": len(V), "E": len(E), "F": F, "euler": len(V) - len(E) + F, "greedy": max(col.values()) + 1,
            "four_found": True, "three_possible": three is not None,
            "greedy_by_degree": max(col2.values()) + 1, "max_degree": max(len(a) for a in adj.values()),
            "bound_3v6": 3 * len(V) - 6, "edges": [[list(a), list(b)] for a, b in sorted(E)],
            "four": [[list(v), c] for v, c in four.items()], "greedy_col": [[list(v), c] for v, c in col.items()]}


ITEMS = {
    "euler": compute_euler, "representation": compute_representation, "bfs": compute_bfs, "dfs": compute_dfs,
    "topo": compute_topo, "scc": compute_scc, "dijkstra": compute_dijkstra, "bellman": compute_bellman,
    "allpairs": compute_allpairs, "astar": compute_astar, "mst": compute_mst, "flow": compute_flow,
    "matching": compute_matching, "hard": compute_hard, "pagerank": compute_pagerank, "planar": compute_planar,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
