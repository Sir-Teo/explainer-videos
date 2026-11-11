"""Independent invariants for the separately named credit teaching examples."""
import numpy as np
from scipy.integrate import solve_ivp
from videos.quant.quant20.synthetic_credit_example import (population, tied_roc, fit_preprocessor, transform,
                                                          rmv_curves)
from explainer.quant.house.credit import auc


def test_synthetic_equity_identity_and_independent_samples():
    x, y, p = population(2000, 123)
    x2, _, _ = population(2000, 124)
    assert np.allclose(x[:, 10], x[:, 9] + np.log(x[:, 6]) + np.log(x[:, 3]))
    assert set(np.unique(y)) == {0, 1} and np.all((p > 0) & (p < 1))
    assert not np.array_equal(x, x2)
    prep = fit_preprocessor(x)
    frozen = {k: v.copy() for k, v in prep.items()}
    transform(x2 * 100, prep)
    assert all(np.array_equal(prep[k], v) for k, v in frozen.items())


def test_roc_ties_move_together_and_match_rank_probability():
    y = np.array([1, 0, 1, 0, 1, 0])
    score = np.array([.7, .7, .7, .2, .2, .1])
    fp, tp = tied_roc(y, score)
    assert len(fp) == 4 and (fp[0], tp[0], fp[-1], tp[-1]) == (0, 0, 1, 1)
    pairwise = ((score[y == 1, None] > score[y == 0]).mean()
                + .5 * (score[y == 1, None] == score[y == 0]).mean())
    assert np.isclose(np.trapezoid(tp, fp), pairwise)
    assert np.isclose(auc(y, score), pairwise)


def test_exact_cir_rmv_matches_independent_riccati_solution():
    d = rmv_curves(); t = np.asarray(d['T']); a = 1 - d['R']
    def ode(_, state):
        A, B = state
        return [-d['kappa'] * d['theta'] * B, a - d['kappa'] * B - .5 * d['sigma'] ** 2 * B * B]
    solution = solve_ivp(ode, [0, t[-1]], [0, 0], t_eval=t, rtol=1e-11, atol=1e-13)
    for curve in d['curves'].values():
        expected = -(solution.y[0] - solution.y[1] * curve['l0']) / t * 1e4
        assert np.allclose(curve['spread_bp'], expected, rtol=1e-9, atol=1e-8)
        # Concavity of x^(1-R): E[S^(1-R)] <= E[S]^(1-R).
        assert np.all(np.asarray(curve['spread_bp']) >= np.asarray(curve['legacy_approx_bp']) - 1e-8)
