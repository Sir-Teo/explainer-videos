import random
import unittest

from explainer.cs.algo import practice as P


class Ranges(unittest.TestCase):
    def test_prefix_and_diff(self):
        rng = random.Random(0)
        a = [rng.randint(-9, 9) for _ in range(50)]
        S = P.prefix_sums(a)
        for _ in range(100):
            l = rng.randrange(50)
            r = rng.randrange(l, 50)
            self.assertEqual(P.range_sum(S, l, r), sum(a[l:r + 1]))
        ups = [(rng.randrange(10), rng.randrange(10, 20), rng.randint(1, 5)) for _ in range(30)]
        ref = [0] * 20
        for l, r, v in ups:
            for i in range(l, r + 1):
                ref[i] += v
        self.assertEqual(P.diff_apply(20, ups), ref)
        img = [[rng.randint(0, 9) for _ in range(7)] for _ in range(5)]
        I = P.integral_image(img)
        self.assertEqual(P.box_sum(I, 1, 2, 3, 5), sum(img[r][c] for r in range(1, 4) for c in range(2, 6)))

    def test_fenwick(self):
        rng = random.Random(1)
        n = 100
        F = P.Fenwick(n)
        a = [0] * (n + 1)
        for _ in range(500):
            i = rng.randint(1, n)
            v = rng.randint(-5, 5)
            F.add(i, v)
            a[i] += v
            j = rng.randint(1, n)
            self.assertEqual(F.prefix(j), sum(a[1:j + 1]))
            self.assertLessEqual(len(F.last_path), n.bit_length())
        self.assertEqual(P.Fenwick.responsibility(12), (9, 12))

    def test_segment_trees(self):
        rng = random.Random(2)
        a = [rng.randint(0, 99) for _ in range(64)]
        T = P.SegTree(a, min, 10 ** 9)
        L = P.LazySegTree(a)
        b = list(a)
        for _ in range(300):
            l = rng.randrange(64)
            r = rng.randrange(l, 64)
            cov = []
            self.assertEqual(T.query(l, r, cov), min(a[l:r + 1]))
            self.assertLessEqual(len(cov), 2 * 6)
            v = rng.randint(-3, 3)
            L.range_add(l, r, v)
            for i in range(l, r + 1):
                b[i] += v
            l2 = rng.randrange(64)
            r2 = rng.randrange(l2, 64)
            self.assertEqual(L.range_sum(l2, r2), sum(b[l2:r2 + 1]))

    def test_rmq_lca(self):
        rng = random.Random(3)
        a = [rng.randint(0, 999) for _ in range(200)]
        st = P.SparseTable(a)
        for _ in range(300):
            l = rng.randrange(200)
            r = rng.randrange(l, 200)
            self.assertEqual(st.query(l, r), min(a[l:r + 1]))
        n = 80
        parent = [-1] + [rng.randrange(v) for v in range(1, n)]
        kids = {}
        for v in range(1, n):
            kids.setdefault(parent[v], []).append(v)
        E = P.EulerLCA(kids, 0)
        B = P.BinaryLift([0] + parent[1:], 0)

        def anc(v):
            out = []
            while v != -1:
                out.append(v)
                v = parent[v]
            return out
        for _ in range(200):
            u, v = rng.randrange(n), rng.randrange(n)
            au = anc(u)
            ref = next(x for x in anc(v) if x in au)
            self.assertEqual(E.lca(u, v), ref)
            self.assertEqual(B.lca(u, v), ref)
        par = P.cartesian_tree(a[:30])
        self.assertEqual(sum(1 for p in par if p == -1), 1)


class Monotone(unittest.TestCase):
    def test_windows_and_stacks(self):
        rng = random.Random(4)
        for _ in range(50):
            a = [rng.randint(0, 20) for _ in range(rng.randint(1, 40))]
            k = rng.randint(1, len(a))
            self.assertEqual(P.sliding_max(a, k), [max(a[i:i + k]) for i in range(len(a) - k + 1)])
            ng = P.next_greater(a)
            for i, j in enumerate(ng):
                ref = next((t for t in range(i + 1, len(a)) if a[t] > a[i]), -1)
                self.assertEqual(j, ref)
            self.assertEqual(P.largest_rectangle(a)[0], P.largest_rectangle_brute(a))

    def test_search(self):
        w = [3, 2, 2, 4, 1, 4]
        cap, _ = P.ship_within_days(w, 3)
        self.assertEqual(cap, 6)
        a = list(range(0, 2000, 2))
        for x in (0, 1, 2, 999, 1998, 5000):
            j, _ = P.galloping(a, x)
            import bisect
            self.assertEqual(j, bisect.bisect_left(a, x))
        self.assertAlmostEqual(P.ternary_max(lambda t: -(t - 1.3) ** 2, -5, 5), 1.3, places=6)


class Bits(unittest.TestCase):
    def test_bits(self):
        for x in range(1000):
            self.assertEqual(P.popcount(x), bin(x).count("1"))
            self.assertEqual(P.popcount(P.gray(x) ^ P.gray(x + 1)), 1)
        m = 0b101101
        subs = list(P.submasks(m))
        self.assertEqual(len(subs), 2 ** 4)
        self.assertTrue(all(s & ~m == 0 for s in subs))
        self.assertEqual(sum(1 for mm in range(1 << 6) for _ in P.submasks(mm)), 3 ** 6)

    def test_closure_and_lcs(self):
        rng = random.Random(5)
        n = 30
        adj = [[1 if rng.random() < 0.06 else 0 for _ in range(n)] for _ in range(n)]
        Rb = P.transitive_closure_bits(adj)
        Rp = P.transitive_closure_plain(adj)
        for i in range(n):
            self.assertEqual([bool(Rb[i] >> j & 1) for j in range(n)], Rp[i])
        for _ in range(100):
            a = "".join(rng.choice("ab") for _ in range(rng.randint(0, 25)))
            b = "".join(rng.choice("ab") for _ in range(rng.randint(1, 25)))
            self.assertEqual(P.lcs_bitparallel(a, b), P.lcs_dp(a, b))


class Splits(unittest.TestCase):
    def test_mitm_sqrt_mo(self):
        rng = random.Random(6)
        for _ in range(30):
            a = [rng.randint(1, 100) for _ in range(12)]
            t = rng.randint(1, 600)
            self.assertEqual(P.subset_sum_mitm(a, t)[0], P.subset_sum_brute(a, t)[0])
        a = [rng.randint(0, 9) for _ in range(100)]
        S = P.SqrtDecomp(a)
        for _ in range(100):
            i = rng.randrange(100)
            v = rng.randint(0, 9)
            S.update(i, v)
            a[i] = v
            l = rng.randrange(100)
            r = rng.randrange(l, 100)
            self.assertEqual(S.query(l, r), sum(a[l:r + 1]))
        qs = [(l, rng.randrange(l, 100)) for l in (rng.randrange(100) for _ in range(60))]
        ans, _ = P.mo_distinct(a, qs)
        self.assertEqual(ans, [len(set(a[l:r + 1])) for l, r in qs])



class Boundaries(unittest.TestCase):
    def test_integer_domains(self):
        for constructor in (P.Fenwick,):
            with self.assertRaises(ValueError): constructor(-1)
            for value in (True, 2.5):
                with self.assertRaises(TypeError): constructor(value)
        with self.assertRaises(ValueError): P.diff_apply(-1, [])
        with self.assertRaises(TypeError): P.diff_apply(True, [])

    def test_empty_structures(self):
        for tree, query in ((P.SegTree([]), 'query'), (P.LazySegTree([]), 'range_sum'),
                            (P.SparseTable([]), 'query'), (P.SqrtDecomp([]), 'query')):
            with self.assertRaises(IndexError): getattr(tree, query)(0, 0)
        self.assertEqual(P.prefix_sums([]), [0])
        self.assertEqual(P.diff_apply(0, []), [])
        self.assertEqual(P.mo_distinct([], []), ([], 0))

    def test_closed_ranges_and_atomic_updates(self):
        for tree in (P.SegTree([2, 4]), P.SqrtDecomp([2, 4])):
            for l, r in ((-1, 1), (0, 2), (1, 0)):
                with self.assertRaises((IndexError, ValueError)): tree.query(l, r)
            for i in (-1, 2):
                with self.assertRaises(IndexError): tree.update(i, 99)
            self.assertEqual(tree.query(0, 1), 6)
        lazy = P.LazySegTree([2, 4])
        with self.assertRaises(IndexError): lazy.range_add(-1, 1, 99)
        self.assertEqual(lazy.range_sum(0, 1), 6)
        with self.assertRaises(IndexError): P.range_sum([0, 2, 6], -1, 1)
        with self.assertRaises(ValueError): P.diff_apply(2, [(1, 0, 9)])

    def test_fenwick_invalid_indices(self):
        f = P.Fenwick(4)
        for i in (-2, 0, 5):
            with self.assertRaises(IndexError): f.add(i, 7)
        for i in (-1, 5):
            with self.assertRaises(IndexError): f.prefix(i)
        with self.assertRaises(TypeError): f.add(True, 7)
        with self.assertRaises(IndexError): P.Fenwick.responsibility(0)
        self.assertEqual(f.prefix(4), 0)
        self.assertEqual(P.Fenwick(0).prefix(0), 0)

    def test_empty_and_ragged_images(self):
        self.assertEqual(P.integral_image([]), [[0]])
        self.assertEqual(P.integral_image([[], []]), [[0], [0], [0]])
        with self.assertRaises(ValueError): P.integral_image([[1, 2], [3]])
        self.assertEqual(P.integral_image(iter([iter([1, 2]), iter([3, 4])])), [[0, 0, 0], [0, 1, 3], [0, 4, 10]])

    def test_box_and_sparse_bounds(self):
        image = P.integral_image([[1, 2], [3, 4]])
        for box in ((-1, 0, 1, 1), (0, 0, 2, 1), (1, 0, 0, 1)):
            with self.assertRaises((IndexError, ValueError)): P.box_sum(image, *box)
        st = P.SparseTable([4, 2, 2, 5])
        self.assertEqual(st.argmin(0, 3), 1)
        with self.assertRaises(IndexError): st.query(-1, 3)
        with self.assertRaises(ValueError): st.query(3, 0)

    def test_invalid_rooted_trees(self):
        for tree in ({0: [1], 1: [0]}, {0: [1, 1]}, {0: [1, 2], 1: [2]}, {0: [], 1: []}):
            with self.assertRaises(ValueError): P.euler_tour(tree, 0)
        for parent, root in (([], 0), ([0, 4], 0), ([0, -1], 0), ([0, 2, 1], 0), ([1, 0], 0)):
            with self.assertRaises((ValueError, IndexError)): P.BinaryLift(parent, root)
        b = P.BinaryLift([-1, 0, 0], 0)
        with self.assertRaises(IndexError): b.lca(-1, 2)

    def test_cartesian_ties_and_lca(self):
        import itertools
        for n in range(1, 6):
            for values in itertools.product(range(2), repeat=n):
                parent = P.cartesian_tree(values)
                root = parent.index(-1)
                lift = P.BinaryLift(parent, root)
                for l in range(n):
                    for r in range(l, n):
                        expected = min(range(l, r + 1), key=lambda i: (values[i], i))
                        self.assertEqual(lift.lca(l, r), expected)
        self.assertEqual(P.euler_tour({0: iter([1]), 1: []}, 0)[0], [0, 1, 0])

    def test_window_domain(self):
        for k in (0, -1):
            with self.assertRaises(ValueError): P.sliding_max([3, 1], k)
        with self.assertRaises(TypeError): P.sliding_max([3, 1], True)
        self.assertEqual(P.sliding_max([], 2), [])
        self.assertEqual(P.sliding_max([3], 2), [])
        self.assertEqual(P.sliding_max([3, 3, 2], 2), [3, 3])

    def test_histogram_domain(self):
        for value in (-1, float('nan'), float('inf')):
            with self.assertRaises(ValueError): P.largest_rectangle([1, value, 2])
        self.assertEqual(P.largest_rectangle([]), (0, 0, -1, 0))
        self.assertEqual(P.largest_rectangle([10**400])[0], 10**400)

    def test_feasible_binary_answer_and_calls(self):
        seen = []
        answer, calls = P.binary_search_answer(-5, 12, lambda x: seen.append(x) or x >= 3)
        self.assertEqual(answer, 3)
        self.assertEqual(calls, len(seen))
        self.assertEqual(seen[0], 12)
        with self.assertRaises(ValueError): P.binary_search_answer(0, 4, lambda x: False)
        with self.assertRaises(ValueError): P.binary_search_answer(4, 0, lambda x: True)
        self.assertEqual(P.binary_search_answer(2, 2, lambda x: True), (2, 1))

    def test_galloping_actual_comparisons(self):
        import bisect
        class Reads(list):
            def __getitem__(self, i):
                self.reads += 1
                return super().__getitem__(i)
        for n in range(33):
            values = [i // 3 for i in range(n)]
            for start in range(n + 1):
                for x in (-1, 0, 3, 8, 20):
                    array = Reads(values)
                    array.reads = 0
                    found, probes = P.galloping(array, x, start)
                    self.assertEqual(found, bisect.bisect_left(values, x, start))
                    self.assertEqual(probes, array.reads)
        for start in (-1, 2):
            with self.assertRaises(IndexError): P.galloping([1], 2, start)

    def test_shipping_domain(self):
        self.assertEqual(P.ship_within_days([], 3), (0, 0))
        self.assertEqual(P.ship_within_days(iter([3, 2, 2, 4, 1, 4]), 3)[0], 6)
        self.assertEqual(P.ship_within_days([0, 0], 2)[0], 0)
        for weights, days in (([1], 0), ([-1, 2], 1)):
            with self.assertRaises(ValueError): P.ship_within_days(weights, days)

    def test_bit_domains(self):
        for function in (P.lowbit, P.popcount, P.gray):
            with self.assertRaises(ValueError): function(-1)
            with self.assertRaises(TypeError): function(True)
        with self.assertRaises(ValueError): list(P.submasks(-1))
        self.assertEqual(list(P.submasks(0)), [0])
        self.assertEqual(P.lowbit(0), 0)
        self.assertEqual(P.popcount(1 << 1000), 1)

    def test_reflexive_closure_against_bfs(self):
        rng = random.Random(71)
        for n in range(20):
            graph = [[rng.random() < .12 for _ in range(n)] for _ in range(n)]
            got = P.transitive_closure_bits(graph)
            for start in range(n):
                seen, todo = {start}, [start]
                for u in todo:
                    for v in range(n):
                        if graph[u][v] and v not in seen: seen.add(v); todo.append(v)
                self.assertEqual(got[start], sum(1 << v for v in seen))
        for f in (P.transitive_closure_bits, P.transitive_closure_plain):
            with self.assertRaises(ValueError): f([[1, 0]])

    def test_mo_invalid_ranges(self):
        for queries in ([(-1, 0)], [(0, 3)], [(2, 1)]):
            with self.assertRaises((ValueError, IndexError)): P.mo_distinct([1, 2, 1], queries)
        values = [1, 1, 2, 3, 1, 4]
        queries = [(l, r) for l in range(len(values)) for r in range(l, len(values))]
        self.assertEqual(P.mo_distinct(values, iter(queries))[0], [len(set(values[l:r+1])) for l, r in queries])

    def test_sqrt_generator(self):
        tree = P.SqrtDecomp(iter([1, 2, 3, 4]))
        self.assertEqual(tree.query(0, 3), 10)
        tree.update(2, -7)
        self.assertEqual(tree.query(1, 3), -1)

    def test_ternary_finite_domain(self):
        for lo, hi in ((2, 1), (float('nan'), 1), (0, float('inf'))):
            with self.assertRaises(ValueError): P.ternary_max(lambda x: -x*x, lo, hi)
        with self.assertRaises(ValueError): P.ternary_max(lambda x: float('nan'), 0, 1)
        with self.assertRaises(ValueError): P.ternary_max(lambda x: x, 0, 1, -1)
        self.assertEqual(P.ternary_max(lambda x: -abs(x), -1e308, 1e308, 0), 0)


if __name__ == "__main__":
    unittest.main()


class PredictionBounds(unittest.TestCase):
    def test_discrete_worst_case_and_consistency(self):
        from videos.cs.cs24 import measurement_references as R
        for B in range(1,21):
            for lam in ('0.1','0.3','0.6','1'):
                _,_,early,late,consistency,worst=R.ski_parameters(B,lam)
                # Enumerate both forecast branches past both buy thresholds.
                actual=max(R.ski_ratio(B,d,y,lam) for d in range(1,late+3) for y in (0,B))
                self.assertEqual(actual,float(worst))
                perfect=max(R.ski_ratio(B,d,d,lam) for d in range(1,late+3))
                self.assertEqual(perfect,float(consistency))
        self.assertEqual(R.ski_ratio(10,100,0,'0.1'),10.9)

    def test_prediction_domain(self):
        from videos.cs.cs24 import measurement_references as R
        for args in [(0,1,1,.5),(10,0,1,.5),(10,1,1,0),(10,1,1,1.1),(10,1,float('nan'),.5),(10,1,1,float('inf'))]:
            with self.assertRaises(ValueError):R.ski_ratio(*args)
        for args in [(True,1,1,.5),(10,True,1,.5),(10,1,1,True)]:
            with self.assertRaises(TypeError):R.ski_ratio(*args)
