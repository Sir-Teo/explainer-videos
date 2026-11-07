"""Independent checks for the Part 41 numerical teaching examples."""
import numpy as np
import pytest
from scipy.stats import norm
from videos.stats.stats41 import compute as C
from explainer.stats import museum
from explainer.stats.kit import mi as MI


def test_common_imputations_make_delta_curve_affine():
    completed = np.array([[1., 2., 5., 7.], [1., 4., 5., 8.], [1., 3., 5., 9.], [1., 2., 5., 8.]])
    original = completed.copy()
    missing = np.array([False, True, False, True])
    rows = C.delta_curve(completed, missing, [-1., 0., .3, 1.])
    for row in rows:
        assert row['est'] == pytest.approx(completed.mean() + .5 * row['delta'], abs=1e-14)
        assert row['lo'] < row['est'] < row['hi']
    np.testing.assert_array_equal(completed, original)
    # A specified oracle target is crossed at exactly (target-baseline)/missing share.
    target = 5.0
    delta = (target-completed.mean())/.5
    assert C.delta_curve(completed, missing, [delta])[0]['est'] == pytest.approx(target)


def test_ozone_complete_cases_are_not_all_observed_ozone_values():
    # Independently tabulated R airquality summaries: 111 joint complete cases,
    # 116 observed ozone readings. Their means round alike but are distinct.
    a = museum.airquality(complete=False)
    data = np.column_stack([a[k] for k in ('ozone','solar','wind','temp')])
    assert (~np.isnan(data).any(axis=1)).sum() == 111
    assert np.isfinite(a['ozone']).sum() == 116
    d = C.compute_em()
    assert d['cc_mean'] == pytest.approx(42.0990990990991, abs=1e-12)
    assert d['observed_ozone_mean'] == pytest.approx(42.12931034482759, abs=1e-12)


def test_univariate_missing_normal_em_matches_observed_likelihood_mle():
    # Entirely missing rows contribute a factor one, so observed values alone
    # determine the normal MLE. This also checks the covariance, not just a mean.
    y = np.array([2., 4., 7., 8., 10., np.nan, np.nan])
    fit = MI.em_mvn(y[:,None])
    observed = y[np.isfinite(y)]
    expected_mu, expected_sigma = norm.fit(observed)
    assert fit['mu'][0] == pytest.approx(expected_mu, abs=1e-8)
    assert fit['S'][0,0] == pytest.approx(expected_sigma**2, abs=1e-6)
    assert fit['ll'][-1] == pytest.approx(norm.logpdf(observed,expected_mu,expected_sigma).sum(), abs=1e-10)
