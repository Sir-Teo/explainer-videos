"""Psyche's psychophysics module against closed forms and its own planted answers."""

import math

import numpy as np
import pytest
from scipy import optimize, stats

from explainer.psychology.psyche import psychophysics as P


def test_weber_fraction_is_flat_above_the_floor_and_rises_below_it():
    o = P.Observer(k=0.08, sigma0=0.5, lapse=0.0)
    w = P.weber_fractions(o, [1.0, 10.0, 100.0, 1000.0])
    theory = math.sqrt(2) * stats.norm.ppf(0.75) * 0.08
    assert abs(w[-1] - theory) < 1e-3 and abs(w[-2] - theory) < 2e-3
    assert w[0] > 3 * theory  # the floor dominates at low intensity


def test_near_miss_makes_the_fraction_fall_with_level():
    o = P.Observer(k=0.08, sigma0=0.0, lapse=0.0, near_miss=0.1)
    w = P.weber_fractions(o, [10.0, 100.0, 1000.0])
    assert w[0] > w[1] > w[2]


def test_p_correct_matches_simulation():
    o = P.Observer(k=0.08, sigma0=0.5, lapse=0.04)
    rng = np.random.default_rng(0)
    sim = np.mean([o.respond(100.0, 8.0, rng) for _ in range(20000)])
    assert abs(sim - float(o.p_correct(100.0, 8.0))) < 0.01


@pytest.mark.parametrize("form", ["gauss", "logistic", "weibull"])
def test_psychometric_limits_and_threshold_inverse(form):
    fitted = {"alpha": 5.0, "beta": 1.5 if form != "weibull" else 3.0, "gamma": 0.5, "lam": 0.03, "form": form}
    lo = P.psychometric(1e-6 if form == "weibull" else -1e6, 5.0, fitted["beta"], 0.5, 0.03, form)
    hi = P.psychometric(1e6, 5.0, fitted["beta"], 0.5, 0.03, form)
    assert abs(lo - 0.5) < 1e-6 and abs(hi - 0.97) < 1e-6
    x = P.threshold_at(fitted, 0.8)
    assert abs(P.psychometric(x, 5.0, fitted["beta"], 0.5, 0.03, form) - 0.8) < 1e-9


def test_maximum_likelihood_recovers_planted_parameters():
    rng = np.random.default_rng(1)
    x = np.linspace(1, 12, 8)
    n = np.full(8, 400)
    k = rng.binomial(n, P.psychometric(x, 6.0, 2.0, 0.5, 0.02, "gauss"))
    f = P.fit(x, k, n, form="gauss")
    assert abs(f["alpha"] - 6.0) < 0.4 and abs(f["beta"] - 2.0) < 0.4 and f["lam"] <= 0.1
    assert f["deviance"] >= 0


def test_bootstrap_interval_covers_the_planted_threshold():
    rng = np.random.default_rng(2)
    x = np.linspace(1, 12, 6)
    n = np.full(6, 60)
    k = rng.binomial(n, P.psychometric(x, 6.0, 2.0, 0.5, 0.0, "gauss"))
    f = P.fit(x, k, n, form="gauss", lam=0.0)
    b = P.bootstrap(x, k, n, f, n_boot=150, rng=np.random.default_rng(3))
    true75 = P.threshold_at({"alpha": 6.0, "beta": 2.0, "gamma": 0.5, "lam": 0.0, "form": "gauss"}, 0.75)
    lo, hi = b["threshold_ci"]
    assert lo < true75 < hi and lo < f["alpha"] + 1 and hi > f["alpha"] - 1


@pytest.mark.parametrize("k_down, target", [(1, 0.5), (2, 0.7071), (3, 0.7937), (4, 0.8409)])
def test_updown_targets(k_down, target):
    assert abs(P.updown_target(k_down) - target) < 1e-4


def test_two_down_one_up_converges_to_the_707_level():
    o = P.Observer(k=0.08, sigma0=0.5, lapse=0.02)
    level = optimize.brentq(lambda d: float(o.p_correct(100.0, d)) - P.updown_target(2), 0.01, 60)
    fine = [P.staircase(o, 100.0, 30.0, factor=1.12, rng=np.random.default_rng(10 + i), n_trials=200,
                        n_reversals_used=12)["estimate"] for i in range(150)]
    assert abs(np.median(fine) / level - 1) < 0.05
    coarse = [P.staircase(o, 100.0, 30.0, factor=1.25, rng=np.random.default_rng(10 + i), n_trials=120)["estimate"]
              for i in range(150)]
    assert np.median(coarse) < np.median(fine)  # Levitt's target is a small-step result


def test_quest_converges_near_its_target():
    o = P.Observer(k=0.08, sigma0=0.5, lapse=0.02)
    ests = [P.quest(o, 100.0, 50, rng=np.random.default_rng(100 + i))["estimate"] for i in range(60)]
    level = optimize.brentq(lambda d: float(o.p_correct(100.0, d)) - 0.82, 0.01, 60)
    assert abs(np.median(ests) / level - 1) < 0.12


def test_adjustment_spread_gives_the_jnd():
    o = P.Observer(k=0.08, sigma0=0.5, lapse=0.0)
    a = P.method_of_adjustment(o, 100.0, 4000, np.random.default_rng(4))
    assert abs(a["pse"] - 100.0) < 0.6
    assert abs(a["jnd_from_sd"] / float(P.jnd(o, 100.0)) - 1) < 0.04


def test_limits_threshold_moves_with_the_criterion():
    o = P.Observer(k=0.08, sigma0=0.5, lapse=0.0)
    t = [np.mean([P.method_of_limits(o, 100.0, 30, 2.5, 10, np.random.default_rng(i), criterion=c)["threshold"]
                  for i in range(30)]) for c in (0.5, 1.5)]
    assert t[1] > t[0] + 3


def test_fechner_counts_jnds_and_tends_to_the_log_law():
    s = P.fechner([1.0, 10.0, 100.0], 1.0, 0.05)
    assert abs(s[1] - math.log(10) / math.log(1.05)) < 1e-9 and abs(s[2] - 2 * s[1]) < 1e-9
    assert abs(P.fechner(10.0, 1.0, 1e-4) * 1e-4 - math.log(10)) < 1e-3


def test_power_law_exponent_is_recovered_from_magnitude_estimates():
    me = P.magnitude_estimation(np.logspace(0, 3, 10), 0.67, 40, np.random.default_rng(5))
    assert abs(P.fit_power(me["intensity"], me["geometric_mean"])["exponent"] - 0.67) < 0.06
    assert abs(P.cross_modality(0.67, 0.33) - 0.67 / 0.33) < 1e-12


def test_constant_stimuli_counts_add_up():
    o = P.Observer()
    cs = P.constant_stimuli(o, 100.0, [2.0, 8.0, 20.0], 30, np.random.default_rng(6))
    assert cs["k"].sum() == cs["trials"]["correct"].sum() and np.all(cs["n"] == 30)
    assert cs["k"][2] >= cs["k"][0]


def test_battery_threshold_task_runs_on_the_observer():
    from explainer.psychology import battery

    t = battery.run("threshold", P.Observer(), 160, seed=3)
    assert t.task == "threshold" and len(t) == 160 and set(np.unique(t.extra["delta"])) == set(battery.THRESHOLD_DELTAS)
    big = t.correct[t.extra["delta"] == 24.0].mean()
    small = t.correct[t.extra["delta"] == 1.0].mean()
    assert big > small


def test_photon_noise_gives_the_square_root_law_between_the_floor_and_weber():
    o = P.Observer(k=0.01, sigma0=0.05, lapse=0.0, poisson=1.0)
    i = np.array([1.0, 10.0, 100.0, 1e5, 1e6])
    j = P.jnd(o, i)
    middle = math.log10(j[2] / j[1])  # between the floor and the Weber regime
    top = math.log10(j[4] / j[3])
    assert abs(middle - 0.5) < 0.06 and abs(top - 1.0) < 0.02


def test_bootstrap_goodness_of_fit_is_not_small_for_counts_from_the_model_itself():
    rng = np.random.default_rng(7)
    x = np.linspace(1, 12, 8)
    n = np.full(8, 40)
    k = rng.binomial(n, P.psychometric(x, 6.0, 2.0, 0.5, 0.0, "gauss"))
    f = P.fit(x, k, n, form="gauss", lam=0.0)
    b = P.bootstrap(x, k, n, f, n_boot=200, rng=np.random.default_rng(8))
    assert len(b["deviance"]) == 200 and 0.02 < b["p_fit"] <= 1.0
    # a curve that misses the counts badly is rejected
    bad = dict(f, alpha=f["alpha"] * 2.5)
    bad["deviance"] = 2 * (sum(stats.binom.logpmf(k, n, k / n)) - sum(stats.binom.logpmf(
        k, n, P.psychometric(x, bad["alpha"], bad["beta"], 0.5, 0.0, "gauss"))))
    assert P.bootstrap(x, k, n, bad, n_boot=100, rng=np.random.default_rng(9))["p_fit"] < 0.02


def test_triangle_critical_count_and_power_match_the_binomial():
    for n in (12, 30, 60):
        c = P.triangle_critical(n)
        assert stats.binom.sf(c - 1, n, 1 / 3) <= 0.05 < stats.binom.sf(c - 2, n, 1 / 3)
    assert P.triangle_power(30, 0.0) <= 0.05
    assert P.triangle_power(60, 0.3) > P.triangle_power(30, 0.3) > P.triangle_power(30, 0.1)


def test_thurstone_case_v_recovers_a_planted_scale():
    v = np.array([0.0, 0.3, 0.8, 1.0, 1.7])
    p = P.paired_comparisons(v, 4000, np.random.default_rng(11))
    assert np.allclose(p + p.T, 1.0, atol=0.02)
    s = P.thurstone_case_v(p)
    # Case V's unit is the sd of a difference, sqrt(2) here
    assert np.allclose(s, (v - v.mean()) / math.sqrt(2), atol=0.06)
