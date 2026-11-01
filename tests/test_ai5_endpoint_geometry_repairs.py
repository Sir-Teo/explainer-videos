"""Small geometry fixtures from actual Part5 scene code; no data or scene load."""
import ast
import math
from pathlib import Path
import unittest

import numpy as np

ROOT = Path(__file__).resolve().parents[1] / 'videos/ai/ai5'


def scatter_scale():
    tree = ast.parse((ROOT / 's10_sampling.py').read_text())
    node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'normal_scatter_scale')
    scope = {'np': np, 'math': math}
    exec(compile(ast.Module([node], type_ignores=[]), 'actual-normal-view-geometry', 'exec'), scope)
    return scope['normal_scatter_scale']


class Part5EndpointGeometryRepairs(unittest.TestCase):
    def test_normal_view_preserves_tail_coordinates_and_single_linear_scale(self):
        points = np.array([[0., 0.], [2.8, -.5], [3.1, -.5], [-1., -2.9]])
        before = points.copy()
        scale = scatter_scale()(points)
        screen = points * scale
        np.testing.assert_array_equal(points, before)
        np.testing.assert_allclose(screen / scale, points, rtol=0, atol=1e-15)
        self.assertLess(np.abs(screen).max(), 2.04)
        # These distinct real tails collapsed together under the old2.4 cap.
        self.assertGreater(screen[2, 0], screen[1, 0])
        self.assertAlmostEqual(np.linalg.norm(screen[2] - screen[1]), .3 * scale)

    def test_normal_view_fits_small_zero_and_wider_cohorts_without_unit_distortion(self):
        f = scatter_scale()
        for points in [np.zeros((4, 2)), np.array([[.5, -.2]]), np.array([[12., -8.], [0., 0.]])]:
            scale = f(points)
            self.assertGreater(scale, 0)
            self.assertTrue(np.isfinite(scale))
            self.assertLess(np.abs(points * scale).max(), 2.04)
            self.assertAlmostEqual((2 * scale) / scale, 2)

    def test_normal_view_rejects_nonfinite_or_non_coordinate_cohorts(self):
        f = scatter_scale()
        for points in [[], [1., 2.], [[1., 2., 3.]], [[np.nan, 1.]], [[np.inf, 1.]]]:
            with self.subTest(points=points), self.assertRaises(ValueError):
                f(points)
        for radius in [0., -1., np.inf, np.nan]:
            with self.subTest(radius=radius), self.assertRaises(ValueError):
                f([[0., 0.]], radius)

    def test_bayes_passes_true_cached_vertices_and_plot_bounds_to_clipper(self):
        tree = ast.parse((ROOT / 's06_bayes.py').read_text())
        method = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == 'map_')
        nodes = [n for n in method.body if isinstance(n, ast.Assign)
                 and any(isinstance(t, ast.Name) and t.id in ('fm', 'fb') for t in n.targets)]
        calls = []
        def clipped_curve(ax, xs, ys, **kwargs):
            calls.append((ax, xs.copy(), ys.copy(), kwargs))
            return object()
        data = {'fit_mle': np.array([0., 3., 0.]), 'fit_best': np.array([0., -2., 0.])}
        scope = dict(np=np, d=data, xt_=np.array([0., .5, 1.]), ax='axis', clipped_curve=clipped_curve,
                     C=type('Colors', (), {'SURPRISE': 'pink', 'BITS': 'gold'})())
        exec(compile(ast.Module(nodes, type_ignores=[]), 'actual-bayes-curves', 'exec'), scope)
        self.assertEqual(len(calls), 2)
        for call, key in zip(calls, ['fit_mle', 'fit_best']):
            np.testing.assert_array_equal(call[2], data[key])
            self.assertEqual(call[3]['x_bounds'], (0, 1))
            self.assertEqual(call[3]['y_bounds'], (-1.6, 1.6))

    def test_tails_sends_uncapped_exponential_vertices_to_clipper(self):
        tree = ast.parse((ROOT / 's09_tails.py').read_text())
        trick = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == 'trick')
        node = next(n for n in trick.body if isinstance(n, ast.Assign)
                    and any(isinstance(t, ast.Name) and t.id == 'g_' for t in n.targets))
        calls = []
        xs = np.linspace(0, 3, 120)
        def clipped_curve(ax, x, y, **kwargs):
            calls.append((x, y, kwargs))
        scope = dict(np=np, a_='axis', xs_=xs, f=lambda x: np.exp(1.2*(x-1.5)),
                     clipped_curve=clipped_curve, C=type('Colors', (), {'BITS': 'gold'})())
        exec(compile(ast.Module([node], type_ignores=[]), 'actual-tails-exponential', 'exec'), scope)
        self.assertEqual(len(calls), 1)
        np.testing.assert_array_equal(calls[0][1], np.exp(1.2*(xs-1.5)))
        self.assertGreater(calls[0][1].max(), 2.2)
        self.assertEqual(calls[0][2]['x_bounds'], (0, 3))
        self.assertEqual(calls[0][2]['y_bounds'], (0, 2.2))


if __name__ == '__main__':
    unittest.main()
