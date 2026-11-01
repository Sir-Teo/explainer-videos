"""Faithful clipping geometry with actual VMobjects, no scenes or cached data."""
import ast
from pathlib import Path
import unittest

import numpy as np

from videos.ai.ai5.plotting import _clip_segment, clipped_curve


class IdentityAxes:
    def c2p(self, x, y):
        return np.array([x, y, 0.])


class Part5ClippedCurveTests(unittest.TestCase):
    def plot(self, xs, ys, **kw):
        return clipped_curve(IdentityAxes(), xs, ys, x_bounds=(0, 1), y_bounds=(0, 1),
                             color="#7FD3FF", **kw)

    def test_visible_vertices_are_exact_and_segments_linear(self):
        points = [[0., .1, 0.], [.4, .8, 0.], [1., .3, 0.]]
        p = self.plot([x[0] for x in points], [x[1] for x in points])
        np.testing.assert_array_equal(p.get_start_anchors(), points[:-1])
        np.testing.assert_array_equal(p.get_end_anchors(), points[1:])
        for bezier in p.get_cubic_bezier_tuples():
            np.testing.assert_allclose(bezier[1], bezier[0] + (bezier[-1] - bezier[0]) / 3)
            np.testing.assert_allclose(bezier[2], bezier[0] + 2 * (bezier[-1] - bezier[0]) / 3)

    def test_crossing_from_outside_uses_true_intersections(self):
        p = self.plot([-1, 2], [-.25, 1.25])
        np.testing.assert_allclose(p.get_start(), [0, .25, 0])
        np.testing.assert_allclose(p.get_end(), [1, .75, 0])

    def test_excursion_above_window_has_no_false_flat_cap(self):
        p = self.plot([0, .5, 1], [0, 2, 0])
        paths = p.get_subpaths()
        self.assertEqual(len(paths), 2)
        np.testing.assert_array_equal(paths[0][-1], [.25, 1, 0])
        np.testing.assert_array_equal(paths[1][0], [.75, 1, 0])
        self.assertEqual(len(p.get_cubic_bezier_tuples()), 2)

    def test_nan_gap_and_isolated_visible_vertices_are_not_bridged(self):
        p = self.plot([0, .2, np.nan, .8, 1], [.2, .3, np.nan, .7, .8])
        self.assertEqual(len(p.get_subpaths()), 2)
        singles = self.plot([.2, np.nan, .8], [.3, np.nan, .7])
        self.assertEqual(len(singles.get_subpaths()), 2)
        np.testing.assert_array_equal(singles.get_start_anchors(), [[.2, .3, 0], [.8, .7, 0]])

    def test_boundary_parallel_and_corner_contacts(self):
        self.assertEqual(len(self.plot([-1, 2], [2, 2]).points), 0)
        p = self.plot([0, 1], [1, 1])
        np.testing.assert_array_equal(p.get_start(), [0, 1, 0])
        np.testing.assert_array_equal(p.get_end(), [1, 1, 0])
        p = self.plot([-1, 1], [1, -1])
        np.testing.assert_array_equal(p.get_start(), [0, 0, 0])
        np.testing.assert_array_equal(p.get_end(), [0, 0, 0])

    def test_mixed_run_lengths_keep_original_path_order(self):
        p = self.plot([0, .1, np.nan, .5, np.nan, .8, 1],
                      [.1, .2, np.nan, .5, np.nan, .7, .9])
        np.testing.assert_array_equal(p.get_start_anchors(),
                                      [[0, .1, 0], [.5, .5, 0], [.8, .7, 0]])

    def test_empty_singleton_and_invalid_contracts(self):
        self.assertEqual(len(self.plot([], []).points), 0)
        self.assertEqual(len(self.plot([2], [2]).points), 0)
        np.testing.assert_array_equal(self.plot([.2], [.4]).get_start(), [.2, .4, 0])
        with self.assertRaises(ValueError):
            self.plot([0, 1], [0])
        with self.assertRaises(ValueError):
            clipped_curve(IdentityAxes(), [0, 1], [0, 1], x_bounds=(1, 0), y_bounds=(0, 1), color="white")

    def test_unclipped_endpoint_does_not_lose_bits_on_reconstruction(self):
        a, b = (1e16, .25), (1., .75)
        start, end, lo, hi = _clip_segment(a, b, (0, 2e16), (0, 1))
        self.assertEqual((lo, hi), (0, 1))
        self.assertIs(start, a)
        self.assertIs(end, b)
        self.assertEqual(end[0], 1.)

    def test_nonnegative_density_polyline_cannot_spline_below_zero(self):
        p = self.plot([0, .3, .31, .5, 1], [0, 0, .98, .5, .05])
        self.assertTrue((p.points[:, 1] >= 0).all())
        for bezier in p.get_cubic_bezier_tuples():
            for t in np.linspace(0, 1, 17):
                value = (1-t)**3 * bezier[0] + 3*(1-t)**2*t*bezier[1] + 3*(1-t)*t*t*bezier[2] + t**3*bezier[3]
                self.assertGreaterEqual(value[1], 0)

    def test_actual_bell_caller_retains_sampled_vertices_without_smoothing_or_cap(self):
        source = Path(__file__).resolve().parents[1] / "videos/ai/ai5/s02_bell.py"
        tree = ast.parse(source.read_text())
        convolution = next(n for n in ast.walk(tree)
                           if isinstance(n, ast.FunctionDef) and n.name == "convolution")
        shapes = next(n for n in convolution.body if isinstance(n, ast.Assign)
                      and any(isinstance(t, ast.Name) and t.id == "shapes" for t in n.targets))
        axes = IdentityAxes()
        # Include a discontinuity and a genuine outside excursion: only real
        # line/rectangle intersections may replace the unavailable vertices.
        env = {"clipped_curve": clipped_curve, "ax2": axes,
               "zg": np.array([-4., -1.01, -1., 0., 1., 4.]),
               "dens": np.array([[0., 0., .99, .37, .14, .01],
                                  [0., .2, 1.4, .4, .2, .01]]), "DATA": "#7FD3FF"}
        exec(compile(ast.Module([shapes], type_ignores=[]), "actual-Bell-density-caller", "exec"), env)
        for shape in env["shapes"]:
            self.assertTrue((shape.points[:, 1] >= 0).all())
            self.assertTrue((shape.points[:, 1] <= 1).all())
        np.testing.assert_array_equal(env["shapes"][0].get_end_anchors(),
                                      np.column_stack([env["zg"][1:], env["dens"][0, 1:], np.zeros(5)]))
        self.assertEqual(len(env["shapes"][1].get_subpaths()), 2)


if __name__ == "__main__":
    unittest.main()
