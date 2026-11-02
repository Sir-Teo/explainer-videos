"""Small NumPy metric/checkpoint witnesses; no Torch import, model forward or training."""
from __future__ import annotations

import copy
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import numpy as np

from videos.ai.ai30 import grok as G


class GrokMetricsTests(unittest.TestCase):
    def setUp(self):
        self.constants = patch.multiple(G, P=7, N_KEY=2)
        self.constants.start()
        self.addCleanup(self.constants.stop)
        self.a, self.b, self.c = np.ogrid[:7, :7, :7]
        self.target = ((self.a + self.b) % 7)[..., 0].ravel()
        self.tr, self.te = np.arange(0, 49, 2), np.arange(1, 49, 2)
        self.correct = np.cos(2 * np.pi * (self.a + self.b - self.c) / 7)
        self.x = np.stack([self.a[..., 0].repeat(7, axis=1).ravel(),
                           self.b[..., 0].repeat(7, axis=0).ravel(), np.full(49, 7)], axis=1)

    def row(self, step):
        return dict(step=step, _logits=(3 * self.correct).astype(np.float32), spectrum=np.ones(3) / 3,
                    weight_norm=2., train_loss=1., test_loss=1.2, train_acc=.5, test_acc=.4,
                    legacy_key=[2, 3], legacy_restricted_loss=8., legacy_excluded_loss=9., legacy_sum_wave_r2=.1)

    def pins(self, steps=250):
        return G.checkpoint_pins(self.x, self.target, self.tr, self.te, steps)

    def checkpoint(self):
        return dict(metric_schema=G.METRIC_SCHEMA, pins=self.pins(), model={}, opt={}, sched={}, rng=b"fixture",
                    hist=[self.row(s) for s in (0, 100, 200, 250)], step=250)

    def test_basis_and_projection_preserve_sum_waves(self):
        B, _ = G.fourier_basis()
        np.testing.assert_allclose(B @ B.T, np.eye(7), atol=1e-14)
        other = np.cos(4 * np.pi * (self.a + self.b - self.c) / 7)
        np.testing.assert_allclose(G.restricted(3 * self.correct + 2 * other, [1]), 3 * self.correct, atol=1e-14)
        np.testing.assert_allclose(G.restricted(G.restricted(self.correct, [1]), [1]), self.correct, atol=1e-14)

    def test_restricted_preserves_answer_bias_excluded_removes_only_waves(self):
        bias = 2 * (np.arange(7) - 3)[None, None, :]
        L = 6 * self.correct + bias
        got = G.progress_metrics(L, [1], self.target, self.tr, self.te)
        self.assertAlmostEqual(got["restricted_loss"], G._ce(L, self.target, self.te), places=12)
        self.assertAlmostEqual(got["excluded_loss"], G._ce(np.broadcast_to(bias, L.shape), self.target, self.tr), places=12)
        self.assertGreater(got["restricted_loss"], G._ce(6 * self.correct, self.target, self.te) + 1)
        # A per-input scalar is a harmless gauge change, unlike an answer-specific bias.
        changed = G.progress_metrics(L + np.arange(49).reshape(7, 7, 1), [1], self.target, self.tr, self.te)
        np.testing.assert_allclose(list(got.values()), list(changed.values()), atol=1e-12)

    def test_output_key_rule_ignores_dc_and_combines_sine_cosine_energy(self):
        t = np.arange(7)
        WL = np.stack([3 * np.cos(2 * np.pi * t / 7), 4 * np.sin(4 * np.pi * t / 7), np.ones(7) * 1000])
        keys, spectrum = G.output_key_frequencies(WL, n_key=2)
        self.assertEqual(keys, [2, 1])
        np.testing.assert_allclose(spectrum, [9/25, 16/25, 0], atol=1e-14)
        keys, spectrum = G.output_key_frequencies(np.zeros((2, 7)), n_key=2)
        self.assertEqual(keys, [1, 2])  # explicit deterministic tie rule
        np.testing.assert_array_equal(spectrum, np.zeros(3))

    def test_retrospective_fixed_keys_preserve_adaptive_legacy_history(self):
        hist = [self.row(0), self.row(100)]
        hist[0]["legacy_key"] = [3, 2]
        done = G.finalize_history(hist, [1, 2], np.array([.7, .2, .1]), self.target, self.tr, self.te)
        self.assertIs(done, hist)
        for row in hist:
            self.assertEqual(row["key"], [1, 2])
            self.assertEqual(row["legacy_restricted_loss"], 8.)
            self.assertEqual(row["legacy_excluded_loss"], 9.)
            self.assertEqual(row["key_selection"], "retrospective_final_output_map")
        self.assertEqual(hist[0]["legacy_key"], [3, 2])
        self.assertAlmostEqual(hist[0]["restricted_loss"], hist[1]["restricted_loss"], places=14)
        np.testing.assert_array_equal(hist[-1]["output_spectrum"], [.7, .2, .1])
        self.assertAlmostEqual(hist[-1]["strict_cos_r2"], 1., places=12)

    def test_wrong_phase_passes_sum_fit_but_fails_correct_phase_fit(self):
        wrong = np.cos(2 * np.pi * (self.a + self.b + self.c) / 7)
        got = G.circuit_diagnostics(wrong, [1])
        self.assertAlmostEqual(got["sum_wave_r2"], 1., places=14)
        self.assertAlmostEqual(got["strict_cos_r2"], 0., places=14)
        self.assertAlmostEqual(got["strict_cos_coefficients"][0], 0., places=14)
        self.assertAlmostEqual((wrong.argmax(-1).ravel() == self.target).mean(), 1/7)

    def test_strict_fit_recovers_signed_amplitudes_and_addition_accuracy(self):
        other = np.cos(4 * np.pi * (self.a + self.b - self.c) / 7)
        got = G.circuit_diagnostics(3 * self.correct + 2 * other, [1, 2])
        np.testing.assert_allclose(got["strict_cos_coefficients"], [3, 2], atol=1e-14)
        self.assertAlmostEqual(got["strict_cos_r2"], 1., places=14)
        self.assertEqual(got["strict_cos_accuracy"], 1.)
        self.assertEqual(got["strict_cos_key"], [1, 2])
        negative = G.circuit_diagnostics(-self.correct, [1])
        self.assertAlmostEqual(negative["strict_cos_coefficients"][0], -1., places=14)
        self.assertEqual(negative["strict_cos_accuracy"], 0.)
        self.assertTrue(np.isnan(G.circuit_diagnostics(np.zeros((7, 7, 7)), [1])["strict_cos_r2"]))

    def test_checkpoint_accepts_complete_history_including_off_grid_endpoint(self):
        ck = self.checkpoint()
        G.validate_checkpoint(ck, self.pins(), 250)
        # Finalized public metrics are optional at an intermediate recovery checkpoint.
        G.finalize_history(ck["hist"], [1, 2], np.ones(3)/3, self.target, self.tr, self.te)
        G.validate_checkpoint(ck, self.pins(), 250)

    def test_checkpoint_rejects_legacy_missing_logits_and_missing_measurements(self):
        for defect in ("schema", "logits", "middle", "endpoint", "duplicate", "nonfinite"):
            with self.subTest(defect=defect):
                ck = self.checkpoint()
                if defect == "schema":
                    del ck["metric_schema"]
                elif defect == "logits":
                    del ck["hist"][1]["_logits"]
                elif defect == "middle":
                    ck["hist"].pop(1)
                elif defect == "endpoint":
                    ck["hist"][-1]["step"] = 249
                elif defect == "duplicate":
                    ck["hist"][2]["step"] = 100
                else:
                    ck["hist"][0]["_logits"][0, 0, 0] = np.nan
                with self.assertRaises(ValueError):
                    G.validate_checkpoint(ck, self.pins(), 250)

    def test_checkpoint_rejects_source_recipe_dataset_runtime_changes_and_later_state(self):
        ck = self.checkpoint()
        for component in ("source_sha256", "recipe", "dataset_sha256", "runtime_versions"):
            with self.subTest(component=component):
                expected = copy.deepcopy(self.pins())
                expected[component] = "changed"
                with self.assertRaisesRegex(ValueError, "pins mismatch"):
                    G.validate_checkpoint(ck, expected, 250)
        with self.assertRaisesRegex(ValueError, "precede checkpoint"):
            G.validate_checkpoint(ck, self.pins(200), 200)
        with self.assertRaisesRegex(ValueError, "pins mismatch"):
            G.validate_checkpoint(ck, self.pins(300), 300)
        # Same target labels but a different split must change the dataset binding.
        self.assertNotEqual(self.pins()["dataset_sha256"],
                            G.checkpoint_pins(self.x, self.target, self.te, self.tr, 250)["dataset_sha256"])

    def test_atomic_checkpoint_preserves_prior_file_on_serialization_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "grok.ckpt"
            path.write_bytes(b"previous")

            def fail(state, stream):
                stream.write(b"partial")
                raise RuntimeError("serialization interrupted")

            # A tiny serializer stub avoids importing Torch or constructing any model.
            with patch.dict(sys.modules, {"torch": SimpleNamespace(save=fail)}):
                with self.assertRaisesRegex(RuntimeError, "interrupted"):
                    G._atomic_checkpoint(path, {})
            self.assertEqual(path.read_bytes(), b"previous")
            self.assertEqual(list(Path(directory).iterdir()), [path])
            with patch.dict(sys.modules, {"torch": SimpleNamespace(save=lambda state, stream: stream.write(b"complete"))}):
                G._atomic_checkpoint(path, {})
            self.assertEqual(path.read_bytes(), b"complete")
            self.assertEqual(list(Path(directory).iterdir()), [path])


if __name__ == "__main__":
    unittest.main()
