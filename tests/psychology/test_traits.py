"""Psyche's traits module (Part 32)."""

import numpy as np

from explainer.psychology import archive
from explainer.psychology.psyche import traits as T


def test_spearman_matrix_and_one_factor():
    R = np.array(archive.SPEARMAN_1904.data["R"])
    means = (R[:4, :4].sum(1) - 1) / 3
    assert np.allclose(np.round(means, 2), archive.SPEARMAN_1904.data["averages"], atol=0.005)
    f = T.one_factor(R)
    assert np.all(f["loadings"] > 0.5) and f["rmsr"] < 0.05
    # one exact factor: tetrads vanish
    lam = np.array([0.9, 0.8, 0.7, 0.6, 0.5])
    exact = np.outer(lam, lam)
    np.fill_diagonal(exact, 1.0)
    assert np.max(np.abs(T.tetrads(exact))) < 1e-12


def test_three_worlds_all_show_a_positive_manifold():
    for X in (T.common_cause(n=1500), T.sampling(n=1500), T.mutualism(n=1500)):
        R = T.corr(X)
        off = R[~np.eye(len(R), dtype=bool)]
        assert off.min() > 0.1
        assert T.one_factor(R)["rmsr"] < 0.05


def test_training_separates_the_worlds():
    c = T.train_one("common", n=1500)["change"]
    m = T.train_one("mutualism", n=1500)["change"]
    assert abs(c[1:]).max() < 1e-9
    assert m[1:].min() > 0.02


def test_scales_and_corrections():
    assert np.isclose(T.ratio_iq(12, 10), 120)
    assert np.isclose(T.deviation_iq(30, 20, 10), 115)
    s = T.sem_interval(100, 0.91)
    assert np.isclose(s["sem"], 4.5)
    assert T.restriction_corrected(0.3, 0.6) > 0.3
    assert np.isclose(T.restriction_corrected(0.3, 1.0), 0.3)
    o = T.overlap(1.0)
    assert np.isclose(o["above_mean"], 0.158655, atol=1e-5)


def test_matrix_items_and_solver():
    rng = np.random.default_rng(0)
    for k in range(5):
        it = T.matrix_item(rng, k)
        assert sum(r != "constant" for r in it["rules"].values()) == k
        assert np.array_equal(it["options"][it["correct"]], it["answer"])
        assert T.solve(it, 4, rng) == it["correct"]
    assert T.solver_accuracy(2, 1) == 1.0
    assert T.solver_accuracy(1, 4, trials=200) < 0.5


def test_invariance_patterns():
    a = T.invariance_demo(latent_gap=0.4, bias=0.0)
    assert a["d_tests"].min() > 0.15  # every test moves
    b = T.invariance_demo(latent_gap=0.0, bias=0.6)
    others = np.delete(b["d_tests"], 2)
    assert b["d_tests"][2] > 0.4 and abs(others).max() < 0.1  # only the biased test moves


def test_practice_formulas():
    rng = np.random.default_rng(7)
    true = 72.0
    obs = true + 15 * np.sqrt(0.05) * rng.normal(size=200_000)
    assert abs((obs < 70).mean() - T.below_cut(true)) < 0.005
    assert np.isclose(T.kelley(70, 0.9), 73.0)
    x = rng.normal(size=400_000)
    y = 0.4 * x + np.sqrt(1 - 0.16) * rng.normal(size=x.size)
    top = x > np.quantile(x, 0.8)
    assert abs(y[top].mean() - T.selection_gain(0.4, 0.2)) < 0.01
    lo = rng.normal(size=x.size) - 0.5
    cut = np.quantile(x, 0.7)
    assert abs((lo > cut).mean() / 0.3 - T.impact_ratio(0.5, 0.3)["ratio"]) < 0.01
