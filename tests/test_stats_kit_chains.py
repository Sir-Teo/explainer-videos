"""statkit.chains: the coupling and mixing lab (Part 44)."""

from __future__ import annotations

import math

import numpy as np
import pytest
from scipy import stats

from explainer.stats.kit import chains as CH


def test_two_state_fit_and_block_variance():
    g = np.random.default_rng(0)
    P = np.array([[0.4, 0.6], [0.8, 0.2]])
    x = [0]
    for _ in range(200_000):
        x.append(int(g.random() < P[x[-1], 1]))
    f = CH.two_state_fit(x)
    assert f["P"] == pytest.approx(P, abs=0.01)
    pi1 = 0.6 / (0.6 + 0.8)
    assert f["pi1"] == pytest.approx(pi1, abs=0.01)
    x = np.array(x[:200_000])
    blocks = x.reshape(-1, 100).sum(1)
    assert blocks.var() == pytest.approx(CH.block_count_variance(pi1, 0.2 - 0.6, 100), rel=0.08)


def test_mixing_cycle_and_hypercube():
    n = 16
    P = CH.lazy_cycle(n)
    pi = CH.stationary(P)
    assert pi == pytest.approx(np.full(n, 1 / n))
    d = CH.distance_curve(P, pi, [1, 10, 50, 200], starts=[0])
    assert np.all(np.diff(d) <= 1e-12)
    t = CH.mixing_time(P, pi, 0.25, starts=[0])
    assert 0.05 * n * n < t < 1.0 * n * n  # order n^2
    gap = CH.spectral_gap(P)
    assert gap == pytest.approx(0.5 * (1 - math.cos(2 * math.pi / n)), rel=1e-9)
    for dd in (8, 32):
        H = CH.lazy_hypercube_weight(dd)
        pih = stats.binom.pmf(np.arange(dd + 1), dd, 0.5)
        assert CH.stationary(H) == pytest.approx(pih, abs=1e-10)
    t8 = CH.mixing_time(CH.lazy_hypercube_weight(8), stats.binom.pmf(np.arange(9), 8, 0.5), starts=[0])
    t32 = CH.mixing_time(CH.lazy_hypercube_weight(32), stats.binom.pmf(np.arange(33), 32, 0.5), starts=[0])
    assert t32 / t8 < 16  # d log d, not d^2


def test_riffle_bayer_diaconis():
    vals = [CH.riffle_tv(52, k) for k in range(1, 11)]
    known = [1.000, 1.000, 1.000, 1.000, 0.924, 0.614, 0.334, 0.167, 0.085, 0.043]
    assert vals == pytest.approx(known, abs=1.5e-3)
    assert CH.riffle_tv(3, 1) == pytest.approx(0.5 * sum(abs(p - 1 / 6) for p in [4 / 8, 1 / 8, 1 / 8, 1 / 8, 1 / 8, 0]))


def test_coupling_and_polya():
    g = np.random.default_rng(1)
    t = CH.coupling_time_cycle(20, 2000, g)
    assert t.mean() == pytest.approx(100, rel=0.08)  # (n/2)^2
    assert CH.polya_return(1, 4000, 400, g) > 0.95
    r3 = CH.polya_return(3, 4000, 600, g)
    assert 0.25 < r3 < 0.40  # Polya's constant 0.3405


def test_ruin_and_betting():
    r = CH.ruin(0.5, 3, 10)
    assert r["win"] == pytest.approx(0.3) and r["duration"] == pytest.approx(21)
    g = np.random.default_rng(2)
    wins, durs = 0, []
    for _ in range(20_000):
        s, n = 3, 0
        while 0 < s < 10:
            s += 1 if g.random() < 0.45 else -1
            n += 1
        wins += s == 10
        durs.append(n)
    rr = CH.ruin(0.45, 3, 10)
    assert wins / 20_000 == pytest.approx(rr["win"], abs=0.01)
    assert np.mean(durs) == pytest.approx(rr["duration"], rel=0.03)
    x = (g.random((5000, 500)) < 0.5).astype(int)
    L = CH.betting_paths(x, 0.5, 0.6)
    assert L[:, 19].mean() == pytest.approx(1.0, rel=0.1)  # a mean-one martingale (heavy-tailed for long paths)
    assert np.mean(L.max(axis=1) >= 10) <= 0.1 + 0.01  # Ville


def test_brownian_and_dickey_fuller():
    g = np.random.default_rng(3)
    t = np.linspace(0, 1, 2 ** 12 + 1)
    paths = CH.levy_ciesielski(12, t, g)
    B = paths[-1]
    assert B[0] == 0.0
    qv = CH.quadratic_variation(B)
    assert qv["qv"] == pytest.approx(1.0, abs=0.12)
    assert qv["tv"] > 20
    # var B(1/2) = 1/2 over many draws
    vals = [CH.levy_ciesielski(6, np.array([0.5, 1.0]), g)[-1] for _ in range(3000)]
    v = np.array(vals)
    assert v[:, 0].var() == pytest.approx(0.5, rel=0.08) and v[:, 1].var() == pytest.approx(1.0, rel=0.08)
    df = CH.dickey_fuller(250, 4000, g)
    assert np.quantile(df["t"], 0.05) == pytest.approx(-1.95, abs=0.08)
    assert np.quantile(df["n_rho"], 0.05) == pytest.approx(-8.0, abs=0.6)


def test_mcmc_se_and_ar1():
    g = np.random.default_rng(4)
    x = CH.rwm_normal(100_000, 0.5, g)
    se_bm = CH.batch_means_se(x, 50)
    se_iid = x.std() / math.sqrt(len(x))
    assert se_bm > 3 * se_iid
    cov = 0
    for _ in range(400):
        e = g.standard_normal(301)
        y = np.zeros(301)
        for i in range(1, 301):
            y[i] = 0.5 * y[i - 1] + e[i]
        f = CH.ar1_ols(y)
        cov += abs(f["phi"] - 0.5) <= 1.645 * f["se"]
    assert cov / 400 == pytest.approx(0.9, abs=0.05)
    assert CH.azuma(30, np.ones(100)) == pytest.approx(2 * math.exp(-4.5))
    p = CH.polya_urn(400, 300, g)
    assert stats.kstest(p[:, -1], "uniform").pvalue > 0.01
