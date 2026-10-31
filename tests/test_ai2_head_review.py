"""Head review regressions: true cutoff bounds and source-driven bilingual narration."""
import ast
import re
import unittest
from pathlib import Path
from types import SimpleNamespace

import numpy as np

from explainer.zh_templates import Translator, sources
from videos.ai.ai2 import s07_games


ROOT = Path(__file__).resolve().parents[1]


def traced_tree():
    """Use the actual illustrative LEAVES, with the scene's breadth-first numbering."""
    data, kids, queue = [], [], [s07_games.toy_tree()]
    for node in queue:
        data.append(node)
        first = len(queue)
        queue.extend(node['children'])
        kids.append(list(range(first, len(queue))))
    return SimpleNamespace(node_data=data, kids=kids)


def exact_value(tree, i=0, depth=0):
    if not tree.kids[i]:
        return tree.node_data[i]['v']
    values = [exact_value(tree, j, depth + 1) for j in tree.kids[i]]
    return max(values) if depth % 2 == 0 else min(values)


class AlphaBetaBoundsTests(unittest.TestCase):
    def test_actual_cutoff_value_is_an_upper_bound_and_root_stays_exact(self):
        tree = traced_tree()
        events = s07_games.trace_alphabeta(tree)
        values = {e[1]: e[2:] for e in events if e[0] == 'value'}
        third_min = tree.kids[0][2]
        self.assertEqual(exact_value(tree, third_min, 1), 5)
        self.assertEqual(values[third_min], (6, 'upper'))
        self.assertEqual(s07_games.trace_score_tex(*values[third_min]), r'\le 6')
        self.assertEqual(values[0], (6, 'exact'))
        self.assertEqual(exact_value(tree), 6)

    def test_every_displayed_internal_bound_contains_true_minimax_value(self):
        tree = traced_tree()
        depth = {0: 0}
        for i, children in enumerate(tree.kids):
            for j in children:
                depth[j] = depth[i] + 1
        kinds = set()
        for event in s07_games.trace_alphabeta(tree):
            if event[0] != 'value':
                continue
            _, i, score, bound = event
            actual = exact_value(tree, i, depth[i])
            kinds.add(bound)
            if bound == 'upper':
                self.assertLessEqual(actual, score)
            elif bound == 'lower':
                self.assertGreaterEqual(actual, score)
            else:
                self.assertEqual(actual, score)
            if not tree.kids[i]:
                self.assertEqual(bound, 'exact')
        self.assertEqual(kinds, {'exact', 'lower', 'upper'})


class HeadNarrationTests(unittest.TestCase):
    def setUp(self):
        self.translator = Translator('ai2')
        self.rows = sources('ai2')

    def spoken(self, needle, **values):
        row = next(r for r in self.rows if needle in r.get('en', r.get('tpl', '')))
        if 'en' in row:
            return row['en']
        return eval(compile(ast.parse(row['tpl'], mode='eval'), 'actual-head-narration', 'eval'),
                    {'__builtins__': {}, 'min': min, 'len': len, 'int': int}, values)

    def check_translation(self, english):
        chinese = self.translator(english)
        self.assertIsNotNone(chinese)
        self.assertRegex(chinese, r'[\u4e00-\u9fff]')
        self.assertNotIn('{', chinese)
        self.assertEqual(re.findall(r"<bookmark[^>]+/>", english), re.findall(r"<bookmark[^>]+/>", chinese))
        return chinese

    def test_turing_search_metropolis_samuel_scope_survives_translation(self):
        cases = [self.spoken('The limit appears', d={'bb4_steps':107, 'bb5_steps':47176870, 'bb5_seconds':.33}),
                 self.spoken('Search strategies differ only'), self.spoken('Simulated annealing escapes'),
                 self.spoken("Samuel's delta idea")]
        for text in cases:
            self.check_translation(text)
        self.assertIn('两种纸带符号', self.translator(cases[0]))
        self.assertIn('最深层数', self.translator(cases[1]))
        self.assertIn('平稳分布', self.translator(cases[2]))
        self.assertIn('半梯度', self.translator(cases[3]))

    def test_equal_optimal_cost_and_paired_median_wording_translate(self):
        text = self.spoken('Here are the two searches', C=30.38697, nd=2636, na=239, inside=(100,100))
        self.assertNotIn('same shortest path', text)
        self.assertIn('相同的最优代价', self.check_translation(text))
        # Formatting fixture, not a new measurement of the production map batch.
        text = self.spoken('One map proves little', n_maps=200, med=[2000.,400.,200.,100.], ratio=17.,
                           excess=[0.,0.,.1,.2])
        self.assertIn('配对', self.check_translation(text))

    def test_independent_polished_baseline_and_genetic_wording_translate(self):
        d = {'budget':2000000, 'nn_lengths':[8181], 'nn2opt_lengths':[7657], 'eq_anneal':[7542]*5}
        order = [('annealing',7542),('restarted hill climbing',7705),('the genetic algorithm',7931)]
        verdict = self.spoken('On the same budget', d=d, order=order)
        hits = self.spoken('Annealing found the optimum itself', n_opt=5, d=d)
        text = self.spoken('Is the cooling worth', d=d, opt=7542, verdict=verdict, hits=hits)
        self.assertIn('different start', text)
        self.assertIn('另一个起点', self.check_translation(text))
        text = self.spoken('A third idea keeps a whole population', ga_gap=6.)
        self.assertNotIn('most children', text)
        self.check_translation(text)

    def test_cutoff_narration_translates_with_actual_trace_counts(self):
        tree = traced_tree()
        visited = {e[1] for e in s07_games.trace_alphabeta(tree) if e[0] == 'visit'}
        pruned = [i for i in range(len(tree.kids)) if i not in visited]
        text = self.spoken('Much of a game tree can be skipped', n=len(tree.kids), pruned_all=pruned)
        chinese = self.check_translation(text)
        self.assertIn('inequality', text)
        self.assertIn('不等号', chinese)
        self.assertNotIn('every chess program', text)

    def test_positive_feature_count_includes_small_positive_weights(self):
        tree = ast.parse((ROOT/'videos/ai/ai2/s08_samuel.py').read_text())
        expr = next(n.value for n in ast.walk(tree) if isinstance(n, ast.Assign) and
                    any(isinstance(t, ast.Name) and t.id == 'npos' for t in n.targets))
        # Trusted repository expression: NumPy may lazily import during sum(),
        # so use normal builtins rather than depending on earlier test imports.
        actual = eval(compile(ast.Expression(expr), 'actual-positive-count', 'eval'),
                      {'int':int}, {'fin':np.array([-.1,.001,0,.1,.5])})
        self.assertEqual(actual, 3)
