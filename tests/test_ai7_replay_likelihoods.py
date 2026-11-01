"""Tiny exact references for Part7's replayed numerical states; no cache writes."""
import itertools
import math
import unittest

import numpy as np

from videos.ai.ai7 import compute


def enumerated_hmm_logp(obs, A, B, pi):
    probability = 0.0
    for states in itertools.product(range(len(pi)), repeat=len(obs)):
        p = pi[states[0]] * B[states[0], obs[0]]
        for i in range(1, len(obs)):
            p *= A[states[i - 1], states[i]] * B[states[i], obs[i]]
        probability += p
    return math.log(probability)


class HMMReplayLikelihoods(unittest.TestCase):
    def test_scaled_forward_matches_every_hidden_path(self):
        A = np.array([[.7, .3], [.2, .8]])
        B = np.array([[.6, .3, .1], [.1, .3, .6]])
        pi = np.array([.4, .6])
        for obs in [np.array([0]), np.array([0, 2, 1, 0, 2])]:
            self.assertAlmostEqual(compute.hmm_log_likelihood(obs, A, B, pi),
                                   enumerated_hmm_logp(obs, A, B, pi), places=12)
        self.assertEqual(compute.hmm_log_likelihood([], A, B, pi), 0.0)
        self.assertEqual(compute.hmm_log_likelihood([1], A, np.array([[1., 0.], [1., 0.]]), pi),
                         -math.inf)

    def test_scaled_forward_stays_finite_when_path_products_underflow(self):
        obs = np.ones(1000, dtype=int)
        value = compute.hmm_log_likelihood(obs, np.ones((1, 1)),
                                           np.array([[.999, .001]]), np.ones(1))
        self.assertTrue(math.isfinite(value))
        self.assertAlmostEqual(value, len(obs) * math.log(.001), places=8)

    def test_every_replay_round_has_its_actual_model_likelihood(self):
        obs = np.array([0, 1, 2, 1, 0, 2])
        for seed in (7, 13):
            final = compute.baum_welch(obs, K=3, S=2, iters=4, seed=seed)
            self.assertEqual(final[3].shape, (5, 2, 3))
            self.assertEqual(final[4].shape, (5,))
            self.assertTrue(np.all(np.diff(final[4]) >= -1e-12))
            for round_ in range(5):
                A, B, pi, Bs, lls = compute.baum_welch(obs, K=3, S=2, iters=round_, seed=seed)
                np.testing.assert_allclose(Bs[-1], final[3][round_], atol=1e-14)
                expected = enumerated_hmm_logp(obs, A, B, pi) / len(obs)
                self.assertAlmostEqual(lls[-1], expected, places=12)
                self.assertAlmostEqual(final[4][round_], expected, places=12)


class IBMReplayLikelihoods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Only this small, self-contained20-pair producer is run in memory.
        # Its implementation does not load/save a cache or prepare any corpus.
        cls.data = compute.compute_ibm1()
        cls.fi = {w: i + 1 for i, w in enumerate(cls.data['F'])}
        cls.ei = {w: i for i, w in enumerate(cls.data['E'])}

    def test_duplicate_source_positions_keep_all_expected_credit(self):
        initial = self.data['t'][0]
        counts = np.zeros_like(initial)
        duplicates = False
        for source, target in compute.IBM_TRAIN:
            positions = [0] + [self.fi[w] for w in source.split()]
            duplicates |= len(positions) != len(set(positions))
            for word in target.split():
                column = self.ei[word]
                normalizer = sum(initial[row, column] for row in positions)
                # Scalar accumulation is an independent position-wise reference.
                for row in positions:
                    counts[row, column] += initial[row, column] / normalizer
        self.assertTrue(duplicates, 'Actual teaching corpus must exercise repeated words')
        expected = counts / counts.sum(axis=1, keepdims=True)
        np.testing.assert_allclose(self.data['t'][1], expected, atol=1e-14)

    def test_alignment_and_likelihood_share_round_zero_through_final(self):
        self.assertEqual(len(self.data['t']), 31)
        self.assertEqual(len(self.data['align']), 31)
        self.assertEqual(len(self.data['lls']), 31)
        for round_, table in enumerate(self.data['t']):
            expected = 0.0
            for source, target in compute.IBM_TRAIN:
                positions = [0] + [self.fi[w] for w in source.split()]
                for word in target.split():
                    p = sum(table[row, self.ei[word]] for row in positions) / len(positions)
                    expected += math.log(p)
            self.assertAlmostEqual(self.data['lls'][round_], expected, places=11)
        self.assertTrue(np.all(np.diff(self.data['lls']) >= -1e-10))


if __name__ == '__main__':
    unittest.main()
