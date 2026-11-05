"""statkit.mle, checked against closed forms, SciPy and simulation."""

import numpy as np
import pytest
from scipy import optimize, stats

from explainer.stats.kit import mle as M


def mixture_sample(n=3000, seed=0):
    g = np.random.default_rng(seed)
    z = g.random(n) < 0.4
    return np.where(z, g.normal(0, 1, n), g.normal(3, 0.6, n))


def test_em_is_monotone_and_matches_direct_maximization():
    x = mixture_sample()
    r = M.em_mixture(x, [0.5, -0.5, 1.5, 2.5, 1.5])
    assert np.all(np.diff(r["loglik"]) >= -1e-8)
    th = r["theta"]
    assert th[0] == pytest.approx(0.4, abs=0.03) and th[3] == pytest.approx(3.0, abs=0.05)
    neg = lambda t: -M.mix_loglik(x, t)  # noqa: E731
    ref = optimize.minimize(neg, th, method="Nelder-Mead", options={"xatol": 1e-8, "fatol": 1e-8, "maxiter": 5000})
    assert -ref.fun <= r["loglik"][-1] + 1e-4
    assert 0 < r["rate"] < 1


def test_em_with_counts_equals_em_on_expanded_data():
    g = np.random.default_rng(1)
    v = np.round(mixture_sample(500, 1), 1)
    u, c = np.unique(v, return_counts=True)
    a = M.em_mixture(u, [0.5, 0, 1, 3, 1], w=c, iters=200)
    b = M.em_mixture(v, [0.5, 0, 1, 3, 1], iters=200)
    assert np.allclose(a["theta"], b["theta"], atol=1e-8)


def test_mixture_moments_against_simulation():
    th = [0.3, -1.0, 0.5, 2.0, 1.2]
    g = np.random.default_rng(2)
    n = 2_000_000
    z = g.random(n) < th[0]
    y = np.where(z, g.normal(th[1], th[2], n), g.normal(th[3], th[4], n))
    m = y.mean()
    emp = [m] + [np.mean((y - m) ** k) for k in range(2, 5)]
    assert np.allclose(M.mix_moments(th, 4), emp, rtol=0.01, atol=0.01)


def test_pearson_moments_recovers_a_true_mixture():
    th = np.array([0.4, 0.0, 1.0, 3.0, 0.6])
    # exact moments as "data": build a weighted sample on a fine grid with the mixture density as weights
    x = np.linspace(-6, 7, 20001)
    w = th[0] * stats.norm.pdf(x, 0, 1) + (1 - th[0]) * stats.norm.pdf(x, 3, 0.6)
    r = M.pearson_moments(x, w, starts=200)
    assert any(np.allclose(s, th, atol=2e-3) for s in r["solutions"])


def test_binomial_trinity_closed_forms():
    r = M.binomial_trinity(14, 20, 0.5)
    assert r["score"] == pytest.approx((0.7 - 0.5) ** 2 / (0.25 / 20))
    assert r["wald"] == pytest.approx((0.7 - 0.5) ** 2 / (0.21 / 20))
    ll = lambda p: 14 * np.log(p) + 6 * np.log(1 - p)  # noqa: E731
    assert r["lr"] == pytest.approx(2 * (ll(0.7) - ll(0.5)))


def test_logistic_tests_and_profile_interval():
    g = np.random.default_rng(3)
    x = g.normal(size=200)
    y = (g.random(200) < 1 / (1 + np.exp(-(0.2 + 1.0 * x)))).astype(float)
    r = M.logistic_slope_tests(x, y)
    import statsmodels.api as sm
    ref = sm.Logit(y, sm.add_constant(x)).fit(disp=0)
    assert np.allclose(r["b"], ref.params, atol=1e-6) and r["se"] == pytest.approx(ref.bse[1], rel=1e-5)
    assert r["lr"] == pytest.approx(2 * (ref.llf - ref.llnull), rel=1e-6)
    lo, hi = M.logistic_profile_ci(x, y)
    assert lo < r["b"][1] < hi and hi - lo == pytest.approx(2 * 1.96 * r["se"], rel=0.15)


def test_gamma_profile_peaks_at_the_mle():
    g = np.random.default_rng(4)
    x = g.gamma(3.0, 1 / 2.0, 400)
    a, loc, scale = stats.gamma.fit(x, floc=0)
    pr = M.gamma_profile(x, np.linspace(1, 6, 5001))
    assert pr["a_hat"] == pytest.approx(a, abs=2e-3)


def test_neyman_scott_halves_the_variance():
    r = M.neyman_scott(200_000, 2.0, np.random.default_rng(5))
    assert r["mle"] == pytest.approx(2.0, rel=0.02) and r["fixed"] == pytest.approx(4.0, rel=0.02)


def test_poisson_sandwich_against_statsmodels():
    g = np.random.default_rng(6)
    x = g.normal(size=500)
    mu = np.exp(0.5 + 0.4 * x)
    y = g.negative_binomial(2, 2 / (2 + mu))  # overdispersed counts with mean mu
    X = np.column_stack([np.ones(500), x])
    r = M.poisson_regression(X, y)
    import statsmodels.api as sm
    ref = sm.GLM(y, X, family=sm.families.Poisson()).fit(cov_type="HC0")
    assert np.allclose(r["b"], ref.params, atol=1e-6)
    assert np.allclose(r["se_sandwich"], ref.bse, rtol=1e-4)
    assert r["phi"] > 1.5 and np.all(r["se_sandwich"] > r["se_model"])


def test_cauchy_mle_and_information():
    g = np.random.default_rng(7)
    x = g.standard_cauchy(101) + 2.0
    t = M.cauchy_mle(x)
    ref = optimize.minimize_scalar(lambda s: np.sum(np.log1p((x - s) ** 2)), bracket=(t - 1, t, t + 1)).x
    assert t == pytest.approx(ref, abs=1e-5)
    assert M.cauchy_observed_info(x, t) > 0


def test_numerical_hessian():
    f = lambda t: -(t[0] ** 2 + 3 * t[0] * t[1] + 5 * t[1] ** 2)  # noqa: E731
    assert np.allclose(M.numerical_hessian(f, [0.3, -0.2]), [[-2, -3], [-3, -10]], atol=1e-5)


def test_ising_pseudolikelihood_is_consistent():
    g = np.random.default_rng(8)
    est = [M.ising_pseudo_mle(M.ising_gibbs(48, 0.3, 300, g))["beta"] for _ in range(4)]
    assert np.mean(est) == pytest.approx(0.3, abs=0.03)
