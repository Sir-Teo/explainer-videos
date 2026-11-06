"""Tests for statkit.empirical, the empirical-process toolkit of Part 48."""

import math

import numpy as np
from scipy import stats

from explainer.stats.kit import empirical as E


def rng(seed=0):
    return np.random.default_rng(seed)


def test_kolmogorov_against_scipy():
    t = np.array([0.4, 0.8, 1.0, 1.36, 2.0])
    assert np.allclose(E.kolmogorov_cdf(t), stats.kstwobign.cdf(t), atol=1e-10)
    assert abs(E.kolmogorov_quantile(0.95) - stats.kstwobign.ppf(0.95)) < 1e-8
    u = np.linspace(0.05, 3, 400)
    assert abs(np.trapezoid(E.kolmogorov_density(u), u) - (E.kolmogorov_cdf(3)[0] - E.kolmogorov_cdf(0.05)[0])) < 1e-4
    x = rng(1).random(50)
    assert abs(E.ks_stat(x, lambda v: v) - stats.kstest(x, "uniform").statistic) < 1e-12
    assert abs(E.ks_stats_uniform(x[None, :])[0] - stats.kstest(x, "uniform").statistic) < 1e-12


def test_walk_max_exact():
    n = 12
    S = np.cumsum(rng(2).choice([-1, 1], (400000, n)), axis=1)
    sim = np.mean(np.max(np.abs(np.concatenate([np.zeros((400000, 1)), S], axis=1)), axis=1))
    assert abs(E.walk_max_abs_expectation(n) - sim) < 0.01
    # small case by enumeration
    n = 6
    tot = 0
    for k in range(2 ** n):
        s = np.cumsum([1 if (k >> i) & 1 else -1 for i in range(n)])
        tot += max(0, np.max(np.abs(s)))
    assert abs(E.walk_max_abs_expectation(n) - tot / 2 ** n) < 1e-12
    # the Rademacher average of half-lines decays like 1/sqrt(n)
    r = [E.rademacher_halflines(n) * math.sqrt(n) for n in (25, 100, 400)]
    assert abs(r[2] - math.sqrt(math.pi / 2)) < 0.1  # E sup |W| on [0, 1]


def test_massart_bounds_monte_carlo():
    v = rng(3).choice([0.0, 1.0], (30, 40))
    assert E.rademacher_finite(v, rng(4)) <= E.massart_finite(v)


def test_growth_functions():
    r = rng(5)
    for n in (3, 5, 8):
        pts = r.standard_normal((n, 2))
        assert E.dichotomies_halfplanes(pts) == E.growth_halfplanes(n)
        assert E.dichotomies_halfplanes(pts) <= E.sauer_shelah(n, 3)
    assert E.dichotomies_intervals(r.random(7)) == 29 == E.sauer_shelah(7, 2)
    assert E.dichotomies_halflines(r.random(7)) == 8 == E.sauer_shelah(7, 1)
    # rectangles shatter some 4 points (a diamond) but never 5
    diamond = np.array([[0, 1], [1, 0], [0, -1], [-1, 0]], float)
    assert E.dichotomies_rectangles(diamond) == 16
    for _ in range(5):
        assert E.dichotomies_rectangles(r.standard_normal((5, 2))) < 32


def test_covering_and_bracketing():
    grid = np.linspace(0, 1, 401)
    halflines = (grid[None, :] <= np.linspace(0, 1, 401)[:, None]).astype(float)
    # under L2(uniform), ||1{x<=s} - 1{x<=t}|| = sqrt|s - t|: a net needs about 1/(4 eps^2)... centres every 4 eps^2
    for eps in (0.1, 0.2):
        n = E.greedy_cover(halflines, eps)
        assert 0.5 / (4 * eps ** 2) < n < 2 / eps ** 2
        assert E.bracketing_halflines(eps) == math.ceil(1 / eps ** 2)
    f = E.lipschitz_paths(50, 3000, rng(6))
    assert np.all(np.abs(np.diff(f, axis=1)) <= 1 / 49 + 1e-12)
    assert E.greedy_cover(f, 0.05, "sup") > E.greedy_cover(f, 0.2, "sup")


def test_chaining_and_concentration():
    c = E.chaining_bound_bm()
    assert c["exact"] < c["bound"] < 10 * c["exact"]
    assert c["union"][-1] > c["union"][0]
    assert abs(E.bm_sup_on_grid(8, rng(7), reps=3000, fine=10) - math.sqrt(2 / math.pi)) < 0.08
    # Bousquet and DKW really are upper bounds on the KS tail
    n = 100
    D = E.ks_stats_uniform(rng(8).random((20000, n))) * n
    ez = D.mean()
    for t in (3.0, 6.0, 9.0):
        assert np.mean(D >= ez + t) <= E.bousquet_tail(t, n, 0.25, ez)[0] + 0.005
    s = D / math.sqrt(n)
    for t in (0.8, 1.2, 1.6):
        assert np.mean(s > t) <= E.dkw_tail(t, n)[0] + 0.005


def test_durbin_and_nuisance():
    z = rng(9).standard_normal((30000, 60))
    m, s = z.mean(axis=1), z.std(axis=1, ddof=1)
    for x in (0.0, 1.0):
        sim = np.var(math.sqrt(60) * (np.mean(z <= x, axis=1) - stats.norm.cdf((x - m) / s)))
        assert abs(sim - E.durbin_variance_normal(x)) < 0.006
    d = E.mad_exponential()
    assert d["median"]["correct"] == d["median"]["naive"]
    assert d["mean"]["correct"] > d["mean"]["naive"]
    x = rng(10).exponential(size=(20000, 200))
    est = np.mean(np.abs(x - x.mean(axis=1, keepdims=True)), axis=1)
    assert abs(200 * np.var(est) - d["mean"]["correct"]) < 0.05


def test_chernoff_and_bands():
    c = E.chernoff_draws(rng(11), reps=1500, m=1500)
    assert abs(np.std(c) - E.CHERNOFF_SD) < 0.04
    assert abs(np.mean(c)) < 0.05
    q = E.ks_band_quantiles(30)
    assert q["exact"] < q["kolmogorov"] <= q["dkw"] + 1e-9
    x = rng(12).standard_normal(30)
    assert abs(E.bootstrap_ks_quantile(x, rng(13)) - q["exact"]) < 0.05
    assert abs(E.multiplier_ks_quantile(x, rng(14)) - q["kolmogorov"]) < 0.05
    p = E.parametric_bootstrap_ks(x, rng(15), B=499)
    assert 0 < p["p"] <= 1 and p["crit95"] < q["exact"]
