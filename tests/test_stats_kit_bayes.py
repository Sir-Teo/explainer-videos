import numpy as np
import pytest
from scipy import integrate, special, stats

from explainer.stats.kit import bayes as B


def test_conjugate_updates():
    assert B.beta_update(1, 1, 7, 3) == (8, 4)
    assert B.gamma_update(2, 1, 10, 4) == (12, 5)
    m, s = B.normal_update(0, 1, 2.0, 1.0, 4)
    assert m == pytest.approx(8 / 5) and s == pytest.approx(np.sqrt(1 / 5))
    # sequential = batch
    a, b = B.beta_update(*B.beta_update(1, 1, 3, 2), 4, 1)
    assert (a, b) == B.beta_update(1, 1, 7, 3)


def test_credible_and_hpd():
    d = stats.beta(3, 9)
    lo, hi = B.credible(d)
    assert d.cdf(hi) - d.cdf(lo) == pytest.approx(0.95)
    h0, h1 = B.hpd(d)
    assert d.cdf(h1) - d.cdf(h0) == pytest.approx(0.95, abs=1e-6)
    assert h1 - h0 < hi - lo
    assert d.pdf(h0) == pytest.approx(d.pdf(h1), rel=1e-3)


def test_predictive_and_succession():
    p = B.beta_binomial_pmf(np.arange(11), 10, 3.0, 5.0)
    assert p.sum() == pytest.approx(1.0)
    assert np.allclose(p, stats.betabinom.pmf(np.arange(11), 10, 3, 5))
    assert B.rule_of_succession(5, 5) == pytest.approx(6 / 7)


def test_normal_unknown_variance_matches_t():
    x = np.array([1.2, 0.4, 2.2, 1.9, 0.7, 1.5])
    r = B.normal_unknown_var(x)
    t = stats.t(r["df"], loc=r["loc"], scale=r["scale"])
    assert B.credible(t)[0] == pytest.approx(stats.t.interval(0.95, 5, loc=x.mean(), scale=stats.sem(x))[0])


def test_grid_metropolis_bf():
    g = np.linspace(0, 1, 2001)
    post = B.grid_posterior(g, lambda p: np.zeros_like(p), lambda p: 7 * np.log(np.clip(p, 1e-300, 1)) + 3 * np.log(np.clip(1 - p, 1e-300, 1)))
    assert np.allclose(post, stats.beta(8, 4).pdf(g), atol=2e-3)
    ch = B.metropolis(lambda x: stats.norm.logpdf(x[0], 3, 2), [0.0], 2.5, 20_000, np.random.Generator(np.random.PCG64(1)))
    assert ch.draws[2000:, 0].mean() == pytest.approx(3, abs=0.15) and 0.2 < ch.acceptance < 0.8
    assert 1000 < B.ess(ch.draws[2000:, 0]) < 18_000
    bf = B.bayes_factor_binomial(60, 100)
    exact = integrate.quad(lambda p: stats.binom.pmf(60, 100, p), 0, 1)[0] / stats.binom.pmf(60, 100, 0.5)
    assert bf == pytest.approx(exact, rel=1e-6)
