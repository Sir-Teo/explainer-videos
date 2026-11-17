"""Psyche's workspace module (Part 27)."""
import numpy as np
import pytest
from scipy.stats import norm

from explainer.psychology.psyche import workspace as W


def test_masking_against_simulation():
    rng = np.random.default_rng(1)
    d, c = 1.4, 1.2
    x = d / 2 + rng.standard_normal(400_000)
    seen = np.abs(x) > c
    r = W.masking(d, c)
    assert r["p_seen"] == pytest.approx(seen.mean(), abs=0.003)
    assert r["acc_unseen"] == pytest.approx((x[~seen] > 0).mean(), abs=0.004)
    assert r["acc"] == pytest.approx(norm.cdf(d / 2))


def test_unseen_above_chance_and_criterion():
    assert W.masking(0.0, 1.5)["acc_unseen"] == pytest.approx(0.5)
    lax, strict = W.masking(1.5, 0.8)["acc_unseen"], W.masking(1.5, 2.5)["acc_unseen"]
    assert 0.5 < lax < strict < W.masking(1.5, 2.5)["acc"] + 1e-9
    v = W.visibility_curve([0, 20, 50, 100])
    assert np.all(np.diff(v["p_seen"]) > 0) and np.all(np.diff(v["acc"]) > 0)


def test_rivalry_alternates_with_skewed_durations():
    r = W.rivalry(T=200.0, seed=3)
    d = W.dominance_durations(r["u"], r["dt"])
    assert len(d["all"]) > 30
    assert 1.5 < d["shape"] < 10  # gamma-like, neither exponential nor clockwork
    assert abs(d["mean1"] - d["mean2"]) < 1.5


def test_ignition_is_all_or_none():
    g = W.ignition([0.3, 0.85, 1.4], n_trials=300, seed=1)
    assert g["p_ignite"][0] < 0.05 and g["p_ignite"][2] > 0.95
    late = g["late"][1]
    assert np.mean((late > 0.2) & (late < 0.6)) < 0.1  # bimodal: few trials halfway
    early = g["early"].mean(1)
    assert early[0] < early[1] < early[2]


def test_phi_small_networks():
    assert W.phi(W.network("pairs", 6))["phi"] == pytest.approx(0.0)
    assert W.phi(W.network("ring_copy", 6))["phi"] == pytest.approx(2.0)
    assert W.ei(W.network("ring_copy", 4), (0, 1), (2, 3)) == pytest.approx(1.0)
    assert sum(1 for _ in W.bipartitions(6)) == 31


def test_schurger_ramp():
    s = W.schurger(T=600.0, seed=2)
    assert np.all(s["x"] < 0.298 + 1e-12)
    b = W.back_average(s["x"], s["hits"], s["dt"], 2.0)
    assert b["mean"][-1] > b["mean"][0] + 0.05
    assert np.all(np.diff(b["mean"][::200]) > 0)


def test_lz_and_pci():
    assert W.lz76([0] * 50) <= 2
    rng = np.random.default_rng(0)
    assert W.lz76(rng.integers(0, 2, 2000)) > W.lz76(np.tile([0, 1], 1000))
    assert W.pci(W.responses("wake")) > 0.31 > W.pci(W.responses("sleep"))
    assert W.pci(np.zeros((5, 10))) == 0.0
