"""The capstone pipeline (Part 43): power, small telescopes, the replication Bayes factor, pooling, the frozen plan."""

import numpy as np
from scipy import stats

from explainer.psychology import capstone as C


def test_power_matches_the_normal_approximation_for_large_samples():
    approx = stats.norm.sf(1.96 - 0.3 * np.sqrt(500 / 2))
    assert abs(C.power2(0.3, 500, 500) - approx) < 0.01
    assert abs(C.power2(0.5, 64, 64) - 0.80) < 0.01


def test_d33_has_a_third_power():
    d = C.d33(20, 20)
    assert abs(C.power2(d, 20, 20) - 1 / 3) < 1e-6 and 0.45 < d < 0.55


def test_n_per_group_reaches_the_target():
    n = C.n_per_group(0.5, 0.8)
    assert C.power2(0.5, n, n) >= 0.8 > C.power2(0.5, n - 1, n - 1)


def test_replication_bf_direction():
    assert C.replication_bf(0.6, 0.2, 0.55, 0.05) > 10
    assert C.replication_bf(0.6, 0.2, 0.0, 0.05) < 0.1


def test_pool_fixed_and_random():
    r = C.pool([0.4, 0.6, 0.2], [0.04, 0.02, 0.05], "FE")
    assert abs(r["est"] - 44 / 95) < 1e-12 and r["tau2"] == 0
    assert C.pool([0.4, 0.6, 0.2], [0.04, 0.02, 0.05], "DL")["tau2"] > 0


def test_the_frozen_analysis_has_its_planned_size_and_power():
    plan = C.Plan("t", "g", 1, 0.6, 0.3, 0.1)
    res = C.dry_run(plan, 20, 50, effects=(0.0, 0.3), reps=100)
    assert res[0.0] < 0.12 and res[0.3] > 0.9


def test_verdict_counts_criteria():
    plan = C.Plan("t", "rd", -1, -0.25, 0.1, 0.05)
    r = {"est": -0.16, "se": 0.02, "lo": -0.20, "hi": -0.12, "p_one": 1e-9}
    v = C.verdict(r, plan, 0.16)
    assert v["significant"] and not v["original_inside"] and v["not_below_d33"] and v["n_met"] == 2
