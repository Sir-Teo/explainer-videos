"""Agora's spillovers (Part 15)."""

import numpy as np
import pytest

from explainer.economics.agora import public as pb


def test_externality_pigou_tax_restores_efficiency():
    e = pb.externality(a=100, b=1, c=10, e=1, d=0.5)
    assert e["q_market"] == pytest.approx(45) and e["q_social"] == pytest.approx(36)
    assert e["tax"] == pytest.approx(18) and e["q_with_tax"] == pytest.approx(36)
    # the triangle: half the overproduction times the gap between social cost and demand at the market's quantity
    assert e["dwl"] == pytest.approx(0.5 * 9 * 22.5)


def test_coase_rules_give_the_same_herd_without_transaction_costs():
    c = pb.coase()
    assert c["loss"] == [0, 1, 3, 6, 10]                     # Coase's table, at $1 a ton
    assert c["k_star"] == 2 and c["liable"] == 2 and c["not_liable"] == 2
    lo, hi = c["payment_range"]
    assert lo == pytest.approx(1.5) and hi == pytest.approx(3.0)   # the farmer pays between 1.5 and 3 for the third
    c2 = pb.coase(transaction_cost=2.0)
    assert c2["liable"] == 2 and c2["not_liable"] == 3


def test_public_good_samuelson_nash_lindahl():
    g = pb.public_good((4, 3, 2, 1), 1.0)
    assert g["g_star"] == pytest.approx(9) and g["g_nash"] == pytest.approx(3)
    assert sum(g["lindahl_prices"]) == pytest.approx(1.0) and g["w_star"] > g["w_nash"]


def test_vcm_decays_and_punishment_sustains():
    a = pb.vcm(punish=False)["share"]
    b = pb.vcm(punish=True)["share"]
    assert a[-1] < 0.6 * a[0]
    assert b[-1] > a[-1] + 0.2


def test_fishery_open_access_dissipates_rent():
    f = pb.fishery()
    assert f["rent_oa"] == pytest.approx(0, abs=1e-9) and f["rent_mey"] > 0
    assert f["e_mey"] < f["e_msy"] < f["e_oa"] or f["e_mey"] < f["e_oa"]
    assert f["stock_oa"] < f["stock_mey"]


def test_weitzman_closed_form_matches_simulation():
    for mb, mc in ((0.5, 2.0), (2.0, 0.5)):
        w = pb.prices_quantities(mb, mc, sigma=1.0)
        assert w["loss_quota_sim"] == pytest.approx(w["loss_quota"], rel=0.05)
        assert w["loss_tax_sim"] == pytest.approx(w["loss_tax"], rel=0.05)
        assert w["loss_quota"] - w["loss_tax"] == pytest.approx(w["delta"])
    assert pb.prices_quantities(0.5, 2.0)["prefer"] == "tax"
    assert pb.prices_quantities(2.0, 0.5)["prefer"] == "quota"


def test_bottleneck_queue_is_half_the_cost():
    b = pb.bottleneck()
    t, w = b["t"], b["wait_hours"]
    queue_cost = np.trapezoid(b["alpha"] * w * b["s"], t)
    assert queue_cost == pytest.approx(b["total_cost"] / 2, rel=1e-3)
    assert w[0] == pytest.approx(0, abs=1e-9) and w[-1] == pytest.approx(0, abs=1e-9)
    assert b["max_wait_min"] == pytest.approx(36)


def test_lock_in_tips_to_one_technology():
    r = pb.lock_in(runs=12, adopters=1000)
    assert all(k is not None for k in r["lock_at"])          # every run locks in
    assert all(rc[-1] in (0.0, 1.0) for rc in r["recent"])   # after which every adopter picks the leader
    assert set(r["winners"]) == {"A", "B"}                   # and which one wins is luck
