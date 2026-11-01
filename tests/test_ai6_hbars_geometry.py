"""Quantitative chart regressions without scene/data-producer imports."""
import ast
from pathlib import Path
import unittest

import numpy as np
from manim import DOWN, LEFT, ORIGIN, RIGHT, GREY_A, VGroup, Rectangle, Text, Indicate, YELLOW

ROOT = Path(__file__).resolve().parents[1]


def hbars():
    tree = ast.parse((ROOT / "videos/ai/ai6/common.py").read_text())
    node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "hbars")
    # Actual geometric objects; plain text keeps this unit fixture independent of TeX availability.
    scope = dict(VGroup=VGroup, Rectangle=Rectangle, DOWN=DOWN, LEFT=LEFT, RIGHT=RIGHT, ORIGIN=ORIGIN,
                 GREY_A=GREY_A, label=Text, MathTex=Text)
    exec(compile(ast.Module([node], type_ignores=[]), "actual-ai6-hbars", "exec"), scope)
    return scope["hbars"]


class QuantitativeBars(unittest.TestCase):
    def test_unequal_label_widths_share_baseline_and_preserve_encoded_distances(self):
        values = [.73, .95, .81]
        chart = hbars()([("short", values[0], "#FF7700"),
                         ("a substantially longer label", values[1], "#33CCAA"),
                         ("middle", values[2], "#AA88EE")], width=3.6, lo=.7, hi=1.,
                        fmt=lambda v: f"{v:.3f}")
        np.testing.assert_allclose([r[1].get_left()[0] for r in chart], chart[0][1].get_left()[0], atol=1e-12)
        np.testing.assert_allclose([r[1].width for r in chart], 3.6 * (np.array(values) - .7) / .3, atol=1e-12)
        for row in chart:
            self.assertAlmostEqual(row[1].get_left()[0] - row[0].get_right()[0], .2)
            self.assertAlmostEqual(row[2].get_left()[0] - row[1].get_right()[0], .12)
        self.assertTrue(all(chart[i][1].get_y() > chart[i + 1][1].get_y() for i in range(2)))

    def test_empty_rows_and_legacy_outside_range_lengths_remain_defined(self):
        self.assertEqual(len(hbars()([])), 0)
        chart = hbars()([("below", -.1, "#FF7700"), ("above", 1.2, "#33CCAA")], width=4.,
                        fmt=lambda v: f"{v:.2f}")
        np.testing.assert_allclose([r[1].width for r in chart], [.02, 4.8], atol=1e-12)
        self.assertAlmostEqual(chart[0][1].get_left()[0], chart[1][1].get_left()[0])

    def test_actual_variance_emphasis_keeps_bar_geometry_at_every_encoded_phase(self):
        tree = ast.parse((ROOT / "videos/ai/ai6/s03_gauss.py").read_text())
        call = next(n for n in ast.walk(tree) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
                    and n.func.id == "Indicate" and n.args and isinstance(n.args[0], ast.IfExp)
                    and isinstance(n.args[0].body, ast.Subscript)
                    and isinstance(n.args[0].body.value, ast.Name) and n.args[0].body.value.id == "vb")
        scale = next(ast.literal_eval(k.value) for k in call.keywords if k.arg == "scale_factor")
        chart = hbars()([("least squares", .0101, "#FF7700"), ("Theil Sen", .0067, "#33CCAA")],
                        width=3.4, hi=.0125, fmt=lambda v: f"{v:.4f}")
        row = chart[1]
        points = row[1].get_all_points().copy()
        animation = Indicate(row, color=YELLOW, scale_factor=scale)
        animation.begin()
        for alpha in np.linspace(0., 1., 16):
            animation.interpolate(alpha)
            np.testing.assert_allclose(row[1].get_all_points(), points, atol=1e-12)
        animation.finish()


if __name__ == "__main__":
    unittest.main()
