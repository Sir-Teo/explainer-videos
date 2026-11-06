"""statkit.robust against closed forms, SciPy, statsmodels and published fits."""

import math

import numpy as np
import pytest
import statsmodels.api as sm
import statsmodels.robust.scale as srs
from scipy import stats

from explainer.stats import museum
from explainer.stats.kit import robust as R


def test_location_and_scale():
    g = np.random.default_rng(1)
    x = g.standard_normal(57)
    assert R.mad(x) == pytest.approx(stats.median_abs_deviation(x, scale="normal"))
    assert R.qn_scale(x, finite_sample=False) == pytest.approx(srs.qn_scale(x) * 2.2219 / 2.21914, rel=1e-4)
    assert R.trimmed_mean(x, 0.1) == pytest.approx(stats.trim_mean(x, 0.1))
    w = R.walsh_averages(x)
    assert len(w) == 57 * 58 // 2
    hu = R.m_location(x, "huber")
    u = (x - hu["mu"]) / hu["scale"]
    assert abs(np.sum(R.psi_huber(u))) < 1e-6
    y = np.concatenate([x, [50.0, 60.0]])
    r = sm.RLM(y, np.ones(len(y)), M=sm.robust.norms.HuberT()).fit()
    assert R.m_location(y)["mu"] == pytest.approx(float(r.params[0]), abs=0.05)
    # large samples: the scale estimators are consistent at the normal
    z = g.standard_normal(4000)
    for f in (R.mad, R.qn_scale):
        assert f(z) == pytest.approx(1, abs=0.05)
    assert R.sn_scale(z[:1500]) == pytest.approx(1, abs=0.06)


def test_signed_rank_null_and_hl_interval():
    c = R.signed_rank_null(10)
    assert c.sum() == pytest.approx(1)
    assert c[0] == pytest.approx(2 ** -10)
    k = np.arange(len(c))
    assert np.allclose(c, c[::-1]) and np.sum(k * c) == pytest.approx(10 * 11 / 4)
    assert np.sum(k * k * c) - (10 * 11 / 4) ** 2 == pytest.approx(10 * 11 * 21 / 24)
    g = np.random.default_rng(2)
    hit = 0
    for _ in range(400):
        lo, hi = R.hodges_lehmann_ci(g.standard_t(3, 25))
        hit += lo <= 0 <= hi
    assert 0.93 <= hit / 400 <= 0.985


def test_efficiency_and_huber():
    assert R.wilcoxon_are(stats.norm.pdf, 1) == pytest.approx(3 / math.pi, rel=1e-8)
    f = lambda t: 3 / (20 * math.sqrt(5)) * (5 - t * t) if abs(t) <= math.sqrt(5) else 0.0
    assert R.wilcoxon_are(f, 1, lim=math.sqrt(5)) == pytest.approx(108 / 125, rel=1e-6)
    assert R.huber_k(0.05) == pytest.approx(1.399, abs=1e-3)
    # V(psi_k, Phi) = (2Phi(k) - 1 - 2k phi(k) + 2k^2 (1 - Phi(k))) / (2Phi(k) - 1)^2
    k = 1.345
    v = (2 * stats.norm.cdf(k) - 1 - 2 * k * stats.norm.pdf(k) + 2 * k * k * stats.norm.sf(k)) / (2 * stats.norm.cdf(k) - 1) ** 2
    assert R.m_asymptotic_variance(lambda t: R.psi_huber(t, k), stats.norm.pdf) == pytest.approx(v, rel=1e-5)
    assert 1 / v == pytest.approx(0.95, abs=0.001)
    # the minimax variance is the worst case over the contamination neighbourhood: Huber's psi at F0
    for eps in (0.01, 0.05, 0.1):
        kk = R.huber_k(eps)
        assert R.huber_minimax_variance(eps) >= R.m_asymptotic_variance(lambda t: R.psi_huber(t, kk), stats.norm.pdf) - 1e-9


def test_influence_and_breakdown():
    x = np.linspace(-2, 2, 101)
    grid = np.array([-10.0, -1.0, 0.5, 10.0])
    sc = R.sensitivity_curve(np.mean, x, grid)
    assert np.allclose(sc, grid - x.mean(), atol=1e-9)
    scm = R.sensitivity_curve(np.median, x, grid)
    assert np.all(np.abs(scm) < 5)
    assert R.empirical_breakdown(np.mean, x) == pytest.approx(1 / 101)
    assert R.empirical_breakdown(np.median, x) == pytest.approx(51 / 101)
    assert 0.27 < R.empirical_breakdown(R.hodges_lehmann, x) < 0.31


def test_regression_on_stars_and_mcd_on_hbk():
    xs, ys = museum.stars_cyg()
    X = np.column_stack([np.ones(len(xs)), xs])
    ols = np.linalg.lstsq(X, ys, rcond=None)[0]
    assert ols[1] < 0  # the four giants tilt least squares the wrong way
    L = R.lts(X, ys, rng=np.random.default_rng(1))
    assert L["coef"][1] > 2.5
    assert {10, 19, 29, 33} <= set(L["outliers"].tolist())  # the giants (1-based 11, 20, 30, 34)
    M = R.mm_regression(X, ys, rng=np.random.default_rng(1))
    assert M["coef"] == pytest.approx([-4.97, 2.25], abs=0.15)  # robustbase::lmrob
    H, _ = museum.hbk()
    mc = R.mcd(H, rng=np.random.default_rng(1))
    assert set(mc["outliers"].tolist()) == set(range(14))
    assert np.sum(mc["classical"][:10] > mc["cutoff"]) <= 1  # masking: the classical distances miss the bad ten


def test_heavy_tails():
    g = np.random.default_rng(3)
    err_mean, err_mom = [], []
    for _ in range(300):
        z = g.pareto(2.2, 500)  # infinite third moment; mean 1/1.2
        m = 1 / 1.2
        err_mean.append(abs(z.mean() - m))
        err_mom.append(abs(R.median_of_means(z, 15, g) - m))
    assert np.quantile(err_mom, 0.99) < np.quantile(err_mean, 0.99)
    z = g.standard_normal(1000)
    assert abs(R.catoni(z, 0.01, 1.0) - z.mean()) < 0.02
