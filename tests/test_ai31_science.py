"""Scientific contract regressions for Part31; no shared models or datasets are generated."""
import inspect
import json
import math
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import numpy as np
import torch

from videos.ai.ai31 import compute as C, sims as S


class Part31ScienceTests(unittest.TestCase):
    def test_online_and_batch_ratings_share_an_origin(self):
        with patch.object(S, 'best_of_k_inflation', return_value=np.zeros(5)):
            d = C.compute_arena(n_total=10_000, checkpoints=(100,), boots=2)
        origin = np.mean(d['true'])
        np.testing.assert_allclose(d['elo_path'].mean(1), origin, atol=1e-10)
        np.testing.assert_allclose(d['elo_perm'].mean(1), origin, atol=1e-10)
        self.assertAlmostEqual(d['bt10'].mean(), origin)

    def test_legacy_scientific_outputs_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(C.CACHE, 'dir', Path(directory)):
            for name in C.RECIPES:
                C.CACHE.path(name).write_text('{}')
                with self.assertRaisesRegex(ValueError, '--force'):
                    C.load(name)

    def test_missing_results_never_dispatch_producers_or_write_caches(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(C.CACHE, 'dir', Path(directory)):
            with patch.dict(C.ITEMS, {'w2s': lambda: self.fail('producer dispatched')}):
                with self.assertRaisesRegex(FileNotFoundError, 'Restore and review'):
                    C.load('w2s')
            self.assertEqual(list(Path(directory).iterdir()), [])

    def test_existing_result_is_read_only_and_array_metadata_cannot_override_recipe(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(C.CACHE, 'dir', Path(directory)):
            path = C.CACHE.path('hacking')
            path.write_text(json.dumps({'recipe': C.RECIPES['hacking']}))
            np.savez(path.with_suffix('.npz'), rewards=np.array([0., 1.]))
            before = {p.name: p.read_bytes() for p in Path(directory).iterdir()}
            np.testing.assert_array_equal(C.load('hacking')['rewards'], [0., 1.])
            self.assertEqual(before, {p.name: p.read_bytes() for p in Path(directory).iterdir()})
            np.savez(path.with_suffix('.npz'), recipe=np.array('legacy'))
            with self.assertRaisesRegex(ValueError, 'conflicting'):
                C.load('hacking')
            path.write_text('{}')
            np.savez(path.with_suffix('.npz'), recipe=np.array(C.RECIPES['hacking']))
            with self.assertRaisesRegex(ValueError, 'conflicting'):
                C.load('hacking')

    def test_render_text_reads_never_dispatch_corpus_generation(self):
        from videos.ai.ai1 import compute as c1

        with tempfile.TemporaryDirectory() as directory, patch.object(c1, 'DATA_DIR', Path(directory)):
            with patch.object(c1, 'compute_corpus', side_effect=AssertionError('corpus producer dispatched')):
                with self.assertRaisesRegex(FileNotFoundError, 'restore and review'):
                    C._dp_text()
                with self.assertRaises(FileNotFoundError):
                    C.read_original_text('passage')
                self.assertEqual(list(Path(directory).iterdir()), [])
                (Path(directory) / 'train.txt').write_text('Abc  DEF! xyz')
                (Path(directory) / 'valid.txt').write_text('ABC! DEF')
                self.assertEqual(C._dp_text(), (' def xyz', 'abc def'))

    def test_upstream_reader_rejects_missing_or_stale_without_calling_its_loader(self):
        from videos.ai.ai1 import compute as c1

        with tempfile.TemporaryDirectory() as directory, patch.object(c1, 'DATA_DIR', Path(directory)):
            with patch.object(c1, 'load', side_effect=AssertionError('upstream loader dispatched')):
                with self.assertRaises(FileNotFoundError):
                    C.read_upstream(c1, 'scoreboard')
                self.assertEqual(list(Path(directory).iterdir()), [])
                path = c1.path('scoreboard')
                with patch.dict(c1.CACHE_SCHEMAS, {'scoreboard': 2}):
                    path.write_text('{"schema_version": 1}')
                    with self.assertRaisesRegex(ValueError, 'stale'):
                        C.read_upstream(c1, 'scoreboard')
                    path.write_text('{"schema_version": 2, "rows": []}')
                    before = path.read_bytes()
                    self.assertEqual(C.read_upstream(c1, 'scoreboard')['rows'], [])
                    self.assertEqual(path.read_bytes(), before)

    def test_poisson_inclusion_has_no_duplicate_records(self):
        for q in (0.0, 0.17, 1.0):
            g = torch.Generator().manual_seed(3)
            pick = C._poisson_indices(128, q, g)
            self.assertEqual(len(pick), len(pick.unique()))
            if q in (0.0, 1.0):
                self.assertEqual(len(pick), int(128*q))

    def test_empty_poisson_batches_still_add_noise(self):
        args = dict(text='abcde abcde abcde', valid='abcde abcde abcde', private=True,
                    steps=2, sample_rate=0.0, expected_batch=4)
        zero, _, _ = C._dp_train(**args, sigma=0.0)
        noise, held, _ = C._dp_train(**args, sigma=1.0)
        x = torch.zeros((1, 10), dtype=torch.long)
        self.assertTrue(math.isfinite(held))
        self.assertFalse(torch.equal(zero(x), noise(x)))
        self.assertEqual(noise.clipped, 0.0)

    def test_clipped_sum_matches_per_record_autograd(self):
        text='abcde abcde '; ctx=10; clip=.03; expected_batch=4; V=len(C.DP_ALPHABET)
        g=torch.Generator().manual_seed(0)
        P={'emb':.3*torch.randn(V,12,generator=g),
           'W1':torch.randn(160,120,generator=g)/math.sqrt(120),
           'b1':torch.zeros(160),'W2':torch.randn(V,160,generator=g)/math.sqrt(160),
           'b2':torch.zeros(V)}
        P={k:v.requires_grad_() for k,v in P.items()}
        ix={c:i for i,c in enumerate(C.DP_ALPHABET)}
        X=torch.tensor([ix[c] for c in text]).unfold(0,ctx+1,1)
        sums={k:torch.zeros_like(v) for k,v in P.items()}
        for row in X:
            logits=torch.tanh(P['emb'][row[:-1]].flatten()@P['W1'].T+P['b1'])@P['W2'].T+P['b2']
            loss=torch.nn.functional.cross_entropy(logits[None],row[-1:])
            grads=torch.autograd.grad(loss,tuple(P.values()))
            norm=torch.sqrt(sum((v*v).sum() for v in grads))
            factor=min(1.0,clip/float(norm))
            for k,grad in zip(P,grads):sums[k]+=factor*grad
        trained,_,_=C._dp_train(text,text,True,steps=1,clip=clip,sigma=0.0,lr=.5,
                               sample_rate=1.0,expected_batch=expected_batch)
        actual=inspect.getclosurevars(trained).nonlocals['P']
        for k in P:
            expected=P[k].detach()-.01*sums[k]/expected_batch
            torch.testing.assert_close(actual[k],expected,atol=2e-7,rtol=1e-5)

    def test_timeout_has_zero_terminal_potential(self):
        class OneStep:
            start=(0,0); horizon=1; dist={(0,0):10,(0,1):9}
            def n_states(self):return 2
            def index(self,r,c,last):return c
            def step(self,r,c,last,a):return 0,1,0,0.0,False
        _,_,Q=S.q_learning(OneStep(),mode='shaped',episodes=1,alpha=1.0,seed=0)
        np.testing.assert_array_equal(Q,np.zeros_like(Q))

    def test_accountant_matches_published_reference(self):
        self.assertAlmostEqual(C.rdp_epsilon(.01,4,10_000,1e-5),1.25857474125,places=8)

if __name__=='__main__':unittest.main()
