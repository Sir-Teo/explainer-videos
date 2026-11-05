import numpy as np
import pytest

from explainer.stats.kit import ts as T

sm_tsa = pytest.importorskip("statsmodels.tsa.stattools")


def _ar2(n=400, seed=0):
    return T.simulate_arma([1.3, -0.6], [], n, np.random.default_rng(seed))


def test_acf_pacf_match_statsmodels():
    x = _ar2()
    assert np.allclose(T.acf(x, 10), sm_tsa.acf(x, nlags=10, fft=False))
    assert np.allclose(T.pacf(x, 8), sm_tsa.pacf(x, nlags=8, method="ldb")[1:], atol=1e-10)


def test_yule_walker_matches_statsmodels():
    from statsmodels.regression.linear_model import yule_walker

    x = _ar2(seed=1)
    yw = T.yule_walker(x, 2)
    rho, sig = yule_walker(x, order=2, method="mle")
    assert np.allclose(yw["phi"], rho)
    assert np.isclose(yw["sigma2"], sig ** 2)


def test_ar_ols_recovers_coefficients():
    x = T.simulate_arma([0.6], [], 5000, np.random.default_rng(2), mu=3.0)
    f = T.ar_ols(x, 1)
    assert abs(f["phi"][0] - 0.6) < 0.03 and abs(f["mu"] - 3.0) < 0.1


def test_roots_and_stationarity():
    assert T.is_stationary([0.5]) and not T.is_stationary([1.0]) and not T.is_stationary([1.2])
    assert T.is_stationary([1.3, -0.6]) and not T.is_stationary([0.5, 0.6])
    assert np.allclose(np.abs(T.ar_roots([0.5])), 2.0)


def test_theoretical_acf():
    from statsmodels.tsa.arima_process import arma_acf

    assert np.allclose(T.arma_acf([1.3, -0.6], [0.4], 10), arma_acf([1, -1.3, 0.6], [1, 0.4], 11), atol=1e-8)
    assert np.allclose(T.psi_weights([0.5], [], 5), 0.5 ** np.arange(5))


def test_ljung_box_matches_statsmodels():
    from statsmodels.stats.diagnostic import acorr_ljungbox

    x = np.random.default_rng(3).normal(size=300)
    Q, p = T.ljung_box(x, 10)
    lb = acorr_ljungbox(x, lags=[10])
    assert np.isclose(Q, float(lb["lb_stat"].iloc[0])) and np.isclose(p, float(lb["lb_pvalue"].iloc[0]))


def test_forecast_intervals_widen_to_marginal():
    f = T.ar_forecast([1.0, 2.0], [0.8], 0.0, 1.0, 60)
    assert np.isclose(f["mean"][0], 1.6) and np.isclose(f["se"][0], 1.0)
    assert np.isclose(f["se"][-1], np.sqrt(1 / (1 - 0.64)), rtol=1e-6)


def test_ses_and_holt_winters():
    y = np.array([3.0, 5.0, 4.0])
    assert np.allclose(T.ses(y, 0.5), [3, 3, 4, 4])
    t = np.arange(120)
    y = 10 + 0.1 * t + 2 * np.sin(2 * np.pi * t / 12)
    hw = T.fit_holt_winters(y, 12, h=12)
    assert np.max(np.abs(hw["forecast"] - (10 + 0.1 * (t[-1] + 1 + np.arange(12)) + 2 * np.sin(2 * np.pi * (t[-1] + 1 + np.arange(12)) / 12)))) < 0.2


def test_decompose_recovers_season():
    t = np.arange(96)
    s = np.tile([1.0, -1.0, 2.0, -2.0], 24)
    d = T.decompose(5 + 0.2 * t + s, 4)
    assert np.allclose(d["figure"], [1, -1, 2, -2], atol=1e-8)


def test_mase_naive_is_one():
    y = np.array([1.0, 3.0, 2.0, 5.0])
    assert np.isclose(T.mase(y[1:], y[:-1], y), 1.0)


def test_newey_west_matches_statsmodels():
    import statsmodels.api as sm

    x = T.simulate_arma([0.7], [], 500, np.random.default_rng(4))
    r = sm.OLS(x, np.ones(len(x))).fit(cov_type="HAC", cov_kwds={"maxlags": 8, "use_correction": False})
    assert np.isclose(T.newey_west_se(x, 8), float(r.bse[0]), rtol=1e-6)
    assert np.isclose(T.ar1_neff(100, 0.5), 100 / 3)


def test_ar2_period():
    assert np.isclose(T.ar2_period(0.0, -1.0), 4.0)


def test_block_bootstrap():
    g = np.random.default_rng(5)
    x = g.normal(size=400)
    m = T.block_bootstrap_means(x, 1, 4000, g)
    assert m.shape == (4000,) and abs(m.std() / (x.std() / 20) - 1) < 0.08
    y = T.simulate_arma([0.8], [], 2000, g)
    wide = T.block_bootstrap_means(y, 50, 2000, g).std()
    narrow = T.block_bootstrap_means(y, 1, 2000, g).std()
    assert wide > 2 * narrow  # blocks keep the dependence that inflates the mean's variance
