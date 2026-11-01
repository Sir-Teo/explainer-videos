"""Inference/diagram lineage checks without scenes, caches or corpus loading."""
import ast
import copy
from functools import lru_cache
import math
from pathlib import Path
import unittest

import numpy as np
from scipy.special import logsumexp
from scipy.stats import multivariate_normal


ROOT = Path(__file__).resolve().parents[1]


def function(tree, name):
    return next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == name)


def pure_function(path, name, env, *, remove_part5_import=False):
    node = copy.deepcopy(function(ast.parse(path.read_text()), name))
    if remove_part5_import:
        node.body = [n for n in node.body if not (isinstance(n, ast.ImportFrom)
                     and n.module == "videos.ai.ai5.compute")]
    exec(compile(ast.Module([node], type_ignores=[]), "actual-pure-source-function", "exec"), env)
    return env[name]


@lru_cache(maxsize=1)
def fitted_grid_comparison():
    env = {"np": np, "math": math}
    density = pure_function(ROOT / "videos/ai/ai5/compute.py", "density2", env)
    source = ROOT / "videos/ai/ai7/compute.py"
    pure_function(source, "gauss_logpdf", env)
    vi = pure_function(source, "compute_vi", env, remove_part5_import=True)()
    x, y = np.meshgrid(np.linspace(-4, 4, 161), np.linspace(-3, 3, 121))
    grid = np.column_stack([x.ravel(), y.ravel()])
    logp = np.log(density(x, y).ravel())
    logp -= logsumexp(logp)
    p = np.exp(logp)

    def objective(theta):
        sd = np.exp(theta[2:4])
        correlation = np.tanh(theta[4])
        covariance = np.array([[sd[0]**2, correlation*np.prod(sd)],
                               [correlation*np.prod(sd), sd[1]**2]])
        # Independent density implementation and normalizer, not producer q_of.
        logq = multivariate_normal.logpdf(grid, mean=theta[:2], cov=covariance)
        logq -= logsumexp(logq)
        return float(p @ (logp-logq))

    mean = p @ grid
    covariance = ((grid-mean)*p[:, None]).T @ (grid-mean)
    sd = np.sqrt(np.diag(covariance))
    moment_start = np.r_[mean, np.log(sd), np.arctanh(covariance[0, 1]/np.prod(sd))]
    return vi, objective, moment_start


class BayesianSceneClaims(unittest.TestCase):
    def test_forward_grid_fit_is_stationary_for_the_actual_normalized_objective(self):
        result, objective, moment_start = fitted_grid_comparison()
        self.assertTrue(result["forward_optimizer"]["success"])
        theta = np.asarray(result["t_pq"])
        h = 1e-5
        gradient = lambda point: np.array([
            (objective(point+np.eye(5)[i]*h)-objective(point-np.eye(5)[i]*h))/(2*h)
            for i in range(5)])
        self.assertLess(np.linalg.norm(gradient(theta)), 1e-4)
        self.assertGreater(np.linalg.norm(gradient(moment_start)), .01)
        self.assertLess(objective(theta), objective(moment_start)-1e-4)
        self.assertAlmostEqual(result["kl_pq_final"], objective(theta), places=10)
        self.assertAlmostEqual(result["initial_forward_kl"], objective(moment_start), places=10)

    def test_saved_CAVI_contours_and_scores_share_the_final_sweep(self):
        select = pure_function(ROOT / "videos/ai/ai7/s17_vi.py", "cavi_display_states", {})
        qs = np.array([[10*i, (i+3)**2, 2+i, 20+i] for i in range(12)], dtype=float)
        elbo, kl = np.arange(12, dtype=float)-100, np.arange(12, dtype=float)/10
        original = qs.copy()
        states = select(qs, elbo, kl)
        self.assertEqual([s["sweep"] for s in states], [1, 2, 3, 12])
        for state in states:
            i = state["sweep"]-1
            np.testing.assert_array_equal(state["q"], qs[i])
            self.assertEqual(state["elbo"], elbo[i])
            self.assertEqual(state["kl"], kl[i])
        final = states[-1]
        self.assertEqual(final["index"], len(qs)-1)
        self.assertAlmostEqual(1/math.sqrt(final["q"][1]), 1/14)
        self.assertEqual(final["elbo"]+final["kl"], elbo[-1]+kl[-1])
        np.testing.assert_array_equal(qs, original)
        self.assertIsInstance(final["q"], tuple)

    def test_short_CAVI_histories_never_duplicate_or_invent_a_final_state(self):
        select = pure_function(ROOT / "videos/ai/ai7/s17_vi.py", "cavi_display_states", {})
        for n in (1, 2, 3):
            states = select([[0, 1, 2, 3]]*n, [0]*n, [1]*n)
            self.assertEqual([s["index"] for s in states], list(range(n)))
            self.assertEqual(states[-1]["sweep"], n)
        with self.assertRaises(ValueError):
            select([], [], [])
        with self.assertRaises(ValueError):
            select([[0, 1, 2, 3]], [], [1])
        with self.assertRaises(ValueError):
            select([[0, 1, 2, 3]], [0], [1], preview_updates=-1)


if __name__ == "__main__":
    unittest.main()
