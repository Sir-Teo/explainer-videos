import itertools
import unittest
import warnings
import runpy
from pathlib import Path

import numpy as np

from explainer.ai.viz import contour_segments

# Independent pre-repair fixture, never extracted from current production.
legacy = runpy.run_path(str(Path(__file__).with_name('fixtures') / 'contour_segments_legacy.py'))['contour_segments']


def edges(result):
    return {tuple(sorted((tuple((float(v) for v in p)) for p in pair))) for pair in result}

def degree(result):
    d = {}
    for pair in result:
        for p in pair:
            d[tuple(p)] = d.get(tuple(p), 0) + 1
    return d


class ContourSegmentsTests(unittest.TestCase):

    def test_confirmed_actual_helper_failure_and_vertical_repair(self):
        xy = np.array([-1.0, 0.0, 1.0])
        z = np.tile(xy, (3, 1))
        self.assertEqual(legacy(xy, xy, z, 0), [])
        self.assertEqual(edges(contour_segments(xy, xy, z, 0)), {((0.0, -1.0), (0.0, 0.0)), ((0.0, 0.0), (0.0, 1.0))})

    def test_horizontal_grid_line(self):
        xy = np.array([-1.0, 0.0, 1.0])
        z = np.tile(xy[:, None], (1, 3))
        self.assertEqual(len(contour_segments(xy, xy, z, 0)), 2)
        self.assertTrue(all((p[1] == 0 for s in contour_segments(xy, xy, z, 0) for p in s)))

    def test_diagonal_through_exact_vertices(self):
        xy = np.array([-1.0, 0.0, 1.0])
        z = xy[None, :] - xy[:, None]
        r = contour_segments(xy, xy, z, 0)
        self.assertEqual(edges(r), {((-1.0, -1.0), (0.0, 0.0)), ((0.0, 0.0), (1.0, 1.0))})

    def test_crossing_axes_four_valent_center(self):
        xy = np.array([-1.0, 0.0, 1.0])
        r = contour_segments(xy, xy, xy[:, None] * xy[None, :], 0)
        self.assertEqual(len(r), 4)
        self.assertEqual(degree(r)[0.0, 0.0], 4)

    def test_one_zero_vertex_continuing_curve(self):
        r = contour_segments([0.0, 1.0], [0.0, 1.0], np.array([[0.0, 1.0], [-1.0, 1.0]]), 0)
        self.assertEqual(edges(r), {((0.0, 0.0), (0.5, 1.0))})

    def test_zero_corner_isolated_from_separate_curve(self):
        r = contour_segments([0.0, 1.0], [0.0, 1.0], np.array([[0.0, 1.0], [1.0, -1.0]]), 0)
        self.assertEqual(edges(r), {((0.5, 1.0), (1.0, 0.5))})

    def test_isolated_corner_no_zero_length_segment(self):
        self.assertEqual(contour_segments([0.0, 1.0], [0.0, 1.0], np.array([[0.0, 1.0], [1.0, 1.0]]), 0), [])

    def test_two_opposite_isolated_vertices_not_false_diagonal(self):
        self.assertEqual(contour_segments([0.0, 1.0], [0.0, 1.0], np.array([[0.0, 1.0], [1.0, 0.0]]), 0), [])

    def test_zero_edge_transverse_branch_has_connected_t_junction(self):
        r = contour_segments([0.0, 1.0], [0.0, 1.0], np.array([[0.0, 0.0], [-1.0, 1.0]]), 0)
        self.assertEqual(edges(r), {((0.0, 0.0), (0.5, 0.0)), ((0.5, 0.0), (1.0, 0.0)), ((0.5, 0.0), (0.5, 1.0))})
        self.assertEqual(degree(r)[0.5, 0.0], 3)

    def test_shared_zero_edge_emitted_once(self):
        r = contour_segments([0.0, 1.0], [-1.0, 0.0, 1.0], np.array([[-1.0, 1.0], [0.0, 0.0], [-1.0, 1.0]]), 0)
        self.assertEqual(len(r), 4)
        self.assertEqual(degree(r)[0.5, 0.0], 4)

    def test_three_zero_corners_only_two_boundary_edges(self):
        r = contour_segments([0.0, 1.0], [0.0, 1.0], np.array([[0.0, 0.0], [0.0, 1.0]]), 0)
        self.assertEqual(edges(r), {((0.0, 0.0), (1.0, 0.0)), ((0.0, 0.0), (0.0, 1.0))})

    def test_flat_cell_preserves_legacy_no_contour(self):
        r = contour_segments([0.0, 1.0], [0.0, 1.0], np.zeros((2, 2)), 0)
        self.assertEqual(r, legacy([0.0, 1.0], [0.0, 1.0], np.zeros((2, 2)), 0))
        self.assertEqual(r, [])

    def test_flat_patch_suppresses_internal_cell_edges(self):
        xy = [0.0, 1.0, 2.0]
        r = contour_segments(xy, xy, np.zeros((3, 3)), 0)
        self.assertEqual(r, [])

    def test_plateau_adjacent_to_nonflat_cell_has_boundary(self):
        z = np.array([[0.0, 0.0, 1.0], [0.0, 0.0, 1.0]])
        r = contour_segments([0.0, 1.0, 2.0], [0.0, 1.0], z, 0)
        self.assertEqual(edges(r), {((1.0, 0.0), (1.0, 1.0))})

    def test_nonzero_ambiguous_saddles_keep_legacy_pairing(self):
        for z in [np.array([[1.0, -1.0], [-1.0, 1.0]]), np.array([[2.0, -3.0], [-4.0, 5.0]])]:
            self.assertEqual(contour_segments([0.0, 1.0], [0.0, 1.0], z, 0), legacy([0.0, 1.0], [0.0, 1.0], z, 0))

    def test_random_non_degenerate_output_values_and_order_exact(self):
        rng = np.random.default_rng(8631)
        for k in range(100):
            xs = np.linspace(-2, 3, 6)
            ys = np.linspace(-4, 1, 5)
            z = rng.normal(size=(5, 6))
            level = 0.12345
            self.assertEqual(contour_segments(xs, ys, z, level), legacy(xs, ys, z, level), k)

    def test_all_ternary_cell_patterns_unique_finite_nonzero_segments(self):
        for vals in itertools.product([-1.0, 0.0, 1.0], repeat=4):
            r = contour_segments([0.0, 1.0], [0.0, 1.0], np.array(vals).reshape(2, 2), 0)
            self.assertEqual(len(r), len(edges(r)))
            self.assertTrue(np.isfinite(r).all())
            self.assertTrue(all((a != b for a, b in r)))
            for a, b in r:
                for x, y in [a, b]:
                    z = np.array(vals).reshape(2, 2)
                    v = (1 - x) * (1 - y) * z[0, 0] + x * (1 - y) * z[0, 1] + x * y * z[1, 1] + (1 - x) * y * z[1, 0]
                    self.assertAlmostEqual(v, 0)

    def test_sign_reversal_same_degenerate_geometry(self):
        for vals in itertools.product([-1.0, 0.0, 1.0], repeat=4):
            if 0 not in vals:
                continue
            z = np.array(vals).reshape(2, 2)
            self.assertEqual(edges(contour_segments([0.0, 1.0], [0.0, 1.0], z, 0)), edges(contour_segments([0.0, 1.0], [0.0, 1.0], -z, 0)))

    def test_positive_affine_values_and_levels_keep_geometry(self):
        z = np.array([[0.0, 0.0], [-1.0, 1.0]])
        self.assertEqual(edges(contour_segments([0.0, 1.0], [0.0, 1.0], z, 0)), edges(contour_segments([0.0, 1.0], [0.0, 1.0], 3 * z + 7, 7)))

    def test_finite_extreme_signs_do_not_overflow_geometry(self):
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', RuntimeWarning)
            r = contour_segments([0.0, 1.0], [0.0, 1.0], np.array([[-1e+308, 1e+308], [-1e+308, 1e+308]]), 0)
        self.assertEqual(edges(r), {((0.5, 0.0), (0.5, 1.0))})

    def test_tiny_opposite_values_do_not_underflow_sign_product(self):
        z = np.array([[-1e-300, 1e-300], [-1e-300, 1e-300]])
        self.assertEqual(edges(contour_segments([0.0, 1.0], [0.0, 1.0], z, 0)), {((0.5, 0.0), (0.5, 1.0))})

    def test_nonfinite_values_level_or_axes_rejected(self):
        for bad in [np.nan, np.inf, -np.inf]:
            for args in [([0.0, 1.0], [0.0, 1.0], [[0.0, bad], [1.0, 2.0]], 0), ([0.0, bad], [0.0, 1.0], [[0.0, 1.0], [1.0, 2.0]], 0), ([0.0, 1.0], [0.0, 1.0], [[0.0, 1.0], [1.0, 2.0]], bad)]:
                with self.assertRaises(ValueError):
                    contour_segments(*args)

    def test_malformed_axes_shapes_complex_and_level_rejected(self):
        for args in [([1.0, 0.0], [0.0, 1.0], np.zeros((2, 2)), 0), ([0.0, 0.0], [0.0, 1.0], np.zeros((2, 2)), 0), ([0.0], [0.0, 1.0], np.zeros((2, 1)), 0), ([0.0, 1.0], [0.0, 1.0], np.zeros((3, 2)), 0), ([0.0, 1.0], [0.0, 1.0], np.zeros((2, 2), complex), 0), ([0.0, 1.0], [0.0, 1.0], np.zeros((2, 2)), [0])]:
            with self.assertRaises(ValueError):
                contour_segments(*args)

    def test_closed_circle_through_four_level_vertices(self):
        xy = np.array([-1.0, 0.0, 1.0])
        z = xy[None, :] ** 2 + xy[:, None] ** 2
        r = contour_segments(xy, xy, z, 1)
        self.assertEqual(len(r), 4)
        self.assertEqual(set(degree(r).values()), {2})
        self.assertEqual(set(degree(r)), {(-1.0, 0.0), (1.0, 0.0), (0.0, -1.0), (0.0, 1.0)})

    def test_large_int64_axis_real_crossing_uses_float_geometry_without_wrap(self):
        xy = np.array([-2 ** 62, 2 ** 62], dtype=np.int64)
        r = contour_segments(xy, [0.0, 1.0], np.array([[-1.0, 1.0], [-1.0, 1.0]]), 0)
        self.assertEqual(edges(r), {((0.0, 0.0), (0.0, 1.0))})
        self.assertTrue(all((np.isfinite(v) for s in r for p in s for v in p)))

    def test_integer_axes_unrepresentable_as_float64_rejected_honestly(self):
        for xs in [np.array([2 ** 60, 2 ** 60 + 1], dtype=np.int64), np.array([-2 ** 63, 2 ** 63 - 1], dtype=np.int64)]:
            with self.assertRaisesRegex(ValueError, 'exactly representable'):
                contour_segments(xs, [0.0, 1.0], np.array([[-1.0, 1.0], [-1.0, 1.0]]), 0)

    def test_partial_plateau_with_transverse_branch_keeps_only_interface(self):
        z = np.array([[0.0, 0.0, -1.0], [0.0, 0.0, 1.0]])
        r = contour_segments([0.0, 1.0, 2.0], [0.0, 1.0], z, 0)
        self.assertEqual(edges(r), {((1.0, 0.0), (1.0, 0.5)), ((1.0, 0.5), (1.0, 1.0)), ((1.0, 0.5), (2.0, 0.5))})
        self.assertEqual(degree(r)[1.0, 0.5], 3)

    def test_inputs_unmodified(self):
        x = np.array([0.0, 1.0])
        z = np.array([[0.0, 0.0], [-1.0, 1.0]])
        before = z.copy()
        contour_segments(x, x, z, 0)
        np.testing.assert_array_equal(z, before)
        np.testing.assert_array_equal(x, [0.0, 1.0])
if __name__ == '__main__':
    unittest.main(verbosity=2)
