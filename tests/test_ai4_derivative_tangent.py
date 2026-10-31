"""Execute only the illustration's numeric/geometry AST; no scene/data imports."""
import ast
import math
from pathlib import Path
import unittest

import numpy as np


class Tracker:
    def __init__(self, value):
        self.value = value

    def get_value(self):
        return self.value


class Axes:
    def c2p(self, x, y):
        return np.array([x, y])


class Shape:
    def __init__(self, *points, **kwargs):
        self.points = points


def illustration():
    path = Path(__file__).resolve().parents[1] / 'videos/ai/ai4/s02_derivative.py'
    tree = ast.parse(path.read_text())
    scene = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == 'Derivative')
    method = next(n for n in scene.body if isinstance(n, ast.FunctionDef) and n.name == 'tangent')
    names = {'p0', 'h', 'k', 'crossings', 'x0', 'x1', 'tangent'}
    nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in ('s', 'ds')]
    for node in method.body:
        if isinstance(node, ast.Assign):
            assigned = {n.id for target in node.targets for n in ast.walk(target) if isinstance(n, ast.Name)}
            if assigned & names:
                nodes.append(node)
        elif isinstance(node, ast.FunctionDef) and node.name == 'samples':
            nodes.append(node)
    ns = dict(math=math, ax=Axes(), ValueTracker=Tracker, Line=Shape, Dot=Shape,
              VGroup=lambda *items: items, GRAD='orange', GREY_A='grey',
              C=type('Colors', (), {'SURPRISE': 'pink'}))
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(path), 'exec'), ns)
    return ns


class TangentIllustrationTests(unittest.TestCase):
    def test_line_has_actual_derivative_slope_and_stays_in_plot(self):
        ns = illustration()
        a, b = ns['tangent'].points
        self.assertAlmostEqual((b[1] - a[1]) / (b[0] - a[0]), -4 / math.log(2))
        for point in (a, b):
            self.assertGreaterEqual(point[0], .05 - 1e-12)
            self.assertLessEqual(point[0], .95 + 1e-12)
            self.assertGreaterEqual(point[1], -1e-12)
            self.assertLessEqual(point[1], 6 + 1e-12)

    def test_finite_step_distinguishes_curve_from_linear_prediction(self):
        ns = illustration()
        gap, actual, prediction = ns['samples']()
        np.testing.assert_allclose(actual.points[0], [.55, math.log2(1 / .55)])
        np.testing.assert_allclose(prediction.points[0], [.55, 2 - 1.2 / math.log(2)])
        self.assertGreater(actual.points[0][1] - prediction.points[0][1], .59)
        self.assertGreater(prediction.points[0][1], 0)
        np.testing.assert_allclose(gap.points[0], prediction.points[0])
        np.testing.assert_allclose(gap.points[1], actual.points[0])

    def test_error_shrinks_quadratically_while_tangent_stays_fixed(self):
        ns = illustration()
        line = [p.copy() for p in ns['tangent'].points]
        errors = []
        for step in (.30, .15, .075, .02, .004, .002):
            ns['h'].value = step
            _, actual, prediction = ns['samples']()
            errors.append(actual.points[0][1] - prediction.points[0][1])
            self.assertAlmostEqual(actual.points[0][0], prediction.points[0][0])
            np.testing.assert_allclose(ns['tangent'].points, line)
        self.assertTrue(all(a > b > 0 for a, b in zip(errors, errors[1:])))
        self.assertGreater(errors[-2] / errors[-1], 3.9)
        self.assertLess(errors[-2] / errors[-1], 4.1)


if __name__ == '__main__':
    unittest.main()
