import unittest

import numpy as np

from videos.ai.ai6.compute import fisher_score


class FisherScoreTests(unittest.TestCase):
    def test_unequal_class_sizes_match_the_pooled_scatter_direction(self):
        rng = np.random.default_rng(19)
        a = rng.normal(size=(8, 2)) * [5, 0.5]
        d = rng.normal(size=(90, 2)) * [0.5, 3] + [2, 2]
        scatter = (a - a.mean(0)).T @ (a - a.mean(0)) + (d - d.mean(0)).T @ (d - d.mean(0))
        w = np.linalg.solve(scatter, d.mean(0) - a.mean(0))
        w /= np.linalg.norm(w)
        angles = np.linspace(0, np.pi, 2001)
        directions = np.stack([np.cos(angles), np.sin(angles)], axis=1)
        sampled = max(fisher_score(a, d, u) for u in directions)
        optimum = fisher_score(a, d, w)
        self.assertGreaterEqual(optimum + 1e-12, sampled)
        self.assertAlmostEqual(optimum, sampled, places=5)
        # Scaling a direction must not alter its score.
        self.assertAlmostEqual(optimum, fisher_score(a, d, 17 * w))


if __name__ == "__main__":
    unittest.main()
