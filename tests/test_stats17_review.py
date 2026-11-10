"""Independent numerical and provenance checks for the Part 17 review."""
from pathlib import Path

import numpy as np
import pytest
from scipy import linalg, stats
import statsmodels.api as sm

from explainer.stats import museum
from explainer.stats.kit import ts as T
from videos.stats.stats17 import compute as C


def test_archived_yule_values_and_correlations():
    folder = Path(__file__).resolve().parents[1] / 'tests/fixtures/qa/stats17-polish-20261107'
    arrays = []
    for name, current in [('yule1.dat', museum.YULE_MORTALITY), ('yule2.dat', museum.YULE_CE_MARRIAGES)]:
        values = []
        for line in (folder/name).read_text().splitlines():
            try:
                values.append(float(line.strip()))
            except ValueError:
                pass
        np.testing.assert_array_equal(values, current)
        arrays.append(values)
    assert np.corrcoef(arrays)[0, 1] == pytest.approx(.9515, abs=5e-5)
    assert np.corrcoef(np.diff(arrays, axis=1))[0, 1] == pytest.approx(.0185, abs=1e-4)


def test_exact_ar1_mean_variance_matches_covariance_matrix():
    d = C.compute_meanci()
    cov = linalg.toeplitz(.7 ** np.arange(100)) / (1-.7**2)
    assert d['exact_sd']**2 == pytest.approx(cov.sum()/100**2)
    assert d['exact_sd'] < np.sqrt(d['inflation']/(100*(1-.7**2)))


def test_block_example_uses_basic_interval_like_board():
    d = C.compute_meanci()
    g = C.rng(1987)
    x = T.simulate_arma([.7], [], 100, g)
    means = T.block_bootstrap_means(x, 10, 2000, g)
    expected = 2*x.mean() - np.quantile(means, [.975, .025])
    np.testing.assert_allclose(d['block'], expected)
    assert d['block'][0] < d['block'][1]


def test_spurious_example_matches_ols_and_unselected_seed_pair():
    d = C.compute_spurious()
    x, y = T.random_walk(100, C.rng(0)), T.random_walk(100, C.rng(1))
    np.testing.assert_array_equal(d['ex'], [x, y])
    fit = sm.OLS(y, sm.add_constant(x)).fit()
    assert d['ex_t'] == pytest.approx(fit.tvalues[1])
    assert d['ex_p'] == pytest.approx(fit.pvalues[1], rel=1e-10)
    assert d['ex_r2'] == pytest.approx(fit.rsquared)
    assert d['ex_dw'] == pytest.approx(sm.stats.durbin_watson(fit.resid))
    assert d['reject_diff'] == np.mean(np.abs(d['t_diff']) > stats.t.ppf(.975, 97))
    assert d['visible_mass'] == np.mean(np.abs(d['t']) <= 30)


def test_holt_winters_repeats_known_season_beyond_first_year():
    pattern = np.array([2., -1., 1., -2.])
    y = 10 + np.tile(pattern, 20)
    d = T.holt_winters(y, 4, .4, .2, .3, h=25)
    np.testing.assert_allclose(d['forecast'], 10+np.resize(pattern, 25), atol=1e-12)


def test_forecast_scores_use_training_scale_and_prespecified_window():
    d = C.compute_forecast()
    years, train = C.sunspot_window()
    assert years[-1] == 1924
    assert d['years'] == list(range(1925, 1956))
    for p in [2, d['best']]:
        f = d[f'p{p}']
        reference = np.mean(np.abs(np.asarray(d['actual'][:11])-f['mean'][:11])) / np.mean(np.abs(np.diff(train)))
        assert f['mase'] == pytest.approx(reference)


def test_polyline_clipping_does_not_bridge_missing_values():
    segments = C.clipped_segments([0, 1, 2, 3, 4], [0, 1, np.nan, -1, 0], (0, 4, -2, 2))
    assert len(segments) == 2
    np.testing.assert_allclose(segments[0], [[0, 0], [1, 1]])
    np.testing.assert_allclose(segments[1], [[3, -1], [4, 0]])
