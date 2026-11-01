"""Small independent mathematical fixtures; no production experiment or model load."""
import ast
import math
from contextlib import nullcontext
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest

import numpy as np
from scipy.integrate import quad

from videos.ai.ai5.contracts import (coin_sample_sizes, es_gradient, left_halfspace_reference,
                                     mixture_bin_density, rosen_smoothed_gradient,
                                     rosen_smoothed_minimum, rosen_smoothed_value)


class ProbabilityContractTests(unittest.TestCase):
    def test_coin_minimum_differs_from_eventual_threshold(self):
        result = coin_sample_sizes(.05, .05)
        exact = lambda n: sum(math.comb(n, k) for k in range((11 * n + 19) // 20, n + 1)) / 2 ** n
        self.assertEqual(result['minimum'], 262)
        self.assertEqual(result['eventual'], 281)
        self.assertLessEqual(exact(262), .05)
        self.assertGreater(exact(263), .05)
        for n in [271, 272, 280, 281]:
            self.assertAlmostEqual(result['probabilities'][n - 1], exact(n), places=13)
        self.assertGreater(exact(280), .05)
        self.assertTrue(all(exact(n) > .05 for n in range(1, 262)))
        self.assertTrue(all(exact(n) <= .05 for n in range(281, result['certified_cutoff'] + 1)))
        self.assertLessEqual(math.exp(-2 * result['certified_cutoff'] * .05 ** 2), .05)

    def test_iid_baseline_is_unbiased_by_exact_gaussian_quadrature(self):
        nodes, weights = np.polynomial.hermite.hermgauss(3)
        nodes, weights = nodes * math.sqrt(2), weights / math.sqrt(math.pi)
        corrected, old = 0., 0.
        for a, wa in zip(nodes, weights):
            for b, wb in zip(nodes, weights):
                e = np.array([[a], [b]])
                f = e[:, 0]
                corrected += wa * wb * es_gradient(f, e, 1, 'base')[0]
                old += wa * wb * np.mean((f - f.mean()) * f)
        self.assertAlmostEqual(corrected, 1., places=13)
        self.assertAlmostEqual(old, .5, places=13)
        mirrored = sum(w * es_gradient(np.array([a, -a]), np.array([[a], [-a]]), 1, 'mirror')[0]
                       for a, w in zip(nodes, weights))
        self.assertAlmostEqual(mirrored, 1., places=13)
        with self.assertRaises(ValueError):
            es_gradient([1, 2], [[1], [2]], 1, 'mirror')

    def test_smoothed_rosen_gradient_matches_integrated_objective(self):
        nodes, weights = np.polynomial.hermite.hermgauss(3)
        nodes, weights = nodes * math.sqrt(2), weights / math.sqrt(math.pi)
        def objective(theta):
            return sum(wa * wb * ((1 - theta[0] - .1 * a) ** 2 +
                       5 * (theta[1] + .1 * b - (theta[0] + .1 * a) ** 2) ** 2)
                       for a, wa in zip(nodes, weights) for b, wb in zip(nodes, weights))
        theta = np.array([-1.2, 1.4])
        finite_difference = [(objective(theta + h) - objective(theta - h)) / 2e-5
                             for h in np.eye(2) * 1e-5]
        np.testing.assert_allclose(rosen_smoothed_gradient(theta, .1), [-6.08, -.5], atol=1e-13)
        np.testing.assert_allclose(finite_difference, rosen_smoothed_gradient(theta, .1), atol=1e-7)
        self.assertAlmostEqual(objective(theta), float(rosen_smoothed_value(theta, .1)), places=12)

    def test_smoothed_minimum_moves_with_probe_variance(self):
        optimum = rosen_smoothed_minimum(.1)
        np.testing.assert_allclose(optimum, [5/6, 25/36 + .01], atol=1e-14)
        for sigma in [0., .1, .5]:
            best = rosen_smoothed_minimum(sigma)
            np.testing.assert_allclose(rosen_smoothed_gradient(best, sigma), 0, atol=1e-14)
            offsets = np.array([[0., 0.], [-.01, 0.], [.01, 0.], [0., -.01], [0., .01]])
            self.assertTrue(np.all(rosen_smoothed_value(best + offsets, sigma) >= rosen_smoothed_value(best, sigma)))
        self.assertLess(rosen_smoothed_value(optimum, .1), rosen_smoothed_value([1., 1.], .1))

    def test_halfspace_reference_matches_independent_integration(self):
        def density(x):
            return sum(w * math.exp(-(x - mu) ** 2 / (2 * v)) / math.sqrt(2 * math.pi * v)
                       for w, mu, v in [(2/3, -1.6, .35), (1/3, 1.5, .25)])
        mass = quad(density, -np.inf, 0)[0]
        first = quad(lambda x: x * density(x), -np.inf, 0)[0] / mass
        variance = quad(lambda x: (x - first) ** 2 * density(x), -np.inf, 0)[0] / mass
        result = left_halfspace_reference()
        self.assertAlmostEqual(result['mass'], mass, places=12)
        self.assertAlmostEqual(result['variance'], variance, places=12)
        self.assertNotAlmostEqual(result['variance'], .35, places=3)

    def test_multistart_cauchy_finds_cluster_outside_median_grid(self):
        path = Path(__file__).resolve().parents[1] / 'videos/ai/ai5/compute.py'
        node = next(n for n in ast.parse(path.read_text()).body
                    if isinstance(n, ast.FunctionDef) and n.name == '_cauchy_mle')
        scope = {'np': np}
        exec(compile(ast.Module([node], type_ignores=[]), str(path), 'exec'), scope)
        x = np.array([[0.] * 10 + list(np.arange(100, 1101, 100))])
        fitted, median, report = scope['_cauchy_mle'](x)
        self.assertEqual(median[0], 100)
        self.assertLess(abs(fitted[0]), .01)
        self.assertGreaterEqual(-np.log1p((x - fitted[:, None]) ** 2).sum(), -np.log1p(x * x).sum())
        self.assertEqual(report['stationary_count'], 1)
        self.assertFalse(report['global_optimum_certified'])

    def test_histogram_reference_integrates_real_bins_not_offset_points(self):
        edges = np.linspace(-4, 4, 81)
        weights, means, variances = np.array([.45, .55]), np.array([-1.5, 1.2]), np.array([.35**2, .5**2])
        def density(x):
            return sum(w * math.exp(-(x - mu)**2 / (2 * v)) / math.sqrt(2 * math.pi * v)
                       for w, mu, v in zip(weights, means, variances))
        mass = quad(density, -4, 4)[0]
        expected = [quad(density, a, b)[0] / (mass * (b-a)) for a, b in zip(edges[:-1], edges[1:])]
        result = mixture_bin_density(edges, means, variances, weights)
        np.testing.assert_allclose(result, expected, atol=3e-14)
        self.assertAlmostEqual(float(result @ np.diff(edges)), 1., places=13)
        offset_points = np.linspace(-4, 4, 401)[2::5][:80]
        self.assertGreater(np.max(np.abs(result - [density(x) for x in offset_points])), .005)

    def test_bayes_reads_observed_passage_not_warm_text_memo(self):
        path = Path(__file__).resolve().parents[1] / 'videos/ai/ai5/compute.py'
        tree = ast.parse(path.read_text())
        node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'compute_bayes')
        with tempfile.TemporaryDirectory() as directory:
            raw = 'eab' * 4001
            (Path(directory) / 'passage.txt').write_text(raw)
            def stale_text(*args):
                self.fail('memoized Part1 text was consulted instead of the current input bytes')
            fake = SimpleNamespace(DATA_DIR=Path(directory), to27=lambda s: s, text=stale_text)
            scope = {'np': np, 'ai1': lambda: fake, 'cache_lock': lambda p: nullcontext(),
                     'NS': [0, 10, 100, 1000, 10000]}
            exec(compile(ast.Module([node], type_ignores=[]), str(path), 'exec'), scope)
            result = scope['compute_bayes']()
            self.assertEqual(result['n_all'], len(raw))
            self.assertEqual(result['e_all'], 1/3)
            self.assertEqual(result['k10000'], raw[:10000].count('e'))


if __name__ == '__main__':
    unittest.main()
