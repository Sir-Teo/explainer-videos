"""Part 20's instruments against exact answers and their probability bounds."""

from __future__ import annotations

import math
import unittest
import random

import numpy as np

from explainer.cs.algo import randomized as R


class Randomized(unittest.TestCase):
    def test_freivalds(self):
        rng = np.random.default_rng(1)
        A = rng.integers(-5, 5, (30, 30)); B = rng.integers(-5, 5, (30, 30)); C = A @ B
        assert R.freivalds(A, B, C, 5, rng)
        C2 = C.copy(); C2[3, 4] += 1
        fails = sum(R.freivalds(A, B, C2, 1, rng) for _ in range(400))
        assert fails < 260          # a wrong product passes one round with probability at most 1/2

    def test_det_and_tutte(self):
        assert R.det_mod([[2, 1], [1, 3]], 7) == 5
        rng = random.Random(3)
        cyc6 = [(i, (i + 1) % 6) for i in range(6)]
        star = [(0, i) for i in range(1, 4)]
        assert R.tutte_has_perfect_matching(6, cyc6, rng)
        assert not R.tutte_has_perfect_matching(4, star, rng)
        for _ in range(30):
            n = 8
            es = [(u, v) for u in range(n) for v in range(u + 1, n) if rng.random() < 0.25]
            assert R.tutte_has_perfect_matching(n, es, rng) == R.has_perfect_matching_exact(n, es)

    def test_karger(self):
        rng = random.Random(5)
        # two K5's joined by two edges: min cut 2
        es = [(u, v) for g in (0, 5) for u in range(g, g + 5) for v in range(u + 1, g + 5)] + [(0, 5), (1, 6)]
        cuts = [R.karger(10, es, rng) for _ in range(300)]
        assert min(cuts) == 2 and all(c >= 2 for c in cuts)
        assert R.karger_stein(10, es, rng) >= 2
        merges, groups = R.karger_trace(10, es, rng)
        assert len(merges) == 8 and sum(len(g) for g in groups) == 10

    def test_primes(self):
        cm = R.carmichaels(10000)
        assert cm[:4] == [561, 1105, 1729, 2465]
        assert all(R.fermat_liar(a, 561) for a in range(2, 561) if math.gcd(a, 561) == 1)
        liars = sum(R.mr_liar(a, 561) for a in range(2, 560))
        assert liars <= 560 // 4
        rng = random.Random(1)
        assert R.miller_rabin(2 ** 61 - 1, 20, rng) and not R.miller_rabin(561, 20, rng)
        p = R.random_prime(64, rng)
        assert p.bit_length() == 64 and all(p % q for q in range(3, 1000, 2))

    def test_walks(self):
        rng = random.Random(2)
        cl = R.random_2sat(30, 60, rng)
        assert R.walk_sat(30, cl, rng, 100_000) is not None
        cl3 = R.planted_3sat(20, 80, rng)
        assert R.walk_sat(20, cl3, rng, 200_000, k_restart=60) is not None

    def test_bins_bloom_streams(self):
        rng = np.random.default_rng(0)
        assert R.max_load(10_000, 2, rng) <= 4 < R.max_load(10_000, 1, rng) + 2
        b = R.Bloom(10_000, 7)
        for i in range(1000):
            b.add(b"w%d" % i)
        assert all(b"w%d" % i in b for i in range(1000))
        fp = sum(b"x%d" % i in b for i in range(20_000)) / 20_000
        assert abs(fp - R.bloom_theory(1000, 10_000, 7)) < 0.004
        r = random.Random(4)
        counts = [0] * 10
        for _ in range(4000):
            for x in R.reservoir(range(10), 3, r):
                counts[x] += 1
        assert max(counts) / min(counts) < 1.15
        s = [1] * 50 + [2] * 30 + list(range(100, 120))
        mg = R.misra_gries(s, 4)
        assert 1 in mg and 2 in mg and mg[1] >= 50 - 100 // 4

    def test_distinct_and_f2(self):
        items = [b"%d" % i for i in range(50_000)]
        h = R._h64(items + items[:1000], 7)
        est = R.hyperloglog(h, 12)
        assert abs(est / 50_000 - 1) < 0.05
        assert abs(R.kmv(h, 1024) / 50_000 - 1) < 0.1
        assert abs(R.hyperloglog(R._h64(items[:100], 7), 12) - 100) < 5
        counts = {i: (i % 7) + 1 for i in range(500)}
        f2 = sum(v * v for v in counts.values())
        assert abs(R.ams_f2(None, counts, 64, 5, np.random.default_rng(1)) / f2 - 1) < 0.3

    def test_minhash_and_lsh(self):
        a = {(str(i),) for i in range(200)}
        b = {(str(i),) for i in range(100, 300)}
        j = R.jaccard(a, b)
        sa, sb = R.minhash_sig(a, 300), R.minhash_sig(b, 300)
        assert abs(float(np.mean(sa == sb)) - j) < 0.08
        assert R.lsh_probability(0.8, 5, 20) > 0.99 and R.lsh_probability(0.2, 5, 20) < 0.01

    def test_probabilistic_method(self):
        assert R.ramsey_expected(5, 3) == 10 * 2.0 ** -2
        rng = random.Random(9)
        cl = R.planted_3sat(200, 300, rng)
        steps, x = R.moser_tardos(200, cl, rng)
        assert all(any(x[v] == s for v, s in c) for c in cl)
        es = [(u, v) for u in range(12) for v in range(u + 1, 12) if (u * v) % 3]
        cut, _ = R.maxcut_conditional(12, es)
        assert cut >= len(es) / 2

    def test_randu_planes(self):
        xs = R.randu(1, 3000)
        assert all((9 * xs[i] - 6 * xs[i + 1] + xs[i + 2]) % (1 << 31) == 0 for i in range(len(xs) - 2))


    def test_freivalds_overflow_and_exact_integer_domain(self):
        class Ones:
            def integers(self, low, high, size):
                return np.ones(size, dtype=np.int64)
        a, b = np.array([[2**62]], dtype=np.int64), np.array([[4]], dtype=np.int64)
        self.assertFalse(R.freivalds(a, b, np.array([[0]]), 1, Ones()))
        self.assertTrue(R.freivalds(a, b, np.array([[2**64]], dtype=object), 1, Ones()))
        a = np.array([[1., -2.], [3., 4.]])
        self.assertTrue(R.freivalds(a, a, a @ a, 3, np.random.default_rng(7)))
        with self.assertRaises(ValueError):
            R.freivalds([[0.1]], [[0.2]], [[0.02]])
        with self.assertRaises(ValueError):
            R.freivalds([[1]], [[1]], [[2]], 0)

    def test_freivalds_exact_one_round_probability(self):
        import itertools
        class Bits:
            def __init__(self, bits):
                self.bits = bits
            def integers(self, low, high, size):
                return np.array(self.bits, dtype=np.int64)
        a = np.array([[2, -1], [3, 5]])
        true = a @ a
        for delta in itertools.product(range(-1, 2), repeat=4):
            if not any(delta):
                continue
            wrong = true + np.array(delta).reshape(2, 2)
            passes = sum(R.freivalds(a, a, wrong, 1, Bits(bits))
                         for bits in itertools.product((0, 1), repeat=2))
            self.assertLessEqual(passes, 2)

    def test_determinants_against_leibniz(self):
        import itertools
        rng = random.Random(27)
        for n in range(5):
            for modulus in (7, 2**31 - 1, 2**61 - 1):
                mat = [[rng.randrange(-2**50, 2**50) for _ in range(n)] for _ in range(n)]
                exact = 0
                for perm in itertools.permutations(range(n)):
                    parity = sum(perm[i] > perm[j] for i in range(n) for j in range(i + 1, n))
                    exact += (-1)**parity * math.prod(mat[i][perm[i]] for i in range(n))
                self.assertEqual(R.det_mod(mat, modulus), exact % modulus)
        for modulus in (1, 9, 341, 2**64):
            with self.assertRaises(ValueError):
                R.det_mod([[3, 1], [1, 0]], modulus)
        with self.assertRaises(ValueError):
            R.det_mod([[1, 2]], 7)

    def test_graph_domains_and_disconnected_contraction(self):
        rng = random.Random(5)
        for n, es in ((8, []), (8, [(0, 1), (2, 3)]), (0, []), (1, [])):
            self.assertEqual(R.karger(n, es, rng), 0)
            self.assertEqual(R.karger_stein(n, es, rng), 0)
        self.assertTrue(R.tutte_has_perfect_matching(0, [], rng))
        self.assertFalse(R.tutte_has_perfect_matching(3, [(0, 1)], rng))
        for fn in (R.karger, R.karger_stein, R.tutte_has_perfect_matching):
            with self.assertRaises(ValueError):
                fn(2, [(0, 0)], rng)
        with self.assertRaises(ValueError):
            R.tutte_has_perfect_matching(2, [(0, 1)], rng, p=2)

    def test_fingerprint_preserves_initial_zero_bytes(self):
        self.assertNotEqual(R.fingerprint(b'a', 101), R.fingerprint(b'\x00a', 101))
        self.assertNotEqual(R.fingerprint(b'', 101), R.fingerprint(b'\x00', 101))
        # Collisions still exist modulo a fixed prime; the encoding is not a proof of equality.
        self.assertEqual(R.fingerprint(b'a', 101), R.fingerprint(bytes([198]), 101))

    def test_primality_invalid_rounds_and_small_domains(self):
        for args in ((9, 0), (9, -1)):
            with self.assertRaises(ValueError):
                R.miller_rabin(*args)
        for n in (0, 1, 2, 4):
            with self.assertRaises(ValueError):
                R.mr_liar(1, n)
        with self.assertRaises(ValueError):
            R.random_prime(1, random.Random(1))
        self.assertEqual(R.random_prime(2, random.Random(1)), 3)

    def test_walk_last_flip_and_budgets(self):
        class FalseFirst:
            def random(self): return .9
            def choice(self, xs): return xs[0]
        self.assertEqual(R.walk_sat(1, [((0, True),)], FalseFirst(), 1), 1)
        self.assertIsNone(R.walk_sat(1, [((0, True),)], FalseFirst(), 0))
        self.assertEqual(R.walk_sat(1, [((0, False),)], FalseFirst(), 0), 0)
        for restart in (0, -1):
            with self.assertRaises(ValueError):
                R.walk_sat(1, [((0, True),)], FalseFirst(), 2, k_restart=restart)
        with self.assertRaises(ValueError):
            R.walk_sat(1, [()], FalseFirst(), 2)

    def test_walk_restart_attempts_are_observed(self):
        class Controlled:
            def __init__(self, values): self.values = iter(values)
            def random(self): return next(self.values)
            def choice(self, xs): return xs[0]
        clauses = [((0, True), (1, True))]
        stats = {}
        # The first restart finishes exactly on its final permitted flip.
        self.assertEqual(R.walk_sat(2, clauses, Controlled([.9, .9]), 1,
                                    k_restart=1, statistics=stats), 1)
        self.assertEqual(stats, dict(attempts=1, flips=1, found=True))
        # First attempt flips x0 to false, leaving x1 false; the next starts solved.
        clauses = [((0, False),), ((1, True),)]
        stats = {}
        self.assertEqual(R.walk_sat(2, clauses, Controlled([.1, .9, .9, .1]), 2,
                                    k_restart=1, statistics=stats), 1)
        self.assertEqual(stats, dict(attempts=2, flips=1, found=True))

    def test_packed_bloom_against_bit_reference(self):
        for m in (1, 7, 17, 1025):
            bloom = R.Bloom(m, 11)
            bits = np.zeros(m, dtype=bool)
            for i in range(60):
                word = str(i).encode()
                bits[bloom._idx(word)] = True
                bloom.add(word)
            np.testing.assert_array_equal(bloom.bits, bits)
            self.assertEqual(bloom._packed.nbytes, (m + 7) // 8)
            self.assertTrue(all(str(i).encode() in bloom for i in range(60)))
        for m, k in ((0, 1), (10, 0)):
            with self.assertRaises(ValueError):
                R.Bloom(m, k)

    def test_hll_against_scalar_register_reference(self):
        hashes = R._h64([str(i).encode() for i in range(5000)], 18)
        for b in (4, 6, 12):
            m = 1 << b
            registers = [0] * m
            for h in hashes:
                h = int(h)
                index = h >> (64 - b)
                suffix = h & ((1 << (64 - b)) - 1)
                rank = (64 - b) - suffix.bit_length() + 1
                registers[index] = max(registers[index], rank)
            alpha = {16: .673, 64: .709}.get(m, .7213 / (1 + 1.079 / m))
            expected = alpha * m * m / sum(2.**-r for r in registers)
            zeros = registers.count(0)
            if expected <= 2.5 * m and zeros:
                expected = m * math.log(m / zeros)
            self.assertAlmostEqual(R.hyperloglog(hashes, b), expected, places=9)
        self.assertEqual(R.hyperloglog(np.array([], dtype=np.uint64), 4), 0)
        with self.assertRaises(ValueError):
            R.hyperloglog(hashes, 3)

    def test_kmv_small_and_invalid_samples(self):
        self.assertEqual(R.kmv(np.array([], dtype=np.uint64), 2), 0)
        self.assertEqual(R.kmv(np.array([0, 0], dtype=np.uint64), 2), 1)
        self.assertEqual(R.kmv(np.array([0, 2**63], dtype=np.uint64), 2), 2)
        with self.assertRaises(ValueError):
            R.kmv(np.array([7], dtype=np.uint64), 1)

    def test_empty_minhash_signature(self):
        empty = R.minhash_sig(set(), 25)
        np.testing.assert_array_equal(empty, R.minhash_sig(set(), 25))
        self.assertFalse(np.any(empty == R.minhash_sig({('x',)}, 25)))
        self.assertEqual(R.jaccard(set(), set()), 1)
        with self.assertRaises(ValueError):
            R.minhash_sig(set(), 0)

    def test_misra_gries_all_small_streams(self):
        import itertools
        for stream in itertools.product(range(3), repeat=7):
            counts = __import__('collections').Counter(stream)
            for k in (1, 2, 3, 4):
                sketch = R.misra_gries(stream, k)
                self.assertLessEqual(len(sketch), k - 1)
                for x, freq in counts.items():
                    self.assertTrue(0 <= freq - sketch.get(x, 0) <= len(stream) // k)
                    if freq > len(stream) / k:
                        self.assertIn(x, sketch)
        self.assertEqual(R.reservoir(range(10), 0, random.Random(7)), [])

    def test_moser_initial_assignment_and_exhaustion(self):
        clauses = [((0, True),), ((1, False),)]
        self.assertEqual(R.moser_tardos(2, clauses, random.Random(7), initial=[True, False]), (0, [True, False]))
        steps, x = R.moser_tardos(2, clauses, random.Random(7), initial=[False, True])
        self.assertGreater(steps, 0)
        self.assertEqual(x, [True, False])
        with self.assertRaises(ValueError):
            R.moser_tardos(0, [()], random.Random(7))
        with self.assertRaises(RuntimeError):
            R.moser_tardos(1, [((0, True),), ((0, False),)], random.Random(7), max_resamplings=3)

    def test_conditional_cut_all_small_graphs(self):
        import itertools
        edges = list(itertools.combinations(range(5), 2))
        for bits in range(1 << len(edges)):
            graph = [edge for i, edge in enumerate(edges) if bits >> i & 1]
            cut, side = R.maxcut_conditional(5, graph)
            self.assertEqual(cut, sum(side[u] != side[v] for u, v in graph))
            self.assertGreaterEqual(2 * cut, len(graph))
        with self.assertRaises(ValueError):
            R.maxcut_conditional(1, [(0, 0)])

    def test_generator_and_sketch_domains(self):
        self.assertEqual(R.max_load(0, 1, np.random.default_rng(7)), 0)
        for fn, args in ((R.random_2sat, (1, 1, random.Random(7))),
                         (R.planted_3sat, (2, 1, random.Random(7))),
                         (R.max_load, (3, 0, np.random.default_rng(7))),
                         (R.misra_gries, ([1], 0)),
                         (R.reservoir, ([1], -1, random.Random(7)))):
            with self.assertRaises(ValueError):
                fn(*args)


if __name__ == "__main__":
    unittest.main()
