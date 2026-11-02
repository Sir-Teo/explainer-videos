"""Synthetic source checks; no scene imports, scientific caches, TTS or renderer."""
import ast
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
PART = ROOT / 'videos/ai/ai11'


def method(file, name):
    tree = ast.parse((PART / file).read_text())
    return next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == name)


def voice(file, name):
    return next(n.args[0] for n in ast.walk(method(file, name))
                if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                and n.func.attr == 'voiceover')


def value(node, **scope):
    return eval(compile(ast.Expression(node), '<actual-part11-expression>', 'eval'), scope)


def translator():
    # The real translation matcher only needs a path resolver. Avoid importing
    # explainer.__init__, which loads Manim, by compiling its own source here.
    tree = ast.parse((ROOT / 'explainer/zh_templates.py').read_text())
    tree.body = [n for n in tree.body
                 if not (isinstance(n, ast.ImportFrom) and n.module == 'explainer.paths')]
    scope = {'video_dir': lambda name: PART}
    exec(compile(tree, '<actual-translation-matcher>', 'exec'), scope)
    return scope['Translator']('ai11')


class Part11Repairs(unittest.TestCase):
    def test_natural_replay_never_rewinds_and_syncs_both_maps_and_counter(self):
        fn = method('s09_natural.py', 'race')
        body = next(n for n in fn.body if isinstance(n, ast.With)).body
        start = next(i for i, n in enumerate(body)
                     if isinstance(n, ast.Expr) and isinstance(n.value, ast.Call)
                     and isinstance(n.value.func, ast.Attribute)
                     and n.value.func.attr == 'wait_until'
                     and n.value.args[0].value == 'a')
        nodes = body[start:]
        self.assertFalse(any(isinstance(n, (ast.Import, ast.ImportFrom))
                             for node in nodes for n in ast.walk(node)))
        snap_node = next(n.value for n in ast.parse((PART / 'nets.py').read_text()).body
                         if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name)
                         and n.targets[0].id == 'NG_SNAP')
        snaps = ast.literal_eval(snap_node)
        state = {'step': 0, 'counter': 0, 'maps': {'gd:0', 'ng:0'}}
        events, bookmarks = [], []

        class Tracker:
            @property
            def animate(self):
                return self

            def set_value(self, step):
                return ('step', step)

        class Scene:
            def play(self, *animations, **kw):
                for kind, payload in animations:
                    if kind in ('step', 'counter'):
                        state[kind] = payload
                    elif kind == 'in':
                        state['maps'].add(payload)
                    elif kind == 'out':
                        state['maps'].remove(payload)
                events.append((dict(state, maps=set(state['maps'])), kw['run_time']))

        class Voice:
            def wait_until(self, mark):
                bookmarks.append((mark, state['step']))

        scope = dict(self=Scene(), vo=Voice(), t=Tracker(), stp='counter', snaps=snaps,
                     k100=100, T=300, live=[], linear='linear',
                     maps={o: [f'{o}:{k}' for k in range(len(snaps))] for o in ('gd', 'ng')},
                     FadeIn=lambda obj: ('in', obj), FadeOut=lambda obj: ('out', obj),
                     ChangeDecimalToValue=lambda obj, step: ('counter', step))
        exec(compile(ast.Module(body=nodes, type_ignores=[]), '<actual-replay>', 'exec'), scope)
        steps = [0] + [s['step'] for s, _ in events]
        self.assertEqual(steps, [0, 10, 30, 100, 300, 300])
        self.assertEqual(steps, sorted(steps))
        for s, _ in events:
            index = snaps.index(s['step'])
            self.assertEqual(s['maps'], {f'gd:{index}', f'ng:{index}'})
            self.assertEqual(s['counter'], s['step'])
        self.assertEqual(bookmarks, [('a', 0), ('b', 100), ('c', 300)])
        self.assertAlmostEqual(sum(duration for _, duration in events), 3 + 4 * 1.2 + 1)

    def test_actual_newton_polynomial_has_negative_signed_error(self):
        tree = ast.parse((PART / 'charopt.py').read_text())
        coeffs = next(ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign)
                      and isinstance(n.targets[0], ast.Name) and n.targets[0].id == 'NS_EXACT')
        fn = next(n for n in ast.parse((PART / 's12_newton.py').read_text()).body
                  if isinstance(n, ast.FunctionDef) and n.name == 'poly')
        scope = {}
        exec(compile(ast.Module(body=[fn], type_ignores=[]), '<actual-polynomial>', 'exec'), scope)
        q = scope['poly'](tuple(F(str(v)) for v in coeffs))
        for e in [F(1, 1000), F(-1, 1000), F(1, 10000)]:
            signed = 1 - q(1 - e)
            exact = -e**2 / 2 + 7 * e**3 / 2 - 5 * e**4 / 2 + e**5 / 2
            self.assertEqual(signed, exact)
            self.assertLess(signed, 0)
            self.assertLess(abs(signed / e**2 + F(1, 2)), F(1, 250))
        readme = (PART / 'README.md').read_text()
        self.assertIn('c = −1/2', readme)
        self.assertNotIn('c = 1/2', readme)
        captions = json.loads((PART / 'text_zh_add.json').read_text())['strings']
        self.assertTrue(any(r'e \mapsto -e^2/2' in en and r'e \mapsto -e^2/2' in zh
                            for en, zh in captions.items()))

    def test_correlated_equilibrium_and_orthogonal_model_are_distinct(self):
        # Deterministic covariance algebra, not an experiment or AdamW result.
        eta, decay, beta, u2 = F(1, 10), F(1, 2), F(3, 5), F(7, 3)
        a = 1 - eta * decay
        exact = eta**2 * u2 * (1 + a * beta) / ((1 - a**2) * (1 - a * beta))
        # The stationary cross term follows from the same autocorrelation.
        cross = -eta * u2 * beta / (1 - a * beta)
        self.assertEqual(exact, a**2 * exact - 2 * a * eta * cross + eta**2 * u2)
        orthogonal = eta**2 * u2 / (1 - a**2)
        self.assertNotEqual(exact, orthogonal)
        for epsilon in [F(1, 1000), F(1, 10000)]:
            a = 1 - epsilon
            factor = (1 + a * beta) / ((2 - epsilon) * (1 - a * beta))
            limit = (1 + beta) / (2 * (1 - beta))
            self.assertLess(abs(factor / limit - 1), 4 * epsilon / (1 - beta))
        question = next(n.args[0].elts[-1].value for n in ast.walk(method('s18_outro.py', 'problems'))
                        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == 'problem_set')
        self.assertIn('stationary zero-mean', question)
        self.assertIn(r'\mathbb{E}\langle u_t, u_{t+k}\rangle', question)
        self.assertIn(r'\eta\lambda \ll 1 - \beta', question)
        self.assertNotIn(r'u_t \perp W_t', question)

    def test_corrected_narration_translates_current_fixtures_and_keeps_bookmarks(self):
        tr = translator()
        marks = lambda s: re.findall(r"<bookmark mark=['\"]([^'\"]+)['\"]/>", s)
        cases = [value(voice('s12_newton.py', 'polys')),
                 value(voice('s16_stability.py', 'equilibrium'))]
        for measured_bits in [7.5, 8.1]:
            for said1 in ['its interpolated loss is lower at every shown trained checkpoint.',
                          'compare the sampled continuations at these checkpoints.']:
                en = value(voice('s13_race.py', 'reading'), SAY={'soap': 'SOAP'}, names=['sgdm', 'soap'],
                           b0=[measured_bits], b1=[2.2], steps=[0, 100, 300, 1000, 3000], said1=said1)
                self.assertNotIn('equally likely', en)
                self.assertIn(f'random model scores {measured_bits:.1f} bits per character', en)
                cases.append(en)
        for en in cases:
            zh = tr(en)
            self.assertIsNotNone(zh, en)
            self.assertEqual(marks(en), marks(zh))
            self.assertNotRegex(zh, r'\{[^{}]+\}')
        current = json.loads((PART / 'narration_zh.json').read_text())['lines']
        # Static corrected lines retain exact records; computed Race lines above
        # test translator coverage only, without inventing a measured cache fixture.
        for en in cases[:2]:
            key = hashlib.sha1(' '.join(en.split()).encode()).hexdigest()[:12]
            self.assertEqual(current[key]['en'], en)
            self.assertEqual(current[key]['zh'], tr(en))


if __name__ == '__main__':
    unittest.main()
