"""Psyche's personality module (Part 33)."""

import numpy as np

from explainer.psychology.psyche import personality as P


def test_scoring_reverses_keys():
    items = ["A1", "A2", "C4", "C1"]
    X = np.array([[6, 1, 6, 1], [1, 6, 1, 6]], float)
    s = P.score(X, items)
    assert np.allclose(s["A"], [1, 6]) and np.allclose(s["C"], [1, 6])


def test_parallel_analysis_finds_planted_factors():
    rng = np.random.default_rng(0)
    F = rng.normal(size=(2000, 3))
    L = np.kron(np.eye(3), np.ones((1, 4))) * 0.7
    X = F @ L + rng.normal(size=(2000, 12)) * 0.7
    assert P.parallel(X, n_iter=20)["keep"] == 3


def test_aggregation_follows_spearman_brown():
    a = P.aggregate_curve(P.act_world(n=3000, situations=40, seed=1), ks=(1, 4, 16))
    assert abs(a["single"] - 1 / (1 + 0.36 + 1.96)) < 0.04
    assert np.allclose(a["observed"], a["spearman_brown"], atol=0.03)
    assert a["same_situation"] > a["single"]


def test_type_agreement_matches_the_arcsine_law():
    t = P.type_agreement(0.8, dims=4, n=100_000)
    assert abs(t["one"] - t["one_sim"]) < 0.005 and abs(t["all"] - t["all_sim"]) < 0.005
    assert np.isclose(P.dichotomy_loss(), np.sqrt(2 / np.pi))
    rng = np.random.default_rng(2)
    x = rng.normal(size=200_000)
    assert abs(np.corrcoef(x, np.sign(x))[0, 1] - P.dichotomy_loss()) < 0.005


def test_mahalanobis_grows_with_dimensions():
    rng = np.random.default_rng(3)
    p, d = 25, 0.2
    X1 = rng.normal(size=(20000, p))
    X2 = rng.normal(size=(20000, p)) + d
    m = P.mahalanobis(X1, X2)
    assert abs(m["D"] - d * np.sqrt(p)) < 0.05
    assert abs(P.overlap_d(1.0) - 2 * 0.3085375) < 1e-6
    assert P.besd(0.2) == (0.6, 0.4)


def test_likes_and_faking():
    w = P.likes_world(n=3000, likes=600, seed=4)
    acc = P.likes_accuracy(w, [20, 600], orders=2)
    assert acc["r"][1] > acc["r"][0] > -0.05
    f = P.faking(n=50_000, share=0.3)
    assert f["faker_share_hired"] > f["faker_share_pool"] and f["perf_hired"] <= f["perf_honest"] + 0.02
