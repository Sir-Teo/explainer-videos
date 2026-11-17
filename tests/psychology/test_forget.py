"""Psyche's memory module, Part 21: forgetting laws and Jost's law, the averaging artefact, interference,
consolidation, complementary learning systems, spacing, the bifurcation model, category adjustment, DRM by global
matching, line-ups by signal detection, half-life regression; and the overshadowing replication's open data."""

import numpy as np
import pytest

from explainer.psychology import archive, opendata
from explainer.psychology.psyche import memory as M


def test_power_law_beats_exponential_by_aic():
    s = archive.SAVINGS_REPLICATIONS.data
    t = np.array(s["minutes"], float)
    for who in ("ebbinghaus", "mack", "seitz", "dros"):
        a = {law: M.fit_law(law, t, s[who])["aic"] for law in M.LAWS}
        assert a["power"] < a["exponential"], who


def test_gamma_mixture_of_exponentials_is_a_power_function():
    rng = np.random.default_rng(0)
    rates = rng.gamma(1.5, 0.4, 200_000)
    t = np.array([0.5, 2.0, 10.0, 30.0])
    mc = np.exp(-np.outer(rates, t)).mean(0)
    assert np.allclose(mc, M.gamma_mixture(t, 1.5, 0.4), rtol=0.01)


def test_jost_older_memory_lasts_under_power_not_exponential():
    h = np.linspace(0, 10000, 11)
    py, po = M.jost("power", (0.6, 0.15), 60.0, 2880.0, h)
    ey, eo = M.jost("exponential", (0.6, 3000.0), 60.0, 2880.0, h)
    assert py[0] == pytest.approx(po[0])
    assert np.all(po[1:] > py[1:])
    assert np.allclose(ey, eo)


def test_interference_grows_with_cue_overlap():
    lo = np.mean([M.associator_interference(overlap=0.0, rng=np.random.default_rng(k))["both"] for k in range(10)])
    hi = np.mean([M.associator_interference(overlap=1.0, rng=np.random.default_rng(k))["both"] for k in range(10)])
    first = M.associator_interference(rng=np.random.default_rng(0))["first"]
    assert first > lo > hi


def test_two_store_gives_ribots_gradient():
    age = np.array([0.0, 1.0, 10.0, 50.0, 200.0])
    intact, lesion = M.two_store(age), M.two_store(age, lesion=True)
    assert lesion[0] == 0.0 and intact[0] == 1.0
    assert np.all(intact >= lesion)
    spared = lesion / intact
    assert np.all(np.diff(spared) > 0)  # the older the memory, the more of it survives the lesion


def test_penguin_focused_learning_damages_old_knowledge():
    r = M.penguin_experiment(epochs_base=2000, epochs_new=300)
    assert r["focused"]["robin_can"]["fly"] < r["interleaved"]["robin_can"]["fly"] - 0.2
    assert r["focused"]["old"][-1] > r["interleaved"]["old"][-1]
    assert r["focused"]["new"][-1] < r["focused"]["new"][0]


def test_spacing_ridge_ratio_falls_with_retention():
    gaps = np.unique(np.r_[np.linspace(0, 2, 9), np.geomspace(2, 120, 40)])
    ri = np.array([7.0, 35.0, 70.0, 350.0])
    R = M.spacing_ridge(gaps, ri, c=1.0, a=0.1)
    best = gaps[R.argmax(1)]
    assert np.all(np.diff(best) > 0)
    assert np.all(np.diff(best / ri) < 0)


def test_bifurcation_fit_reproduces_the_crossover():
    r = archive.ROEDIGER_KARPICKE_2006.data
    f = M.fit_bifurcation({"restudy": r["exp1_restudy"], "test": r["exp1_test"]})
    m = f["model"]
    assert m["restudy"][0] > m["test"][0]
    assert m["test"][2] > m["restudy"][2]
    assert f["sse"] < 0.005
    assert 0.6 < m["initial_test"] < 0.9


def test_category_adjustment_trades_bias_for_error():
    pos = np.linspace(5, 85, 9)
    r = M.category_adjustment(pos, 20.0, 22.0)
    assert r["lambda"] == pytest.approx(22.0 ** 2 / (22.0 ** 2 + 20.0 ** 2))
    assert r["bias"][0] > 0 > r["bias"][-1]
    assert r["rmse"].mean() < r["rmse_trace"].mean()


def test_drm_lure_is_accepted_like_a_studied_word():
    d = M.drm_global_matching(lists=100, assoc=0.095, rng=np.random.default_rng(1))
    f = d["familiarity"]
    crit = float(np.quantile(f["studied"], 0.14))
    yes = {k: float(np.mean(v > crit)) for k, v in f.items()}
    assert yes["lure"] > 0.6 and yes["unrelated"] < 0.2


def test_lineup_confidence_accuracy_rises():
    r = M.lineup_cac(1.5, n=50_000)
    assert np.all(np.diff(r["cac"]) > 0)
    assert r["cac"][-1] > 0.9


def test_half_life_regression_recovers_theta():
    s = M.hlr_simulate(learners=300, rng=np.random.default_rng(3))
    f = M.fit_hlr(s["x"], s["gap"], s["recalled"])
    assert f["theta"][0] > 0.5 and f["theta"][1] < -0.2
    assert abs(f["theta"][2] - s["theta"][2]) < 0.5


def test_overshadowing_open_data():
    if not (opendata.available("overshadowing_rrr1") and opendata.available("overshadowing_rrr2")):
        pytest.skip("the replication's workbooks could not be fetched")
    one, two = opendata.overshadowing_rrr(1), opendata.overshadowing_rrr(2)
    assert len(one["labs"]) == 31 and len(two["labs"]) == 22
    pooled = []
    for d in (one, two):
        v, c = d["verbal"], d["control"]
        pooled.append(v[:, 0].sum() / v[:, 1].sum() - c[:, 0].sum() / c[:, 1].sum())
    assert -0.07 < pooled[0] < -0.01 and -0.2 < pooled[1] < -0.12
    o = two["original"]
    assert o[0, 0] / o[0, 1] - o[1, 0] / o[1, 1] == pytest.approx(-0.25)
