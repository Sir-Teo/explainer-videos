import numpy as np
import pytest
import statsmodels.api as sm
from scipy import stats

from explainer.stats import museum
from explainer.stats.kit import glm

T = np.asarray(museum.CHALLENGER_TEMP, float)
Y = (np.asarray(museum.CHALLENGER_DISTRESS) > 0).astype(float)
X = np.column_stack([np.ones(23), T])


def test_logistic_matches_statsmodels():
    f = glm.logistic(X, Y)
    s = sm.GLM(Y, X, family=sm.families.Binomial()).fit()
    assert np.allclose(f.coef, s.params, atol=1e-8)
    assert np.allclose(f.se(), s.bse, rtol=1e-6)
    assert f.deviance == pytest.approx(s.deviance, rel=1e-8)
    assert f.loglik == pytest.approx(s.llf, rel=1e-8)
    assert len(f.path) > 3
    assert f.coef[1] == pytest.approx(-0.2322, abs=1e-3)


def test_binomial_counts_and_profile():
    k = np.asarray(museum.CHALLENGER_DISTRESS, float)
    f = glm.logistic(X, k, n_trials=np.full(23, 6.0))
    s = sm.GLM(np.column_stack([k, 6 - k]), X, family=sm.families.Binomial()).fit()
    assert np.allclose(f.coef, s.params, atol=1e-7)
    b = glm.logistic(X, Y)
    lo, mid, hi = glm.profile_ci(b, np.array([1.0, 31.0]))
    assert lo < mid < hi and hi - mid > mid - lo - 10
    # the profile interval for the slope matches statsmodels' likelihood-ratio inversion via a direct check
    lo_b, bhat, hi_b = glm.profile_coef_ci(b, 1)
    for edge in (lo_b, hi_b):
        r = sm.GLM(Y, X[:, :1], family=sm.families.Binomial(), offset=edge * T).fit()
        assert 2 * (b.loglik - r.llf) == pytest.approx(stats.chi2.ppf(0.95, 1), rel=1e-4)


def test_poisson_offset_quasi_sandwich():
    g = np.random.Generator(np.random.PCG64(3))
    n = 200
    x = g.normal(size=n)
    expo = g.uniform(50, 500, n)
    lam = expo * np.exp(-4 + 0.3 * x) * g.gamma(2, 0.5, n)
    yv = g.poisson(lam)
    Xp = np.column_stack([np.ones(n), x])
    f = glm.poisson(Xp, yv, offset=np.log(expo))
    s = sm.GLM(yv, Xp, family=sm.families.Poisson(), offset=np.log(expo)).fit()
    assert np.allclose(f.coef, s.params, atol=1e-8) and np.allclose(f.se(), s.bse, rtol=1e-6)
    sq = sm.GLM(yv, Xp, family=sm.families.Poisson(), offset=np.log(expo)).fit(scale="X2")
    assert np.allclose(f.se("quasi"), sq.bse, rtol=1e-6)
    sh = sm.GLM(yv, Xp, family=sm.families.Poisson(), offset=np.log(expo)).fit(cov_type="HC0")
    assert np.allclose(f.se("sandwich"), sh.bse, rtol=1e-6)
    assert f.pearson_dispersion > 1.5


def test_tables_and_cmh():
    t = glm.table2x2(647, 2, 622, 27)
    assert t["or"] == pytest.approx(647 * 27 / (2 * 622))
    assert t["p_fisher"] == pytest.approx(stats.fisher_exact([[647, 2], [622, 27]]).pvalue)
    tabs = [[[ma, mr], [fa, fr]] for ma, mr, fa, fr in museum.BERKELEY.values()]
    c = glm.cmh(tabs)
    from statsmodels.stats.contingency_tables import StratifiedTable
    st = StratifiedTable([np.array(tb) for tb in tabs])
    assert c["or_mh"] == pytest.approx(st.oddsratio_pooled)
    assert c["chi2"] == pytest.approx(st.test_null_odds(correction=False).statistic)


def test_roc_brier_calibration():
    g = np.random.Generator(np.random.PCG64(1))
    s = g.normal(size=500)
    yv = g.random(500) < 1 / (1 + np.exp(-2 * s))
    fpr, tpr, auc = glm.roc(s, yv)
    mw = stats.mannwhitneyu(s[yv], s[~yv]).statistic / (yv.sum() * (~yv).sum())
    assert auc == pytest.approx(mw)
    assert glm.brier([0.0, 1.0], [0, 1]) == 0.0
    pred, obs, cnt = glm.calibration(1 / (1 + np.exp(-2 * s)), yv, bins=5)
    assert cnt.sum() == 500 and np.all(np.diff(pred) > 0)


def test_profile_near_separation_matches_grid():
    from scipy import special
    g = np.random.Generator(np.random.PCG64(5))
    a0, b0 = glm.logistic(X, Y).coef
    for _ in range(2):
        yv = (g.random(23) < special.expit(a0 + b0 * T)).astype(float)
    f = glm.logistic(X, yv)
    lo, eta, hi = glm.profile_ci(f, np.array([1.0, 31.0]))
    bs = np.linspace(-3, 1, 40001)
    for e in (lo, hi):
        P = np.clip(special.expit(e + bs[:, None] * (T[None, :] - 31)), 1e-15, 1 - 1e-15)
        L = (yv * np.log(P) + (1 - yv) * np.log1p(-P)).sum(1).max()
        assert f.loglik - L == pytest.approx(stats.chi2.ppf(0.95, 1) / 2, abs=1e-3)
