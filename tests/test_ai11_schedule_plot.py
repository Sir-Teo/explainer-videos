"""Portable consumer AST checks with explicit synthetic in-memory arrays only.
No cache reads, scene/model/producer imports, generation, training or rendering.
"""
import ast
import json
from pathlib import Path
import re
from types import SimpleNamespace
import unittest

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
PART = ROOT / 'videos/ai/ai11'


def method(root, file, name):
    return next(n for n in ast.walk(ast.parse((root / 'videos/ai/ai11' / file).read_text()))
                if isinstance(n, ast.FunctionDef) and n.name == name)


def plot(file, name, s, root=ROOT):
    fn = method(root, file, name)
    target = 'lg' if name == 'ema' else 'cnt'
    stop = next(i for i, n in enumerate(fn.body) if isinstance(n, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == target for t in n.targets))
    seen = SimpleNamespace(lines=[], axes=[], trackers=[])

    class Group:
        def __init__(self):
            self.items = []

        def add(self, item):
            self.items.append(item)
            return self

    class Path:
        def __init__(self, **kw):
            pass

        def set_points_as_corners(self, points):
            self.points = np.asarray(points)
            return self

    def axes(x, y, **kw):
        seen.axes.append((x, y))
        return SimpleNamespace(ax=SimpleNamespace(c2p=lambda x, y: (float(x), float(y))))

    def draw(ax, xs, ys, *args):
        seen.lines.append((np.array(xs), np.array(ys)))

    def tracker(v):
        seen.trackers.append(v)
        return v

    scope = dict(np=np, load=lambda _: s, bits_axes=axes, ValueTracker=tracker,
                 VGroup=Group, VMobject=Path, growing=draw, curve=draw,
                 Dot=lambda point, **kw: point, CON='constant', COS='cosine',
                 WSD='wsd', EMA='ema', SF='sf')
    exec(compile(ast.Module(body=fn.body[:stop], type_ignores=[]), '<actual-consumer-plot-prefix>', 'exec'), scope)
    seen.scope = scope
    return seen


def caption(name, file, s):
    fn = method(ROOT, file, name)
    node = next(n.value for n in ast.walk(fn) if isinstance(n, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id in {'tag', 'note_'} for t in n.targets))
    return eval(compile(ast.Expression(node.func.value.args[0]), '<actual-caption-expression>', 'eval'), dict(s=s))


def synthetic():
    """Entirely synthetic in-memory examples; no model outcomes or cache reads."""
    s = dict(lr=.01, lengths=[1000, 2000, 4000], seeds=[0, 1])
    for sd in s['seeds']:
        for S in s['lengths']:
            xs = np.arange(0, S + 1, 100)
            s[f'cos_{S}_{sd}'] = np.column_stack([xs, 3 - xs / 10000 + sd / 100])
            bx = np.arange(int(.8*S) + 100, S + 1, 100)
            s[f'wsdcurve_{S}_{sd}'] = np.column_stack([bx, 2.8 - bx / 10000 + sd / 100])
            s[f'wsdquick_{S}_{sd}'] = 2.8 - S / 10000 + sd / 100
        xs = np.arange(0, 4001, 100)
        s[f'const_{sd}'] = np.column_stack([xs, 3 - xs / 20000 + sd / 100])
        s[f'ema_{sd}'] = np.column_stack([xs[1:], 2.95 - xs[1:] / 20000 + sd / 100])
        s[f'sf_{sd}'] = np.column_stack([xs, 3 - xs / 10000 + sd / 100])
    return s


class SchedulePlot(unittest.TestCase):
    def test_actual_schedule_ast_preserves_raw_late_curves_branch_points_and_all_bounds(self):
        s = synthetic()
        s['const_0'][0, 1] = 999
        s['wsdcurve_1000_0'][0, 1] = 12
        s['wsdcurve_2000_0'][0, 1] = .1
        seen = plot('s14_schedule.py', 'charmodel', s)
        self.assertEqual(seen.trackers, [0])
        self.assertEqual(seen.axes[0][0], [0, 4000])
        lo, hi = seen.axes[0][1]
        self.assertLess(lo, .1)
        self.assertGreater(hi, 12)
        self.assertLess(hi, 999)
        for key, (xs, ys) in zip(['const_0'] + [f'cos_{S}_0' for S in s['lengths']], seen.lines):
            expected = s[key][s[key][:, 0] >= 500]
            np.testing.assert_array_equal(np.column_stack([xs, ys]), expected)
            self.assertEqual(xs[0], 500)
            self.assertTrue(np.all((lo < ys) & (ys < hi)))
        for S, branch in zip(s['lengths'], seen.scope['brs'].items):
            start = [int(.8*S), np.interp(int(.8*S), s['const_0'][:, 0], s['const_0'][:, 1])]
            np.testing.assert_array_equal(branch.points, np.vstack([start, s[f'wsdcurve_{S}_0']]))
            self.assertTrue(np.all((lo < branch.points[:, 1]) & (branch.points[:, 1] < hi)))

    def test_actual_ema_ast_retains_all_four_raw_curves_and_wsd_outlier_in_bounds(self):
        s = synthetic()
        s['wsdcurve_4000_0'][0, 1] = 12
        s['wsdcurve_4000_0'] = np.vstack([[900, 999], s['wsdcurve_4000_0']])
        seen = plot('s15_free.py', 'ema', s)
        self.assertEqual(seen.axes[0][0], [1000, 4000])
        lo, hi = seen.axes[0][1]
        for key, (xs, ys) in zip(['const_0', 'ema_0', 'cos_4000_0', 'wsdcurve_4000_0'], seen.lines):
            np.testing.assert_array_equal(np.column_stack([xs, ys]), s[key][s[key][:, 0] >= 1000])
            self.assertTrue(np.all((lo < ys) & (ys < hi)))
        self.assertGreater(hi, 12)
        self.assertLess(hi, 999)

    def test_actual_sf_ast_keeps_all_six_raw_dots_both_seed_bounds_and_late_display(self):
        s = synthetic()
        s['sf_1'][10, 1] = .1
        s['sf_0'][0, 1] = 999
        s['wsdquick_1000_0'] = s['wsdquick_1000_1'] = 12
        seen = plot('s15_free.py', 'measure', s)
        self.assertEqual(seen.trackers, [0])
        self.assertEqual(seen.axes[0][0], [0, 4000])
        lo, hi = seen.axes[0][1]
        np.testing.assert_array_equal(np.column_stack(seen.lines[0]), s['sf_0'][s['sf_0'][:, 0] >= 500])
        expected = []
        for S in s['lengths']:
            expected.extend([(S, np.mean([s[f'cos_{S}_{sd}'][-1, 1] for sd in s['seeds']])),
                             (S, np.mean([s[f'wsdquick_{S}_{sd}'] for sd in s['seeds']]))])
        np.testing.assert_array_equal(seen.scope['pts'].items, expected)
        self.assertEqual(len(expected), 6)
        self.assertLess(lo, .1)
        self.assertGreater(hi, 12)
        self.assertLess(hi, 999)

    def test_actual_prefix_empty_before_500_then_interpolates_adjacent_finite_samples(self):
        class Line:
            def __init__(self, **kw): self.paths = []
            def start_new_path(self, p): self.paths.append([p])
            def add_points_as_corners(self, pts): self.paths[-1].extend(pts)
        fn = method(ROOT, 'common.py', 'curve_prefix')
        scope = dict(np=np, VMobject=Line)
        exec(compile(ast.Module(body=[fn], type_ignores=[]), '<actual-prefix-helper>', 'exec'), scope)
        f = scope['curve_prefix']
        ax = SimpleNamespace(c2p=lambda x, y: (float(x), float(y)))
        for t in [0, 100, 499.999]:
            self.assertEqual(f(ax, [500, 600], [4, 2], t, 'synthetic').paths, [])
        self.assertEqual(f(ax, [500, 600], [4, 2], 550, 'synthetic').paths[0][-1], (550, 3))
        paths = f(ax, [500, 600, 700, 800], [4, float('nan'), 2, 1], 750, 'synthetic').paths
        self.assertEqual(len(paths), 2)
        self.assertEqual(paths[0][-1], (500, 4))
        self.assertEqual(paths[1][-1], (750, 1.5))

    def test_production_caption_translation_preserves_numeric_domains_and_late_view_label(self):
        table = json.loads((PART / 'text_zh_add.json').read_text())
        for pat, rep in table['patterns']:
            re._parser.parse_template(rep, re.compile(pat))
        tree = ast.parse((ROOT / 'explainer/zh_text.py').read_text())
        names = {'translate', '_by_numbers'}
        assignments = {'_SPACE', '_NUM', '_TEXT_CMD'}
        nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in names
                 or isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id in assignments for t in n.targets)]
        scope = dict(re=re, lang=SimpleNamespace(LANG='zh'), _TABLE=table, _BY_NUMBERS=None)
        exec(compile(ast.Module(body=nodes, type_ignores=[]), '<actual-production-caption-translator>', 'exec'), scope)
        for rate in [.01, .004]:  # synthetic numeric formatting checks only
            s = synthetic()
            s['lr'] = rate
            for name, file in [('charmodel', 's14_schedule.py'), ('measure', 's15_free.py')]:
                en = caption(name, file, s)
                zh = scope['translate'](en)
                self.assertIn('losses shown from step $500$; earlier values omitted', en)
                self.assertIn('省略更早的值', zh)
                self.assertNotIn('losses shown', zh)
                self.assertEqual(re.findall(r'\$[^$]*\$', en), re.findall(r'\$[^$]*\$', zh))
                self.assertEqual(en.count('\\\\'), zh.count('\\\\'))
                scope['lang'].LANG = 'en'
                self.assertEqual(scope['translate'](en), en)
                scope['lang'].LANG = 'zh'


if __name__ == '__main__':
    unittest.main()
