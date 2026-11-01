"""Small mathematical counterexamples tied to Part7's displayed/narrated claims.

No scene imports, corpus loading, training, or cache access.
"""
import ast
import itertools
import math
from pathlib import Path
import unittest

import numpy as np

ROOT = Path(__file__).resolve().parents[1] / 'videos/ai/ai7'


def method(file, name):
    return next(n for n in ast.walk(ast.parse((ROOT / file).read_text()))
                if isinstance(n, ast.FunctionDef) and n.name == name)


def assignment(fn, name):
    return next(n.value for n in ast.walk(fn) if isinstance(n, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == name for t in n.targets))


def evaluate(node, **scope):
    return eval(compile(ast.Expression(node), 'actual-scene-expression', 'eval'), dict(np=np, **scope))


def voiceovers(fn):
    return [n.args[0] for n in ast.walk(fn) if isinstance(n, ast.Call)
            and isinstance(n.func, ast.Attribute) and n.func.attr == 'voiceover']


class CountingSceneClaims(unittest.TestCase):
    def test_model1_equation_normalizes_for_fixed_target_length_only(self):
        eq = next(n for n in ast.walk(method('s09_translation.py', 'model1'))
                  if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == 'cmath')
        terms = [ast.literal_eval(n) for n in eq.args]
        self.assertEqual(terms[:3], [r'P(e \mid f,m)', '=', r'\frac{1}{(\ell+1)^m}'])
        # Two normalized lexical rows: NULL plus one source position. Summing
        # every target string at any fixed m needs the displayed 2**(-m) factor.
        table = np.array([[.8, .2], [.1, .9]])
        for m in range(1, 5):
            raw = sum(math.prod(table[:, w].sum() for w in out)
                      for out in itertools.product(range(2), repeat=m))
            self.assertAlmostEqual(raw, 2 ** m)
            self.assertAlmostEqual(raw / 2 ** m, 1.)
        # Fixed-length distributions still require a length prior to combine
        # different lengths; otherwise their total is one per length.
        self.assertAlmostEqual(sum(2. ** (-m - 1) for m in range(100)), 1.)

    def test_transition_updates_count_departures_not_terminal_visits(self):
        fn = method('s08_baumwelch.py', 'derive')
        rows = assignment(fn, 'rows')
        transition = ast.literal_eval(rows.elts[-1].args[2])
        self.assertEqual(transition, r'\frac{\sum_{t<T} \xi_t(i, j)}{\sum_{t<T} \gamma_t(i)}')
        gamma = np.array([[.8, .2], [.3, .7], [.6, .4]])
        xi = np.array([[[.2, .6], [.1, .1]], [[.2, .1], [.4, .3]]])
        np.testing.assert_allclose(xi.sum(2), gamma[:-1])
        correct = xi.sum(0) / gamma[:-1].sum(0)[:, None]
        np.testing.assert_allclose(correct.sum(1), 1.)
        wrong = xi.sum(0) / gamma.sum(0)[:, None]
        self.assertTrue(np.all(wrong.sum(1) < 1.))
        derive = evaluate(voiceovers(fn)[0])
        self.assertIn('cannot decrease', derive)
        self.assertIn('fixed point', derive)

    def test_two_directional_transition_rates_are_not_one_alternation_rate(self):
        fn = method('s08_baumwelch.py', 'learn')
        line = evaluate(voiceovers(fn)[-1], partition_voice='Different letter preferences.',
                        A=np.array([[.1, .9], [.2, .8]]))
        self.assertIn('second 90 percent', line)
        self.assertIn('first, 20 percent', line)
        self.assertIn('two directional probabilities', line)
        # Their stationary-weighted switching rate would be ~32.7%, neither
        # displayed direction. It must not be narrated as the first direction.
        stationary = np.array([.2, .9]) / 1.1
        self.assertAlmostEqual(stationary @ np.array([.9, .2]), .36 / 1.1)

    def test_infini_cap_can_stop_before_context_disappears(self):
        source = ast.parse((ROOT / 'infini.py').read_text())
        scope = {'np': np, '__name__': 'synthetic-infini-proof'}
        exec(compile(source, 'actual-small-infini', 'exec'), scope)
        a = np.ones(620, np.uint8)
        sa = scope['suffix_array'](a, log=lambda *_: None)
        index = scope['Index'](a, sa)
        lengths = []
        L, lo, hi = index.longest(a, 610, cap=500, lengths=lengths)
        self.assertEqual(L, 500)
        self.assertGreater(index.count(bytes(np.ones(501, np.uint8))), 0)
        self.assertGreater(hi - lo, 1)
        fn = method('s11_infini.py', 'grow')
        for count in (1, 121):
            last = evaluate(assignment(fn, 'last'), counts=[count])
            self.assertNotIn('vanish', last)
        result = method('s11_infini.py', 'result')
        caption = next(n for n in ast.walk(assignment(result, 'en_'))
                       if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == 'label').args[0]
        text = evaluate(caption, n_bands=7)
        self.assertIn('$7$ length bands', text)
        self.assertIn('$2$ types', text)
        self.assertIn('one or several distinct next characters', text)

    def test_kn_context_order_and_trend_follow_the_measured_case(self):
        fn = method('s10_kn.py', 'orders')
        trend = assignment(fn, 'trend')
        nonmonotone = evaluate(trend, kn=np.array([3., 2., 2.3]))
        self.assertIn('does not improve every measured order', nonmonotone)
        monotone = evaluate(trend, kn=np.array([3., 2., 1.9]))
        self.assertIn('Across these measured orders', monotone)
        line = evaluate(voiceovers(method('s10_kn.py', 'board'))[0],
                        k={'best': 3, 'best_bits': 2.123})
        self.assertIn('With 3 characters', line)
        self.assertIn('selected on the validation books', line)
        self.assertIn('why stop at 3 characters', line)

    def test_viterbi_is_joint_map_and_forward_event_includes_the_space(self):
        compute = ast.parse((ROOT / 'compute.py').read_text())
        fn = next(n for n in compute.body if isinstance(n, ast.FunctionDef) and n.name == 'viterbi')
        scope = {'np': np}
        exec(compile(ast.Module([fn], type_ignores=[]), 'actual-viterbi-only', 'exec'), scope)
        # Search a fixed tiny family for the distinction between a best whole
        # path and independently optimal states. Exhaustive only 16 paths/case.
        g = np.random.default_rng(2801)
        found = False
        for _ in range(100):
            A, B, pi = g.dirichlet(np.ones(2), 2), g.dirichlet(np.ones(2), 2), g.dirichlet(np.ones(2))
            obs = [0, 1, 0, 1]
            paths = list(itertools.product(range(2), repeat=4))
            weights = np.array([pi[s[0]] * B[s[0], obs[0]] * math.prod(
                A[s[t-1], s[t]] * B[s[t], obs[t]] for t in range(1, 4)) for s in paths])
            marginal = np.zeros((4, 2))
            for path, p in zip(paths, weights / weights.sum()):
                for t, state in enumerate(path):
                    marginal[t, state] += p
            joint = list(paths[int(weights.argmax())])
            self.assertEqual(scope['viterbi'](np.array(obs), A, B, pi), joint)
            if joint != marginal.argmax(1).tolist():
                found = True
                break
        self.assertTrue(found)
        res = assignment(method('s07_hmm.py', 'forward'), 'res')
        self.assertIn(r'\sqcup', ast.unparse(res))
        decode = evaluate(voiceovers(method('s07_hmm.py', 'decode'))[0])
        self.assertIn('complete hidden-state sequence', decode)


if __name__ == '__main__':
    unittest.main()
