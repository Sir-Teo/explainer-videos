"""Psyche at work (Part 51): the laws, the watch, the alarm and the defences behave as the part says."""

import numpy as np
from scipy import stats

from explainer.psychology.psyche import work as Wk


def test_fitts_recovers_its_law():
    f = Wk.fitts_trials(n=2000, seed=1)
    assert abs(f["b"] - 0.15) < 0.01 and abs(f["a"] - 0.05) < 0.03
    assert np.isclose(Wk.fitts_mt(15, 1), 0.05 + 0.15 * 4)


def test_hick_grows_with_log_choices_and_incompatibility_costs():
    n = np.array([1, 3, 7])
    rt = Wk.hick_rt(n)
    assert np.allclose(np.diff(rt), 0.15)  # log2(N + 1) = 1, 2, 3
    assert np.all(Wk.hick_rt(n, compatible=False) > rt)


def test_vigilance_recovers_planted_decline():
    v = Wk.vigilance(watchers=400, seed=2)
    assert np.all(np.abs(v["d"] - v["d_true"]) < 0.15)
    assert np.all(np.abs(v["c"] - v["c_true"]) < 0.12)
    assert v["hit"][0] - v["hit"][-1] > 0.15


def test_prevalence_raises_misses():
    o = Wk.prevalence(prevs=(0.5, 0.1, 0.01))
    p = Wk.prevalence_partial(prevs=(0.5, 0.1, 0.01), shift=0.35)
    assert np.isclose(o["miss"][0], stats.norm.cdf(-1.0))  # unbiased at a half, d = 2
    assert np.all(np.diff(o["miss"]) > 0) and np.all(p["miss"] < o["miss"] + 1e-12)


def test_tlx_weights_and_takeover_irony():
    assert Wk.nasa_tlx([70, 40, 60, 50, 30, 80], [5, 1, 3, 2, 0, 4]) == 66.0
    t = Wk.takeover(seed=3)
    assert np.all(np.diff(t["median_s"]) > 0) and np.all(np.diff(t["within"]) < 0)
    assert np.all(np.diff(t["system_fail"]) < 0)  # the system still gets safer


def test_alarm_ppv_and_best_threshold():
    a = Wk.alarm()
    k = int(np.argmin(np.abs(a["threshold"] - 1.0)))
    ppv = 0.01 * a["hit"][k] / (0.01 * a["hit"][k] + 0.99 * a["fa"][k])
    assert np.isclose(a["ppv"][k], ppv)
    assert 2.3 < a["best"] < 3.1 and a["best_caught"] < 0.3


def test_swiss_cheese_correlation_multiplies_risk():
    p0 = Wk.swiss_cheese(rho=0.0, seed=4)
    assert abs(p0 - 1e-4) < 5e-5
    assert Wk.swiss_cheese(rho=0.6, seed=4) > 50 * p0


def test_fatigue_line_matches_report():
    b = Wk.awake_bac([8, 17, 24])
    assert b[0] == 0 and np.isclose(b[1], 0.05) and np.isclose(b[2], 0.10)


# ---- Part 52 ----
def test_mhp_and_klm_add_up():
    assert Wk.mhp_reaction()["typical"] == 240 and Wk.mhp_reaction("name")["typical"] == 380
    assert np.isclose(Wk.klm_time("MKKKKK"), 1.35 + 5 * 0.28)
    assert Wk.klm_place_m("PBBHKKK") == "MPBBHMKKK"


def test_effective_width_and_throughput():
    r = Wk.fitts_effective(n=4000, distance=256, width=32, sd_scale=0.25, seed=5)
    assert abs(r["We"] - 4.133 * 0.25 * 32) < 1.0
    assert abs(r["errors"] - 2 * stats.norm.sf(2.0)) < 0.01  # half-width = 2 SD
    assert np.isclose(Wk.steering_time(400, 20), 0.2 + 0.08 * 20)


def test_menus_foraging_discovery():
    p, u = Wk.menu_time(), Wk.menu_time(practised=False, read=0.25)
    assert np.argmin(p["time"]) == len(p["time"]) - 1 and u["breadth"][np.argmin(u["time"])] == 8
    lv = Wk.mvt_leave(20.0)
    g = Wk.patch_gain(lv["t"])
    assert np.isclose((10 / 30) * np.exp(-lv["t"] / 30), g / (lv["t"] + 20), rtol=1e-6)
    assert Wk.mvt_leave(5.0)["t"] < lv["t"] < Wk.mvt_leave(60.0)["t"]
    d = Wk.discovery(np.array([5]), a=0.6, b=1.34, seed=1)
    assert np.isclose(d["homog"][0], 1 - (1 - 0.6 / 1.94) ** 5) and d["hetero"][0] < d["homog"][0]


def test_charts_contrast_habits():
    e = [Wk.graphical_error(k, seed=2)["log_err"] for k in ("position", "length", "angle", "area", "volume")]
    assert all(np.diff(e) > 0)
    assert np.isclose(Wk.contrast_ratio((0, 0, 0), (255, 255, 255)), 21.0)
    assert 4.5 < Wk.contrast_ratio((118, 118, 118), (255, 255, 255)) < 4.6
    assert np.isclose(Wk.habit_curve(66) / 100, 0.95)


# ---- Part 53 ----
def test_selection_corrections_recover_truth():
    s = Wk.selection(n=200000, seed=7)
    assert s["r_obs"] < 0.25 < s["r_all_true"]
    assert abs(s["r_both"] - s["r_all_true"]) < 0.04
    assert np.isclose(Wk.case2(0.3, 1.0), 0.3)


def test_taylor_russell_and_utility():
    assert np.isclose(Wk.taylor_russell(0.0, 0.5, 0.2), 0.5, atol=1e-6)
    assert Wk.taylor_russell(0.5, 0.5, 0.1) > Wk.taylor_russell(0.5, 0.5, 0.5) > 0.5
    u = Wk.bcg_utility(0.3, 0.1, 15000.0, n_hired=50, years=4)
    assert abs(u["zbar"] - stats.norm.pdf(stats.norm.ppf(0.9)) / 0.1) < 1e-9
    assert abs(u["gain"] - 50 * 4 * 0.3 * 15000 * u["zbar"]) < 1e-6


def test_impact_and_frontier():
    a = Wk.adverse_impact(0.0, 0.2)
    assert np.isclose(a["impact_ratio"], 1.0) and np.isclose(a["majority"], 0.2)
    assert Wk.adverse_impact(0.8, 0.2)["impact_ratio"] < Wk.adverse_impact(0.4, 0.2)["impact_ratio"] < 0.8
    f = Wk.frontier()
    assert np.isclose(f["validity"][0], 0.42) and np.isclose(f["validity"][-1], 0.31)
    assert f["validity"].max() > 0.42


def test_interviews_rule_beats_impression():
    iv = Wk.interviews(n=40000, seed=3)
    assert iv["structured"] > iv["unstructured"] and iv["mechanical"] > max(iv["holistic"], iv["test"])


# ---- Part 54 ----
def test_capped_activation_is_finite_and_spacing_wins():
    a = Wk.pa_activation_capped([0, 0.01, 0.02, 0.03, 0.04], 60.0)
    assert np.isfinite(a)
    r = {p: Wk.schedule(p, seed=4, base=0.6, n_items=30)["recall"] for p in ("massed", "expanding", "fixed", "model")}
    assert r["massed"] < r["expanding"] < r["fixed"] + 1e-9 and r["model"] >= r["fixed"] - 0.01
    t = Wk.schedule("expanding", seed=4)["first_item_times"]
    assert np.allclose(np.diff(t), [28 / 15, 2 * 28 / 15, 4 * 28 / 15, 8 * 28 / 15])


def test_simple_view():
    assert Wk.simple_view(0.0, 1.0) == 0.0 and np.isclose(Wk.simple_view(0.4, 0.9), 0.36)


# ---- Part 55 ----
def test_default_inertia_inverts():
    d = Wk.default_inertia(0.4, 0.9)
    q, p = d["inertia"], d["prefer"]
    assert np.isclose((1 - q) * p, 0.4) and np.isclose(q + (1 - q) * p, 0.9)


def test_megastudy_curse_and_shrinkage():
    est, tru, shr = [], [], []
    for r in range(120):
        m = Wk.megastudy(seed=r)
        est.append(m["winner_est"]); tru.append(m["winner_true"]); shr.append(m["winner_shrunk"])
    est, tru, shr = map(np.array, (est, tru, shr))
    assert est.mean() > tru.mean() + 0.01
    assert np.mean((shr - tru) ** 2) < np.mean((est - tru) ** 2)


def test_publication_filter_inflates():
    g = Wk.publication_gap(seed=3)
    assert abs(g["units"]["mean_reported"] - g["truth"]) < 0.002
    assert g["academic"]["mean_reported"] > 2.5 * g["truth"]


# ---- Part 56 ----
def test_lineups_roc_and_ratio():
    s = Wk.lineup_roc("simultaneous", n=40000, seed=1)
    q = Wk.lineup_roc("sequential", n=40000, seed=2)
    assert np.all(np.diff(s["hit"]) <= 1e-9) and np.all(np.diff(s["fa"]) <= 1e-9)  # stricter criteria, fewer IDs
    up = float(min(s["fa"].max(), q["fa"].max()))
    assert Wk.partial_auc(s["fa"], s["hit"], up) > Wk.partial_auc(q["fa"], q["hit"], up)
    assert np.isclose(Wk.partial_auc([0, 1], [0, 1], 1.0), 0.5)


def test_feedback_inflates_and_risk_impossibility():
    c = Wk.confidence_feedback(n=60000, seed=3)
    assert np.all(np.diff(c["initial"]) > 0) and c["after"][-1] < c["initial"][-1]
    r = Wk.risk_groups(n=200000, seed=4)
    assert r[0.5]["fpr"] > 2 * r[0.3]["fpr"] and r[0.3]["fnr"] > r[0.5]["fnr"]
    iv = Wk.score_interval(100, 0.91)
    assert np.isclose(iv["sem"], 4.5)


# ---- Part 57 ----
def test_placebo_is_precision_weighted():
    p = Wk.placebo_pain(stimulus=7, expected=(7, 5), sensory_sd=1.0, prior_sd=2.0)
    assert np.isclose(p["weight"], 0.2) and np.isclose(p["placebo"], 6.6)
    b = Wk.placebo_by_noise()
    assert np.all(np.diff(b["effect"]) > 0)


def test_stepped_care_queues():
    hi = Wk.stepped_care("high_only", weeks=60, seed=1)
    st = Wk.stepped_care("stepped", weeks=60, low_slots=100, high_slots=24, seed=1)
    assert hi["mean_wait"] > 10 > st["mean_wait"]
    assert st["recovered_26"] > hi["recovered_26"]
