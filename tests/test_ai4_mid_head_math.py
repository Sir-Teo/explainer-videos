"""Small Part4 scene-contract checks; no scene imports, cache loads or rendering."""
import ast
import math
from pathlib import Path
import unittest

import numpy as np

from explainer.ai.autodiff import Tensor, sigmoid, tape


PART = Path(__file__).resolve().parents[1] / "videos/ai/ai4"


def function(filename, name):
    tree = ast.parse((PART / filename).read_text())
    node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name)
    env = dict(np=np, math=math)
    exec(compile(ast.Module([node], type_ignores=[]), str(PART / filename), "exec"), env)
    return env[name]


class TrainingDisplayTests(unittest.TestCase):
    def test_uniform_raw_zero_is_negative_log_vocabulary_not_zero(self):
        normalize = function("s09_train.py", "row_log_probabilities")
        lp = normalize(np.zeros((27, 27)))
        np.testing.assert_allclose(lp, -math.log(27))
        np.testing.assert_allclose(np.exp(lp).sum(1), 1)

    def test_large_scores_and_row_shift_do_not_change_probabilities(self):
        normalize = function("s09_train.py", "row_log_probabilities")
        z = np.array([[1000., 999., 998.], [-1000., -1002., -999.]])
        with np.errstate(over="raise", invalid="raise"):
            lp = normalize(z)
            shifted = normalize(z + np.array([[750.], [-320.]]))
        np.testing.assert_allclose(lp, shifted, atol=1e-12)
        np.testing.assert_allclose(np.exp(lp).sum(1), 1)

    def test_invalid_snapshot_rejected_without_computation(self):
        normalize = function("s09_train.py", "row_log_probabilities")
        for z in ([1., 2.], [[0., np.nan]], [[0., np.inf]]):
            with self.subTest(z=z), self.assertRaises(ValueError):
                normalize(z)

    def test_single_curve_point_never_reveals_future_sample(self):
        prefix = function("s09_train.py", "recorded_curve_prefix")
        values = np.array([[1., 4.75], [25., 4.], [50., 3.8]])
        self.assertEqual(prefix(values, 0).shape, (0, 2))
        np.testing.assert_array_equal(prefix(values, 1), np.repeat(values[:1], 2, axis=0))
        np.testing.assert_array_equal(prefix(values, 2), values[:2])
        np.testing.assert_array_equal(prefix(values, 100), values)

    def summary(self, **updates):
        result = dict(bits_train=3.34, bits_valid=3.4, H_cond=3.33, corr=.98, steps=1500,
                      metrics={"correlation": {"threshold": 1e-4, "count": 321}})
        result.update(updates)
        return result

    def test_producer_accepted_correlation_and_weaker_run_both_remain_visible(self):
        read = function("s09_train.py", "training_readout")
        near = read(self.summary())
        far = read(self.summary(bits_train=4.1, corr=.2))
        self.assertAlmostEqual(near["gap"], .01)
        self.assertAlmostEqual(far["gap"], .77)
        self.assertNotEqual(near["loss_verdict"], far["loss_verdict"])
        self.assertEqual(far["correlation"], {"threshold": 1e-4, "count": 321})
        self.assertEqual(far["corr_tex"], "0.200")

    def test_undefined_correlation_is_not_replaced_with_a_numeric_success(self):
        read = function("s09_train.py", "training_readout")
        for corr in (math.nan, None):
            result = read(self.summary(corr=corr, metrics={"correlation": {"threshold":1e-4,"count":0}}))
            self.assertIn("undefined", result["corr_tex"])
            self.assertEqual(result["correlation"]["count"], 0)

    def test_nonfinite_loss_summary_is_invalid_data_not_underperformance(self):
        with self.assertRaises(ValueError):
            function("s09_train.py", "training_readout")(self.summary(bits_train=math.nan))


class TapeAndCheckTests(unittest.TestCase):
    def test_gradient_gap_preserves_exact_zero_and_reports_small_positive_errors(self):
        describe = function("s08_library.py", "gap_report")
        self.assertIn("exactly zero", describe(0))
        self.assertNotIn("exactly zero", describe(1e-12))
        self.assertIn("-12", describe(1e-12))
        for gap in (-1, math.nan, math.inf):
            with self.subTest(gap=gap), self.assertRaises(ValueError):
                describe(gap)

    def test_actual_forward_tape_loop_highlights_edge_destination(self):
        w, b = Tensor(.7, requires_grad=True), Tensor(-.2, requires_grad=True)
        e = sigmoid(w * 2 + b) - 1.5
        tp = tape(e * e)
        self.assertEqual([v["op"] for v in tp], ["input", "*", "input", "+", "sigmoid", "+", "*"])
        edges = [(str(a), str(v["i"])) for v in tp for a in sorted(set(v["args"]))]
        tree = ast.parse((PART / "s08_library.py").read_text())
        order = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == "order")
        loop = next(n for n in ast.walk(order) if isinstance(n, ast.For)
                    and any(isinstance(x, ast.Name) and x.id == "destination" for x in ast.walk(n.target)))
        class Line:
            def __init__(self, index): self.index = index
            @property
            def animate(self): return self
            def set_color(self, color): return self.index
        class Scene:
            def __init__(self): self.calls = []
            def play(self, pulse, highlighted, **kw): self.calls.append((pulse, highlighted))
        scene = Scene()
        env = dict(edges=edges, fwd=edges, lines=[Line(i) for i in range(len(tp))], self=scene, VALUE="blue")
        exec(compile(ast.Module([loop], type_ignores=[]), "actual-forward-tape-loop", "exec"), env)
        self.assertEqual([line for _, line in scene.calls], [int(b) for _, b in edges])
        self.assertEqual([line for _, line in scene.calls], [1, 3, 3, 4, 5, 6])


class FloatingPointTests(unittest.TestCase):
    def test_normal_bound_does_not_extend_to_half_a_subnormal_ulp(self):
        x = 2. ** -25
        rounded = float(np.float16(x))
        self.assertEqual(rounded, 0.)
        self.assertEqual(abs(rounded - x) / x, 1.)
        self.assertGreater(abs(rounded - x) / x, 2. ** -11)
        values = np.asarray(np.arange(1, 33) * 2. ** -24, dtype=np.float16).astype(float)
        np.testing.assert_array_equal(np.diff(values), np.full(31, 2. ** -24))

    def test_actual_ulp_plot_bounds_include_smallest_finite_gap(self):
        tree = ast.parse((PART / "s10_floats.py").read_text())
        method = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == "ulp")
        names = {"format_keys", "finite_logs", "ylo", "yhi"}
        assignments = [n for n in method.body if isinstance(n, ast.Assign)
                       and isinstance(n.targets[0], ast.Name) and n.targets[0].id in names]
        d = {f"ulp_{key}":np.array([2.**-50, 2.**-20, 2.**12, np.nan])
             for key in ("fp32", "bf16", "fp16", "e5m2", "e4m3")}
        env = dict(np=np, math=math, d=d)
        exec(compile(ast.Module(assignments,type_ignores=[]), "actual-ulp-plot-bounds", "exec"), env)
        self.assertLessEqual(env["ylo"], math.log10(2.**-50))
        self.assertGreaterEqual(env["yhi"], math.log10(2.**12))


class ModeTimingTests(unittest.TestCase):
    def test_exact_timing_tie_is_not_counted_as_reverse_mode_win(self):
        agreement = function("s06_modes.py", "cheaper_mode_agreement")
        # Reverse is cheaper in the first cell, but both clocks are equal.
        wins, total = agreement([[4., 1., 2.]], [[1., 4., 2.]], [[1., 1., 1.]], [[1., 2., 7.]])
        self.assertEqual((wins, total), (1, 2))

    def test_count_order_and_clock_order_are_compared_independently(self):
        agreement = function("s06_modes.py", "cheaper_mode_agreement")
        self.assertEqual(agreement([10., 1.], [1., 10.], [2., 2.], [1., 1.]), (1, 2))


if __name__ == "__main__":
    unittest.main()
