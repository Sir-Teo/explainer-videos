"""Psyche's decisions in time (Part 25): the closed forms against quadrature and simulation."""

import numpy as np
from scipy import integrate

from explainer.psychology.psyche import decide as D


def test_density_integrates_to_the_closed_form():
    v, a, w = 1.2, 1.5, 0.4
    up = integrate.quad(lambda t: float(D.fpt_density(t, v, a, w, "upper")), 0, 30, limit=300)[0]
    lo = integrate.quad(lambda t: float(D.fpt_density(t, v, a, w, "lower")), 0, 30, limit=300)[0]
    assert abs(up - D.p_upper(v, a, w)) < 1e-8
    assert abs(up + lo - 1) < 1e-8
    m = integrate.quad(lambda t: t * float(D.fpt_density(t, v, a, w, "upper") + D.fpt_density(t, v, a, w, "lower")),
                       0, 30, limit=300)[0]
    assert abs(m - D.mean_dt(v, a, w)) < 1e-6


def test_zero_drift_limits():
    assert abs(D.p_upper(0.0, 2.0, 0.3) - 0.3) < 1e-12
    assert abs(D.mean_dt(0.0, 2.0, 0.5) - 1.0) < 1e-12  # z (a - z) = 1 * 1
    assert abs(D.p_upper(1e-7, 2.0, 0.3) - 0.3) < 1e-5


def test_drift_variability_is_integrated_exactly():
    v, a, w, sv = 1.2, 1.5, 0.4, 1.0
    up = integrate.quad(lambda t: float(D.fpt_density(t, v, a, w, "upper", sv=sv)), 0, 40, limit=300)[0]
    rng = np.random.default_rng(1)
    mc = D.p_upper(v + sv * rng.standard_normal(400000), a, w).mean()
    assert abs(up - mc) < 2e-3


def test_simulation_matches_the_closed_forms():
    rt, up = D.simulate(1.0, 1.4, 0.5, 0.3, n=20000, seed=3, dt=0.0005)
    assert abs(up.mean() - D.p_upper(1.0, 1.4, 0.5)) < 0.012
    assert abs((np.nanmean(rt) - 0.3) - D.mean_dt(1.0, 1.4, 0.5)) < 0.03  # Euler overshoot is small at this dt


def test_fit_recovers_parameters():
    rt, up = D.simulate(1.5, 1.2, 0.5, 0.3, n=3000, seed=5, dt=0.0005)
    f = D.fit_ddm(rt, up, fix={"w": 0.5})
    assert abs(f["v"] - 1.5) < 0.2 and abs(f["a"] - 1.2) < 0.08 and abs(f["t0"] - 0.3) < 0.02


def test_ez_recovers_parameters_with_an_unbiased_start():
    rt, up = D.simulate(1.5, 1.2, 0.5, 0.3, n=20000, seed=7, dt=0.0005)
    e = D.ez(up.mean(), np.var(rt[up]), np.mean(rt[up]), s=1.0)
    assert abs(e["v"] - 1.5) < 0.1 and abs(e["a"] - 1.2) < 0.06 and abs(e["t0"] - 0.3) < 0.02


def test_sprt_beats_the_fixed_sample():
    oc0, n0 = D.sprt_oc_asn(0.5, 0.5, 0.7)
    oc1, n1 = D.sprt_oc_asn(0.7, 0.5, 0.7)
    assert abs(oc0 - 0.95) < 1e-6 and abs(oc1 - 0.05) < 1e-6
    nf = D.fixed_n(0.5, 0.7)
    assert max(n0, n1) < 0.6 * nf
    s = D.sprt_simulate(0.7, 0.5, 0.7, reps=4000, seed=2)
    assert 0.93 < s["accept_h1"] < 0.98 and s["mean_n"] < 0.6 * nf


def test_lba_defective_densities_add_to_the_finishing_probability():
    vs, A, b = [1.0, 0.5], 0.5, 1.0
    tot = sum(integrate.quad(lambda t: float(D.lba_defective(t, i, vs, A, b)), 0, 60, limit=400)[0] for i in (0, 1))
    rt, win = D.lba_simulate(vs, A, b, t0=0.0, n=200000, seed=1)
    assert abs(tot - len(rt) / 200000) < 0.005
    p0 = integrate.quad(lambda t: float(D.lba_defective(t, 0, vs, A, b)), 0, 60, limit=400)[0] / tot
    assert abs(p0 - (win == 0).mean()) < 0.006


def test_stop_race_and_integration_method():
    rng = np.random.default_rng(0)
    go = 0.35 + rng.gamma(4, 0.04, 200000)
    ssrt = 0.22
    ssds = np.array([0.1, 0.2, 0.3])
    r = D.stop_race(go, ssds, ssrt)
    assert np.all(np.diff(r["p_respond"]) > 0)  # the inhibition function rises with delay
    for d, p in zip(ssds, r["p_respond"]):
        if 0.05 < p < 0.95:
            assert abs(D.ssrt_integration(go, d, p) - ssrt) < 0.005
    # signal-respond times are faster than go times: the race's fingerprint
    assert np.all(r["srrt"][r["p_respond"] > 0.01] < go.mean())


def test_confidence_is_higher_when_right():
    c = D.race_confidence([0.5, 1.5], n=3000, seed=1)
    assert np.all(c["conf_correct"] > c["conf_error"])
    assert c["acc"][1] > c["acc"][0]


def test_stepping_averages_to_a_ramp():
    s = D.stepping(n=2000, seed=0)
    single = s["trials"][0]
    assert len(np.unique(single)) <= 2  # each trial steps once
    assert np.all(np.diff(s["mean"]) >= -1e-12) and s["mean"][-1] - s["mean"][0] > 0.5  # the average ramps
