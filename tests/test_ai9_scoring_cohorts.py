"""Synthetic presentation contracts; no model, scene, cache or renderer imports.

These tests verify cohort attribution and translated narration, not pixels/audio.
"""

import ast
import copy
import importlib.util
import json
from pathlib import Path
import re
import sys
import types
import unittest

ROOT = Path(__file__).resolve().parents[1]
PART = ROOT / 'videos/ai/ai9'
spec = importlib.util.spec_from_file_location('ai9_pure_scoring', PART / 'scoring.py')
scoring = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = scoring
spec.loader.exec_module(scoring)


def method(filename, name):
    return next(n for n in ast.walk(ast.parse((PART / filename).read_text()))
                if isinstance(n, ast.FunctionDef) and n.name == name)


def assigned(fn, name, env):
    node = next(n.value for n in ast.walk(fn) if isinstance(n, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == name for t in n.targets))
    return eval(compile(ast.Expression(node), '<actual-scene-expression>', 'eval'), env)


def narrated(fn, env):
    node = next(n.args[0] for n in ast.walk(fn) if isinstance(n, ast.Call)
                and isinstance(n.func, ast.Attribute) and n.func.attr == 'voiceover')
    return eval(compile(ast.Expression(node), '<actual-scene-narration>', 'eval'), env)


def translator():
    # Execute only the stdlib template engine, supplying its path dependency.
    # Read translation dictionaries by AST; do not import the scene package or
    # root's independent math overrides (they have their own review scope).
    source = ast.parse((ROOT / 'explainer/zh_templates.py').read_text())
    source.body = [n for n in source.body if not (isinstance(n, ast.ImportFrom)
                   and n.module == 'explainer.paths')]
    module = types.ModuleType('ai9_scoring_template_engine')
    module.video_dir = lambda _: PART
    exec(compile(source, 'explainer/zh_templates.py', 'exec'), module.__dict__)
    tables = {'TITLE': '', 'CHAPTERS': {}}
    for n in ast.parse((PART / 'zh_lines.py').read_text()).body:
        if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name):
            key = n.targets[0].id
            if key in ('ZH', 'PHRASES'):
                tables[key] = ast.literal_eval(n.value)
        if (isinstance(n, ast.Expr) and isinstance(n.value, ast.Call)
                and isinstance(n.value.func, ast.Attribute) and n.value.func.attr == 'update'
                and isinstance(n.value.func.value, ast.Name) and isinstance(n.value.args[0], ast.Dict)):
            tables[n.value.func.value.id].update(ast.literal_eval(n.value.args[0]))
    module.table = lambda _: tables
    return module.Translator('ai9')


class Cohorts(unittest.TestCase):
    def test_inclusive_target_counts_and_validation_prefixes(self):
        self.assertEqual(scoring.PASSAGE_COUNTING.count, 21399)
        self.assertEqual(scoring.PASSAGE_NEURAL.count, 21382)
        self.assertEqual(scoring.VALIDATION_CHECKPOINT.count, 49976)
        self.assertEqual(scoring.VALIDATION_MIXTURE.count, 199976)
        self.assertEqual(scoring.VALIDATION_FINAL.count, 1239833)
        self.assertNotEqual(scoring.METRIC_COHORTS['legacy_kn'], scoring.METRIC_COHORTS['mix_bits'])
        self.assertNotEqual(scoring.METRIC_COHORTS['curve_validation'], scoring.METRIC_COHORTS['valid_bits'])
        self.assertEqual(scoring.METRIC_COHORTS['curve_passage'], scoring.METRIC_COHORTS['mix_bits'])

    def test_grouped_rows_preserve_scores_without_using_legacy_kn(self):
        # Deliberately extreme synthetic legacy scalar: never a Part 9 row or ranking.
        lm = dict(n_ctx=24, kn=-9876, passage_bits=3.1234567, mix_bits=2.7654321)
        kn, infini = dict(best_bits=2.7), dict(mix_bits=2.6)
        original = copy.deepcopy((lm, kn, infini))
        (neural_scope, neural), (count_scope, history) = scoring.passage_groups(lm, kn, infini)
        self.assertEqual((neural_scope.first, neural_scope.last), (24, 21405))
        self.assertEqual((count_scope.first, count_scope.last), (7, 21405))
        self.assertEqual([r['bits'] for r in neural], [lm['passage_bits'], lm['mix_bits']])
        self.assertEqual([r['bits'] for r in history], [kn['best_bits'], infini['mix_bits']])
        self.assertEqual([r['key'] for r in history], ['kn', 'infini'])
        neural[0]['bits'] = 999
        self.assertEqual((lm, kn, infini), original)
        with self.assertRaises(ValueError):
            scoring.passage_groups(dict(lm, n_ctx=25), kn, infini)

    def test_honest_axis_includes_initial_checkpoint_and_rejects_invalid_data(self):
        for data in ([8.12, 5., 2.37], [2., 2.], [0., .01], [10.5, 100.1]):
            low, high = scoring.score_range(data)
            self.assertLessEqual(low, min(data))
            self.assertGreaterEqual(high, max(data))
            self.assertGreater(high, low)
        for data in ([], [float('nan')], [float('inf')], [-1.]):
            with self.assertRaises(ValueError):
                scoring.score_range(data)
        for step in (0, -1, float('nan'), float('inf')):
            with self.assertRaises(ValueError):
                scoring.score_range([2.], step)


class NarrationAndSource(unittest.TestCase):
    def setUp(self):
        self.tr = translator()

    def assert_translates(self, en, *phrases):
        zh = self.tr(en)
        self.assertIsNotNone(zh, en)
        self.assertNotRegex(zh, r'\{[^{}]+\}')
        self.assertEqual(re.findall(r"<bookmark mark='([^']+)'/>", en),
                         re.findall(r"<bookmark mark='([^']+)'/>", zh))
        for phrase in phrases:
            self.assertIn(phrase, zh)
        return zh

    def test_bilingual_training_preserves_bookmarks_and_adds_monitored_scope(self):
        fn = method('s16_lm.py', 'training')
        env = dict(nn=2.73, wr=[[0, 0, 0, 0, .1], [1, 0, 0, 0, .2],
                               [2, 0, 0, 0, .3], [300, 0, 0, 0, .4]], s1=300)
        env['early'] = assigned(fn, 'early', env)
        env['end'] = assigned(fn, 'end', env)
        self.assertIn('positions 24 through 21,405', env['end'])
        self.assertIn('monitored during training', env['end'])
        self.assert_translates(narrated(fn, env), '21382', '第24到第21405', '训练过程中', '2.73')
        self.assertNotIn('np.clip', ast.unparse(fn))
        self.assertNotIn('board_rows()', ast.unparse(fn))
        self.assertNotIn('knl', ast.unparse(fn))
        self.assertIn('checkpoint_prefix', ast.unparse(fn))

    def test_mixture_statement_is_conditional_only_against_paired_neural_score(self):
        fn = method('s16_lm.py', 'mixing')
        for mix, expected in ((2.1, '低于单独的网络'), (2.8, '并不低于单独的网络'), (2.7, '并不低于单独的网络')):
            env = dict(nn=2.7, mix=mix, wins=.37)
            env['comparison'] = assigned(fn, 'comparison', env)
            env['said'] = assigned(fn, 'said', env)
            zh = self.assert_translates(narrated(fn, env), expected, '37%', '不是预测准确率', '单独得分没有保存')
            self.assertNotIn('better than either', env['said'])
            self.assertIn('observed next character', env['said'])
            self.assertIn('前20万个字符', zh)
        self.assertNotIn("d['kn']", ast.unparse(fn))
        self.assertNotIn('min(kn', ast.unparse(fn))

    def test_separate_board_and_recap_translate_without_global_winner_claim(self):
        board = method('s16_lm.py', 'board')
        self.assert_translates(narrated(board, {}), '21382', '21399', '不能用来相互排名')
        recap = method('s17_outro.py', 'recap')
        env = dict(nn_b=2.7, mix_b=2.3)
        env['last'] = assigned(recap, 'last', env)
        self.assert_translates(narrated(recap, env), '2.70', '2.30', '21382', '不同的目标范围')
        for fn in (board, recap):
            source = ast.unparse(fn)
            for invalid in ('best machine', 'every counting model', 'behind GPT-2', 'best_counting', 'nn_b - kn_b'):
                self.assertNotIn(invalid, source)
        self.assertNotIn('board_rows()', ast.unparse(board))
        self.assertTrue(any(isinstance(n, ast.FunctionDef) and n.name == 'board_rows'
                            for n in ast.parse((PART/'s16_lm.py').read_text()).body))

    def test_delta_translates_new_scope_labels_and_preserves_all_numbers(self):
        delta = json.loads((PART/'scoring_text_zh.json').read_text())
        self.assertEqual(set(delta), {'strings', 'phrases', 'patterns'})
        strings = delta['strings']
        for name, fn_name in (('s16_lm.py', 'training'), ('s16_lm.py', 'mixing'), ('s16_lm.py', 'board')):
            for node in ast.walk(method(name, fn_name)):
                if isinstance(node, ast.Constant) and isinstance(node.value, str):
                    text = node.value
                    if ('targets $' in text or 'validation bits/' in text or 'Scores on two' in text
                            or text.startswith('Part 9:') or text.startswith('Part 7:')
                            or text.startswith('Zero-based target')):
                        self.assertIn(text, strings)
        for en, zh in strings.items():
            self.assertEqual(re.findall(r'\d+(?:[.,]\d+)*', en), re.findall(r'\d+(?:[.,]\d+)*', zh), en)
        self.assertIn(r'neural LM: $2.37$ bits/char \\ targets $24$--$21405$', strings)


if __name__ == '__main__':
    unittest.main()
