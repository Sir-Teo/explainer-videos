"""Independent numerical checks for Part 9's teaching examples."""
from itertools import combinations

import numpy as np
import pytest
from scipy import stats

from videos.stats.stats9.compute import (
    clipped_segments, compute_examples, compute_likelihood, gamma_mle,
    histogram_density, tank_estimates,
)


def test_tank_estimators_and_conditional_improvement_exhaustively():
    N, k = 9, 3
    samples = np.array(list(combinations(range(1, N + 1), k)))
    estimates = tank_estimates(samples)
    for name in ('mom', 'umvue', 'range'):
        assert estimates[name].mean() == pytest.approx(N)
    for maximum in range(k, N + 1):
        selected = samples.max(1) == maximum
        assert estimates['mom'][selected].mean() == pytest.approx(estimates['umvue'][selected][0])
    assert estimates['umvue'].var() == pytest.approx((N - k) * (N + 1) / (k * (k + 2)))
    assert estimates['umvue'].var() < estimates['mom'].var()
    assert np.any(estimates['max'] == N)  # The maximum can equal the truth.


def test_gamma_shape_and_scale_agree_with_scipy_fit():
    x = np.random.default_rng(91).gamma(2.5, 2, 70)
    shape, scale = gamma_mle(x)
    reference_shape, _, reference_scale = stats.gamma.fit(x, floc=0)
    assert shape == pytest.approx(reference_shape, rel=1e-8)
    assert scale == pytest.approx(reference_scale, rel=1e-8)


def test_likelihoods_are_relative_to_the_exact_maximum():
    d = compute_likelihood()
    p = np.asarray(d['ps'])
    for n in (10, 100, 1000):
        k = int(.7 * n)
        expected = stats.binom.logpmf(k, n, p) - stats.binom.logpmf(k, n, k / n)
        np.testing.assert_allclose(d[str(n)], expected, atol=1e-10)
    e = compute_examples()
    theta, likelihood = np.asarray(e['th']), np.asarray(e['u_lik'])
    at_max = theta == e['u_max']
    assert at_max.sum() == 1
    assert likelihood[at_max][0] == pytest.approx(1)
    assert (likelihood[theta < e['u_max']] == 0).all()
    expected = len(e['exp_x']) * np.log(np.asarray(e['rates']) / e['rate_hat']) - (np.asarray(e['rates']) - e['rate_hat']) * sum(e['exp_x'])
    np.testing.assert_allclose(e['exp_ll'], expected, atol=1e-12)


def test_histogram_keeps_offscreen_probability_mass():
    values = np.array([-9, .25, .75, 1.5, 9])
    edges = np.array([0, 1, 2])
    density = histogram_density(values, edges)
    assert (density * np.diff(edges)).sum() == pytest.approx(3 / 5)


def test_clipping_does_not_bridge_an_offscreen_excursion():
    segments = clipped_segments([0, 1, 2], [.5, 2, .5], (0, 2, 0, 1))
    assert len(segments) == 2
    np.testing.assert_allclose(segments[0][1], [1 / 3, 1])
    np.testing.assert_allclose(segments[1][0], [5 / 3, 1])
