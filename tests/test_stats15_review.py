"""Independent probability and integration checks for First Bayes."""

import numpy as np
import pytest
from scipy import integrate, special, stats

from videos.stats.stats15 import compute as c


def test_laplace_tiny_tail_matches_binomial_identity_without_normal_approximation():
    d = c.compute_laplace()
    reference = stats.binom.sf(d['a']-1, d['a']+d['b']-1, .5)
    assert d['exact'] == pytest.approx(reference, rel=1e-9, abs=0)
    assert d['log10_p'] == pytest.approx(np.log10(reference))


def test_predictive_and_plugin_share_mean_and_obey_total_variance():
    d = c.compute_predictive()
    k, a, b, m = np.arange(11), 9, 5, 10
    mu, variance = a/(a+b), stats.beta.var(a, b)
    assert k @ d['pred'] == pytest.approx(m*mu)
    assert k @ d['plug'] == pytest.approx(m*mu)
    assert d['pred_sd']**2-d['plug_sd']**2 == pytest.approx(m*(m-1)*variance)
    for j in (0, 5, 10):
        reference = integrate.quad(lambda p: stats.binom.pmf(j, m, p)*stats.beta.pdf(p, a, b), 0, 1)[0]
        assert d['pred'][j] == pytest.approx(reference)


def test_grid_rectangle_and_resolution_converge_for_slope_mean_and_tail():
    d = c.compute_grid()
    x, y = np.linspace(-30, 140, 1701), np.linspace(-2, .4, 1441)
    # Integrate in rows to avoid constructing a large likelihood tensor.
    marginal = np.array([np.trapezoid(np.exp(c.challenger_logpost(x, np.array(b))), x) for b in y])
    marginal /= np.trapezoid(marginal, y)
    assert d['b1_mean'] == pytest.approx(np.trapezoid(marginal*y, y), abs=2e-5)
    cutoff = np.r_[y[y < 0], 0.]
    probability = np.trapezoid(np.interp(cutoff, y, marginal), cutoff)
    assert d['p_b1_neg'] == pytest.approx(probability, abs=2e-5)
    assert sum(d['p31_hist']) == pytest.approx(1)


def test_grid_marginal_ratio_matches_adaptive_quadrature():
    d = c.compute_grid()
    estimates = np.interp([-.2, -.4], d['gy'], d['my'])
    reference = [integrate.quad(lambda a: np.exp(c.challenger_logpost(np.array(a), np.array(b))),
                                 -20, 100, epsabs=1e-14, epsrel=1e-9)[0] for b in (-.2, -.4)]
    assert estimates[0]/estimates[1] == pytest.approx(reference[0]/reference[1], rel=1e-7)


def test_conjugate_mixture_updates_component_weights_and_probability():
    d = c.compute_mixture()
    evidence = np.array([integrate.quad(lambda p: stats.beta.pdf(p, a, a)*p**7*(1-p)**3,
                                        0, 1, epsabs=1e-12)[0] for a in (50, 1)])
    weights = evidence/evidence.sum()
    assert d['weights'] == pytest.approx(weights)
    prior = lambda p: .5*stats.beta.pdf(p, 50, 50)+.5
    numerator = integrate.quad(lambda p: prior(p)*p**7*(1-p)**3, .4, .6)[0]
    assert d['p_near'] == pytest.approx(numerator/(.5*evidence.sum()))


def test_prior_averaged_coverage_is_exact_without_pointwise_guarantee():
    n, a, b = 50, 18, 2
    k = np.arange(n+1)
    lo, hi = stats.beta.ppf(np.array([.025, .975])[:, None], a+k, b+n-k)
    weights = stats.betabinom.pmf(k, n, a, b)
    mass = stats.beta.cdf(hi, a+k, b+n-k)-stats.beta.cdf(lo, a+k, b+n-k)
    assert weights @ mass == pytest.approx(.95)
    assert np.all(lo > .05)  # Every possible sample misses this fixed truth.


def test_odds_summaries_use_all_retained_draws():
    chain = c.B.metropolis(lambda t: float(c.challenger_logpost_c(np.array(t[0]), np.array(t[1]))),
                           [0., 0.], (1., .1), 20_000, c.rng(1954))
    odds = np.exp(-10*chain.draws[2000:, 1])
    d = c.compute_mcmc()
    assert d['or_median'] == pytest.approx(np.median(odds))
    assert d['or_ci'] == pytest.approx(np.quantile(odds, [.025, .975]))
    assert d['p_or_gt5'] == pytest.approx(np.mean(odds > 5))
