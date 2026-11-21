"""Agora's dissertation (Part 68): the year-on-year difference in differences, the discontinuity in time, the
calibrated congestion model and its counterfactual, and the Island study."""

import numpy as np
import pytest

from explainer.economics import data
from explainer.economics.agora import congestion as C


def test_yoy_did_cancels_seasons_and_levels():
    weeks = [f"{y}-{m:02d}-01" for y in range(2022, 2027) for m in range(1, 13)]
    season = {m: 1 + 0.2 * np.sin(m) for m in range(1, 13)}
    series = {}
    for k, base in ((C.TREATED[0], 5.0), (C.TREATED[1], 3.0)):
        series[k] = np.array([base * season[int(w[5:7])] * (0.97 if w >= "2025" else 1.0) for w in weeks])
    for k in C.CONTROLS:
        series[k] = np.array([2.0 * season[int(w[5:7])] for w in weeks])
    D = C.yoy_did({"weeks": weeks, "series": series})
    assert D["effect"] == pytest.approx(np.log(0.97), abs=1e-12)
    assert D["placebo_mean"] == pytest.approx(0.0, abs=1e-12)
    assert D["after_2026"] == pytest.approx(0.0, abs=1e-12)


def test_the_real_data():
    D = C.yoy_did(C.crossings_panel(data.mta_crossings()))
    assert D["n"] == 12 and D["effect"] < D["effect"] - D["placebo_mean"] < 0
    T = data.crz_tod()
    assert T["weekdays"] > 400 and len(T["hour"]) == 144
    assert C.time_rd(T, 21.0)["jump"] > 0.1 and C.time_rd(T, 5.0)["jump"] < -0.2


def test_time_rd_recovers_a_known_jump():
    hours = np.repeat(np.arange(24), 6)
    minutes = np.tile(np.arange(0, 60, 10), 24)
    t = hours + minutes / 60
    y = np.exp(7 + 0.05 * (t - 21) + 0.3 * (t >= 21))
    R = C.time_rd({"hour": hours.tolist(), "minute": minutes.tolist(), "cars": y.tolist(), "weekdays": 1}, 21.0)
    assert R["jump"] == pytest.approx(0.3, abs=1e-9)


def test_model_identities():
    M = C.congestion_model(-0.04, -0.02, 9.0, 20.0, miles=3.0, mph=10.0)
    assert M["e_tv"] == pytest.approx(0.5) and M["s_old"] == pytest.approx(0.125)
    assert M["mec_old"] == pytest.approx(M["e_tv"] * M["T_old"] * M["vot"], rel=1e-9)   # e x T x VOT
    e = C.equilibrium(M, 9.0)
    assert e["lnV"] == pytest.approx(-0.04, abs=2e-3)                                     # the observed point
    o = C.optimal_toll(M)
    assert o["toll"] == pytest.approx(o["mec"], abs=1e-3)
    assert C.equilibrium(M, 15.0)["lnV"] < e["lnV"] < 0
    assert np.allclose(C.bpr_time([0, 1]), [1, 1.15])


def test_counterfactual_ranges_are_ordered():
    R = C.counterfactual(-0.039, -0.019, 0.006, 0.005, 9.0, 15.0, draws=300)
    for k in ("lnV", "dT", "mec", "opt", "eta"):
        assert R[k][0] <= R[k][1] <= R[k][2]
    assert R["lnV"][2] < 0 and R["kept"] > 250


def test_island_study():
    clean = C.island_study(sims=150)
    trend = C.island_study(pretrend=-0.015, sims=150)
    divert = C.island_study(divert=0.5, sims=150)
    assert abs(clean["bias"]) < 0.004
    assert trend["bias"] == pytest.approx(-0.015, abs=0.004) and abs(trend["adjusted"] - trend["truth"]) < 0.004
    assert divert["mean"] < clean["mean"]                                   # diversion overstates the effect
