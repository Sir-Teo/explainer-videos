"""Part 17's data structures: reference checks, measurement regressions, and Job v2 output semantics."""

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
        # An independent Bellman-Ford reference catches bugs shared by custom heaps.
        bellman = {i: float("inf") for i in range(n)}
        bellman[0] = 0
        for _ in range(n - 1):
            changed = False
            for u in adj:
                for v, w in adj[u]:
                    if bellman[u] + w < bellman[v]:
                        bellman[v] = bellman[u] + w
                        changed = True
            if not changed:
                break
        self.assertEqual(ref, {k: v for k, v in bellman.items() if v < float("inf")})
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


class MeasurementRegressions(unittest.TestCase):
    def test_rank_boundaries_and_invalid_positions(self):
        for n in (0, 1, 63, 64, 65, 511, 512, 513, 65536):
            bits = [int((i * 17 + i // 7) % 5 < 2) for i in range(n)]
            rank = D.RankSelect(bits)
            total = 0
            for i, bit in enumerate(bits):
                self.assertEqual(rank.rank(i), total)
                total += bit
            self.assertEqual(rank.rank(n), total)
            for invalid in (-1, n + 1, 0.5, '0'):
                with self.assertRaises(ValueError):
                    rank.rank(invalid)
            if bits:
                bits[0] ^= 1
                self.assertEqual(rank.rank(n), total)
        with self.assertRaises(ValueError):
            D.RankSelect([0, 2])

    def test_robin_hood_controls_home_hash_and_displacement(self):
        rng = random.Random(41)
        for m, n in ((16, 12), (128, 100), (1024, 900)):
            home = D.Universal(P, m, rng)
            keys = rng.sample(range(10**8), n)
            lp, rh = D.LinearProbing(m, home), D.RobinHood(m, home)
            for k in keys:
                lp.insert(k)
                rh.insert(k)
            self.assertEqual([x is not None for x in lp.t], [x is not None for x in rh.t])
            actual = []
            seen = set()
            for i, item in enumerate(rh.t):
                if item is not None:
                    key, recorded = item
                    seen.add(key)
                    displacement = (i - home(key)) % m
                    self.assertEqual(recorded, displacement)
                    actual.append(displacement)
            self.assertEqual(seen, set(keys))
            self.assertEqual(sum(actual), sum(lp.find(k) - 1 for k in keys))

    def test_fibonacci_counts_only_executed_key_comparisons(self):
        heap = D.FibHeap()
        heap.insert('first', 10)
        self.assertEqual(heap.cmp, 0)
        heap.decrease('first', 9)
        self.assertEqual(heap.cmp, 1)  # min comparison, no nonexistent parent comparison
        heap.insert('second', 20)
        self.assertEqual(heap.cmp, 2)

    def test_uniform_permutation_expectation_exhaustive(self):
        import itertools
        from fractions import Fraction
        from videos.cs.cs17.measurements import sample
        for m in range(1, 8):
            for free in range(1, m + 1):
                total = count = 0
                for permutation in itertools.permutations(range(m)):
                    total += next(i + 1 for i, slot in enumerate(permutation) if slot >= m - free)
                    count += 1
                self.assertEqual(Fraction(total, count), Fraction(m + 1, free + 1))
                rng = random.Random(7)
                for _ in range(30):
                    self.assertLessEqual(sample(m, free, rng), m - free + 1)
        for free in (0, 9):
            with self.assertRaises(ValueError):
                sample(8, free, random.Random(1))

    def test_job_explicit_capacities_and_edge_outputs(self):
        from explainer.cs.algo import job2 as J
        import re
        from collections import Counter
        capacities = dict(letter_capacity=4096, distinct_capacity=128, slot_capacity=256)
        c = J.compile_job(**capacities)
        memory = 1 << (len(c.program.image) + (1 << 20) - 1).bit_length()
        for text in (b'', b'The a the B a b', b'a' * 600 + b' ' + b'a' * 600,
                     b' '.join(bytes([97 + i // 26, 97 + i % 26]) for i in range(100))):
            counts = Counter(re.findall(rb'[a-z]+', text.lower()))
            # Counter preserves first occurrence; stable sort handles ties independently.
            expected = b''.join(w + b' ' + str(n).encode() + b'\n'
                                for w, n in sorted(counts.items(), key=lambda item: -item[1])[:20])
            self.assertEqual(bytes(J.run(c, text, mem_size=memory).output), expected)
        for kwargs in (dict(letter_capacity=0), dict(slot_capacity=100),
                       dict(slot_capacity=64, distinct_capacity=100)):
            with self.assertRaises(ValueError):
                J.job_source(**kwargs)

    def test_native_word_counters_full_output_edge_cases(self):
        import re, subprocess, tempfile
        from collections import Counter
        from pathlib import Path
        from videos.cs.cs17.compute import JOB_CPP, JOB_OA_C
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)
            for source, compiler, name in ((JOB_CPP, 'g++', 'cpp'), (JOB_OA_C, 'gcc', 'c')):
                file = path / ('counter.cpp' if compiler == 'g++' else 'counter.c')
                file.write_text(source)
                subprocess.run([compiler, '-O1', '-fsanitize=undefined', '-fno-sanitize-recover=all',
                                str(file), '-o', str(path / name)], check=True, capture_output=True)
                for text in (b'', b'Only', b'B a b A c', b'x' * 600 + b' ' + b'x' * 600,
                             b' '.join(bytes([97 + i // 26, 97 + i % 26]) for i in range(300))):
                    counts = Counter(re.findall(rb'[a-z]+', text.lower()))
                    expected = b''.join(w + b' ' + str(n).encode() + b'\n'
                                        for w, n in sorted(counts.items(), key=lambda item: -item[1])[:20])
                    (path / 'input').write_bytes(text)
                    result = subprocess.run([str(path / name), str(path / 'input')], check=True, capture_output=True)
                    self.assertEqual(result.stderr, expected)
                    self.assertGreater(float(result.stdout), 0)

    def test_native_lookup_zero_aliases_and_duplicate_values(self):
        import json, subprocess, tempfile
        from pathlib import Path
        from videos.cs.cs17.compute import CACHE_CPP
        keys = [0, 1, 12, 13, 12, 0xffffffff, 0, 1]
        queries = [12, 13, 0, 1, 0xffffffff, 12, 1, 0] * 2
        fixture = CACHE_CPP.replace('const long Q=2000000;', 'const long Q=16;')
        old = 'vector<uint32_t>keys(n);for(auto&k:keys)k=(uint32_t)rng();keys[0]=12;keys[1]=13;'
        new = 'vector<uint32_t>keys={' + ','.join(str(x)+'u' for x in keys) + '};'
        self.assertIn(old, fixture)
        fixture = fixture.replace(old, new)
        old = 'vector<uint32_t>q(Q);for(auto&x:q)x=keys[rng()%n];q[0]=12;q[1]=13;'
        new = 'vector<uint32_t>q={' + ','.join(str(x)+'u' for x in queries) + '};'
        self.assertIn(old, fixture)
        fixture = fixture.replace(old, new)
        expected = {key: i for i, key in enumerate(keys)}
        checksum = 14695981039346656037
        for query in queries:
            checksum = ((checksum ^ expected[query]) * 1099511628211) & ((1 << 64) - 1)
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder);(path/'fixture.cpp').write_text(fixture)
            subprocess.run(['g++', '-O1', '-std=c++17', '-fsanitize=undefined', '-fno-sanitize-recover=all',
                            str(path/'fixture.cpp'), '-o', str(path/'lookup')], check=True, capture_output=True)
            result = subprocess.run([str(path/'lookup'), '8'], check=True, capture_output=True, text=True)
            payload = json.loads(result.stdout)
            self.assertEqual(payload['checks'], [1, 1, 1, 1])
            self.assertEqual(payload['checksum'], str(checksum))
            self.assertEqual(payload['unique'], len(expected))


if __name__ == "__main__":
    unittest.main()
