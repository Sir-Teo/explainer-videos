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


if __name__ == "__main__":
    unittest.main()
