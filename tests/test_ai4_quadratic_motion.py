"""Actual Manim interpolation of the local trajectory reveal, without a scene render."""

import ast
from pathlib import Path
from types import SimpleNamespace
import unittest

import numpy as np
from manim import Create, Dot, Scene, UpdateFromAlphaFunc, VGroup, VMobject, linear, smooth


SOURCE = Path(__file__).resolve().parents[1] / "videos/ai/ai4/s15_quadratic.py"
node = next(n for n in ast.parse(SOURCE.read_text()).body
            if isinstance(n, ast.FunctionDef) and n.name == "trajectory_reveal")
namespace = {"np": np, "math": __import__("math"), "UpdateFromAlphaFunc": UpdateFromAlphaFunc, "VGroup": VGroup}
exec(compile(ast.Module([node], type_ignores=[]), str(SOURCE), "exec"), namespace)
trajectory_reveal = namespace["trajectory_reveal"]


class TrajectoryRevealTests(unittest.TestCase):
    def animation(self, vertices, rate=linear):
        path = VMobject(color="#ff9933", stroke_width=4).set_points_as_corners(vertices)
        original = path.copy()
        dot = Dot(original.get_start(), radius=0.08, color="#ff9933")
        animation = trajectory_reveal(path, dot)
        animation.rate_func = rate
        animation.begin()
        return path, original, dot, animation

    def assert_coupled(self, path, dot):
        np.testing.assert_allclose(dot.get_center(), path.get_end(), rtol=0, atol=2e-14)

    def test_unequal_segments_use_arc_length_not_curve_index(self):
        path, original, dot, animation = self.animation([[0, 0, 0], [10, 0, 0], [10, 1, 0]])
        animation.interpolate(0.5)
        np.testing.assert_allclose(path.get_end(), [5.5, 0, 0], atol=1e-13)
        self.assert_coupled(path, dot)
        animation.interpolate(10 / 11)
        np.testing.assert_allclose(path.get_end(), [10, 0, 0], atol=1e-13)
        animation.interpolate(0.95)
        np.testing.assert_allclose(path.get_end(), [10, 0.45, 0], atol=1e-13)
        self.assert_coupled(path, dot)

    def test_dense_interpolation_preserves_corners_and_visible_length(self):
        vertices = np.array([[0, 0, 0], [7, 0, 0], [7, 2, 0], [8, 2, 0]], float)
        path, original, dot, animation = self.animation(vertices)
        for alpha in np.linspace(0, 1, 201):
            animation.interpolate(alpha)
            self.assert_coupled(path, dot)
            curves = path.get_cubic_bezier_tuples()
            distance = sum(np.linalg.norm(c[-1] - c[0]) for c in curves)
            self.assertAlmostEqual(distance, 10 * alpha, places=11)
            for vertex, boundary in [(vertices[1], 0.7), (vertices[2], 0.9)]:
                if alpha > boundary:
                    self.assertTrue(any(np.array_equal(vertex, c[-1]) for c in curves[:-1]))
        np.testing.assert_array_equal(path.points, original.points)
        self.assertEqual(path.get_stroke_color(), original.get_stroke_color())
        self.assertEqual(path.get_stroke_width(), original.get_stroke_width())

    def test_zero_length_segments_and_stationary_trajectory(self):
        for vertices in [
            [[0, 0, 0], [0, 0, 0], [3, 0, 0], [3, 0, 0], [3, 2, 0], [3, 2, 0]],
            [[2, -1, 0], [2, -1, 0], [2, -1, 0]],
        ]:
            path, original, dot, animation = self.animation(vertices)
            total = sum(np.linalg.norm(b - a) for a, b in zip(np.array(vertices), np.array(vertices)[1:]))
            for alpha in np.linspace(0, 1, 101):
                animation.interpolate(alpha)
                self.assertTrue(np.isfinite(path.points).all())
                self.assert_coupled(path, dot)
                actual = sum(np.linalg.norm(c[-1] - c[0]) for c in path.get_cubic_bezier_tuples())
                self.assertAlmostEqual(actual, total * alpha, places=12)
            np.testing.assert_array_equal(path.points, original.points)

    def test_endpoints_and_default_smooth_rate_are_retained(self):
        vertices = [[-4.5, 0.9, 0], [0, 0, 0]]
        path, original, dot, animation = self.animation(vertices, smooth)
        self.assertIs(animation.rate_func, Create(original).rate_func)
        for alpha in [0, 0.2, 0.4, 0.8, 1]:
            animation.interpolate(alpha)
            expected = np.array(vertices[0]) + smooth(alpha) * (np.array(vertices[-1]) - vertices[0])
            np.testing.assert_allclose(path.get_end(), expected, atol=2e-14)
            self.assert_coupled(path, dot)

    def test_dot_is_in_animated_family_for_cairo_static_cache(self):
        path, original, dot, animation = self.animation([[0, 0, 0], [2, 0, 0]])
        scene = Scene.__new__(Scene)
        scene.mobjects = [dot, path]
        scene.foreground_mobjects = []
        scene.renderer = SimpleNamespace(camera=SimpleNamespace(use_z_index=False))
        moving = scene.get_moving_mobjects(animation)
        self.assertIn(dot, moving)
        self.assertIn(path, moving)

    def test_rejects_empty_or_nonuniform_curved_geometry(self):
        with self.assertRaises(ValueError):
            trajectory_reveal(VMobject(), Dot())
        curved = VMobject().set_points([[0, 0, 0], [0, 1, 0], [1, 1, 0], [1, 0, 0]])
        with self.assertRaises(ValueError):
            trajectory_reveal(curved, Dot())


if __name__ == "__main__":
    unittest.main()
