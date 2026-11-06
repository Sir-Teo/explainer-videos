"""statkit.thesis (Part 65): the dissertation's bound, weights, intervals and study."""

import math

import numpy as np

from explainer.stats.kit import thesis as T


def test_tv_formulas_agree():
    # the closed form for Gaussian shifts against the grid integral of the reweighted source
    for mu, lam in ((1.0, 0.5), (1.5, 0.0), (0.5, 1.2), (1.0, 1.0)):
        w = lambda x, mu=mu, lam=lam: np.exp(lam * (mu * x - mu * mu / 2))  # noqa: E731
        assert abs(T.tv_reweighted(w, mu) - T.tv_gauss_shift(lam * mu, mu)) < 1e-7
    assert T.tv_gauss_shift(0.0, 0.0) == 0.0
    assert abs(T.coverage_bound(0.1, 1.0, 1.0) - 0.9) < 1e-12
    # Pinsker: TV <= sqrt(KL / 2), with KL(N(a,1) || N(b,1)) = (a - b)^2 / 2
    for d in (0.1, 0.5, 1.0, 2.0):
        assert T.tv_gauss_shift(0, d) <= math.sqrt(d * d / 4) + 1e-12


def test_logistic_weights_recover_a_gaussian_tilt():
    rng = np.random.default_rng(1)
    xs, xt = rng.standard_normal(20000), 1.0 + rng.standard_normal(20000)
    w = T.logistic_weights(xs, xt)
    # log w = b0 + b1 x with b1 near mu = 1 and b0 near -mu^2 / 2
    assert abs(w.coef[1] - 1.0) < 0.05 and abs(w.coef[0] + 0.5) < 0.05


def test_weighted_interval_scale_invariance_and_unweighted_case():
    rng = np.random.default_rng(2)
    xc, yc = T.draw(300, 0.0, 0.5, rng)
    xt = rng.standard_normal(20)
    w1 = lambda x: np.exp(0.7 * np.asarray(x))  # noqa: E731
    w2 = lambda x: 5.0 * np.exp(0.7 * np.asarray(x))  # noqa: E731
    assert np.allclose(T.weighted_interval(xc, yc, w1, xt, 0.1), T.weighted_interval(xc, yc, w2, xt, 0.1))
    # constant weights reproduce ordinary split conformal (up to the test point's weight at +inf)
    h0 = T.weighted_interval(xc, yc, None, xt, 0.1)
    hc = T.weighted_interval(xc, yc, lambda x: np.ones_like(np.asarray(x, float)), xt, 0.1)
    assert np.allclose(h0, hc)


def test_the_theorem_holds_in_a_small_study():
    rng = np.random.default_rng(3)
    res = T.study([1.0], [1.0], ["none", "oracle", "tempered"], 150, 300, 300, 0.1, rng)
    by = {r["method"]: r for r in res}
    for r in res:
        assert r["coverage"] >= r["bound"] - 4 * r["mcse"]
    assert by["oracle"]["coverage"] > 0.88 and by["none"]["coverage"] < 0.8
    assert by["none"]["bound"] < by["tempered"]["bound"] < by["oracle"]["bound"] + 1e-9


def test_selection_probs():
    p = T.selection_probs(np.array([45.0, 85.0, 20.0]))
    assert abs(p[0] - 0.5) < 1e-12 and p[1] < 0.01 and p[2] > 0.95
