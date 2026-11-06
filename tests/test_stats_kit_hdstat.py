"""Tests for statkit.hdstat, the high-dimensional statistics toolkit of Part 52."""

import math

import numpy as np
from scipy import integrate

from explainer.stats.kit import hdstat as H


def rng(seed=0):
    return np.random.default_rng(seed)


def test_random_matrix_laws():
    for g in (0.1, 0.25, 0.5, 1.0):
        a, b = H.mp_edges(g)
        assert abs(integrate.quad(lambda x: H.mp_pdf(np.array([x]), g)[0], a, b, limit=200)[0] - 1) < 1e-4
        x = np.linspace(a + 0.01, b - 0.01, 50)
        assert np.max(np.abs(H.density_from_stieltjes(x, g) - H.mp_pdf(x, g))) < 1e-3
    assert abs(integrate.quad(lambda x: H.semicircle_pdf(np.array([x]))[0], -2, 2)[0] - 1) < 1e-8
    ev = H.wigner(800, rng(1))
    assert abs(ev.max() - 2) < 0.1 and abs(np.mean(ev ** 2) - 1) < 0.02


def test_spikes():
    g = 0.5
    assert abs(H.spike_eigenvalue(0.5, g) - (1 + math.sqrt(g)) ** 2) < 1e-12  # below threshold: the edge
    assert H.spike_overlap(0.5, g) == 0
    for ell in (1.5, 3.0):
        assert abs(H.spike_invert(float(H.spike_eigenvalue(ell, g)), g) - ell) < 1e-10
    n, p, ell = 1000, 500, 3.0
    tops, ovs = [], []
    r = rng(2)
    for _ in range(40):
        X = H.spiked_sample(n, p, ell, r)
        l, v = H.top_eig(X)
        tops.append(l)
        ovs.append(v[0] ** 2)
    assert abs(np.mean(tops) - H.spike_eigenvalue(ell, g)) < 0.05
    assert abs(np.mean(ovs) - H.spike_overlap(ell, g)) < 0.02
    assert abs(np.std(tops) / H.spike_sd(ell, g, n) - 1) < 0.3


def test_tracy_widom():
    m1 = H.tracy_widom_moments(1)
    m2 = H.tracy_widom_moments(2)
    assert abs(m1["mean"] + 1.2065) < 2e-3 and abs(m1["sd"] - 1.2680) < 2e-3
    assert abs(m2["mean"] + 1.7711) < 2e-3 and abs(m2["sd"] - 0.9018) < 2e-3
    assert abs(H.tracy_widom_quantile(0.95, 1) - 0.9793) < 2e-3
    n, p = 400, 200
    mu, sig = H.johnstone_center_scale(n, p)
    r = rng(3)
    z = [(np.linalg.eigvalsh((X := r.standard_normal((n, p))).T @ X)[-1] - mu) / sig for _ in range(300)]
    assert abs(np.mean(z) - m1["mean"]) < 0.25 and abs(np.std(z) - m1["sd"]) < 0.25


def test_lasso_tools():
    r = rng(4)
    n, p, s = 200, 400, 5
    X = r.standard_normal((n, p))
    beta = np.zeros(p)
    beta[:s] = 2.0
    y = X @ beta + r.standard_normal(n)
    b = H.SPK.lasso_cd(X, y, H.lasso_lambda(n, p))
    assert np.linalg.norm(b - beta) < 3 * H.oracle_rate(n, p, s) * 2
    assert H.irrepresentable(X, np.arange(s), np.ones(s)) < 1
    assert H.signed_support_on_path(X, y, beta)
    # a design that violates irrepresentability: a noise column that copies the signal's sum
    Xb = X.copy()
    Xb[:, s] = X[:, :s].sum(1) / math.sqrt(s) * 0.9 + 0.1 * r.standard_normal(n)
    assert H.irrepresentable(Xb, np.arange(s), np.ones(s)) > 1


def test_covariance_and_perturbation():
    r = rng(5)
    p, n = 100, 100
    Sig = H.ar1_cov(p, 0.6)
    X = r.multivariate_normal(np.zeros(p), Sig, n)
    S = X.T @ X / n
    e0 = H.op_norm(S - Sig)
    assert H.op_norm(H.band(S, 5) - Sig) < e0
    assert H.op_norm(H.threshold(S, 0.3) - Sig) < e0
    L, rho = H.ledoit_wolf(X)
    assert 0 < rho < 1 and H.op_norm(L - Sig) < e0
    u = np.eye(5)[0]
    assert H.sin_theta(u, u + 0.1 * np.eye(5)[1]) < 0.1 and H.davis_kahan(0.1, 1.0) == 0.2


def test_sparse_pca_and_graphs():
    r = rng(6)
    X, v = H.sparse_spike_sample(200, 1000, 10, 3.0, r)
    vd = H.diagonal_thresholding(X, 10)
    _, vp = H.top_eig(X)
    assert (vd @ v) ** 2 > (vp @ v) ** 2
    p = 20
    Q = H.chain_precision(p, 0.4)
    Xg = r.multivariate_normal(np.zeros(p), np.linalg.inv(Q), 500)
    E = H.neighbourhood_selection(Xg, 0.1)
    truth = np.abs(Q) > 0
    np.fill_diagonal(truth, False)
    assert np.mean(E[truth]) > 0.9 and np.mean(E[~truth & ~np.eye(p, dtype=bool)]) < 0.05
    M = H.low_rank(30, 20, 2, r)
    assert np.linalg.matrix_rank(M) == 2
