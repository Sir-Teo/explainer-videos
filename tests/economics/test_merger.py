"""Agora's merger-review toolkit (Part 59): the Island's office-supply market and the tools an agency and a court use,
checked against their definitions and against the truth the Island knows."""

import numpy as np
import pytest

from explainer.economics.agora import io as IO
from explainer.economics.agora import merger as M


@pytest.fixture(scope="module")
def small_towns():
    return M.towns(n=12, seed=7)


def test_equilibrium_solves_the_first_order_conditions():
    eq = M.equilibrium(np.ones(4, bool))
    p, s, mc = eq["p"], eq["s"], eq["mc"]
    J = IO.jacobian(eq["f"], p)
    foc = s + np.diag(J) * (p - mc)
    assert np.max(np.abs(foc)) < 1e-7
    assert np.all(p > mc)


def test_critical_diversion_and_the_playit_pairs():
    assert M.critical_diversion(0.05, 0.4) == pytest.approx(0.05 / 0.45)
    pairs = M.playit_pairs()
    assert [q["one_market"] for q in pairs] == [True, False, True]
    for q in pairs:
        assert q["critical"] == pytest.approx(0.05 / (0.05 + q["M"]))


def test_hypothetical_monopolist_and_cellophane():
    assert not M.hmt(candidate=(0,))["passes"]
    assert M.hmt(candidate=(0, 1))["passes"]
    h = M.hmt(candidate=(0, 1, 2))
    assert h["passes"] and h["actual_loss"] < h["critical_loss"]
    assert h["critical_loss"] == pytest.approx(0.05 / (0.05 + h["margin"]))
    cel = M.cellophane()
    assert cel["competitive"]["passes"] and not cel["monopoly"]["passes"]
    assert np.all(np.array(cel["p_mono"][:3]) > np.array(cel["p_comp"][:3]))


def test_hhi_and_the_guidelines():
    r = M.presumption([30, 25, 20, 15, 10], (3, 4))
    assert r["delta"] == pytest.approx(2 * 15 * 10)
    assert r["post"] == pytest.approx(r["pre"] + r["delta"])
    grocers = next(x for x in M.industries() if x["name"] == "grocers")
    assert grocers["verdict"] == {1982: True, 2010: False, 2023: True}
    # the 2023 share test: 30% buys 4% in an unconcentrated market
    s = [30, 4] + [6.6] * 10
    v = M.presumption(s, (0, 1))
    assert v["post"] < 1800 and v["verdict"] == {1982: False, 2010: False, 2023: True}


def test_pricing_pressure_against_simulation():
    U = M.upp()
    a = U["products"]["Alder"]
    p, c = U["prices"], U["mc"]
    assert a["guppi"] == pytest.approx(a["diversion"] * (p[1] - c[1]) / p[0])
    # the first-order screen and the full simulation agree to within a couple of points here
    assert abs(a["guppi"] - U["simulation"]["dp"][0]) < 0.02
    assert all(x > 0.1 for x in U["cmcr"])


def test_functional_forms_order_and_linear_closed_form():
    F = M.functional_forms(0.3, 0.3)
    lin, logit, loglin, ce = F["rise"]
    assert lin < logit < loglin < ce
    e = 1 / 0.3
    b, d, c = e, 0.3 * e, 0.7
    a = 1 + b - d
    assert lin == pytest.approx(100 * ((a + (b - d) * c) / (2 * (b - d)) - 1), rel=1e-6)
    # a saving lowers every prediction
    assert all(x < y for x, y in zip(M.functional_forms(0.3, 0.3, 0.05)["rise"], F["rise"]))


def test_pass_through_merged_below_single():
    P = M.pass_through()
    assert 0 < P["merged"][0] < P["single"] < 1


def test_vertical_threshold_is_break_even():
    V = M.vertical()
    assert V["fee_rise"] == pytest.approx(0.5 * 0.10 * 0.45 * 40)
    assert M.vertical(depart=V["threshold"])["net"] == pytest.approx(0.0, abs=1e-12)


def test_cartel_overcharge_and_screen():
    C = M.cartel()
    assert abs(C["estimate"] - C["truth"]) < 0.01
    v = M.variance_screen(C["price"], C["cost"])
    inside = v["cv"][C["start"] + 12:C["end"] - 1].mean()
    outside = np.r_[v["cv"][12:C["start"] - 1], v["cv"][C["end"] + 12:]].mean()
    assert inside < 0.5 * outside


def test_labour_merger_lowers_wages():
    L = M.labour_merger()
    assert L["after"][0] < L["before"][0]
    assert L["markdown_after"] > L["markdown_before"] > 0


def test_plain_logit_understates_the_harm(small_towns):
    A = M.agency_logit(small_towns)
    pred, truth = np.array(A["predicted"]), np.array(A["truth"])
    assert len(pred) == int(small_towns["birch"].sum())
    assert np.all(pred < truth)


def test_regression_and_witness(small_towns):
    R = M.price_regression(small_towns)
    assert R["birch"] > 0
    W = M.witness(small_towns)
    assert W["loo_min"] <= W["base"] <= W["loo_max"]


def test_regulated_prices():
    r = M.rate_case()
    assert r["requirement"] == pytest.approx(40 + 20 + 10 + 0.07 * 500)
    cap = M.price_cap()
    assert cap["price_cap"][5] == pytest.approx(cap["cost_cap"][5])
    assert cap["price_cap"][3] == pytest.approx(cap["price_cap"][2] * (1 + cap["rpi"] - cap["X"]))
    e = M.ecpr()
    assert e["access"] == pytest.approx(e["network_cost"] + e["margin"])
