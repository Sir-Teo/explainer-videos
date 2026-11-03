"""Synthetic regression fixtures, not regenerated Part29 scientific results.

No renders, datasets or full experiments. The compute module's optional rendering
cache import is substituted only to allow testing in a CPU-only Python runtime.
All numerical functions under test are compiled unchanged from production source.
RealCache tests execute the original Cache module with only its TTS root import
substituted; actual JSON/NPZ merging, locks and file-signature invalidation run.
"""
import ast
import json
import importlib.util
from pathlib import Path
import tempfile
import sys
import types
import unittest
from unittest.mock import patch

import numpy as np

from videos.ai.ai29 import dreamer
from videos.ai.ai29.envs import Catch

ROOT = Path(__file__).resolve().parents[1]
PART = ROOT / 'videos/ai/ai29'
lock_spec = importlib.util.spec_from_file_location('ai29_test_real_cache_lock', ROOT / 'explainer/cache_lock.py')
lock_module = importlib.util.module_from_spec(lock_spec)
lock_spec.loader.exec_module(lock_module)


class CacheFixture:
    def __init__(self, name):
        self.dir = Path('/unavailable-synthetic-cache')
        self.items = {}

    def path(self, name):
        return self.dir / (name + '.json')

    def load(self, name):
        return json.loads(self.path(name).read_text())


def compute_module():
    tree = ast.parse((PART / 'compute.py').read_text())
    tree.body = [n for n in tree.body if not
                 (isinstance(n, ast.ImportFrom) and n.module in ('explainer.ai.cache', 'explainer.cache_lock'))]
    mod = types.ModuleType('videos.ai.ai29.synthetic_compute_test')
    mod.__package__ = 'videos.ai.ai29'
    mod.Cache = CacheFixture
    mod.locked_item = lock_module.locked_item
    exec(compile(tree, str(PART / 'compute.py'), 'exec'), mod.__dict__)
    return mod


c = compute_module()


class ScientificContracts(unittest.TestCase):
    def test_all_correct_lookups_pay_for_real_checks(self):
        w = c.Warehouse(c.rng(1))
        original = w.call
        invocations = []
        def observed(tool, arg):
            invocations.append((tool, arg))
            return original(tool, arg)
        w.call = observed
        ok, calls, trace = c.agent_episode(w, ['bolt', 'gear', 'hinge'], 'check', c.rng(2),
                                          rates=dict(head=0, malformed=0, silent=0, catch=1), trace=True)
        self.assertTrue(ok)
        self.assertEqual(calls, 6)
        self.assertEqual(calls, len(invocations))
        self.assertEqual(sum('[check]' in s for s in trace), 3)

    def test_failed_checks_respect_call_budget(self):
        w = c.Warehouse(c.rng(1))
        original = w.call
        calls = []
        def observed(tool, arg):
            calls.append((tool, arg))
            return original(tool, arg)
        w.call = observed
        ok, charged, _ = c.agent_episode(w, ['bolt'], 'check', c.rng(3),
                                         rates=dict(head=0, malformed=0, silent=1, catch=1))
        self.assertFalse(ok)
        self.assertEqual(charged, len(calls))
        self.assertLessEqual(charged, 7)

    def test_segment_collision_not_just_endpoints(self):
        self.assertTrue(c.segment_hits_circle([-1, 0], [1, 0], [0, 0], .3))
        self.assertTrue(c.segment_hits_circle([-1, .3], [1, .3], [0, 0], .3))
        self.assertFalse(c.segment_hits_circle([-1, .31], [1, .31], [0, 0], .3))
        self.assertTrue(c.segment_hits_circle([0, 0], [0, 0], [0, 0], .3))
        self.assertFalse(c.segment_hits_circle([1, 0], [1, 0], [0, 0], .3))
        paths, hit, reached = c.detour_rollout(lambda p: np.array([2., 0.]), [0.], 1)
        self.assertTrue(hit[0])
        self.assertFalse(reached[0])
        self.assertLess(paths[0][-1, 0], 0.)
        self.assertTrue(np.isnan(c.detour_crossing_y(paths[0])))

    def test_rollout_stops_at_exact_step_budget(self):
        paths, _, _ = c.detour_rollout(lambda p: np.tile([0., .01], 4), [1.], 4, max_steps=5)
        self.assertEqual(len(paths[0])-1, 5)

    def test_crossing_interpolates_and_does_not_invent_a_side(self):
        self.assertTrue(np.isnan(c.detour_crossing_y(np.array([[-1., 1.], [-.2, 2.]]))))
        self.assertAlmostEqual(c.detour_crossing_y(np.array([[-1., 1.], [1., 3.]])), 2.)
        self.assertTrue(np.isnan(c.detour_crossing_y(np.array([[1., 1.], [-1., 3.]]))))

    def test_full_integer_alphabet_and_out_of_range_guard(self):
        bounds = c.quantizer_alphabet(np.array([-5, 0, 5]))
        c.require_alphabet(np.arange(bounds[0], bounds[1]+1), bounds)
        c.require_alphabet(np.array([-4, 2, 4]), bounds)  # absent from training
        with self.assertRaisesRegex(ValueError, 'outside'):
            c.require_alphabet(np.array([bounds[1]+1]), bounds)
        rules = c.bpe_train([(0, 0, 0, 0)] * 3, 2)
        self.assertEqual(c.bpe_encode([2], rules), [2])

    def test_horizon_error_averages_match_independent_reference(self):
        lane = c.Lane()
        table = np.ones(lane.S, dtype=int)
        _, ps = lane.run(None, 12)
        per = []
        for distribution in ps[:-1]:
            per.append(sum(distribution[i] * lane.Pobs[i, j] * (table[j] != lane.expert[i])
                           for i in range(lane.S) for j in range(lane.S)))
        expected = [np.mean(per[:t]) for t in range(1, 13)]
        np.testing.assert_allclose(lane.eps_curve(table, 12), expected)
        self.assertNotEqual(expected[0], expected[-1])

    def test_landing_state_matches_observation_and_transition_count(self):
        env = Catch(np.random.default_rng(0), drops=2)
        obs, acts, rewards, states = dreamer.run_episode(env, lambda *args: (1, None), None)
        landings = np.flatnonzero(rewards)
        self.assertEqual(len(landings), 2)
        self.assertTrue(np.all(states[landings, 1] == Catch.S - 1))
        for i in landings:
            x, y, _ = states[i]
            self.assertEqual(obs[i].reshape(Catch.S, Catch.S)[y-1, min(x, Catch.S-2)], 1)
        rep = dreamer.Replay()
        rep.add(obs, dreamer.onehot(acts), rewards)
        self.assertEqual(rep.steps, 2*(Catch.S-1))
        self.assertEqual(rep.steps, len(obs)-1)

    def test_cache_guard_scoped_and_no_implicit_generation(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(c.CACHE, 'dir', Path(directory)):
            for name in ('dreamer', 'belief'):
                with self.assertRaises(FileNotFoundError): c.load(name)
            c.CACHE.path('belief').write_text('{"unmodified": true}')
            with patch.object(c.CACHE, 'load', wraps=c.CACHE.load) as reader:
                self.assertTrue(c.load('belief')['unmodified'])
                reader.assert_called_once_with('belief')
            def locked_read(name):
                self.assertIn(c.CACHE.path(name).resolve(), lock_module._local.held)
                return {'locked': True}
            with patch.object(c.CACHE, 'load', side_effect=locked_read):
                self.assertTrue(c.load('belief')['locked'])
            c.CACHE.path('fast').write_text('{}')
            with self.assertRaisesRegex(ValueError, 'legacy'): c.load('fast')
            c.CACHE.path('fast').write_text(json.dumps({'recipe_version': c.RECIPE_VERSIONS['fast']}))
            self.assertEqual(c.load('fast')['recipe_version'], c.RECIPE_VERSIONS['fast'])


def real_cache_class():
    """Load actual Cache implementation without importing optional Manim/TTS."""
    package = types.ModuleType('explainer')
    package.__path__ = [str(ROOT / 'explainer')]
    tts = types.ModuleType('explainer.tts')
    tts.REPO_ROOT = ROOT
    spec = importlib.util.spec_from_file_location('ai29_test_real_cache', ROOT / 'explainer/ai/cache.py')
    module = importlib.util.module_from_spec(spec)
    with patch.dict(sys.modules, {'explainer': package, 'explainer.tts': tts,
                                 'explainer.cache_lock': lock_module}):
        spec.loader.exec_module(module)
    return module.Cache


class RealCacheContracts(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.cache = real_cache_class()('ai29')
        self.cache.dir = Path(self.temporary.name)
        self.cache.items = {name: lambda: self.fail('implicit producer called') for name in ('fast', 'belief')}
        self.patcher = patch.object(c, 'CACHE', self.cache)
        self.patcher.start()
        self.addCleanup(self.patcher.stop)

    def write_pair(self, name, metadata, arrays):
        self.cache.path(name).write_text(json.dumps(metadata))
        np.savez(self.cache.path(name).with_suffix('.npz'), **arrays)

    def test_actual_json_npz_merge_and_replacement_are_read(self):
        metadata = {'recipe_version': c.RECIPE_VERSIONS['fast'], 'params': {'fixture': True}}
        self.write_pair('fast', metadata, {'example': np.array([1., 2.])})
        loaded = c.load('fast')
        self.assertEqual(loaded['params'], {'fixture': True})
        np.testing.assert_array_equal(loaded['example'], [1., 2.])
        np.savez(self.cache.path('fast').with_suffix('.npz'), example=np.array([3., 4., 5.]))
        np.testing.assert_array_equal(c.load('fast')['example'], [3., 4., 5.])

    def test_npz_cannot_shadow_recipe_or_other_json_metadata(self):
        metadata = {'recipe_version': c.RECIPE_VERSIONS['fast'], 'params': {'fixture': True}, 'tasks': 3}
        for key, value in [('recipe_version', np.array('old')),
                           ('params', np.array([5])), ('tasks', np.array([7]))]:
            with self.subTest(key=key):
                self.write_pair('fast', metadata, {key: value})
                with self.assertRaisesRegex(ValueError, 'NPZ shadows'):
                    c.load('fast')
        # Reserved protocol fields are also forbidden when absent in JSON.
        self.write_pair('fast', {'recipe_version': c.RECIPE_VERSIONS['fast']}, {'params': np.array([5])})
        with self.assertRaisesRegex(ValueError, 'NPZ shadows'):
            c.load('fast')

    def test_reject_shadow_after_previously_accepted_cached_load(self):
        metadata = {'recipe_version': c.RECIPE_VERSIONS['fast']}
        self.write_pair('fast', metadata, {'example': np.array([1.])})
        c.load('fast')
        np.savez(self.cache.path('fast').with_suffix('.npz'), recipe_version=np.array('old'))
        with self.assertRaisesRegex(ValueError, 'NPZ shadows'):
            c.load('fast')

    def test_unaffected_reader_keeps_existing_merge_semantics(self):
        self.write_pair('belief', {'fixture': 'historical'}, {'fixture': np.array([1, 2])})
        np.testing.assert_array_equal(c.load('belief')['fixture'], [1, 2])
        self.cache.path('belief').unlink()
        with self.assertRaises(FileNotFoundError):
            c.load('belief')


class DreamerRNGContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import torch
        torch.set_num_threads(1)

    def test_rng_context_restores_even_after_exception(self):
        import torch
        torch.manual_seed(15)
        before = torch.get_rng_state().clone()
        with self.assertRaises(RuntimeError):
            with dreamer.diagnostic_rng(72):
                torch.rand(100)
                raise RuntimeError('synthetic diagnostic failure')
        self.assertTrue(torch.equal(before, torch.get_rng_state()))

    def test_tiny_training_is_invariant_to_diagnostic_schedule(self):
        # Two tiny optimizer updates, not a scientific experiment or acceptance dataset.
        kwargs = dict(iters=2, steps_per_iter=1, B=1, L=4, H=2, starts=2,
                      init_eps=1, eval_eps=1, train_policy=True)
        a = dreamer.train(8, eval_every=1, snap_iters=(0, 1, 2), log=lambda s: None, **kwargs)
        b = dreamer.train(8, eval_every=2, snap_iters=(), log=None, **kwargs)
        np.testing.assert_array_equal(a['loss'], b['loss'])
        np.testing.assert_array_equal(a['kl'], b['kl'])
        np.testing.assert_array_equal(a['open_err'], b['open_err'])
        np.testing.assert_array_equal(a['curve'][[0, -1]], b['curve'])


if __name__ == '__main__':
    unittest.main()
