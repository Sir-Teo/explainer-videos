"""Portable display geometry checks; no scenes, producers or cached data imported."""
import ast
import itertools
import math
from pathlib import Path
import unittest

PART = Path(__file__).resolve().parent


def function(filename, name):
    node = next(n for n in ast.parse((PART / filename).read_text()).body
                if isinstance(n, ast.FunctionDef) and n.name == name)
    namespace = {'math': math}
    exec(compile(ast.Module(body=[node], type_ignores=[]), filename, 'exec'), namespace)
    return namespace[name]


lower = function('s04_hoeffding.py', '_segments_above_floor')
upper = function('s07_margins.py', '_segments_below_top')


class DisplayGeometry(unittest.TestCase):
    def test_visible_points_and_boundary_are_preserved(self):
        self.assertEqual(upper([0, 1, 2], [0, 1, 2], 2),
                         ([[(0.0, 0.0), (1.0, 1.0), (2.0, 2.0)]], []))
        self.assertEqual(lower([0, 1], [-5, -4], -5),
                         ([[(0.0, -5.0), (1.0, -4.0)]], []))

    def test_fully_hidden_curves_are_omitted(self):
        self.assertEqual(upper([0, 1], [3, 4], 2), ([], []))
        self.assertEqual(lower([0, 1], [-6, -7], -5), ([], []))

    def test_crossing_positions_are_interpolated(self):
        self.assertEqual(upper([0, 2], [3, 1], 2),
                         ([[(1.0, 2.0), (2.0, 1.0)]], [1.0]))
        self.assertEqual(upper([0, 2], [1, 3], 2),
                         ([[(0.0, 1.0), (1.0, 2.0)]], [1.0]))

    def test_hidden_excursions_do_not_become_false_plateaus(self):
        self.assertEqual(upper([0, 1, 2], [1, 3, 1], 2),
                         ([[(0.0, 1.0), (0.5, 2.0)], [(1.5, 2.0), (2.0, 1.0)]], [0.5, 1.5]))
        self.assertEqual(lower([0, 1, 2], [-4, -6, -4], -5),
                         ([[(0.0, -4.0), (0.5, -5.0)], [(1.5, -5.0), (2.0, -4.0)]], [0.5, 1.5]))

    def test_visible_trough_is_one_segment(self):
        self.assertEqual(upper([0, 1, 2], [3, 1, 3], 2),
                         ([[(0.5, 2.0), (1.0, 1.0), (1.5, 2.0)]], [0.5, 1.5]))

    def test_boundary_touch_does_not_duplicate_markers(self):
        self.assertEqual(upper([0, 1, 2], [3, 2, 3], 2), ([[(1.0, 2.0)]], [1.0]))

    def test_empty_and_nonfinite_inputs(self):
        for clip, boundary in [(upper, 2), (lower, -5)]:
            self.assertEqual(clip([], [], boundary), ([], []))
            for xs, ys, bound in [([0], [], boundary), ([0], [math.nan], boundary),
                                  ([math.inf], [1], boundary), ([0], [1], math.inf)]:
                with self.subTest(clip=clip.__name__, xs=xs, ys=ys, bound=bound):
                    with self.assertRaises(ValueError):
                        clip(xs, ys, bound)

    def test_lower_and_upper_clipping_agree_under_sign_inversion(self):
        for ys in itertools.product((-7, -5, -3), repeat=5):
            segments, crossings = upper(range(5), [-y for y in ys], 5)
            expected = [[(x, -y) for x, y in segment] for segment in segments], crossings
            self.assertEqual(lower(range(5), ys, -5), expected)


if __name__ == '__main__':
    unittest.main()
