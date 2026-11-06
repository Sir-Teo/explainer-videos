"""Tests for statkit.testing, the Neyman-structure lab of Part 46."""

import math

import numpy as np
from scipy import stats

from explainer.stats.kit import testing as T


def rng(seed=0):
    return np.random.default_rng(seed)


def test_behrens_fisher():
    # equal ns, phi = 45 degrees: c between the t_{n-1} and normal quantiles' range
    c = T.bf_critical(math.pi / 4, 10, 10)
    assert stats.norm.ppf(0.975) < c < stats.t.ppf(0.975, 9)
    assert abs(T.bf_critical(0.0, 10, 6) - stats.t.ppf(0.975, 5)) < 1e-6  # phi = 0: only the second sample's t
    d = T.welch_df(1.0, 1.0, 11, 11)
    assert abs(d - 20) < 1e-12
    r = T.two_sample_sizes(5, 3.0, 25, 1.0, 20000, rng(1))
    assert r["pooled"].mean() > 0.15  # badly broken: the small sample has the large variance
    assert abs(r["welch"].mean() - 0.05) < 0.01
    assert r["bf"].mean() < 0.055


def test_np_and_umpu():
    n, p0 = 20, 0.3
    u = T.ump_binomial(n, p0)
    assert abs(T.power(u["phi"], n, p0)[0] - 0.05) < 1e-12
    t = T.umpu_binomial(n, p0)
    phi = t["phi"]
    assert abs(T.power(phi, n, p0)[0] - 0.05) < 1e-10
    h = 1e-6
    deriv = (T.power(phi, n, p0 + h)[0] - T.power(phi, n, p0 - h)[0]) / (2 * h)
    assert abs(deriv) < 1e-6  # unbiased: the power has a minimum at p0
    ps = np.linspace(0.01, 0.99, 99)
    assert np.all(T.power(phi, n, ps) >= 0.05 - 1e-9)
    et = T.equal_tailed_binomial(n, p0)
    assert abs(T.power(et, n, p0)[0] - 0.05) < 1e-10
    assert np.min(T.power(et, n, np.linspace(0.2, 0.4, 2001))) < 0.05 - 5e-5  # biased: dips below alpha
    # the generalized NP lemma reproduces the UMPU test for an alternative on either side
    x = np.arange(n + 1)
    f0 = stats.binom.pmf(x, n, p0)
    for p1 in (0.15, 0.5):
        g = T.generalized_np(f0, stats.binom.pmf(x, n, p1), [f0, x * f0], [0.05, 0.05 * n * p0])
        assert abs(T.power(g, n, p1)[0] - T.power(phi, n, p1)[0]) < 1e-8


def test_neyman_structure():
    m, n = 8, 10
    r = T.conditional_test(m, n, randomized=True)
    sizes = T.unconditional_size(r["phi"], m, n, np.linspace(0.05, 0.95, 10))
    assert np.allclose(sizes, 0.05, atol=1e-10)  # similar: size alpha at every nuisance value
    nr = T.conditional_test(m, n, randomized=False)
    s2 = T.unconditional_size(nr["phi"], m, n, np.linspace(0.05, 0.95, 10))
    assert np.all(s2 < 0.05)


def test_chibar_and_intervals():
    c = T.chibar_critical(0.05)
    z = rng(2).normal(0, 1, 400000)
    assert abs(np.mean(np.maximum(z, 0) ** 2 > c) - 0.05) < 0.002
    n = 20
    iv = [T.clopper_pearson(x, n) for x in range(n + 1)]
    cov = T.coverage_binomial(iv, n, np.linspace(0.01, 0.99, 197))
    assert np.all(cov >= 0.95 - 1e-9)
    w = [T.wald_binomial(x, n) for x in range(n + 1)]
    assert np.min(T.coverage_binomial(w, n, np.linspace(0.01, 0.99, 197))) < 0.5


def test_fieller():
    f = T.fieller(2.0, 4.0, 0.1, 0.1)
    assert f["kind"] == "bounded" and f["lo"] < 0.5 < f["hi"]
    assert T.fieller(0.2, 0.1, 0.1, 0.1)["kind"] == "all"
    assert T.fieller(2.0, 0.5, 0.01, 0.1)["kind"] == "exclusive"


def test_feldman_cousins():
    # Feldman & Cousins (1998), Table II (b = 0): n = 0..3 give [0, 2.44], [0.11, 4.36], [0.53, 5.91], [1.10, 7.42]
    f0 = T.fc_intervals(0.0, 0.9, mu_grid=np.linspace(0, 15, 3001), nmax=40)
    for k, (a, b) in enumerate([(0.0, 2.44), (0.11, 4.36), (0.53, 5.91), (1.10, 7.42)]):
        assert abs(f0["lo"][k] - a) < 0.015 and abs(f0["hi"][k] - b) < 0.015
    fc = T.fc_intervals(3.0, 0.9, mu_grid=np.linspace(0, 15, 1501), nmax=40)
    assert fc["lo"][0] == 0 and fc["hi"][0] < f0["hi"][0]
    cov = T.poisson_coverage(fc["lo"], fc["hi"], 3.0, np.linspace(0, 10, 101))
    assert np.all(cov >= 0.9 - 1e-6)
    ff = T.flipflop_intervals(3.0, 0.9, nmax=40)
    cff = T.poisson_coverage(ff["lo"], ff["hi"], 3.0, np.linspace(0, 10, 201))
    assert np.min(cff) < 0.88  # undercovers somewhere


def test_closed_testing():
    g = rng(3)
    for _ in range(50):
        p = g.random(4) ** 2
        assert np.array_equal(T.closed_test(p, 0.05, "bonferroni"), T.holm(p, 0.05))
    p = np.array([0.02, 0.03, 0.04])
    assert T.closed_test(p, 0.05, "simes").all() and not T.holm(p, 0.05).any()
    assert abs(T.scheffe_constant(1) - stats.norm.ppf(0.975)) < 1e-9


def test_conditional_and_evidence():
    r = T.t2_conditional(0.3, 1 + math.sqrt(2), 200000, rng(4))
    assert abs(r["overall"] - 0.5) < 0.005 and r["conditional"] > 0.6
    b = T.berger_sellke(0.05)
    assert abs(b["all"] - 0.128) < 0.002
    assert b["all"] < b["symmetric"] < b["normal"]
    assert abs(b["B_calib"] - (-math.e * 0.05 * math.log(0.05))) < 1e-12


def test_lilliefors():
    r = T.ks_estimated(20, 20000, rng(5))
    assert r["size"] < 0.01  # far too conservative with the naive critical value
    assert r["crit_lilliefors"] < r["crit_naive"]
