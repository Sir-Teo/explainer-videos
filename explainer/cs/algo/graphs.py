"""Graph algorithms for Part 18, each counting its work.

A graph is ``{u: [(v, w), ...]}`` (weighted) or ``{u: [v, ...]}`` (unweighted); undirected graphs list each edge
both ways.

    euler_circuit(adj)                  Hierholzer's algorithm; None if some degree is odd or the graph is split
    bfs(adj, s)                         distances, parents, layers
    bipartite(adj)                      a 2-colouring, or an odd cycle
    dfs(adj)                            discovery and finish times, and the class of every edge
    topo_kahn(adj) / topo_dfs(adj)      a topological order, or None if there is a cycle
    tarjan_scc(adj) / kosaraju(adj)     strongly connected components
    two_sat(n, clauses)                 a satisfying assignment, or None
    dijkstra(adj, s, t=None)            distances and the number of vertices settled and edges relaxed
    bidijkstra, astar, alt_query        point-to-point searches, counting settled vertices
    CH(adj)                             contraction hierarchies: preprocessing shortcuts, query by upward search
    bellman_ford(adj, s)                distances, or a negative cycle
    floyd_warshall(n, edges), johnson(adj)
    kruskal, prim, boruvka              minimum spanning trees
    edmonds_karp(cap, s, t)             max flow, the augmenting paths, and a min cut
    hungarian(cost)                     the assignment problem in O(n^3)
    gale_shapley(men, women)            a stable matching and the number of proposals
    held_karp(dist)                     exact travelling salesman by dynamic programming over subsets
    pagerank(adj, d)                    by power iteration, with the residual after each step
"""

from __future__ import annotations

import heapq
import itertools
import math
import random
from collections import defaultdict, deque


# ------------------------------------------------------------------------------------------------- traversal
def euler_circuit(adj):
    """Undirected multigraph circuit in expected O(V+E) time, including incidence validation.

    Every non-loop edge must appear at both ends; a loop appears twice. Isolated
    vertices are allowed. Return [] for an empty graph, [u] for an edgeless graph,
    or None when non-isolated components are disconnected or some degree is odd.
    """
    incident = {u: [] for u in adj}
    pending = defaultdict(list)
    edge_count = 0
    for u, neighbours in adj.items():
        for v in neighbours:
            if v not in adj:
                raise ValueError('every endpoint must have an adjacency list')
            reverse = pending.get((v, u))
            if reverse:
                edge = reverse.pop()
            else:
                edge = edge_count
                edge_count += 1
                pending[(u, v)].append(edge)
            incident[u].append((v, edge))
    if any(pending.values()):
        raise ValueError('undirected edge incidences must be symmetric; loops appear twice')
    if any(len(vs) % 2 for vs in adj.values()):
        return None
    start = next((u for u, vs in adj.items() if vs), None)
    if edge_count == 0:
        return [next(iter(adj))] if adj else []
    used = [False] * edge_count
    stack, out = [start], []
    while stack:
        u = stack[-1]
        while incident[u] and used[incident[u][-1][1]]:
            incident[u].pop()
        if incident[u]:
            v, edge = incident[u].pop()
            used[edge] = True
            stack.append(v)
        else:
            out.append(stack.pop())
    return out[::-1] if len(out) == edge_count + 1 else None


def bfs(adj, s, weighted=False):
    """Breadth-first search; ``weighted`` if neighbours are (vertex, weight) pairs (the weights are ignored)."""
    dist, parent = {s: 0}, {s: None}
    q = deque([s])
    layers = [[s]]
    while q:
        u = q.popleft()
        for v in adj[u]:
            if weighted:
                v = v[0]
            if v not in dist:
                dist[v] = dist[u] + 1
                parent[v] = u
                if dist[v] == len(layers):
                    layers.append([])
                layers[dist[v]].append(v)
                q.append(v)
    return dist, parent, layers


def bipartite(adj):
    """A 2-colouring {u: 0/1}, or ('odd cycle', [vertices])."""
    colour, parent = {}, {}
    for s in adj:
        if s in colour:
            continue
        colour[s], parent[s] = 0, None
        q = deque([s])
        while q:
            u = q.popleft()
            for v in adj[u]:
                if v not in colour:
                    colour[v], parent[v] = 1 - colour[u], u
                    q.append(v)
                elif colour[v] == colour[u]:
                    # the two tree paths up to their common ancestor, plus the edge (u, v)
                    pu, pv = [u], [v]
                    while pu[-1] is not None:
                        pu.append(parent[pu[-1]])
                    while pv[-1] is not None:
                        pv.append(parent[pv[-1]])
                    su = set(pu)
                    a = next(x for x in pv if x in su)
                    cyc = pu[:pu.index(a) + 1] + pv[:pv.index(a)][::-1]
                    return ("odd cycle", cyc)
    return colour


def dfs(adj):
    """Iterative DFS over every vertex: discovery d, finish f, and each edge's class (tree, back, forward, cross)."""
    d, f, cls = {}, {}, {}
    t = 0
    for s in adj:
        if s in d:
            continue
        t += 1
        d[s] = t
        stack = [(s, iter(adj[s]))]
        while stack:
            u, it = stack[-1]
            for v in it:
                if v not in d:
                    cls[(u, v)] = "tree"
                    t += 1
                    d[v] = t
                    stack.append((v, iter(adj[v])))
                    break
                if v not in f:
                    cls[(u, v)] = "back"
                elif d[v] > d[u]:
                    cls[(u, v)] = "forward"
                else:
                    cls[(u, v)] = "cross"
            else:
                stack.pop()
                t += 1
                f[u] = t
    return d, f, cls


def topo_kahn(adj):
    indeg = defaultdict(int)
    for u in adj:
        for v in adj[u]:
            indeg[v] += 1
    q = deque(u for u in adj if indeg[u] == 0)
    out = []
    while q:
        u = q.popleft()
        out.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return out if len(out) == len(adj) else None


def topo_dfs(adj):
    d, f, cls = dfs(adj)
    if any(c == "back" for c in cls.values()):
        return None
    return sorted(adj, key=lambda u: -f[u])


def tarjan_scc(adj):
    """Tarjan (1972): one DFS, low-links; components in reverse topological order."""
    index, low, on, st, comps = {}, {}, set(), [], []
    counter = itertools.count()
    for s in adj:
        if s in index:
            continue
        work = [(s, iter(adj[s]))]
        index[s] = low[s] = next(counter)
        st.append(s)
        on.add(s)
        while work:
            u, it = work[-1]
            advanced = False
            for v in it:
                if v not in index:
                    index[v] = low[v] = next(counter)
                    st.append(v)
                    on.add(v)
                    work.append((v, iter(adj[v])))
                    advanced = True
                    break
                if v in on:
                    low[u] = min(low[u], index[v])
            if advanced:
                continue
            work.pop()
            if work:
                p = work[-1][0]
                low[p] = min(low[p], low[u])
            if low[u] == index[u]:
                comp = []
                while True:
                    w = st.pop()
                    on.discard(w)
                    comp.append(w)
                    if w == u:
                        break
                comps.append(comp)
    return comps


def kosaraju(adj):
    d, f, _ = dfs(adj)
    rev = defaultdict(list)
    for u in adj:
        for v in adj[u]:
            rev[v].append(u)
    seen, comps = set(), []
    for s in sorted(adj, key=lambda u: -f[u]):
        if s in seen:
            continue
        comp, st = [], [s]
        seen.add(s)
        while st:
            u = st.pop()
            comp.append(u)
            for v in rev[u]:
                if v not in seen:
                    seen.add(v)
                    st.append(v)
        comps.append(comp)
    return comps


def two_sat(n, clauses):
    """Variables 1..n; literal +i / -i; clauses (a, b) meaning a or b.  Aspvall, Plass & Tarjan (1979)."""
    adj = {lit: [] for i in range(1, n + 1) for lit in (i, -i)}
    for a, b in clauses:
        adj[-a].append(b)
        adj[-b].append(a)
    comps = tarjan_scc(adj)
    which = {}
    for k, c in enumerate(comps):
        for lit in c:
            which[lit] = k
    out = {}
    for i in range(1, n + 1):
        if which[i] == which[-i]:
            return None
        out[i] = which[i] < which[-i]        # Tarjan emits components in reverse topological order
    return out


# -------------------------------------------------------------------------------------------- shortest paths
def dijkstra(adj, s, t=None, h=None, *, settled_order=None):
    """Binary-heap Dijkstra for nonnegative weights; A* when h is supplied.

    A* requires an admissible heuristic with h(t)=0 and reopens an improved
    vertex, so inconsistent admissible estimates are supported. With consistent
    h (including zero) each vertex expands once. Return distances, parents,
    expansion count and scanned arcs. settled_order optionally records actual
    expansions, including reopenings; discovered parent keys are not that set.
    """
    dist, parent = {s: 0}, {s: None}
    done = set()
    serial = itertools.count()
    pq = [(h(s) if h else 0, next(serial), 0, s)]
    relax = expansions = 0
    while pq:
        _, _, current, u = heapq.heappop(pq)
        if current != dist.get(u) or u in done:
            continue
        done.add(u)
        expansions += 1
        if settled_order is not None:
            settled_order.append(u)
        if u == t:
            break
        for v, w in adj[u]:
            relax += 1
            nd = current + w
            if nd < dist.get(v, math.inf):
                dist[v], parent[v] = nd, u
                if h is not None:
                    done.discard(v)
                heapq.heappush(pq, (nd + (h(v) if h else 0), next(serial), nd, v))
    return dist, parent, expansions, relax


def order_settled(adj, s):
    """The order in which Dijkstra settles vertices (for drawing the wavefront)."""
    dist = {s: 0}
    done, order = set(), []
    pq = [(0, s)]
    while pq:
        d, u = heapq.heappop(pq)
        if u in done:
            continue
        done.add(u)
        order.append((u, d))
        for v, w in adj[u]:
            if d + w < dist.get(v, math.inf):
                dist[v] = d + w
                heapq.heappush(pq, (d + w, v))
    return order


def bidijkstra(adj, radj, s, t):
    """Bidirectional Dijkstra: stop when the two frontiers' minima add up to at least the best path seen."""
    if s == t:
        return 0, 0
    df, db = {s: 0}, {t: 0}
    sf, sb = set(), set()
    pf, pb = [(0, s)], [(0, t)]
    best = math.inf
    while pf and pb:
        if pf[0][0] + pb[0][0] >= best:
            break
        for pq, dist, done, other, g in ((pf, df, sf, db, adj), (pb, db, sb, df, radj)):
            if not pq:
                continue
            d, u = heapq.heappop(pq)
            if u in done:
                continue
            done.add(u)
            for v, w in g[u]:
                nd = d + w
                if nd < dist.get(v, math.inf):
                    dist[v] = nd
                    heapq.heappush(pq, (nd, v))
                if v in other:
                    best = min(best, nd + other[v])
    return best, len(sf) + len(sb)


def landmark_distances(adj, radj, landmarks):
    """Precompute directed distances to/from landmarks once, separately from queries."""
    return ([dijkstra(radj, L)[0] for L in landmarks],
            [dijkstra(adj, L)[0] for L in landmarks])


def alt_heuristic(adj, radj, landmarks, t, *, distances=None):
    """ALT lower bound; omit any difference whose operands are unreachable.

    Pass landmark_distances(...) to reuse preprocessing across target queries.
    The connected undirected city experiment yields consistent heuristics.
    """
    to_l, from_l = distances if distances is not None else landmark_distances(adj, radj, landmarks)

    def h(v):
        best = 0
        for a, b in zip(to_l, from_l):
            if v in a and t in a:
                best = max(best, a[v] - a[t])
            if v in b and t in b:
                best = max(best, b[t] - b[v])
        return best
    return h


class CH:
    """Contraction hierarchies (Geisberger, Sanders, Schultes & Delling 2008), on an undirected weighted graph.
    Contract vertices in order of edge difference; add a shortcut u-w through v unless a witness path no longer
    than it exists.  A query searches upward from both ends."""

    def __init__(self, adj, witness_limit=60):
        self.g = {u: dict() for u in adj}
        for u in adj:
            for v, w in adj[u]:
                if v != u:
                    self.g[u][v] = min(w, self.g[u].get(v, math.inf))
        self.rank, self.shortcuts = {}, 0
        work = {u: dict(nb) for u, nb in self.g.items()}
        up = {u: {} for u in adj}
        contracted = set()

        def needed(v, nb):
            adds = []
            items = list(nb.items())
            for i, (u, wu) in enumerate(items):
                # a witness search from u avoiding v, bounded by the longest shortcut it could replace
                limit = wu + max(ww for _, ww in items)
                dist = {u: 0}
                pq = [(0, u)]
                pops = 0
                while pq and pops < witness_limit:
                    d, x = heapq.heappop(pq)
                    if d > dist.get(x, math.inf) or d > limit:
                        continue
                    pops += 1
                    for y, wy in work[x].items():
                        if y == v or y in contracted:
                            continue
                        if d + wy < dist.get(y, math.inf):
                            dist[y] = d + wy
                            heapq.heappush(pq, (d + wy, y))
                for w_, ww in items[i + 1:]:
                    if dist.get(w_, math.inf) > wu + ww:
                        adds.append((u, w_, wu + ww))
            return adds

        deleted = defaultdict(int)          # contracted neighbours: spreads the contraction evenly

        def priority(v):
            nb = {u: w for u, w in work[v].items() if u not in contracted}
            return len(needed(v, nb)) - len(nb) + 2 * deleted[v]
        pq = [(priority(v), v) for v in adj]
        heapq.heapify(pq)
        r = 0
        while pq:
            p, v = heapq.heappop(pq)
            if v in contracted:
                continue
            np_ = priority(v)               # lazy update
            if pq and np_ > pq[0][0]:
                heapq.heappush(pq, (np_, v))
                continue
            nb = {u: w for u, w in work[v].items() if u not in contracted}
            for u, w_, d in needed(v, nb):
                if d < work[u].get(w_, math.inf):
                    work[u][w_] = work[w_][u] = d
                    self.shortcuts += 1
            for u, w in nb.items():
                up[v][u] = w               # edges to vertices contracted later go upward
                deleted[u] += 1
            contracted.add(v)
            self.rank[v] = r
            r += 1
        self.up = up

    def query(self, s, t):
        def search(src):
            dist = {src: 0}
            pq = [(0, src)]
            done = set()
            while pq:
                d, u = heapq.heappop(pq)
                if u in done:
                    continue
                done.add(u)
                # stall on demand: a higher neighbour already reached more cheaply proves u is not on a
                # shortest upward path, so its edges need not be relaxed
                if any(dist.get(v, math.inf) + w < d for v, w in self.up[u].items()):
                    continue
                for v, w in self.up[u].items():
                    if d + w < dist.get(v, math.inf):
                        dist[v] = d + w
                        heapq.heappush(pq, (d + w, v))
            return dist, done
        a, da = search(s)
        b, db = search(t)
        self.last_settled = (da, db)        # for pictures: the two upward searches
        best = min((a[x] + b[x] for x in a if x in b), default=math.inf)
        return best, len(da) + len(db)


def bellman_ford(adj, s):
    """Bellman (1958), Ford (1956): n - 1 rounds of relaxing every edge; returns (dist, None) or (None, cycle)."""
    verts = list(adj)
    dist, parent = {v: math.inf for v in verts}, {v: None for v in verts}
    dist[s] = 0
    last = None
    for _ in range(len(verts)):
        last = None
        for u in verts:
            if dist[u] == math.inf:
                continue
            for v, w in adj[u]:
                if dist[u] + w < dist[v] - 1e-12:
                    dist[v], parent[v] = dist[u] + w, u
                    last = v
        if last is None:
            return dist, None
    # a relaxation in round n: walk back n steps to land on the cycle, then collect it
    x = last
    for _ in range(len(verts)):
        x = parent[x]
    cyc, y = [x], parent[x]
    while y != x:
        cyc.append(y)
        y = parent[y]
    return None, cyc[::-1]


def floyd_warshall(n, edges):
    INF = math.inf
    d = [[0 if i == j else INF for j in range(n)] for i in range(n)]
    for u, v, w in edges:
        d[u][v] = min(d[u][v], w)
    for k in range(n):
        dk = d[k]
        for i in range(n):
            dik = d[i][k]
            if dik == INF:
                continue
            di = d[i]
            for j in range(n):
                if dik + dk[j] < di[j]:
                    di[j] = dik + dk[j]
    return d


def johnson(adj):
    """Johnson (1977): Bellman-Ford from a new source gives potentials p; w'(u,v) = w + p(u) - p(v) >= 0; then
    Dijkstra from every vertex.  Returns (all distances, the reweighted graph's minimum weight)."""
    g = dict(adj)
    q = object()  # a fresh identity cannot collide with a user vertex
    g[q] = [(v, 0) for v in adj]
    p, cyc = bellman_ford(g, q)
    if p is None:
        return None, cyc
    rw = {u: [(v, w + p[u] - p[v]) for v, w in adj[u]] for u in adj}
    minw = min((w for u in rw for _, w in rw[u]), default=0)
    out = {}
    for s in adj:
        d = dijkstra(rw, s)[0]
        out[s] = {v: dv - p[s] + p[v] for v, dv in d.items()}
    return out, minw


# ------------------------------------------------------------------------------------------- spanning trees
def kruskal(n, edges):
    from explainer.cs.algo.ds import UnionFind
    uf = UnionFind(n)
    tree, total = [], 0
    for w, u, v in sorted(edges):
        if uf.union(u, v):
            tree.append((u, v, w))
            total += w
    return total, tree


def prim(n, adj, s=0):
    seen, total, tree = {s}, 0, []
    pq = [(w, s, v) for v, w in adj[s]]
    heapq.heapify(pq)
    while pq and len(seen) < n:
        w, u, v = heapq.heappop(pq)
        if v in seen:
            continue
        seen.add(v)
        total += w
        tree.append((u, v, w))
        for x, wx in adj[v]:
            if x not in seen:
                heapq.heappush(pq, (wx, v, x))
    return total, tree


def boruvka(n, edges):
    """Borůvka (1926): every component picks its cheapest outgoing edge, at once; components at least halve."""
    from explainer.cs.algo.ds import UnionFind
    uf = UnionFind(n)
    total, tree, rounds = 0, [], 0
    comps = n
    while comps > 1:
        rounds += 1
        best = {}
        for w, u, v in edges:
            a, b = uf.find(u), uf.find(v)
            if a == b:
                continue
            for c in (a, b):
                if c not in best or (w, u, v) < best[c]:
                    best[c] = (w, u, v)
        if not best:
            break
        for w, u, v in set(best.values()):
            if uf.union(u, v):
                total += w
                tree.append((u, v, w))
                comps -= 1
    return total, tree, rounds


# ---------------------------------------------------------------------------------------------- flows
def edmonds_karp(cap, s, t):
    """Max flow by shortest augmenting paths (Edmonds & Karp 1972).  ``cap``: {u: {v: c}}.  Returns the flow
    value, the list of augmenting paths with their bottlenecks, and the source side of a minimum cut."""
    if s == t:
        raise ValueError("source and sink must differ")
    res = defaultdict(lambda: defaultdict(int))
    for u in cap:
        for v, c in cap[u].items():
            res[u][v] += c
            res[v][u] += 0
    flow, paths = 0, []
    while True:
        parent = {s: None}
        q = deque([s])
        while q and t not in parent:
            u = q.popleft()
            for v, c in res[u].items():
                if c > 0 and v not in parent:
                    parent[v] = u
                    q.append(v)
        if t not in parent:
            break
        path, v = [t], t
        while parent[v] is not None:
            v = parent[v]
            path.append(v)
        path = path[::-1]
        b = min(res[a][c] for a, c in zip(path, path[1:]))
        for a, c in zip(path, path[1:]):
            res[a][c] -= b
            res[c][a] += b
        flow += b
        paths.append((path, b))
    side = set(parent)
    return flow, paths, side


def ford_fulkerson_dfs(cap, s, t):
    """Augment along any path found by DFS: the count of augmentations can depend on the capacities."""
    if s == t:
        raise ValueError("source and sink must differ")
    res = defaultdict(lambda: defaultdict(int))
    for u in cap:
        for v, c in cap[u].items():
            res[u][v] += c
            res[v][u] += 0
    flow, aug = 0, 0
    while True:
        parent = {s: None}
        st = [s]
        while st and t not in parent:
            u = st.pop()
            for v in sorted(res[u], key=lambda x: str(x)):
                if res[u][v] > 0 and v not in parent:
                    parent[v] = u
                    st.append(v)
        if t not in parent:
            return flow, aug
        path, v = [t], t
        while parent[v] is not None:
            v = parent[v]
            path.append(v)
        path = path[::-1]
        b = min(res[a][c] for a, c in zip(path, path[1:]))
        for a, c in zip(path, path[1:]):
            res[a][c] -= b
            res[c][a] += b
        flow += b
        aug += 1


def hungarian(cost):
    """The assignment problem (Kuhn 1955, Munkres 1957), O(n^3) with potentials.  Returns (total, assignment)."""
    n = len(cost)
    INF = math.inf
    u, v = [0] * (n + 1), [0] * (n + 1)
    p, way = [0] * (n + 1), [0] * (n + 1)
    for i in range(1, n + 1):
        p[0] = i
        j0 = 0
        minv = [INF] * (n + 1)
        used = [False] * (n + 1)
        while True:
            used[j0] = True
            i0, delta, j1 = p[j0], INF, 0
            for j in range(1, n + 1):
                if not used[j]:
                    cur = cost[i0 - 1][j - 1] - u[i0] - v[j]
                    if cur < minv[j]:
                        minv[j], way[j] = cur, j0
                    if minv[j] < delta:
                        delta, j1 = minv[j], j
            for j in range(n + 1):
                if used[j]:
                    u[p[j]] += delta
                    v[j] -= delta
                else:
                    minv[j] -= delta
            j0 = j1
            if p[j0] == 0:
                break
        while True:
            j1 = way[j0]
            p[j0] = p[j1]
            j0 = j1
            if j0 == 0:
                break
    assign = [0] * n
    for j in range(1, n + 1):
        assign[p[j] - 1] = j - 1
    return sum(cost[i][assign[i]] for i in range(n)), assign


def gale_shapley(prop_pref, recv_pref):
    """Gale & Shapley (1962): proposers propose in order of preference; receivers hold the best offer so far.
    Returns (matching proposer -> receiver, proposals made)."""
    n = len(prop_pref)
    rank = [{p: r for r, p in enumerate(prefs)} for prefs in recv_pref]
    nxt = [0] * n
    held = [None] * n
    free = deque(range(n))
    proposals = 0
    while free:
        p = free.popleft()
        r = prop_pref[p][nxt[p]]
        nxt[p] += 1
        proposals += 1
        if held[r] is None:
            held[r] = p
        elif rank[r][p] < rank[r][held[r]]:
            free.append(held[r])
            held[r] = p
        else:
            free.append(p)
    match = {held[r]: r for r in range(n)}
    return match, proposals


def is_stable(match, prop_pref, recv_pref):
    rank_p = [{r: k for k, r in enumerate(pr)} for pr in prop_pref]
    rank_r = [{p: k for k, p in enumerate(pr)} for pr in recv_pref]
    partner = {r: p for p, r in match.items()}
    for p, r_now in match.items():
        for r in prop_pref[p][:rank_p[p][r_now]]:
            if rank_r[r][p] < rank_r[r][partner[r]]:
                return False
    return True


# ---------------------------------------------------------------------------------------------- hard ones
def held_karp(d):
    """Exact TSP over all n cities in O(2^n n^2) (Bellman 1962; Held & Karp 1962)."""
    n = len(d)
    if any(len(row) != n for row in d):
        raise ValueError("the distance matrix must be square")
    if n <= 1:
        return 0
    best = {(1, 0): 0}
    for size in range(2, n + 1):
        for subset in itertools.combinations(range(1, n), size - 1):
            mask = 1 | sum(1 << k for k in subset)
            for j in subset:
                prev = mask ^ (1 << j)
                best[(mask, j)] = min(best[(prev, k)] + d[k][j] for k in ([0] + list(subset)) if k != j and
                                      (prev, k) in best)
    full = (1 << n) - 1
    return min(best[(full, j)] + d[j][0] for j in range(1, n))


def pagerank(adj, d=0.85, iters=100, tol=1e-12):
    """Brin & Page (1998): the stationary distribution of a surfer who follows a random link with probability d and
    jumps anywhere otherwise.  Dangling pages spread their rank evenly.  Returns (rank, residuals)."""
    if not 0 <= d < 1 or not isinstance(iters, int) or iters < 1 or tol < 0:
        raise ValueError("require 0 <= damping < 1, positive iterations and nonnegative tolerance")
    nodes = list(adj)
    n = len(nodes)
    if not nodes:
        return {}, []
    r = {u: 1 / n for u in nodes}
    res = []
    for _ in range(iters):
        dang = sum(r[u] for u in nodes if not adj[u])
        new = {u: (1 - d) / n + d * dang / n for u in nodes}
        for u in nodes:
            if adj[u]:
                share = d * r[u] / len(adj[u])
                for v in adj[u]:
                    new[v] += share
        delta = sum(abs(new[u] - r[u]) for u in nodes)
        res.append(delta)
        r = new
        if delta < tol:
            break
    return r, res


def greedy_colouring(adj, order=None):
    colour = {}
    for u in order or adj:
        used = {colour[v] for v in adj[u] if v in colour}
        c = 0
        while c in used:
            c += 1
        colour[u] = c
    return colour


# ---------------------------------------------------------------------------------------------- generators
def grid_city(w, h, rng, jitter=0.4, arterial=8):
    """A city: a w x h grid of intersections with road lengths around 1, some roads missing, a few fast
    diagonals.  Returns (adj with (v, length), positions)."""
    pos = {(x, y): (x + rng.uniform(-jitter, jitter) * 0.3, y + rng.uniform(-jitter, jitter) * 0.3)
           for x in range(w) for y in range(h)}
    adj = {p: [] for p in pos}

    def add(a, b, f=1.0):
        L = f * math.dist(pos[a], pos[b])
        adj[a].append((b, L))
        adj[b].append((a, L))
    for x in range(w):
        for y in range(h):
            # every eighth street is an arterial road: three times as fast, never closed
            if x + 1 < w and (y % arterial == 0 or rng.random() > 0.08):
                add((x, y), (x + 1, y), 0.35 if y % arterial == 0 else 1.0)
            if y + 1 < h and (x % arterial == 0 or rng.random() > 0.08):
                add((x, y), (x, y + 1), 0.35 if x % arterial == 0 else 1.0)
    return adj, pos


def random_web(n, m_per, rng):
    """Preferential attachment (Barabási & Albert 1999), directed links from each new page to m_per older ones."""
    if n < 0 or m_per < 0:
        raise ValueError("graph size and links per page must be nonnegative")
    if n < 2:
        return {u: [] for u in range(n)}
    adj = {0: [], 1: [0]}
    targets = [0, 1]
    for u in range(2, n):
        out = set()
        while len(out) < min(m_per, u):
            out.add(rng.choice(targets))
        adj[u] = sorted(out)
        targets.extend(out)
        targets.append(u)
    return adj


def colour_k(adj, k):
    """A proper k-colouring by backtracking, most-constrained vertex first (DSATUR order), or None."""
    colour = {}
    verts = list(adj)

    def pick():
        best, key = None, None
        for v in verts:
            if v in colour:
                continue
            sat = len({colour[u] for u in adj[v] if u in colour})
            kk = (sat, len(adj[v]))
            if key is None or kk > key:
                best, key = v, kk
        return best

    def go():
        v = pick()
        if v is None:
            return True
        used = {colour[u] for u in adj[v] if u in colour}
        for c in range(k):
            if c not in used:
                colour[v] = c
                if go():
                    return True
                del colour[v]
        return False
    return dict(colour) if go() else None
