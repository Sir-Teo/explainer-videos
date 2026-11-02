"""Portable source contracts and explicitly synthetic translation fixtures.
No scene/model imports, scientific cache reads, regeneration or rendering.
"""
import ast
import math
import json
from pathlib import Path
import re
import unittest
from test_ai11_source_repairs import method, voice, value, translator

PART = Path(__file__).resolve().parents[1] / 'videos/ai/ai11'


def assignment(file, fn, name, scope):
    node = next(n.value for n in ast.walk(method(file, fn))
                if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in n.targets))
    return value(node, **scope)


def fixtures():
    """Invented formatting inputs only; these are not measured model outcomes."""
    for held in (False, True):
        scope = dict(held=held)
        scope['said1'] = assignment('s02_gd.py', 'convex', 'said1', scope)
        yield 'GradientDescent', value(voice('s02_gd.py', 'convex'), **scope)
        scope = dict(held=held, ks=list(range(2000)), ratio=118.36)
        scope['said1'] = assignment('s03_momentum.py', 'nesterov', 'said1', scope)
        yield 'Momentum', value(voice('s03_momentum.py', 'nesterov'), **scope)
    for close in (False, True):
        scope = dict(close=close, slope=.89, rate=[.99899], rpred=[.999], i1000=0)
        for name in ('said2', 'said3'):
            scope[name] = assignment('s02_gd.py', 'measure', name, scope)
        yield 'GradientDescent', value(voice('s02_gd.py', 'measure'), **scope)
    scope = dict(sg=.89, sh=.58, sn=.46, it_g=2745, it_h=187, it_n=142,
                 rh=.9418, rhp=.9387, rn=.9702, rnp=.9684)
    scope['said2'] = assignment('s03_momentum.py', 'measure', 'said2', scope)
    yield 'Momentum', value(voice('s03_momentum.py', 'measure'), **scope)


class QuadraticMetrics(unittest.TestCase):
    def test_gap_and_root_mode_require_different_step_coefficients(self):
        # For an exact scalar geometric mode, square-root gap ratio is rho;
        # objective gap ratio is rho^2. Large-kappa coefficients differ by two.
        kappa = 10000
        rho = (math.sqrt(kappa) - 1) / (math.sqrt(kappa) + 1)
        count = math.log(1e6) / (-2 * math.log(rho))
        self.assertAlmostEqual(count, 345.3762507166141)
        nodes = ast.walk(method('s03_momentum.py', 'derive'))
        formulas = [n.value for n in nodes if isinstance(n, ast.Constant) and isinstance(n.value, str)]
        self.assertIn(r'\tfrac{\sqrt{\kappa}}{4}\,\ln(1/\varepsilon)', formulas)
        self.assertTrue(any('relative gap' in s and 'prefactors' in s for s in formulas))
        # Zero initial velocity at the lower repeated root has this exact form.
        eta = 4 / (math.sqrt(kappa) + 1)**2
        beta = rho**2
        x0, x1 = 1., 1. - eta
        x2 = (1 + beta - eta) * x1 - beta * x0
        exact = (1 + (1-rho)*2) * rho**2
        self.assertAlmostEqual(x2, exact)
        self.assertGreater(abs(x2*x2 - beta**2), .001)
        readme = (PART/'README.md').read_text()
        self.assertNotIn('f shrinks by β per step', readme)
        self.assertIn('not a per-step contraction or guaranteed finite count', readme)
        self.assertNotIn('f 每步乘以 β', readme)
        self.assertIn('不是每步收缩因子，也不是保证达到的有限步数', readme)
        self.assertIn('(1 + β − ηλ)² < 4β；等号处的实重根', readme)

    def test_current_and_alternate_metric_narration_translate_with_bookmarks(self):
        tr = translator()
        marks = lambda s: re.findall(r"<bookmark mark=['\"]([^'\"]+)['\"]/>", s)
        for scene, en in fixtures():
            with self.subTest(scene=scene, en=en):
                zh = tr(en)
                self.assertIsNotNone(zh, en)
                self.assertEqual(marks(en), marks(zh))
                self.assertNotRegex(zh, r'\{[^{}]+\}')
                if en.startswith('Check it.') or en.startswith('Back to'):
                    self.assertIn('square root of the gap', en)
                    self.assertIn('差距平方根', zh)
                if en.startswith('In 1983'):
                    self.assertIn('objective gap', en)
                    self.assertIn('目标差距', zh)

    def test_new_caption_math_does_not_escape_chinese_punctuation(self):
        additions = json.loads((PART/'text_zh_add.json').read_text())['strings']
        changed = {en:zh for en,zh in additions.items() if en.startswith(r'late $\sqrt{f-f^*}$')}
        self.assertEqual(len(changed), 2)
        for en, zh in changed.items():
            self.assertNotRegex(zh, r'\\[^\x00-\x7f]')
            self.assertIn(r'\sqrt{f-f^*}', zh)

    def test_quadratic_animation_waits_use_declared_bookmarks(self):
        # Check the public source itself: waiting for an undeclared bookmark can
        # break narration even when its translation preserves every marker.
        checked = 0
        for name in ('s02_gd.py', 's03_momentum.py'):
            tree = ast.parse((PART/name).read_text())
            for fn in (n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)):
                declared = {mark for n in ast.walk(fn)
                            if isinstance(n, ast.Constant) and isinstance(n.value, str)
                            for mark in re.findall(r"<bookmark mark=['\"]([^'\"]+)['\"]/>", n.value)}
                loop_values = {}
                for loop in (n for n in ast.walk(fn) if isinstance(n, ast.For)):
                    if (isinstance(loop.target, ast.Tuple) and len(loop.target.elts) == 2
                            and isinstance(loop.target.elts[1], ast.Name)
                            and isinstance(loop.iter, ast.Call) and isinstance(loop.iter.func, ast.Name)
                            and loop.iter.func.id == 'enumerate' and loop.iter.args
                            and isinstance(loop.iter.args[0], ast.Constant)
                            and isinstance(loop.iter.args[0].value, str)):
                        loop_values[loop.target.elts[1].id] = set(loop.iter.args[0].value)
                for call in (n for n in ast.walk(fn) if isinstance(n, ast.Call)
                             and isinstance(n.func, ast.Attribute) and n.func.attr == 'wait_until'):
                    self.assertTrue(call.args, (name, fn.name))
                    arg = call.args[0]
                    if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                        referenced = {arg.value}
                    else:
                        self.assertIsInstance(arg, ast.Name)
                        self.assertIn(arg.id, loop_values, (name, fn.name))
                        referenced = loop_values[arg.id]
                    self.assertTrue(referenced <= declared, (name, fn.name, referenced - declared))
                    checked += len(referenced)
        self.assertGreater(checked, 0)


if __name__ == '__main__':unittest.main()
