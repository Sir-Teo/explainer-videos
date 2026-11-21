"""Agora's firm from the inside (Part 62): checked against closed forms and the truths the simulations plant."""

import numpy as np
import pytest

from explainer.economics.agora import org as O


def test_competition_narrows_the_survivors_spread():
    D = O.dispersion()
    ratios = [r["ratio_90_10"] for r in D["rows"]]
    assert all(a > b for a, b in zip(ratios, ratios[1:]))
    assert ratios[0] < D["entry_ratio_90_10"]


def test_management_slope_and_owner_ranking():
    M = O.management()
    assert M["slope"] == pytest.approx(M["planted_slope"], abs=0.05)
    by = M["by_owner"]
    assert by["family-owned, family chief executive"] < by["dispersed shareholders"]


def test_cheap_practices_pay_most():
    P = O.practices()
    assert P["best"] == "record and act on defects"
    assert P["rows"]["a faster loom"]["mean_net"] < 0


def test_experiment_recovers_the_planted_effect():
    X = O.experiment(reps=150)
    assert X["plants"] == 28
    assert abs(X["mean_est"] - X["effect"]) < 4 * X["sd_est"] / np.sqrt(150)


def test_piece_rates_raise_output_by_effort_and_sorting():
    P = O.piece_rates()
    assert 0 < P["gain_effort"] < P["gain_total"]
    assert 0.2 < P["share_sorting"] < 0.8
    assert P["ability_hires"] > P["ability_staff"]


def test_best_manager_beats_best_seller():
    R = O.peter()["rules"]
    assert R["the best manager"]["team_sales"] > R["the best seller"]["team_sales"]
    assert R["the best seller"]["sales_skill"] > R["the best manager"]["sales_skill"]


def test_gabaix_landier_scaling():
    C = O.ceo_pay()
    assert C["ratio_after_sixfold"] == pytest.approx(6.0)
    assert C["elasticity_own_size"] == pytest.approx(1 / 3)
    pay = np.array(C["pay"])
    assert pay[0] / pay[7] == pytest.approx(8 ** (1 / 3))


def test_weak_boards_pay_for_luck():
    L = O.pay_for_luck()
    assert abs(L["strong board"]["on_luck"]) < 0.05
    assert L["weak board"]["on_luck"] > 0.4


def test_tradeoff_interior_and_perks_closed_form():
    T = O.tradeoff()
    assert 0 < T["best"] < 0.95 and T["gain"] > 0
    P = O.perks(alphas=[0.5, 1.0], k=3.0)
    assert P["perks"] == pytest.approx([5.0, 2.0])


def test_buyouts_cut_old_jobs_and_raise_productivity():
    B = O.buyouts()
    assert B["emp_original"][5] < 0 < B["productivity"][5]
    assert B["emp_firm"][5] > B["emp_original"][5]


def test_hierarchy_comparative_statics():
    H = O.hierarchy(hs=(0.6, 0.1), cs=(0.08, 0.03))["rows"]
    at = {(r["h"], r["c"]): r for r in H}
    assert at[(0.1, 0.08)]["zw"] < at[(0.6, 0.08)]["zw"]          # cheap communication: workers know less
    assert at[(0.6, 0.03)]["zw"] > at[(0.6, 0.08)]["zw"]          # cheap knowledge: workers know more
    r = at[(0.6, 0.08)]
    assert r["span"] == pytest.approx(np.exp(r["zw"]) / 0.6, rel=1e-6)


def test_wfh_trial_and_discount_selection():
    W = O.wfh()
    assert W["performance"] == pytest.approx(1.09 * 1.04 - 1, abs=3 * W["performance_se"])
    assert W["quit_home"] < W["quit_office"]
    G = O.conglomerates()
    assert G["discount"] < G["true_effect"] < 0
