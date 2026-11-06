"""statkit.ts (II), Part 38: spectra, unit roots, cointegration, GARCH, long memory, Kalman, VARs; against statsmodels."""

from __future__ import annotations

import warnings

import numpy as np
import pytest

from explainer.stats import museum
from explainer.stats.kit import ts as T


def _g(s):
    return np.random.default_rng(s)


def test_adf_and_critical_values_match_statsmodels():
    from statsmodels.tsa.stattools import adfuller

    x = np.cumsum(_g(1).standard_normal(250))
    for tr in ("n", "c", "ct"):
        a = T.adf(x, 3, tr)
        s = adfuller(x, maxlag=3, regression=tr, autolag=None)
        assert a["t"] == pytest.approx(s[0], rel=1e-9)
        assert a["crit5"] == pytest.approx(s[4]["5%"], rel=1e-9)


def test_kpss_engle_granger_and_johansen_match_statsmodels():
    from statsmodels.tsa.stattools import coint, kpss
    from statsmodels.tsa.vector_ar.vecm import coint_johansen

    g = _g(2)
    x = np.cumsum(g.standard_normal(300))
    y = 0.7 * x + g.standard_normal(300)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        assert T.kpss(x, "c", 8)["eta"] == pytest.approx(kpss(x, "c", nlags=8)[0], rel=1e-9)
    e = T.engle_granger(y, x)
    c = coint(y, x, trend="c", maxlag=0, autolag=None)
    assert e["t"] == pytest.approx(c[0], rel=1e-9) and e["crit5"] == pytest.approx(c[2][1], rel=1e-9)
    Y = np.column_stack([x, y, np.cumsum(g.standard_normal(300))])
    assert np.allclose(T.johansen_trace(Y, 2)["trace"], coint_johansen(Y, 0, 1).lr1)


def test_var_and_impulse_responses_match_statsmodels():
    from statsmodels.tsa.api import VAR

    Z = _g(3).standard_normal((250, 3)).cumsum(0) * 0.1 + _g(4).standard_normal((250, 3))
    v = T.var_fit(Z, 2)
    r = VAR(Z).fit(2)
    assert np.allclose(v["A"][1], r.coefs[1])
    assert np.allclose(T.irf(v, 6), r.orth_ma_rep(6))


def test_periodogram_of_white_noise_is_inconsistent_and_welch_is_not():
    g = _g(5)
    small, big = T.periodogram(g.standard_normal(256)), T.periodogram(g.standard_normal(4096))
    assert np.std(big["I"]) > 0.8  # an exponential with mean 1: its spread does not shrink with n
    assert np.std(T.welch(g.standard_normal(4096), 128)["S"]) < 0.3
    assert T.multitaper(g.standard_normal(1024))["S"].mean() == pytest.approx(1.0, abs=0.1)


def test_sunspot_cycle_is_eleven_years():
    yrs, s = museum.sunspots()
    p = T.welch(s, 64)
    assert 1 / p["f"][np.argmax(p["S"])] == pytest.approx(11, abs=1)


def test_garch_recovers_its_parameters():
    g = _g(6)
    n, w, a, b = 4000, 0.05, 0.08, 0.9
    e, s2 = np.zeros(n), np.full(n, w / (1 - a - b))
    for t in range(1, n):
        s2[t] = w + a * e[t - 1] ** 2 + b * s2[t - 1]
        e[t] = np.sqrt(s2[t]) * g.standard_normal()
    f = T.garch11_fit(e)
    assert f["alpha"] == pytest.approx(a, abs=0.03) and f["beta"] == pytest.approx(b, abs=0.04)
    assert T.arch_lm(e)["p"] < 1e-6


def test_long_memory_estimators_find_d():
    x = T.simulate_arfima(0.3, 8192, _g(7))
    assert T.gph(x)["d"] == pytest.approx(0.3, abs=0.12)
    assert T.local_whittle(x)["d"] == pytest.approx(0.3, abs=0.07)
    assert T.arfima_acf(0.3, 100)[100] == pytest.approx(T.arfima_acf(0.3, 100)[50] * 2 ** (2 * 0.3 - 1), rel=0.02)
    assert T.hurst_rs(np.cumsum(_g(8).standard_normal(4000)) * 0 + _g(9).standard_normal(4000))["H"] < 0.62


def test_nile_local_level_matches_durbin_koopman_and_em():
    """Durbin & Koopman (2012), section 2.10: sigma_eps^2 = 15099, sigma_eta^2 = 1469.1."""
    yrs, y = museum.nile()
    f = T.local_level_mle(y)
    assert f["r"] == pytest.approx(15099, rel=0.005) and f["q"] == pytest.approx(1469.1, rel=0.01)
    e = T.local_level_em(y, 1000.0, 10000.0, iters=300)
    assert np.all(np.diff(e["path"][:, 2]) > -1e-6)
    assert e["q"] == pytest.approx(f["q"], rel=0.01)


def test_kalman_matches_statsmodels_local_level_likelihood():
    import statsmodels.api as sm

    yrs, y = museum.nile()
    m = sm.tsa.UnobservedComponents(y, "local level")
    ll = lambda r, q: T.kalman(y, [[1.0]], [[1.0]], [[q]], [[r]], [y[0]], [[1e7]])["loglik"]
    # the starts differ (exact diffuse vs a variance of 1e7), so compare likelihood ratios
    d_sm = m.loglike([15099.0, 1469.1]) - m.loglike([9000.0, 3000.0])
    assert ll(15099.0, 1469.1) - ll(9000.0, 3000.0) == pytest.approx(d_sm, abs=0.05)


def test_particle_filter_beats_ekf_on_kitagawa():
    from videos.stats.stats38.compute import kitagawa

    g = _g(10)
    x, y, f, h = kitagawa(100, g)
    fj = lambda m, t: 0.5 + 25 * (1 - m * m) / (1 + m * m) ** 2
    e = T.ekf(y, f, fj, h, lambda m: m / 10, 10.0, 1.0, 0.1, 5.0)["m"]
    p = T.bootstrap_pf(y, f, h, 10.0, 1.0, 0.1, 5.0, 2000, g)["m"]
    assert np.sqrt(np.mean((p - x) ** 2)) < np.sqrt(np.mean((e - x) ** 2))


def test_hamilton_filter_probabilities_and_bootstraps():
    g = _g(11)
    s = np.zeros(400, int)
    for t in range(1, 400):
        s[t] = s[t - 1] if g.random() < 0.95 else 1 - s[t - 1]
    y = np.where(s == 1, 3.0, -1.0) + g.standard_normal(400)
    h = T.hamilton_fit(y)
    assert h["mu"][0] == pytest.approx(-1, abs=0.4) and h["mu"][1] == pytest.approx(3, abs=0.4)
    assert np.mean((h["p_low"] > 0.5) == (s == 0)) > 0.9
    x = np.repeat(g.standard_normal(100), 5)  # strongly dependent
    assert T.stationary_bootstrap_means(x, 20, 500, g).std() > 1.5 * x[g.integers(0, 500, (500, 500))].mean(1).std()
