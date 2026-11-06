"""Tests for statkit.semipar, the semiparametric toolkit of Part 49."""

import math

import numpy as np

from explainer.stats.kit import semipar as S


def rng(seed=0):
    return np.random.default_rng(seed)


def test_discrete_gradients_and_paths():
    p = np.array([0.1, 0.2, 0.3, 0.4])
    g = np.array([1.0, 2.0, 5.0, 7.0])
    phi = S.gradient_discrete(lambda q: float(np.sum(q * g)), p)
    assert np.allclose(phi, g - np.sum(p * g), atol=1e-6)
    # a nonlinear functional: the variance; its influence function is (g - mu)^2 - sigma^2
    var = lambda q: float(np.sum(q * g ** 2) - np.sum(q * g) ** 2)  # noqa: E731
    mu = np.sum(p * g)
    assert np.allclose(S.gradient_discrete(var, p), (g - mu) ** 2 - var(p), atol=1e-5)
    # pathwise derivative = <phi, s> for any score s
    for s in (np.array([1.0, -1, 0.5, 0]), np.array([0.0, 0, 1, -1])):
        assert abs(S.pathwise_derivative(var, p, s) - S.inner(p, S.gradient_discrete(var, p), S.center(p, s))) < 1e-5


def test_projection_and_independence_bound():
    p1, p2 = np.array([0.3, 0.7]), np.array([0.6, 0.4])
    P = np.outer(p1, p2).ravel()
    phi = S.gradient_discrete(lambda q: q[0], P)
    eff = S.project(P, phi, S.independence_scores(2, 2))
    assert abs(S.bound(P, phi) - P[0] * (1 - P[0])) < 1e-6
    target = p2[0] ** 2 * p1[0] * (1 - p1[0]) + p1[0] ** 2 * p2[0] * (1 - p2[0])  # delta method for p1 q1
    assert abs(S.bound(P, eff) - target) < 1e-6
    # the residual is orthogonal to the tangent space
    for b in S.independence_scores(2, 2):
        assert abs(S.inner(P, phi - eff, S.center(P, b))) < 1e-9
    # simulation: the product of margins has the efficient variance
    n = 400
    x1 = rng(1).random((20000, n)) < p1[0]
    x2 = rng(2).random((20000, n)) < p2[0]
    est = x1.mean(axis=1) * x2.mean(axis=1)
    assert abs(n * est.var() - target) < 0.006


def test_fisher_information_and_adaptive():
    assert abs(S.fisher_location("t3") - 2 / 3) < 1e-12
    assert 0.6 < S.fisher_location("mixture") < 0.8
    r = rng(3)
    est, mean = [], []
    for _ in range(300):
        x = S.draw_symmetric("t3", r, 400) + 2.0
        est.append(S.adaptive_location(x)["est"])
        mean.append(x.mean())
    v = 400 * np.var(est)
    assert abs(np.mean(est) - 2.0) < 0.03
    assert v < 400 * np.var(mean)  # better than the mean for t3
    assert v < 1.4 / S.fisher_location("t3")  # within 40% of the bound at n = 400


def test_ate_estimators():
    r = rng(4)
    o, t, cov = [], [], []
    for _ in range(300):
        w = S.rate_world(800, r)
        a = S.ate_one_step(w["y"], w["t"], w["mu0"], w["mu1"], w["e"])
        b = S.ate_tmle(w["y"], w["t"], w["mu0"], w["mu1"], w["e"])
        assert abs(b["eif_mean"]) < 1e-8  # TMLE solves the EIF equation
        o.append(a["est"])
        t.append(b["est"])
        cov.append(a["lo"] <= 1.5 <= a["hi"])
    assert abs(np.mean(o) - 1.5) < 0.02 and abs(np.mean(t) - 1.5) < 0.02
    assert 0.85 < np.mean(cov) < 0.95
    w = S.rate_world(800, r)
    ip = S.ate_ipw(w["y"], w["t"], w["e"])
    assert abs(ip["est"] - 1.5) < 5 * ip["se"]


def test_product_rate():
    r = rng(5)

    def bias(a, b, n, reps=150):
        out = []
        for _ in range(reps):
            w = S.rate_world(n, r)
            k = S.corrupt(w, a, b)
            out.append(S.ate_one_step(w["y"], w["t"], k["mu0"], k["mu1"], k["e"])["est"] - 1.5)
        return math.sqrt(n) * np.mean(out)

    # a + b = 1/2: root-n bias stays put; a + b = 1/4: it grows like n^(1/4)
    s1, s2 = bias(0.25, 0.25, 400), bias(0.25, 0.25, 6400)
    f1, f2 = bias(0.125, 0.125, 400), bias(0.125, 0.125, 6400)
    assert abs(s2 / s1 - 1) < 0.35
    assert 1.5 < f2 / f1 < 2.6


def test_mar_mean_and_int_sq():
    r = rng(6)
    n = 4000
    X = r.standard_normal(n)
    y = 1 + 2 * X + r.standard_normal(n)
    e = 1 / (1 + np.exp(-(0.5 + X)))
    R = (r.random(n) < e).astype(float)
    o = S.mar_mean(y, R, X, e, 1 + 2 * X)
    assert abs(o["aipw"] - 1) < 4 * o["aipw_se"]
    assert o["cc"] > 1.3  # complete cases are biased upward
    assert abs(o["ipw"] - 1) < 0.15
    psi = S.int_sq_normal()
    vals = [S.int_sq_estimates(r.standard_normal(400), 0.05, r) for _ in range(200)]
    b_plug = np.mean([v["plugin"] for v in vals]) - psi
    b_u = np.mean([v["ustat"] for v in vals]) - psi
    assert b_plug > 3 * abs(b_u)  # the diagonal term 1/(n h sqrt(4 pi)) is the plug-in's bias
