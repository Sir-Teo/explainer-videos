"""Psyche's precision-psychiatry bench (Part 59)."""

import numpy as np

from explainer.psychology.psyche import precision as Pr


def test_difference_reliability_formula():
    assert abs(Pr.difference_reliability(15, 120, 60) - 225 / (225 + 480)) < 1e-12
    # Spearman-Brown: nine times the trials take 0.5 to 0.9
    r = 0.5
    sb2 = 1.0
    err = sb2 * (1 - r) / r
    assert abs(sb2 / (sb2 + err / 9) - 0.9) < 1e-12


def test_paradox_large_t_low_reliability():
    p = Pr.paradox(n_people=300, seed=1)
    assert p["t"] > 25
    assert abs(p["retest_r"] - p["expected_r"]) < 0.15
    assert p["retest_r"] < 0.55


def test_design_tradeoff_directions():
    d = Pr.design_tradeoff()
    rel = d["reliability"]
    assert np.all(np.diff(rel, axis=1) > 0)  # more between-person share, more reliable
    assert np.all(np.diff(rel, axis=0) > 0)  # more trials, more reliable
    assert np.all(np.diff(d["group_d"]) < 0)


def test_attenuation():
    assert abs(Pr.attenuated_r(0.5, 0.4, 0.8) - 0.5 * np.sqrt(0.32)) < 1e-12


def test_adjusted_rand():
    a = np.array([0, 0, 1, 1, 2, 2])
    assert Pr.adjusted_rand(a, a) == 1.0
    assert Pr.adjusted_rand(a, np.array([5, 5, 7, 7, 9, 9])) == 1.0
    rng = np.random.default_rng(0)
    x, y = rng.integers(0, 4, 2000), rng.integers(0, 4, 2000)
    assert abs(Pr.adjusted_rand(x, y)) < 0.02


def test_circular_biotypes_differ_but_are_unstable():
    none = Pr.biotypes(structure=0.0, seed=4)
    real = Pr.biotypes(structure=1.5, seed=4)
    assert none["symptom_p"] < 0.2
    assert real["stability_ari"] > none["stability_ari"] + 0.2


def test_logistic_and_auc():
    rng = np.random.default_rng(3)
    X = rng.standard_normal((2000, 2))
    y = (rng.random(2000) < 1 / (1 + np.exp(-(0.5 + X @ [1.0, -2.0])))).astype(float)
    w = Pr.fit_logistic(X, y, ridge=1e-6)
    assert np.allclose(w, [0.5, 1.0, -2.0], atol=0.2)
    s = np.array([0.1, 0.4, 0.35, 0.8])
    assert Pr.auc(s, np.array([0, 0, 1, 1.0])) == 0.75


def test_cross_trial_ordering():
    t = Pr.cross_trial(reps=8, seed=2)
    assert t["apparent"] > t["cv"] > 0.5
    assert t["new_trial"] < t["apparent"]


def test_interaction_needs_four_times():
    s = Pr.pai_sample(0.3)
    assert abs(s["interaction_total"] / s["main_total"] - 4) < 1e-12
    assert 330 < s["main_total"] < 360
