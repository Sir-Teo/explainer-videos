"""statkit.ols, Part 23 additions: checked against statsmodels and against identities."""

import numpy as np
import pytest
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import OLSInfluence

from explainer.stats.kit import ols as O


@pytest.fixture(scope="module")
def data():
    g = np.random.default_rng(23)
    n, G = 300, 30
    groups = np.repeat(np.arange(G), n // G)
    u = g.normal(size=G)[groups]
    x = g.normal(size=n) + 0.5 * g.normal(size=G)[groups]
    z = g.normal(size=n)
    y = 1 + 0.5 * x - 0.3 * z + u + g.normal(size=n) * (1 + 0.5 * np.abs(x))
    X = np.column_stack([np.ones(n), x, z])
    return X, y, groups


def test_cluster_cov_matches_statsmodels(data):
    X, y, groups = data
    f = O.fit(X, y)
    sm_fit = sm.OLS(y, X).fit(cov_type="cluster", cov_kwds={"groups": groups})
    assert np.allclose(np.sqrt(np.diag(O.cluster_cov(f, groups))), sm_fit.bse, rtol=1e-8)


def test_hac_matches_statsmodels(data):
    X, y, _ = data
    f = O.fit(X, y)
    sm_fit = sm.OLS(y, X).fit(cov_type="HAC", cov_kwds={"maxlags": 4, "use_correction": False})
    assert np.allclose(np.sqrt(np.diag(O.hac_cov(f, 4))), sm_fit.bse, rtol=1e-8)


def test_glh_matches_statsmodels(data):
    X, y, _ = data
    f = O.fit(X, y)
    C = np.array([[0, 1, 1], [0, 1, -1.0]])
    r = O.glh(f, C, [0.2, 0.8])
    t = sm.OLS(y, X).fit().f_test((C, np.array([0.2, 0.8])))
    assert np.isclose(r["F"], float(np.squeeze(t.fvalue)), rtol=1e-9)
    assert np.isclose(r["p"], float(t.pvalue), rtol=1e-7)


def test_gls_matches_statsmodels():
    g = np.random.default_rng(5)
    n = 80
    X = np.column_stack([np.ones(n), np.arange(n) / n])
    Om = O.ar1_omega(n, 0.6)
    e = np.linalg.cholesky(Om) @ g.normal(size=n)
    y = X @ [1.0, 2.0] + e
    f = O.gls(X, y, Om)
    s = sm.GLS(y, X, sigma=Om).fit()
    assert np.allclose(f.coef, s.params, rtol=1e-9)
    assert np.allclose(f.se(), s.bse, rtol=1e-8)
    pw = O.prais_winsten(X, y)
    assert 0.3 < pw["rho"] < 0.85


def test_dfbetas_and_jackknife(data):
    X, y, _ = data
    f = O.fit(X, y)
    assert np.allclose(O.dfbetas(f), OLSInfluence(sm.OLS(y, X).fit()).dfbetas, rtol=1e-7, atol=1e-10)
    J = O.jackknife_coefs(X, y)
    for i in (0, 17, 299):
        keep = np.arange(len(y)) != i
        assert np.allclose(J[i], O.fit(X[keep], y[keep]).coef, rtol=1e-9)


def test_bspline_partition_of_unity_and_span():
    x = np.linspace(0, 10, 200)
    B = O.bspline_basis(x, [2.5, 5, 7.5])
    assert B.shape == (200, 7)
    assert np.allclose(B.sum(1), 1)
    T = O.truncated_power(x, [2.5, 5, 7.5])
    y = np.sin(x)
    assert np.allclose(O.fit(B, y).fitted, O.fit(T, y).fitted, atol=1e-8)  # the same space of cubic splines


def test_deming_tls_and_digits():
    g = np.random.default_rng(1)
    t = g.normal(size=500)
    x, y = t + 0.3 * g.normal(size=500), 2 * t + 0.3 * g.normal(size=500)
    d = O.deming(x, y, 1.0)
    b = O.tls(np.column_stack([x - x.mean()]), y - y.mean())
    assert np.isclose(d["slope"], b[0], rtol=1e-8)
    assert 1.85 < d["slope"] < 2.15
    assert O.correct_digits([1.0001], [1.0])[0] == pytest.approx(4, abs=0.01)


def test_householder_reproduces_qr(data):
    X, _, _ = data
    h = O.householder(X[:12])
    R = np.linalg.qr(X[:12])[1]
    assert np.allclose(np.abs(np.diag(h["R"])), np.abs(np.diag(R)))
    assert np.allclose(np.tril(h["steps"][-1][:3], -1), 0, atol=1e-12)


def test_wild_cluster_bootstrap_null_p_is_uniformish():
    g = np.random.default_rng(9)
    ps = []
    for r in range(40):
        G = 10
        groups = np.repeat(np.arange(G), 20)
        x = np.repeat(g.normal(size=G), 20)
        y = np.repeat(g.normal(size=G), 20) + g.normal(size=200)
        X = np.column_stack([np.ones(200), x])
        ps.append(O.wild_cluster_boot(X, y, groups, 1, 0.0, R=199, g=g)["p"])
    ps = np.array(ps)
    assert 0.25 < ps.mean() < 0.75
    assert np.mean(ps < 0.05) <= 0.15


def test_qreg_se_close_to_statsmodels():
    g = np.random.default_rng(3)
    n = 400
    x = g.uniform(0, 4, n)
    y = 1 + x + (0.5 + 0.5 * x) * g.normal(size=n)
    X = np.column_stack([np.ones(n), x])
    q = sm.QuantReg(y, X).fit(q=0.5)
    se = O.qreg_se(X, y, 0.5, q.params)
    assert np.allclose(se, q.bse, rtol=0.25)
