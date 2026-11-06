"""Tests for statkit.bnp, the Bayesian asymptotics and nonparametric Bayes toolkit of Part 53."""

import math

import numpy as np
from scipy import stats

from explainer.stats.kit import bnp as B


def rng(seed=0):
    return np.random.default_rng(seed)


def test_sequence_model_posterior_and_risk():
    K, n = 400, 1000
    lam = B.prior_var(K, 1.0)
    th = B.sobolev_truth(K, 1.0)
    r = rng(1)
    Y = th + r.standard_normal((3000, K)) / math.sqrt(n)
    post = B.posterior(Y, n, lam)
    mc = np.mean(np.sum((post["mean"] - th) ** 2, axis=1))
    ex = B.risk(th, n, lam)
    assert abs(mc / ex["risk"] - 1) < 0.03
    # the posterior variance is the conjugate one
    assert np.allclose(post["var"], 1 / (1 / lam + n))


def test_coverage_exact_and_oversmoothing():
    K, n = 2000, 10000
    th = B.sobolev_truth(K, 1.0)
    a = np.zeros(K)
    a[0] = 1.0  # the first coefficient
    good = B.functional_coverage(th, n, B.prior_var(K, 1.0), a)
    assert abs(good["coverage"] - 0.95) < 0.01
    # Monte Carlo check of the exact formula
    lam = B.prior_var(K, 2.0)
    r = rng(2)
    w = n * lam / (1 + n * lam)
    Y0 = th[0] + r.standard_normal(200000) / math.sqrt(n)
    c = B.functional_coverage(th, n, lam, a)
    hit = np.abs(w[0] * Y0 - th[0]) <= 1.959964 * c["s_post"]
    assert abs(hit.mean() - c["coverage"]) < 0.005
    over = B.credible_ball_coverage(th, n, B.prior_var(K, 2.5), reps=2000, rng=rng(3))
    under = B.credible_ball_coverage(th, n, B.prior_var(K, 0.5), reps=2000, rng=rng(4))
    assert over["coverage"] < 0.2 and under["coverage"] > 0.95


def test_empirical_bayes_and_rates():
    K, n = 2000, 10000
    th = B.sobolev_truth(K, 1.0)
    Y = th + rng(5).standard_normal(K) / math.sqrt(n)
    a = B.eb_alpha(Y, n)
    assert 0.5 < a < 2.0
    assert abs(B.contraction_rate(n, 1.0, 1.0) - n ** (-1 / 3)) < 1e-12


def test_bvm_and_misspecification():
    tv = [B.bvm_tv_beta(int(0.3 * m), m) for m in (10, 100, 1000, 10000)]
    assert all(a > b for a, b in zip(tv, tv[1:])) and tv[-1] < 0.01
    r = rng(6)
    y = r.negative_binomial(2, 0.2, 400)
    lo, hi = B.poisson_gamma_ci(y)
    lo2, hi2 = B.poisson_gamma_ci(y, eta=B.calibrated_eta(y))
    assert (hi2 - lo2) > 1.8 * (hi - lo)


def test_dirichlet_process():
    r = rng(7)
    data = r.standard_normal(200)
    x = np.linspace(-3, 3, 61)
    H = B.dp_posterior_cdf(x, data, 1.0, stats.norm.cdf)
    lo, hi = B.dp_band(x, data, 1.0, stats.norm.cdf)
    mid = (H > 0.05) & (H < 0.95)  # in the far tails a skewed Beta's 97.5% point can sit below its mean
    assert np.all(lo[mid] <= H[mid]) and np.all(H[mid] <= hi[mid])
    assert np.max(np.abs(H - stats.norm.cdf(x))) < 0.12  # the KS 99% point is 1.63/sqrt(200)
    d = B.polya_urn(2000, 5.0, lambda g: g.standard_normal(), r)
    k = len(np.unique(d))
    assert abs(k - 5 * math.log(1 + 2000 / 5)) < 12  # expected number of tables ~ alpha log(1 + n/alpha)
    w = B.stick_weights(2.0, 200, r)
    assert abs(w.sum() - 1) < 1e-3
    x2 = np.concatenate([r.normal(0, 1, 80), r.normal(5, 0.6, 80)])
    out = B.dp_mixture_gibbs(x2, 1.0, 120, r, burn=40)
    assert np.median(out["k_trace"][40:]) >= 2
    assert abs(np.trapezoid(out["density"], out["grid"]) - 1) < 0.05


def test_sparse_means():
    r = rng(8)
    theta = np.concatenate([np.zeros(450), np.full(50, 5.0)])
    y = theta + r.standard_normal(500)
    ss = B.spike_slab_posterior(y)
    assert ss["incl"][-50:].mean() > 0.9 and ss["incl"][:450].mean() < 0.1
    lo, hi = B.spike_slab_interval(0.0, 3.0, 1.0)
    assert lo == 0.0 or abs(lo) < 1e-6
    h = B.horseshoe_posterior(6.0, 0.1)
    assert 4.5 < h["mean"] < 6.0 and h["lo"] < 6.0 < h["hi"] + 2
    h0 = B.horseshoe_posterior(0.0, 0.1)
    assert abs(h0["mean"]) < 1e-6
