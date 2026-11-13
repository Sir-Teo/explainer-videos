"""The measurement library (``explainer/psychology/measure.py``) and the Pool's trait block: the estimators
recover what the Pool planted."""

from __future__ import annotations

import math

import numpy as np
import pytest

from explainer.psychology import measure as M
from explainer.psychology import pool as pool_mod

POOL = pool_mod.Pool()
IDS = np.arange(40_000)


def test_the_planted_traits_are_recoverable():
    r = np.corrcoef([POOL.conscientious, POOL.neurotic, POOL.extravert, POOL.grit])
    assert r[0, 1] == pytest.approx(-0.25, abs=0.01) and r[0, 2] == pytest.approx(0.10, abs=0.01)
    assert r[0, 3] == pytest.approx(pool_mod.GRIT_R, abs=0.005)
    assert POOL.conflict.mean() == pytest.approx(60, abs=0.5) and POOL.conflict.std() == pytest.approx(17, abs=0.3)
    assert (POOL.conflict > 0).all()
    for m in pool_mod.METHODS:
        assert abs(np.corrcoef(POOL.style[m], POOL.conscientious)[0, 1]) < 0.02


def test_the_part_1_and_part_2_people_are_unchanged():
    small = pool_mod.Pool(n=1000)
    assert small.age[:3].tolist() == pool_mod.Pool(n=1000).age[:3].tolist()
    assert POOL.keen.std() == pytest.approx(1.0, abs=0.02)


def test_scale_types_and_recodings():
    rng = np.random.default_rng(1)
    v = np.arange(1, 6.0)
    assert (np.diff(M.recode("ordinal", v, rng)) > 0).all()
    assert sorted(M.recode("nominal", v, rng)) == list(v)
    shifted = ([0.3, 0.3, 0.2, 0.1, 0.1], [0.1, 0.1, 0.2, 0.3, 0.3])  # one group higher throughout
    crossed = ([0.0, 0.2, 0.6, 0.2, 0.0], [0.3, 0.1, 0.1, 0.1, 0.4])  # one in the middle, one at the ends
    assert not M.order_can_flip(*shifted) and M.flip_share(*shifted, n=500, rng=rng) == 0
    assert M.order_can_flip(*crossed) and 0 < M.flip_share(*crossed, n=2000, rng=rng) < 1


def test_reliability_three_ways_agree():
    a = POOL.scale("conscientious", IDS, 10, seed=1, points=None)
    b = POOL.scale("conscientious", IDS, 10, seed=2, points=None)
    truth = M.reliability(POOL.conscientious[IDS], a)
    exact = M.spearman_brown(0.36, 10)  # one item of loading 0.6 has reliability 0.36
    assert truth == pytest.approx(exact, abs=0.01)
    assert np.corrcoef(a, b)[0, 1] == pytest.approx(exact, abs=0.01)  # parallel forms
    items = POOL.items("conscientious", IDS, 10, seed=1, points=None)
    assert M.cronbach_alpha(items) == pytest.approx(exact, abs=0.01)
    assert M.split_half(items) == pytest.approx(exact, abs=0.015)
    assert M.length_for(0.36, exact) == pytest.approx(10)
    assert M.sem(10.0, 0.84) == pytest.approx(4.0)


def test_alpha_is_not_unidimensionality():
    two = np.hstack([POOL.items("conscientious", IDS, 10, seed=3, points=None),
                     POOL.items("extravert", IDS, 10, seed=4, points=None)])
    assert M.cronbach_alpha(two) > 0.7  # a respectable alpha for a test that measures two things


def test_attenuation_and_its_correction():
    x = POOL.scale("conscientious", IDS, 6, seed=5, points=None)
    y = POOL.scale("grit", IDS, 6, seed=6, points=None)
    rel = M.spearman_brown(0.36, 6)
    observed = np.corrcoef(x, y)[0, 1]
    assert observed == pytest.approx(pool_mod.GRIT_R * rel, abs=0.01)
    assert M.disattenuate(observed, rel, rel) == pytest.approx(pool_mod.GRIT_R, abs=0.015)


def test_kappa_and_icc():
    rng = np.random.default_rng(2)
    truth = rng.random(20_000) < 0.1
    a = np.where(rng.random(20_000) < 0.85, truth, ~truth)
    b = np.where(rng.random(20_000) < 0.85, truth, ~truth)
    assert M.agreement(a, b) > 0.7 and M.cohen_kappa(a, b) < 0.35  # they mostly agree that it is absent
    assert M.cohen_kappa(a, a) == pytest.approx(1.0)
    s1, s2 = POOL.conflict_task(IDS, 120, 1), POOL.conflict_task(IDS, 120, 2)
    expected = 17.0 ** 2 / (17.0 ** 2 + 2 * 100.0 ** 2 / 120)
    assert M.icc(s1["cost"], s2["cost"]) == pytest.approx(expected, abs=0.02)
    assert M.icc(s1["congruent"], s2["congruent"]) > 0.9
    assert M.icc(s1["cost"], s2["cost"] + 30) < M.icc(s1["cost"], s2["cost"])  # absolute agreement


def test_mtmm_shows_planted_method_variance():
    scores = {(t, m): POOL.scale(t, IDS, 8, seed=10 * i + j, method=m, method_loading=0.45, points=None)
              for i, t in enumerate(pool_mod.TRAITS) for j, m in enumerate(pool_mod.METHODS)}
    out = M.mtmm(scores)
    assert out["r"].shape == (9, 9) and len(out["labels"]) == 9
    assert out["convergent"] > out["same_method"] > out["neither"]
    clean = {(t, m): POOL.scale(t, IDS, 8, seed=10 * i + j, points=None)
             for i, t in enumerate(pool_mod.TRAITS) for j, m in enumerate(pool_mod.METHODS)}
    assert M.mtmm(clean)["same_method"] == pytest.approx(M.mtmm(clean)["neither"], abs=0.02)


def test_a_network_and_a_factor_can_imply_the_same_matrix():
    r = M.mutualism(6, 0.12)
    assert np.allclose(np.diag(r), 1) and np.ptp(r[~np.eye(6, dtype=bool)]) < 1e-12
    fit = M.one_factor(r)
    assert fit["rms"] < 1e-6 and np.allclose(fit["loadings"], math.sqrt(r[0, 1]), atol=1e-4)
    with pytest.raises(ValueError):
        M.mutualism(6, 0.25)


def test_cancellation_conditions():
    additive = np.add.outer([0.0, 1.0, 2.5], [0.0, 0.7, 3.0])
    assert M.independence(additive) and M.double_cancellation(np.exp(additive))  # any increasing function of a sum
    crossing = np.array([[1.0, 2.0, 3.0], [2.0, 3.0, 1.0], [3.0, 1.0, 2.0]])
    assert not M.independence(crossing)
    # ordered the same way in every row and column, and still no additive scale: double cancellation fails
    bad = np.array([[1.0, 2.0, 6.0], [3.0, 5.0, 7.0], [4.0, 8.0, 9.0]])
    assert M.independence(bad) and not M.double_cancellation(bad)
