"""Replay quantities and bilingual outcomes, using actual source expressions on small fixtures.

These checks do not train a policy, provide benchmark results, or establish rendered acceptance.
"""
import ast
from pathlib import Path
import types
import unittest

import numpy as np

from videos.ai.ai26.envs import CartPole

ROOT = Path(__file__).resolve().parents[1]
PART = ROOT / 'videos/ai/ai26'


def function(filename, name):
    return next(n for n in ast.walk(ast.parse((PART / filename).read_text()))
                if isinstance(n, ast.FunctionDef) and n.name == name)


def value(filename, method, name, context):
    fn = function(filename, method)
    expression = next(n.value for n in ast.walk(fn) if isinstance(n, ast.Assign)
                      and any(isinstance(t, ast.Name) and t.id == name for t in n.targets))
    return eval(compile(ast.Expression(expression), filename, 'eval'), context)


def translator():
    # Load the actual template engine without importing rendering or generating caches.
    tree = ast.parse((ROOT / 'explainer/zh_templates.py').read_text())
    tree.body = [n for n in tree.body if not (isinstance(n, ast.ImportFrom) and n.module == 'explainer.paths')]
    module = types.ModuleType('ai26_template_contract')
    module.video_dir = lambda _: PART
    exec(compile(tree, 'actual-zh-template-engine', 'exec'), module.__dict__)
    return module.Translator('ai26')


class ReplayContracts(unittest.TestCase):
    def test_rollout_state_count_is_not_transition_count(self):
        count = value('s08_dqn.py', 'replay_training', 'episode_steps', {'L': np.array([10, 501])})
        np.testing.assert_array_equal(count, [9, 500])
        fn = function('s08_dqn.py', 'replay_training')
        condition = next(n for n in fn.body if isinstance(n, ast.If) and isinstance(n.test, ast.Compare))
        end = condition.orelse[0].value
        spoken = eval(compile(ast.Expression(end), 'actual-dqn-end', 'eval'),
                      {'steps': [0, 50_000], 'best': 1, 'episode_steps': count})
        self.assertIn('500 of five hundred', spoken)
        self.assertNotIn('501', spoken)

    def test_failure_uses_simulator_thresholds_even_at_time_limit(self):
        fn = function('common.py', 'cartpole_failed')
        module = types.ModuleType('actual-cartpole-failure')
        module.CartPole = CartPole
        exec(compile(ast.Module(body=[fn], type_ignores=[]), 'actual-common-helper', 'exec'), module.__dict__)
        failed = module.cartpole_failed
        self.assertFalse(failed(CartPole.x_max, CartPole.theta_max))
        self.assertTrue(failed(CartPole.x_max + 1e-8, 0))
        self.assertTrue(failed(0, -CartPole.theta_max - 1e-8))
        env = CartPole(np.random.default_rng(11))
        env.reset()
        for _ in range(500):
            state, _, terminated, truncated = env.step(0)
            self.assertEqual(failed(state[0], state[2]), terminated)
            if terminated or truncated:
                break
        self.assertTrue(terminated)

    def test_cliff_replay_counts_falls_only_in_displayed_segment(self):
        # An ordinary down-step to S is not a fall; the stored cliff sentinel is.
        shown = [(2, 0), (3, 0), (3, 1), (3, 0), (2, 0), (3, 0)]
        falls = value('s07_qlearning.py', 'training', 'falls', {'shown': shown, 'R': 4, 'Cc': 12})
        self.assertEqual(falls, 1)

    def test_divergence_threshold_never_invents_a_crossing(self):
        tr = translator()
        fn = function('s08_dqn.py', 'divergence')
        spoken = next(n.args[0] for n in ast.walk(fn) if isinstance(n, ast.Call)
                      and isinstance(n.func, ast.Attribute) and n.func.attr == 'voiceover')
        for magnitudes, expected, zh_expected in [([1, 900, 999], 'do not cross', '没有超过'),
                                                   ([1001, 1200, 1300], 'step 0', '第0步'),
                                                   ([1, 1000, 1001], 'step 2,000', '第2000步')]:
            ctx = {'np': np, 'st': np.array([0, 1000, 2000]),
                   'v': {'no_target': magnitudes, 'full': [1, 2, 3], 'bound': 100}}
            ctx['crossings'] = value('s08_dqn.py', 'divergence', 'crossings', ctx)
            ctx['threshold'] = value('s08_dqn.py', 'divergence', 'threshold', ctx)
            self.assertIn(expected, ctx['threshold'])
            en = eval(compile(ast.Expression(spoken), 'actual-divergence-voiceover', 'eval'), ctx)
            zh = tr(en)
            self.assertIsNotNone(zh)
            self.assertIn(zh_expected, zh)
            self.assertNotIn('sampled', zh)
            self.assertNotIn('threshold', zh)

    def test_solver_outcome_narration_translates_all_nine_pairs(self):
        fn = function('s12_mcts.py', 'growth')
        expression = [n.args[0] for n in ast.walk(fn) if isinstance(n, ast.Call)
                      and isinstance(n.func, ast.Attribute) and n.func.attr == 'voiceover'][-1]
        tr = translator()
        for best in ['wins', 'draws', 'loses']:
            for chosen in ['wins', 'draws', 'loses']:
                en = eval(compile(ast.Expression(expression), 'actual-mcts-verdict', 'eval'),
                          {'best_true': 2, 'best_mc': 5, 'best_result': best, 'chosen_result': chosen})
                zh = tr(en)
                self.assertIsNotNone(zh, en)
                self.assertIn('3', zh)
                self.assertIn('6', zh)
                self.assertNotIn('wins', zh)
                self.assertNotIn('loses', zh)
                self.assertNotIn('draws', zh)
                self.assertIn('有限预算', zh)


if __name__ == '__main__':
    unittest.main()
