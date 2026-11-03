"""Exercise the exact sampler's actual correction statements on synthetic distributions."""
import ast
from pathlib import Path
import unittest
import numpy as np

ROOT = Path(__file__).resolve().parents[1]

def actual_correction(p, q, seed=17, n=100000):
    source = ROOT / 'videos/ai/ai19/compute.py'
    tree = ast.parse(source.read_text())
    fn = next(x for x in tree.body if isinstance(x, ast.FunctionDef) and x.name == 'compute_exact')
    start = next(i for i, x in enumerate(fn.body) if isinstance(x, ast.Assign)
                 and any(isinstance(t, ast.Name) and t.id == 'resid' for t in x.targets))
    end = next(i for i in range(start, len(fn.body)) if isinstance(fn.body[i], ast.Assign)
               and any(isinstance(t, ast.Name) and t.id == 'y' for t in fn.body[i].targets))
    g = np.random.default_rng(seed); k = len(p)
    x = g.choice(k, n, p=q)
    acc = g.random(n) < np.minimum(1, p[x] / q[x])
    scope = {'np': np, 'p': p, 'q': q, 'g': g, 'K': k, 'N': n, 'x': x, 'acc': acc}
    exec(compile(ast.Module(fn.body[start:end+1], type_ignores=[]), str(source), 'exec'), scope)
    return np.bincount(scope['y'], minlength=k) / n

class SpeculativeCorrection(unittest.TestCase):
    def test_identical_distributions_do_not_divide_by_zero(self):
        p = np.array([.2, .3, .5])
        np.testing.assert_allclose(actual_correction(p, p), p, atol=.007)

    def test_asymmetric_distributions_recover_target(self):
        p, q = np.array([.05, .25, .7]), np.array([.55, .35, .1])
        np.testing.assert_allclose(actual_correction(p, q), p, atol=.007)

    def test_nonzero_residual_matches_original_seeded_recipe(self):
        p, q = np.array([.05, .25, .7]), np.array([.55, .35, .1])
        g = np.random.default_rng(17); n = 100000
        x = g.choice(len(p), n, p=q)
        acc = g.random(n) < np.minimum(1, p[x] / q[x])
        residual = np.maximum(p - q, 0); residual /= residual.sum()
        y = np.where(acc, x, g.choice(len(p), n, p=residual))
        np.testing.assert_array_equal(actual_correction(p, q), np.bincount(y, minlength=len(p)) / n)

if __name__ == '__main__':
    unittest.main()
