"""Independent references for Part 5's probability and numerical examples."""

import numpy as np
import pytest
from scipy import stats

from videos.stats.stats5 import compute


def test_normal_ratio_retains_the_cauchy_tail_probability():
    result = compute.compute_jacobian()
    draws = np.asarray(result['ratio'])
    assert len(draws) == 40_000
    tail = np.mean(np.abs(draws) > 6)
    assert tail == pytest.approx(2 * stats.cauchy.sf(6), abs=.006)
    counts, edges = np.histogram(draws, np.linspace(-6, 6, 61))
    integral = np.sum(counts / (len(draws) * np.diff(edges)) * np.diff(edges))
    assert integral == pytest.approx(1 - tail)


def test_test_retest_uses_standard_units_and_gaussian_conditional_means():
    result = compute.compute_regression()
    # A standard normal's mean above its 90th percentile is phi(q)/0.1.
    expected_top = stats.norm.pdf(stats.norm.ppf(.9)) / .1
    assert result['best_t1'] == pytest.approx(expected_top, abs=.07)
    assert result['best_t2'] == pytest.approx(.5 * expected_top, abs=.07)
    assert result['worst_t1'] == pytest.approx(-expected_top, abs=.07)
    assert result['worst_t2'] == pytest.approx(-.5 * expected_top, abs=.07)
    assert np.std(result['t1']) == pytest.approx(1, abs=.05)


def test_ols_variance_components_add_without_a_hidden_cross_term():
    result = compute.compute_extras()['stable']
    assert result['b2vx'] + result['res'] == pytest.approx(result['vy'], abs=1e-12)
    x, y = compute.galton_points()
    slope = stats.linregress(x, y).slope
    assert result['b2vx'] == pytest.approx(slope ** 2 * np.var(x), abs=1e-12)


def test_copula_samplers_have_uniform_margins_and_match_their_target_tau():
    result = compute.compute_copulas()
    for key in ('gauss', 'clayton', 'gumbel'):
        pair = np.asarray(result[key]['uv'])
        for margin in pair.T:
            assert stats.kstest(margin, 'uniform').statistic < .05
        assert result[key]['tau'] == pytest.approx(.5, abs=.025)
    assert result['clayton']['lower'] > result['clayton']['upper'] + .4
    assert result['gumbel']['upper'] > result['gumbel']['lower'] + .15
