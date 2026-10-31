"""MI measurements must follow the sampled joint distribution, not a hoped-for tail."""

import math
import unittest
from unittest.mock import patch

import numpy as np

from videos.ai.ai1 import compute


class MutualInformationTests(unittest.TestCase):
    def measure(self, text):
        with patch.object(compute, 'text', return_value=text):
            return compute.compute_mi()

    def test_exact_pair_marginals_and_active_alphabet_correction(self):
        result = self.measure(' abaa')
        # At lag 1, P(Y=a)=3/4, P(Y=b)=1/4; only X=a is uncertain,
        # with probability 1/2 and one conditional bit. H(Y)-H(Y|X).
        entropy_y = -.75 * math.log2(.75) - .25 * math.log2(.25)
        expected_plugin = entropy_y - .5
        expected_bias = (3 - 1) * (2 - 1) / (2 * 4 * math.log(2))
        self.assertAlmostEqual(result['mi_plugin'][0], expected_plugin)
        self.assertAlmostEqual(result['bias'][0], expected_bias)
        self.assertAlmostEqual(result['mi'][0], expected_plugin - expected_bias)
        self.assertLess(result['mi'][0], 0)  # retained, not clamped or rejected
        self.assertEqual(result['pair_counts'][0], 4)

    def test_constant_data_has_no_positive_log_fit_and_does_not_abort(self):
        result = self.measure('a' * 1200)
        np.testing.assert_array_equal(result['mi'], 0)
        np.testing.assert_array_equal(result['shuffled_mi'], 0)
        self.assertIsNone(result['slope'])
        self.assertIsNone(result['intercept'])
        self.assertEqual(len(result['fit_d']), 0)

    def test_shuffled_reference_is_reproducible_and_fit_uses_only_positive_estimates(self):
        random = np.random.default_rng(11)
        text = ''.join(random.choice(list(' abc'), size=4000))
        first, second = self.measure(text), self.measure(text)
        np.testing.assert_array_equal(first['shuffled_mi'], second['shuffled_mi'])
        self.assertEqual(first['shuffle_replicates'], 1)
        np.testing.assert_array_equal(first['fit_d'], first['d'][(first['d'] >= 20) & (first['mi'] > 0)])
        self.assertTrue(np.isfinite(first['mi']).all())
        self.assertTrue(np.isfinite(first['shuffled_mi']).all())
        if len(first['fit_d']) >= 2:
            self.assertTrue(math.isfinite(first['slope']))

    def test_too_short_input_is_rejected_as_an_input_invariant(self):
        for text in ('', 'a'):
            with self.subTest(text=text), self.assertRaisesRegex(ValueError, 'at least two'):
                self.measure(text)


if __name__ == '__main__':
    unittest.main()
