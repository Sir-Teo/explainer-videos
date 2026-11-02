"""Single-class probe draws retain the observed data; no model training."""

import unittest

import torch

from videos.ai.ai30.items import single_class_probe_scores


class SingleClassProbeTests(unittest.TestCase):
    def test_constant_training_class_is_scored_without_changing_labels(self):
        tests = [torch.tensor([0., 0., 1.]), torch.tensor([1., 1.])]
        for label, expected in ((0., (2 / 3, 0.)), (1., (1 / 3, 1.))):
            with self.subTest(label=label):
                observed = torch.full((16,), label)
                original = observed.clone()
                actual = single_class_probe_scores(observed, tests)
                self.assertTrue(torch.equal(observed, original))
                for score, target in zip(actual, expected):
                    self.assertAlmostEqual(score, target, places=6)

    def test_two_class_draw_uses_the_normal_probe_path(self):
        self.assertIsNone(single_class_probe_scores(torch.tensor([0., 1.]), []))

    def test_empty_training_draw_fails_explicitly(self):
        with self.assertRaises(ValueError):
            single_class_probe_scores(torch.tensor([]), [])


if __name__ == "__main__":
    unittest.main()
