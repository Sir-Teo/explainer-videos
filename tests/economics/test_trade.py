"""Agora's trade, part I (Part 35): Ricardo, the continuum, Heckscher-Ohlin and its theorems, specific factors,
tariffs, protection for sale, the tariff war, and the tests and measures."""

import numpy as np
import pytest

from explainer.economics.agora import trade


def test_ricardo_both_gain_and_price_between_costs():
    r = trade.ricardo_trade((3, 6), (1, 4), 1200, 600)
    assert r["p"] == pytest.approx(3.0) and r["H"]["gain"] > 0 and r["F"]["gain"] > 0
    assert r["H"]["q1"] == 0 and r["F"]["q2"] == 0                      # complete specialization
    # a large country trading at its own autarky price gains nothing
    big = trade.ricardo_trade((1, 2), (3, 4), 1200, 1200)
    assert big["p"] == pytest.approx(2.0) and big["H"]["gain"] == pytest.approx(0, abs=1e-12)
    # market clearing: spending on good 2 equals its value
    for R in (r, big):
        Q1 = R["H"]["q1"] + R["F"]["q1"]
        Q2 = R["H"]["q2"] + R["F"]["q2"]
        assert R["p"] * Q2 == pytest.approx(Q1)


def test_ricardo_wage_band():
    r = trade.ricardo_trade((100, 120), (90, 80), 1.25, 1.0)
    assert r["p"] == pytest.approx(1.0) and 10 / 9 <= r["wage_ratio"] <= 1.5


def test_dfs_balances_trade_and_responds_to_growth():
    z = (np.arange(400) + 0.5) / 400
    A = 0.4 * np.exp(1.5 * (1 - 2 * z))
    f = trade.dfs(A, L=1, Lf=2)
    zbar = f["share_home"]
    assert f["omega"] == pytest.approx(zbar / (1 - zbar) * 2, rel=0.02)   # the B curve
    g = trade.dfs(A, L=1, Lf=3)
    assert g["omega"] > f["omega"] and g["share_home"] < zbar
    s = trade.dfs(A, L=1, Lf=2, g=0.8)
    assert s["nontraded"].any() and s["zH"] < s["zF"]


def test_ho_zero_profits_and_full_employment():
    al, p = (0.7, 0.3), (1.0, 1.1)
    o = trade.ho_outputs(al, p, 120, 50)
    for i, a in enumerate(al):
        assert trade.unit_cost(a, o["w"], o["r"]) == pytest.approx(p[i])
    assert o["A"] @ o["Q"] == pytest.approx(np.array([120, 50]))


def test_ho_world_pattern_and_fpe():
    W = trade.ho_world((0.7, 0.3), {"lab": (120, 50), "cap": (80, 130)})
    assert W["lab"]["X"][0] > 0 > W["lab"]["X"][1]                       # labour-abundant exports cloth
    assert W["lab"]["X"] == pytest.approx(-W["cap"]["X"])                # trade balances, markets clear
    assert W["lab"]["w"] == pytest.approx(W["cap"]["w"])                 # factor prices equalized
    aL, aC = trade.ho_autarky((0.7, 0.3), 120, 50), trade.ho_autarky((0.7, 0.3), 80, 130)
    assert aL["p"] > W["p"] > aC["p"]


def test_stolper_samuelson_magnifies_and_rybczynski():
    ss = trade.stolper_samuelson((0.7, 0.3), (1.0, 1.0), 0.10, 0)
    assert ss["dw"] > 0.10 and ss["dr"] < 0
    assert np.log(1 + ss["dw"]) == pytest.approx(1.75 * np.log(1.1))   # w-hat = p-hat / (a1 - a2)
    ry = trade.rybczynski((0.7, 0.3), (1.0, 1.0), 80, 130, 0.10)
    assert ry["dQ"][1] > 0.10 and ry["dQ"][0] < 0


def test_specific_factors():
    c = trade.specific_change(1.0, 1.0, 0.10)
    assert 0 < c["dw"] < 0.10 < c["drT"] and c["drK"] < 0
    a = trade.specific_factors(1.0, 1.0)
    assert a["LM"] == pytest.approx(50.0) and a["income"] == pytest.approx(a["w"] * 100 + a["rK"] * 100 + a["rT"] * 100)


def test_tariff_areas_and_quota():
    s = trade.tariff_small(100, 10, -20, 10, 4, 1)
    assert (s["cs_loss"], s["ps_gain"], s["revenue"]) == (55, 25, 20)
    assert s["cs_loss"] - s["ps_gain"] - s["revenue"] == pytest.approx(s["dwl_production"] + s["dwl_consumption"])
    q = trade.quota_equivalent(100, 10, -20, 10, 4, 20)
    assert q["p"] == pytest.approx(5) and q["rent"] == pytest.approx(20)


def test_optimal_tariff_is_inverse_elasticity():
    o = trade.optimal_tariff(100, 10, -20, 10, -120, 40)
    assert o["ad_valorem"] == pytest.approx(o["inverse_elasticity"], rel=1e-4)
    assert o["welfare"] > 0 and trade.tariff_large(100, 10, -20, 10, -120, 40, 2.4)["welfare"] < 0


def test_protection_for_sale_signs():
    t = trade.protection_for_sale([2, 2], [2, 2], [1, 0], 50, 0.05)
    assert t[0] > 0 > t[1]
    assert trade.protection_for_sale([2], [2], [1], 5, 0.05)[0] > t[0]


def test_tariff_war_is_a_prisoners_dilemma():
    W = trade.tariff_war()
    p = W["payoffs"]
    assert p[("tariff", "free")][0] > p[("free", "free")][0] > p[("tariff", "tariff")][0] > p[("free", "tariff")][0]
    assert 0 < W["nash"] < trade.prohibitive(10, 0.5, 2)


def test_measures():
    assert trade.leontief_ratio({"capital": 2550780, "labour": 182.313},
                                {"capital": 3091339, "labour": 170.004})["ratio"] == pytest.approx(1.30, abs=0.005)
    assert trade.inner_product([1, 2], [3, -2]) == -1
    assert trade.acr_gains(0.93, 5) == pytest.approx(1 - 0.93 ** 0.2)
    assert trade.grubel_lloyd(5, 5) == 1 and trade.grubel_lloyd(5, 0) == 0


def test_factor_content_on_a_perfect_hov_world():
    rng = np.random.default_rng(0)
    cs, fs = [f"c{i}" for i in range(6)], ["K", "L"]
    V = {(c, f): rng.uniform(1, 10) for c in cs for f in fs}
    Y = {c: rng.uniform(1, 5) for c in cs}
    s = {c: Y[c] / sum(Y.values()) for c in cs}
    D = {"country": [], "factor": [], "at": [], "v": [], "y": [], "b": []}
    for c in cs:
        for f in fs:
            Vw = sum(V[x, f] for x in cs)
            D["country"].append(c)
            D["factor"].append(f)
            D["at"].append(V[c, f] - s[c] * Vw)
            D["v"].append(V[c, f])
            D["y"].append(Y[c])
            D["b"].append(0.0)
    F = trade.factor_content(D)
    assert F["sign_test"] == 1.0 and F["variance_ratio"] == pytest.approx(1.0)
