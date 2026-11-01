"""Tiny actual-source GP coordinate checks; no scene, loader, TeX or producer imports."""
import ast
from pathlib import Path
from types import SimpleNamespace
import unittest

import numpy as np

SOURCE = Path(__file__).resolve().parents[1] / 'videos/ai/ai7/s14_gp.py'


def function(name, method=None):
    tree = ast.parse(SOURCE.read_text())
    if method:
        tree = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == method)
    return next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == name)


def pure(name, env, method=None):
    node = function(name, method)
    exec(compile(ast.Module(body=[node], type_ignores=[]), 'actual-GP-coordinate-source', 'exec'), env)
    return env[name]


class PathSink:
    def __init__(self, *args, **kwargs):
        self.points = np.array(args) if args else None

    def set_points_as_corners(self, points):
        self.points = np.array(points)
        return self


class GPViewport(unittest.TestCase):
    def test_actual_model_viewport_covers_prior_post_subset_bands_and_data(self):
        viewport = pure('gp_viewport', {'np': np})
        env = {'gp_viewport': viewport, 'y': np.array([0., 1., 2.]),
               'prior': np.array([[-8., 0., 1.]]), 'post': np.array([[0., 14., 1.]]),
               'mean': np.array([1., 1., 1.]), 'sd': np.array([1., 1., 1.]),
               'mean20': np.array([-30., 1., 1.]), 'sd20': np.array([.5, .5, .5])}
        body = function('functions')
        assignment = next(n for n in ast.walk(body) if isinstance(n, ast.Assign)
                          and isinstance(n.targets[0], ast.Tuple)
                          and ast.unparse(n.targets[0]) == '(ylo, yhi)')
        low, high = eval(compile(ast.Expression(assignment.value), 'actual-viewport-inputs', 'eval'), env)
        self.assertLess(low, -31.)
        self.assertGreater(high, 14.)
        np.testing.assert_array_equal(env['mean20'], [-30., 1., 1.])

    def test_every_sequential_state_uses_one_inclusive_viewport(self):
        viewport = pure('gp_viewport', {'np': np})
        means = np.array([[0., 1., 2.], [-25., 2., 3.], [0., 1., 20.]])
        sds = np.array([[1., 1., 1.], [5., 1., 1.], [1., 1., 5.]])
        env = {'gp_viewport': viewport, 'y': np.array([0., 1., 2.]), 'means': means, 'sds': sds}
        assignment = next(n for n in ast.walk(function('land')) if isinstance(n, ast.Assign)
                          and isinstance(n.targets[0], ast.Tuple)
                          and ast.unparse(n.targets[0]) == '(ylo, yhi)')
        low, high = eval(compile(ast.Expression(assignment.value), 'actual-sequential-inputs', 'eval'), env)
        self.assertLess(low, -35.)
        self.assertGreater(high, 30.)

    def test_negative_and_high_sampled_vertices_are_not_relocated_or_smoothed(self):
        xs = np.array([0., 1., 2.])
        ax = SimpleNamespace(c2p=lambda x, y: np.array([x, y, 0.]))
        env = {'np': np, 'ax': ax, 'xs': xs, 'VMobject': PathSink}
        curve = pure('curve', env, method='functions')
        values = np.array([-5., 12., -5.])
        result = curve(values, 'unused')
        np.testing.assert_array_equal(result.points[:, 1], values)
        # The old lower/upper clamp would manufacture equal boundary vertices.
        other = curve(np.array([-2., 11., -2.]), 'unused')
        self.assertTrue(np.all(result.points[[0, 2], 1] < other.points[[0, 2], 1]))

    def test_sequential_polygon_and_mean_retain_actual_coordinates(self):
        means = np.array([[-20., 1., 30.]])
        sd = np.array([[2., 3., 4.]])
        env = {'np': np, 'k': SimpleNamespace(get_value=lambda: 0), 'means': means, 'sds': sd,
               'xs': np.array([0., 1., 2.]), 'ax': SimpleNamespace(c2p=lambda x, y: [x, y, 0.]),
               'VGroup': lambda *objects: objects, 'Polygon': PathSink, 'VMobject': PathSink,
               'FN': 'unused', 'WHITE': 'unused'}
        band = pure('bandf', env, method='land')()
        np.testing.assert_array_equal(band[0].points[:3, 1], means[0] + 2 * sd[0])
        np.testing.assert_array_equal(band[0].points[3:, 1], (means[0] - 2 * sd[0])[::-1])
        np.testing.assert_array_equal(band[1].points[:, 1], means[0])

    def test_constant_trace_has_a_range_and_invalid_input_is_explicit(self):
        viewport = pure('gp_viewport', {'np': np})
        low, high = viewport(np.full(3, 5.))
        self.assertLess(low, 5.)
        self.assertGreater(high, 5.)
        for values in [(), ([],), ([np.nan],), ([np.inf],)]:
            with self.subTest(values=values), self.assertRaises(ValueError):
                viewport(*values)


if __name__ == '__main__':
    unittest.main()
