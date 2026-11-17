"""Psyche's imaging module against closed forms and its own known answers."""

import math

import numpy as np
import pytest
from scipy import stats

from explainer.psychology.psyche import imaging as I


def rng(seed):
    return np.random.default_rng(seed)


def test_tuning_curve_peaks_at_the_preferred_orientation_and_wraps():
    assert I.tuning_curve(45.0) == pytest.approx(40.0)
    assert I.tuning_curve(135.0) == pytest.approx(2.0, abs=0.01)
    assert I.tuning_curve(45.0 + 180.0) == pytest.approx(I.tuning_curve(45.0))
    counts = I.spike_counts([45.0, 135.0], trials=400, window=0.5, rng=rng(1))
    assert counts[0].mean() == pytest.approx(20.0, rel=0.05) and counts[1].mean() == pytest.approx(1.0, rel=0.2)


def test_aligned_dipoles_add_and_random_ones_grow_as_the_square_root():
    assert I.dipole_sum(10_000, True) == 10_000
    assert I.dipole_sum(10_000, False, rng=rng(2)) == pytest.approx(math.sqrt(10_000 * math.pi) / 2, rel=0.08)


def test_a_silent_source_exists_and_changes_no_electrode():
    L = I.lead_field(I.electrodes(9), I.source_grid(6))
    assert L.shape[1] > L.shape[0]
    v = I.silent_source(L, rng=rng(3))
    assert np.linalg.norm(v) == pytest.approx(1.0) and np.abs(L @ v).max() < 1e-10
    with pytest.raises(ValueError):
        I.silent_source(np.eye(3))


def test_averaging_leaves_the_component_and_shrinks_noise_by_root_n():
    t = np.arange(-100.0, 800.0, 4.0)
    trials = I.erp_trials(1600, t, "n400", noise_sd=20.0, rng=rng(4))
    noise = trials - I.erp_template(t, "n400")
    assert noise.std() == pytest.approx(20.0, rel=1e-6)
    for n in (16, 100):
        left = np.sqrt((noise.reshape(-1, n, len(t)).mean(axis=1) ** 2).mean())
        assert left == pytest.approx(float(I.erp_noise(20.0, n)), rel=0.12)
    assert I.erp_template(400.0, "n400") < -4.5 and I.erp_template(400.0, "none") == pytest.approx(0.0, abs=0.01)
    assert I.erp_template(350.0, "p300") > 7.5


def test_relaxation_and_the_fourier_pair():
    r = I.relaxation(np.array([0.0, 1000.0]), t1=1000.0, t2=100.0)
    assert r["recovery"][0] == 0 and r["recovery"][1] == pytest.approx(1 - math.exp(-1))
    assert r["decay"][1] == pytest.approx(math.exp(-10))
    im = I.phantom(32)
    assert np.allclose(I.from_kspace(I.kspace(im)), im, atol=1e-10)
    err = [np.abs(I.from_kspace(I.kspace(im), f) - im).mean() for f in (0.5, 0.25, 0.125)]
    assert err[0] < err[1] < err[2]


def test_the_haemodynamic_response_peaks_near_five_seconds_and_responses_add():
    t = np.linspace(0, 30, 3001)
    h = I.hrf(t)
    assert t[np.argmax(h)] == pytest.approx(5.0, abs=0.1) and h.max() == pytest.approx(1.0, abs=1e-6)
    assert h.min() < 0 and 12 < t[np.argmin(h)] < 20
    one, two = I.bold([10.0], 60, 1.0), I.bold([16.0], 60, 1.0)
    assert np.allclose(I.bold([10.0, 16.0], 60, 1.0), one + two)
    assert np.argmax(one) == pytest.approx(15, abs=1)


def test_the_linear_model_recovers_a_known_weight_and_matches_scipy():
    X = I.design_matrix({"task": np.arange(20.0, 220.0, 40.0)}, 120, 2.0, duration=20.0)
    g = rng(5)
    y = 0.7 * X[:, 0] + 3.0 + 0.5 * g.standard_normal(120)
    fit = I.glm(y, X, [1, 0])
    assert fit["beta"][0, 0] == pytest.approx(0.7, abs=0.15) and fit["beta"][1, 0] == pytest.approx(3.0, abs=0.15)
    ref = stats.linregress(X[:, 0], y)
    assert fit["beta"][0, 0] == pytest.approx(ref.slope) and fit["t"][0] == pytest.approx(ref.slope / ref.stderr)
    assert fit["df"] == 118


def test_thresholds_on_a_brain_with_two_active_regions():
    brain = I.SyntheticBrain(regions=((16, 15, 3.0, 0.5), (30, 33, 4.0, 0.5)))
    s = brain.scan(rng=rng(6))
    for rule in ("uncorrected", "bonferroni", "fdr"):
        hit = I.threshold_map(s["t"], s["df"], brain.mask, rule)
        assert (hit & brain.active).sum() > 0.9 * brain.active.sum()
        assert (hit & ~brain.mask).sum() == 0
    strict = I.threshold_map(s["t"], s["df"], brain.mask, "bonferroni")
    loose = I.threshold_map(s["t"], s["df"], brain.mask, "uncorrected")
    assert strict.sum() <= loose.sum()
    with pytest.raises(ValueError):
        I.threshold_map(s["t"], s["df"], brain.mask, "magic")


def test_false_discovery_threshold_is_benjamini_hochberg():
    p = np.array([0.001, 0.008, 0.039, 0.041, 0.042, 0.06, 0.074, 0.205, 0.212, 0.216])
    assert I.fdr_threshold(p, 0.05) == pytest.approx(0.008)  # the textbook example: two discoveries
    assert I.fdr_threshold(np.array([0.5, 0.6, 0.9]), 0.05) == 0.0


def test_null_brains_uncorrected_inflates_and_the_corrections_hold():
    maps, mask = I.null_tmaps(400, rng=rng(7))
    extent = I.cluster_extent(I.null_tmaps(400, rng=rng(8))[0], mask, 118)
    r = I.familywise_rates(maps, mask, 118, extent)
    assert r["uncorrected"] > 0.3 and r["bonferroni"] < 0.08 and r["fdr"] < 0.1 and r["cluster"] < 0.12
    assert r["mean_uncorrected_voxels"] == pytest.approx(r["voxels"] * 0.001, rel=0.35)
    assert I.chance_of_any(1000) == pytest.approx(1 - 0.999 ** 1000)


def test_cluster_threshold_fails_on_long_tailed_noise():
    r = I.cluster_calibration(brains=300, long_tail=0.5, rng=rng(9))
    assert r["gaussian"] < 0.1 and r["long_tail"] > 1.8 * max(r["gaussian"], 0.03)


def test_circular_selection_makes_a_correlation_from_nothing():
    v = I.voodoo(subjects=16, voxels=10_000, threshold=0.7, rng=rng(10))
    assert v["selected"] > 0 and v["r_same"] > 0.7 and abs(v["r_fresh"]) < 0.25
    assert np.all(v["r_all"][v["chosen"]] > 0.7)


def test_reverse_inference_ceiling_and_sample_sizes():
    r = I.reverse_inference(0.5, 0.23, 0.10)
    assert r["bayes_factor"] == pytest.approx(2.3) and r["posterior"] == pytest.approx(2.3 / 3.3)
    assert I.r_ceiling(0.5, 0.8) == pytest.approx(math.sqrt(0.4))
    assert I.r_critical(25) == pytest.approx(0.396, abs=0.001)
    assert I.n_for_correlation(0.2) == 194 and 2000 < I.n_for_correlation(0.06) < 2300
    s = I.small_study(0.06, 25, studies=20_000, rng=rng(11))
    assert 0.04 < s["power"] < 0.08 and s["mean_sig_r"] > 0.4 and 0.1 < s["wrong_sign"] < 0.3
