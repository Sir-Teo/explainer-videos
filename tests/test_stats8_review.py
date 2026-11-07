"""Reference checks for Part 8's sampling and design calculations."""
from itertools import combinations

import numpy as np
import pytest
from scipy import stats

from videos.stats.stats8 import compute


def test_srs_standard_error_matches_exhaustive_design_distribution():
    population = np.array([-5., 0., 2., 8., 15.])
    for n in range(1,len(population)+1):
        means = [np.mean(sample) for sample in combinations(population,n)]
        assert compute.srs_mean_se(population,n) == pytest.approx(np.std(means))
    assert compute.srs_mean_se(population,1,replace=True) == pytest.approx(population.std())
    assert compute.srs_mean_se(population,len(population)) == 0


def test_displayed_student_histogram_retains_rounded_and_infinite_tails():
    d = compute.compute_student()
    t = np.array(d['t'])
    assert np.count_nonzero(~np.isfinite(t)) == d['ties']
    widths = np.diff(d['edges'])
    mass = np.dot(d['hist'],widths)
    assert mass == pytest.approx(np.mean((t >= -6)&(t <= 6)))
    assert mass < 1
    np.testing.assert_allclose(d['hist'],np.histogram(t,d['edges'])[0]/(750*widths))


def test_sleep_analysis_matches_scipy_paired_reference():
    a,b = np.asarray(compute.museum.SLEEP_DRUG1),np.asarray(compute.museum.SLEEP_DRUG2)
    result = stats.ttest_rel(b,a)
    d = compute.compute_tdist()['sleep']
    assert d['t'] == pytest.approx(result.statistic)
    assert d['p_t'] == pytest.approx(result.pvalue)
    ci=result.confidence_interval()
    np.testing.assert_allclose(d['ci'],[ci.low,ci.high])


def test_ratio_design_variance_matches_exact_constant_auxiliary_case():
    # With a constant auxiliary variable, the ratio total is exactly N * sample mean.
    # Exhaustive design variance must equal the average estimated variance.
    population = np.array([2., 5., 10., 20., 30.])
    n, N = 3, len(population)
    totals, estimated_variances = [], []
    for sample in combinations(population,n):
        totals.append(N*np.mean(sample))
        estimated_variances.append(compute.ratio_total_se(sample,np.full(n,2.),2*N,n/N)**2)
    assert np.mean(estimated_variances) == pytest.approx(np.var(totals))
    assert compute.ratio_total_se([3.,6.,9.],[1.,2.,3.],100.,.2) == pytest.approx(0,abs=1e-14)


def test_proportion_histogram_uses_integer_success_counts():
    d=compute.compute_extras2()['prop']
    tall=compute.adult_heights()>180
    counts=tall[compute.rng(94).integers(0,len(tall),(20000,100))].sum(1)
    np.testing.assert_allclose(d['hist'],np.bincount(counts,minlength=101)/20000)
    assert sum(d['hist']) == pytest.approx(1)
