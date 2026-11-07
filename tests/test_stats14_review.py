"""Independent numerical references for Counts and Categories."""

import numpy as np
import pytest
import statsmodels.api as sm
from scipy import optimize, special

from videos.stats.stats14 import compute as c


def test_screening_design_counts_two_boolean_positives():
    X = c.screening_design([40, 50, 60, 70], [False, True, False, True],
                           [False, False, True, True])
    assert np.array_equal(X[:, 2], [0, 1, 1, 2])
    assert np.array_equal(X[:, 1], [-1, 0, 1, 2])


def test_scoring_pipeline_matches_independent_binomial_fit_and_training_baseline():
    actual = c.compute_scoring()
    g = c.rng(1997)
    adults = np.flatnonzero(c.W.adult)
    train = g.choice(adults, 50_000, replace=False)
    test = g.choice(np.setdiff1d(adults, train), 50_000, replace=False)
    s, age = c.W.screening, c.W.age
    yt, ye = s['sick'][train].astype(float), s['sick'][test].astype(float)
    def design(indices):
        return np.column_stack([np.ones(len(indices)), (age[indices]-50)/10,
            s['test_a'][indices].astype(int)+s['test_b'][indices].astype(int)])
    fit = sm.GLM(yt, design(train), family=sm.families.Binomial()).fit()
    predicted = fit.predict(design(test))
    assert actual['both_coef'] == pytest.approx(fit.params, abs=1e-7)
    assert actual['brier_both'] == pytest.approx(np.mean((predicted-ye)**2))
    assert actual['base_risk'] == pytest.approx(yt.mean())
    assert actual['brier_base'] == pytest.approx(np.mean((yt.mean()-ye)**2))
    assert yt.mean() != ye.mean()


def test_complete_separation_has_zero_supremum_without_finite_mle():
    for y in (np.zeros(23), np.ones(23), (c.T < 65).astype(float)):
        ll, fit, kind = c.logistic_supremum(y)
        assert ll == 0 and fit is None and kind == 'complete'


def test_quasi_separation_retains_entropy_of_mixed_tied_outcomes():
    threshold = next(t for t in np.unique(c.T) if np.sum(c.T == t) >= 2)
    y = (c.T < threshold).astype(float)
    tied = np.flatnonzero(c.T == threshold)
    y[tied[0]] = 1
    p = 1/len(tied)
    expected = np.log(p)+(len(tied)-1)*np.log1p(-p)
    ll, fit, kind = c.logistic_supremum(y)
    assert kind == 'quasi' and fit is None
    assert ll == pytest.approx(expected)
    eta = special.logit(p)+100*(threshold-c.T)
    finite_ll = np.sum(y*eta-np.logaddexp(0, eta))
    assert finite_ll == pytest.approx(ll, abs=1e-10)
    assert ll < 0


def test_finite_logistic_supremum_matches_statsmodels():
    ll, fit, kind = c.logistic_supremum(c.Y)
    reference = sm.GLM(c.Y, c.XC, family=sm.families.Binomial()).fit()
    assert kind is None and fit is not None
    assert ll == pytest.approx(reference.llf, abs=1e-9)
    assert fit.coef == pytest.approx(reference.params, abs=1e-7)
    assert fit.cov() == pytest.approx(reference.cov_params(), rel=1e-5)


def test_constrained_likelihoods_match_scalar_optimization():
    def loglik(eta):
        return np.sum(c.Y*eta-np.logaddexp(0, eta))
    for slope in (-.4, -.2322, -.05):
        reference = optimize.minimize_scalar(lambda a: -loglik(a+slope*c.T),
                                             bounds=(-10, 40), method='bounded')
        assert c._intercept_only(c.Y, slope*c.T)[1] == pytest.approx(-reference.fun, abs=1e-8)
    for eta31 in (1.5, 7.85, 18):
        reference = optimize.minimize_scalar(lambda b: -loglik(eta31+b*(c.T-31)),
                                             bounds=(-2, 1), method='bounded')
        assert c._ll_eta31_fixed(c.Y, eta31) == pytest.approx(-reference.fun, abs=1e-8)


def test_auc_awards_half_credit_for_ties_and_is_monotone_invariant():
    score = np.array([.1, .1, .4, .4, .4, .9])
    y = np.array([0, 1, 0, 1, 1, 0])
    differences = score[y == 1, None]-score[y == 0]
    expected = np.mean((differences > 0)+.5*(differences == 0))
    assert c.glm.roc(score, y)[2] == pytest.approx(expected)
    assert c.glm.roc(special.expit(special.logit(score)+np.log(4)), y)[2] == pytest.approx(expected)
