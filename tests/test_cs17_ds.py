"""Part 17's data structures: each one correct against a reference, and the Job v2 exact."""

import math
import random
import unittest

from explainer.cs.algo import ds as D

P = (1 << 61) - 1


class Hashing(unittest.TestCase):
    def test_open_addressing_finds_everything(self):
        rng = random.Random(1)
        for cls in (D.LinearProbing, D.DoubleHashing):
            t = cls(1024, D.Universal(P, 1024, rng), D.Universal(P, 1024, rng))
            keys = rng.sample(range(10 ** 9), 800)
            for k in keys:
                t.insert(k)
            for k in keys:
                self.assertEqual(t.t[list(t.seq(k))[t.find(k) - 1]], k)

    def test_linear_probing_near_knuth(self):
        rng = random.Random(2)
        m, a = 1 << 13, 0.5
        t = D.LinearProbing(m, D.Universal(P, m, rng))
        keys = rng.sample(range(10 ** 12), int(a * m))
        for k in keys:
            t.insert(k)
        hit = sum(t.find(k) for k in keys) / len(keys)
        self.assertAlmostEqual(hit, 0.5 * (1 + 1 / (1 - a)), delta=0.1)

    def test_cuckoo_and_fks(self):
        rng = random.Random(3)
        c = D.Cuckoo(1000, rng)
        keys = rng.sample(range(10 ** 12), 700)
        for k in keys:
            self.assertIsNotNone(c.insert(k))
        self.assertTrue(all(c.find(k) for k in keys))
        self.assertLessEqual(D.fks(keys, rng)["space"], 5 * len(keys))

    def test_birthday(self):
        e, a = D.birthday(23, 365)
        self.assertAlmostEqual(e, 0.5073, places=3)


class Trees(unittest.TestCase):
    def test_balanced_trees_are_bsts_and_short(self):
        rng = random.Random(4)
        n = 3000
        for cls in (D.AVL, D.LLRB, D.Splay, D.BST):
            t = cls()
            ks = list(range(n))
            rng.shuffle(ks)
            for k in ks:
                t.insert(k)
            out = []
            st, node = [], t.root
            while st or node:
                while node:
                    st.append(node)
                    node = node.left
                node = st.pop()
                out.append(node.key)
                node = node.right
            self.assertEqual(out, list(range(n)))
        a = D.AVL()
        for k in range(n):
            a.insert(k)
        self.assertLessEqual(a.height(), 1.4405 * math.log2(n + 2))
        r = D.LLRB()
        for k in range(n):
            r.insert(k)
        self.assertLessEqual(r.height(), 2 * math.log2(n + 1))

    def test_btree_and_skiplist(self):
        rng = random.Random(5)
        ks = rng.sample(range(10 ** 6), 5000)
        b = D.BTree(8)
        for k in ks:
            b.insert(k)
        def keys(x):
            if not x.kids:
                return list(x.keys)
            out = []
            for i, k in enumerate(x.keys):
                out += keys(x.kids[i]) + [k]
            return out + keys(x.kids[-1])
        self.assertEqual(keys(b.root), sorted(ks))
        s = D.SkipList(rng)
        for k in ks:
            s.insert(k)
        x, out = s.head[0], []
        while x is not None:
            out.append(x)
            x = s.nodes[x][0]
        self.assertEqual(out, sorted(ks))

    def test_persistence(self):
        p = D.PersistentBST()
        for k in (5, 3, 8, 1):
            p.insert(k)
        self.assertTrue(D.PersistentBST.contains(p.versions[2], 3))
        self.assertFalse(D.PersistentBST.contains(p.versions[2], 8))
        self.assertTrue(D.PersistentBST.contains(p.versions[4], 1))


class Heaps(unittest.TestCase):
    def test_dijkstra_agrees(self):
        rng = random.Random(6)
        n = 300
        adj = {i: [] for i in range(n)}
        for _ in range(1500):
            a, b, w = rng.randrange(n), rng.randrange(n), rng.randrange(1, 50)
            adj[a].append((b, w))
            adj[b].append((a, w))
        ref = D.dijkstra(adj, 0, D.BinaryHeap)[0]
        for cls in (D.PairingHeap, D.FibHeap):
            self.assertEqual(D.dijkstra(adj, 0, cls)[0], ref)


class UnionFindTest(unittest.TestCase):
    def test_components(self):
        rng = random.Random(7)
        n = 2000
        uf = D.UnionFind(n)
        edges = [(rng.randrange(n), rng.randrange(n)) for _ in range(1500)]
        for a, b in edges:
            uf.union(a, b)
        # reference: BFS components
        adj = {i: [] for i in range(n)}
        for a, b in edges:
            adj[a].append(b)
            adj[b].append(a)
        comp = {}
        for s in range(n):
            if s in comp:
                continue
            st = [s]
            comp[s] = s
            while st:
                u = st.pop()
                for v in adj[u]:
                    if v not in comp:
                        comp[v] = s
                        st.append(v)
        for a in range(0, n, 37):
            for b in range(0, n, 53):
                self.assertEqual(uf.find(a) == uf.find(b), comp[a] == comp[b])


class JobV2(unittest.TestCase):
    def test_job_v2_exact(self):
        from explainer.cs.algo import job2 as J
        from explainer.cs.pebble import programs as PR
        from videos.cs.cs13.compute import _tapes
        c = J.compile_job()
        for t in _tapes(3, 300, 1500, seed=5):
            m = J.run(c, t)
            self.assertEqual(bytes(m.output), PR.job_reference(t))
            f = J.features(t)
            self.assertEqual(f, J.features_native(t)[0])
            self.assertEqual(f["words"], f["found"] + f["new"])


if __name__ == "__main__":
    unittest.main()
