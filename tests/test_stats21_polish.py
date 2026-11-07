"""Independent mathematical checks for Part 21's corrected demonstrations."""
import numpy as np
import pytest
from scipy.optimize import brentq, minimize
from scipy.special import expit

from videos.stats.stats21 import compute as C
from explainer.stats.kit import optim as O


def test_profile_curvature_accounts_for_the_nuisance_intercept():
    X, y = C.vote_data(800, 21)
    fit = O.logistic_scoring(X, y)
    a, b = fit['b']
    def profile(v):
        intercept = brentq(lambda u: np.sum(y - expit(u + v * X[:, 1])), -50, 50)
        eta = intercept + v * X[:, 1]
        return np.sum(y * eta - np.logaddexp(0, eta))
    h = 1e-4
    curvature = -(profile(b+h)-2*profile(b)+profile(b-h))/h**2
    d = C.compute_convex()
    assert d['profile_se'] == pytest.approx(1/np.sqrt(curvature), rel=1e-5)
    assert d['profile_se'] >= 1/np.sqrt(fit['info'][1, 1])
    # Profiling can only improve on fixing the intercept at its joint MLE.
    assert np.all(np.asarray(d['profile']) >= np.asarray(d['logistic']) - 1e-9)


def test_tv_banded_solver_matches_an_independent_constrained_optimizer():
    y = np.array([0., -.3, .2, 2., 1.6, 2.2, -.5, -.7])
    lam = .6
    n = len(y)
    D = np.diff(np.eye(n), axis=0)
    # Epigraph formulation: minimize .5||y-b||² + lambda sum(t), with t >= +/- Db.
    ref = minimize(lambda v: .5*np.sum((y-v[:n])**2)+lam*v[n:].sum(),
                   np.r_[y, np.abs(D@y)], method='SLSQP',
                   constraints={'type':'ineq','fun':lambda v: np.r_[v[n:]-D@v[:n],v[n:]+D@v[:n]]},
                   options={'ftol':1e-12,'maxiter':1000})
    assert ref.success
    got = C.fused_lasso(y, lam, iters=3000)
    np.testing.assert_allclose(got['b'], ref.x[:n], atol=2e-6)
    assert got['primal_res'][-1] < 1e-10
    assert got['dual_res'][-1] < 1e-10
    assert C.fused_lasso([3.], .5)['b'][0] == 3


def test_world_target_solves_the_census_score_equation():
    b = C.population_vote_target()
    X = np.column_stack([np.ones(len(C._li)), (C._li-C.Z_MEAN)/C.Z_SD])
    y = C.W.survey['vote_blue'][C.W.adult].astype(float)
    assert len(y) == C.W.adult.sum()
    assert np.max(np.abs(X.T@(y-expit(X@b)))) < 1e-7


def test_clipping_preserves_crossings_without_flattening_or_bridging_missing_data():
    segments = C.clipped_segments([0,1,2,3,4], [.5,2,np.nan,2,.5], (0,4,0,1))
    assert len(segments) == 2
    np.testing.assert_allclose(segments[0][0], [0,.5])
    np.testing.assert_allclose(segments[0][1], [1/3,1])
    np.testing.assert_allclose(segments[1][0], [11/3,1])
    np.testing.assert_allclose(segments[1][1], [4,.5])


def test_lasso_equality_at_the_kkt_threshold_does_not_force_a_zero():
    X = np.eye(2)*np.sqrt(2)
    y = np.array([3., .2])
    lam = .5
    fit = O.cd_lasso(X, y, lam, sweeps=2)['b']
    score = X.T@(y-X@fit)/2
    assert fit[0] > 0
    assert abs(score[0]) == pytest.approx(lam)
    assert fit[1] == 0
    assert abs(score[1]) < lam
