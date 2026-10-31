"""A resumed benchmark must use the same passage as its cached model rows."""

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np

from videos.ai.ai1 import compute


class LanguageModelResumeTests(unittest.TestCase):
    def test_changed_passage_invalidates_completed_models_in_partial_run(self):
        models = [("first", "first", 10, 2020, 8), ("second", "second", 20, 2021, 8)]

        def score(model, window, passage):
            bits = np.full(len(passage), 1.0 if model == "first" else .5)
            return {"bits": bits, "offsets": [(i, i + 1) for i in range(len(passage))],
                    "tokens": list(passage)}

        with tempfile.TemporaryDirectory() as tmp, patch.object(compute, "DATA_DIR", Path(tmp)), \
                patch.object(compute, "LMS", models):
            first_passage = "first\nsecond\nthird"
            result = score("first", 8, first_passage)
            with patch.object(compute, "text", return_value=first_passage), \
                    patch.object(compute, "lm_bits", side_effect=[result, RuntimeError("interrupted")]):
                with self.assertRaisesRegex(RuntimeError, "interrupted"):
                    compute.compute_lms()
            self.assertTrue((Path(tmp) / "lms.partial.json").exists())
            with patch.object(compute, "text", return_value="first\nsecond\nnew third"), \
                    patch.object(compute, "lm_bits", side_effect=score) as scoring:
                completed = compute.compute_lms()
            self.assertEqual(scoring.call_count, 2)
            self.assertEqual(completed["paragraph"], "new third")
            self.assertEqual(len(completed["surprise"]["first"]["tokens"]), len("new third"))
            self.assertFalse((Path(tmp) / "lms.partial.json").exists())
