"""Independent checks for the capstone's design and two-stage uncertainty."""
import numpy as np
import pytest
from scipy import stats

from videos.stats.stats20 import pipeline as P
from videos.stats.stats20 import compute as C


def test_two_day_weights_are_aligned_and_used_for_two_day_analysis():
    d = P.nhanes_frame()
    k, _ = P.clean(d)
    k &= d['diet2_ok'] == 1
    assert np.all(np.isfinite(d['wt_diet2'][k]) & (d['wt_diet2'][k] > 0))
    assert not np.allclose(d['wt_diet1'][k], d['wt_diet2'][k])
    r = P.fit(d, {'exposure': 'mean2'})
    X = r['X']
    ref = np.linalg.lstsq(X * np.sqrt(d['wt_diet2'][k])[:, None],
                         r['y'] * np.sqrt(d['wt_diet2'][k]), rcond=None)[0]
    np.testing.assert_allclose(r['b'], ref, atol=1e-8)


def test_joint_calibration_variance_matches_independent_weight_perturbations():
    d = P.nhanes_frame()
    r = P.calibrated(d, {'energy': False})
    k = r['keep']
    # Differentiate the entire two-stage estimator by perturbing each PSU's weights.
    # This refits both equations and is independent of the analytic influence formula.
    hvals = []
    eps = 1e-4
    for h in np.unique(d['strata']):
        grads = []
        for j in np.unique(d['psu'][d['strata'] == h]):
            mask = (d['strata'] == h) & (d['psu'] == j)
            vals = []
            for sign in [-1, 1]:
                dd = dict(d)
                dd['wt_diet2'] = d['wt_diet2'] * (1 + sign * eps * mask)
                vals.append(P.calibrated(dd, {'energy': False})['est'])
            grads.append((vals[1] - vals[0]) / (2 * eps))
        hvals.append(len(grads) / (len(grads) - 1) * np.sum((grads - np.mean(grads)) ** 2))
    assert r['est_se'] ** 2 == pytest.approx(sum(hvals), rel=2e-5)
    # Exact linear-model identity uses the SAME two-day sample, weights and covariates.
    D, _ = P.design(d, k, {**P.SPEC, 'energy': False})
    w = d['wt_diet2'][k]
    naive = np.linalg.lstsq(D * np.sqrt(w)[:, None], r['y'] * np.sqrt(w), rcond=None)[0][1]
    assert r['est'] == pytest.approx(naive / r['lam'], rel=1e-8)


def test_world_draw_weights_use_exact_age_stratum_inclusion_probabilities():
    W = C.W
    d = P.world_frame(W, 0)
    ids = d['seqn'].astype(int)
    for h in np.unique(d['strata']):
        ts = np.flatnonzero(W.towns['region'] == h - 1)
        eligible = W.adult & (W.age >= 18)
        sizes = np.bincount(W.town[eligible], minlength=len(W.towns['region']))
        for j in [1, 2]:
            sel = (d['strata'] == h) & (d['psu'] == j)
            town = W.town[ids[sel]][0]
            assert np.all(W.town[ids[sel]] == town)
            p_town = sizes[town] / sizes[ts].sum()
            assert len(np.unique(ids[sel])) == 250
            for old in [False, True]:
                population_n = np.sum(eligible & (W.town == town) & ((W.age >= 60) == old))
                rows = sel & ((d['age'] >= 60) == old)
                assert rows.sum() > 0
                np.testing.assert_allclose(d['wt_diet1'][rows], population_n / (2 * p_town * rows.sum()))


def test_interaction_slopes_use_the_refitted_centered_main_effect():
    d, k, _ = C.frame()
    r = P.fit(d, keep=k)
    X = np.column_stack([r['X'], r['X'][:, 1] * (d['age'][k] - 50)])
    sw = np.sqrt(r['w'])
    b = np.linalg.lstsq(X * sw[:, None], r['y'] * sw, rcond=None)[0]
    got = C.compute_checks()
    assert got['inter_main'] == pytest.approx(b[1], abs=1e-8)
    assert got['inter_main'] != pytest.approx(r['est'], abs=.1)
    assert got['wald_p'] == pytest.approx(stats.f.sf(got['wald'] / 2, 2, 15))


def test_design_effect_display_uses_the_same_srs_baseline():
    d = C.compute_design()
    assert (d['sbp_se'] / d['sbp_srs_se']) ** 2 == pytest.approx(d['deff'])
    assert d['neff'] == pytest.approx(4948 / d['deff'])


def test_two_day_unweighted_calibration_honors_weight_choice():
    d = P.nhanes_frame()
    unweighted = P.calibrated(d, {'weights': False})
    dd = dict(d, wt_diet2=np.ones(len(d['age'])))
    weighted_ones = P.calibrated(dd)
    assert unweighted['est'] == pytest.approx(weighted_ones['est'])
    assert unweighted['est_se'] == pytest.approx(weighted_ones['est_se'])
