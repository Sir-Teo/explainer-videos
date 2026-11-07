"""Independent numerical checks for Part 11's interval claims."""

import itertools

import numpy as np
import pytest
from scipy import stats

from explainer.stats.kit import intervals as I
from videos.stats.stats11.compute import (
    clipped_segments,
    compute_likelihood,
    empirical_cdf_sup,
    jeffreys_credible,
    mid_p,
)


def test_whole_cdf_sup_matches_exhaustive_finite_populations_with_ties():
    # Midpoints and the support enumerate every distinct pair of CDF values.
    population = np.array([0, 0, 1, 3, 3, 8.0])
    probes = np.array([-1, 0, .5, 1, 2, 3, 5.5, 8, 9])
    truth = np.mean(population[:, None] <= probes, axis=0)
    for sample in itertools.product([0.0, 1.0, 3.0, 8.0], repeat=3):
        observed = np.mean(np.asarray(sample)[:, None] <= probes, axis=0)
        assert empirical_cdf_sup(sample, population) == pytest.approx(max(abs(observed - truth)))
    # Checking a plotting grid can entirely miss a discrepancy in a narrow gap.
    assert empirical_cdf_sup([0, 1], [.1, 1]) == .5
    assert np.array_equal(np.searchsorted([0, 1], [-1, 2]), np.searchsorted([.1, 1], [-1, 2]))


def test_likelihood_uses_exact_peak_and_lr_endpoints_agree():
    d = compute_likelihood()
    ps, ll = np.asarray(d['ps']), np.asarray(d['ll'])
    peak = np.flatnonzero(ps == d['x'] / d['n'])
    assert len(peak) == 1
    assert ll[peak[0]] == pytest.approx(0, abs=1e-14)
    top = stats.binom.logpmf(d['x'], d['n'], d['x'] / d['n'])
    for endpoint in d['ints']['lr']:
        drop = 2 * (top - stats.binom.logpmf(d['x'], d['n'], endpoint))
        assert drop == pytest.approx(stats.chi2.ppf(.95, 1), abs=1e-8)


def test_credible_intervals_retain_posterior_mass_at_boundary_counts():
    for x in (0, 1, 10, 20):
        lo, hi = jeffreys_credible(x, 20)
        posterior = stats.beta(x + .5, 20 - x + .5)
        assert posterior.cdf(lo) == pytest.approx(.025)
        assert posterior.sf(hi) == pytest.approx(.025)
    # The frequentist boundary modification deliberately changes posterior mass.
    assert I.jeffreys(0, 20)[0] == 0 < jeffreys_credible(0, 20)[0]


def test_midp_inverts_half_mass_tails_and_distinguishes_poisson_sides():
    for x in (1, 4, 24):
        lo, hi = mid_p(x, 25)
        assert stats.binom.sf(x, 25, lo) + stats.binom.pmf(x, 25, lo) / 2 == pytest.approx(.025)
        assert stats.binom.cdf(x - 1, 25, hi) + stats.binom.pmf(x, 25, hi) / 2 == pytest.approx(.025)
    assert stats.chi2.ppf(.975, 2) / 2 == pytest.approx(-np.log(.025))
    assert -np.log(.05) < stats.chi2.ppf(.975, 2) / 2


def test_offscreen_coverage_is_clipped_geometrically_without_false_floor():
    result = list(clipped_segments([0, 1, 2, 3], [.9, .5, .5, .9], (0, 3, .8, 1)))
    assert len(result) == 2
    assert np.asarray(result[0]) == pytest.approx(np.array([[0, .9], [.25, .8]]))
    assert np.asarray(result[1]) == pytest.approx(np.array([[2.75, .8], [3, .9]]))
