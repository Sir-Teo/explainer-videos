"""Independent finite-distribution and simulation references for Part 10."""
from itertools import product
from math import comb

import numpy as np
import pytest
from scipy import stats

from videos.stats.stats10.compute import (
    compute_knapsack, load, monte_carlo_pvalue,
)


def test_tea_null_and_explicit_imperfect_perception_model():
    d = load('tea')
    for cups in (6, 8, 10, 12):
        k = cups // 2
        np.testing.assert_allclose(d[str(cups)]['pmf'], stats.hypergeom.pmf(np.arange(k + 1), cups, k, k))
    for q in (.7, .8, .9):
        # A: true milk cups perceived as milk; B: tea cups perceived as milk.
        exact = sum(stats.binom.pmf(a, 4, q) * q**4 / comb(8 - a, 4 - a) for a in range(4))
        exact += q**4 * sum(stats.binom.pmf(b, 4, 1 - q) / comb(4 + b, 4) for b in range(5))
        se = np.sqrt(exact * (1 - exact) / 40000)
        assert d['power'][str(q)] == pytest.approx(exact, abs=4 * se)


def test_randomized_np_frontier_dominates_all_deterministic_regions():
    d = compute_knapsack()
    front = np.array(d['front'])
    allowed = np.interp(d['size'], front[:, 0], front[:, 1])
    assert (np.array(d['power']) <= allowed + 1e-12).all()
    assert d['best_size'] == pytest.approx(1 / 6)
    assert d['best_power'] == pytest.approx(7 / 30)
    assert np.array(d['sums'])[d['best_mask']].tolist() == [10, 11, 12]


def test_plus_one_mc_pvalues_are_superuniform_exhaustively():
    # Observed and both simulated statistics are exchangeable draws from the same null.
    p = np.array([monte_carlo_pvalue(row[0], np.array(row[1:]))
                  for row in product((-1., 0., 1., 2.), repeat=3)])
    assert p.min() >= 1 / 3
    for level in (1 / 3, 2 / 3, 1):
        assert np.mean(p <= level) <= level + 1e-12
    assert monte_carlo_pvalue(100, np.array([0., 1.])) == pytest.approx(1 / 3)


def test_poisson_lrt_simulation_matches_exact_null_rejection_rates():
    d = load('wilks')
    for n in (3, 30):
        total = np.arange(0, 250)
        # scipy.special.xlogy handles the 0 log 0 convention independently.
        from scipy.special import xlogy
        w = 2 * (xlogy(total, total / (2 * n)) - (total - 2 * n))
        exact = stats.poisson.pmf(total, 2 * n)[w > stats.chi2.ppf(.95, 1)].sum()
        se = np.sqrt(exact * (1 - exact) / 100000)
        assert d[str(n)]['size'] == pytest.approx(exact, abs=4 * se)
        assert np.dot(d[str(n)]['hist'], np.diff(d['edges'])) <= 1 + 1e-12


def test_type_s_and_m_match_truncated_normal_reference():
    for key, row in load('power')['sm'].items():
        mu = float(key.split('_')[0]); se = row['se']
        upper, lower = 1.96 - mu / se, -1.96 - mu / se
        power = stats.norm.sf(upper) + stats.norm.cdf(lower)
        type_s = stats.norm.cdf(lower) / power
        exaggeration = (mu * (stats.norm.sf(upper) - stats.norm.cdf(lower))
                        + se * (stats.norm.pdf(upper) + stats.norm.pdf(lower))) / (mu * power)
        assert row['power'] == pytest.approx(power, abs=4 * np.sqrt(power * (1 - power) / 200000))
        assert row['type_s'] == pytest.approx(type_s, abs=.006)
        assert row['exaggeration'] == pytest.approx(exaggeration, rel=.02)
