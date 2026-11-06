"""statkit.multi against statsmodels, closed forms and simulation."""

import numpy as np
import pandas as pd
import pytest
import statsmodels.multivariate.api as smv
from scipy import stats

from explainer.stats import museum
from explainer.stats.kit import multi as M


def test_mds_recovers_euclidean_configurations():
    g = np.random.default_rng(1)
    P = g.normal(size=(30, 2))
    D = np.sqrt(((P[:, None] - P[None]) ** 2).sum(-1))
    r = M.classical_mds(D)
    assert r["negative_share"] < 1e-9 and r["explained"] == pytest.approx(1)
    assert M.procrustes(P, r["X"])["rmse"] < 1e-8
    names, E = museum.eurodist()
    assert M.classical_mds(E)["explained"] > 0.8


def test_wishart_and_hotelling():
    g = np.random.default_rng(2)
    S = np.array([[2.0, 0.6, 0.1], [0.6, 1.0, -0.3], [0.1, -0.3, 0.5]])
    W = np.mean([M.wishart_bartlett(S, 8, g) for _ in range(6000)], 0)
    assert np.allclose(W / 8, S, atol=0.05)
    # T^2's exact F calibration has the right size under the null
    rej = np.mean([M.hotelling_one(g.multivariate_normal(np.zeros(3), S, 15), np.zeros(3))["p"] < 0.05 for _ in range(3000)])
    assert abs(rej - 0.05) < 0.015
    X, y, _ = museum.iris()
    h = M.hotelling_two(X[y == 1], X[y == 2])
    assert h["p"] < 1e-20


def test_manova_matches_statsmodels():
    X, y, _ = museum.iris()
    df = pd.DataFrame(X, columns=list("abcd"))
    df["g"] = y.astype(str)
    st = smv.MANOVA.from_formula("a + b + c + d ~ g", df).mv_test().results["g"]["stat"]
    r = M.manova(X, y)
    assert r["wilks"] == pytest.approx(st.loc["Wilks' lambda", "Value"])
    assert r["pillai"] == pytest.approx(st.loc["Pillai's trace", "Value"])
    assert r["hotelling_lawley"] == pytest.approx(st.loc["Hotelling-Lawley trace", "Value"])
    assert r["roy"] == pytest.approx(st.loc["Roy's greatest root", "Value"])
    assert r["wilks_F"] == pytest.approx(st.loc["Wilks' lambda", "F Value"])


def test_pca_cca_fa_against_statsmodels():
    X, y, _ = museum.iris()
    p = M.pca(X)
    assert p["variances"] == pytest.approx(np.sort(np.linalg.eigvalsh(np.cov(X.T)))[::-1])
    _, L, _ = museum.lifecycle()
    cc = smv.CanCorr(L[:, [1, 2]], L[:, [0, 3, 4]])
    assert M.cca(L[:, [1, 2]], L[:, [0, 3, 4]])["r"] == pytest.approx(cc.cancorr)
    names, R, n = museum.harman74()
    f = M.factor_ml(R, 4, n)
    fs = smv.Factor(corr=R, n_factor=4, method="ml", nobs=n).fit()
    assert f["uniqueness"] == pytest.approx(fs.uniqueness, abs=2e-3)
    v = M.varimax(f["loadings"])
    assert np.allclose(v["loadings"] @ v["loadings"].T, f["loadings"] @ f["loadings"].T)


def test_discriminants_and_clustering():
    X, y, _ = museum.iris()
    assert M.loo_error(X, y, "lda") == pytest.approx(0.02)
    g = np.random.default_rng(3)
    gm = M.gmm_em(X, 3, g)
    assert M.adjusted_rand(gm["labels"], y) > 0.85
    assert M.adjusted_rand(y, y) == pytest.approx(1)


def test_graphical_lasso_kkt_and_sparsity():
    names, R, n = museum.harman74()
    for lam in (0.1, 0.3):
        gl = M.graphical_lasso(R, lam, tol=1e-12)
        W, T = gl["covariance"], gl["precision"]
        off = ~np.eye(len(R), dtype=bool)
        G = (W - R)[off]
        assert np.abs(G).max() <= lam + 1e-8
        nz = np.abs(T[off]) > 1e-8
        assert np.allclose(np.abs(G[nz]), lam, atol=1e-7)
        assert np.allclose(W @ T, np.eye(len(R)), atol=1e-8)
    # independent coordinates: the true graph is empty
    g = np.random.default_rng(4)
    Z = g.standard_normal((400, 6))
    assert M.graphical_lasso(np.corrcoef(Z.T), 0.25)["edges"] == 0
