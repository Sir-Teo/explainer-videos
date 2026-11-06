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


if __name__ == "__main__":
    unittest.main()
