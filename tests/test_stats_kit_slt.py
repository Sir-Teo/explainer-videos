"""Tests for statkit.slt, the statistical learning theory toolkit of Part 54."""

import math

import numpy as np

from explainer.stats.kit import slt as L


def rng(seed=0):
    return np.random.default_rng(seed)


def test_erm_and_vc():
    r = rng(1)
    dev, ex = [], []
    for _ in range(200):
        x, y = L.threshold_data(400, r)
        t = L.erm_threshold(x, y)
        ex.append(float(L.threshold_risk(t) - 0.1))
        dev.append(L.uniform_deviation_threshold(x, y))
    assert np.mean(dev) < L.rademacher_vc_bound(400, 1) < L.vc_bound(400, 1)
    assert np.mean(ex) < np.mean(dev)  # excess risk is faster than the uniform deviation (Massart noise)
    # realizable: excess risk ~ 1/n
    e = []
    for _ in range(400):
        x, y = L.threshold_data(500, r, eta=0.0)
        e.append(float(L.threshold_risk(L.erm_threshold(x, y), eta=0.0)))
    assert abs(np.mean(e) * 500 - 1) < 0.25
    assert L.finite_class_bound(1000, 10) < L.finite_class_bound(1000, 1000)


def test_rademacher():
    r = rng(2)
    X = r.standard_normal((300, 8))
    a = L.rademacher_linear(X, 1.0, r)
    assert a <= L.rademacher_linear_bound(X, 1.0) and a > 0.9 * L.rademacher_linear_bound(X, 1.0)
    K = L.gaussian_kernel(X, 1.5)
    assert L.rademacher_kernel(K, 1.0, r) <= math.sqrt(np.trace(K)) / 300 + 1e-12


def test_boosting_and_pac_bayes():
    r = rng(3)
    X = r.standard_normal((200, 2))
    y = np.sign(X[:, 0] ** 2 + X[:, 1] ** 2 - 1.4)
    out = L.adaboost(X, y, 150)
    assert out["train"][-1] < out["train"][0]
    assert L.kl_bernoulli(0.1, 0.1) < 1e-12
    p = L.kl_inverse(0.1, 0.05)
    assert abs(L.kl_bernoulli(0.1, p) - 0.05) < 1e-6
    b = L.pac_bayes_bounds(0.1, 3.0, 2000)
    assert 0.1 < b["kl"] < b["mcallester"]
    rho = L.gibbs_posterior([0.1, 0.2, 0.3], 50.0)
    assert rho[0] > rho[1] > rho[2] and abs(rho.sum() - 1) < 1e-12


def test_stability_online_surrogates():
    r = rng(4)
    X = r.standard_normal((200, 5))
    X /= np.linalg.norm(X, axis=1, keepdims=True)
    y = np.clip(X @ np.ones(5) / 3 + 0.1 * r.standard_normal(200), -1, 1)
    s1 = L.ridge_stability(X, y, 0.1)
    s2 = L.ridge_stability(X, y, 1.0)
    assert s2["stability"] < s1["stability"] and s1["stability"] <= s1["bound"]
    Lm = r.random((3000, 20))
    reg = L.hedge(Lm, math.sqrt(8 * math.log(20) / 3000))["regret"][-1]
    assert reg <= L.hedge_bound(3000, 20) + 5
    th = np.linspace(-1, 1, 11)
    for loss in ("hinge", "squared", "exponential", "logistic"):
        ps = L.psi_transform(th, loss)
        assert np.all(ps >= -1e-12) and abs(L.psi_transform([0.0], loss)[0]) < 1e-9 and np.all(ps <= np.abs(th) + 1e-9)


def test_interpolation():
    r = rng(5)
    peak = L.min_norm_risk(100, 100, r, reps=5)
    under = L.min_norm_risk(100, 50, r, reps=5)
    over = L.min_norm_risk(100, 400, r, reps=5)
    assert peak > 5 * under and peak > 5 * over
    b = L.benign_risk(200, r, reps=3)
    assert b["excess"] < 0.2 * b["noise"]


def test_sgd_stability_and_bandits():
    r = rng(7)
    n, p = 100, 5
    X = r.standard_normal((n, p))
    X /= np.maximum(1, np.linalg.norm(X, axis=1))[:, None]
    y = np.sign(X[:, 0] + 0.3 * r.standard_normal(n))
    d = L.sgd_divergence(X, y, 500, 0.5, r, reps=10)
    assert np.all(d["divergence"] <= d["bound"] + 1e-9)  # Seeded mean diagnostic; the HRS theorem is in expectation, not pathwise.
    assert d["divergence"][-1] > d["divergence"][50]
    mu = [0.5, 0.4, 0.3]
    ucb = np.mean([L.bandit(mu, 20000, "ucb", r)[-1] for _ in range(3)])
    gr = np.mean([L.bandit(mu, 20000, "greedy", r, eps=0.1)[-1] for _ in range(3)])
    assert ucb < gr  # fixed exploration costs linear regret
    assert abs(gr - 20000 * 0.1 * (0.1 + 0.2) / 3) < 40
    assert L.lai_robbins(mu, 20000) < ucb
