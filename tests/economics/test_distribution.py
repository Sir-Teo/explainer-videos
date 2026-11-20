"""Agora's distribution (Part 40): measures, Pareto tails, random growth and its Kolmogorov equation, generations."""

import numpy as np
import pytest

from explainer.economics.agora import distribution as D


def test_gini_and_lorenz_known_values():
    assert D.gini([1, 1, 1, 1]) == pytest.approx(0.0)
    # one person has everything among n: Gini = 1 - 1/n with this (grouped) definition
    assert D.gini([0, 0, 0, 1]) == pytest.approx(0.75)
    x = [1, 2, 3, 4, 10]
    p, L = D.lorenz(x)
    assert p[0] == 0 and L[0] == 0 and p[-1] == pytest.approx(1) and L[-1] == pytest.approx(1)
    # mean absolute difference over twice the mean, with the n^2 convention
    xs = np.array(x, float)
    g = np.abs(xs[:, None] - xs[None, :]).sum() / (2 * len(xs) ** 2 * xs.mean())
    assert D.gini(x) == pytest.approx(g)
    # weights act like repetitions
    assert D.gini([1, 3], w=[2, 1]) == pytest.approx(D.gini([1, 1, 3]))


def test_atkinson_theil_and_top_shares():
    x = np.array([1.0, 2.0, 3.0, 4.0, 10.0])
    assert D.atkinson(x, 0.0) == pytest.approx(0.0)
    assert D.atkinson(x, 1.0) == pytest.approx(1 - np.exp(np.log(x).mean()) / x.mean())
    a = [D.atkinson(x, e) for e in (0.5, 1.0, 2.0, 4.0)]
    assert all(b > c for b, c in zip(a[1:], a[:-1]))
    assert D.theil(np.ones(5)) == pytest.approx(0.0) and D.mld(np.ones(5)) == pytest.approx(0.0)
    assert D.top_share(x, 0.2) == pytest.approx(10 / 20)
    assert D.top_share(np.ones(100), 0.01) == pytest.approx(0.01)


def test_measures_have_standard_errors():
    rng = np.random.default_rng(0)
    m = D.measures(np.exp(rng.normal(size=1000)), B=100, seed=1)
    assert 0 < m["gini"]["se"] < 0.05 and m["top1"]["se"] > 0
    # a lognormal with sigma 1 has Gini 2 Phi(1/sqrt 2) - 1 = 0.52
    assert m["gini"]["value"] == pytest.approx(0.52, abs=0.04)


def test_pareto_alpha_round_trip_and_hill():
    alpha = 1.6
    share = lambda p: p ** (1 - 1 / alpha)  # noqa: E731
    assert D.pareto_alpha(share(0.01), share(0.001), 0.01, 0.001) == pytest.approx(alpha)
    assert D.inverted_b(2.0) == pytest.approx(2.0)
    rng = np.random.default_rng(3)
    x = (1 - rng.random(200000)) ** (-1 / alpha)
    assert D.hill(x, 2000) == pytest.approx(alpha, rel=0.06)


def test_random_growth_tail_matches_theory():
    nu, s, d = 0.0, 0.144, 0.025
    z = D.zeta(nu, s, d)
    assert (s * s / 2) * z * z + nu * z - d == pytest.approx(0.0, abs=1e-12)
    K = D.KFE(nu, s, d, y_lo=-1.0)
    p = K.stationary()
    m = (K.y > 3) & (K.y < 9)
    slope = np.polyfit(K.y[m], np.log(p[m]), 1)[0]
    assert -slope == pytest.approx(z, rel=0.01)
    x = D.simulate_growth(20000, 300, nu, s, d, seed=4)
    assert D.hill(x, 200) == pytest.approx(z, rel=0.15)
    assert D.top_share(x, 0.01) == pytest.approx(K.top_share(p, 0.01), abs=0.04)


def test_transitions_pure_slow_types_fast():
    d = 0.025
    K0 = D.KFE(0.0, 0.0894, d, y_lo=-1.0)
    K1 = D.KFE(0.0, 0.144, d, y_lo=-1.0)
    pure = K1.path(K0.stationary(), 40, dt=0.5)
    Ka = D.KFE(-0.03, 0.10, d, nu_h=0.085, psi=0.2, q_h=0.15, y_lo=-1.0)
    Kb = D.KFE(-0.03, 0.10, d, nu_h=0.16, psi=0.2, q_h=0.15, y_lo=-1.0)
    types = Kb.path(Ka.stationary(), 40, dt=0.5)
    hp = D.half_life(pure["t"], np.log(pure[0.01]), np.log(K1.top_share(K1.stationary(), 0.01)))
    ht = D.half_life(types["t"], np.log(types[0.01]), np.log(Kb.top_share(Kb.stationary(), 0.01)))
    assert np.isnan(hp) or hp > 40   # pure random growth has not closed half the gap in forty years
    assert ht < 25
    assert np.all(np.diff(pure[0.01]) > 0)


def test_wealth_tail_fattens_with_r_minus_g():
    z = [D.wealth_zeta(r, 0.03, 0.15, 0.02) for r in (0.0, 0.01, 0.02, 0.03)]
    assert all(b < a for a, b in zip(z, z[1:]))


def test_kuznets_inverted_u():
    k = D.kuznets(np.linspace(0, 1, 21), n=20000, seed=1)
    g = np.array(k["gini"])
    i = int(np.argmax(g))
    assert 0 < i < len(g) - 1 and g[i] > g[0] and g[i] > g[-1]
    v = np.array(k["var_log"])
    j = int(np.argmax(v))
    assert 0 < j < len(v) - 1   # the variance of logs has its own inverted U (peaking later, as sd_m > sd_a)


def test_attenuation_and_ranks():
    g = D.generations(20000, 0.45, 0.6, 0.55, 15, seed=2)
    for T in (1, 5, 15):
        b = D.ige(g["child"], g["parent_years"][:, :T].mean(axis=1))[0]
        assert b == pytest.approx(0.45 * D.attenuation(T, 0.6, 0.55), abs=0.02)
    assert D.ige(g["child"], g["parent"])[0] == pytest.approx(0.45, abs=0.02)
    assert D.rank_slope(g["child"], g["parent_years"][:, 0]) < D.rank_slope(g["child"], g["parent"])


def test_gatsby_mechanism_monotone():
    r = D.gatsby((0.3, 0.6, 0.9), n=20000, seed=1)
    assert r["gini"][0] < r["gini"][1] < r["gini"][2]
    assert r["ige"][0] < r["ige"][1] < r["ige"][2]
    assert r["ige"][2] == pytest.approx(r["ige_theory"][2], abs=0.03)


def test_between_gini_and_incidence():
    assert D.between_gini([1, 1], [5, 7]) == pytest.approx(0.0)
    assert D.between_gini([1, 3], [1, 1]) == pytest.approx(D.gini([1, 3]))
    rng = np.random.default_rng(5)
    x = np.exp(rng.normal(size=5000))
    r = D.incidence(x, 0.2)
    # the transfers are paid for by the tax: gains sum to zero across equal-sized deciles
    assert sum(r["gain"]) == pytest.approx(0.0, abs=1e-6 * x.mean() * 10)
    assert r["gini_post"] == pytest.approx(0.8 * r["gini_pre"], rel=1e-6)
    assert r["gain"][0] > 0 > r["gain"][-1]
