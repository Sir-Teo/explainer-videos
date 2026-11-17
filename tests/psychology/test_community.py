"""Psyche's research community (Part 61)."""

import numpy as np

from explainer.psychology.psyche import community as Cm


def test_cohort_ceiling():
    X, y, r2 = Cm.cohort(n=3000, seed=1)
    assert abs(r2 - (0.25 ** 2 + 0.2 ** 2 + 0.15 ** 2 + 0.12 ** 2 + 0.06)) < 1e-9
    assert abs(np.var(y) - 1) < 0.08


def test_challenge_stays_under_the_ceiling():
    c = Cm.challenge(teams=30, seed=2)
    assert c["best"] < c["ceiling"]
    assert abs(c["best"] - c["baseline"]) < 0.05


def test_many_labs_no_heterogeneity_is_mostly_sampling():
    i2 = [Cm.many_labs(tau=0.0, seed=s)["I2"] for s in range(20)]
    j2 = [Cm.many_labs(tau=0.3, seed=s)["I2"] for s in range(20)]
    assert np.mean(i2) < 0.2 < np.mean(j2)


def test_selection_bias_does_not_shrink():
    s = Cm.selected_sample(ns=(1000, 100000), seed=3)
    assert s["half"][1] < s["half"][0] / 5
    assert s["mean"][1] > 0.15


def test_design_space_and_surrogate():
    cells, eff = Cm.design_space(k=10, seed=4)
    assert cells.shape == (1024, 10)
    r = Cm.integrative(seed=4)
    assert r["held_out_r"] > 0.9
    assert 0 < r["share_negative"] < 0.5


def test_bad_science_rules():
    a = Cm.bad_science(generations=120, seed=5)
    b = Cm.bad_science(generations=120, rule="registered", seed=5)
    assert a["effort"][-1] < 10 and a["fdr"][-10:].mean() > 0.7
    assert b["effort"].min() >= 50 - 1e-9 and b["fdr"][-10:].mean() < a["fdr"][-10:].mean()


def test_adaptive_design_needs_fewer_trials():
    d = Cm.adaptive_design(people=300, trials=60, seed=1)
    assert d["trials_adaptive"] < d["trials_fixed"]
    assert d["share_adaptive"] >= d["share_fixed"]
    # the most informative lag at the start is where the theories part most: the longest
    assert int(np.argmax(d["info0"])) == len(d["lags"]) - 1
    assert d["median_adaptive"][0] == 0.5
