"""statkit.glm (II), Part 24: families, IRLS, deviance, extensions; checked against statsmodels."""

import numpy as np
import pytest
import statsmodels.api as sm
from scipy import special

from explainer.stats.kit import glm as G

BLISS = np.array([[1.6907, 59, 6], [1.7242, 60, 13], [1.7552, 62, 18], [1.7842, 56, 28],
                  [1.8113, 63, 52], [1.8369, 59, 53], [1.8610, 62, 61], [1.8839, 60, 60]])


@pytest.mark.parametrize("link,sm_link", [("logit", sm.families.links.Logit()), ("probit", sm.families.links.Probit()),
                                          ("cloglog", sm.families.links.CLogLog())])
def test_bliss_links_match_statsmodels(link, sm_link):
    x, n, k = BLISS.T
    X = np.column_stack([np.ones(8), x])
    f = G.glm_fit(X, k / n, G.family("binomial", link), n=n)
    s = sm.GLM(np.column_stack([k, n - k]), X, family=sm.families.Binomial(link=sm_link)).fit()
    assert np.allclose(f.coef, s.params, rtol=1e-6)
    assert np.allclose(f.se(), s.bse, rtol=1e-5)
    assert np.isclose(f.deviance, s.deviance, rtol=1e-6)
    assert np.allclose(f.pearson, s.resid_pearson, rtol=1e-4)  # statsmodels stops at its own tolerance
    assert np.allclose(f.deviance_resid, s.resid_deviance, rtol=1e-4)


def test_gamma_and_poisson():
    g = np.random.default_rng(1)
    X = np.column_stack([np.ones(200), g.normal(size=200)])
    mu = np.exp(1 + 0.5 * X[:, 1])
    yg = g.gamma(2.0, mu / 2.0)
    f = G.glm_fit(X, yg, G.family("gamma", "log"))
    s = sm.GLM(yg, X, family=sm.families.Gamma(sm.families.links.Log())).fit()
    assert np.allclose(f.coef, s.params, rtol=1e-6)
    assert np.isclose(f.phi, s.scale, rtol=1e-6)
    assert np.allclose(f.se(), s.bse, rtol=1e-5)
    yp = g.poisson(mu)
    fp = G.glm_fit(X, yp, G.family("poisson"))
    sp = sm.GLM(yp, X, family=sm.families.Poisson()).fit(cov_type="HC0")
    assert np.allclose(fp.coef, sp.params, rtol=1e-7)
    assert np.allclose(fp.se("sandwich"), sp.bse, rtol=1e-6)


def test_ld50_and_quantile_residuals():
    x, n, k = BLISS.T
    X = np.column_stack([np.ones(8), x])
    f = G.glm_fit(X, k / n, G.family("binomial"), n=n)
    r = G.ld50(f)
    assert 1.76 < r["x"] < 1.78
    assert r["fieller"][0] < r["x"] < r["fieller"][1]
    q = G.glm_fit(X, k / n, G.family("binomial", "cloglog"), n=n).quantile_resid(np.random.default_rng(2))
    assert np.all(np.isfinite(q)) and len(q) == 8


def test_firth_finite_under_separation():
    x = np.array([-2, -1.5, -1, -0.5, 0.5, 1, 1.5, 2.0])
    y = (x > 0).astype(float)
    X = np.column_stack([np.ones(8), x])
    fr = G.firth_logistic(X, y)
    assert np.all(np.isfinite(fr["coef"])) and 1 < fr["coef"][1] < 10
    s = G.logistic_path_separated(X, y, 25)
    assert s["slope"][-1] > s["slope"][5] > 0 and np.all(np.diff(s["loglik"]) >= -1e-9)


def test_negbin_matches_statsmodels():
    g = np.random.default_rng(3)
    X = np.column_stack([np.ones(500), g.normal(size=500)])
    mu = np.exp(0.5 + 0.4 * X[:, 1])
    y = g.negative_binomial(1.5, 1.5 / (1.5 + mu))
    r = G.negbin_fit(X, y)
    s = sm.NegativeBinomial(y, X).fit(disp=0)
    assert np.allclose(r["coef"], s.params[:2], rtol=1e-4)
    assert np.isclose(1 / r["k"], s.params[2], rtol=1e-3)
    assert np.isclose(r["loglik"], s.llf, rtol=1e-6)


def test_zip_and_hurdle():
    g = np.random.default_rng(4)
    n = 2000
    X = np.column_stack([np.ones(n), g.normal(size=n)])
    lam = np.exp(0.8 + 0.3 * X[:, 1])
    y = np.where(g.random(n) < 0.3, 0, g.poisson(lam))
    z = G.zip_em(X, y)
    assert abs(z["pi"][0] - 0.3) < 0.05 and abs(z["beta"][1] - 0.3) < 0.06
    assert np.all(np.diff(z["path"]) >= -1e-8)
    from statsmodels.discrete.count_model import ZeroInflatedPoisson
    s = ZeroInflatedPoisson(y, X, exog_infl=np.ones((n, 1))).fit(disp=0, maxiter=500)
    assert np.isclose(z["loglik"], s.llf, rtol=1e-5)
    h = G.hurdle(X, y)
    assert np.isfinite(h["loglik"])


def test_multinomial_and_ordinal():
    g = np.random.default_rng(5)
    n = 1500
    x = g.normal(size=n)
    X = np.column_stack([np.ones(n), x])
    eta = np.column_stack([np.zeros(n), 0.2 + 0.8 * x, -0.5 - 0.6 * x])
    P = special.softmax(eta, axis=1)
    cat = np.array([g.choice(3, p=p) for p in P])
    Y = np.eye(3)[cat]
    r = G.multinomial_logit(X, Y)
    s = sm.MNLogit(cat, X).fit(disp=0)
    assert np.allclose(r["coef"], s.params, rtol=1e-6)
    from statsmodels.miscmodels.ordinal_model import OrderedModel
    lat = 0.7 * x + g.logistic(size=n)
    yo = np.digitize(lat, [-1.0, 0.5, 1.5])
    po = G.proportional_odds(x[:, None], yo, 4)
    so = OrderedModel(yo, x[:, None], distr="logit").fit(method="bfgs", disp=0)
    assert np.isclose(po["beta"][0], so.params[0], rtol=1e-4)
    assert np.isclose(po["se_beta"][0], so.bse[0], rtol=2e-2)


def test_gee_matches_statsmodels():
    g = np.random.default_rng(6)
    G_, m = 60, 12
    groups = np.repeat(np.arange(G_), m)
    u = g.normal(0, 1, G_)[groups]
    x = g.normal(size=G_ * m)
    y = (g.random(G_ * m) < special.expit(-0.3 + 0.7 * x + u)).astype(float)
    X = np.column_stack([np.ones(G_ * m), x])
    for cs, smc in (("independence", sm.cov_struct.Independence()), ("exchangeable", sm.cov_struct.Exchangeable())):
        r = G.gee_logistic(X, y, groups, cs)
        s = sm.GEE(y, X, groups=groups, family=sm.families.Binomial(), cov_struct=smc).fit()
        assert np.allclose(r["coef"], s.params, rtol=1e-4, atol=1e-6)
        assert np.allclose(r["se_robust"], s.bse, rtol=2e-3)


def test_scoring_rules():
    from scipy import stats
    y = 0.3
    from scipy import integrate
    num = integrate.quad(lambda t: stats.norm.cdf(t) ** 2, -np.inf, y)[0] + integrate.quad(lambda t: stats.norm.sf(t) ** 2, y, np.inf)[0]
    assert np.isclose(G.crps_normal(0.0, 1.0, y), num, rtol=1e-8)
    assert G.log_score([0.9], [1]) < G.log_score([0.6], [1])
