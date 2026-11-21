"""Agora's economic approach (Part 49): crime, police, the household, marriage, children, bargaining, schools,
health and addiction."""

import numpy as np

from explainer.economics.agora import family as fm
from explainer.economics.island import truths

T = truths(49)


def _gains(n=20000, seed=1):
    rng = np.random.default_rng(seed)
    return np.exp(0.8 * rng.standard_normal(n))


def test_risk_neutral_offenders_respond_to_the_product():
    g = _gains()
    assert abs(fm.offend_share(0.2, 3.0, g) - np.mean(g > 0.6)) < 1e-12
    r = fm.play_doubling(0.2, 3.0, g, {"n": (0.0, 1.0), "a": (0.5, 1.0), "d": (0.0, 0.75)})
    assert r["n"]["double_p"] == r["n"]["double_s"]
    assert r["a"]["double_s"] < r["a"]["double_p"]            # the risk-averse fear the long sentence
    assert r["d"]["double_p"] < r["d"]["double_s"]            # the present-minded fear being caught


def test_felt_punishment():
    assert fm.felt_punishment(3.0, 1.0) == 3.0
    assert abs(fm.felt_punishment(2.0, 0.5) - 1.5) < 1e-12


def test_beckers_planner_sets_the_largest_fine():
    r = fm.optimal_enforcement(_gains(5000), harm=2.0, cost_p=1.0, f_max=40.0, n_p=40, n_f=40)
    assert r["f_star"] == 40.0 and r["p_star"] < 0.3


def test_police_estimates():
    P = fm.police_blocks(**T["police"])
    assert P["naive"] > 0                                     # police go where crime is
    assert abs(P["fd_noisy"]) < abs(P["fd_true"])             # counting errors attenuate
    assert abs(P["experiment"] - P["elasticity"]) < 3 * P["experiment_se"]


def test_household_specializes_by_comparative_advantage():
    low = fm.household_time(1.0, 0.4, 0.6, 1.0)
    high = fm.household_time(1.0, 1.5, 0.6, 1.0)
    assert low["market2"] == 0.0 and low["market1"] == 1.0
    assert high["market2"] > 0.2


def test_choo_siow_adds_up_and_is_read_back():
    M = T["marriage"]
    phi = np.array(M["phi"])
    eq = fm.choo_siow(M["men"], M["women"], phi)
    mu = np.array(eq["mu"])
    assert np.allclose(mu.sum(1) + eq["single_men"], M["men"])
    assert np.allclose(mu.sum(0) + eq["single_women"], M["women"])
    assert np.allclose(fm.choo_siow_estimate(mu, eq["single_men"], eq["single_women"]), phi, atol=1e-8)
    assert fm.sorting_index(mu) > 1.0


def test_quantity_quality():
    r = fm.quantity_quality(3.0, 1.0, 0.15, 0.05, 0.3, 0.15)
    Y, pi = 4.0, 0.2
    assert abs(r["c"] + r["n"] * (pi + r["q"]) - Y) < 1e-12
    assert abs(r["q"] - 0.15 * pi / 0.15) < 1e-12
    assert fm.quantity_quality(3.0, 2.0)["n"] < fm.quantity_quality(3.0, 0.5)["n"]


def test_wald_recovers_an_effect():
    rng = np.random.default_rng(3)
    n = 200000
    z = rng.integers(0, 2, n)
    u = rng.normal(size=n)
    d = ((0.3 * z + 0.5 * u + rng.normal(size=n)) > 0.5).astype(float)
    y = -5.0 * d + 3.0 * u + rng.normal(size=n)
    w = fm.wald(z, d, y)
    assert abs(w["wald"] + 5.0) < 4 * w["se"]


def test_collective_household():
    uni = [fm.collective(1 - s, s, unitary=True)["child"] for s in (0.1, 0.5, 0.9)]
    col = [fm.collective(1 - s, s)["child"] for s in (0.1, 0.5, 0.9)]
    assert max(uni) - min(uni) < 1e-12
    assert col[0] < col[1] < col[2]


def test_maimonides():
    assert list(fm.maimonides([40, 41, 80, 81, 120, 121])) == [40, 20.5, 40, 27, 40, 30.25]
    r = fm.maimonides_study(**T["maimonides"])
    assert abs(r["iv"] - r["effect"]) < 3 * r["iv_se"]


def test_teacher_value_added():
    a = fm.teacher_va(**T["teachers"])
    b = fm.teacher_va(**T["teachers"], sorting=1.0)
    assert a["sd_shrunk"] < a["sd_true"] < a["sd_raw"]
    assert abs(a["forecast_coef"] - 1) < 3 * a["forecast_se"]
    assert b["forecast_coef"] < 0.6


def test_grossman_and_addiction():
    g = fm.grossman(np.arange(20, 111), **T["grossman"])
    assert np.all(np.diff(g["health"]) < 0) and 70 < g["death_age"] < 100
    A = T["addiction"]
    r = fm.addiction_path(**A, rational=True)["consumption"]
    m = fm.addiction_path(**A, rational=False)["consumption"]
    i0, i1 = A["announce_at"], A["rise_at"]
    assert r[i1 - 1] < r[i0 - 1]                              # cuts back on the news
    assert m[i1 - 1] > m[i0 - 1]                              # the myopic user does not
