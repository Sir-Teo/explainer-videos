"""Portable source/AST checks with explicitly synthetic in-memory fixtures only.
No private cache/baseline, scene/model imports, generation or rendering.
"""
import ast
from pathlib import Path
from types import SimpleNamespace
import unittest

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'videos/ai/ai11/s18_outro.py'


def tree(path=SOURCE):
    return ast.parse(path.read_text())


def raw_range(path=SOURCE):
    fn = next(n for n in tree(path).body if isinstance(n, ast.FunctionDef) and n.name == '_mini_range')
    ns = dict(np=np)
    exec(compile(ast.Module(body=[fn], type_ignores=[]), '<actual-mini-range>', 'exec'), ns)
    return ns['_mini_range']


def section(path, first, last):
    fn = next(n for n in ast.walk(tree(path)) if isinstance(n, ast.FunctionDef) and n.name == 'tiles')
    index = lambda name: next(i for i, n in enumerate(fn.body) if isinstance(n, ast.Assign)
                              and any(isinstance(t, ast.Name) and t.id == name for t in n.targets))
    return fn.body[index(first):index(last)]


def tile(number, data, path=SOURCE):
    seen = SimpleNamespace(axes=[], curves=[], paths=[])

    class Group:
        def __init__(self, *args):
            self.items = list(args)
        def add(self, item):
            self.items.append(item)
            return self

    class Path:
        def __init__(self, **kw):
            self.kw = kw
        def set_points_as_corners(self, points):
            self.points = np.asarray(points)
            seen.paths.append(self.points)
            return self

    def axes(xr, yr):
        ax = SimpleNamespace(x_range=xr, y_range=yr, c2p=lambda x, y: (float(x), float(y)))
        seen.axes.append(ax)
        return ax

    def curve(ax, xs, ys, *args):
        seen.curves.append((ax, np.asarray(xs), np.asarray(ys)))

    scope = dict(np=np, load=lambda _: data, axes=axes, curve=curve, VGroup=Group,
                 VMobject=Path, out=[], WHITE='white', OPT_COLORS={o: o for o in data.get('opts', [])},
                 SCHED_COLORS=dict(constant='constant', wsd='wsd'))
    if any(isinstance(n, ast.FunctionDef) and n.name == '_mini_range' for n in tree(path).body):
        scope['_mini_range'] = raw_range(path)
    nodes = section(path, 'rc', 's') if number == 6 else section(path, 's', 'q8')
    exec(compile(ast.Module(body=nodes, type_ignores=[]), '<actual-outro-tile-AST>', 'exec'), scope)
    seen.scope = scope
    return seen


def synthetic_race():
    # Deliberately not a scientific outcome fixture.
    data = dict(opts=['a', 'b', 'c'])
    for i, opt in enumerate(data['opts']):
        data[f'curves_{opt}'] = np.array([[[0, 999], [150, 4+i], [3000, 2+i/10]],
                                         [[0, 999], [150, 5+i], [3000, 2.1+i/10]],
                                         [[0, 999], [150, 6+i], [3000, 2.2+i/10]]], float)
    return data


def synthetic_schedule():
    # Deliberately not a scientific outcome fixture.
    xs = [0, 100, 800, 1000, 1600, 2000, 3200, 3900, 4000]
    data = dict(lengths=[1000, 2000, 4000], seeds=[0],
                const_0=np.column_stack([xs, [999, 8, 4, 3.8, 3.7, 3.6, 3.5, 3.4, 3.3]]))
    for S in data['lengths']:
        data[f'wsdcurve_{S}_0'] = np.array([[.8*S+100, 3], [S, .5]], float)
        data[f'wsdfinal_{S}_0'] = 3.5  # old range must not control the new data domain
    return data


class OutroMiniPlot(unittest.TestCase):
    def test_shared_raw_range_contains_constant_and_cross_series_outliers(self):
        f = raw_range()
        lo, hi = f([2, 3], [.1, 12])
        self.assertLess(lo, .1)
        self.assertGreater(hi, 12)
        lo, hi = f([4, 4], [4])
        self.assertLess(lo, 4)
        self.assertGreater(hi, 4)
        self.assertTrue(np.isfinite([lo, hi]).all())
        for bad in [[], [float('nan')], [float('inf')]]:
            with self.assertRaises(ValueError):
                f(bad)

    def test_race_uses_one_shared_range_and_unmodified_selected_medians(self):
        data = synthetic_race()
        seen = tile(6, data)
        self.assertEqual(len(seen.axes), 1)
        ax = seen.axes[0]
        self.assertEqual(tuple(ax.x_range), (0, 3000))
        lo, hi = ax.y_range
        self.assertLess(hi, 999)
        for o, (same, xs, ys) in zip(data['opts'], seen.curves):
            self.assertIs(same, ax)
            c = data[f'curves_{o}']
            np.testing.assert_array_equal(xs, c[0, 1:, 0])
            np.testing.assert_array_equal(ys, np.median(c[:, 1:, 1], axis=0))
            self.assertTrue(np.all((lo < ys) & (ys < hi)))

    def test_schedule_uses_one_shared_range_for_raw_trunk_branches_and_starts(self):
        data = synthetic_schedule()
        seen = tile(7, data)
        self.assertEqual(len(seen.axes), 1)
        ax = seen.axes[0]
        self.assertEqual(tuple(ax.x_range), (0, 4000))
        lo, hi = ax.y_range
        self.assertLess(lo, .5)
        self.assertGreater(hi, 8)
        self.assertLess(hi, 999)
        _, xs, ys = seen.curves[0]
        np.testing.assert_array_equal(np.column_stack([xs, ys]), data['const_0'][1:])
        for S, points in zip(data['lengths'], seen.paths):
            k0 = int(.8*S)
            start = [k0, np.interp(k0, data['const_0'][:, 0], data['const_0'][:, 1])]
            np.testing.assert_array_equal(points, np.vstack([start, data[f'wsdcurve_{S}_0']]))
            self.assertTrue(np.all((lo < points[:, 1]) & (points[:, 1] < hi)))


if __name__ == '__main__':
    unittest.main()
