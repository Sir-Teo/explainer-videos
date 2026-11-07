"""Reference calculations for the Part 18 sampling review."""
import itertools

import numpy as np
import pytest

from explainer.stats.kit import survey as S
from videos.stats.stats18 import compute as C


def test_ht_constant_contributions_need_a_fixed_sample_size():
    y = np.array([1., 2., 3.])
    pi = y / 4
    estimates, probabilities = [], []
    for mask in itertools.product([False, True], repeat=3):
        mask = np.array(mask)
        estimates.append(S.horvitz_thompson(y[mask], pi[mask]))
        probabilities.append(np.prod(np.where(mask, pi, 1-pi)))
    estimates, probabilities = np.array(estimates), np.array(probabilities)
    assert probabilities @ estimates == pytest.approx(y.sum())
    # Independent Poisson inclusion has random size, even though y_i/pi_i = 4.
    variance = probabilities @ (estimates-y.sum())**2
    assert variance == pytest.approx(np.sum(y**2*(1-pi)/pi))
    assert variance > 0
    # One PPS draw is fixed-size and gives the total exactly.
    np.testing.assert_allclose(y / (y/y.sum()), y.sum())


def test_meng_identity_and_realized_error_comparison():
    y = np.array([0., 0., 0., 1., 1., 1., 1.])
    selected = np.array([False, False, True, True, True, True, False])
    d = S.meng(y, selected)
    assert d['identity'] == pytest.approx(y[selected].mean()-y.mean())
    assert d['n_eff'] == pytest.approx(y.var()/d['error']**2)
    # This is the small-SRS-fraction comparison, not an exact finite-N size.
    exact_size = len(y)/(1+(len(y)-1)*d['error']**2/y.var())
    assert exact_size != pytest.approx(d['n_eff'])


def test_integer_allocations_and_exact_design_variance():
    np.testing.assert_array_equal(C.integer_allocation([2.2, 3.2, 4.6], 10), [2, 3, 5])
    groups = [np.array([1., 3., 5.]), np.array([2., 4., 9., 13.])]
    sizes = np.array([len(g) for g in groups])
    estimates = [sizes[0]/sizes.sum()*np.mean(a)+sizes[1]/sizes.sum()*np.mean(b)
                 for a in itertools.combinations(groups[0], 2)
                 for b in itertools.combinations(groups[1], 2)]
    expected = S.stratified_variance(sizes, [g.std(ddof=1) for g in groups], [2, 2])
    assert np.var(estimates) == pytest.approx(expected)
    d = C.load('strat')
    assert sum(d['prop']) == sum(d['ney']) == 1000
    P = C.adults()
    assert d['se_srs']**2 == pytest.approx((1-1000/len(P['income']))*P['income'].var(ddof=1)/1000)


def test_ratio_example_uses_the_plotted_observations():
    d = C.load('ratio')
    P = C.adults()
    indices = np.array(d['one_indices'], dtype=int)
    y, x = np.array(d['one_income']), np.array(d['one_last'])
    np.testing.assert_array_equal(y, P['income'][indices])
    assert len(np.unique(indices)) == 400
    assert d['one_plain'] == pytest.approx(y.mean())
    assert d['one']['ratio'] == pytest.approx(y.sum()/x.sum())
    register = np.exp(np.log(P['income']) + C.rng(5).normal(0, .25, len(P['income'])))
    np.testing.assert_array_equal(x, register[indices])
    assert d['one']['mean'] == pytest.approx(y.sum()/x.sum()*register.mean())


def test_displayed_raking_rounds_match_their_own_margins():
    P = C.adults()
    steps, income_target, age_target = C.raking_steps(P, C.digest_returns(P), 8)
    assert len(steps) == 9  # initial state plus four income/age rounds
    for i, (income, age) in enumerate(steps[1:], 1):
        np.testing.assert_allclose(income if i % 2 else age,
                                   income_target if i % 2 else age_target, atol=2e-15)
    gap = max(np.max(np.abs(steps[-1][0]-income_target)),
              np.max(np.abs(steps[-1][1]-age_target)))
    assert gap < 1e-4
    assert gap > 0  # the other margin is not made exact by the final half-step


def test_offscale_curves_intersect_viewport_without_flattening():
    segments = C.clipped_segments([0, 1, 2, 3], [2, 1.5, .5, .2], (0, 3, 0, 1))
    assert len(segments) == 2
    np.testing.assert_allclose(segments[0], [[1.5, 1], [2, .5]])
    assert not C.clipped_segments([0, 1], [2, 3], (0, 3, 0, 1))
    assert not C.clipped_segments([0, 1, 2], [.2, np.nan, .4], (0, 3, 0, 1))
