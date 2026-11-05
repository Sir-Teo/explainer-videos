"""statkit.mixed and statkit.shrink (Part 25): checked against statsmodels and against theory."""

import numpy as np
import pytest
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy import special

from explainer.stats.kit import mixed as MX
from explainer.stats.kit import shrink as SH


@pytest.fixture(scope="module")
def panel():
    g = np.random.default_rng(25)
    G, m = 40, 8
    groups = np.repeat(np.arange(G), m)
    x = g.normal(size=G * m)
    b0 = g.normal(0, 1.0, G)[groups]
    b1 = g.normal(0, 0.5, G)[groups]
    y = 2 + 0.7 * x + b0 + b1 * x + g.normal(0, 1, G * m)
    X = np.column_stack([np.ones(G * m), x])
    return X, y, groups


@pytest.mark.parametrize("method", ["REML", "ML"])
def test_random_intercept_matches_statsmodels(panel, method):
    X, y, groups = panel
    f = MX.lmm(y, X, groups, method=method)
    s = sm.MixedLM(y, X, groups=groups).fit(reml=(method == "REML"))
    assert np.allclose(f.beta, s.fe_params, rtol=1e-5)
    assert np.isclose(f.sigma2, s.scale, rtol=1e-4)
    assert np.isclose(f.G[0, 0], np.asarray(s.cov_re)[0, 0], rtol=1e-3)
    assert np.allclose(f.se, s.bse_fe, rtol=5e-3)  # statsmodels: observed Hessian; here (X'V^-1X)^-1, as lme4
    assert np.isclose(f.loglik, s.llf, rtol=1e-6)


def test_random_slope_matches_statsmodels(panel):
    X, y, groups = panel
    f = MX.lmm(y, X, groups, slopes=[1], method="REML")
    s = sm.MixedLM(y, X, groups=groups, exog_re=X).fit(reml=True)
    assert np.allclose(f.beta, s.fe_params, rtol=1e-4)
    assert np.allclose(f.G, np.asarray(s.cov_re), rtol=2e-2, atol=2e-3)
    assert np.isclose(f.loglik, s.llf, rtol=1e-6)
    re = np.array([np.asarray(v) for v in s.random_effects.values()])
    assert np.allclose(f.blup, re, atol=2e-3)


def test_satterthwaite_balanced_between_effect():
    g = np.random.default_rng(3)
    G, m = 12, 5
    groups = np.repeat(np.arange(G), m)
    trt = np.repeat(np.arange(G) % 2, m).astype(float)
    y = 1 + 0.5 * trt + g.normal(0, 1, G)[groups] + g.normal(0, 1, G * m)
    X = np.column_stack([np.ones(G * m), trt])
    f = MX.lmm(y, X, groups)
    d = MX.satterthwaite(f, [0, 1])
    assert abs(d["df"] - (G - 2)) < 0.5  # a between-group contrast in a balanced design: G - 2 df
    assert np.isclose(d["se"], f.se[1], rtol=1e-4)


def test_glmm_laplace_and_agq():
    g = np.random.default_rng(4)
    G, m = 60, 10
    groups = np.repeat(np.arange(G), m)
    x = g.normal(size=G * m)
    u = g.normal(0, 1.2, G)[groups]
    y = (g.random(G * m) < special.expit(-0.5 + 1.0 * x + u)).astype(float)
    X = np.column_stack([np.ones(G * m), x])
    lap = MX.glmm_logit(y, X, groups, nagq=1)
    agq = MX.glmm_logit(y, X, groups, nagq=15)
    agq30 = MX.glmm_logit(y, X, groups, nagq=30)
    assert np.allclose(agq["beta"], agq30["beta"], atol=1e-4)  # quadrature converged
    assert abs(agq["beta"][1] - 1.0) < 0.25 and abs(agq["sigma"] - 1.2) < 0.4
    assert abs(lap["beta"][1] - agq["beta"][1]) < 0.1


def test_james_stein_dominates():
    theta = np.linspace(-1, 1, 10)
    r = SH.js_risk_exact(theta, 1.0, R=20000, rng=np.random.default_rng(1))
    assert r["js"] < r["mle"] and r["js_plus"] <= r["js"] + 1e-9
    assert abs(r["mle"] - 10) < 0.2
    g = np.random.default_rng(2)
    sures = [SH.sure_js(theta + g.normal(size=10)) for _ in range(20000)]
    assert abs(np.mean(sures) - r["js"]) < 0.1  # SURE is unbiased for the risk


def test_eb_meta_fay_herriot():
    g = np.random.default_rng(5)
    k = 300
    s2 = g.uniform(0.2, 2.0, k)
    th = 1.0 + g.normal(0, 0.8, k)
    x = th + np.sqrt(s2) * g.normal(size=k)
    e = SH.eb_normal(x, s2)
    assert abs(e["tau2"] - 0.64) < 0.2 and abs(e["mu"] - 1.0) < 0.15
    assert np.mean((e["theta"] - th) ** 2) < np.mean((x - th) ** 2)
    m = SH.meta(x[:8], s2[:8])
    assert m["ci_hk"][0] < m["mu"] < m["ci_hk"][1] and 0 <= m["I2"] <= 1
    X = np.column_stack([np.ones(k), g.normal(size=k)])
    y = X @ [1, 0.5] + g.normal(0, 0.7, k) + np.sqrt(s2) * g.normal(size=k)
    fh = SH.fay_herriot(y, s2, X)
    assert abs(fh["A"] - 0.49) < 0.2 and np.all((fh["gamma"] > 0) & (fh["gamma"] < 1))


def test_npmle_two_point_prior():
    g = np.random.default_rng(6)
    th = np.where(g.random(2000) < 0.5, -2.0, 2.0)
    x = th + g.normal(size=2000)
    r = SH.npmle(x, 1.0, grid=np.linspace(-5, 5, 201))
    mass_near = r["w"][np.abs(np.abs(r["grid"]) - 2) < 0.4].sum()
    assert mass_near > 0.85
    assert np.mean((r["post_mean"] - th) ** 2) < 0.5


def test_vc_lmm_one_factor_matches_lmm(panel):
    X, y, groups = panel
    for method in ("REML", "ML"):
        a = MX.lmm(y, X, groups, method=method)
        b = MX.vc_lmm(y, X, {"g": groups}, method=method)
        assert np.allclose(a.beta, b["beta"], rtol=1e-5)
        assert np.isclose(a.G[0, 0], b["var"]["g"], rtol=1e-3)
        assert np.isclose(a.sigma2, b["sigma2"], rtol=1e-4)
        assert np.isclose(a.loglik, b["loglik"], rtol=1e-6)
        assert np.allclose(np.asarray(a.blup).ravel(), b["blup"]["g"], atol=1e-3)


def test_vc_lmm_crossed_matches_statsmodels():
    g = np.random.default_rng(8)
    E, R = 30, 5
    essay = np.repeat(np.arange(E), R)
    rater = np.tile(np.arange(R), E)
    y = 5 + g.normal(0, 1, E)[essay] + g.normal(0, 0.6, R)[rater] + g.normal(0, 0.7, E * R)
    f = MX.vc_lmm(y, np.ones((E * R, 1)), {"essay": essay, "rater": rater})
    import pandas as pd
    df = pd.DataFrame({"y": y, "essay": essay, "rater": rater, "one": 1})
    s = smf.mixedlm("y ~ 1", df, groups="one", re_formula="0", vc_formula={"essay": "0 + C(essay)", "rater": "0 + C(rater)"}).fit(reml=True)
    vc = dict(zip(s.model.exog_vc.names, s.vcomp))
    assert np.isclose(f["var"]["essay"], vc["essay"], rtol=2e-3)
    assert np.isclose(f["var"]["rater"], vc["rater"], rtol=2e-3)
    assert np.isclose(f["sigma2"], s.scale, rtol=2e-3)
