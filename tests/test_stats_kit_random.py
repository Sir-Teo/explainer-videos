"""statkit.random against SciPy and against its own algebra."""

import numpy as np
from scipy import stats

from explainer.stats.kit.random import (M31, PCG32, AliasTable, box_muller, discrete_inverse, lcg, marsaglia_tsang,
                                        randu, rejection, simulate, streams)


def test_randu_lies_on_15_planes():
    x = randu(1, 3000)
    k = (9 * x[:-2] - 6 * x[1:-1] + x[2:]) / M31
    assert np.allclose(k, np.round(k)) and len(set(np.round(k).astype(int))) <= 15


def test_lcg_periods():
    assert len(set(lcg(5, 3, 64, 1, 64))) == 64  # Hull-Dobell: full period
    assert len(set(lcg(5, 0, 64, 1, 64))) == 16  # multiplicative: a quarter of the modulus


def test_pcg32_is_uniform_and_reproducible():
    a, b = PCG32(7).random(20000), PCG32(7).random(20000)
    assert np.array_equal(a, b)
    assert stats.kstest(a, "uniform").pvalue > 0.01
    assert not np.array_equal(PCG32(7, stream=1).random(10), PCG32(7, stream=2).random(10))


def test_samplers_match_their_laws():
    rng = np.random.default_rng(0)
    z1, z2 = box_muller(rng.random(20000), rng.random(20000))
    assert stats.kstest(z1, "norm").pvalue > 0.01 and abs(np.corrcoef(z1, z2)[0, 1]) < 0.03
    g, rate = marsaglia_tsang(2.5, 20000, rng)
    assert stats.kstest(g, stats.gamma(2.5).cdf).pvalue > 0.01 and rate > 0.95
    x, acc = rejection(lambda t: stats.beta.pdf(t, 2, 5), 2.4576, 20000, rng)
    assert stats.kstest(x, stats.beta(2, 5).cdf).pvalue > 0.01 and abs(acc - 1 / 2.4576) < 0.02
    p = [0.05, 0.3, 0.1, 0.25, 0.2, 0.1]
    d = AliasTable.build(p).draw(60000, rng)
    assert np.allclose(np.bincount(d, minlength=6) / 60000, p, atol=0.01)
    k = discrete_inverse(p, rng.random(60000))
    assert np.allclose(np.bincount(k, minlength=6) / 60000, p, atol=0.01)


def test_streams_and_simulate():
    s = streams(1, 3)
    assert len({float(g.random()) for g in s}) == 3

    def method(x):
        m, se = x.mean(), x.std(ddof=1) / np.sqrt(len(x))
        return m, m - 1.96 * se, m + 1.96 * se
    out = simulate(lambda rng: rng.normal(0, 1, 50), method, 0.0, 2000, seed=3)
    assert abs(out["coverage"] - 0.95) < 4 * out["coverage_mcse"] + 0.01
    assert abs(out["bias"]) < 4 * out["bias_mcse"]
