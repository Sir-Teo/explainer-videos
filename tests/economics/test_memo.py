"""Agora's policy memo (Part 50): the credits' rules, the microsimulation's calibration and comparisons, the value of
public funds and the cost of a top surtax."""

import numpy as np
import pytest

from explainer.economics.agora import memo


def test_old_credit_phases_in_and_offsets_tax():
    e = np.array([0.0, 2500.0, 10000.0, 20000.0, 30000.0, 60000.0])
    k = np.full_like(e, 2)
    m = np.zeros_like(e, dtype=int)
    c = memo.ctc_2020(e, k, m)
    assert np.allclose(c, [0.0, 0.0, 1125.0, 2745.0, 3920.0, 4000.0])


def test_allowance_is_flat_then_phases_out():
    e = np.array([0.0, 50000.0, 75000.0, 101000.0, 127000.0, 200000.0])
    one = np.ones_like(e)
    single = np.zeros_like(e, dtype=int)
    a = memo.allowance_2021(e, one, one, single)
    assert np.allclose(a[:3], 6600.0)
    assert a[3] == pytest.approx(6600.0 - 0.05 * 26000.0)
    assert a[4] == pytest.approx(4000.0) and a[5] == pytest.approx(4000.0)   # back to the old 2,000 a child


def test_eitc_2021_parameters():
    one = np.array([1, 2, 3])
    single = np.zeros(3, dtype=int)
    assert np.allclose(memo.eitc_2021(np.full(3, 15000.0), one, single), [3618.0, 5980.0, 6728.0])
    # the phase-out begins at 19,520 for a single parent and 25,470 for a couple
    assert memo.eitc_2021([19520.0], [2], [0])[0] == pytest.approx(5980.0)
    assert memo.eitc_2021([25470.0], [2], [1])[0] == pytest.approx(5980.0)
    assert memo.eitc_2021([60000.0], [2], [0])[0] == 0.0


def test_hybrid_keeps_the_reward_for_work():
    e = np.array([0.0, 20000.0])
    one = np.ones(2)
    single = np.zeros(2, dtype=int)
    h = memo.hybrid_2021(e, one, one, single)
    o = memo.ctc_2020(e, 2 * one, single)
    assert h[0] == pytest.approx(2600.0)
    assert (h[1] - h[0]) == pytest.approx(o[1] - o[0])


@pytest.fixture(scope="module")
def fam():
    return memo.families(n=8000, married_share=0.65, seed=3)


def test_calibration_under_the_old_credit(fam):
    s = memo.simulate(fam, "ctc", elasticity=0.25)
    assert s["work_single"] == pytest.approx(0.85, abs=0.02)
    assert s["work_married"] == pytest.approx(0.95, abs=0.01)


def test_comparison_orders_and_is_noise_free_at_zero_elasticity(fam):
    r0 = memo.compare(fam, elasticity=0.0)
    assert r0["exits"] == 0
    assert r0["new"]["child_poverty"] == pytest.approx(r0["static_child_poverty"])
    assert r0["cost"] == pytest.approx(r0["static_cost"])
    r = memo.compare(fam, elasticity=0.25)
    assert r["static_child_poverty"] < r["new"]["child_poverty"] < r["old"]["child_poverty"]
    assert r["exits"] > 0
    hi = memo.compare(fam, elasticity=0.5)
    assert hi["new"]["child_poverty"] > r["new"]["child_poverty"]
    assert hi["new"]["deep"] > r0["new"]["deep"]


def test_take_up_lowers_cost_and_the_poverty_fall(fam):
    full = memo.compare(fam, elasticity=0.25, take_up=1.0)
    part = memo.compare(fam, elasticity=0.25, take_up=0.85)
    assert part["per_child"] < full["per_child"]
    assert part["new"]["child_poverty"] > full["new"]["child_poverty"]


def test_second_design_is_cheaper_with_few_exits(fam):
    a = memo.compare(fam, elasticity=0.25)
    h = memo.compare(fam, elasticity=0.25, policy="hybrid")
    assert h["per_child"] < a["per_child"]
    assert h["exits"] < 0.1 * a["exits"]
    assert h["new"]["deep"] < h["old"]["deep"]


def test_mvpf_and_top_surtax():
    assert memo.mvpf(100.0, 100.0) == 1.0
    assert memo.mvpf(100.0, 100.0, child_return=50.0) == 2.0
    assert memo.mvpf(100.0, 100.0, child_return=100.0) == float("inf")
    assert memo.top_mcpf(0.4, 1.5, 0.25) == pytest.approx(4 / 3)
    assert memo.top_mcpf(0.4, 1.5, 0.5) == pytest.approx(2.0)
    assert memo.top_mcpf(0.4, 1.5, 0.0) == pytest.approx(1.0)
    assert memo.top_mcpf(0.7, 1.5, 1.0) == float("inf")


def test_tornado_shapes(fam):
    rows = memo.tornado(fam, {"elasticity": 0.25, "income_effect": 0.0, "take_up": 1.0},
                        {"elasticity": (0.0, 0.5), "take_up": (0.85, 1.0)})
    by = {r["dial"]: r for r in rows}
    assert by["elasticity"]["at_low"] < by["elasticity"]["at_high"]
    assert by["take_up"]["at_low"] > by["take_up"]["at_high"]


def test_poverty_line_scales_with_family_size():
    assert memo.poverty_line(1, 2) == pytest.approx(24000.0)
    assert memo.poverty_line(0, 2) == pytest.approx(24000.0 * np.sqrt(0.75))
