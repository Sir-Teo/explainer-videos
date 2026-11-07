"""Independent numerical references for the least-squares illustrations."""

import numpy as np
import pytest
import statsmodels.api as sm
from scipy import optimize, stats

from explainer.stats import museum
from explainer.stats.kit import ols
from videos.stats.stats12.compute import (
    compute_collin, compute_fallacy, compute_hetsim, histogram_density,
)


def test_full_mass_histograms_do_not_renormalize_cropped_tails():
    edges = np.array([0., 1., 3.])
    assert histogram_density([-100, .5, 2, 2, 100], edges) == pytest.approx([.2, .2])
    assert np.dot(histogram_density([-100, .5, 2, 2, 100], edges), np.diff(edges)) == pytest.approx(.6)


def test_anscombe_absolute_loss_matches_independent_linear_program():
    x, y = map(np.asarray, museum.ANSCOMBE[3])
    X = np.column_stack([np.ones(len(x)), x])
    n = len(x)
    # Minimize sum of nonnegative absolute-residual slack variables.
    program = optimize.linprog(np.r_[0., 0., np.ones(n)],
        A_ub=np.r_[np.c_[X, -np.eye(n)], np.c_[-X, -np.eye(n)]],
        b_ub=np.r_[y, -y], bounds=[(None, None)] * 2 + [(0, None)] * n, method='highs')
    assert program.success
    estimate = ols.lad(x, y)
    assert abs(y - X @ estimate).sum() == pytest.approx(program.fun, abs=2e-5)


def test_heteroskedastic_oracle_covariance_matches_fixed_design_simulation():
    d = compute_hetsim()
    x = np.asarray(d['x'])
    X = ols.design(x)
    g = np.random.default_rng(1234)
    responses = 1 + x[:, None] + x[:, None] * g.normal(size=(len(x), 30000))
    estimates = np.linalg.lstsq(X, responses, rcond=None)[0]
    assert estimates.std(axis=1) == pytest.approx(d['oracle_se'], rel=.015)


def test_joint_confidence_ellipse_uses_f_cutoff_with_estimated_variance():
    d = compute_collin()
    for case in d.values():
        C = np.asarray(case['cov'])
        cutoff = 2 * stats.f.ppf(.95, 2, case['df'])
        # Every direction of the displayed ellipse has the same joint Wald/F value.
        root = np.linalg.cholesky(C)
        for angle in np.linspace(0, 2*np.pi, 20):
            delta = np.sqrt(cutoff) * root @ [np.cos(angle), np.sin(angle)]
            F = delta @ np.linalg.solve(C, delta) / 2
            assert stats.f.sf(F, 2, case['df']) == pytest.approx(.05)
        assert cutoff > stats.chi2.ppf(.95, 2)


def test_fwl_and_omitted_variable_identity_match_full_model_reference():
    g = np.random.default_rng(1933)
    z = g.normal(size=80)
    x = .6*z + g.normal(size=80)
    y = 1 + .08*x + .1*z + g.normal(size=80)
    full = sm.OLS(y, ols.design(x, z)).fit()
    short = ols.fit(ols.design(x), y)
    auxiliary = ols.fit(ols.design(x), z)
    rx = sm.OLS(x, ols.design(z)).fit().resid
    ry = sm.OLS(y, ols.design(z)).fit().resid
    assert np.dot(rx, ry) / np.dot(rx, rx) == pytest.approx(full.params[1])
    assert short.coef[1] == pytest.approx(full.params[1] + full.params[2] * auxiliary.coef[1])


def test_selected_score_gain_has_correct_population_sd_units():
    d = compute_fallacy()
    # For two tests = stable N(0,1) ability + independent N(0,1) noise,
    # E[test2 | test1] = test1 / 2. Selection of the lowest decile therefore
    # creates this apparent gain even without a treatment effect.
    theoretical_raw_gain = stats.norm.pdf(stats.norm.ppf(.1)) / (.1 * np.sqrt(2))
    assert d['gain'] == pytest.approx(theoretical_raw_gain, abs=.1)
    assert d['gain_sd'] == pytest.approx(d['gain'] / np.sqrt(2))
