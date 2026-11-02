"""Actual source AST and translator checks with tiny synthetic stubs only.
No repository scene/producer/model imports, cache reads, generation or training.
"""
import ast
import contextlib
import hashlib
import io
import json
import math
from pathlib import Path
import re
from types import SimpleNamespace
import unittest

import numpy as np
from test_ai11_source_repairs import method, translator, value, voice

ROOT = Path(__file__).resolve().parents[1]
PART = ROOT / 'videos/ai/ai11'


def assign(file, fn, name, scope):
    node = next(n.value for n in ast.walk(method(file, fn))
                if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in n.targets))
    return value(node, **scope)


def branch(file, fn, name, scope):
    node = next(n for n in method(file, fn).body if isinstance(n, ast.If)
                and any(isinstance(q, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name
                       for t in q.targets) for q in ast.walk(n)))
    scope = dict(scope)
    exec(compile(ast.Module(body=[node], type_ignores=[]), '<actual-isolated-consumer-branch>', 'exec'), scope)
    return scope[name]


class RaceProtocol(unittest.TestCase):
    def test_actual_adaptive_control_flow_caps_extensions_and_reuses_seed_zero(self):
        # Extract actual constants and control flow, replacing all scientific work
        # with tiny in-memory synthetic records. No producer module is imported.
        tree = ast.parse((PART / 'compute.py').read_text())
        nodes = [n for n in tree.body if isinstance(n, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id in {'RACE_OPTS', '_A', 'RACE_LRS', 'RACE_STEPS_N',
                                               'RACE_WRITE', 'RACE_SEEDS'} for t in n.targets)]
        nodes += [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'compute_race']
        for mode, total, edge in [('interior', 48, False), ('high', 66, True), ('low', 66, True)]:
            calls, piece = [], {}
            scope = dict(np=np)

            def pieces(part, jobs, ignored):
                for key, (opt, rate, seed) in jobs.items():
                    if key in part:
                        continue
                    calls.append((opt, rate, seed))
                    target = scope['RACE_LRS'][opt][2]
                    final = ((math.log2(rate / target)) ** 2 if mode == 'interior'
                             else -rate if mode == 'high' else rate)
                    part[key] = dict(final=final, curve=[[0, 5.0], [3000, 2.0]], ms=1.0,
                                     writes={str(k): 'synthetic' for k in scope['RACE_WRITE']})

            scope.update(CACHE=SimpleNamespace(partial=lambda *args: piece),
                         _run_pieces=pieces, _race_job=object())
            exec(compile(ast.Module(body=nodes, type_ignores=[]), '<isolated-actual-race-control>', 'exec'), scope)
            with contextlib.redirect_stdout(io.StringIO()):
                result = scope['compute_race']()
            self.assertEqual(len(calls), total)
            self.assertEqual(len(calls), len(set(calls)))
            for opt in scope['RACE_OPTS']:
                self.assertEqual(result['edge_' + opt], edge)
                self.assertEqual(sum(o == opt and seed > 0 for o, lr, seed in calls), 2)
                self.assertEqual(len(result['lrs_' + opt]), 6 if not edge else 9)
            self.assertEqual(total * scope['RACE_STEPS_N'], 144000 if not edge else 198000)

    def test_timing_boundaries_and_metric_domains_are_actual_producer_semantics(self):
        fn = method('charopt.py', 'train')
        defaults = dict(zip([a.arg for a in fn.args.args][-len(fn.args.defaults):], fn.args.defaults))
        self.assertEqual(ast.literal_eval(defaults['final_n']), 100000)
        self.assertEqual(ast.unparse(defaults['eval_n']), 'EVAL_N')
        self.assertEqual(ast.literal_eval(defaults['eval_every']), 150)
        body = fn.body
        start = next(i for i, n in enumerate(body) if isinstance(n, ast.Assign)
                     and any(isinstance(t, ast.Name) and t.id == 't0' for t in n.targets))
        loop_index = next(i for i, n in enumerate(body) if isinstance(n, ast.For)
                          and isinstance(n.target, ast.Name) and n.target.id == 'k')
        timing = next(i for i, n in enumerate(body) if isinstance(n, ast.Assign)
                      and isinstance(n.targets[0], ast.Subscript) and ast.unparse(n.targets[0]) == "out['ms']")
        self.assertLess(start, loop_index)
        self.assertLess(loop_index, timing)
        initial = ast.unparse(ast.Module(body=body[:start], type_ignores=[]))
        timed = ast.unparse(body[loop_index])
        after = ast.unparse(ast.Module(body=body[timing + 1:], type_ignores=[]))
        self.assertIn('bits(model, eval_n)', initial)
        self.assertIn('write(model)', initial)
        self.assertIn('bits(model, eval_n)', timed)
        self.assertIn('write(model)', timed)
        self.assertIn('bits(model, final_n)', after)
        end_node = next(n.value for n in method('charopt.py', 'bits').body
                        if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name)
                        and n.targets[0].id == 'end')
        scope = dict(va=[None] * 100000, CTX=8)
        self.assertEqual(value(end_node, n=20000, **scope) - 8, 20000)
        self.assertEqual(value(end_node, n=100000, **scope) - 8, 99992)
        # Actual producer aggregation: a mean of run timings, not a run's time.
        mean_node = next(n for n in ast.walk(method('compute.py', 'compute_race'))
                         if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Subscript)
                         and ast.unparse(n.targets[0]) == "out[f'ms_{o}']")
        env = dict(np=np, o='soap', runs=[dict(ms=x) for x in [1.0, 3.0, 8.0]], out={})
        exec(compile(ast.Module(body=[mean_node], type_ignores=[]), '<actual-timing-mean>', 'exec'), env)
        self.assertEqual(env['out']['ms_soap'], 4.0)

    def test_reading_role_and_interpolation_use_actual_ast(self):
        standings = [('sgdm', 1, 1, 1), ('muon', 2, 2, 2), ('soap', 3, 3, 3)]
        for ordered, comparison in [(standings, 'muon'), (standings[1:] + standings[:1], 'muon')]:
            names = assign('s13_race.py', 'reading', 'names', dict(st=ordered))
            self.assertEqual(names, ['sgdm', comparison])
        fn = method('s13_race.py', 'reading')
        loop = next(n for n in fn.body if isinstance(n, ast.For) and ast.unparse(n.target) == 'n')
        curves = np.array([[[0, 10], [150, 7], [300, 6], [900, 4], [1050, 3], [3000, 2]]], float)
        env = dict(np=np, names=['sgdm', 'soap'], steps=[0, 100, 300, 1000, 3000], bits_at={},
                   r={'curves_sgdm': curves, 'curves_soap': curves})
        exec(compile(ast.Module(body=[loop], type_ignores=[]), '<actual-reading-interpolation>', 'exec'), env)
        np.testing.assert_allclose(env['bits_at']['soap'], [10, 8, 6, 10 / 3, 2])
        source = ast.unparse(fn)
        self.assertIn('bits interpolated from the validation curve', source)
        self.assertIn('best non-SGD comparison', source)
        self.assertNotIn('and the winner,', source)

    def test_branch_translation_and_bookmarks_without_saved_computed_fixtures(self):
        tr = translator()
        cases = [value(voice('s13_race.py', 'rules'))]
        say = dict(sgdm='SGD with momentum', soap='SOAP', muon='Muon', adamw='AdamW', lion='Lion')
        for sep in [True, False]:
            scope = dict(sep=sep, SAY=say, w='soap', wm=2.1, s2='muon',
                         last=('lion', 3.0, 2.9, 3.1), aw=('adamw', 2.4, 2.3, 2.5))
            scope['verdict'] = branch('s13_race.py', 'replay', 'verdict', scope)
            scope['rel'] = assign('s13_race.py', 'replay', 'rel', scope)
            if sep:
                self.assertIn('two observed three-seed ranges', scope['verdict'])
                self.assertNotIn('luck', scope['verdict'])
            cases.append(value(voice('s13_race.py', 'replay'), **scope))
        for edges in [[], ['soap'], ['soap', 'muon']]:
            scope = dict(edges=edges, SAY=say)
            scope['etxt'] = assign('s13_race.py', 'sweeps', 'etxt', scope)
            cases.append(value(voice('s13_race.py', 'sweeps'), **scope))
        for ahead in [True, False]:
            scope = dict(ahead=ahead, SAY=say, names=['sgdm', 'soap'], b0=[8.1], b1=[2.3],
                         steps=[0, 100, 300, 1000, 3000])
            scope['said1'] = assign('s13_race.py', 'reading', 'said1', scope)
            cases.append(value(voice('s13_race.py', 'reading'), **scope))
        cost = value(voice('s13_race.py', 'cost'), mu=1.2, sh=1.4)
        self.assertIn("each optimizer's mean timed-loop wall time per step across three seeds", cost)
        cases.append(cost)
        for hf, hs in [(2.0, 3.0), (3.0, 2.0)]:
            scope = dict(hf=hf, hs=hs, mx_s=123.0, mx_f=456.0)
            scope['said1'] = assign('s16_stability.py', 'logits', 'said1', scope)
            en = value(voice('s16_stability.py', 'logits'), **scope)
            self.assertIn('differences between scores', en)
            self.assertIn('Raw maxima alone', en)
            self.assertNotIn('heads stop learning', en)
            cases.append(en)
        marks = lambda s: re.findall(r"<bookmark mark=['\"]([^'\"]+)['\"]/>", s)
        for en in cases:
            with self.subTest(en=en):
                zh = tr(en)
                self.assertIsNotNone(zh)
                self.assertEqual(marks(en), marks(zh))
                self.assertNotRegex(zh, r'\{[^{}]+\}')
                self.assertNotIn('interpolated', zh)
                self.assertNotIn('Raw maxima', zh)

    def test_new_caption_keys_cover_actual_source_literals(self):
        table = json.loads((PART / 'text_zh_add.json').read_text())['strings']
        source = ast.parse((PART / 's13_race.py').read_text())
        values = [n.value for n in ast.walk(source) if isinstance(n, ast.Constant) and isinstance(n.value, str)]
        selected = [text for text in values if text.startswith((
            'each optimizer:', 'full validation slice', 'curves: first $20{,}000$',
            'seed $0$ texts', 'mean loop time per step', 'includes validation and $4$'))]
        self.assertEqual(len(selected), 7)
        for text in selected:
            self.assertIn(text, table)
            self.assertTrue(table[text])



if __name__ == '__main__':
    unittest.main()
