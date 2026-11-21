"""Agora's machines that learn (Part 64): checked against the truths the simulations plant and closed forms."""

import numpy as np
import pytest

from explainer.economics.agora import learn as L


@pytest.fixture(scope="module")
def courts():
    return L.courts(n=20000, trees=40)


def test_forest_beats_charge_weighting_judges(courts):
    P = L.policy_curves(courts)
    assert P["crime_cut"] > 0.05 and P["detain_cut"] > 0.1
    c = np.array(P["crime"])
    assert np.all(np.diff(c) <= 1e-12)                         # detaining more never raises failures


def test_contraction_uses_observed_outcomes_and_naive_flatters(courts):
    K = L.contraction(courts)
    assert all(r["algorithm"] < r["judges"] for r in K["rows"])
    assert K["naive"] < K["truth"]                               # filling in understates the detained's failures
    assert K["s_detained"] > K["s_released"]


def test_targeting_by_effect_beats_risk():
    T = L.targeting(n=8000, trial=2500)
    P = T["per100"]
    assert P["largest effect (truth)"] >= P["largest effect (estimated)"] > P["at random"] > P["highest risk"]


def test_double_ml_centred_where_linear_controls_are_not():
    D = L.dml_study(n=1200, reps=6, K=2)
    assert abs(D["double ML"]["mean"] - 1) < 0.08
    assert D["linear controls"]["mean"] > 1.2


def test_ppi_unbiased_and_narrower():
    X = L.text_measure(reps=150)
    assert abs(X["prediction-powered"]["mean"] - X["share"]) < 0.005
    assert X["prediction-powered"]["width"] < X["hand-labelled"]["width"]
    assert X["classifier"]["coverage"] < 0.2


def test_euler_net_finds_brock_mirman():
    E = L.euler_net(steps=1500)
    assert E["max_err"] < 0.005
    assert E["exact"] == pytest.approx(0.33 * 0.95)


def test_chouldechova_identity_and_unequal_errors():
    F = L.fairness(n=100000)
    for g in "AB":
        assert F[g]["identity"] == pytest.approx(F[g]["fpr"], rel=1e-9)
    assert F["B"]["base"] > F["A"]["base"] and F["B"]["fpr"] > F["A"]["fpr"]


def test_private_signal_erodes_the_algorithms_edge():
    S = L.signal_sweep(signals=(0.0, 1.8), n=15000, trees=30)
    assert S["rows"][0]["crime_cut"] > 0 > S["rows"][1]["crime_cut"]
