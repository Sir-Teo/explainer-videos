"""Synthetic math/plot regressions; no scene, producer, cache or Manim imports."""

import ast
import importlib.util
from pathlib import Path
from types import SimpleNamespace
import unittest

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PART = ROOT / 'videos/ai/ai9'
spec = importlib.util.spec_from_file_location('ai9_math_plotting', PART / 'plotting.py')
plotting = importlib.util.module_from_spec(spec)
spec.loader.exec_module(plotting)


def function(filename, name, env):
    node = next(n for n in ast.walk(ast.parse((PART / filename).read_text()))
                if isinstance(n, ast.FunctionDef) and n.name == name)
    exec(compile(ast.Module(body=[node], type_ignores=[]), 'actual-scene-closure', 'exec'), env)
    return env[name]


class PathSink:
    def __init__(self, **kwargs):
        pass

    def set_points_as_corners(self, points):
        self.points = np.asarray(points, float)
        return self


class RecordedRanges(unittest.TestCase):
    def test_log_range_contains_every_value_without_modifying_histories(self):
        histories = [np.array([3., .2, 1e-10]), np.array([8., np.nan, np.inf, 5e-324])]
        before = [h.copy() for h in histories]
        lo, hi = plotting.log_plot_range(histories)
        for values, original in zip(histories, before):
            logs = plotting.safe_log_values(values)
            valid = np.isfinite(values)
            self.assertTrue((logs[valid] > lo).all())
            self.assertTrue((logs[valid] < hi).all())
            np.testing.assert_array_equal(logs[valid], np.log10(values[valid]))
            self.assertTrue(np.isnan(logs[~valid]).all())
            np.testing.assert_array_equal(values, original)

    def test_constant_histories_expand_axes_without_creating_observations(self):
        for value in (0.01, 1., 7.):
            lo, hi = plotting.log_plot_range([[value, value]])
            self.assertLess(lo, np.log10(value))
            self.assertGreater(hi, np.log10(value))
        for value in (-7., 0., 0.1, 12.):
            lo, hi = plotting.linear_plot_range([[value, value]])
            self.assertLess(lo, value)
            self.assertGreater(hi, value)

    def test_linear_range_uses_full_histories_not_only_final_values(self):
        histories = [np.array([17., 4., 3.]), np.array([-2., np.nan, np.inf, 3.1])]
        before = [h.copy() for h in histories]
        lo, hi = plotting.linear_plot_range(histories)
        self.assertLess(lo, -2.)
        self.assertGreater(hi, 17.)
        for values, original in zip(histories, before):
            np.testing.assert_array_equal(values, original)

    def test_invalid_or_absent_data_fail_explicitly(self):
        for histories in ([], [[]], [[np.nan, np.inf, -np.inf]]):
            for helper in (plotting.log_plot_range, plotting.linear_plot_range):
                with self.subTest(helper=helper.__name__, histories=histories), self.assertRaises(ValueError):
                    helper(histories)
        for values in ([0.], [-1.], [1., 0., np.nan]):
            with self.assertRaisesRegex(ValueError, 'zero needs explicit'):
                plotting.safe_log_values(values)
            with self.assertRaises(ValueError):
                plotting.log_plot_range([values])
        for padding in (0., -1., np.nan, np.inf):
            for helper in (plotting.log_plot_range, plotting.linear_plot_range):
                with self.assertRaises(ValueError):
                    helper([[1., 2.]], padding=padding)
        with self.assertRaises(ValueError):
            plotting.linear_plot_range([[-1e308, 1e308]])


class ActualSceneCoordinates(unittest.TestCase):
    def test_barron_path_keeps_subfloor_errors_and_original_endpoints(self):
        xs = np.array([4., 16., 64., 256., 1024.])
        errors = np.array([.1, .003, 2e-5, 9e-7, 5e-8])  # synthetic, not a scientific result
        before = errors.copy()
        env = dict(np=np, ax=None, safe_log_values=plotting.safe_log_values,
                   curve=lambda ax, x, y, *args: np.column_stack((x, y)))
        path = function('s07_barron.py', 'path', env)
        actual = path(xs, errors, 'unused')
        np.testing.assert_array_equal(actual, np.column_stack((np.log10(xs), np.log10(errors))))
        self.assertTrue(np.all(np.diff(actual[-3:, 1]) < 0))
        np.testing.assert_array_equal(errors, before)

    def test_kan_replay_never_exposes_future_vertices_and_keeps_final_errors(self):
        current = SimpleNamespace(value=0.)
        arr = np.column_stack(([0., 10., 40., 100.], [0., 0., 0., 0.], [7., .3, 1e-5, 2e-8]))
        before = arr.copy()
        env = dict(np=np, safe_log_values=plotting.safe_log_values, checkpoint_prefix=plotting.checkpoint_prefix,
                   t=SimpleNamespace(get_value=lambda: current.value), VMobject=PathSink,
                   g=SimpleNamespace(ax=SimpleNamespace(c2p=lambda x, y: [x, y, 0.])))
        make = function('s15_kan.py', 'upto', env)(arr, 'unused')
        for step in np.linspace(0., 100., 401):
            current.value = step
            points = make().points
            self.assertLessEqual(points[:, 0].max(), step)
            self.assertTrue((np.diff(points[:, 0]) >= 0).all())
            np.testing.assert_allclose(points[-1], [step, np.interp(step, arr[:, 0], np.log10(arr[:, 2])), 0.])
        np.testing.assert_array_equal(make().points, np.column_stack((arr[:, 0], np.log10(arr[:, 2]), np.zeros(4))))
        np.testing.assert_array_equal(arr, before)

    def test_kan_edge_scales_are_fixed_per_edge_over_all_snapshots(self):
        # Deliberately distinct amplitudes and offsets at every synthetic edge/time.
        E = np.arange(3 * 15 * 5, dtype=float).reshape(3, 15, 5)
        before = E.copy()
        tree = ast.parse((PART / 's15_kan.py').read_text())
        method = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == 'replay')
        limits = next(n for n in method.body if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Tuple)
                      and any(isinstance(t, ast.Name) and t.id == 'edge_lo' for t in n.targets[0].elts))
        env = {'E': E}
        exec(compile(ast.Module(body=[limits], type_ignores=[]), 'actual-edge-limits', 'exec'), env)

        class Edge:
            def __init__(self, ys, lo, hi):
                self.ys, self.lo, self.hi = ys.copy(), lo, hi

            def move_to(self, position):
                return self

        class Group(list):
            def add(self, item):
                self.append(item)

        env.update(np=np, VGroup=Group, KANC='unused', C=SimpleNamespace(BITS='unused'),
                   xs=np.arange(5), pos1=[None] * 10, pos2=[None] * 5,
                   mini_plot=lambda xs, ys, color, lo, hi: Edge(ys, lo, hi))
        edges = function('s15_kan.py', 'edges', env)
        order = [2 * (i % 5) + i // 5 for i in range(10)] + list(range(10, 15))
        for k in range(3):
            for j, edge in zip(order, edges(k)):
                self.assertEqual(edge.lo, E[:, j, :].min())
                self.assertEqual(edge.hi, E[:, j, :].max())
                np.testing.assert_array_equal(edge.ys, E[k, j])
        np.testing.assert_array_equal(E, before)



class ViewportGeometry(unittest.TestCase):
    def test_crossing_ramp_has_true_boundary_intersections_without_flattened_tails(self):
        xs,ys=np.arange(5.),np.arange(5.)-2
        before=ys.copy();runs=plotting.clip_y_segments(xs,ys,-.5,.5)
        self.assertEqual(len(runs),1)
        np.testing.assert_array_equal(runs[0],[[1.5,-.5],[2.,0.],[2.5,.5]])
        np.testing.assert_array_equal(ys,before)
    def test_offscreen_excursion_does_not_create_a_false_boundary_plateau(self):
        runs=plotting.clip_y_segments([0,1,2],[0,2,0],0,1)
        self.assertEqual(len(runs),2)
        np.testing.assert_array_equal(runs[0],[[0,0],[.5,1]])
        np.testing.assert_array_equal(runs[1],[[1.5,1],[2,0]])
        self.assertEqual(plotting.clip_y_segments([0,1],[2,2],0,1),[])
    def test_missing_values_split_runs_and_invalid_bounds_are_rejected(self):
        self.assertEqual(plotting.clip_y_segments([0,1,2],[0,np.nan,1],0,1),[])
        with self.assertRaises(ValueError):plotting.clip_y_segments([0,1],[0,1],1,1)

if __name__ == '__main__':
    unittest.main()
