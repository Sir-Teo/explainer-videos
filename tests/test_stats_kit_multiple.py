import numpy as np
import pytest
from statsmodels.stats.multitest import multipletests

from explainer.stats import museum
from explainer.stats.kit import multiple as MT
from explainer.stats.world import World


def test_adjust_matches_statsmodels():
    rng = np.random.default_rng(0)
    p = np.r_[rng.uniform(0, 0.01, 10), rng.uniform(0, 1, 90)]
    for ours, theirs in (("bonferroni", "bonferroni"), ("sidak", "sidak"), ("holm", "holm"),
                         ("hochberg", "simes-hochberg"), ("bh", "fdr_bh"), ("by", "fdr_by")):
        assert np.allclose(MT.adjust(p, ours), multipletests(p, method=theirs)[1]), ours
    r = MT.bh(p, 0.1)
    assert r["k"] == int((MT.adjust(p, "bh") <= 0.1).sum())
    assert np.array_equal(r["reject"], MT.adjust(p, "bh") <= 0.1)


def test_closed_testing_is_holm():
    p = np.array([0.001, 0.012, 0.02, 0.04, 0.3])
    assert np.allclose(MT.closed_testing_bonferroni(p), MT.adjust(p, "holm"))


def test_bh_controls_fdr_and_storey():
    rng = np.random.default_rng(1)
    r = MT.fdp_sim(500, 0.8, 2.5, 0.0, 0.1, 300, rng)
    assert abs(r["fdr"] - 0.08) < 0.015
    p = np.r_[rng.uniform(size=800), rng.uniform(0, 0.01, 200)]
    assert abs(MT.storey_pi0(p) - 0.8) < 0.08
    assert np.all(MT.qvalues(p) <= MT.adjust(p, "bh") + 1e-12)


def test_locfdr_null_and_prostate():
    rng = np.random.default_rng(2)
    z = np.r_[rng.standard_normal(9500), rng.normal(3, 1, 500)]
    lf = MT.locfdr(z)
    assert 0.9 < lf["pi0"] < 1.0
    assert lf["fdr_at"](0.0) > 0.9 and lf["fdr_at"](4.0) < 0.2
    le = MT.locfdr(z, null="empirical")
    assert abs(le["delta0"]) < 0.1 and abs(le["sigma0"] - 1) < 0.1
    t, zz = museum.prostate_z()
    lp = MT.locfdr(zz, null="empirical")
    assert len(zz) == 6033 and 1.0 < lp["sigma0"] < 1.15


def test_knockoffs_control_fdr():
    rng = np.random.default_rng(3)
    n, p, k = 300, 60, 10
    rho = 0.3
    S = rho ** np.abs(np.subtract.outer(np.arange(p), np.arange(p)))
    L = np.linalg.cholesky(S)
    fdps = []
    for _ in range(20):
        X = rng.standard_normal((n, p)) @ L.T
        beta = np.zeros(p)
        beta[:k] = 0.6
        y = X @ beta + rng.standard_normal(n)
        Xk = MT.gaussian_knockoffs(X, S, rng)
        W = MT.lasso_W(X, Xk, y, 0.05)
        t = MT.knockoff_threshold(W, 0.2)
        sel = np.flatnonzero(W >= t)
        fdps.append(np.mean(sel >= k) if len(sel) else 0.0)
    assert np.mean(fdps) <= 0.3
    assert MT.knockoff_threshold(np.array([5.0, 4, 3, -1, 2, 1]), 0.5) == 1.0


def test_phack_and_ppv_and_egger():
    rng = np.random.default_rng(4)
    r = MT.phack(800, rng)
    assert 0.03 < r["none"] < 0.07 and r["A"] > 0.08 and 0.5 < r["ABCD"] < 0.72
    assert MT.ppv(0.5, 0.8) == pytest.approx(0.8 / 0.85, rel=1e-9)
    s = MT.publication_sim(2000, 0.2, rng, publish_null=0.1)
    e = MT.egger(s["est"][s["published"]], s["se"][s["published"]])
    assert e["p"] < 0.01 and e["intercept"] > 0
    g = np.linspace(0.001, 0.049, 49)
    assert np.allclose(MT.pcurve_density(0.0, 30, g), 20.0)
    d = MT.pcurve_density(0.5, 40, g)
    assert d[0] > d[-1]


def test_world_genes_and_fcr():
    w = World()
    g = w.genes
    assert g["x"].shape == (50, 5000) and g["nonnull"].sum() == 250
    est = np.r_[np.full(10, 3.0), np.zeros(90)]
    f = MT.fcr_intervals(est, np.ones(100), est > 2, 0.1)
    assert f["level"] == pytest.approx(0.99)


def test_pvalue_sea():
    from explainer.stats.viz import PValueSea

    rng = np.random.default_rng(7)
    p = np.r_[rng.uniform(0, 1e-3, 20), rng.uniform(size=980)]
    sea = PValueSea(p, ranks=100)
    assert sea.k(0.1) == MT.bh(p, 0.1)["k"]
    assert len(sea.mark(0.1)) == sea.k(0.1)
    g = PValueSea.grid(p[:100], cols=10)
    assert len(g) == 100
