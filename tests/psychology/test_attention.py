"""Psyche's attention (Part 18): each model against a closed form or the pattern it is built to show."""

import numpy as np
from scipy.stats import binom, norm

from explainer.psychology.psyche import attention as A


def test_dichotic_matches_the_normal_and_the_filter_blocks_everything():
    att = A.dichotic(attenuation=0.4, noise=0.25, thresholds={"name": 0.55})
    assert np.isclose(att["name"][1], norm.sf((0.55 - 0.4) / 0.25))
    assert np.isclose(att["name"][0], norm.sf((0.55 - 1.0) / 0.25))
    flt = A.dichotic(model="filter")
    assert all(v[1] == 0.0 for v in flt.values())
    # the own name gets through more often than an ordinary word
    d = A.dichotic()
    assert d["own name"][1] > 10 * d["an ordinary word"][1]


def test_load_removes_flanker_interference():
    f = A.flanker_interference(np.arange(7), capacity=4.0, full=60.0)
    assert f[0] == 60.0 and np.all(np.diff(f) <= 0) and np.all(f[4:] == 0)


def test_cue_effects():
    soa = np.array([0, 50, 100, 200, 400, 800, 3000])
    endo = A.cue_effect(soa, "endogenous", gain=30)
    assert endo[0] == 0 and np.all(np.diff(endo) > 0) and abs(endo[-1] - 60) < 0.1
    exo = A.cue_effect(soa, "exogenous", gain=30)
    assert exo[1] > 20 and exo[-1] < -10  # facilitation early, inhibition of return late
    r = A.posner_rts(400, rng=np.random.default_rng(1))
    assert r["valid"].mean() < r["neutral"].mean() < r["invalid"].mean()


def test_search_slopes_flat_shallow_and_two_to_one():
    rng = np.random.default_rng(2)
    feat = A.search_slopes("feature", n=120, rng=rng)
    conj = A.search_slopes("conjunction", n=120, rng=rng)
    spat = A.search_slopes("spatial", n=120, rng=rng)
    assert abs(feat["slopes"][0]) < 3 and abs(feat["slopes"][1]) < 6
    assert 4 < conj["slopes"][0] < spat["slopes"][0]
    ratio = spat["slopes"][1] / spat["slopes"][0]
    assert 1.6 < ratio < 2.4
    # misses stay near Φ(−z) and false alarms never happen
    assert np.all(spat["present"][1] < 0.15) and np.all(spat["absent"][1] == 0)


def test_prevalence_effect():
    m = A.prevalence_misses(np.array([0.01, 0.1, 0.5]), d_prime=2.95)
    assert np.isclose(m[-1], norm.cdf(-2.95 / 2))
    assert m[0] > m[1] > m[2] and m[0] > 3 * m[2]


def test_saliency_map_and_scan_path_find_the_odd_bar():
    f = np.zeros((60, 60))
    f[10:50:8, 10:50:8] = 1.0  # a field of bright dots in one channel
    g = np.zeros((60, 60))
    g[42, 18] = 1.0  # one dot that differs in a second channel
    sal = A.saliency_map({"luminance": f + g, "colour": g})
    i, j = np.unravel_index(np.argmax(sal), sal.shape)
    assert abs(i - 42) <= 2 and abs(j - 18) <= 2
    path = A.scan_path(sal, k=4, ior_radius=5)
    assert path[0] == (i, j)
    for a in range(4):
        for b in range(a):
            assert np.hypot(path[a][0] - path[b][0], path[a][1] - path[b][1]) > 5


def test_flicker():
    w = np.ones(30)
    w[0] = 8.0
    ci = np.mean([A.flicker(w, 0, rng=np.random.default_rng(s)) for s in range(200)])
    mi = np.mean([A.flicker(w, 5, rng=np.random.default_rng(s)) for s in range(200)])
    assert ci < mi and A.flicker(w, 5, transient=True) == 1


def test_attentional_blink_and_lag1_sparing():
    p = A.attentional_blink([1, 2, 3, 8], rng=np.random.default_rng(3))
    assert p[1] < p[0] and p[1] < p[3] and p[3] > 0.95


def test_prp_slope_minus_one_then_flat():
    r = A.prp(np.array([0, 25, 1000, 1500]), cv=0.05, rng=np.random.default_rng(4))
    assert abs((r["rt2"][1] - r["rt2"][0]) / 25 + 1) < 0.1
    assert abs(r["rt2"][2] - r["rt2"][3]) < 1.0
    assert abs(r["rt2"][3] - 330) < 5  # A2 + B2 + C2


def test_diffusion_matches_closed_forms():
    v, a = 1.2, 1.5
    rt, ok = A.diffusion_rt(np.full(6000, v), bound=a, ter=0.0, scale=1000.0, dt=0.5, rng=np.random.default_rng(5))
    p_exact = 1 / (1 + np.exp(-2 * v * a))
    assert abs(ok.mean() - p_exact) < 0.02
    mdt = a / v * np.tanh(a * v) * 1000
    assert abs(rt.mean() / mdt - 1) < 0.04


def test_stroop_asymmetries_and_the_sequence_effect():
    rng = np.random.default_rng(6)
    m = {c: A.stroop(c, rng=rng)[0].mean() for c in ("congruent", "neutral", "incongruent")}
    assert m["incongruent"] - m["neutral"] > m["neutral"] - m["congruent"] > 0
    w = {c: A.stroop(c, "word", rng=rng)[0].mean() for c in ("congruent", "incongruent")}
    assert w["incongruent"] - w["congruent"] < 0.25 * (m["incongruent"] - m["congruent"])
    rt, ic = A.stroop("incongruent", rng=rng)
    rc, cc = A.stroop("congruent", rng=rng)
    x, y = A.delta_plot(rc, rt)
    assert y[-1] > y[0] > 0  # interference grows over the RT distribution
    conds = np.random.default_rng(7).choice(["congruent", "incongruent"], 4000)
    rts, ok, _ = A.stroop_sequence(conds, rng=np.random.default_rng(8))
    prev = np.concatenate([[""], conds[:-1]])
    eff = {}
    for pc in ("congruent", "incongruent"):
        sel = (prev == pc) & ok
        eff[pc] = rts[sel & (conds == "incongruent")].mean() - rts[sel & (conds == "congruent")].mean()
    assert eff["incongruent"] < eff["congruent"]


def test_switch_cost_falls_to_a_residual():
    s = A.switch_cost(np.array([0, 150, 600, 5000]))
    assert s[0] == 200 and np.all(np.diff(s) < 0) and abs(s[-1] - 80) < 0.5


def test_normalization_model_contrast_versus_response_gain():
    c = np.logspace(-2, 0, 15)
    small = A.gain_type(c, A.normalization_crf(c, 1, 8, False), A.normalization_crf(c, 1, 8, True))
    large = A.gain_type(c, A.normalization_crf(c, 8, 1, False), A.normalization_crf(c, 8, 1, True))
    assert small["c50_ratio"] < 0.85 and abs(small["rmax_ratio"] - 1) < 0.1
    assert large["rmax_ratio"] > 1.3


def test_tva_whole_report_matches_the_binomial():
    n_items, C, t0, K, e = 6, 30.0, 20.0, 4, 120.0
    got = A.tva_whole_report([e, 5.0, 5000.0], n_items, C, t0, K, n=20000, rng=np.random.default_rng(9))
    p = 1 - np.exp(-C / n_items / 1000 * (e - t0))
    exact = sum(min(k, K) * binom.pmf(k, n_items, p) for k in range(n_items + 1))
    assert abs(got[0] - exact) < 0.03
    assert got[1] == 0.0 and abs(got[2] - K) < 1e-9


def test_vigilance_decrement():
    v = A.vigilance(np.array([0, 30, 60, 120]))
    assert np.all(np.diff(v["hits"]) < 0) and np.all(np.diff(v["fas"]) <= 0)


def test_notice_probability_rises_with_similarity():
    p = A.notice_probability(np.array([0.1, 0.5, 0.9]))
    assert p[0] < p[1] < p[2] and abs(p[1] - 0.5) < 1e-9


def test_battery_tasks_three_and_four():
    from explainer.psychology import battery

    t = battery.run("stroop", {}, 300, seed=1)
    assert len(t) == 300 and set(t.condition) == {"congruent", "neutral", "incongruent"}
    assert t.mean_rt("incongruent") > t.mean_rt("neutral") > t.mean_rt("congruent")
    s = battery.run("search", {}, 320, seed=2)
    assert set(s.condition) == {"feature", "conjunction"}
    big = s.where("conjunction") & (s.extra["set_size"] == 32) & s.extra["present"] & s.correct
    small = s.where("conjunction") & (s.extra["set_size"] == 4) & s.extra["present"] & s.correct
    assert s.rt[big].mean() > s.rt[small].mean()
