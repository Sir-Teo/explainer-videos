"""Psyche's signal detection against closed forms and its own planted answers."""

import math

import numpy as np
from scipy import stats

from explainer.psychology.psyche import sdt as D


def test_dprime_and_c_invert_the_rates():
    for d, k in ((1.0, 0.2), (2.0, 1.5), (0.5, -0.4)):
        h, f = D.rates(d, k)
        assert abs(D.dprime(h, f) - d) < 1e-9
        assert abs(D.criterion_c(h, f) - (k - d / 2)) < 1e-9
        assert abs(math.log(D.beta(h, f)) - d * (k - d / 2)) < 1e-9


def test_loglinear_keeps_perfect_rates_finite():
    r = D.from_counts(50, 50, 0, 50)
    assert np.isfinite(r["d"]) and 3 < r["d"] < 6


def test_auc_matches_simulation_and_the_2afc_identity():
    rng = np.random.default_rng(1)
    for d, s in ((1.0, 1.0), (1.5, 1.25)):
        xs = d + s * rng.standard_normal(200000)
        xn = rng.standard_normal(200000)
        assert abs(np.mean(xs > xn) - D.auc(d, s)) < 0.004
    assert abs(D.auc(1.3) - D.pc_2afc(1.3)) < 1e-12
    assert abs(D.d_from_2afc(D.pc_2afc(1.7)) - 1.7) < 1e-9


def test_mafc_reduces_to_2afc_and_falls_with_m():
    assert abs(D.pc_mafc(1.2, 2) - D.pc_2afc(1.2)) < 1e-7
    assert D.pc_mafc(1.2, 4) < D.pc_mafc(1.2, 2)
    assert abs(D.pc_mafc(0.0, 4) - 0.25) < 1e-7


def test_zroc_slope_is_one_over_sigma():
    fa, hit = D.roc(1.5, 1.25, criteria=np.linspace(-0.5, 2.5, 7))
    z = D.zroc(hit, fa)
    assert abs(z["slope"] - 0.8) < 1e-9 and abs(z["intercept"] - 1.5 / 1.25) < 1e-9


def test_rating_fit_recovers_unequal_variance():
    obs = D.Observer(d=1.4, sigma_s=1.25)
    cs, cn = D.simulate_ratings(obs, [-0.5, 0.2, 0.8, 1.4, 2.0], 4000, 4000, np.random.default_rng(3))
    f = D.fit_rating(cs, cn)
    assert abs(f["d"] - 1.4) < 0.1 and abs(f["sigma_s"] - 1.25) < 0.08
    eq = D.fit_rating(cs, cn, equal_variance=True)
    assert f["loglik"] > eq["loglik"] + 5


def test_optimal_criterion_maximizes_expected_value():
    for p, pay in ((0.5, {}), (0.1, {}), (0.3, {"c_fa": 2.0}), (0.5, {"c_miss": 4.0})):
        k = D.optimal_criterion(1.5, p, **pay)
        grid = np.linspace(-3, 5, 8001)
        ev = D.expected_value(1.5, grid, p, **{"v_hit": 1.0, "v_cr": 1.0, **pay})
        assert abs(grid[np.argmax(ev)] - k) < 2e-3


def test_high_threshold_roc_is_a_straight_line_to_the_corner():
    g = np.linspace(0, 1, 11)
    fa, hit = D.high_threshold_roc(0.4, g)
    assert np.allclose(np.diff(hit) / np.diff(fa), 0.6) and abs(hit[-1] - 1) < 1e-12


def test_dual_process_roc_starts_above_zero():
    fa, hit = D.dual_process_roc(0.3, 1.0, [8.0])
    assert fa[0] < 1e-9 and abs(hit[0] - 0.3) < 1e-9


def test_natural_frequencies_give_the_mammogram_answer():
    r = D.natural_frequencies(0.01, 0.8, 0.096)
    assert abs(r["true_positive"] - 8) < 1e-9 and abs(r["false_positive"] - 95.04) < 1e-6
    assert abs(r["ppv"] - 0.0776) < 1e-3


def test_prevalence_moves_the_optimal_criterion_up_and_hits_down():
    k = D.prevalence_criteria(2.0, [0.5, 0.1, 0.01])
    assert k[0] == 1.0 and k[0] < k[1] < k[2]
    hit, _ = D.rates(2.0, k)
    assert hit[0] > hit[1] > hit[2]
