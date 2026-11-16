"""Psyche's brain data (Part 49): group maps, thresholds, decoding, geometry, populations, sample sizes."""

import numpy as np
import pytest

from explainer.psychology.psyche import neurodata as N


def test_one_sample_t_matches_scipy():
    from scipy import stats
    rng = np.random.default_rng(1)
    maps = rng.normal(0.3, 1, (15, 6, 6))
    mask = np.ones((6, 6), bool)
    t, df = N.one_sample_t(maps, mask)
    assert df == 14
    assert t[2, 3] == pytest.approx(stats.ttest_1samp(maps[:, 2, 3], 0).statistic)


def test_fixed_effects_inflate():
    r = N.fixed_vs_random(reps=40, seed=2)
    assert r["fixed"] > 20 * r["random"]
    assert r["random"] < 0.004


def test_sign_flip_null_is_symmetric():
    rng = np.random.default_rng(3)
    maps = rng.normal(size=(12, 10, 10))
    mask = np.ones((10, 10), bool)
    mt, mc = N.sign_flip_null(maps, mask, perms=60, primary_t=2.0, seed=3)
    assert len(mt) == 60 and np.all(mt > 0) and np.all(mc >= 0)


def test_leaky_decoding_reads_noise():
    d = N.decoding(trials=30, voxels=400, reps=15, seed=4)
    assert abs(d["nested"] - 0.5) < 0.08
    assert d["leaky"] > 0.75


def test_rsa_and_ceiling():
    r = N.rsa(n_subj=6, seed=5)
    assert r["r_category"] > r["r_size"] > 0
    assert r["ceiling_high"] >= r["ceiling_low"] > r["r_category"]


def test_erp_double_dip():
    e = N.erp_windows(reps=300, seed=6)
    assert e["a_priori"] < 0.1 and e["orthogonal"] < 0.1
    assert e["double_dip"] > 0.25


def test_population_vector_improves():
    p = N.population_vector_error(ns=(4, 64, 256), trials=300, seed=7)
    assert p["error_deg"][0] > p["error_deg"][1] > p["error_deg"][2]


def test_wolpaw():
    assert N.wolpaw_itr(2, 1.0, 60) == pytest.approx(1.0)
    assert N.wolpaw_itr(4, 0.25, 1.0) == pytest.approx(0.0, abs=1e-9)


def test_global_signal_regression_makes_anticorrelations():
    g = N.global_signal(seed=8)
    assert g["between_raw"] > 0 > g["between_gsr"]


def test_bwas_inflation():
    b = N.bwas(true_r=0.1, ns=(25, 2000), studies=3000, seed=9)
    assert b["reported"][0] > 0.35
    assert abs(b["reported"][1] - 0.1) < 0.03
    assert N.attenuated(0.2, 0.4, 0.8) == pytest.approx(0.2 * np.sqrt(0.32))
