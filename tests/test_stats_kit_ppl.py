"""statkit.ppl (Part 27): NUTS, HMC and ADVI against closed-form posteriors; diagnostics; PSIS."""

import numpy as np
import pytest
from scipy import stats

from explainer.stats.kit import bayes as B
from explainer.stats.kit import ppl as P


def test_gradient_by_finite_differences():
    y = np.array([1.2, -0.3, 2.2])

    def logp(p):
        return P.normal_lpdf(y, p["mu"], p["s"]) + P.halfcauchy_lpdf(p["s"], 2.0) + P.normal_lpdf(p["mu"], 0.0, 5.0)

    m = P.Model({"mu": (1, "real"), "s": (1, "positive")}, logp)
    u = np.array([0.4, -0.2])
    _, g = m.logp_grad(u)
    h = 1e-6
    fd = [(m.log_density(u + h * e) - m.log_density(u - h * e)) / (2 * h) for e in np.eye(2)]
    assert np.allclose(g, fd, rtol=1e-5)


def test_nuts_normal_mean_matches_conjugate():
    g = np.random.default_rng(1)
    y = g.normal(1.0, 2.0, 20)

    def logp(p):
        return P.normal_lpdf(p["mu"], 0.0, 3.0) + P.normal_lpdf(y, p["mu"], 2.0)

    fit = P.sample(P.Model({"mu": (1, "real")}, logp), chains=2, iters=1500, warmup=500, seed=2)
    mu = fit.draws["mu"][..., 0].ravel()
    m, s = B.normal_update(0.0, 3.0, y.mean(), 2.0, 20)
    assert abs(mu.mean() - m) < 4 * s / np.sqrt(P.ess_bulk(fit.draws["mu"][..., 0]))
    assert abs(mu.std() / s - 1) < 0.08
    assert P.rhat(fit.draws["mu"][..., 0]) < 1.01
    assert fit.divergent.sum() == 0


def test_nuts_beta_binomial_with_unit_transform():
    s_, n_ = 7, 20

    def logp(p):
        return P.binomial_logit_lpmf(s_, n_, (p["p"] / (1.0 - p["p"])).log()) + 0.0 * p["p"].sum()

    fit = P.sample(P.Model({"p": (1, "unit")}, logp), chains=2, iters=2000, warmup=500, seed=3)
    pdraws = fit.draws["p"][..., 0].ravel()
    a, b = 1 + s_, 1 + n_ - s_  # uniform prior: the transform's Jacobian makes it so
    assert abs(pdraws.mean() - a / (a + b)) < 0.01
    assert abs(np.quantile(pdraws, 0.9) - stats.beta.ppf(0.9, a, b)) < 0.015


def test_nuts_noncentred_eight_schools_matches_grid():
    y = np.array([28.0, 8, -3, 7, -1, 1, 18, 12])
    s = np.array([15.0, 10, 16, 11, 9, 11, 10, 18])

    def logp(p):
        theta = p["mu"] + p["tau"] * p["z"]
        return (P.normal_lpdf(p["mu"], 0.0, 5.0) + P.halfcauchy_lpdf(p["tau"], 5.0) + P.normal_lpdf(p["z"], 0.0, 1.0)
                + P.normal_lpdf(y, theta, s))

    fit = P.sample(P.Model({"mu": (1, "real"), "tau": (1, "positive"), "z": (8, "real")}, logp), chains=2, iters=1000,
                   warmup=1000, seed=4)
    tau = fit.draws["tau"][..., 0].ravel()
    grid = np.linspace(0, 60, 6001)
    h = B.hier_normal(y, s, grid, lambda t: stats.halfcauchy.logpdf(t, scale=5), mu_prior=(0.0, 5.0))
    cdf = np.cumsum(h.post_tau * np.gradient(grid))
    cdf /= cdf[-1]
    med = np.interp(0.5, cdf, grid)
    assert abs(np.median(tau) - med) < 0.35
    assert fit.divergent.mean() < 0.01


def test_rhat_flags_stuck_chains():
    g = np.random.default_rng(5)
    good = g.normal(size=(4, 1000))
    bad = good + np.array([0, 0, 0, 3.0])[:, None]
    assert P.rhat(good) < 1.01 and P.rhat(bad) > 1.3
    assert 3000 < P.ess_bulk(good) < 5000


def test_ess_of_ar1_matches_theory():
    g = np.random.default_rng(6)
    phi, n = 0.8, 20000
    x = np.zeros((2, n))
    for c in range(2):
        e = g.normal(size=n)
        for t in range(1, n):
            x[c, t] = phi * x[c, t - 1] + e[t]
    theory = 2 * n * (1 - phi) / (1 + phi)
    assert abs(P.ess_basic(x) / theory - 1) < 0.15


def test_gpd_fit_recovers_shape():
    for k in (0.2, 0.5, 0.8):
        x = stats.genpareto.rvs(k, scale=1, size=2000, random_state=1)
        assert abs(P._gpd_fit(x)[0] - k) < 0.06


def test_psis_khat():
    g = np.random.default_rng(7)
    # target N(0, 1), proposal t_3: bounded weights, k-hat small
    x = stats.t.rvs(3, size=4000, random_state=g)
    _, k_good = P.psis(stats.norm.logpdf(x) - stats.t.logpdf(x, 3))
    # target Cauchy, proposal N(0, 1): weights with infinite variance, k-hat large
    z = g.normal(size=4000)
    _, k_bad = P.psis(stats.cauchy.logpdf(z) - stats.norm.logpdf(z))
    assert k_good < 0.5 and k_bad > 0.7


def test_advi_mean_field_gaussian():
    rho = 0.9
    S = np.array([[1, rho], [rho, 1]])
    Si = np.linalg.inv(S)

    def logp(p):
        x = p["x"]
        return ((x @ Si) * x).sum() * -0.5

    fit = P.advi(P.Model({"x": (2, "real")}, logp), 3000, np.random.default_rng(8), lr=0.02)
    sd = np.exp(fit["log_sd"])
    assert np.allclose(sd, np.sqrt(1 - rho ** 2), rtol=0.15)  # mean field: 1/sqrt(precision diagonal)
    assert np.allclose(fit["mean"], 0, atol=0.1)


def test_gibbs_probit_matches_mle():
    g = np.random.default_rng(9)
    X = np.column_stack([np.ones(400), g.normal(size=400)])
    y = (X @ np.array([-0.3, 0.8]) + g.normal(size=400) > 0).astype(float)
    draws = P.gibbs_probit(X, y, 3000, g)[500:]
    import statsmodels.api as sm
    mle = sm.Probit(y, X).fit(disp=0)
    assert np.allclose(draws.mean(0), mle.params, atol=0.03)
    assert np.allclose(draws.std(0), mle.bse, rtol=0.12)


def test_smc_evidence_matches_exact():
    g = np.random.default_rng(10)
    x = np.linspace(-1, 1, 15)
    X = np.column_stack([np.ones(15), x])
    y = 0.3 + 0.9 * x + 0.3 * g.normal(size=15)
    alpha, sig = 1.0, 0.3
    exact = B.blr_log_evidence(X, y, alpha, sig)
    res = P.smc_tempering(lambda n, r: r.normal(0, 1 / np.sqrt(alpha), (n, 2)),
                          lambda w: float(np.sum(stats.norm.logpdf(y, X @ w, sig))),
                          lambda w: float(np.sum(stats.norm.logpdf(w, 0, 1 / np.sqrt(alpha)))), 2000, g)
    assert abs(res["log_evidence"] - exact) < 0.15


def test_particle_filter_against_kalman():
    g = np.random.default_rng(11)
    x = np.cumsum(g.normal(0, 0.5, 50))
    y = x + g.normal(0, 1.0, 50)
    k = P.kalman_local_level(y, 0.25, 1.0)
    pf = P.particle_filter(y, 4000, 0.25, 1.0, g)
    assert np.max(np.abs(pf["mean"] - k["mean"])) < 0.15
    assert abs(pf["loglik"] - k["loglik"]) < 0.5


def test_cftp_returns_coalesced_state():
    res = P.cftp_ising(6, 0.3, np.random.default_rng(12))
    assert res["state"].shape == (6, 6) and set(np.unique(res["state"])) <= {-1, 1}
    m = res["mags"]
    assert np.isclose(m[-1, 0], m[-1, 1])
