"""Agora's tax (Part 41): Laffer, Harberger's incidence, the triangle, Ramsey, Diamond's schedule, the top rate,
bunching and evasion."""

import numpy as np
import pytest

from explainer.economics.agora import tax as T


def test_laffer_peak_matches_the_curve():
    t = np.linspace(0, 0.999, 9991)
    for e in (0.1, 0.25, 0.5, 1.0, 3.0):
        assert t[int(np.argmax(T.laffer(t, e)))] == pytest.approx(T.laffer_peak(e), abs=2e-4)
    assert T.laffer(0.0, 1.0) == 0 and T.laffer(1.0, 0.5) == 0


def test_harberger_closed_open_and_monotone():
    closed = T.harberger(0.2, 0.0)
    assert closed["K"] == pytest.approx(1.0) and closed["worker_share"] == pytest.approx(0.0, abs=1e-12)
    # with a fixed stock the owners lose exactly the revenue: no deadweight loss
    assert closed["owner_loss"] == pytest.approx(closed["revenue"]) and closed["dwl"] == pytest.approx(0.0, abs=1e-12)
    shares = [T.harberger(0.2, e)["worker_share"] for e in (0.0, 0.5, 1.0, 5.0, 50.0)]
    assert all(b > a for a, b in zip(shares, shares[1:]))
    op = T.harberger(0.2, np.inf)
    # small open economy: the net return is pinned, workers bear everything and more than the revenue
    assert op["r_net"] == pytest.approx(op["r0"]) and op["worker_share"] == pytest.approx(1.0)
    assert op["worker_per_revenue"] > 1.0
    # the closed form solves the market for capital: K = K0 (r_net / r0)^eta
    for eta in (0.5, 2.0):
        h = T.harberger(0.3, eta)
        assert h["K"] == pytest.approx((h["r_net"] / h["r0"]) ** eta, rel=1e-10)


def test_triangle_exact_against_approximation():
    small = T.triangle(0.01, 0.5, 1.0)
    assert small["dwl"] == pytest.approx(small["approx"], rel=0.03)
    # buyers bear eps_s / (eps_d + eps_s) for a small tax
    assert small["buyer_share"] == pytest.approx(2 / 3, abs=0.01)
    # the loss grows roughly with the square of the rate
    a, b = T.triangle(0.05, 0.5, 1.0)["dwl"], T.triangle(0.10, 0.5, 1.0)["dwl"]
    assert b / a == pytest.approx(4.0, rel=0.08)


def test_ramsey_inverse_elasticity_and_gain():
    r = T.ramsey([0.2, 1.0, 2.0], 0.3)
    m = np.array(r["ramsey"]) / (1 + np.array(r["ramsey"]))
    assert m * np.array(r["eps"]) == pytest.approx(np.full(3, r["k"]), rel=1e-6)
    assert sum(r["rev_ramsey"]) == pytest.approx(0.3, rel=1e-6)
    assert sum(r["rev_uniform"]) == pytest.approx(0.3, rel=1e-6)
    assert r["total_ramsey"] < r["total_uniform"]
    # equal elasticities: Ramsey is the uniform rate
    eq = T.ramsey([1.0, 1.0], 0.2)
    assert eq["ramsey"][0] == pytest.approx(eq["uniform"], rel=1e-6)


def test_diamond_schedule_shape_and_limit():
    d = T.diamond_schedule(e=0.25, alpha=2.0)
    tp = d["Tprime"]
    assert np.all((tp >= 0) & (tp < 1))
    # incomes' Pareto exponent is alpha / (1 + e), and the limit is Saez's 1 / (1 + a e)
    assert d["a_income"] == pytest.approx(2.0 / 1.25)
    assert d["top"] == pytest.approx(1 / (1 + 1.6 * 0.25))
    # the integrals include the tail beyond the grid, so the rate approaches the limit instead of falling to zero
    assert tp[-1] == pytest.approx(d["top"], abs=0.005)
    assert tp[np.searchsorted(d["F"], 0.999)] == pytest.approx(d["top"], abs=0.01)
    # U shape: lower in the middle than at both ends
    mid = tp[np.searchsorted(d["F"], 0.6)]
    assert mid < tp[np.searchsorted(d["F"], 0.05)] and mid < tp[-1]


def test_top_rate_is_the_peak_of_the_bracket_revenue():
    taus = np.linspace(0, 0.999, 9991)
    for a in (1.5, 2.0, 2.5):
        for e in (0.1, 0.25, 1.0):
            assert taus[int(np.argmax(T.top_revenue(taus, a, e)))] == pytest.approx(T.top_rate(a, e), abs=2e-4)
    assert T.top_rate(1.5, 0.25, g=1.0) == pytest.approx(0.0)
    assert T.top_rate(1.5, 0.25, g=0.25) < T.top_rate(1.5, 0.25)


def test_bunching_recovers_the_elasticity():
    for e in (0.15, 0.3):
        b = T.bunching(n=200000, e=e, seed=3)
        assert b["e_hat"] == pytest.approx(e, abs=0.04)
        assert b["share_bunched"] > 0


def test_allingham_sandmo_thresholds():
    assert T.allingham_sandmo(0.01) == pytest.approx(0.0)
    assert T.allingham_sandmo(0.6) == pytest.approx(1.0)
    ds = [T.allingham_sandmo(p) for p in (0.15, 0.25, 0.35, 0.45)]
    assert all(b >= a for a, b in zip(ds, ds[1:]))
    # a heavier fine makes honesty pay at lower audit rates
    assert T.allingham_sandmo(0.25, theta=2.0) > T.allingham_sandmo(0.25, theta=1.0)
