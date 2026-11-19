"""Agora's markets with private information (Part 13)."""

import numpy as np
import pytest

from explainer.economics.agora import info


def test_lemons_partial_and_total_unravelling():
    add = info.lemons(0, 100, 30, "add")
    assert add["p_eq"] == pytest.approx(60) and add["share_traded"] == pytest.approx(0.6)
    # proportional premium below 2: the average boat offered is never worth the price, so nothing trades
    mult = info.lemons(0, 100, 1.5, "mult")
    assert mult["p_eq"] == pytest.approx(0) and mult["share_traded"] == pytest.approx(0)
    # a premium of 2 or more lets everything trade
    assert info.lemons(0, 100, 2.5, "mult")["share_traded"] == pytest.approx(1)


def test_lemons_offers_buyer_optimum():
    rows = info.lemons_offers([20, 30, 40, 60, 80])
    gains = {r["p"]: r["expected_gain"] for r in rows}
    assert gains[60] == pytest.approx(0) and gains[80] < 0
    assert max(gains, key=gains.get) == 30


def test_spence_range_and_intuitive_criterion():
    s = info.spence(1.0, 2.0, 1.0, 0.5, 0.5)
    assert (s["e_min"], s["e_max"]) == pytest.approx((1.0, 2.0))
    assert s["least_cost"] == s["e_min"]
    # with many high types, the highs would prefer pooling at no education to separating
    assert info.spence(share_high=0.9)["high_prefers_pooling"]


def test_rothschild_stiglitz_existence():
    r = info.rothschild_stiglitz(share_high=0.3)
    assert r["exists"] and 0 < r["x_low"] < r["d"]
    assert not info.rothschild_stiglitz(share_high=0.05)["exists"]
    # the high risks are indifferent between full cover and the low risks' contract
    W, d, ph = r["W"], r["d"], r["p_high"]
    full = np.log(W - ph * d)
    mimic = (1 - ph) * np.log(W - r["prem_low"]) + ph * np.log(W - d + r["x_low"] - r["prem_low"])
    assert mimic == pytest.approx(full, abs=2e-3)


def test_einav_finkelstein_reproduces_the_paper():
    e = info.einav_finkelstein()
    assert e["p_eq"] == pytest.approx(463.7, abs=0.5)        # the paper: $463
    assert e["p_eff"] == pytest.approx(264, abs=3)             # the paper: $264
    assert e["share_drop"] == pytest.approx(0.14, abs=0.005)   # the paper: 14 percentage points
    assert e["loss"] == pytest.approx(9.55, abs=0.2)           # the paper: $9.55 per employee per year
    assert e["gap_at_eq"] == pytest.approx(138, abs=3)         # the paper: $138


def test_death_spiral_shrinks_and_charges_climb():
    rows = info.death_spiral()["rows"]
    shares = [r["share"] for r in rows]
    charges = [r["charge"] for r in rows]
    assert all(a > b for a, b in zip(shares, shares[1:]))
    assert all(a < b for a, b in zip(charges, charges[1:]))
    assert all(r["cost_leavers"] < r["cost_enrolled"] for r in rows[1:])


def test_positive_correlation_signs():
    assert info.positive_correlation(selection="adverse")["lo"] > 0
    assert info.positive_correlation(selection="advantageous")["hi"] < 0
    n = info.positive_correlation(selection="none")
    assert n["lo"] < 0 < n["hi"]


def test_stiglitz_weiss_rationing_rate():
    sw = info.stiglitz_weiss()
    assert sw["R_star"] == pytest.approx(sw["safe_leave"], abs=0.2)
    assert sw["return_star"] > np.nanmax(sw["bank_return"][sw["R"] > sw["safe_leave"] + 1])


def test_reputation_bayes():
    r = info.reputation(feedback=[1, 1, 0])
    b = r["belief"]
    assert b[1] > b[0] and b[3] < b[2]
    assert r["price"][0] == pytest.approx(0.8 * 100 + 0.2 * 40)
