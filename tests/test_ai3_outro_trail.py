"""Actual Manim interpolation of Outro's local smooth trail, without scene/data imports."""

import ast
import math
from pathlib import Path
from types import SimpleNamespace
import unittest

import numpy as np
from manim import Create, Dot, DOWN, MoveAlongPath, Scene, UpdateFromAlphaFunc, VGroup, VMobject


SOURCE = Path(__file__).resolve().parents[1] / "videos/ai/ai3/s19_outro.py"
TREE = ast.parse(SOURCE.read_text())
HELPER = next(n for n in TREE.body if isinstance(n, ast.FunctionDef) and n.name == "smooth_trail_reveal")
scope = {"UpdateFromAlphaFunc": UpdateFromAlphaFunc, "VGroup": VGroup}
exec(compile(ast.Module([HELPER], type_ignores=[]), str(SOURCE), "exec"), scope)
smooth_trail_reveal = scope["smooth_trail_reveal"]


def actual_trail():
    """Extract only the tiny illustrative path recipe; no scene/producer/load execution."""
    method = next(n for n in ast.walk(TREE) if isinstance(n, ast.FunctionDef) and n.name == "next_time")
    nodes = []
    for n in method.body:
        if isinstance(n, ast.FunctionDef) and n.name == "grad":
            nodes.append(n)
        elif isinstance(n, ast.Assign) and any(
            isinstance(t, ast.Tuple) and any(isinstance(x, ast.Name) and x.id == "path" for x in t.elts)
            or isinstance(t, ast.Name) and t.id == "trail" for t in n.targets
        ):
            nodes.append(n)
        elif isinstance(n, ast.For):
            nodes.append(n)
    namespace = {"np": np, "math": math, "VMobject": VMobject, "WHITE": "#ffffff", "DOWN": DOWN}
    exec(compile(ast.Module(nodes, type_ignores=[]), str(SOURCE), "exec"), namespace)
    return namespace["trail"]


class OutroTrailTests(unittest.TestCase):
    def test_every_encoded_alpha_matches_create_and_dot_tracks_same_prefix(self):
        path = actual_trail()
        full = path.copy()
        original_controls = full.points.copy()
        marker = Dot(full.get_start())
        animation = smooth_trail_reveal(path, marker)
        reference = full.copy()
        create = Create(reference)
        self.assertIs(animation.rate_func, create.rate_func)
        animation.begin()
        create.begin()
        # Original 3-second, 15-fps animation samples, explicit terminal state,
        # then a dense/nonmonotonic sweep to detect accidental mutable feedback.
        alphas = [*np.arange(45) / 45, 1.0, *np.linspace(1, 0, 201), 0.137, 1.0]
        for alpha in alphas:
            with self.subTest(alpha=float(alpha)):
                animation.interpolate(float(alpha))
                create.interpolate(float(alpha))
                np.testing.assert_array_equal(path.points, reference.points)
                np.testing.assert_allclose(marker.get_center(), path.get_end(), rtol=0, atol=2e-14)
                np.testing.assert_array_equal(full.points, original_controls)
        np.testing.assert_array_equal(path.points, original_controls)
        self.assertEqual(path.get_stroke_color(), full.get_stroke_color())
        self.assertEqual(path.get_stroke_width(), full.get_stroke_width())

    def test_copy_only_arc_length_motion_does_not_match_actual_smooth_prefix(self):
        path = actual_trail()
        full = path.copy()
        create = Create(path)
        marker = Dot(full.get_start())
        move = MoveAlongPath(marker, full.copy())
        create.begin()
        move.begin()
        separations = []
        for alpha in np.arange(45) / 45:
            create.interpolate(float(alpha))
            move.interpolate(float(alpha))
            separations.append(float(np.linalg.norm(marker.get_center() - path.get_end())))
        self.assertGreater(max(separations), 1.0)

    def test_both_objects_are_moving_for_cairo_static_cache(self):
        path = actual_trail()
        marker = Dot(path.get_start())
        animation = smooth_trail_reveal(path, marker)
        scene = Scene.__new__(Scene)
        scene.mobjects = [marker, path]
        scene.foreground_mobjects = []
        scene.renderer = SimpleNamespace(camera=SimpleNamespace(use_z_index=False))
        moving = scene.get_moving_mobjects(animation)
        self.assertIn(marker, moving)
        self.assertIn(path, moving)

    def test_scene_keeps_original_three_second_play_and_uses_coupled_family(self):
        method = next(n for n in ast.walk(TREE) if isinstance(n, ast.FunctionDef) and n.name == "next_time")
        plays = [n for n in ast.walk(method) if isinstance(n, ast.Call)
                 and isinstance(n.func, ast.Attribute) and n.func.attr == "play"
                 and any(isinstance(a, ast.Call) and isinstance(a.func, ast.Name)
                         and a.func.id == "smooth_trail_reveal" for a in n.args)]
        self.assertEqual(len(plays), 1)
        self.assertEqual(ast.literal_eval(next(k.value for k in plays[0].keywords if k.arg == "run_time")), 3.0)
        self.assertFalse(any(k.arg == "rate_func" for k in plays[0].keywords))
        self.assertFalse(any(isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
                             and n.func.id == "MoveAlongPath" for n in ast.walk(method)))


if __name__ == "__main__":
    unittest.main()
