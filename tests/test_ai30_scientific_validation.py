"""Small scientific invariants; no shared model or experiment fitting."""

import unittest

import numpy as np

from videos.ai.ai30.items import _spearman, probe_window_starts, copying_benefit_gap


class RankCorrelationTests(unittest.TestCase):
    def test_ties_use_average_ranks(self):
        self.assertAlmostEqual(_spearman([0, 0, 0, 1], [0, 1, 0, 0]), -1 / 3)

    def test_monotone_sequences_have_expected_signs(self):
        self.assertAlmostEqual(_spearman([1, 2, 3], [10, 20, 30]), 1)
        self.assertAlmostEqual(_spearman([1, 2, 3], [30, 20, 10]), -1)

    def test_undefined_or_malformed_observations_fail(self):
        for a, b in (([1, 1], [1, 2]), ([1], [2]), ([1, 2], [1]),
                     ([1, np.nan], [1, 2]), ([[1, 2]], [[1, 2]])):
            with self.subTest(a=a, b=b), self.assertRaises(ValueError):
                _spearman(a, b)


class CopyingNormalizationTests(unittest.TestCase):
    def test_positive_log_probability_benefit(self):
        self.assertAlmostEqual(copying_benefit_gap(-1., -4.), 3.)

    def test_zero_reversed_or_nonfinite_gap_is_not_a_fraction(self):
        for clean, corrupt in ((-2., -2.), (-4., -1.), (np.nan, -1.), (0., -1e-8)):
            with self.subTest(clean=clean, corrupt=corrupt), self.assertRaises(ValueError):
                copying_benefit_gap(clean, corrupt)


class ProbeSplitTests(unittest.TestCase):
    def test_real_recipe_preserves_test_windows_and_removes_span_overlap(self):
        length, n, T, seed = 346584, 160, 128, 1919
        original = np.random.Generator(np.random.PCG64(seed)).integers(0, length - T - 1, n)
        fixed = probe_window_starts(length, n, T, seed)
        split, span = n // 2, T + 1
        np.testing.assert_array_equal(fixed[split:], original[split:])
        self.assertTrue(np.any(fixed[:split] != original[:split]))
        overlap = ((fixed[:split, None] < fixed[None, split:] + span) &
                   (fixed[:split, None] + span > fixed[None, split:]))
        self.assertFalse(overlap.any())
        np.testing.assert_array_equal(fixed, probe_window_starts(length, n, T, seed))

    def test_invalid_stream_or_window_count_fails(self):
        for args in ((100, 1, 10, 0), (10, 2, 10, 0), (100, 2, 0, 0)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                probe_window_starts(*args)


if __name__ == "__main__":
    unittest.main()
