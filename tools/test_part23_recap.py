"""Focused no-training regressions for recap units, missing values and providers."""
from pathlib import Path
import ast
import sys
import unittest

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from videos.ai.ai23.recap import bpe_trace, entropy_threshold, entropy_window, modality_products


class RecapContracts(unittest.TestCase):
    def test_bpe_sampling_is_merge_count_not_array_index(self):
        x, y = bpe_trace(dict(n_merges=100, saved=[1] * 100, sample_chars=1000, length=[1000, 950, 900]))
        np.testing.assert_array_equal(x, [0, 50, 100])
        np.testing.assert_array_equal(y, [1000, 950, 900])

    def test_bpe_inconsistent_or_missing_samples_are_refused(self):
        for length in ([1000, 951, 900], [1000, 950], [1000, float("nan"), 900]):
            with self.assertRaises(ValueError):
                bpe_trace(dict(n_merges=100, saved=[1] * 100, sample_chars=1000, length=length))

    def test_unscored_byte_keeps_its_position_and_nan(self):
        original = np.array([np.nan, 0.0, 3.0, 2.0])
        positions, scores = entropy_window({"example_H": original}, 3)
        np.testing.assert_array_equal(positions, [0, 1, 2])
        self.assertTrue(np.isnan(scores[0]))
        np.testing.assert_array_equal(scores[1:], [0.0, 3.0])
        self.assertTrue(np.isnan(original[0]))
        self.assertEqual(len(original), 4)

    def test_zero_initial_score_and_nonfinite_targets_are_refused(self):
        for scores in ([0.0, 1.0], [np.nan, np.inf], [np.nan, -1.0]):
            with self.assertRaises(ValueError):
                entropy_window({"example_H": scores})

    def test_cached_but_unaccepted_modalities_are_refused(self):
        products = {k: {} for k in ["vqtrain", "nyquist", "codec", "ctc", "clip"]}
        with self.assertRaises(ValueError):
            modality_products({"products": products})
        with self.assertRaises(ValueError):
            modality_products({"numerical_acceptance": {"status": "passed"}, "products": {"clip": {}}})

    def test_nonfinite_or_negative_entropy_threshold_is_refused(self):
        for value in [np.nan, np.inf, -np.inf, -1.0]:
            with self.assertRaises(ValueError):
                entropy_threshold({"threshold": value})
        self.assertEqual(entropy_threshold({"threshold": 0.0}), 0.0)

    def test_no_recap_scene_path_calls_historical_producers(self):
        path = Path(__file__).resolve().parents[1] / "videos/ai/ai23/s18_outro.py"
        tree = ast.parse(path.read_text())
        calls = [n.args[0].value for n in ast.walk(tree)
                 if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "load"
                 and n.args and isinstance(n.args[0], ast.Constant)]
        self.assertEqual(set(calls), {"bpe_qa_accepted", "recap_modalities_qa_accepted"})
        cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "Outro")
        tiles = next(n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == "tiles")
        # Missing modalities must be rejected before constructing the text tiles.
        gate = next(i for i, n in enumerate(tiles.body) if "recap_modalities_qa_accepted" in ast.unparse(n))
        text = next(i for i, n in enumerate(tiles.body) if "self.text_tiles()" in ast.unparse(n))
        self.assertLess(gate, text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
