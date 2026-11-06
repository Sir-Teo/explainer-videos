"""statkit.bayes II (Part 26): the hierarchical normal model, Bayes factors, evidence, SBC and the CRP."""

import numpy as np
from scipy import integrate, stats

from explainer.stats.kit import bayes as B

Y = np.array([28.0, 8, -3, 7, -1, 1, 18, 12])
S = np.array([15.0, 10, 16, 11, 9, 11, 10, 18])


def test_tau_posterior_matches_brute_force():
    h = B.hier_normal(Y, S, np.linspace(0, 40, 2001))

    def joint(mu, tau):  # p(mu, tau | y) up to a constant, flat priors
        return np.prod(stats.norm.pdf(Y, mu, np.sqrt(S ** 2 + tau ** 2)))

    taus = [1.0, 5.0, 10.0, 20.0]
    brute = np.array([integrate.quad(lambda m: joint(m, t), -100, 100)[0] for t in taus])
    mine = np.interp(taus, h.tau, h.post_tau)
    assert np.allclose(mine / mine[0], brute / brute[0], rtol=1e-4)


def test_eight_schools_known_summaries():
    h = B.hier_normal(Y, S, np.linspace(0, 60, 3001))
    d = h.draws(200_000, np.random.default_rng(1))
    # BDA3 Table 5.3 (uniform prior on tau): posterior medians about 10 (A) ... 7 (E); mean of mu about 8
    assert 7 < np.mean(d["mu"]) < 9
    med = np.median(d["theta"], 0)
    assert 9 < med[0] < 11.5 and 4 < med[4] < 6.5
    mean, var = h.cond_theta()
    k = np.searchsorted(h.tau, 10.0)
    assert np.all(np.abs(mean[k] - h.mu_hat[k]) <= np.abs(Y - h.mu_hat[k]) + 1e-9)
    assert np.allclose(mean[0], h.mu_hat[0]) and np.allclose(var[0], h.v_mu[0])  # tau = 0: complete pooling
    assert np.allclose(mean[-1], Y, atol=1.5)  # tau = 60: nearly no pooling


def test_bf01_normal_by_integration():
    xbar, n, sig, tau = 0.4, 25, 1.0, 0.5
    m1 = integrate.quad(lambda m: stats.norm.pdf(xbar, m, sig / 5) * stats.norm.pdf(m, 0, tau), -10, 10)[0]
    m0 = stats.norm.pdf(xbar, 0, sig / 5)
    assert np.isclose(B.bf01_normal(xbar, n, sig, tau), m0 / m1, rtol=1e-8)


def test_lindley_bf_grows_with_n_at_fixed_p():
    bfs = [B.bf01_normal(1.96 / np.sqrt(n), n, 1.0, 1.0) for n in (10, 100, 10_000)]
    assert bfs[0] < bfs[1] < bfs[2] and bfs[2] > 10


def test_sbb_bound():
    assert np.isclose(B.sbb_bound(0.05), -np.e * 0.05 * np.log(0.05))
    assert B.sbb_bound(0.5) == 1.0


def test_blr_evidence_by_integration():
    g = np.random.default_rng(3)
    x = g.normal(size=(6, 1))
    y = 0.7 * x[:, 0] + 0.3 * g.normal(size=6)
    alpha, sig = 2.0, 0.3
    ev = integrate.quad(lambda w: np.prod(stats.norm.pdf(y, w * x[:, 0], sig)) * stats.norm.pdf(w, 0, 1 / np.sqrt(alpha)), -10, 10)[0]
    assert np.isclose(B.blr_log_evidence(x, y, alpha, sig), np.log(ev), rtol=1e-6)


def test_sbc_uniform_for_a_correct_posterior():
    def prior(r):
        return r.normal()

    def data(th, r):
        return th + r.normal(size=5)

    def post(yv, L, r):
        v = 1 / (1 + 5)
        return v * yv.sum() + np.sqrt(v) * r.normal(size=L)

    ranks = B.sbc_ranks(prior, data, post, 2000, 19, np.random.default_rng(4))
    counts = np.bincount(ranks, minlength=20)
    assert stats.chisquare(counts).pvalue > 0.001


def test_crp_tables():
    g = np.random.default_rng(5)
    k = [len(np.unique(B.crp(200, 2.0, g))) for _ in range(400)]
    assert abs(np.mean(k) - B.crp_expected_tables(200, 2.0)) < 0.25
    w = B.stick_breaking(2.0, 400, g)
    assert np.isclose(w.sum(), 1.0, atol=1e-6)
