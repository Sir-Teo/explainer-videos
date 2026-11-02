"""Synthetic coordinate regressions only: no scene/compute imports or scientific caches.

PathSink records geometry commands; it does not render or establish visual QA.
"""

import ast
import importlib.util
from pathlib import Path
from types import SimpleNamespace
import tarfile
import unittest

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
PART = ROOT / 'videos/ai/ai9'
BASELINE = ROOT / 'tests/fixtures/ai9-source-baseline/sources.tar.gz'
spec = importlib.util.spec_from_file_location('ai9_pure_plotting', PART / 'plotting.py')
plotting = importlib.util.module_from_spec(spec)
spec.loader.exec_module(plotting)


def original(filename):
    with tarfile.open(BASELINE) as archive:
        return archive.extractfile('videos/ai/ai9/' + filename).read().decode()


def function(source, name, env):
    node = next(n for n in ast.walk(ast.parse(source))
                if isinstance(n, ast.FunctionDef) and n.name == name)
    exec(compile(ast.Module(body=[node], type_ignores=[]), 'actual-plot-function', 'exec'), env)
    return env[name]


class PathSink:
    def __init__(self, *args, **kwargs):
        self.points = np.empty((0, 3))
        self.subpaths = []

    def set_points_as_corners(self, points):
        self.points = np.asarray(points, dtype=float)
        return self

    def add_subpath(self, points):
        self.subpaths.append(np.asarray(points).copy())


class CheckpointChronology(unittest.TestCase):
    def test_initial_and_exact_checkpoint_vertices(self):
        xs, ys = [0, 10, 40, 100], [8, 5, 3, 2.5]  # synthetic irregular history
        np.testing.assert_array_equal(plotting.checkpoint_prefix(xs, ys, 0), [[0, 8], [0, 8]])
        np.testing.assert_array_equal(plotting.checkpoint_prefix(xs, ys, 40), [[0, 8], [10, 5], [40, 3]])
        np.testing.assert_array_equal(plotting.checkpoint_prefix(xs, ys, 200), np.column_stack((xs, ys)))
        np.testing.assert_array_equal(plotting.checkpoint_prefix(xs, ys, -1), [[0, 8], [0, 8]])
        np.testing.assert_array_equal(plotting.checkpoint_prefix([5], [3], 9), [[5, 3], [5, 3]])

    def test_actual_scene_closures_never_reveal_future_or_backtrack_and_end_at_marker(self):
        for filename, name, ys, low, high in [
            ('s01_hook.py', 'acc_line', [.5, .9, .6, .99], .4, 1.),
            ('s16_lm.py', 'upto', [8., 5., 3., 2.5], -np.inf, np.inf),
        ]:
            cv = np.column_stack(([0., 10., 40., 100.], [0., 0., 0., 0.], ys))
            before = cv.copy()
            current = SimpleNamespace(value=0.)
            tracker = SimpleNamespace(get_value=lambda: current.value)
            ax = SimpleNamespace(c2p=lambda x, y: [x, y, 0.])
            env = dict(np=np, cv=cv, sv=tracker, t=tracker, ax=ax, g=SimpleNamespace(ax=ax),
                       clip=lambda y: float(np.clip(y, low, high)), checkpoint_prefix=plotting.checkpoint_prefix,
                       VMobject=PathSink, C=SimpleNamespace(BITS='unused', NEURAL='unused'))
            build = function((PART / filename).read_text(), name, env)
            for step in np.linspace(0, 100, 401):
                with self.subTest(scene=filename, step=step):
                    current.value = step
                    points = build().points
                    self.assertLessEqual(points[:, 0].max(), step)
                    self.assertTrue(np.all(np.diff(points[:, 0]) >= 0))
                    np.testing.assert_allclose(points[-1], [step, np.clip(np.interp(step, cv[:, 0], cv[:, 2]), low, high), 0.])
                    self.assertTrue(np.isfinite(points).all())
            np.testing.assert_array_equal(cv, before)

    def test_original_closures_reproduce_the_specific_defects_on_synthetic_data(self):
        cv = np.column_stack(([0., 10., 40.], [0., 0., 0.], [.5, .8, .9]))
        tracker = SimpleNamespace(get_value=lambda: 2.)
        ax = SimpleNamespace(c2p=lambda x, y: [x, y, 0.])
        env = dict(np=np, cv=cv, sv=tracker, t=tracker, ax=ax, g=SimpleNamespace(ax=ax),
                   clip=lambda y: y, VMobject=PathSink, C=SimpleNamespace(BITS='unused', NEURAL='unused'))
        hook = function(original('s01_hook.py'), 'acc_line', dict(env))().points
        lm = function(original('s16_lm.py'), 'upto', dict(env))().points
        self.assertGreater(hook[:, 0].max(), 2.)
        self.assertGreater(lm[:, 0].max(), 2.)
        self.assertTrue(np.any(np.diff(lm[:, 0]) < 0))

    def test_invalid_checkpoint_contract_fails_before_manufacturing_geometry(self):
        for xs, ys, step in [([], [], 0), ([0, 0], [1, 2], 0), ([1, 0], [1, 2], 0),
                             ([0, 1], [1], 0), ([0, 1], [1, np.nan], 0),
                             ([0, np.inf], [1, 2], 0), ([0, 1], [1, 2], np.nan)]:
            with self.subTest(xs=xs, ys=ys, step=step), self.assertRaises(ValueError):
                plotting.checkpoint_prefix(xs, ys, step)


class NonfiniteLossGeometry(unittest.TestCase):
    def test_actual_ablation_expression_keeps_nonfinite_observations_missing(self):
        method = next(n for n in ast.walk(ast.parse((PART / 's14_block.py').read_text()))
                      if isinstance(n, ast.FunctionDef) and n.name == 'ablation')
        expr = next(n.value for n in method.body if isinstance(n, ast.Assign)
                    and any(isinstance(t, ast.Name) and t.id == 'lines' for t in n.targets))
        values = np.array([8., 4., np.nan, np.inf, -np.inf, 3.])
        before = values.copy()
        env = dict(np=np, b={'synthetic': np.column_stack((np.arange(6), values))},
                   kinds=['synthetic'], VARIANT={'synthetic': ('unused', 'unused')},
                   g=SimpleNamespace(ax=None), lo=2., hi=5., finite_plot_values=plotting.finite_plot_values,
                   curve=lambda ax, xs, ys, *args: np.column_stack((xs, ys)))
        line = eval(compile(ast.Expression(expr), 'actual-ablation-lines', 'eval'), env)['synthetic']
        np.testing.assert_array_equal(line[[0, 1, 5], 1], [5., 4., 3.])
        self.assertTrue(np.isnan(line[2:5, 1]).all())
        np.testing.assert_array_equal(values, before)

    def test_actual_shared_curve_does_not_bridge_nonfinite_loss_intervals(self):
        shared = function((ROOT / 'explainer/ai/viz.py').read_text(), 'curve', dict(np=np, VMobject=PathSink))
        values = plotting.finite_plot_values([4., 3., np.nan, np.inf, 3.5, 2.5, -np.inf], 2., 5.)
        line = shared(SimpleNamespace(c2p=lambda x, y: [x, y, 0.]), np.arange(7), values, 'unused')
        self.assertEqual(len(line.subpaths), 2)
        np.testing.assert_array_equal(line.subpaths[0][:, 0], [0., 1.])
        np.testing.assert_array_equal(line.subpaths[1][:, 0], [4., 5.])
        self.assertTrue(all(np.isfinite(p).all() for p in line.subpaths))
        empty = shared(SimpleNamespace(c2p=lambda x, y: [x, y, 0.]), [0, 1],
                       plotting.finite_plot_values([np.nan, np.inf], 2., 5.), 'unused')
        self.assertEqual(empty.subpaths, [])

    def test_finite_only_viewport_behavior_is_unchanged(self):
        values = np.array([-2., 2., 2.5, 4., 8.])
        np.testing.assert_array_equal(plotting.finite_plot_values(values, 2., 5.), np.clip(values, 2., 5.))

    def test_actual_ablation_dashes_only_nonempty_paths(self):
        method = next(n for n in ast.walk(ast.parse((PART / 's14_block.py').read_text()))
                      if isinstance(n, ast.FunctionDef) and n.name == 'ablation')
        loop = next(n for n in method.body if isinstance(n, ast.For))
        empty = SimpleNamespace(has_points=lambda: False)
        finite = SimpleNamespace(has_points=lambda: True)
        calls = []

        def dash(path, num_dashes):
            if not path.has_points():
                raise IndexError('Manim 0.22 cannot dash an empty curve')
            calls.append((path, num_dashes))
            return 'dashed-finite-path'

        env = {'lines': {'post_ln': empty, 'pre_rms': finite}, 'DashedVMobject': dash}
        exec(compile(ast.Module(body=[loop], type_ignores=[]), 'actual-ablation-dash-loop', 'exec'), env)
        self.assertIs(env['lines']['post_ln'], empty)
        self.assertEqual(env['lines']['pre_rms'], 'dashed-finite-path')
        self.assertEqual(calls, [(finite, 40)])


class PreservedNarrationAndTiming(unittest.TestCase):
    def test_all_voiceover_expressions_bookmarks_play_wait_and_clear_calls_are_unchanged(self):
        def calls(source):
            return [ast.dump(n, include_attributes=False) for n in ast.walk(ast.parse(source))
                    if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                    and n.func.attr in {'voiceover', 'play', 'wait', 'wait_until', 'clear_scene'}]
        for filename in ['s01_hook.py']:
            with self.subTest(scene=filename):
                self.assertEqual(calls(original(filename)), calls((PART / filename).read_text()))

    def test_visual_scene_polish_preserves_narration_waits_and_requested_beat_lengths(self):
        def calls(source, names):
            return [ast.dump(n, include_attributes=False) for n in ast.walk(ast.parse(source))
                    if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr in names]

        def play_durations(source):
            return [[ast.dump(k, include_attributes=False) for k in n.keywords if k.arg == 'run_time']
                    for n in ast.walk(ast.parse(source)) if isinstance(n, ast.Call)
                    and isinstance(n.func, ast.Attribute) and n.func.attr == 'play']

        for filename in ['s02_neurons.py', 's03_perceptron.py']:
            before, after = original(filename), (PART / filename).read_text()
            with self.subTest(scene=filename):
                self.assertEqual(calls(before, {'voiceover', 'wait', 'wait_until', 'clear_scene'}),
                                 calls(after, {'voiceover', 'wait', 'wait_until', 'clear_scene'}))
                self.assertEqual(play_durations(before), play_durations(after))

        tree = ast.parse((PART / 's02_neurons.py').read_text())
        swap = next(n for n in ast.walk(tree) if isinstance(n, ast.Call)
                    and isinstance(n.func, ast.Name) and n.func.id == 'Succession'
                    and len(n.args) == 2 and isinstance(n.args[1], ast.Call)
                    and isinstance(n.args[1].func, ast.Name) and n.args[1].func.id == 'Write')
        durations = [ast.literal_eval(next(k.value for k in n.keywords if k.arg == 'run_time')) for n in swap.args]
        # Original Manim0.22 Write(rule) infers2s for this long formula (>=15
        # family members with points); the recorded EN/ZH transition is also2s.
        self.assertAlmostEqual(sum(durations), 2.)


if __name__ == '__main__':
    unittest.main()
