"""statkit.spatial (Part 39): Matern covariances, variograms, kriging, likelihoods, Vecchia, GMRFs, areal data, points."""

from __future__ import annotations

import numpy as np
import pytest

from explainer.stats import museum
from explainer.stats.kit import spatial as SP


def _g(s):
    return np.random.default_rng(s)


def test_matern_closed_forms_match_bessel():
    d = np.linspace(0, 3, 50)
    for nu in (0.5, 1.5, 2.5):
        closed = SP.matern(d, 2.0, 0.7, nu)
        general = SP.matern(d, 2.0, 0.7, nu + 1e-9)
        assert closed == pytest.approx(general, abs=1e-6)
    assert SP.matern(np.array([0.0]), 3.0, 1.0, 1.2)[0] == pytest.approx(3.0)


def test_simple_kriging_is_the_gp_posterior():
    """Against Gaussian conditioning done the other way round: through the joint precision matrix of (z0, z)."""
    g = _g(1)
    xy = g.random((40, 2))
    z = np.sin(4 * xy[:, 0]) + g.normal(0, 0.1, 40)
    x0 = g.random((10, 2))
    cov = lambda d: SP.matern(d, 1.5, 0.3, 1.5)
    k = SP.krige(xy, z, x0, cov, nugget=0.01, mean=0.0)
    allp = np.vstack([x0, xy])
    S = cov(SP.dists(allp))
    S[10:, 10:] += 0.01 * np.eye(40)
    Pm = np.linalg.inv(S)
    P00 = Pm[:10, :10]
    mu = -np.linalg.solve(P00, Pm[:10, 10:] @ z)
    var = np.diag(np.linalg.inv(P00))
    assert k["pred"] == pytest.approx(mu, abs=1e-7)
    assert k["var"] == pytest.approx(var, abs=1e-7)


def test_kriging_interpolates_and_universal_reduces_to_ordinary():
    g = _g(2)
    xy = g.random((30, 2))
    z = g.standard_normal(30)
    cov = lambda d: SP.matern(d, 1.0, 0.4, 1.5)
    ok = SP.krige(xy, z, xy[:5], cov)
    assert ok["pred"] == pytest.approx(z[:5], abs=1e-6) and ok["var"] == pytest.approx(np.zeros(5), abs=1e-6)
    far = SP.krige(xy, z, np.array([[50.0, 50.0]]), cov)
    assert far["pred"][0] == pytest.approx(far["beta"][0], abs=1e-6)  # far from the data: the GLS mean
    assert far["var"][0] > 1.0  # the field's variance plus the mean's uncertainty


def test_variogram_fit_recovers_parameters():
    g = _g(3)
    n = 500
    xy = g.random((n, 2)) * 4
    K = SP.matern(SP.dists(xy), 2.0, 0.5, 0.5) + 0.2 * np.eye(n)
    z = np.linalg.cholesky(K) @ g.standard_normal(n)
    v = SP.variogram(xy, z, np.linspace(0, 2, 21))
    f = SP.fit_variogram(v["lag"], v["gamma"], v["n"], "exp")
    assert f["nugget"] + f["sill"] == pytest.approx(2.2, rel=0.35)
    assert f["range"] == pytest.approx(0.5, rel=0.6)


def test_vecchia_with_all_neighbours_is_exact_and_converges():
    g = _g(4)
    n = 120
    xy = g.random((n, 2))
    z = np.linalg.cholesky(SP.matern(SP.dists(xy), 1.0, 0.2, 1.5) + 0.1 * np.eye(n)) @ g.standard_normal(n)
    ex = SP.exact_loglik(xy, z, 1.0, 0.2, 1.5, 0.1)
    assert SP.vecchia_loglik(xy, z, 1.0, 0.2, 1.5, 0.1, m=n) == pytest.approx(ex, abs=1e-6)
    assert abs(SP.vecchia_loglik_fast(xy, z, 1.0, 0.2, 1.5, 0.1, m=20) - ex) < abs(SP.vecchia_loglik_fast(xy, z, 1.0, 0.2, 1.5, 0.1, m=1) - ex)


def test_reml_recovers_the_covariate_effect():
    g = _g(5)
    n = 200
    xy = g.random((n, 2))
    x = g.standard_normal(n)
    w = np.linalg.cholesky(SP.matern(SP.dists(xy), 1.0, 0.2, 1.5) + 1e-9 * np.eye(n)) @ g.standard_normal(n)
    y = 2 + 1.5 * x + w + 0.3 * g.standard_normal(n)
    f = SP.gp_fit(xy, y, x, nu=1.5, reml=True)
    assert f["beta"][1] == pytest.approx(1.5, abs=4 * np.sqrt(f["cov_beta"][1, 1]))


def test_gmrf_precision_is_sparse_symmetric_positive():
    Q = SP.gmrf_precision(20, 15, 0.5)
    A = Q.toarray()
    assert np.allclose(A, A.T)
    assert np.linalg.eigvalsh(A).min() > 0
    assert Q.nnz < 0.05 * A.size


def test_morans_i_and_ripley_under_the_null():
    g = _g(6)
    W = np.zeros((50, 50))
    for i in range(49):
        W[i, i + 1] = W[i + 1, i] = 1
    assert SP.morans_i(g.standard_normal(50), W, 499, g)["p"] > 0.01
    assert SP.morans_i(np.cumsum(g.standard_normal(50)), W, 499, g)["p"] < 0.01
    pts = g.random((800, 2))
    k = SP.ripley_k(pts, np.array([0.05, 0.1]), (0, 1, 0, 1))
    assert k["L"] == pytest.approx([0.05, 0.1], abs=0.015)


def test_snow_broad_street_is_the_nearest_pump_for_most_deaths():
    s = museum.snow_map()
    near = np.argmin(SP.dists(s["deaths"], s["pumps"]["xy"]), 1)
    assert s["pumps"]["label"][np.bincount(near).argmax()] == "Broad St"
    assert len(s["deaths"]) == 578


def test_meuse_kriging_beats_the_mean_in_cross_validation():
    m = museum.meuse()
    xy = np.column_stack([m["x"], m["y"]]) / 1000
    z = np.log(m["zinc"])
    cov = lambda d: SP.matern(d, 0.6, 0.3, 0.5)
    err = [z[i] - SP.krige(np.delete(xy, i, 0), np.delete(z, i), xy[i:i + 1], cov, nugget=0.05)["pred"][0] for i in range(0, 155, 5)]
    assert np.sqrt(np.mean(np.square(err))) < 0.6 * np.std(z)


def test_expected_improvement_and_gneiting():
    assert SP.expected_improvement(np.array([0.0]), np.array([1.0]), 0.0)[0] == pytest.approx(0.3989, abs=1e-3)
    assert SP.gneiting(0.0, 0.0) == pytest.approx(1.0)
    assert SP.gneiting(1.0, 1.0, beta=0.0) == pytest.approx(SP.gneiting(1.0, 0.0, beta=0.0) * SP.gneiting(0.0, 1.0, beta=0.0))
