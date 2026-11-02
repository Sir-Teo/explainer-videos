"""Portable consumer AST tests with explicit synthetic in-memory fixtures only.
No scientific caches, scene/model imports, training, rendering, or data generation.
Fixture values are invented only to exercise plotting branches.
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


def method(path, name):
    return next(n for n in ast.walk(ast.parse(path.read_text()))
                if isinstance(n, ast.FunctionDef) and n.name == name)


def synthetic_data():
    """Invented values, not optimizer measurements; three seeds per curve."""
    steps = [0, 150, 300, 900, 3000]
    values = {
        'synthetic_a': [[999, 4.0, 3.5, 3.0, 2.5], [999, 4.4, 3.9, 3.2, 2.6], [999, 4.1, 3.6, 3.1, 2.55]],
        'synthetic_b': [[999, 4.2, 3.8, 3.1, 2.4], [999, 4.6, 3.7, 3.3, 2.5], [999, 4.3, 3.9, 3.2, 2.45]],
        'synthetic_c': [[999, 4.1, 3.6, 3.2, 2.7], [999, 4.5, 3.8, 3.4, 2.8], [999, 4.2, 3.7, 3.3, 2.75]],
        'synthetic_d': [[999, 4.0, 3.4, 2.9, 2.3], [999, 4.3, 3.6, 3.0, 2.4], [999, 4.1, 3.5, 2.95, 2.35]],
        'synthetic_e': [[999, 3.9, 3.3, 2.8, 2.2], [999, 4.2, 3.5, 2.9, 2.3], [999, 4.0, 3.4, 2.85, 2.25]],
        'synthetic_f': [[999, 4.3, 3.9, 3.4, 2.8], [999, 4.5, 4.0, 3.6, 2.9], [999, 4.4, 3.95, 3.5, 2.85]],
    }
    result = {'opts': list(values)}
    for name, seeds in values.items():
        result[f'curves_{name}'] = np.array([list(zip(steps, ys)) for ys in seeds], dtype=float)
    return result


def prefix(r):
    fn = method(PART / 's13_race.py', 'replay')
    stop = next(i for i, n in enumerate(fn.body) if isinstance(n, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == 'cnt' for t in n.targets))
    seen = SimpleNamespace(lines=[], bands=[], axes=[], trackers=[])

    class Group:
        def add(self, *args):
            return self

    def axes(x, y, **kw):
        seen.axes.append((x, y))
        return SimpleNamespace(ax=object())

    def tracker(v):
        seen.trackers.append(v)
        return v

    def growing(ax, xs, ys, *args):
        seen.lines.append((np.array(xs), np.array(ys)))

    def band(ax, xs, lo, hi, *args):
        seen.bands.append((np.array(xs), np.array(lo), np.array(hi)))

    scope = dict(np=np, load=lambda _: r, bits_axes=axes, ValueTracker=tracker,
                 VGroup=Group, growing=growing, band=band,
                 OPT_COLORS={o: o for o in r['opts']})
    exec(compile(ast.Module(body=fn.body[:stop], type_ignores=[]), '<actual-replay-prefix>', 'exec'), scope)
    return seen


class Line:
    def __init__(self, **kw):
        self.paths = []

    def start_new_path(self, p):
        self.paths.append([p])

    def add_points_as_corners(self, pts):
        self.paths[-1].extend(pts)


def replay_prefix():
    fn = method(PART / 'common.py', 'curve_prefix')
    scope = dict(np=np, VMobject=Line)
    exec(compile(ast.Module(body=[fn], type_ignores=[]), '<actual-part11-prefix-helper>', 'exec'), scope)
    return scope['curve_prefix']


class RacePlot(unittest.TestCase):
    def test_actual_ast_passes_synthetic_retained_medians_and_bands_unmodified(self):
        r = synthetic_data()
        before = {k: v.copy() for k, v in r.items() if isinstance(v, np.ndarray)}
        seen = prefix(r)
        self.assertEqual(len(seen.lines), len(r['opts']))
        self.assertEqual(len(seen.bands), len(r['opts']))
        self.assertEqual(seen.trackers, [0])
        self.assertEqual(seen.axes[0][0], [0, 3000])
        lo, hi = seen.axes[0][1]
        retained = []
        for i, o in enumerate(r['opts']):
            c = r[f'curves_{o}']
            xs, med = seen.lines[i]
            np.testing.assert_array_equal(xs, c[0, 1:, 0])
            np.testing.assert_array_equal(med, np.median(c[:, 1:, 1], axis=0))
            bx, lower, upper = seen.bands[i]
            np.testing.assert_array_equal(bx, xs)
            np.testing.assert_array_equal(lower, c[:, 1:, 1].min(0))
            np.testing.assert_array_equal(upper, c[:, 1:, 1].max(0))
            self.assertEqual(xs[0], 150)
            retained.extend(c[:, 1:, 1].ravel())
        self.assertLess(lo, min(retained))
        self.assertGreater(hi, max(retained))
        self.assertGreaterEqual(hi - lo, 1.6)
        self.assertLess(hi, 999)
        for key, value in before.items():
            np.testing.assert_array_equal(r[key], value)

    def test_synthetic_intermediate_seed_outliers_determine_bounds_not_initial_or_only_final(self):
        c = np.array([[[0, 999], [150, 3], [300, 2.5], [3000, 2]],
                      [[0, 999], [150, 9], [300, -1], [3000, 2]],
                      [[0, 999], [150, 3], [300, 2.5], [3000, 2]]], float)
        seen = prefix(dict(opts=['synthetic'], curves_synthetic=c))
        lo, hi = seen.axes[0][1]
        self.assertLess(lo, -1)
        self.assertGreater(hi, 9)
        self.assertLess(hi, 999)
        self.assertEqual(seen.bands[0][2][0], 9)
        self.assertEqual(seen.bands[0][1][1], -1)
        np.testing.assert_array_equal(seen.lines[0][1], [3, 2.5, 2])
        small = c.copy()
        small[:, 1:, 1] = 2
        low, high = prefix(dict(opts=['synthetic'], curves_synthetic=small)).axes[0][1]
        self.assertAlmostEqual(high - low, 1.6)
        # X domain comes from retained observations, not a hard-coded run length.
        short = c.copy()
        short[:, -1, 0] = 750
        self.assertEqual(prefix(dict(opts=['synthetic'], curves_synthetic=short)).axes[0][0], [0, 750])

    def test_actual_helper_empty_before_150_interpolates_only_after_first_observation(self):
        f = replay_prefix()
        ax = SimpleNamespace(c2p=lambda x, y: (float(x), float(y)))
        for t in [0, 1, 149.999]:
            self.assertEqual(f(ax, [150, 300], [4, 2], t, 'synthetic').paths, [])
        self.assertEqual(f(ax, [150, 300], [4, 2], 150, 'synthetic').paths[0][-1], (150, 4))
        self.assertEqual(f(ax, [150, 300], [4, 2], 225, 'synthetic').paths[0][-1], (225, 3))
        paths = f(ax, [150, 300, 450, 600], [4, float('nan'), 2, 1], 525, 'synthetic').paths
        self.assertEqual(len(paths), 2)
        self.assertEqual(paths[0][-1], (150, 4))
        self.assertEqual(paths[1][-1], (525, 1.5))

    def test_actual_growing_wrapper_reads_current_tracker_and_preserves_transform(self):
        f = replay_prefix()
        callbacks = []
        fn = method(PART / 'common.py', 'growing')
        scope = dict(ValueTracker=object, curve_prefix=f, always_redraw=lambda callback: callbacks.append(callback))
        exec(compile(ast.Module(body=[fn], type_ignores=[]), '<actual-growing-wrapper>', 'exec'), scope)
        ax = SimpleNamespace(c2p=lambda x, y: (float(x), float(y)))
        tracker = SimpleNamespace(value=0)
        tracker.get_value = lambda: tracker.value
        scope['growing'](ax, [150, 300], [4, 2], tracker, 'synthetic', 2, lambda y: y * 2)
        self.assertEqual(len(callbacks), 1)
        self.assertEqual(callbacks[0]().paths, [])
        tracker.value = 225
        self.assertEqual(callbacks[0]().paths[0][-1], (225, 6))
        tracker.value = 300
        self.assertEqual(callbacks[0]().paths[0][-1], (300, 4))

    def test_actual_replay_reveals_full_bands_after_tracker_finishes(self):
        fn = method(PART / 's13_race.py', 'replay')
        voice = next(n for n in fn.body if isinstance(n, ast.With))
        statements = [ast.unparse(n) for n in voice.body]
        finish = next(i for i, s in enumerate(statements) if 't.animate.set_value(S)' in s)
        reveal = next(i for i, s in enumerate(statements) if 'FadeIn(bands)' in s)
        self.assertLess(finish, reveal)

    def test_actual_caption_production_exact_match_preserves_math_and_backslashes(self):
        src = method(PART / 's13_race.py', 'replay')
        text = next(n.value for n in ast.walk(src) if isinstance(n, ast.Constant)
                    and isinstance(n.value, str) and n.value.startswith('curves: first $20{,}000$'))
        table = json.loads((ROOT / 'videos/ai/ai_text_zh.json').read_text())
        local = json.loads((PART / 'text_zh_add.json').read_text())
        table.setdefault('strings', {}).update(local['strings'])
        self.assertIn('losses shown from step $150$; initial values omitted', text)
        self.assertIn('median of $3$ seeds', text)
        self.assertIn('band: \\ min to max', text)
        tree = ast.parse((ROOT / 'explainer/zh_text.py').read_text())
        fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'translate')
        space = next(n for n in tree.body if isinstance(n, ast.Assign)
                     and any(isinstance(t, ast.Name) and t.id == '_SPACE' for t in n.targets))
        scope = dict(re=re, lang=SimpleNamespace(LANG='zh'), _TABLE=table)
        exec(compile(ast.Module(body=[space, fn], type_ignores=[]), '<actual-production-caption-translate>', 'exec'), scope)
        zh = scope['translate'](text)
        self.assertEqual(zh, table['strings'][text])
        self.assertIn('省略初始值', zh)
        self.assertEqual(text.count('\\\\'), zh.count('\\\\'))
        self.assertEqual(re.findall(r'\$[^$]*\$', text), re.findall(r'\$[^$]*\$', zh))
        scope['lang'].LANG = 'en'
        self.assertEqual(scope['translate'](text), text)


if __name__ == '__main__':
    unittest.main()
