"""Psyche's circuits (``explainer/psychology/psyche/circuits.py``) against closed forms and known behaviour."""

from __future__ import annotations

import numpy as np
import pytest

from explainer.psychology.psyche import circuits as C


def test_alpha_peaks_at_tau():
    t = np.linspace(-1, 10, 1101)
    a = C.alpha(t, 2.0)
    assert a[t < 0].max() == 0 and a.max() == pytest.approx(1.0, abs=1e-4) and t[a.argmax()] == pytest.approx(2.0, abs=0.02)


def test_synapses_add_less_than_linearly_and_in_time():
    m = C.Membrane()
    one = m.response(exc=[5.0])["peak"]
    together = m.response(exc=[5.0, 5.0])["peak"]
    apart = m.response(exc=[5.0, 45.0], t_end=100.0)["peak"]
    assert one > 1.0 and one < together < 2 * one  # two at once: more than one, less than twice
    assert apart == pytest.approx(one, rel=0.05)  # 40 ms later the first is nearly forgotten (tau = 10 ms)
    assert m.response(inh=[5.0])["trough"] < -0.5  # an IPSP, toward -80


def test_shunting_inhibition_divides():
    m = C.Membrane()
    assert m.steady_voltage() == m.e_l
    assert m.steady_voltage(g_i=0.3, e_i=m.e_l) == pytest.approx(m.e_l)  # a shunt alone moves nothing
    alone = m.steady_voltage(g_e=0.05) - m.e_l
    shunted = m.steady_voltage(g_e=0.05, g_i=0.15, e_i=m.e_l) - m.e_l
    assert shunted == pytest.approx(alone * (m.g_l + 0.05) / (m.g_l + 0.05 + 0.15))  # divided, by the extra conductance
    assert m.steady_voltage(g_e=1e6) == pytest.approx(m.e_e, abs=1e-3)


def test_hebb_diverges_and_oja_finds_the_principal_component():
    rng = np.random.default_rng(2)
    x = rng.standard_normal((4000, 2)) @ np.array([[2.0, 0.0], [1.2, 0.5]])
    h = C.hebb(x, eta=0.01, rule="hebb", rng=np.random.default_rng(1))
    o = C.hebb(x, eta=0.01, rule="oja", rng=np.random.default_rng(1))
    assert h["norm"][-1] > 1e3 and h["cosine"][-1] > 0.99  # unbounded, in the right direction
    assert np.linalg.norm(o["w"]) == pytest.approx(1.0, abs=0.08) and o["cosine"][-200:].mean() > 0.99
    pc = C.principal_component(x)
    assert np.linalg.norm(pc) == pytest.approx(1.0) and abs(pc[0]) > abs(pc[1])


def test_bcm_becomes_selective():
    out = C.bcm([[1.0, 0.2], [0.2, 1.0]], rng=np.random.default_rng(3))
    r = np.sort(out["final"])
    assert r[1] > 0.5 and r[0] < 0.1 * r[1] and out["selectivity"] > 0.85
    assert out["theta"][-1] == pytest.approx(0.5 * r[1] ** 2, rel=0.35)  # the threshold tracks <y^2>


def test_stdp_window():
    assert C.stdp(10.0) > 0 > C.stdp(-10.0) and C.stdp(0.0) == 0
    assert C.stdp(5.0) > C.stdp(40.0) > 0 and C.stdp(-5.0) < C.stdp(-80.0) < 0
    assert C.stdp(17.0) == pytest.approx(np.exp(-1))


def test_mach_bands_from_lateral_inhibition():
    e = np.r_[np.full(40, 1.0), np.full(40, 2.0)]
    r = C.lateral(e)
    assert r.min() > 0
    low, high = r[15:25].mean(), r[55:65].mean()
    assert r[35:40].min() < low - 0.02 and r[40:45].max() > high + 0.02  # a dark band and a bright band at the edge
    flat = C.lateral(np.full(80, 1.5))
    assert np.ptp(flat[20:60]) < 1e-6  # no bands without an edge
    assert np.allclose((np.eye(80) + C.inhibition_kernel(80)) @ r, e)


def test_hermann_grid_under_a_centre_surround_filter():
    h = C.hermann_response()
    assert h["image"][h["at"], h["at"]] == 1.0 and h["crossing"] < h["street"]  # less response at the crossing
    blurred = C.dog(np.ones((60, 60)), 3.0)
    assert abs(blurred[30, 30]) < 1e-6  # a uniform field gives nothing


def test_winner_take_all_holds_a_choice():
    w = C.WTA()
    a = w.simulate((1.2, 1.0))
    b = w.simulate((1.0, 1.2))
    assert a["winner"] == 0 and b["winner"] == 1 and a["margin"] > 0.8

    def then_equal(t):  # a difference for 150 ms, equal inputs afterwards
        return (1.2, 1.0) if t < 150 else (1.1, 1.1)

    held = w.simulate(then_equal)
    assert held["winner"] == 0 and held["margin"] > 0.8  # the choice outlasts the evidence
    weak = C.WTA(w_self=0.0, w_cross=0.5).simulate(then_equal)
    assert weak["margin"] < 0.05  # without the loop it is forgotten


def test_half_centre_oscillator():
    h = C.HalfCentre()
    s = h.simulate()
    assert h.oscillates and s["correlation"] < -0.5 and 300 < s["period"] < 3000
    quiet = C.HalfCentre(a=0.8)
    assert not quiet.oscillates and np.ptp(quiet.simulate()["y"][-2000:, 0]) < 1e-3  # too little inhibition: steady


def test_wilson_cowan_rest_and_rhythm():
    wc = C.WilsonCowan()
    assert wc.simulate(0.0)["amplitude"] < 0.01
    osc = wc.simulate(1.25)
    assert osc["amplitude"] > 0.1 and 5 < osc["frequency"] < 80
