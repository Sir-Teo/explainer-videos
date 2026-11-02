"""Portable synthetic dependency/math contracts; no scene/cache/model imports.

Run with unittest discovery. In a repository this reads videos/ai/ai13/compute.py;
in the isolated source candidate it reads the adjacent compute.py. All page data
below are invented, and the upstream pages contract is represented by a fake.
"""
import ast
import copy
import math
from pathlib import Path
import types
import unittest

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'videos/ai/ai13/compute.py'
if not SOURCE.exists():
    SOURCE = ROOT / 'compute.py'


def recipe(provider):
    """Compile only the function body; never import the real producer module."""
    tree = ast.parse(SOURCE.read_text())
    fn = copy.deepcopy(next(n for n in tree.body if isinstance(n, ast.FunctionDef)
                            and n.name == 'compute_smoother'))
    assert isinstance(fn.body[0], ast.ImportFrom)
    assert fn.body[0].module == 'videos.ai.ai7'
    assert [(a.name, a.asname) for a in fn.body[0].names] == [('compute', 'c7')]
    fn.body = fn.body[1:]
    env = {'np': np, 'c7': provider}
    exec(compile(ast.Module(body=[fn], type_ignores=[]), '<isolated-smoother>', 'exec'), env)
    return env['compute_smoother']


def invented_pages(permuted=False):
    # Interleave books; only original row order within book1400 should be used.
    X = np.array([[1., 0., 8.], [9., 99., 6.], [2., 4., 3.],
                  [7., 88., 2.], [5., 1., 4.], [4., 7., 1.]])
    book = np.array([1400, 17, 1400, 17, 1400, 1400])
    vocab = ['other', 'her', 'word']
    if permuted:
        X, vocab = X[:, [1, 2, 0]].astype(int), ['her', 'word', 'other']
    return X, np.array([1, 0, 1, 0, 1, 1]), book, vocab


class Reader:
    def __init__(self, pages=None, failure=None):
        self.data, self.failure, self.calls = pages, failure, 0
    def pages(self):
        self.calls += 1
        if self.failure:
            raise self.failure
        return self.data
    def load(self, name):
        raise AssertionError('No fitted GP or other cached experiment may be loaded')


def quotient(x, y, at, h, omit=None):
    # Scalar fsum reference, independent of NumPy matrix broadcasting.
    scores = [-.5*((float(at)-float(t))/float(h))**2 for t in x]
    if omit is not None:
        scores[omit] = -math.inf
    maximum = max(scores)
    raw = [math.exp(v-maximum) for v in scores]
    total = math.fsum(raw)
    weights = np.array([v/total for v in raw])
    return math.fsum(w*float(v) for w,v in zip(weights,y)), weights


class SmootherPagesDependency(unittest.TestCase):
    def test_raw_observation_projection_uses_validated_reader_once(self):
        for permuted in (False, True):
            pages = invented_pages(permuted)
            saved = copy.deepcopy(pages)
            provider = Reader(pages)
            out = recipe(provider)()
            self.assertEqual(provider.calls, 1)
            np.testing.assert_array_equal(out['x'], [0.,1.,2.,3.])
            np.testing.assert_array_equal(out['y'], [0.,4.,1.,7.])
            for a,b in zip(pages[:3],saved[:3]):
                np.testing.assert_array_equal(a,b)
            self.assertEqual(pages[3],saved[3])

    def test_every_saved_fit_weight_query_and_error_matches_scalar_reference(self):
        out = recipe(Reader(invented_pages()))()
        x,y = out['x'],out['y']
        self.assertEqual(out['hs'], [.6,2.5,10.])
        self.assertEqual(out['q'],120.)
        self.assertEqual(len(out['xs']),400)
        self.assertEqual((out['xs'][0],out['xs'][-1]),(0.,3.))
        for i,h in enumerate(out['hs']):
            tag = f'{h:g}'
            fits = [quotient(x,y,t,h)[0] for t in out['xs']]
            np.testing.assert_allclose(out['fit'+tag],fits,rtol=1e-12,atol=1e-12)
            at,w = quotient(x,y,out['q'],h)
            np.testing.assert_allclose(out['w'+tag],w,rtol=1e-12,atol=1e-12)
            self.assertAlmostEqual(out['at'+tag],at)
            self.assertAlmostEqual(float(out['w'+tag].sum()),1.)
            self.assertTrue(np.all(out['w'+tag]>=0))
            training = np.array([quotient(x,y,t,h)[0] for t in x])
            self.assertAlmostEqual(out['fit_mse'][i],float(np.mean((training-y)**2)))

    def test_leave_one_out_excludes_self_and_selects_only_the_saved_grid(self):
        out = recipe(Reader(invented_pages()))()
        expected = [float(np.mean([(quotient(out['x'],out['y'],t,h,j)[0]-out['y'][j])**2
                                  for j,t in enumerate(out['x'])])) for h in out['loo_h']]
        self.assertEqual(len(out['loo_h']),40)
        np.testing.assert_allclose(out['loo'],expected,atol=1e-11,rtol=1e-12)
        self.assertEqual(out['best_h'],float(out['loo_h'][np.argmin(out['loo'])]))
        self.assertFalse(np.allclose(out['fit_mse'][0],out['loo'][0]))

    def test_upstream_contract_failure_propagates_without_gp_fallback(self):
        provider = Reader(failure=RuntimeError('Retained pages contract failed'))
        with self.assertRaisesRegex(RuntimeError,'Retained pages contract failed'):
            recipe(provider)()
        self.assertEqual(provider.calls,1)

    def test_missing_word_fails_without_loading_gp(self):
        pages = list(invented_pages())
        pages[3] = ['other','missing','word']
        with self.assertRaises(ValueError):
            recipe(Reader(tuple(pages)))()

    def test_constant_response_is_preserved_without_forcing_unique_loo_choice(self):
        pages = list(invented_pages())
        pages[0] = pages[0].copy()
        pages[0][:,1] = 3.
        out = recipe(Reader(tuple(pages)))()
        for h in out['hs']:
            np.testing.assert_allclose(out[f'fit{h:g}'],3.,atol=1e-13)
        np.testing.assert_allclose(out['loo'],0.,atol=1e-25)
        self.assertIn(out['best_h'],out['loo_h'])


if __name__ == '__main__':
    unittest.main()
