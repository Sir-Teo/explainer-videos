"""Agora's exam module (Part 56): each question's formula against its brute-force check, and the textbook answers."""

import numpy as np
import pytest

from explainer.economics.agora import exam


def test_kinked_budget_segments_slutsky_and_cv():
    k = exam.kinked_budget()
    assert k["where"] == "second segment" and k["x"] == pytest.approx(24) and k["y"] == pytest.approx(72)
    assert k["total"] == pytest.approx(-8.0) and k["substitution"] == pytest.approx(-7.2)
    assert k["wrong_total"] == pytest.approx(-12.0)
    assert k["cv"] == pytest.approx(120 * 1.25 ** 0.4 - 130, abs=1e-8) and k["cv"] < k["laspeyres"] == pytest.approx(2)
    # a consumer with alpha in [0.2, 1/3] bunches at the kink
    for alpha in (0.25, 0.3):
        assert exam.kinked_budget(alpha=alpha)["where"] == "the kink"
    assert exam.kinked_budget(alpha=0.15)["where"] == "first segment"


def test_externality_pareto_and_pigou():
    e = exam.externality_box()
    assert e["xa_eq"] == 5 and e["p_eq"] == pytest.approx(0.8)
    assert e["xa_po"] == pytest.approx((26 - np.sqrt(26 ** 2 - 320)) / 2)
    assert e["tax"] == pytest.approx(0.5) and e["gain"] > 0
    assert exam.externality_box(e=0.0)["xa_po"] == pytest.approx(5.0)


def test_reserve_auction_revenue_and_best_response():
    a = exam.reserve_auction(draws=200_000)
    assert a["rev"] == pytest.approx(5 / 12) and a["rev0"] == pytest.approx(1 / 3)
    assert abs(a["rev_fp_sim"] - a["rev"]) < 5e-3 and abs(a["rev_sp_sim"] - a["rev"]) < 5e-3
    assert a["b_08"] == pytest.approx((0.64 + 0.25) / 1.6)


def test_screening_two_types_and_continuum():
    s = exam.screening()
    assert (s["q_l"], s["q_h"], s["t_l"], s["t_h"]) == pytest.approx((0.5, 2.0, 0.5, 3.5))
    assert s["profit"] == pytest.approx(0.75) and s["profit_c"] == pytest.approx(2 / 3, abs=1e-4)
    th, t = np.array(s["theta"]), np.array(s["t"])
    assert np.allclose(t, th ** 2 - 1, atol=1e-4)
    # when the high type is common enough, the low type is shut out
    assert exam.screening(pi_h=0.5)["q_l"] == 0


def test_ramsey_tax_transition():
    r = exam.ramsey_tax()
    assert r["k_new"] == pytest.approx((1 / 3 / 0.09) ** 1.5) and r["k_old"] == pytest.approx((1 / 3 / 0.08) ** 1.5)
    assert r["c0"] > r["c_old"] > r["c_new"]
    assert r["path_k"][-1] == pytest.approx(r["k_new"], rel=1e-3)


def test_mccall_reservation_wages_fall_toward_exhaustion():
    m = exam.mccall_expiring()
    res = np.array(m["res"])
    assert np.all(np.diff(res) > 0) and res[-1] < m["res_inf"]
    assert res[0] == pytest.approx(0.7404, abs=1e-3)


def test_discretion_bias_and_commitment():
    d = exam.discretion()
    assert d["pi_bar"] == pytest.approx(1.0) and d["x_bar"] == pytest.approx(0.1)
    assert d["loss_c"] < d["loss_d"] and d["pi_c"][0] < d["pi_d"][0]


def test_supply_demand_wald_beats_ols():
    sd = exam.supply_demand()
    assert abs(sd["wald"] + 1) < 3 * sd["se_wald"] + 0.05 and abs(sd["ols"] + 1) > 0.5
    assert sd["plim_ols"] == pytest.approx(-1 + 0.5 / 0.71)


def test_euler_gmm_counts():
    g = exam.euler_gmm(T=1500)
    assert g["m"] == 8 and g["df"] == 6
    assert abs(g["two"]["theta"][1] - 3) < 0.5


def test_staggered_did_twfe_and_bacon():
    st = exam.staggered_did()
    assert st["twfe"] == pytest.approx(2.0) and st["att"] == pytest.approx(46 / 12)
    assert st["imputation"] == pytest.approx(st["att"], abs=1e-6) and st["neg_weight_cells"] == 4
    assert exam.staggered_did(never=False)["twfe"] == pytest.approx(-1 / 6)


def test_long_run_var_identifies_b():
    lv = exam.long_run_var(reps=30)
    B, L = np.array(lv["B"]), np.array(lv["L"])
    assert abs(L[0, 1]) < 1e-12
    assert np.allclose(np.array(lv["B_est_mean"]), B, atol=0.08)
