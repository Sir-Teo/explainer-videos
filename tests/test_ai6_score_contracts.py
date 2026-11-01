"""Actual small score functions/data-flow expressions, without default producers."""
from __future__ import annotations

import ast
from pathlib import Path
import unittest
from types import SimpleNamespace

import numpy as np

from videos.ai.ai6 import contracts

SOURCE = Path(__file__).resolve().parents[1] / "videos/ai/ai6/compute.py"


def function_ast(names, namespace):
    tree = ast.parse(SOURCE.read_text())
    nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in names]
    if len(nodes) != len(names):
        raise AssertionError("Actual source function missing")
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(SOURCE), "exec"), namespace)
    return namespace


class ScoreTests(unittest.TestCase):
    def test_public_load_dispatches_through_current_cached_only_instance_guard(self):
        calls = []
        cache = SimpleNamespace(load=lambda name: calls.append(name))
        env = function_ast(["load"], {"CACHE": cache})
        def guard(name):
            raise RuntimeError("QA guard before any producer")
        cache.load = guard
        with self.assertRaisesRegex(RuntimeError, "QA guard"):
            env["load"]("missing")
        self.assertEqual(calls, [])

    def test_extreme_wrong_confidence_is_not_silently_capped(self):
        z = np.array([1000., -1000., 1000., -1000.])
        y = np.array([0, 1, 1, 0])
        p = .5 * (1 + np.tanh(.5 * z))
        row = contracts.score_summary(z, y, p)
        self.assertEqual(row["logloss"], 500.)
        self.assertEqual(row["score"]["rows_beyond_old_probability_floor"], 4)
        self.assertEqual(row["score"]["wrong_label_losses_above_old_cap"], 2)
        self.assertIsNone(row["score"]["probability_clip"])
        self.assertEqual(row["score"]["unit"], "nats per page")
        self.assertTrue(np.isfinite(row["logloss"]))

    def test_moderate_logits_match_exact_probability_log_score(self):
        z = np.array([-4., -.5, 0., 1., 5.])
        y = np.array([1, 0, 1, 0, 1])
        p = .5 * (1 + np.tanh(.5 * z))
        expected = -np.mean(y * np.log(p) + (1 - y) * np.log1p(-p))
        actual = contracts.score_summary(z, y, p)
        self.assertAlmostEqual(actual["logloss"], expected)
        self.assertEqual(actual["score"]["rows_beyond_old_probability_floor"], 0)
        self.assertEqual(actual["count"].sum(), len(y))
        self.assertAlmostEqual(actual["brier"], float(np.mean((p - y) ** 2)))

    def test_score_rejects_invalid_or_misaligned_cohorts(self):
        cases = [([0.], [.5], [.5]), ([float("inf")], [1], [1.]),
                 ([0.], [1, 0], [.5]), ([0.], [1], [.9]), ([], [], []),
                 ([[0.]], [[1]], [[.5]])]
        for z, y, p in cases:
            with self.subTest(z=z, y=y, p=p), self.assertRaises(ValueError):
                contracts.score_summary(z, y, p)

    def test_actual_reliability_requires_original_logits(self):
        env = function_ast(["reliability"], {"score_summary": contracts.score_summary})
        with self.assertRaises(TypeError):
            env["reliability"](np.array([1.]), np.array([0]))
        self.assertEqual(env["reliability"](np.array([1.]), np.array([0]), logits=np.array([1000.]))["logloss"], 1000.)

    def test_actual_calibration_retains_all_oof_logits_without_running_a_fitter(self):
        n = 20
        X = np.zeros((n, 70)); X[:, 0] = np.arange(n)
        y = np.arange(n) % 2
        X2 = X[:, :2].copy()
        fits = []; nb_fits = []; platt_inputs = []

        def no_fit(a, labels, l2):
            fits.append((a[:, 0].copy(), labels.copy()))
            w = np.zeros(a.shape[1]); w[0] = 1000.
            return w, -500.

        def no_nb_fit(a, labels):
            nb_fits.append(a[:, 0].copy())
            w = np.zeros(a.shape[1]); w[0] = -200.
            return w, 100.

        def no_platt_fit(scores, labels):
            platt_inputs.append((scores.copy(), labels.copy()))
            return .001, -.5

        # Identity transform keeps synthetic row IDs visible to the fit spies.
        # This fixture checks actual outer/inner data flow, not an optimizer.
        def identity_scaling(a, b):
            return a, b, np.zeros(a.shape[1]), np.ones(a.shape[1])

        env = function_ast(["rng", "kfold", "sigmoid", "acc_of", "reliability", "compute_calibration"],
                           {"np": np, "FOLDS": 10, "math": __import__("math"),
                            "split": lambda: (X, y, np.arange(n) % 3 == 0, X2),
                            "standardize": identity_scaling, "newton_logreg": no_fit, "nb_fit": no_nb_fit,
                            "platt": no_platt_fit, "score_summary": contracts.score_summary,
                            "canonical": contracts.content_digest,
                            "benchmark_protocol": contracts.benchmark_protocol})
        result = env["compute_calibration"]()
        f = result["fold_ids"]
        self.assertEqual(len(fits), 20)
        self.assertEqual(len(nb_fits), 60)
        self.assertEqual(len(platt_inputs), 10)
        for fold in range(10):
            train_ids = np.flatnonzero(f != fold)
            for ids, labels in fits[2 * fold:2 * fold + 2]:
                np.testing.assert_array_equal(ids, train_ids)
                np.testing.assert_array_equal(labels, y[train_ids])
            np.testing.assert_array_equal(nb_fits[6 * fold], train_ids)
            np.testing.assert_array_equal(platt_inputs[fold][0], -200 * train_ids + 100)
            np.testing.assert_array_equal(platt_inputs[fold][1], y[train_ids])
            # Every inner fit excludes a nonempty part of outer training data.
            for inner_ids in nb_fits[6 * fold + 1:6 * fold + 6]:
                self.assertTrue(set(inner_ids) < set(train_ids))
        for key in ("lr2", "lr70", "nb", "nb_platt"):
            self.assertEqual(result[f"z_{key}"].shape, (n,))
            np.testing.assert_array_equal(result[f"p_{key}"], env["sigmoid"](result[f"z_{key}"]))
            self.assertGreaterEqual(result[key]["logloss"], 0)
        np.testing.assert_array_equal(result["nb_z"], result["z_nb"])
        self.assertGreater(result["lr2"]["logloss"], 27.632)
        self.assertTrue(contracts.valid_structure("calibration", result, dict(n_pages=n, labels=y.tolist())))
        result["lr2"]["logloss"] = 27.631
        self.assertFalse(contracts.valid_structure("calibration", result, dict(n_pages=n, labels=y.tolist())))

    def test_actual_logistic_guard_accepts_a_legitimate_unexpected_ranking(self):
        tree = ast.parse(SOURCE.read_text())
        fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "compute_logistic")
        guard = next(n.test for n in ast.walk(fn) if isinstance(n, ast.Assert))
        code = compile(ast.Expression(guard), str(SOURCE), "eval")
        env = dict(np=np, acc2=.8, acc70=.6, loss=.3, eig=np.array([.01, .1, 1.]))
        self.assertTrue(eval(code, env))
        self.assertTrue(eval(code, dict(env, acc70=.8)))
        self.assertFalse(eval(code, dict(env, eig=np.array([float("nan"), .1, 1.]))))
        self.assertFalse(eval(code, dict(env, eig=np.array([-.1, .1, 1.]))))

    def test_fixed_lexicon_protocol_is_explicit_about_evaluation_domain(self):
        p = contracts.benchmark_protocol()
        self.assertTrue(p["transductive_vocabulary"])
        self.assertEqual(p["book_ids"], [1342, 158, 98, 1400, 46])
        self.assertIn("including evaluation pages", p["vocabulary_fit"])
        self.assertIn("not unseen novels", p["evaluation_scope"])

    def test_nonfinite_nested_and_object_arrays_are_rejected(self):
        self.assertFalse(contracts.finite_tree({"nested": [{"score": float("nan")}]}))
        self.assertFalse(contracts.finite_tree(np.array([object()], dtype=object)))
        self.assertTrue(contracts.finite_tree({"crossover": None, "status": "not observed"}))


if __name__ == "__main__":
    unittest.main()
