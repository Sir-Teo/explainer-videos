"""Agora's economics of AI (Part 65): the task model, the J-curve, the support desk, Hulten's arithmetic, growth with
automated research, Baumol, the race between automation and capital, Varian's shoppers, entry, Keynes's forecasts."""

import numpy as np
import pytest

from explainer.economics.agora import automation as A


def test_task_wage_formula_and_decomposition():
    # the short-run wage is Y^(1/sigma) (N - I)^(1/sigma) L^(-1/sigma): check against a numerical derivative
    s = 0.8
    d = A.tasks(0.4, sigma=s, K=2.0, L=1.0)
    h = 1e-6
    dY = (A.tasks(0.4, sigma=s, K=2.0, L=1.0 + h)["Y"] - A.tasks(0.4, sigma=s, K=2.0, L=1.0 - h)["Y"]) / (2 * h)
    assert d["w"] == pytest.approx(dY, rel=1e-6)
    assert d["w"] == pytest.approx(d["Y"] ** (1 / s) * 0.6 ** (1 / s), rel=1e-9)
    T = A.task_paths()
    # automation stops where machines are no longer cheaper: K/(K + L) with equal productivities
    assert T["parity"] == pytest.approx(2 / 3, abs=1e-6)
    assert T["displacement"] + T["productivity"] == pytest.approx(T["dlnw"], abs=1e-9)
    assert T["displacement"] < 0 < T["productivity"]


def test_long_run_share_falls_and_new_tasks_restore_it():
    T = A.task_paths()
    ls = np.array(T["long"]["labour_share"])
    assert np.all(np.diff(ls) < 0) and np.all(np.diff(T["long"]["w"]) > 0)
    nt = T["new_tasks"]
    assert np.all(np.diff(nt["labour_share"]) > 0) and nt["w"][-1] > nt["w"][0]
    # the unit-cost condition holds in the long run: labour's share + capital's = 1
    d = A.tasks(0.5, sigma=0.8, R=0.8)
    assert d["labour_share"] + d["r"] * (d["Y"] * 0.5 * (0.8) ** (-0.8)) / d["Y"] == pytest.approx(1.0, abs=1e-9)


def test_so_so_automation_gains_shrink_with_the_machine_cost():
    rows = A.so_so()["rows"]
    gains = [r["wage_gain"] for r in rows]
    assert all(a > b for a, b in zip(gains, gains[1:])) and gains[-1] < 0.05 < 0.5 < gains[0]
    assert all(r["w_over_R"] > 1 for r in rows)                 # automation is profitable throughout


def test_j_curve_dips_then_overshoots():
    J = A.j_curve()
    assert J["low"] < 0.95 and J["start"] < J["low_year"] < J["start"] + J["build"]
    assert J["end"] > J["end_true"] > 1.0 and J["cross"] is not None


def test_support_desk_recovers_the_planted_effects():
    D = A.support_desk()
    assert D["lo"] < D["truth"] < D["hi"]
    F = D["fifths"]
    assert F[0]["est"] > F[-1]["est"] + 0.2
    assert all(f["lo"] - 0.02 < f["truth"] < f["hi"] + 0.02 for f in F)
    assert D["gap_treated"] < D["gap_control"]


def test_hulten_reproduces_acemoglu():
    h = A.hulten_ai()
    assert float(h["share_affected"]) == pytest.approx(0.046, abs=1e-9)
    assert float(h["cost_saving"]) == pytest.approx(0.14445, abs=1e-9)
    assert float(h["tfp"]) == pytest.approx(0.0066, abs=1e-4)


def test_research_automation_booms_then_bottlenecks():
    g0 = A.ideas_growth(0.0)
    # semi-endogenous balanced growth: g_A = n/(1 - phi) = 2%, output per person g_A/(1 - alpha)
    assert g0["ideas_growth"][-1] == pytest.approx(0.02, abs=0.002)
    assert g0["growth"][-1] == pytest.approx(0.02 / 0.65, abs=0.003)
    g9 = A.ideas_growth(0.9)
    assert max(g9["growth"]) > 0.15 and g9["growth"][-1] < 0.06 and not g9["exploded"]
    assert g9["people_share"][0] < 0.01 and g9["people_share"][-1] > 0.99
    assert A.ideas_growth(1.0)["exploded"]


def test_baumol_slides_to_the_slow_sector():
    B = A.baumol(years=301)
    assert B["share_fast"][-1] < 0.01
    assert B["growth"][-1] == pytest.approx(B["g_slow"], abs=0.001)
    assert np.all(np.diff(B["growth"]) < 0)


def test_race_wage_floor_and_labour_share():
    R = A.race_scenarios()
    bau, f20 = R["business as usual"], R["every task in 20 years"]
    assert bau["w"][-1] > 2 * bau["w"][0] * 0.9
    assert f20["w"][-1] == pytest.approx(1.0, abs=1e-3)        # the machine-equivalent wage, A_L r / A_K
    assert f20["labour_share"][-1] < 0.1 and f20["Y"][-1] > 3 * bau["Y"][-1]


def test_varian_average_price_formula():
    S = A.shoppers()
    for r in S["rows"]:
        assert r["average_paid"] == pytest.approx(S["c"] + (1 - r["mu"]) * (S["v"] - S["c"]), abs=2e-3)
        assert S["c"] - 1e-9 <= r["shoppers_pay"] <= r["mean_price"] <= S["v"] + 1e-9


def test_frontier_entry_formula():
    E = A.frontier_entry()
    for m, c, n in zip(E["market"], E["cost"], E["n"]):
        assert n == max(1, int(np.floor(np.sqrt(m / c) - 1)))
    assert E["n"][0] > E["n"][-1]


def test_keynes_forecasts_on_the_data_room():
    K = A.keynes()
    assert all(4.0 < v < 8.0 for v in K["ratio"].values())    # inside his four to eight
    assert all(min(h["hours"][-3:]) > 2 * K["keynes_hours"] * 0.8 for h in K["hours"].values())
