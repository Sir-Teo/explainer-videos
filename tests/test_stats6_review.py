"""Reference checks for Part 6's asymptotic diagnostics and extreme-value fit."""

import numpy as np
import pytest
from scipy import stats

from videos.stats.stats6 import compute


def test_normal_distance_checks_the_left_side_of_cdf_jumps():
    assert compute.normal_cdf_distance([2]) == pytest.approx(stats.norm.cdf(2))
    points = np.array([-2., .4, 1.2])
    masses = np.array([.1, .7, .2])
    # Compare a discrete scipy law immediately before and at every support point.
    law = stats.rv_discrete(values=(points, masses))
    probes = np.concatenate((points, np.nextafter(points, -np.inf)))
    expected = np.max(np.abs(law.cdf(probes) - stats.norm.cdf(probes)))
    assert compute.normal_cdf_distance(points, masses) == pytest.approx(expected)


def test_histogram_density_does_not_renormalize_omitted_tails():
    density = compute.histogram_density([-5, -1, 0, 1, 5], [-2, 0, 2])
    np.testing.assert_allclose(density, [.1, .2])
    assert np.dot(density, [2, 2]) == pytest.approx(.6)


def test_exact_sample_threshold_requires_a_successful_suffix():
    with pytest.raises(ValueError, match='increase hi'):
        compute.exact_n(.5, .01, .001, 1, 10)
    threshold, first = compute.exact_n(.5, .2, .2, 1, 40)
    passing = []
    for n in range(1, 41):
        k = np.arange(n + 1)
        mass = stats.binom.pmf(k, n, .5)[np.abs(k / n - .5) <= .2 + 1e-12].sum()
        passing.append(mass >= .8 - 1e-12)
    assert first == np.flatnonzero(passing)[0] + 1
    assert all(passing[threshold - 1:])
    assert threshold == 1 or not passing[threshold - 2]


def test_clipping_retains_crossing_slopes_and_omits_off_scale_plateaus():
    segments = compute.clipped_segments([0, 3], [-1, 2], [0, 3, 0, 1])
    np.testing.assert_allclose(segments, [[[1, 0], [2, 1]]])
    assert compute.clipped_segments([0, 1, 2], [2, 3, 2], [0, 2, 0, 1]) == []
    assert compute.clipped_segments([0, 1, 2], [0, np.nan, 1], [0, 2, 0, 1]) == []


@pytest.mark.parametrize('xi', [-.2, 0., .15])
def test_gev_likelihood_and_return_levels_match_scipy_conventions(xi):
    mu, scale = 3.8, .2
    x = np.array([3.6, 3.8, 3.9, 4.2])
    expected = -stats.genextreme.logpdf(x, -xi, loc=mu, scale=scale).sum()
    assert compute.gev_nll([mu, np.log(scale), xi], x) == pytest.approx(expected, abs=1e-12)
    for period in (2, 100, 10000):
        level = compute.return_level(mu, scale, xi, period)
        assert stats.genextreme.sf(level, -xi, loc=mu, scale=scale) == pytest.approx(1 / period, rel=1e-10)
