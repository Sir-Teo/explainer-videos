"""Psyche's drive module (Part 28)."""
import numpy as np
import pytest

from explainer.psychology.psyche import drive as D


def test_thermostat_steady_error_and_integral():
    dist = lambda t: -1.0 if t >= 20 else 0.0  # noqa: E731
    p = D.thermostat(T=120.0, k=0.2, disturbance=dist)
    assert p["x"][-1] == pytest.approx(20.0 - 1.0 / 0.2, abs=1e-3)
    pi = D.thermostat(T=200.0, k=0.2, ki=0.05, disturbance=dist)
    assert pi["x"][-1] == pytest.approx(20.0, abs=0.02)
    free = D.thermostat(T=60.0, dt=0.001, k=0.2, x0=14.0)
    t = free["t"]
    assert np.allclose(free["x"], 20 - 6 * np.exp(-0.2 * (t + 0.001)), atol=2e-3)


def test_body_weight_settles_and_defends():
    s = D.body_weight(days=6000, diet=(0, 6000), cut=500.0)
    assert 80 - s["W"][-1] == pytest.approx(500 / 24, rel=0.01)
    d = D.body_weight(days=6000, diet=(0, 6000), cut=500.0, hunger=60, thrift=25)
    assert 80 - d["W"][-1] == pytest.approx(500 / (24 + 60 + 25), rel=0.01)
    assert D.static_rule(400, (100, 400), 500)[-1] == pytest.approx(80 - 500 * 300 / 7700)


def test_self_stimulation_starves_only_when_current_beats_food():
    low = D.self_stimulation(stim=1, stim_value=0.5, seed=1)
    high = D.self_stimulation(stim=1, stim_value=2.0, seed=1)
    assert low["energy"][-500:].mean() > 0.3
    assert high["energy"][-500:].mean() < 0.05 and high["choice"][-500:].mean() > 0.95
    food = D.self_stimulation(stim=0, seed=1)
    assert food["choice"].sum() == 0


def test_salt_cue_cached_never_turns_positive():
    s = D.salt_cue()
    k = s["switch"]
    assert np.all(s["cached"] <= 1e-12)
    assert s["incentive"][k] > 0 > s["incentive"][k - 1]


def test_self_perception_discounts():
    a = D.self_perception()
    assert 0.5 < a["reward"] < a["no_reward"]
    assert D.self_perception(reward=50.0)["reward"] == pytest.approx(0.5, abs=1e-6)
    assert D.atkinson(0.5) == pytest.approx(0.25) and D.atkinson(0.5, 0.2, 1.0) < 0


def test_evc_and_intensity():
    c = D.evc_curve([0.5, 8.0])
    assert c["u"][0] < 0.05 and c["u"][1] > 1.0
    i = D.intensity([0.5, 1.2, 2.5], reward=4.0)
    assert i["u"][0] < i["u"][1] and i["u"][2] == 0.0


def test_waiting():
    t = np.array([0.0, 5.0, 10.0])
    n, p = D.remaining_wait(t, "normal"), D.remaining_wait(t, "pareto")
    assert np.all(np.diff(n) < 0) and np.all(np.diff(p) > 0)
    assert D.give_up_time("pareto")["best"] < D.give_up_time("normal")["best"]


def test_confounding_and_meta():
    c = D.confounded_delay()
    assert c["controlled"] == pytest.approx(c["truth"], abs=0.02) and c["alone"] > 2 * c["controlled"]
    g, v = D.hedges_g(1.0, 1.0, 50, 0.0, 1.0, 50)
    assert g == pytest.approx(0.992, abs=0.001) and v > 0.04
    rng = np.random.default_rng(0)
    se = rng.uniform(0.1, 0.4, 40)
    gs = 0.3 + se * rng.standard_normal(40)
    r = D.random_effects(gs, se ** 2)
    assert r["lo"] < 0.3 < r["hi"]
    assert D.pet(0.2 + 2 * se, se)["intercept"] == pytest.approx(0.2)


def test_titration_recovers_k():
    for k in (0.002, 0.02, 0.1):
        r = D.discount_titration(k)
        assert r["k_fit"] == pytest.approx(k, rel=0.1)
    assert D.discount_titration(0.002)["auc"] > D.discount_titration(0.1)["auc"]
