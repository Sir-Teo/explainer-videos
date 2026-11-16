"""Psyche over time and within persons (Part 47)."""

import numpy as np

from explainer.psychology.psyche import within as Wi


def test_items_as_fixed_inflates_false_positives():
    r = Wi.false_positive_rates(reps=120, seed=1)
    assert r["F1"] > 0.25 and r["minF"] < 0.09


def test_min_f_close_to_crossed_model():
    d = Wi.priming_study(n_subj=12, n_items=12, seed=3)
    assert abs(Wi.min_f_test(d)["p"] - Wi.crossed_test(d)["p"]) < 0.1


def test_simpson_signs():
    s = Wi.simpson_cloud(seed=2)
    assert s["between"] > 0 > s["within"] and s["pooled"] > 0


def test_blups_beat_own_slopes():
    p = Wi.person_slopes(n_obs=15, seed=4)
    assert p["rmse_blup"] < p["rmse_ols"]


def test_nonergodic_group_describes_no_one():
    r = Wi.nonergodic(n_people=80, T=60, seed=5)
    assert r["cross_mean"] > 0.5 and abs(r["within"].mean()) < 0.15


def test_inertia_bias_matches_kendall():
    r = Wi.inertia_bias(phi=0.4, Ts=(20, 100), reps=600, seed=6)
    assert np.allclose(r["mean_est"], r["kendall"], atol=0.03)


def test_critical_slowing_down():
    d = Wi.double_well(T=3000, seed=4)
    ind = Wi.rolling_indicators(d["x"][: max(350, d["tip"] - 50)], 300)
    assert Wi.kendall_trend(ind["ac"]) > 0.2
