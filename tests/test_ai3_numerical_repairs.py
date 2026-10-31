"""Tiny real-kernel/orchestration checks; no production models, corpus or training."""
import copy
import json
import math
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import numpy as np

from videos.ai.ai3 import compute as c


class RetrievalTests(unittest.TestCase):
    def test_recall_denominator_counts_all_distinct_unseen_targets(self):
        score = lambda u: np.arange(30, 0, -1, dtype=float)
        self.assertEqual(c.retrieval_recall(score, [0], {0: list(range(20))}, {0: set()})['recall'], .5)
        self.assertEqual(c.retrieval_recall(score, [0], {0: [0, 0, 1, 11]}, {0: {0}})['recall'], .5)
        self.assertAlmostEqual(c.retrieval_recall(score, [0], {0: [0, 1, 11]}, {})['recall'], 2 / 3)

    def test_macro_empty_and_exhausted_candidates(self):
        scores = {0: np.arange(30, 0, -1), 1: np.arange(30, 0, -1), 2: np.ones(30)}
        r = c.retrieval_recall(scores.__getitem__, [0, 1, 2],
                               {0: [0], 1: list(range(20)), 2: []}, {})
        self.assertEqual(r['recall'], .75)
        self.assertEqual((r['evaluated_users'], r['eligible_targets'], r['excluded_empty_users']), (2, 21, 1))
        empty = c.retrieval_recall(lambda u: np.ones(1), [0], {0: [0]}, {0: {0}})
        self.assertTrue(math.isnan(empty['recall']))
        self.assertEqual(empty['evaluated_users'], 0)
        self.assertEqual(c.retrieval_recall(lambda u: [math.nan], [0], {0: [0]}, {})['recall'], 0)

    def test_invalid_item_ids_are_rejected(self):
        with self.assertRaises(ValueError):
            c.retrieval_recall(lambda u: [1], [0], {0: [1]}, {})

    def test_actual_evaluator_orders_raw_then_prior_ablation(self):
        # Compile the actual evaluator, supplying only its ranking dependencies.
        import ast
        tree = ast.parse(Path(c.__file__).read_text())
        outer = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'compute_twotower')
        evaluator = next(n for n in outer.body if isinstance(n, ast.FunctionDef) and n.name == 'eval_tt')
        ns = dict(np=np, TT_TAU=.1, warm_eval=[0], cold_users=[1], hist_train={0: []}, cold_hist={1: []},
                  warm_target={0: [0]}, cold_target={1: [0]}, seen_w={0: set()}, seen_c={1: set()},
                  prior=np.log([.1, .9]), tower_scores=lambda us, h: np.log([[.6, .4]]) * .1,
                  recall=lambda fn, us, targets, seen: int(np.argmax(fn(us[0]))))
        exec(compile(ast.Module(body=[evaluator], type_ignores=[]), c.__file__, 'exec'), ns)
        self.assertEqual(ns['eval_tt'](), [0, 0, 1, 1])


class SpectralTests(unittest.TestCase):
    def test_selected_tail_matches_independent_scipy_two_sided_ks(self):
        from scipy.stats import kstest
        x = np.array([.3, .5, .7, 1., 1.1, 1.2, 1.5, 2., 2.5, 3., 4., 8., 9., 10., 14., 30.])
        fitted = c.powerlaw_fit(x, min_tail=3)
        candidates = []
        for i in range(len(x) // 2, len(x) - 3 + 1):
            t = x[i:]
            alpha = 1 + len(t) / np.log(t / t[0]).sum()
            ks = kstest(t, lambda z: 1 - (z / t[0]) ** (1 - alpha)).statistic
            candidates.append((ks, t[0], alpha, len(t)))
        expected = min(candidates)
        self.assertAlmostEqual(fitted['ks'], expected[0])
        self.assertEqual(fitted['xmin'], expected[1])
        self.assertEqual(fitted['n_tail'], expected[3])
        self.assertEqual(c.powerlaw_fit(np.ones(20))['fit_status'], 'unavailable')

    def test_neighbours_mask_query_under_ties_and_zero_rows(self):
        E = np.array([[1., 0], [1., 0], [0, 0], [0, 1]])
        vocab = ['first', 'query', 'zero', 'last']; idx = {w: i for i, w in enumerate(vocab)}
        self.assertEqual([w for w, _ in c.neighbours(E, vocab, idx, 'query', 10)], ['first', 'last'])
        self.assertEqual(c.neighbours(E, vocab, idx, 'zero'), [])


class GPT2NeighbourLoopTests(unittest.TestCase):
    def actual_loop(self, tokens, query):
        import ast
        tree = ast.parse(Path(c.__file__).read_text())
        body = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'compute_gpt2').body
        loop = next(n for n in body if isinstance(n, ast.For) and isinstance(n.iter, ast.Name)
                    and n.iter.id == 'NEIGHBOUR_WORDS')
        decoded = []
        class Tokenizer:
            def decode(self, ids):
                decoded.extend(ids)
                return tokens[ids[0]]
        ns = dict(np=np, NEIGHBOUR_WORDS=['query'], token_id=lambda tok, w: query,
                  tok=Tokenizer(), Wn=np.ones((len(tokens), 1)), nb={})
        exec(compile(ast.Module(body=[loop], type_ignores=[]), c.__file__, 'exec'), ns)
        return ns['nb']['query'], decoded

    def test_tied_query_is_not_first_and_best_other_token_is_kept(self):
        result, decoded = self.actual_loop(['best', 'QUERY', 'best', 'query', '123',
                                             'alpha', 'beta', 'gamma', 'delta', 'epsilon'], 3)
        self.assertEqual([word for word, score in result], ['best', 'alpha', 'beta', 'gamma', 'delta', 'epsilon'])
        self.assertNotIn(3, decoded)
        self.assertEqual(decoded[0], 0)

    def test_original_other_candidate_budget_is_preserved(self):
        tokens = ['invalid123'] * 100
        tokens[79], tokens[90] = 'outside', 'query'
        result, decoded = self.actual_loop(tokens, 90)
        self.assertEqual(result, [])
        self.assertEqual(decoded, list(range(79)))
        self.assertEqual(c.item_recipe('gpt2')['candidate_cap'], 79)
        with tempfile.TemporaryDirectory() as td:
            cache = c.SchemaCache('ai3'); cache.dir = Path(td)
            cache.path('gpt2').write_text('{"legacy":true}')
            self.assertFalse(cache.current('gpt2'))


class MatrixFactorizationTests(unittest.TestCase):
    def test_final_baselines_and_ranks_fit_same_ratings(self):
        class Pieces(dict):
            @property
            def done(self): return self
            def finish(self): pass
        n_users, n_items = 8, 12
        split = np.arange(10) / 10
        world = dict(split=split, r=np.array([1., 2, 3, 4, 5, 1, 2, 3, 4, 5]),
                     genre=np.arange(n_items) % 6)
        calls, partial_params = [], []
        random = np.random.default_rng(3)
        P, Q = random.normal(size=(n_users, 8)), random.normal(size=(n_items, 8))
        def train(w, rank, lam, seed, **kw):
            calls.append((rank, kw['train_mask'].copy(), kw['eval_mask'].copy()))
            return dict(hist=[(0, 1., 1.), (40, .8, .9 + lam)], P=P, Q=Q,
                        qs=[Q.copy() for _ in range(7)])
        def partial(name, params):
            partial_params.append(params); return Pieces()
        with patch.multiple(c, N_USERS=n_users, N_ITEMS=n_items, MF_RANKS=[8], MF_LAMS=[0., .1]), \
                patch.object(c, 'ratings_world', return_value=world), patch.object(c, 'mf_train', side_effect=train), \
                patch.object(c.CACHE, 'partial', side_effect=partial):
            out = c.compute_mf()
        final = split < .9; test = split >= .9
        self.assertTrue(all(np.array_equal(mask, final) for rank, mask, ev in calls if np.array_equal(ev, test)))
        self.assertAlmostEqual(out['rmse_mean'], np.sqrt(np.mean((world['r'][test] - world['r'][final].mean()) ** 2)))
        self.assertEqual(out['fit_counts'], dict(tuning_train=8, validation=1, final_train=9, test=1))
        self.assertEqual(partial_params[0]['v'], 2)
        self.assertEqual(partial_params[0]['split'], out['split_fingerprint'])


class CheckpointTests(unittest.TestCase):
    def setUp(self):
        import torch
        self.torch = torch; torch.set_num_threads(1)
        torch.manual_seed(4)
        self.ei, self.eo = torch.nn.Embedding(5, 2), torch.nn.Embedding(5, 2)
        self.opt = torch.optim.Adam(list(self.ei.parameters()) + list(self.eo.parameters()), lr=.003)
        self.g = np.random.default_rng(7)
        self.losses = [self.step(), self.step()]
        self.expected = dict(provenance={'fingerprint': 'same-corpus-and-recipe'}, vocab=list('abcde'),
                             checks=[0, 1, 2, 4], batches_per_epoch=2, epochs=2)
        self.state = dict(checkpoint_schema=1, contract=copy.deepcopy(self.expected), epoch=0,
                          E_in=copy.deepcopy(self.ei.state_dict()), E_out=copy.deepcopy(self.eo.state_dict()),
                          opt=copy.deepcopy(self.opt.state_dict()), g=copy.deepcopy(self.g.bit_generator.state),
                          torch=torch.get_rng_state().clone(), losses=self.losses.copy(),
                          snaps=[{}, {}, {}], snap_steps=[0, 1, 2])

    def step(self):
        torch = self.torch
        idx = torch.tensor(self.g.integers(0, 5, 3))
        negatives = torch.randint(0, 5, (3,))
        loss = ((self.ei(idx) * self.eo(negatives)).sum(1) - 1).square().mean()
        self.opt.zero_grad(); loss.backward(); self.opt.step()
        return float(loss.detach())

    def test_serialized_resume_matches_uninterrupted_next_step(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / 'tiny.ckpt'; self.torch.save(self.state, path)
            state = self.torch.load(path, weights_only=False)
        next_loss = self.step()
        expected = [p.detach().clone() for p in (*self.ei.parameters(), *self.eo.parameters())]
        self.torch.manual_seed(9)
        self.ei, self.eo = self.torch.nn.Embedding(5, 2), self.torch.nn.Embedding(5, 2)
        self.opt = self.torch.optim.Adam(list(self.ei.parameters()) + list(self.eo.parameters()), lr=.003)
        self.g = np.random.default_rng(999)
        c.restore_sgns_checkpoint(state, self.expected, self.ei, self.eo, self.opt, self.g, self.torch)
        self.assertEqual(self.step(), next_loss)
        for actual, wanted in zip((*self.ei.parameters(), *self.eo.parameters()), expected):
            self.assertTrue(self.torch.equal(actual, wanted))

    def test_invalid_states_never_mutate_live_models_optimizer_or_rng(self):
        corruptions = [lambda s: s.pop('checkpoint_schema'),
                       lambda s: s['contract']['vocab'].reverse(),
                       lambda s: s.update(epoch=9), lambda s: s['losses'].append(0.),
                       lambda s: s['opt'].update(param_groups=[]), lambda s: s.update(g={}),
                       lambda s: s.update(torch=self.torch.ones(1)),
                       lambda s: next(iter(s['opt']['state'].values()))['exp_avg'].fill_(float('nan'))]
        for corrupt in corruptions:
            with self.subTest(corrupt=corrupt):
                state = copy.deepcopy(self.state); corrupt(state)
                before = [p.detach().clone() for p in (*self.ei.parameters(), *self.eo.parameters())]
                rng = copy.deepcopy(self.g.bit_generator.state); trng = self.torch.get_rng_state().clone()
                with self.assertRaises(c.IncompatibleSGNSCheckpoint):
                    c.restore_sgns_checkpoint(state, self.expected, self.ei, self.eo, self.opt, self.g, self.torch)
                for actual, wanted in zip((*self.ei.parameters(), *self.eo.parameters()), before):
                    self.assertTrue(self.torch.equal(actual, wanted))
                self.assertEqual(self.g.bit_generator.state, rng)
                self.assertTrue(self.torch.equal(self.torch.get_rng_state(), trng))


class CorpusPublicationTests(unittest.TestCase):
    def test_malformed_completion_metadata_is_stale_without_producing(self):
        with tempfile.TemporaryDirectory() as td:
            cache = c.SchemaCache('ai3'); cache.dir = Path(td)
            for value in ([], None, 3, 'not-a-mapping'):
                cache.path('jl').write_text(json.dumps(value))
                self.assertFalse(cache.current('jl'))

    def test_changed_consumed_corpus_cannot_publish_completed_cache(self):
        with tempfile.TemporaryDirectory() as td:
            cache = c.SchemaCache('ai3'); cache.dir = Path(td) / 'ai3'
            source = Path(td) / 'ai1' / 'train.txt'; source.parent.mkdir(); source.write_text('old corpus')
            consumed = c.file_digest(source); source.write_text('new corpus')
            with self.assertRaisesRegex(ValueError, 'corpus changed'):
                cache.save('words', {'provenance': {'corpus_sha256': consumed}})
            self.assertFalse(cache.path('words').exists())


if __name__ == '__main__':
    unittest.main()
