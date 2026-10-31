import math
import unittest

from videos.ai.ai8.compute import compression_bound, vc_bound


class LearningBoundTests(unittest.TestCase):
    def test_compression_confidence_covers_selecting_the_size_from_data(self):
        for samples in (10, 100):
            delta = 0.05
            failure_budget = 0.0
            for retained in range(samples):
                epsilon = compression_bound(retained, samples, delta)
                if epsilon < 1:
                    failure_budget += math.exp(retained * math.log(samples) - (samples - retained) * epsilon)
            self.assertLessEqual(failure_budget, delta)
            self.assertEqual(compression_bound(samples, samples, delta), 1)

    def test_vc_gap_inverts_the_probability_bound_shown_in_the_proof(self):
        for dimension, samples, confidence in ((3, 448, 0.05), (71, 448, 0.05), (71, 50000, 0.01)):
            epsilon = vc_bound(dimension, samples, confidence)
            # Evaluate the preceding probability bound in log space. Dropping
            # sqrt(8) in the final gap would fail to achieve the claimed delta.
            log_probability = (math.log(4) + dimension * math.log(2 * math.e * samples / dimension)
                               - samples * epsilon**2 / 8)
            self.assertAlmostEqual(log_probability, math.log(confidence))


if __name__ == "__main__":
    unittest.main()
