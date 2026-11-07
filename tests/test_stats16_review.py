"""Independent reference checks for Part 16's corrected numerical examples."""
from itertools import combinations
from math import comb

import numpy as np
import pytest
from scipy import stats

from videos.stats.stats16 import compute as C


def test_tied_challenger_rank_law_matches_exhaustive_labelings():
    d = C.compute_mw()
    pooled = np.r_[d['warm'], d['cold']]
    # Enumerate labelled subsets independently of the production DP.
    ranks = stats.rankdata(pooled)
    chosen = np.asarray(list(combinations(range(23), 7)))
    null = 112 - (ranks[chosen].sum(1) - 28)
    values, counts = np.unique(null, return_counts=True)
    np.testing.assert_array_equal(values, d['u_grid'])
    np.testing.assert_allclose(counts / comb(23, 7), d['pmf'], atol=1e-15)
    assert d['U'] == 87.5
    expected = np.mean(np.abs(null - 56) >= 31.5)
    assert d['p'] == pytest.approx(expected)
    assert d['allocations'] == 245157


def test_midrank_auc_matches_direct_pairs_including_all_ties():
    for x, y in [([1, 1, 2], [1, 2]), ([3, 3], [3, 3]), ([1, 4], [2, 3])]:
        d = C.conditional_mann_whitney(x, y)
        diff = np.subtract.outer(x, y)
        assert d['auc'] == pytest.approx(np.mean((diff > 0) + .5 * (diff == 0)))
        assert np.sum(d['pmf']) == pytest.approx(1)
        if np.all(diff == 0):
            assert d['p'] == 1


def test_untied_rank_test_agrees_with_scipy_exact():
    x, y = [1, 3, 5], [2, 4, 6, 7]
    d = C.conditional_mann_whitney(x, y)
    ref = stats.mannwhitneyu(x, y, method='exact')
    assert d['U'] == ref.statistic
    assert d['p'] == pytest.approx(ref.pvalue)


def test_random_permutation_p_includes_observation_and_both_tails():
    assert C.monte_carlo_p([0, .1, -.7], .5) == .5
    assert C.monte_carlo_p([0] * 99, .9) == .01
    assert C.monte_carlo_p([0] * 99, 0) == 1


def test_uniform_maximum_interval_has_exact_95_percent_coverage():
    for n in [1, 3, 50, 1000]:
        lo, hi = C.uniform_max_interval(.8, n)
        assert lo == .8
        # Coverage iff M/theta >= .05**(1/n), using the exact Beta law.
        assert stats.beta(n, 1).sf(lo / hi) == pytest.approx(.95, abs=1e-12)
    d = C.compute_maxfail()
    assert d['exact_ci'] == list(C.uniform_max_interval(d['max'], 50))
    assert d['exact_ci'][1] < 1.03


def test_population_histogram_retains_omitted_tail_mass():
    d = C.compute_kde()
    pop = C.W.height[C.W.adult]
    counts, edges = np.histogram(pop, bins=130, range=(140, 205))
    np.testing.assert_allclose(d['true_y'], counts / (len(pop) * np.diff(edges)))
    assert np.dot(d['true_y'], np.diff(edges)) == pytest.approx(d['visible_mass'])
    assert d['visible_mass'] < 1


def test_bca_levels_reconstruct_endpoints_and_jackknife_scaling():
    d = C.compute_law()
    levels = np.asarray(d['bca_levels'])
    np.testing.assert_allclose(np.quantile(d['reps'], levels), d['bca'], atol=1e-14)
    loo = np.asarray(d['jack']['loo'])
    assert d['jack']['se'] == pytest.approx((len(loo)-1) * stats.sem(loo))
    assert 0 < levels[0] < levels[1] < 1


def test_geometric_clipping_preserves_crossings_and_disconnected_paths():
    pieces = C.clipped_segments([0, 1, 2, 3, 4], [0, 3, 3, -3, 0], (0, 4, -1, 1))
    assert len(pieces) == 3
    np.testing.assert_allclose(pieces[0], [[0, 0], [1/3, 1]])
    np.testing.assert_allclose(pieces[1], [[7/3, 1], [8/3, -1]])
    np.testing.assert_allclose(pieces[2], [[11/3, -1], [4, 0]])
