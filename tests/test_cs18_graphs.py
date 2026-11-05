"""Part 18's graph algorithms, each checked against a brute-force or independent reference."""

import itertools
import math
import random
import unittest

from explainer.cs.algo import graphs as G


def random_digraph(n, m, rng, w=(1, 20)):
    adj = {i: [] for i in range(n)}
    for _ in range(m):
        a, b = rng.randrange(n), rng.randrange(n)
        if a != b:
            adj[a].append((b, rng.randint(*w)))
    return adj


class Traversal(unittest.TestCase):
    def test_euler(self):
        k = {"A": ["B", "B", "C", "C", "D"], "B": ["A", "A", "D"], "C": ["A", "A", "D"], "D": ["A", "B", "C"]}
        self.assertIsNone(G.euler_circuit(k))
        g = {0: [1, 2, 3, 4], 1: [0, 2], 2: [0, 1], 3: [0, 4], 4: [0, 3]}
        c = G.euler_circuit(g)
        self.assertEqual(len(c), 7)
        used = sorted(tuple(sorted(e)) for e in zip(c, c[1:]))
        want = sorted(tuple(sorted((u, v))) for u in g for v in g[u] if u < v)
        self.assertEqual(used, want)

    def test_topo_and_scc(self):
        rng = random.Random(1)
        for _ in range(20):
            n = 12
            order = list(range(n))
            rng.shuffle(order)
            pos = {v: i for i, v in enumerate(order)}
            adj = {v: [u for u in range(n) if pos[u] > pos[v] and rng.random() < 0.3] for v in range(n)}
            for topo in (G.topo_kahn(adj), G.topo_dfs(adj)):
                p = {v: i for i, v in enumerate(topo)}
                self.assertTrue(all(p[u] < p[v] for u in adj for v in adj[u]))
            g = {v: [u for u, _ in random_digraph(n, 25, rng)[v]] for v in range(n)}
            reach = {v: set() for v in g}
            for s in g:
                st = [s]
                while st:
                    u = st.pop()
                    for x in g[u]:
                        if x not in reach[s]:
                            reach[s].add(x)
                            st.append(x)
            for comps in (G.tarjan_scc(g), G.kosaraju(g)):
                for c in comps:
                    for a in c:
                        for b in c:
                            self.assertTrue(a == b or (b in reach[a] and a in reach[b]))
                self.assertEqual(sorted(x for c in comps for x in c), sorted(g))

    def test_two_sat(self):
        rng = random.Random(2)
        for _ in range(50):
            n = 5
            cl = [(rng.choice([1, -1]) * rng.randint(1, n), rng.choice([1, -1]) * rng.randint(1, n)) for _ in range(9)]
            sat = any(all((a > 0) == bits[abs(a) - 1] or (b > 0) == bits[abs(b) - 1] for a, b in cl)
                      for bits in itertools.product([False, True], repeat=n))
            r = G.two_sat(n, cl)
            self.assertEqual(r is not None, sat)
            if r:
                self.assertTrue(all(r[abs(a)] == (a > 0) or r[abs(b)] == (b > 0) for a, b in cl))


class Paths(unittest.TestCase):
    def test_dijkstra_family(self):
        rng = random.Random(3)
        adj, pos = G.grid_city(15, 15, rng)
        ch = G.CH(adj)
        for _ in range(10):
            s = (rng.randrange(15), rng.randrange(15))
            t = (rng.randrange(15), rng.randrange(15))
            d = G.dijkstra(adj, s)[0][t]
            self.assertAlmostEqual(G.dijkstra(adj, s, t, h=lambda v: 0.35 * math.dist(pos[v], pos[t]))[0][t], d)
            self.assertAlmostEqual(G.bidijkstra(adj, adj, s, t)[0], d)
            self.assertAlmostEqual(ch.query(s, t)[0], d)

    def test_negative_and_all_pairs(self):
        rng = random.Random(4)
        n = 9
        adj = random_digraph(n, 30, rng, w=(-3, 12))
        edges = [(u, v, w) for u in adj for v, w in adj[u]]
        fw = G.floyd_warshall(n, edges)
        neg = any(fw[i][i] < 0 for i in range(n))
        dist, cyc = G.bellman_ford(adj, 0)
        if cyc is None:
            for v in range(n):
                self.assertAlmostEqual(dist[v], fw[0][v]) if fw[0][v] < math.inf else None
        else:
            total = sum(next(w for x, w in adj[a] if x == b) for a, b in zip(cyc, cyc[1:] + cyc[:1]))
            self.assertLess(total, 0)
        if not neg:
            J, minw = G.johnson(adj)
            self.assertGreaterEqual(minw, 0)
            for u in range(n):
                for v, dv in J[u].items():
                    self.assertAlmostEqual(dv, fw[u][v])


class Trees(unittest.TestCase):
    def test_mst(self):
        rng = random.Random(5)
        n = 8
        edges = list({(rng.randint(1, 30), *sorted(rng.sample(range(n), 2))) for _ in range(20)})
        adj = {i: [] for i in range(n)}
        for w, u, v in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))
        from explainer.cs.algo.ds import UnionFind
        best = math.inf
        for sub in itertools.combinations(edges, n - 1):
            uf = UnionFind(n)
            if all(uf.union(u, v) for _, u, v in sub):
                best = min(best, sum(w for w, _, _ in sub))
        if best < math.inf:
            self.assertEqual(G.kruskal(n, edges)[0], best)
            self.assertEqual(G.prim(n, adj)[0], best)
            self.assertEqual(G.boruvka(n, edges)[0], best)


class Flows(unittest.TestCase):
    def test_flow_equals_cut(self):
        rng = random.Random(6)
        nodes = list(range(7))
        cap = {u: {} for u in nodes}
        for _ in range(16):
            a, b = rng.sample(nodes, 2)
            cap[a][b] = rng.randint(1, 9)
        f, paths, side = G.edmonds_karp(cap, 0, 6)
        cut = sum(c for u in side for v, c in cap[u].items() if v not in side)
        self.assertEqual(f, cut)
        best = min(sum(c for u in S for v, c in cap[u].items() if v not in S)
                   for k in range(0, 6) for rest in itertools.combinations(range(1, 6), k) for S in [{0, *rest}])
        self.assertEqual(f, best)

    def test_matching(self):
        rng = random.Random(7)
        n = 6
        cost = [[rng.randint(0, 20) for _ in range(n)] for _ in range(n)]
        brute = min(sum(cost[i][p[i]] for i in range(n)) for p in itertools.permutations(range(n)))
        self.assertEqual(G.hungarian(cost)[0], brute)
        P = [rng.sample(range(n), n) for _ in range(n)]
        R = [rng.sample(range(n), n) for _ in range(n)]
        m, _ = G.gale_shapley(P, R)
        self.assertTrue(G.is_stable(m, P, R))

    def test_held_karp_and_pagerank(self):
        rng = random.Random(8)
        pts = [(rng.random(), rng.random()) for _ in range(7)]
        D = [[math.dist(a, b) for b in pts] for a in pts]
        brute = min(sum(D[p[i]][p[(i + 1) % 7]] for i in range(7)) for p in [(0,) + q for q in
                                                                             itertools.permutations(range(1, 7))])
        self.assertAlmostEqual(G.held_karp(D), brute)
        r, _ = G.pagerank(G.random_web(300, 2, rng))
        self.assertAlmostEqual(sum(r.values()), 1.0)


if __name__ == "__main__":
    unittest.main()
