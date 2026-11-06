"""Tests for statkit.decision, the risk-set explorer of Part 45."""

import math

import numpy as np
from scipy import stats

from explainer.stats.kit import decision as D


def rng(seed=0):
    return np.random.default_rng(seed)


def test_finite_problem_bayes_and_minimax():
    # a coin is fair (p = .5) or biased (p = .8); X = heads in 3 tosses; actions: say fair / say biased
    px = np.array([stats.binom.pmf(range(4), 3, 0.5), stats.binom.pmf(range(4), 3, 0.8)])
    loss = np.array([[0, 1], [2, 0]])
    rp = D.risk_points(px, loss)
    assert len(rp["rules"]) == 16
    R = rp["R"]
    # the rule 'always say fair' has risk (0, 2); 'always biased' (1, 0)
    assert np.allclose(R[0], [0, 2]) and np.allclose(R[-1], [1, 0])
    lb = D.lower_boundary(R)
    assert np.allclose(lb[0], [0, 2]) and np.allclose(lb[-1], [1, 0])
    # every point lies on or above the lower boundary's supporting lines: the Bayes risk is minimized on the boundary
    for pi in (0.2, 0.5, 0.8):
        b = D.bayes_rule(R, pi)
        assert b["bayes_risk"] <= np.min(R @ [pi, 1 - pi]) + 1e-12
        assert np.min(lb @ [pi, 1 - pi]) <= b["bayes_risk"] + 1e-12
    mm = D.minimax(R)
    assert abs(mm["point"][0] - mm["point"][1]) < 1e-8  # an equalizer rule here
    # the minimax value equals the Bayes risk of the least favourable prior
    lf = mm["least_favourable"][0]
    assert abs(D.bayes_rule(R, lf)["bayes_risk"] - mm["value"]) < 1e-8


def test_binomial_risks():
    n = 16
    p = np.linspace(0, 1, 11)
    a = math.sqrt(n) / 2
    r = D.binomial_mse(n, p, a, a)
    assert np.allclose(r, 1 / (4 * (1 + math.sqrt(n)) ** 2))
    assert np.allclose(D.binomial_mse(n, p), p * (1 - p) / n)
    # simulated check of one Bayes risk
    g = rng(1)
    pp = g.beta(2, 3, 200000)
    x = g.binomial(n, pp)
    est = (x + 1) / (n + 2)
    assert abs(np.mean((est - pp) ** 2) - D.binomial_bayes_risk(n, 1, 1, 2, 3)) < 2e-4


def test_scale_and_absurd():
    n = 10
    c = np.array([1 / (n - 1), 1 / n, 1 / (n + 1)])
    m = D.scale_mse(n, c)
    assert abs(m[0] - 2 / (n - 1)) < 1e-12 and np.argmin(m) == 2 and abs(m[2] - 2 / (n + 1)) < 1e-12
    lam = np.array([0.3, 1.0, 2.5])
    a = D.absurd_umvue(lam)
    x = np.arange(200)
    for i, l in enumerate(lam):
        pmf = stats.poisson.pmf(x, l)
        t = math.exp(-2 * l)
        assert abs(np.sum(pmf * (-1.0) ** x) - t) < 1e-12  # unbiased
        assert abs(np.sum(pmf * ((-1.0) ** x - t) ** 2) - a["umvue"][i]) < 1e-12
        assert abs(np.sum(pmf * (np.exp(-2 * x) - t) ** 2) - a["mle"][i]) < 1e-12
        assert abs(np.sum(pmf * ((x % 2 == 0) - t) ** 2) - a["even"][i]) < 1e-12
    assert np.all(a["even"] < a["umvue"])


def test_expfam_duality():
    eta = np.linspace(-3, 2, 11)
    for name, A in (("bernoulli", lambda e: np.logaddexp(0, e)), ("poisson", np.exp), ("normal", lambda e: e ** 2 / 2)):
        d = D.expfam(name, eta)
        h = 1e-5
        dA = (A(eta + h) - A(eta - h)) / (2 * h)
        d2 = (A(eta + h) - 2 * A(eta) + A(eta - h)) / h ** 2
        assert np.allclose(dA, d["mu"], atol=1e-6) and np.allclose(d2, d["V"], atol=1e-3)
        num = D.legendre(A, np.linspace(-12, 12, 200001), d["mu"])
        assert np.allclose(num, d["Astar"], atol=1e-6)


def test_tanks():
    N, k = 300, 6
    t = D.tank_estimators(N, k)
    assert abs(t["umvue_mean"] - N) < 1e-8 and abs(t["umvue"] - t["umvue_exact"]) < 1e-8
    assert t["umvue"] < t["mom"] < t["one"]
    m, p = D.tank_max_pmf(N, k)
    assert abs(p.sum() - 1) < 1e-12
    # Rao-Blackwell: averaging 2 X_1 - 1 given M reproduces the UMVUE
    g = rng(2)
    draws = np.array([g.choice(N, k, replace=False) + 1 for _ in range(40000)])
    M = draws.max(1)
    sel = M == 280
    assert abs(np.mean(2 * draws[sel, 0] - 1) - D.rao_blackwell_one(280, k)) < 8
    assert abs(D.rao_blackwell_one(280, k) - (280 * 7 / 6 - 1)) < 1e-12


def test_ancillarity():
    c = D.cox_instruments()
    assert abs(0.5 * (c["cover_precise"] + c["cover_rough"]) - 0.9) < 1e-10
    assert c["cover_precise"] > 0.999 and 0.79 < c["cover_rough"] < 0.81
    g = rng(3)
    hits = 0
    for _ in range(4000):
        x = 2.0 + g.random(5) - 0.5
        lo, hi = D.uniform_location_interval(x)
        hits += lo <= 2.0 <= hi
    assert abs(hits / 4000 - 0.9) < 0.015


def test_information_bounds():
    b = D.bhattacharyya_theta2(np.array([0.0, 1.0]), 10)
    assert np.allclose(b["var_umvue"], b["bhatt2"]) and np.all(b["cr"] < b["var_umvue"])
    g = rng(4)
    x = g.normal(1.0, 1, (200000, 10)).mean(1)
    assert abs(np.var(x ** 2 - 0.1) - b["var_umvue"][1]) < 0.005
    for n in (2, 5, 20):
        cr = D.chapman_robbins_uniform(n)
        assert cr["bound"] < cr["var_umvue"]
        assert cr["bound"] * n ** 2 > 0.3 and cr["bound"] * n ** 2 < 1.0  # both are order 1/n^2


def test_pitman():
    g = rng(5)
    x = g.normal(0.3, 1, 7)
    assert abs(D.pitman_location(x, lambda z: -z ** 2 / 2) - x.mean()) < 1e-6  # normal: the mean
    xs = g.random((3000, 6)) - 0.5
    mid = (xs.max(1) + xs.min(1)) / 2
    assert abs(np.mean(mid ** 2) - 1 / (2 * 7 * 8)) < 0.0015
    # Laplace: Pitman beats the mean and the median
    xl = g.laplace(0, 1, (1500, 5))
    pit = np.array([D.pitman_location(r, lambda z: -np.abs(z), width=20, m=2001) for r in xl])
    assert np.mean(pit ** 2) < np.mean(np.median(xl, 1) ** 2) and np.mean(pit ** 2) < np.mean(xl.mean(1) ** 2)


def test_james_stein_exact_and_sure():
    p = 10
    for nrm in (0.0, 4.0, 25.0):
        theta = np.zeros(p)
        theta[0] = math.sqrt(nrm)
        x = rng(6).normal(theta, 1, (100000, p))
        s = np.sum(x ** 2, 1, keepdims=True)
        js = (1 - (p - 2) / s) * x
        sim = np.mean(np.sum((js - theta) ** 2, 1))
        assert abs(sim - D.js_risk(p, nrm)[0]) < 0.05
    assert abs(D.js_risk(p, 0.0)[0] - 2.0) < 1e-10  # p - (p - 2)^2 / (p - 2) = 2
    g = lambda z: -(p - 2) / np.sum(z ** 2) * z  # noqa: E731
    z = rng(7).normal(0, 1, p)
    assert abs(D.sure(z, g) - (p - (p - 2) ** 2 / np.sum(z ** 2))) < 1e-5


def test_strawderman_and_brown():
    p, a = 5, 0.5
    s = np.array([0.5, 3.0, 10.0, 40.0])
    e = D.strawderman_shrink(s, p, a)
    # check against direct numerical integration
    from scipy import integrate
    for si, ei in zip(s, e):
        k = p / 2 - a
        num = integrate.quad(lambda l: l ** (k + 1) * np.exp(-l * si / 2), 0, 1)[0]
        den = integrate.quad(lambda l: l ** k * np.exp(-l * si / 2), 0, 1)[0]
        assert abs(num / den - ei) < 1e-8
    # minimax: risk below p at several theta
    g = rng(8)
    for nrm in (0.0, 9.0, 36.0):
        theta = np.zeros(p)
        theta[0] = math.sqrt(nrm)
        x = g.normal(theta, 1, (60000, p))
        sh = D.strawderman_shrink(np.sum(x ** 2, 1), p, a)
        risk = np.mean(np.sum(((1 - sh)[:, None] * x - theta) ** 2, 1))
        assert risk < p
    R = np.array([10.0, 1e4])
    assert np.all(np.diff(D.brown_integral(3, R)) > 0) and D.brown_integral(3, 1e12) < 1.0 + 1e-9
    assert D.brown_integral(2, 1e12) > 27
    assert abs(D.bm_hit_ball(3, 2.0, 1e12) - 0.5) < 1e-9 and D.bm_hit_ball(2, 2.0, 1e12) > 0.97


def test_empirical_bayes():
    counts = [7840, 1317, 239, 42, 14, 4, 4, 1]
    r = D.robbins(counts)
    assert np.allclose(np.round(r[:7], 3), [0.168, 0.363, 0.527, 1.333, 1.429, 6.0, 1.75])
    gp = D.gamma_poisson(counts)
    assert gp["post_mean"][0] < gp["post_mean"][1] < gp["post_mean"][2]
    npm = D.poisson_npmle(counts)
    assert npm["loglik"] >= gp["loglik"] - 1e-6  # the NPMLE's likelihood is at least the gamma fit's
    assert np.all(np.diff(npm["post_mean"]) > 0)  # NPMLE posterior means are monotone
