"""Numerical checks for Statistics, Built Part 3's distributions and encodings."""

import numpy as np
import pytest
from scipy import stats

from videos.stats.stats3 import compute


def test_binomial_poisson_distances_include_the_unbounded_poisson_tail():
    result = compute.compute_rare()
    for row in result['rows']:
        n, lam = row['n'], result['lam']
        # TV is the probability discrepancy on the event where binomial mass
        # exceeds Poisson mass. This avoids mirroring the half-L1 computation.
        support = np.arange(n + 1)
        b = stats.binom.pmf(support, n, lam / n)
        p = stats.poisson.pmf(support, lam)
        event = b > p
        expected = b[event].sum() - p[event].sum()
        assert row['tv'] == pytest.approx(expected, abs=2e-14)
        assert row['tv'] <= row['lecam']
    assert np.all(np.diff(result['tvs']) < 0)


def test_box_muller_coordinates_preserve_radius_and_recover_both_uniforms():
    result = compute.compute_transforms()
    x, y = result['z1'], result['z2']
    radius_squared = x * x + y * y
    np.testing.assert_allclose(np.exp(-radius_squared / 2), result['u1'], atol=1e-15)
    theta = np.mod(np.arctan2(y, x), 2 * np.pi)
    np.testing.assert_allclose(theta / (2 * np.pi), result['u2'], atol=1e-15)
    assert abs(np.corrcoef(x, y)[0, 1]) < .05


def test_student_scale_mixture_keeps_tail_draws_in_the_histogram_denominator():
    result = compute.compute_mixtures()
    draws = result['t_x']
    observed_tail = np.mean(np.abs(draws) > 6)
    expected_tail = 2 * stats.t.sf(6, result['nu'])
    assert observed_tail == pytest.approx(expected_tail, abs=.003)
    counts, edges = np.histogram(draws, np.linspace(-6, 6, 61))
    integrated_density = (counts / (len(draws) * np.diff(edges)) * np.diff(edges)).sum()
    assert integrated_density == pytest.approx(1 - observed_tail)
    assert integrated_density < 1


def test_zipf_reference_line_is_the_fitted_line_rather_than_anchored_at_first_town():
    result = compute.compute_tails()
    x = np.log(result['ranks'][:150])
    y = np.log(result['pops'][:150])
    residuals = y - (result['intercept_rank'] + result['slope_rank'] * x)
    assert residuals.sum() == pytest.approx(0, abs=1e-10)
    assert np.dot(x, residuals) == pytest.approx(0, abs=1e-10)

