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

    def test_explicit_array_capacities(self):
        tape = b"aa bb aa "
        source = J.job_source(word_capacity=4, letter_capacity=8, distinct_capacity=3)
        self.assertIn("pool: [8]char", source)
        compiled = J.compile_job(word_capacity=4, letter_capacity=8, distinct_capacity=3)
        self.assertEqual(bytes(J.run(compiled, tape).output), PR.job_reference(tape))
        with self.assertRaises(ValueError):
            J.job_source(word_capacity=0)


class TestCountingRepairs(unittest.TestCase):
    def test_small_group_counts_actual_comparisons(self):
        class Key:
            calls = 0

            def __init__(self, value):
                self.value = value

            def __lt__(self, other):
                Key.calls += 1
                return self.value < other.value

        seen = set()
        for permutation in itertools.permutations(range(5)):
            Key.calls = 0
            value, stats = S.median_of_medians([Key(v) for v in permutation], 2)
            self.assertEqual(value.value, 2)
            self.assertEqual(stats["cmp"], Key.calls)
            self.assertEqual(stats["partition_cmp"], 0)
            seen.add(Key.calls)
        self.assertEqual(min(seen), 4)
        self.assertEqual(max(seen), 10)

    def test_median_three_counts_implemented_pivot_rule(self):
        for values, expected in [([0, 1, 2], 2), ([2, 1, 0], 3)]:
            output, stats = S.quicksort(values, "median3")
            self.assertEqual(output, [0, 1, 2])
            self.assertEqual(stats["pivot_cmp"], expected)
            self.assertEqual(stats["partition_cmp"], 2)
            self.assertEqual(stats["cmp"], expected + 2)

    def test_selection_rank_and_duplicates(self):
        for algorithm in [S.quickselect, S.median_of_medians]:
            for values in [[7], [7] * 21, [4, 1, 4, 2, 1, 3, 3]]:
                for rank in range(len(values)):
                    self.assertEqual(algorithm(values, rank)[0], sorted(values)[rank])
            for values, rank in [([], 0), ([1], -1), ([1], 1)]:
                with self.assertRaises(ValueError):
                    algorithm(values, rank)

    def test_uneven_integer_recurrence(self):
        from videos.cs.cs16.measurements import uneven_recurrence

        expected = [0, 1, 2]
        for size in range(3, 201):
            left = size // 3
            expected.append(expected[left] + expected[size - left] + size)
        self.assertEqual([uneven_recurrence(n) for n in range(201)], expected)
        with self.assertRaises(ValueError):
            uneven_recurrence(-1)

    def test_stale_cache_rejected_before_upgrade(self):
        import json
        import tempfile
        from pathlib import Path
        from unittest.mock import Mock, patch
        from tools.qa_series import StaleDataError, require_current_cache
        from videos.cs.cs16 import compute as C

        with tempfile.TemporaryDirectory() as directory:
            cache = C.CountingCache("cs16")
            cache.dir = Path(directory)
            cache.path("master").write_text(json.dumps({"schema": 1, "old": True}))
            producer = Mock(return_value={"schema": C.SCHEMAS["master"], "repaired": True})
            with patch.object(C, "CACHE", cache), patch.dict(C.ITEMS, master=producer):
                with self.assertRaises(StaleDataError):
                    require_current_cache(C, "cs16", cache.path("master"), "master")
                producer.assert_not_called()
                self.assertEqual(json.loads(cache.path("master").read_text())["schema"], 1)
                self.assertTrue(C.load("master")["repaired"])
                producer.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
