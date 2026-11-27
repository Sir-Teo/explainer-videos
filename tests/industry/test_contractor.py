"""The Works' contractor (Part 24): sealed bids and the winner's curse, and the cash a contractor's jobs hand it."""

import math

import numpy as np

from explainer.industry.works import contractor as K


def test_with_one_bidder_the_margin_is_the_markup():
    t = K.Tender(rivals=0)
    r = t.bid(0.08)
    assert math.isclose(r["win"], 1.0, rel_tol=1e-9)
    assert math.isclose(r["profit"], 8.0, rel_tol=1e-3)
    assert abs(r["est_if_won"]) < 1e-6


def test_the_winners_curse():
    r = K.Tender().bid(0.08)
    assert r["margin"] < 0.08 / 3          # adding 8% leaves under a third of it
    assert r["est_if_won"] < -0.04         # the winner's estimate was low
    assert 0 < r["loss_if_won"] < 1


def test_win_rate_falls_and_margin_rises_with_the_markup():
    t = K.Tender()
    rs = [t.bid(m) for m in (0.0, 0.04, 0.08, 0.12, 0.16)]
    assert all(a["win"] > b["win"] for a, b in zip(rs, rs[1:]))
    assert all(a["margin"] < b["margin"] for a, b in zip(rs, rs[1:]))
    assert t.bid(0.02)["profit"] < 0 < t.bid(0.08)["profit"]


def test_matching_the_rivals_wins_a_fair_share():
    assert math.isclose(K.Tender().bid(0.08)["win"], 1 / 5, rel_tol=1e-3)


def test_win_chance_matches_a_simulation():
    t = K.Tender()
    rng = np.random.default_rng(24)
    e = rng.normal(0, t.sd, (200_000, 5))
    bids = t.cost * (1 + e) * np.array([1.05, 1.08, 1.08, 1.08, 1.08])
    assert abs((bids.argmin(axis=1) == 0).mean() - t.bid(0.05)["win"]) < 0.005


def test_a_shrinking_order_book_drains_cash_while_profit_rises():
    p = K.cash_path([1] * 24 + [0] * 12)
    cash, profit = p["cash"], p["profit"]
    peak = int(np.argmax(cash[:40]))
    assert 20 <= peak <= 30
    assert cash[peak + 8] < cash[peak] - 20 and profit[peak + 8] > profit[peak]
    assert math.isclose(cash[-1], profit[-1], rel_tol=1e-9)   # in the end cash and profit agree


def test_one_job_ends_with_its_margin_in_cash():
    f = K.job_flows(value=100, margin=0.03)
    assert math.isclose(f.sum(), 3.0, rel_tol=1e-9)
