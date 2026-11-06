"""Tests for statkit.asymptotics, the risk-bump explorer of Part 47."""

import math

import numpy as np
from scipy import stats

from explainer.stats.kit import asymptotics as A


def rng(seed=0):
    return np.random.default_rng(seed)


def test_hodges_exact_against_simulation():
    n = 100
    for theta in (0.0, 0.1, 0.3, 1.0):
        xb = rng(1).normal(theta, 1 / math.sqrt(n), 400000)
        T = np.where(np.abs(xb) >= n ** -0.25, xb, 0.0)
        sim = n * np.mean((T - theta) ** 2)
        assert abs(sim - A.hodges_risk(theta, n)) < 0.03 * max(1, sim)
    assert A.hodges_risk(0.0, 10000) < 1e-6  # superefficient at 0
    # the bump: the maximal scaled risk grows with n
    h = np.linspace(0, 20, 2001)
    m1, m2 = A.hodges_local(h, 100).max(), A.hodges_local(h, 10000).max()
    assert m2 > m1 > 1.5


def test_bahadur():
    small = A.bahadur_remainder(50, 4000, rng(2))
    big = A.bahadur_remainder(5000, 1000, rng(3))
    assert big["rms_rem"] < small["rms_rem"]
    assert abs(big["sd_full"] - big["theory_sd"]) < 0.1


def test_u_statistics():
    g = A.gini_variance(20)
    x = rng(4).normal(0, 1, (4000, 20))
    us = np.array([A.u_statistic(r, lambda a, b: np.abs(a - b)) for r in x])
    assert abs(us.mean() - g["theta"]) < 0.01
    assert abs(us.var() - g["var"]) / g["var"] < 0.08


def test_lan_and_efficiency():
    r = A.cauchy_local_llr(400, 1.5, 20000, rng(5))
    assert abs(r["mean"] - r["lan_mean"]) < 0.05 and abs(r["var"] - r["lan_var"]) < 0.08
    assert abs(A.pitman_are("wilcoxon_normal") - 0.9549) < 1e-3 and A.pitman_are("wilcoxon_min") > 0.86
    assert abs(A.local_power(0.0, 1.0)[()] - 0.05) < 1e-12


def test_saddlepoint():
    n = 5
    x = np.linspace(0.2, 3, 50)
    d = A.mean_exp_density(x, n)
    rel = d["saddle"] / d["exact"]
    assert np.allclose(rel, rel[0], rtol=1e-10)  # exact up to a constant (Stirling's)
    assert abs(rel[0] - 1) < 0.02
    t = A.lugannani_rice(np.array([1.5, 2.0, 2.5]), n)
    assert np.all(np.abs(t["lr"] / t["exact"] - 1) < 0.01)
    assert np.all(np.abs(t["normal"][1:] / t["exact"][1:] - 1) > 0.5)  # the normal tail is far off beyond 2


def test_uniform_bootstrap():
    r = A.uniform_max_bootstrap(200, 20000, rng(6))
    assert abs(r["atom0"] - (1 - (1 - 1 / 200) ** 200)) < 0.02
    mm = A.uniform_max_bootstrap(2000, 20000, rng(7), m=40)
    assert mm["atom0"] < 0.05 and mm["ks_exp"] < r["ks_exp"]
