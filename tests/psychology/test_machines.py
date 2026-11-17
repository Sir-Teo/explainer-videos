"""Psyche's machine-psychology bench (Part 60)."""

import numpy as np

from explainer.psychology.psyche import machines as M


def test_contamination_memorizer_falls_to_chance():
    runs = [M.contamination(seed=s) for s in range(10)]
    mem = np.mean([r["memorizer"] for r in runs], 0)
    rea = np.mean([r["reasoner"] for r in runs], 0)
    assert mem[0] > rea[0] and mem[1] < rea[1]
    assert abs(mem[1] - 0.25) < 0.04
    assert abs(mem[0] - (0.8 + 0.2 * 0.25)) < 0.04


def test_one_model_interval_is_too_narrow():
    p = M.prompt_sample(n_models=1, seed=1)
    naive = p["naive_ci"][1] - p["naive_ci"][0]
    honest = p["honest_ci"][1] - p["honest_ci"][0]
    assert honest > 10 * naive


def test_benchmark_information_concentrates():
    b = M.benchmark_irt(seed=2, boot=100)
    assert b["useful_share_info"] > 0.35
    assert np.corrcoef(b["theta"], b["accuracy"])[0, 1] > 0.9
    assert 0 <= b["top_stable"] <= 1


def test_items_to_separate_formula():
    s = M.items_to_separate(delta_acc=0.03, acc=0.7, paired_corr=0.5)
    z = 1.959963984540054 + 0.8416212335729143
    assert abs(s["independent"] - 2 * 0.21 * z ** 2 / 0.03 ** 2) < 1e-6
    assert abs(s["paired"] / s["independent"] - 0.5) < 1e-12


def test_silicon_matches_mean_but_not_spread():
    s = M.silicon(seed=3)
    assert abs(s["human_mean"] - s["silicon_mean"]) < 0.15
    assert s["silicon_sd"] < 0.6 * s["human_sd"]
    assert abs(s["group_error"][-1]) > abs(s["group_error"][0])


def test_reliance_line_and_aversion():
    r = M.reliance(aid_acc=0.8, human_acc=0.7)
    assert abs(r["accuracy"][len(r["shares"]) // 2] - 0.75) < 1e-12
    a = M.aversion(seed=4)
    assert a["reliance"][-1] < a["reliance"][0]
    assert a["accuracy"][-5:].mean() < a["best"]


def test_specification_curve():
    sc = M.specification_curve(M.screen_data(n=4000, seed=5))
    assert len(sc["beta"]) == 288
    assert np.all(np.diff(sc["beta"]) >= 0)
    assert sc["median_beta"] < 0 and sc["median_r2"] < 0.05
