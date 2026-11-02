"""Synthetic/static Part 13 contracts; no empirical inputs or scene/producer imports.

These checks cover mathematical text, selected protocol boundaries and bilingual
source templates. They do not certify rendered pixels, audio, or the gated
Smoother/Outro candidates. All numerical fixtures below are invented.
"""
import ast
import copy
import math
import json
from pathlib import Path
import re
import types
import unittest

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
PART = ROOT / 'videos/ai/ai13'


def tree(filename):
    return ast.parse((PART / filename).read_text())


def method(filename, name):
    return next(n for n in ast.walk(tree(filename))
                if isinstance(n, ast.FunctionDef) and n.name == name)


def assigned(fn, name, index=0):
    return [n.value for n in ast.walk(fn) if isinstance(n, ast.Assign)
            and any(isinstance(t, ast.Name) and t.id == name for t in n.targets)][index]


def voice(fn):
    return next(n.args[0] for n in ast.walk(fn) if isinstance(n, ast.Call)
                and isinstance(n.func, ast.Attribute) and n.func.attr == 'voiceover')


def evaluate(node, **env):
    return eval(compile(ast.Expression(node), '<synthetic-source-contract>', 'eval'),
                {'np': np, 'math': math, **env})


def strings(filename):
    return '\n'.join(n.value for n in ast.walk(tree(filename))
                     if isinstance(n, ast.Constant) and isinstance(n.value, str))


def translator():
    # Execute only the stdlib template engine; replace its part-table loader with
    # literal source tables. Reading source templates never imports a scene.
    engine = ast.parse((ROOT / 'explainer/zh_templates.py').read_text())
    engine.body = [n for n in engine.body if not (
        isinstance(n, ast.ImportFrom) and n.module == 'explainer.paths')]
    module = types.ModuleType('ai13_source_template_contract')
    module.video_dir = lambda _: PART
    exec(compile(engine, 'explainer/zh_templates.py', 'exec'), module.__dict__)
    tables = {'TITLE': '', 'CHAPTERS': {}, 'ZH': {}, 'PHRASES': {}}
    translation_tree = tree('zh_lines.py')
    helpers = {}
    for n in translation_tree.body:
        if isinstance(n, ast.FunctionDef) and n.name == '_spoken_lists':
            # The existing list enumerator imports itertools only, not a scene.
            imports = [x.module for x in ast.walk(n) if isinstance(x, ast.ImportFrom)]
            if imports != ['itertools']:
                raise AssertionError('Unexpected spoken-list helper imports')
            exec(compile(ast.Module(body=[n], type_ignores=[]), '<spoken-list-template>', 'exec'), helpers)
    for n in translation_tree.body:
        if isinstance(n, ast.Assign):
            for target in n.targets:
                if isinstance(target, ast.Name) and target.id in tables:
                    tables[target.id] = ast.literal_eval(n.value)
        elif (isinstance(n, ast.Expr) and isinstance(n.value, ast.Call)
              and isinstance(n.value.func, ast.Attribute)
              and isinstance(n.value.func.value, ast.Name)
              and n.value.func.value.id in tables and n.value.func.attr == 'update'):
            arg = n.value.args[0]
            if isinstance(arg, ast.Dict):
                addition = ast.literal_eval(arg)
            elif (isinstance(arg, ast.Call) and isinstance(arg.func, ast.Name)
                  and arg.func.id == '_spoken_lists' and not arg.args and not arg.keywords):
                addition = helpers['_spoken_lists']()
            else:
                raise AssertionError('Unexpected nonliteral translation-table update')
            tables[n.value.func.value.id].update(addition)
    module.table = lambda _: tables
    return module.Translator('ai13')


class MathematicalDisplay(unittest.TestCase):
    def test_sinusoidal_shift_has_explicit_arguments_and_correct_rotation(self):
        text = strings('s09_positions.py')
        self.assertIn(r'\sin((t+k)\omega)', text)
        self.assertIn(r'\cos((t+k)\omega)', text)
        t, k, omega = .7, -2., .43
        rotation = np.array([[math.cos(k*omega), math.sin(k*omega)],
                             [-math.sin(k*omega), math.cos(k*omega)]])
        np.testing.assert_allclose(rotation @ [math.sin(t*omega), math.cos(t*omega)],
                                   [math.sin((t+k)*omega), math.cos((t+k)*omega)], atol=1e-14)
        self.assertIn('unnormalized weights', text)
        self.assertIn('beyond that 1,024-entry table', text)

    def test_rope_signed_offset_is_conditional_on_fixed_vectors(self):
        text = strings('s10_rope.py')
        self.assertIn('fixed pre-RoPE', text)
        self.assertIn('signed offset', text)
        self.assertIn('not monotone', text)
        self.assertIn('equal energy', text)
        def rotation(x):
            return np.array([[math.cos(x), -math.sin(x)], [math.sin(x), math.cos(x)]])
        q, k = np.array([2., -1.]), np.array([.5, 3.])
        m, n, theta = 2., -3., .37
        self.assertAlmostEqual((rotation(m*theta)@q) @ (rotation(n*theta)@k),
                               q @ rotation((n-m)*theta) @ k)

    def test_saturation_is_a_finite_gradient_statement(self):
        self.assertIn('this gradient path', strings('s04_scale.py'))
        p = np.array([.999, .0007, .0003])
        jacobian = np.diag(p)-np.outer(p, p)
        np.testing.assert_allclose(jacobian.sum(1), 0., atol=1e-15)
        self.assertGreater(np.linalg.norm(jacobian), 0.)
        self.assertLess(np.linalg.norm(jacobian), .003)

    def test_hopfield_exact_pattern_curve_names_sign_readout(self):
        text = strings('s03_memory.py')
        for phrase in ['sign readout', 'continuous overlap', 'small-error, one-step',
                       'sufficiently separated', 'asymptotic capacity']:
            self.assertIn(phrase, text)
        modern = method('compute.py', 'modern')
        returns = [n.value for n in ast.walk(modern) if isinstance(n, ast.Return)]
        self.assertTrue(any(isinstance(n, ast.Call) and ast.unparse(n.func) == 'np.sign'
                            for n in returns))

    def test_heads_rank_energy_and_normalization_scopes(self):
        text = strings('s05_heads.py')
        for phrase in ['at most', 'squared singular values', 'pre-RoPE',
                       'not its offset or input-dependent rescaling']:
            self.assertIn(phrase, text)
        singular = np.array([5., 2., 1., 0.])
        energy = np.cumsum(singular**2) / np.sum(singular**2)
        self.assertNotEqual(np.searchsorted(energy, .9),
                            np.searchsorted(np.cumsum(singular)/singular.sum(), .9))

    def test_mask_measurement_is_raw_logits_and_combined_ablation(self):
        text = strings('s06_masks.py')
        self.assertIn('raw logits', text)
        self.assertIn('combined ablation', text)
        self.assertIn('generate with masked or iterative procedures', text)
        # This verifies the separation-lane animation's geometry contract, not pixels.
        order = method('s06_masks.py', 'order')
        source = ast.unparse(order)
        self.assertIn('card_=card_', source)
        self.assertIn('clear_updaters', source)
        times = [evaluate(k.value) for n in ast.walk(order) if isinstance(n, ast.Call)
                 and ast.unparse(n.func) == 'self.play' for k in n.keywords
                 if k.arg == 'run_time' and isinstance(k.value, ast.Constant)]
        self.assertTrue(any(times[i:i+3] == [.25, 1., .25] for i in range(len(times)-2)))
        self.assertGreater(1.1-.7, 0.)

    def test_differential_coefficients_can_be_negative_and_need_not_sum_to_one(self):
        text = strings('s13_sinks.py')
        for phrase in ['signed, not probabilities', 'mean feature openness',
                       'small final value, not a measured decrease', 'not whole-task equivalence']:
            self.assertIn(phrase, text)
        first = np.array([[.2, .8], [.6, .4]])
        second = np.array([[.7, .3], [.1, .9]])
        lam = .35
        coefficients = first-lam*second
        self.assertLess(coefficients.min(), 0.)
        np.testing.assert_allclose(coefficients.sum(1), 1-lam)

    def test_log_length_margin_is_exact_ln_n_minus_one(self):
        text = strings('s12_longer.py')
        self.assertIn(r'\ln(n-1)', text.replace(' ', ''))
        self.assertIn('equal-other-scores', text)
        self.assertIn('does not guarantee fixed sharpness or entropy', text)
        p = .63
        for n in (3, 11, 61):
            delta = math.log(n-1)+math.log(p/(1-p))
            self.assertAlmostEqual(math.exp(delta)/(math.exp(delta)+n-1), p)

    def test_scatter_range_preserves_synthetic_extrema(self):
        fn = method('s16_icl.py', 'agree')
        pl, pg = np.array([-9.3, .8, 12.2]), np.array([-10.1, .4, 13.4])
        limit = evaluate(assigned(fn, 'lim'), pl=pl, pg=pg)
        self.assertGreaterEqual(limit, np.max(np.abs(np.r_[pl, pg])))
        points = next(n for n in ast.walk(fn) if isinstance(n, ast.Assign)
                      and any(isinstance(t, ast.Name) and t.id == 'pts' for t in n.targets))
        self.assertNotIn('np.clip', ast.unparse(points))
        text = strings('s16_icl.py')
        self.assertIn('same evaluation prompts', text)
        self.assertIn('zero linear correlation', text)
        self.assertIn('does not establish identical predictions', text)

    def test_cost_names_architecture_and_matrix_counter_scope(self):
        text = strings('s08_cost.py')
        self.assertIn('matrix-FLOP counter convention', text)
        self.assertIn('leaves out normalization, activation and softmax', text)
        self.assertIn('neglecting the vocabulary projection', text)
        # The two parameter shares have different denominators even synthetically.
        attention, mlp, other = 40., 80., 20.
        self.assertNotEqual(attention/(attention+mlp), attention/(attention+mlp+other))

    def test_rasp_formal_claims_keep_precision_and_hypothesis_assumptions(self):
        text = strings('s17_rasp.py')
        for phrase in ['fixed depth', 'log-space-computable', 'conjecture',
                       'short causal all-length program', 'no repeated tokens']:
            self.assertIn(phrase, text)

    def test_known_copy_display_excludes_last_query_without_next_copy_target(self):
        fn = method('s15_induction.py', 'forming')
        maps = np.zeros((2, 1, 96, 96))
        for q in range(60, 79):
            maps[0, 0, q, q-49] = 1.
            maps[1, 0, q, q-49] = .25
        result = evaluate(assigned(fn, 'ind_sc'), L2=maps, hi=0, steps=[0, 1])
        np.testing.assert_allclose(result, [1., .25])
        self.assertIn('queries $60$--$78$', strings('s15_induction.py'))
        self.assertIn('earliest earlier matching token', strings('s15_induction.py'))


class ScoringCohorts(unittest.TestCase):
    def test_rows_preserve_synthetic_scores_without_global_sorting(self):
        fn = copy.deepcopy(method('s07_transformer.py', 'board_rows'))
        fn.body = [n for n in fn.body if not isinstance(n, (ast.Import, ast.ImportFrom))]
        original = {'rows': [dict(key='uniform', bits=4.2), dict(key='best', bits=3.1)]}
        t = dict(ctx=256, passage_bits=8.8)
        k = dict(best=7, best_bits=.4)
        n = dict(n_ctx=24, passage_bits=6.6, mix_bits=5.5)
        saved = copy.deepcopy((original, t, k, n))
        env = dict(load=lambda _:t, c1=types.SimpleNamespace(load=lambda _:original),
                   c6=types.SimpleNamespace(load=lambda _:k), c8=types.SimpleNamespace(load=lambda _:n))
        exec(compile(ast.Module(body=[fn], type_ignores=[]), '<synthetic-board>', 'exec'), env)
        rows, _, _, _ = env['board_rows']()
        self.assertEqual([r['key'] for r in rows], ['uniform', 'best', 'kn', 'nlm', 'mix', 'tf'])
        self.assertEqual([r['bits'] for r in rows[-4:]], [.4, 6.6, 5.5, 8.8])
        self.assertEqual((original, t, k, n), saved)
        for row in rows[-4:]:
            first, last = row['cohort']['targets']
            self.assertEqual(row['cohort']['count'], last-first+1)
            self.assertEqual(row['cohort']['index_convention'], 'zero-based inclusive')
        self.assertNotEqual(rows[-4]['cohort']['targets'], rows[-3]['cohort']['targets'])
        self.assertNotEqual(rows[-3]['cohort']['targets'], rows[-1]['cohort']['targets'])

    def test_board_qualifies_distinct_targets_instead_of_a_universal_winner(self):
        text = strings('s07_transformer.py')
        self.assertIn('distinct target', text)
        self.assertIn('not a', text)
        board = ast.unparse(method('s07_transformer.py', 'board'))
        self.assertNotIn('input_text_sha256', ast.unparse(method('s07_transformer.py', 'board_rows')))
        self.assertNotIn('np.argmin', board)
        self.assertNotIn('sorted(', board)


class BilingualSourceTemplates(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tr = translator()

    def translated(self, en):
        zh = self.tr(en)
        self.assertIsNotNone(zh, en)
        self.assertRegex(zh, '[一-鿿]')
        self.assertNotRegex(zh, r'\{[^{}]+\}')
        self.assertEqual(re.findall(r"<bookmark mark='([^']+)'/>", en),
                         re.findall(r"<bookmark mark='([^']+)'/>", zh))
        return zh

    def test_both_dynamic_induction_composition_branches_translate_recursively(self):
        fn = method('s15_induction.py', 'composition')
        # One clearly separated contrast and one non-separated contrast. These are
        # synthetic matrix summaries, not saved experiment measurements.
        for k1, q1, o1, phrase in [(.8, .2, .3, 'changes from'),
                                  (.24, .4, .5, 'it ends at')]:
            env = dict(n_p=3, n_i=2, k0=.15, k1=k1, q1=q1, o1=o1,
                       bsd=.03, base=.17, has_other=True)
            env['v'] = evaluate(assigned(fn, 'v'), **env)
            self.assertIn(phrase, env['v'])
            branch = self.translated(env['v'])
            self.assertIn(f'{k1:.2f}', branch)
            self.assertRegex(branch, '因果')
            complete = self.translated(evaluate(voice(fn), **env))
            self.assertIn(f'{k1:.2f}', complete)
            self.assertEqual(re.findall(r"<bookmark mark='([^']+)'/>", complete), ['a', 'b'])

    def test_all_pairs_selected_branch_never_formats_a_missing_other_mean(self):
        fn = method('s15_induction.py', 'composition')
        env = dict(n_p=3, n_i=2, k0=.14, k1=.21, q1=.19, o1=None,
                   bsd=.04, base=.13, has_other=False)
        env['v'] = evaluate(assigned(fn, 'v'), **env)
        self.assertIn('There is no other comparison group', env['v'])
        self.translated(env['v'])
        self.translated(evaluate(voice(fn), **env))

    def test_icl_both_correlation_branches_keep_evaluation_protocol(self):
        fn = method('s16_icl.py', 'agree')
        for i, correlation in enumerate((.995, .25)):
            env = {'r_':correlation}
            env['v_line'] = evaluate(assigned(fn, 'v_line', i), **env)
            zh = self.translated(evaluate(voice(fn), **env))
            self.assertIn(f'{correlation:.3f}', zh)
            self.assertIn('59', zh)
            self.assertRegex(zh, '相同|同一')
            self.assertRegex(zh, '不能|不代表|不等于')

    def test_hook_keeps_held_out_training_and_many_model_scope(self):
        en = evaluate(voice(method('s01_hook.py','reading')))
        self.assertIn('excluded from gradient training', en)
        self.assertIn('many large language models', en)
        self.translated(en)


class CaptionProposal(unittest.TestCase):
    def setUp(self):
        self.shared_path = ROOT / 'videos/ai/ai_text_zh.json'
        self.original_bytes = self.shared_path.read_bytes()
        self.base = json.loads(self.original_bytes)
        delta = json.loads((PART / 'reviewed_caption_delta.json').read_text())
        self.assertEqual(delta['target'], 'videos/ai/ai_text_zh.json')
        self.operations = delta['operations']
        self.merged = copy.deepcopy(self.base)
        self.assertEqual(len({(x['table'], x['key']) for x in self.operations}), len(self.operations))
        for op in self.operations:
            if op['table'] == 'strings':
                if op['operation'] == 'add':
                    self.assertTrue(op['expected_absent'])
                    if op['key'] in self.merged['strings']:
                        self.assertEqual(self.merged['strings'][op['key']], op['value'])
                else:
                    self.assertEqual(op['operation'], 'replace')
                    self.assertIn(self.merged['strings'][op['key']], (op['expected_before'], op['value']))
                self.merged['strings'][op['key']] = op['value']
            else:
                self.assertEqual((op['table'], op['operation']), ('patterns', 'append'))
                self.assertTrue(op['expected_absent'])
                existing = [p for p in self.merged['patterns'] if p[0] == op['key']]
                re.compile(op['key'])
                if existing:
                    self.assertEqual(existing, [[op['key'], op['value']]])
                else:
                    self.merged['patterns'].append([op['key'], op['value']])

    def test_delta_preserves_every_unowned_shared_entry_in_memory(self):
        owned = {x['key'] for x in self.operations if x['table'] == 'strings'}
        self.assertEqual({k:v for k,v in self.base['strings'].items() if k not in owned},
                         {k:v for k,v in self.merged['strings'].items() if k not in owned})
        self.assertEqual(self.merged['patterns'][:len(self.base['patterns'])], self.base['patterns'])
        self.assertEqual(self.shared_path.read_bytes(), self.original_bytes)

    def test_actual_caption_engine_preserves_synthetic_dynamic_values(self):
        # Extract only pure translation functions/constants, excluding Manim imports.
        source = ast.parse((ROOT / 'explainer/zh_text.py').read_text())
        constants = {'_NUM', '_SPACE', '_TEXT_CMD', '_TABLE', '_BY_NUMBERS'}
        selected = []
        for n in source.body:
            if isinstance(n, ast.FunctionDef) and n.name in {'_by_numbers', 'translate'}:
                selected.append(n)
            elif isinstance(n, (ast.Assign, ast.AnnAssign)):
                targets = n.targets if isinstance(n, ast.Assign) else [n.target]
                if any(isinstance(t, ast.Name) and t.id in constants for t in targets):
                    selected.append(n)
        env = {'re': re, 'lang': types.SimpleNamespace(LANG='zh')}
        exec(compile(ast.Module(body=selected, type_ignores=[]), '<pure-caption-engine>', 'exec'), env)
        env['_TABLE'], env['_BY_NUMBERS'] = self.merged, None
        examples = [
            (r'nonzero directions: \ at most $7$', '7'),
            (r'final mean value norm: \ $0.73\times$ the other mean norm', '0.73'),
            (r'correlation on $4{,}000$ prompts: \ $0.482$', '0.482'),
        ]
        for text, number in examples:
            translated = env['translate'](text)
            self.assertRegex(translated, '[一-鿿]')
            self.assertIn(number, translated)
            self.assertNotRegex(translated, r'\\g[<\d]')
        self.assertEqual(self.shared_path.read_bytes(), self.original_bytes)


if __name__ == '__main__':
    unittest.main()
