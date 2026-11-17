"""Psyche's lifespan module (Part 31)."""

import numpy as np
import pytest

from explainer.psychology.psyche import lifespan as L


def test_apc_identity_any_shift():
    for k in (-3.0, 0.5, 10.0):
        r = L.apc_equivalent(0.1, -0.2, 0.3, k, [20, 45, 70], [1980, 2000, 2020])
        assert r["max_diff"] < 1e-9


def test_designs_disagree_and_cohort_sequential_recovers():
    w = L.ability_world(n=20_000)
    cs = L.cross_sectional(w)
    # cross-sectional "decline" already by 50, where the true curve is flat
    i50 = list(cs["age"]).index(50.0)
    assert cs["mean"][0] - cs["mean"][i50] > 0.3
    lo = L.longitudinal(w)
    # practice and drop-out make the survivors improve through their forties
    assert lo["kept"][3] > lo["kept"][0] + 0.15
    assert lo["n"][-1] < lo["n"][0]
    cq = L.cohort_sequential(w)
    assert abs(cq["cohort_gain_hat"] - 0.02) < 0.004
    truth = L.true_ageing(cq["age"]) - L.true_ageing(40)
    assert np.max(np.abs(cq["curve"] - truth)) < 0.12


def test_growth_model_recovers_parameters_and_shrinks():
    g = L.growth_data(n=150, seed=5)
    f = L.fit_growth(g["t"], g["y"], iters=200)
    assert abs(f["beta"][1] - 6.0) < 0.6
    assert abs(f["sd_slope"] - 2.0) < 0.6
    assert abs(f["sd_e"] - 5.0) < 0.6
    # BLUP slopes are pulled toward the mean: less spread than each child's own line
    assert np.std(f["blup"][:, 1]) < np.nanstd(f["ols"][:, 1])


def test_lexis_kinds():
    a = L.lexis("age")["table"]
    assert np.allclose(a, a[:, :1])  # rows constant across periods
    p = L.lexis("period")["table"]
    assert np.allclose(p, p[:1, :])  # columns constant across ages
    c = L.lexis("cohort")
    t = c["table"]
    assert np.isclose(t[0, 0], t[1, 1])  # constant along diagonals
    with pytest.raises(ValueError):
        L.lexis("weather")


def test_dual_systems_and_reserve():
    d = L.dual_systems(np.arange(10, 31))
    assert 10 + int(np.argmax(d["seeking"])) == 19
    assert 13 <= 10 + int(np.argmax(d["gap"])) <= 18
    ages = np.arange(50, 96)
    lo, hi = L.reserve(ages, 0.5), L.reserve(ages, 2.0)
    assert hi["onset"] > lo["onset"]
    assert np.isclose(lo["cognition"][-1], hi["cognition"][-1])  # same end
    # once past threshold, the high-reserve decline is steeper
    assert np.min(np.diff(hi["cognition"])) < np.min(np.diff(lo["cognition"]))


def test_ace_and_paf():
    s = L.sibling_correlations(0.5, 0.3)
    assert np.isclose(s["mz"] - s["dz"], 0.25) and s["adoptive"] == 0.3
    assert np.isclose(L.paf(0.5, 2.0), 1 / 3)
    assert L.combined_paf([0.1, 0.1]) < 0.2
    assert np.isclose(L.flynn_norms(20), 106.0)
