"""Agora's geoeconomics (Part 66): the reciprocal formula, tariffs with revenue in hat algebra, the two-bloc war, the
repeated game, dependence, resilience, infant industries and subsidy races."""

import numpy as np
import pytest

from explainer.economics.agora import tradewar as T

TWO = np.array([[0.214084, 0.020899], [0.020899, 0.744118]])


def test_reciprocal_formula():
    assert T.reciprocal_rate(136.6, 13.1) == pytest.approx(0.5 * (136.6 - 13.1) / 136.6)
    assert T.reciprocal_rate(100, 120) == 0.10                          # surplus partners get the floor
    assert T.reciprocal_rate(136.6, 13.1, phi=0.945) == pytest.approx(0.5 * (123.5 / 136.6) / 3.78, rel=1e-6)


def test_tariff_hat_zero_tariffs_is_identity_and_clears_markets():
    R = T.tariff_hat(TWO, np.zeros((2, 2)), 4.0)
    assert np.allclose(R["w"], 1) and np.allclose(R["welfare"], 0)
    t = np.array([[0, 0.2], [0.1, 0]])
    R = T.tariff_hat(TWO, t, 4.0)
    E, Y = TWO.sum(1), TWO.sum(0)
    sales = (R["pi_new"] * R["E_new"][:, None] / (1 + t)).sum(0)
    assert np.allclose(sales, R["w"] * Y, rtol=1e-8)
    # revenue is what spending exceeds income by, with balanced trade
    assert np.allclose(R["E_new"] - R["w"] * Y, R["revenue"], rtol=1e-8)
    assert E.sum() == pytest.approx(Y.sum())


def test_large_country_gains_alone_and_both_lose_in_war():
    one = T.tariff_hat(TWO, np.array([[0, 0.25], [0, 0]]), 4.0)["welfare"]
    war = T.tariff_hat(TWO, np.array([[0, 0.25], [0.25, 0]]), 4.0)["welfare"]
    assert one[0] > 0 > one[1]
    assert war[0] < 0 and war[1] < 0


def test_two_bloc_nash_and_optimal_tariff():
    B = T.two_bloc(TWO, 0, 4.0, grid=np.round(np.linspace(0, 0.6, 13), 3))
    assert 0.15 <= B["optimal"] <= 0.35
    assert B["nash_us"] < 0 and B["nash_ro"] < 0
    # the optimal tariff falls as trade becomes more responsive
    B8 = T.two_bloc(TWO, 0, 8.0, grid=np.round(np.linspace(0, 0.6, 13), 3))
    assert B8["optimal"] < B["optimal"]


def test_repeated_game():
    B = T.two_bloc(TWO, 0, 4.0, grid=np.round(np.linspace(0, 0.6, 13), 3))
    R = T.repeated(T.stage_payoffs(B, 0.25))
    assert R["best"]["never retaliates"] == "a tariff, kept"
    assert R["best"]["retaliates for ever"] == "free trade throughout"
    assert R["best"]["tit for tat"] == "free trade throughout"


def test_cutoff_loss_matches_acr():
    assert float(T.cutoff_loss(0.2, 4.0)) == pytest.approx(1 - 0.8 ** 0.25)
    assert float(T.cutoff_loss(0.0, 4.0)) == 0.0
    s = np.linspace(0, 0.5, 11)
    assert np.all(np.diff(T.cutoff_loss(s, 2.0)) > 0)
    assert np.all(T.cutoff_loss(s[1:], 2.0) > T.cutoff_loss(s[1:], 8.0))


def test_resilience_private_above_social():
    R = T.resilience()
    assert R["x_private"] == pytest.approx(0.5) and R["x_social"] == pytest.approx(0.25)
    assert R["social_at_social"] < R["social_at_private"]
    g = np.array(R["grid"])
    assert g[np.argmin(R["social"])] == pytest.approx(R["x_social"], abs=0.01)


def test_infant_industry_tests():
    slow, mid, fast = (T.infant_industry(b, r=0.10) for b in (0.15, 0.20, 0.30))
    assert not slow["mill"] and not slow["bastable"]
    assert mid["mill"] and not mid["bastable"]
    assert fast["mill"] and fast["bastable"]


def test_brander_spencer():
    B = T.brander_spencer(a=10, c=1)
    assert B["s_one"] == pytest.approx(9 / 4) and B["s_nash"] == pytest.approx(9 / 5)
    assert B["none"]["w1"] == pytest.approx(81 / 9)
    assert B["one"]["w1"] > B["none"]["w1"] > B["both"]["w1"]
    assert B["both"]["consumers"] > B["none"]["consumers"]
    # the one-sided subsidy is a best response: welfare falls if it is moved either way
    def w(s1):
        q1 = (9 + 2 * s1) / 3
        return (9 - s1) / 3 * q1
    assert w(B["s_one"]) > w(B["s_one"] + 0.1) and w(B["s_one"]) > w(B["s_one"] - 0.1)
