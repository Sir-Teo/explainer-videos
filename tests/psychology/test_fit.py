"""Psyche's fit module (Part 48): averages, likelihoods, recovery and checks."""

import numpy as np
import pytest

from explainer.psychology.psyche import fit as F


def test_jump_average_matches_formula():
    j = F.jump_learners(n=4000, seed=1)
    assert set(np.unique(j["each"])) <= {0.1, 0.95}
    assert np.max(np.abs(j["mean"] - j["smooth"])) < 0.03


def test_power_law_is_an_average():
    p = F.practice_curves(n=40, trials=150, seed=2)
    assert p["exp_wins_individual"] > 0.7
    assert p["avg_rss_pow"] < p["avg_rss_exp"]


def test_random_model_likelihood_is_exact():
    C = np.array([0, 1, 1, 0, 1])
    R = np.zeros(5)
    assert F.loglik("random", (0.5,), C, R) == pytest.approx(5 * np.log(0.5))


def test_loglik_is_a_probability_sum():
    C, R = F.simulate("q_persev", (0.4, 4.0, 1.0), trials=120, seed=3)
    for m, p in [("random", (0.3,)), ("wsls", (0.2,)), ("q", (0.4, 4.0)), ("q_persev", (0.4, 4.0, 1.0))]:
        ll = F.loglik(m, p, C, R)
        assert np.isfinite(ll) and ll < 0


def test_fit_recovers_a_q_learner():
    C, R = F.simulate("q", (0.3, 6.0), trials=600, seed=4)
    f = F.fit("q", C, R)
    assert abs(f["params"][0] - 0.3) < 0.15 and abs(f["params"][1] - 6.0) < 2.5
    assert f["bic"] < F.fit("random", C, R)["bic"]


def test_bic_formula():
    C, R = F.simulate("q", (0.3, 5.0), trials=200, seed=5)
    f = F.fit("q", C, R)
    assert f["bic"] == pytest.approx(-2 * f["ll"] + 2 * np.log(200))
    assert f["aic"] == pytest.approx(-2 * f["ll"] + 4)


def test_stay_after_and_ppc():
    C = np.array([0, 0, 1, 1, 1, 0])
    R = np.array([1, 0, 1, 1, 0, 0])
    s = F.stay_after(C, R)
    assert s["win"] == pytest.approx(1.0) and s["loss"] == pytest.approx(0.0)
    a = F.posterior_predictive("q_persev", (0.3, 5.0, 1.5), "q", n=8, seed=6)
    b = F.posterior_predictive("q_persev", (0.3, 5.0, 1.5), "q_persev", n=8, seed=6)
    assert abs(b["pred"][1] - b["obs"][1]) < abs(a["pred"][1] - a["obs"][1])


def test_group_shrinkage_helps():
    g = F.group_fit(n_people=20, trials=60, seed=7)
    assert g["rmse_eb"] < g["rmse_ml"]
