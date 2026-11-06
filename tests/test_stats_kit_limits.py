"""statkit.limits: the weak-convergence lab (Part 43)."""

from __future__ import annotations

import math

import numpy as np
import pytest
from scipy import stats

from explainer.stats.kit import limits as LI


def test_kolmogorov_lattice_matches_dense_grid_and_berry_esseen():
    for n in (5, 20, 80):
        b = LI.bernoulli_sum_atoms(n, 0.5)
        k = LI.kolmogorov_lattice(b["atoms"], b["probs"], stats.norm.cdf)
        F = LI.lattice_cdf(b["atoms"], b["probs"])
        x = np.linspace(-6, 6, 200_001)
        dense = LI.kolmogorov(F, stats.norm.cdf, x)
        assert k["d"] == pytest.approx(dense, abs=2e-4)
        assert k["d"] <= LI.berry_esseen(LI.third_abs_moment("bernoulli"), n)
        # the symmetric binomial's distance is about 1/sqrt(2 pi n) (half its largest atom)
        assert k["d"] == pytest.approx(1 / math.sqrt(2 * math.pi * n), rel=0.2)


def test_distances_order_and_wasserstein_matches_scipy():
    g = np.random.default_rng(0)
    a, b = g.standard_normal(4000), g.standard_normal(4000) * 1.3 + 0.2
    Fa = lambda x: np.searchsorted(np.sort(a), x, side="right") / len(a)  # noqa: E731
    Fb = lambda x: np.searchsorted(np.sort(b), x, side="right") / len(b)  # noqa: E731
    x = np.linspace(-8, 8, 40_001)
    w = LI.wasserstein1(Fa, Fb, x)
    assert w == pytest.approx(stats.wasserstein_distance(a, b), rel=1e-3)
    L, K = LI.levy(Fa, Fb, x), LI.kolmogorov(Fa, Fb, x)
    assert L <= K + 1e-9


def test_prokhorov_bracket_exponential_sums_shrinks():
    x = np.linspace(-8, 12, 20_001)
    prev = None
    for n in (2, 8, 32):
        r = LI.prokhorov_bracket(LI.exponential_sum_cdf(n), stats.norm.cdf, LI.exponential_sum_ppf(n), stats.norm.ppf, x)
        assert r["levy"] <= r["ky_fan"] + 1e-6
        if prev is not None:
            assert r["ky_fan"] < prev
        prev = r["ky_fan"]


def test_ky_fan_simple():
    assert LI.ky_fan(np.zeros(100)) == 0.0
    d = np.r_[np.full(10, 5.0), np.zeros(90)]  # 10% of mass moved by 5: Ky Fan = 0.1
    assert LI.ky_fan(d) == pytest.approx(0.1)


def test_stein_bounds_and_identity():
    g = np.random.default_rng(1)
    z = g.standard_normal(400_000)
    assert abs(LI.stein_residual(np.sin, np.cos, z)) < 0.01
    e = g.exponential(1.0, 400_000) - 1
    assert abs(LI.stein_residual(np.sin, np.cos, e)) > 0.05
    # the Stein solution satisfies f' - w f = h - Eh for h = 1(w <= 0)
    h = lambda w: (np.asarray(w) <= 0.0).astype(float)  # noqa: E731
    w = np.linspace(-3, 3, 601)
    f = LI.stein_solution(h, w)
    fp = np.gradient(f, w)
    keep = np.abs(w) > 0.05
    assert np.max(np.abs((fp - w * f - (h(w) - 0.5))[keep])) < 2e-2
    # the measured Wasserstein distance for exponential sums sits under rho / sqrt(n)
    rho = LI.third_abs_moment("exponential")
    x = np.linspace(-8, 14, 30_001)
    for n in (4, 16, 64):
        assert LI.wasserstein1(LI.exponential_sum_cdf(n), stats.norm.cdf, x) <= LI.stein_wasserstein(rho, n)


def test_third_moments():
    g = np.random.default_rng(2)
    e = g.exponential(1.0, 2_000_000)
    assert LI.third_abs_moment("exponential") == pytest.approx(np.mean(np.abs(e - 1) ** 3), rel=0.01)
    u = g.random(2_000_000)
    assert LI.third_abs_moment("uniform") == pytest.approx(np.mean(np.abs(u - 0.5) ** 3) / (1 / 12) ** 1.5, rel=0.01)
    assert LI.third_abs_moment("bernoulli") == pytest.approx(1.0)


def test_cf_inversion_and_levy_tail_bound():
    x = np.linspace(-3, 3, 7)
    f = LI.cf_invert_density(lambda t: np.exp(-t ** 2 / 2), x)
    assert np.max(np.abs(f - stats.norm.pdf(x))) < 1e-6
    f = LI.cf_invert_density(lambda t: np.exp(-np.abs(t)), x, T=400.0, m=400_001)
    assert np.max(np.abs(f - stats.cauchy.pdf(x))) < 1e-3
    for u in (0.5, 1.0, 2.0):
        assert LI.levy_tail_bound(lambda t: np.exp(-np.abs(t)), u) >= stats.cauchy.sf(2 / u) * 2 - 1e-9


def test_stable_sampler():
    g = np.random.default_rng(3)
    z = LI.stable_sample(2.0, 0.0, 200_000, g)
    assert np.std(z) == pytest.approx(math.sqrt(2), rel=0.02)
    c = LI.stable_sample(1.0, 0.0, 200_000, g)
    assert stats.kstest(c, "cauchy").statistic < 0.01
    s = LI.stable_sample(1.5, 0.0, 200_000, g)
    t = np.array([0.5, 1.0, 2.0])
    assert np.max(np.abs(np.real(LI.cf_empirical(s, t)) - LI.stable_cf(t, 1.5))) < 0.01


def test_cramer_rate_bernoulli_and_normal():
    p = 0.3
    lm = lambda t: math.log(1 - p + p * math.exp(t))  # noqa: E731
    for a in (0.4, 0.5, 0.7):
        assert LI.cramer_rate(lm, a) == pytest.approx(LI.bernoulli_rate(a, p), abs=1e-7)
    assert LI.cramer_rate(lambda t: t ** 2 / 2, 1.5) == pytest.approx(1.125, abs=1e-8)
    # Chernoff: the exact tail never exceeds exp(-n I(a)), and -log(P)/n approaches I(a)
    for n in (50, 400, 3200):
        P = LI.binomial_upper_tail(n, p, 0.4)
        assert P <= math.exp(-n * LI.bernoulli_rate(0.4, p))
    # the gap is the polynomial prefactor: -log P / n - I(a) is about log(n) / (2n)
    for n in (400, 3200, 25600):
        gap = -math.log(LI.binomial_upper_tail(n, p, 0.4)) / n - LI.bernoulli_rate(0.4, p)
        assert 0 < gap < math.log(n) / n


def test_extremes():
    x = np.linspace(-2, 6, 401)
    assert LI.gev_cdf(x, 0.0) == pytest.approx(stats.gumbel_r.cdf(x))
    assert LI.gev_cdf(x, 0.3) == pytest.approx(stats.genextreme.cdf(x, -0.3), abs=1e-12)
    d = [LI.kolmogorov(LI.max_cdf("exponential", n, x), LI.max_limit("exponential", x), x) for n in (10, 100, 1000)]
    assert d[0] > d[1] > d[2]
    dn = [LI.kolmogorov(LI.max_cdf("normal", n, x), LI.max_limit("normal", x), x) for n in (100, 10_000)]
    assert dn[1] < dn[0] and dn[1] > d[2]  # the normal's maxima converge far more slowly
    xp = np.linspace(0.05, 10, 400)
    assert LI.kolmogorov(LI.max_cdf("pareto", 1000, xp, 2.0), LI.max_limit("pareto", xp, 2.0), xp) < 1e-3


def test_series_digits_cantor():
    g = np.random.default_rng(4)
    p = LI.random_series(1.0, 20_000, 200, g)
    late = np.abs(p[:, -1] - p[:, 9_999])
    assert np.mean(late) < 0.01  # the random harmonic series has settled
    q = LI.random_series(0.4, 20_000, 200, g)
    assert np.mean(np.abs(q[:, -1] - q[:, 9_999])) > 1.0  # p < 1/2: it wanders
    u = g.random(100_000)
    d = LI.binary_digits(u, 8)
    assert d.mean(axis=0) == pytest.approx(np.full(8, 0.5), abs=0.01)
    assert abs(np.corrcoef(d[:, 0], d[:, 1])[0, 1]) < 0.02
    assert LI.cantor_function(np.array([0.0, 1 / 3, 0.5, 2 / 3, 1.0, 0.25])) == pytest.approx([0.0, 0.5, 0.5, 0.5, 1.0, 1 / 3], abs=1e-9)


def test_poisson_limit_and_hill():
    for n, p in ((10, 0.05), (100, 0.01), (1000, 0.002)):
        tv = LI.tv_binomial_poisson(n, p)
        assert 0 < tv <= LI.le_cam_bound(np.full(n, p))
    g = np.random.default_rng(5)
    x = (1 - g.random(200_000)) ** (-1 / 2.5)  # Pareto, alpha = 2.5
    assert LI.hill(x, 2000) == pytest.approx(2.5, rel=0.06)
