"""Lab 18: route across a city with Dijkstra and A*, and certify maximum flows by cuts found by brute force."""

from videos.coursekit import labs
import itertools
import math

import numpy as np

from explainer.cs.algo import graphs

TITLE = "Exact routes with less search, and flows certified by cuts"
GOAL = ("On a seeded city of 1,200 intersections built by the series' generator, answer thirty route queries with "
        "Dijkstra, bidirectional Dijkstra and A*, check that all three return the same distance, and count the "
        "vertices each expands. Then run Edmonds-Karp on random networks and compare the flow with the smallest "
        "cut among all 1,024 ways to split the vertices; and build a spanning tree two ways.")
TASKS = [
    "Multiply A*'s estimate by 3 (so it can overestimate). Find a query whose route gets longer, and count the vertices expanded.",
    "Give one street a negative length and compare graphs.dijkstra with graphs.bellman_ford from the same source. Which distances differ?",
    "Replace graphs.edmonds_karp by graphs.ford_fulkerson_dfs on the same networks. Is the flow value the same? Is the number of augmenting paths?",
]
QUERIES, NETWORKS, FAST = 30, 25, 0.35  # FAST: the cheapest cost per unit of distance (the arterial roads)


def network(rng, n=12, arcs=34):
    """A random directed network on n vertices with integer capacities; 0 is the source and n - 1 the sink."""
    cap = {u: {} for u in range(n)}
    for u in range(n - 1):  # a path through every vertex, so the sink can be reached
        cap[u][u + 1] = int(rng.integers(1, 10))
    for _ in range(arcs):
        u, v = (int(x) for x in rng.choice(n, 2, replace=False))
        cap[u][v] = int(rng.integers(1, 10))
    return cap


def smallest_cut(cap):
    """The least capacity leaving S, over every vertex set S that holds the source and not the sink."""
    n = len(cap)
    best = math.inf
    for mask in itertools.product((False, True), repeat=n - 2):
        S = {0} | {u + 1 for u, inside in enumerate(mask) if inside}
        best = min(best, sum(c for u in S for v, c in cap[u].items() if v not in S))
    return best


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. thirty exact routes, three ways
    adj, pos = graphs.grid_city(40, 30, rng)
    reached = graphs.bfs(adj, (0, 0), weighted=True)[0]  # keep the part of the city joined to the corner
    adj = {u: nbrs for u, nbrs in adj.items() if u in reached}
    verts = list(adj)
    rows, picture = [], None
    for _ in range(QUERIES):
        s, t = (verts[int(i)] for i in rng.choice(len(verts), 2, replace=False))
        plain, astar = [], []
        dist, _, n_dij, _ = graphs.dijkstra(adj, s, t, settled_order=plain)
        dist_a, _, n_ast, _ = graphs.dijkstra(adj, s, t, lambda v, t=t: FAST * math.dist(pos[v], pos[t]),
                                              settled_order=astar)
        dist_b, n_bi = graphs.bidijkstra(adj, adj, s, t)  # the streets are two-way: the reverse graph is the graph
        assert abs(dist[t] - dist_a[t]) < 1e-9 and abs(dist[t] - dist_b) < 1e-9, "three searches, three distances"
        rows.append((n_dij, n_bi, n_ast, dist[t]))
        if picture is None or n_dij - n_ast > picture[0]:  # draw the query where the bound saves most
            picture = (n_dij - n_ast, s, t, plain, astar)
    counts = np.array([r[:3] for r in rows])
    mean = counts.mean(axis=0)
    lab.row("city", f"{len(adj):,} intersections, {sum(len(a) for a in adj.values()) // 2:,} streets, {QUERIES} queries")
    lab.row("same distance from all three searches", f"{QUERIES} of {QUERIES}")
    lab.row("vertices expanded per query", f"Dijkstra {mean[0]:.0f}   bidirectional {mean[1]:.0f}   A* {mean[2]:.0f}")
    assert np.all(counts[:, 2] <= counts[:, 0]), "A* with a consistent bound never expands more than Dijkstra"
    assert mean[2] < 0.75 * mean[0] and mean[1] < 0.85 * mean[0], "the goal-directed searches should do less work"

    # 2. max flow = min cut, with the cut found by brute force
    flows = []
    for _ in range(NETWORKS):
        cap = network(rng)
        flow, paths, side = graphs.edmonds_karp(cap, 0, len(cap) - 1)
        certificate = sum(c for u in side for v, c in cap[u].items() if v not in side)
        brute = smallest_cut(cap)
        assert flow == certificate == brute, f"flow {flow}, its cut {certificate}, the smallest cut {brute}"
        assert flow == sum(b for _, b in paths)
        flows.append((flow, brute, len(paths)))
    lab.row("max flow = smallest of 1,024 cuts", f"{NETWORKS} of {NETWORKS} networks   "
                                                 f"(values {min(f[0] for f in flows)} to {max(f[0] for f in flows)})")
    lab.row("augmenting paths per network", f"{np.mean([f[2] for f in flows]):.1f} on average")

    # 3. one tree, two algorithms
    index = {v: i for i, v in enumerate(verts)}
    edges = [(w, index[u], index[v]) for u in adj for v, w in adj[u] if index[u] < index[v]]
    by_index = {index[u]: [(index[v], w) for v, w in adj[u]] for u in adj}
    kruskal, tree = graphs.kruskal(len(verts), edges)
    prim, _ = graphs.prim(len(verts), by_index)
    lab.row("minimum spanning tree of the city", f"Kruskal {kruskal:.3f}   Prim {prim:.3f}   ({len(tree):,} edges)")
    assert abs(kruskal - prim) < 1e-6 and len(tree) == len(verts) - 1
    lab.note = ("A lower bound on the remaining distance lets A* ignore most of the city without giving up "
                "exactness, and a flow is proved maximum by exhibiting a cut of the same value: no cut among all "
                "of them is smaller.")

    fig, ax = labs.figure(2, size=(11, 4.6))
    _, s, t, plain, astar = picture
    for u in adj:
        for v, _ in adj[u]:
            if index[u] < index[v]:
                ax[0].plot([pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]], color=labs.GRID, lw=0.6, zorder=1)
    for pts, color, size, label in ((plain, labs.BLUE, 9, f"Dijkstra expands {len(plain)}"),
                                    (astar, labs.GOLD, 5, f"A* expands {len(astar)}")):
        ax[0].scatter([pos[v][0] for v in pts], [pos[v][1] for v in pts], s=size, color=color, label=label, zorder=2)
    ax[0].scatter(*pos[s], s=70, color=labs.INK, edgecolor=labs.BG, zorder=4, label="source")
    ax[0].scatter(*pos[t], s=70, color=labs.RED, edgecolor=labs.BG, zorder=4, label="target")
    ax[0].set(title="One query: the intersections each search expands", xticks=[], yticks=[])
    ax[0].grid(False)
    ax[0].legend(loc="upper center", bbox_to_anchor=(0.5, -0.02), ncols=4, fontsize=8, handletextpad=0.3,
                 columnspacing=1.0)
    top = counts[:, 0].max() * 1.05
    ax[1].plot([0, top], [0, top], color=labs.GREY, ls="--", lw=1, label="as much work as Dijkstra")
    ax[1].scatter(counts[:, 0], counts[:, 1], s=20, color=labs.GREEN, label="bidirectional Dijkstra")
    ax[1].scatter(counts[:, 0], counts[:, 2], s=20, color=labs.GOLD, label="A* (straight-line bound)")
    ax[1].set(title=f"Vertices expanded on {QUERIES} queries", xlabel="Dijkstra", ylabel="the other search",
              xlim=(0, top), ylim=(0, top))
    ax[1].legend(loc="upper left")
    lab.fig = fig
    return lab
