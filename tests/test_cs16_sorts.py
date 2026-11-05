"""Part 16: the sorts and selection algorithms, the decision-tree bound, and the Job v1 with its instruction model."""
import itertools
import random
import unittest

from explainer.cs.algo import job as J
from explainer.cs.algo import sorts as S
from explainer.cs.pebble import programs as PR


class TestSorts(unittest.TestCase):
    def test_all_sorts_sort(self):
        rng = random.Random(3)
        for n in (0, 1, 2, 3, 7, 50, 257):
            xs = [rng.randrange(40) for _ in range(n)]
            for f in (S.insertion_sort, S.binary_insertion_sort, S.merge_sort, S.heapsort, S.ford_johnson):
                self.assertEqual(f(xs)[0], sorted(xs), f.__name__)
            for rule in ("first", "random", "median3"):
                self.assertEqual(S.quicksort(xs, rule)[0], sorted(xs))
            self.assertEqual(S.radix_sort(xs)[0], sorted(xs))
            self.assertEqual(S.counting_sort(xs, 40)[0], sorted(xs))

    def test_inversions_and_insertion(self):
        for p in itertools.permutations(range(5)):
            inv = sum(1 for i in range(5) for j in range(i + 1, 5) if p[i] > p[j])
            self.assertEqual(S.inversions(p), inv)
            self.assertEqual(S.insertion_sort(p)[1]["moves"], inv)

    def test_lower_bound_and_merge_insertion(self):
        for n in range(1, 8):
            self.assertEqual(S.worst_case(S.ford_johnson, n), S.ford_johnson_formula(n))
            self.assertGreaterEqual(S.ford_johnson_formula(n), S.lower_bound(n))
        self.assertEqual(S.ford_johnson_formula(12), 30)
        self.assertEqual(S.lower_bound(12), 29)

    def test_merge_worst_case(self):
        for n in (2, 4, 8):
            k = n.bit_length() - 1
            self.assertEqual(S.worst_case(S.merge_sort, n), n * k - n + 1)

    def test_selection(self):
        rng = random.Random(5)
        xs = [rng.random() for _ in range(999)]
        s = sorted(xs)
        for k in (0, 1, 499, 998):
            self.assertEqual(S.quickselect(xs, k)[0], s[k])
            self.assertEqual(S.median_of_medians(xs, k)[0], s[k])

    def test_quicksort_mean(self):
        n = 400
        rng = random.Random(9)
        xs = [rng.random() for _ in range(n)]
        mean = sum(S.quicksort(xs, "random", random.Random(r))[1]["cmp"] for r in range(200)) / 200
        self.assertLess(abs(mean - S.quicksort_expected(n)) / S.quicksort_expected(n), 0.02)

    def test_replacement_selection(self):
        rng = random.Random(2)
        runs = S.replacement_selection([rng.random() for _ in range(50000)], 200)
        self.assertLess(abs(sum(runs[1:-1]) / len(runs[1:-1]) - 400) / 400, 0.1)
        self.assertEqual(S.replacement_selection(list(range(5000)), 100), [5000])


class TestJobV1(unittest.TestCase):
    def test_output_and_features(self):
        from videos.cs.cs13.compute import _tapes
        c = J.compile_job()
        for t in _tapes(3, 200, 1500, seed=4):
            m = J.run(c, t)
            self.assertEqual(bytes(m.output), PR.job_reference(t))
            f = J.features(t)
            g, out = J.features_native(t)
            self.assertEqual(f, g)
            self.assertEqual(out, PR.job_reference(t))


if __name__ == "__main__":
    unittest.main()
