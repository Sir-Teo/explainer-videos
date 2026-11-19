"""Agora's competition among the few (Part 12), each result checked against a closed form."""

import numpy as np
import pytest

from explainer.economics.agora import oligopoly as ol


def test_cournot_closed_form_and_lerner_hhi():
    r = ol.cournot(100.0, 1.0, [10.0, 10.0])
    assert r["q"][0] == pytest.approx(30.0) and r["P"] == pytest.approx(40.0)
    assert r["hhi"] == pytest.approx(0.5)
    assert r["lerner"] == pytest.approx(r["lerner_hhi"])          # sum s_i (P - c_i)/P = HHI / eps
    asym = ol.cournot(100.0, 1.0, [10.0, 40.0])
    assert asym["lerner"] == pytest.approx(asym["lerner_hhi"])
    many = [ol.cournot(100.0, 1.0, [10.0] * n)["P"] for n in (1, 2, 5, 50)]
    assert many == sorted(many, reverse=True) and many[-1] < 12       # converges to cost


def test_cournot_drops_firms_that_would_produce_nothing():
    r = ol.cournot(10.0, 1.0, [1.0, 9.5])
    assert r["q"][1] == 0 and r["q"][0] == pytest.approx(4.5)


def test_cournot_dynamics_converge():
    path = ol.cournot_dynamics(100.0, 1.0, 10.0, 10.0, steps=40)
    assert path[-1] == pytest.approx([30.0, 30.0], abs=1e-6)


def test_bertrand_paradox_and_asymmetric_costs():
    assert ol.bertrand(100.0, 1.0, [10.0, 10.0])["P"] == pytest.approx(10.0)
    r = ol.bertrand(100.0, 1.0, [10.0, 20.0])
    assert r["P"] == pytest.approx(19.99) and r["profit"] > 0


def test_differentiated_bertrand_is_a_fixed_point():
    r = ol.bertrand_differentiated(10.0, 2.0, 1.0, 1.0)
    assert r["p"] == pytest.approx((10 + 2 * 1 + 1 * r["p"]) / 4)


def test_kreps_scheinkman_gives_cournot():
    k = ol.kreps_scheinkman(100.0, 1.0, 10.0)
    assert k["P"] == pytest.approx(k["cournot"]["P"])
    assert k["deviation_gain"] <= 1e-9


def test_salop_excess_entry_and_dixit_stiglitz():
    s = ol.salop(1.0, 0.01)
    assert s["n_free"] == pytest.approx(10) and s["n_opt"] == pytest.approx(5)
    assert s["cost_free"] > s["cost_opt"]
    d = ol.dixit_stiglitz(4.0, 1.0, 1.0, 100.0)
    assert d["markup"] == pytest.approx(4 / 3) and d["n"] == pytest.approx(25)


def test_dixit_credible_capacity():
    d = ol.dixit_entry(100.0, 1.0, 10.0, 30.0, 144.0)
    assert (d["S"], d["T"], d["monopoly_q"]) == pytest.approx((20, 40, 30))
    assert d["regime"] == "deter" and d["deter_k"] == pytest.approx(36)
    assert d["pi_deter"] == pytest.approx(864) and d["pi_accommodate"] == pytest.approx(450)
    k = list(d["ks"]).index(36.0) if 36.0 in list(d["ks"]) else None
    assert k is not None and d["entrant_profit"][k] == pytest.approx(0, abs=1e-6)
    assert ol.dixit_entry(100.0, 1.0, 10.0, 30.0, 50.0)["regime"] == "impossible"
    assert ol.dixit_entry(100.0, 1.0, 10.0, 30.0, 300.0)["regime"] == "blockaded"


def test_stackelberg_and_collusion_thresholds():
    st = ol.stackelberg(100.0, 1.0, 10.0)
    assert st["qL"] == pytest.approx(45) and st["qF"] == pytest.approx(22.5)
    assert st["piL"] > st["cournot"]["profits"][0] > st["piF"]
    assert ol.collusion_threshold(2, "bertrand")["delta"] == pytest.approx(0.5)
    assert ol.collusion_threshold(5, "bertrand")["delta"] == pytest.approx(0.8)
    assert ol.collusion_threshold(2, "cournot")["delta"] == pytest.approx(9 / 17)


def test_merger_paradox_and_hhi():
    m = ol.merger_cournot(3)
    assert not m["profitable"]                                         # Salant, Switzer and Reynolds
    assert ol.merger_cournot(2)["profitable"]                          # duopoly to monopoly pays
    assert m["saving_needed"] > 0
    assert ol.hhi([50, 50]) == pytest.approx(5000) and ol.hhi([0.5, 0.5]) == pytest.approx(5000)


def test_mhhi_no_common_owners_equals_hhi():
    s = [0.5, 0.5]
    own = np.eye(2)
    r = ol.mhhi(s, own, own)
    assert r["mhhi"] == pytest.approx(5000) and r["delta"] == 0
    common = np.array([[0.5, 0.5], [0.5, 0.5]])                        # each investor owns half of each firm
    assert ol.mhhi(s, common, common)["mhhi"] == pytest.approx(10000)


def test_green_porter_has_price_wars_without_cheating():
    g = ol.green_porter()
    assert 0 < g["share_war"] < 0.6


def test_leniency_makes_confessing_dominant():
    assert ol.leniency_race(100.0, 0.2, leniency=1.0)["dominant"]
    assert not ol.leniency_race(100.0, 0.2, leniency=0.5)["dominant"]
