import itertools
import random
import unittest

from explainer.cs.algo import proofs as P


class Proofs(unittest.TestCase):
    def test_fingerprints(self):
        rng = random.Random(1)
        n = 200
        q = P.next_prime(n * n)
        x = [rng.randrange(2) for _ in range(n)]
        self.assertTrue(all(P.fingerprint_eq(x, x, q, rng)[0] for _ in range(50)))
        y = x[:]
        y[17] ^= 1
        wrong = sum(P.fingerprint_eq(x, y, q, rng)[0] for _ in range(2000))
        self.assertLess(wrong / 2000, 3 * n / q)

    def test_restriction_and_depth(self):
        rng = random.Random(2)
        for _ in range(30):
            n = 6
            f = P.dnf_random(n, 4, 3, rng)
            rho = P.random_restriction(n, 0.5, rng)
            g = P.restrict(f, rho)
            free = [v for v in range(n) if v not in rho]
            tab = P.truth_table(g, free)
            for m in range(1 << len(free)):
                x = {v: rho[v] for v in rho}
                x.update({v: bool(m >> i & 1) for i, v in enumerate(free)})
                self.assertEqual(tab[m], P.dnf_eval(f, x))
            self.assertLessEqual(P.dt_depth(tab, len(free)), len(free))
        self.assertEqual(P.dt_depth((False, True, True, False), 2), 2)   # xor
        self.assertEqual(P.dt_depth((False, False, True, True), 2), 1)   # x_1

    def test_sumcheck(self):
        rng = random.Random(3)
        for _ in range(10):
            n = 4
            cl = [rng.sample([1, 2, 3, 4, -1, -2, -3, -4], 3) for _ in range(4)]
            cl = [c for c in cl if len({abs(l) for l in c}) == 3] or [[1, 2, 3]]
            true = P.count_sat(cl, n)
            ok, _, _ = P.sumcheck(cl, n, 101, true, rng)
            self.assertTrue(ok)
        caught = sum(not P.sumcheck([[1, 2, -3], [-1, 3, 4]], 4, 10007, 3, rng, cheat=True)[0] for _ in range(50))
        self.assertGreaterEqual(caught, 49)

    def test_zero_knowledge(self):
        rng = random.Random(4)
        edges = [(0, 1), (1, 2), (2, 0), (2, 3)]
        good = [0, 1, 2, 0]
        caught, rev = P.zk_colouring(4, edges, good, 200, rng)
        self.assertIsNone(caught)
        self.assertTrue(all(a != b for a, b in rev))
        bad = [0, 1, 2, 2]
        caught, _ = P.zk_colouring(4, edges, bad, 500, rng)
        self.assertIsNotNone(caught)

    def test_blr(self):
        n = 4
        lin = [bin(5 & x).count("1") & 1 for x in range(1 << n)]
        self.assertEqual(P.blr_rejection(lin, n), 0.0)
        self.assertEqual(P.distance_to_linear(lin, n), 0.0)
        g = lin[:]
        g[3] ^= 1
        self.assertGreater(P.blr_rejection(g, n), 0)

    def test_vertex_cover(self):
        rng = random.Random(5)
        for _ in range(20):
            n = 9
            edges = [(u, v) for u, v in itertools.combinations(range(n), 2) if rng.random() < 0.3]
            best = next(k for k in range(n + 1) if P.vc_brute(edges, n, k)[0] is not None)
            c, _ = P.vc_branch(edges, best)
            self.assertIsNotNone(c)
            self.assertTrue(all(u in c or v in c for u, v in edges))
            self.assertIsNone(P.vc_branch(edges, best - 1)[0] if best else None)

    def test_permanent_and_det(self):
        rng = random.Random(6)
        for n in range(1, 7):
            A = [[rng.randrange(-2, 3) for _ in range(n)] for _ in range(n)]
            self.assertEqual(P.permanent_ryser(A), P.permanent_brute(A))
        self.assertEqual(P.det_bareiss([[2, 1], [7, 4]]), 1)

    def test_fine_grained(self):
        self.assertTrue(P.ov_brute([0b101, 0b011], [0b010]))
        self.assertFalse(P.ov_brute([0b111], [0b001, 0b010]))
        self.assertEqual(sum(P.three_sum([-5, 1, 4, 10, 2])), 0)
        self.assertIsNone(P.three_sum([1, 2, 3]))


class TestAverage(unittest.TestCase):
    def test_planted_and_rho(self):
        rng = random.Random(1)
        adj, S = P.planted_clique(300, 60, rng)
        self.assertTrue(all((adj[u] >> v) & 1 for u in S for v in S if u != v))
        self.assertEqual(P.degree_recover(adj, 60), S)
        n = P.next_prime(10 ** 6) * P.next_prime(2 * 10 ** 6)
        f, _ = P.pollard_rho(n, random.Random(2))
        self.assertTrue(1 < f < n and n % f == 0)


if __name__ == "__main__":
    unittest.main()


class TestUgOv(unittest.TestCase):
    def test_ug(self):
        rng = random.Random(3)
        edges, planted = P.ug_instance(50, 120, 5, 0.0, rng)
        self.assertEqual(P.ug_value(edges, planted, 5), 1.0)
        self.assertEqual(P.ug_value(edges, P.ug_propagate(50, edges, 5, 0), 5), 1.0)

    def test_sat_to_ov(self):
        for s in range(6):
            rng = random.Random(s)
            cl = [[rng.choice([-1, 1]) * v for v in rng.sample(range(1, 11), 3)] for _ in range(45)]
            A, B = P.sat_to_ov(cl, 10)
            sat = any(all(any(((bits >> (abs(l) - 1)) & 1) == (l > 0) for l in c) for c in cl)
                      for bits in range(1 << 10))
            self.assertEqual(P.ov_brute(A, B), sat)


class TestPit(unittest.TestCase):
    def test_vandermonde(self):
        rng = random.Random(4)
        for _ in range(50):
            xs = [rng.randrange(10007) for _ in range(6)]
            self.assertTrue(P.vandermonde_test(xs, 10007))
        self.assertEqual(P.det_mod([[2, 1], [1, 3]], 7), 5)
        self.assertLess(sum(P.vandermonde_test([rng.randrange(10007) for _ in range(6)], 10007, True)
                            for _ in range(200)), 10)
