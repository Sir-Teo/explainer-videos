import unittest

import numpy as np

from videos.ai.ai12.compute import best_rate_index, mean_seed_loss


class ScalingSweepTests(unittest.TestCase):
    def test_one_successful_seed_cannot_hide_a_diverged_seed(self):
        runs = [[1.0, 2.0, 3.0], [np.nan, 2.2, 2.8]]
        means = mean_seed_loss(runs)
        self.assertTrue(np.isinf(means[0]))
        np.testing.assert_allclose(means[1:], [2.1, 2.9])
        self.assertEqual(best_rate_index(runs), 1)

    def test_entirely_unstable_sweep_has_no_best_rate(self):
        with self.assertRaisesRegex(ValueError, "every seed"):
            best_rate_index([[1.0, np.inf], [np.nan, 2.0]])


if __name__ == "__main__":
    unittest.main()
