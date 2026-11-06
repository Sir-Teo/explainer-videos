"""Tests for statkit.hdp, the high-dimensional probability toolkit of Part 51."""

import math

import numpy as np
from scipy import integrate

from explainer.stats.kit import hdp as H


def rng(seed=0):
    return np.random.default_rng(seed)


def test_sphere():
    for n in (3, 10, 100):
        assert abs(integrate.quad(lambda t: H.sphere_coordinate_pdf(np.array([t]), n)[0], -1, 1)[0] - 1) < 1e-8
    x = H.sample_sphere(200, 20000, rng(1))
    assert abs(np.mean(np.abs(x[:, 0]) <= 0.1) - H.sphere_band_mass(0.1, 200)) < 0.01
    assert abs(H.sphere_band_for(0.95, 1000) - 1.96 / math.sqrt(1000)) < 0.002  # ~ N(0, 1/n)
    assert abs(integrate.quad(lambda t: H.angle_pdf(np.array([t]), 20)[0], 0, math.pi)[0] - 1) < 1e-8


def test_shells_and_jl():
    m = H.norm_chi_moments(500)
    g = np.linalg.norm(rng(2).standard_normal((4000, 500)), axis=1)
    assert abs(g.mean() - m["mean"]) < 0.05 and abs(g.std() - m["sd"]) < 0.05
    assert abs(m["sd"] - 1 / math.sqrt(2)) < 0.01
    X = rng(3).standard_normal((40, 3000))
    d = H.jl_distortion(X, H.jl_dimension(40, 0.4), rng(4))
    assert d["max_dev"] < 0.4


def test_tail_bounds():
    for t in (0.05, 0.1, 0.2):
        ex = H.binomial_mean_tail(t, 200, 0.1)[0]
        assert ex <= H.chernoff_binomial(t, 200, 0.1)[0] <= H.hoeffding_tail(t, 200)[0] + 1e-12
        assert ex <= H.bernstein_tail(t, 200, 0.09, 1.0)[0]
    assert abs(H.psi_norm_empirical(rng(5).standard_normal(300000)) - H.psi2_norm_normal()) < 0.03


def test_lipschitz_and_matrices():
    assert abs(H.expected_max_gaussians(100) - 2.5076) < 1e-3
    mx = np.max(rng(6).standard_normal((4000, 1000)), axis=1)
    assert np.var(mx) < 1.0  # Gaussian Poincare: Var f <= 1 for 1-Lipschitz f
    for t in (1.0, 2.0):
        assert np.mean(mx - mx.mean() >= t) <= H.gaussian_concentration(t)[0]
    s = H.singular_extremes(500, 100, rng(7), reps=10)
    assert s["max"] <= s["gordon_max"] + 0.5 and s["min"] >= s["gordon_min"] - 0.5
    e = H.covariance_error(800, 200, rng(8), reps=10)
    assert abs(e - H.covariance_error_limit(800, 200)) < 0.15
    assert abs(integrate.quad(lambda t: H.marchenko_pastur_pdf(np.array([t]), 0.3)[0], 0.0, 3.0, limit=200)[0] - 1) < 1e-6
    mb = H.matrix_bernstein_rank_one(300, 40, rng(9), reps=30)
    assert mb["mean"] <= mb["bound"]


def test_comparison_and_stat_dim():
    r = rng(10)
    assert H.exchangeable_max(200, 0.5, r) < H.exchangeable_max(200, 0.0, r)  # Slepian
    assert H.sudakov_lower(1.0, 100) < H.expected_max_gaussians(100)
    d = H.stat_dim_l1(10, 200)
    assert 10 < d < 200
    assert H.stat_dim_l1(1, 200) < H.stat_dim_l1(20, 200)
    w = H.gaussian_width_l1_ball(1000)
    assert abs(w - math.sqrt(2 * math.log(2000))) < 0.6


def test_chaining():
    assert abs(H.dudley_brownian(0.0) - math.sqrt(math.pi / 2)) < 1e-6
    assert H.dudley_brownian(0.1) < H.dudley_brownian(0.01) < H.dudley_brownian(0.0)
    w = H.walk_max(2000, rng(9), reps=2000)
    assert abs(w - math.sqrt(2 / math.pi)) < 0.05  # grid maximum approaches sqrt(2/pi) from below
    assert H.union_bound_max(1000) > 3 * w
