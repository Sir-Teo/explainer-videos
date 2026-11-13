"""Psyche's neuron (``explainer/psychology/psyche/neuron.py``) against closed forms and the figures of 1952."""

from __future__ import annotations

import itertools
import math

import numpy as np
import pytest

from explainer.psychology.psyche import neuron as N


def test_nernst_and_goldman():
    assert N.thermal_voltage(6.3) == pytest.approx(24.08, abs=0.01)
    e_k, e_na = N.nernst(*N.SQUID["K"]), N.nernst(*N.SQUID["Na"])
    assert e_k == pytest.approx(-72.1, abs=0.2) and e_na == pytest.approx(52.4, abs=0.2)
    assert N.nernst(2.0, 1e-4, z=2, temp_c=37) == pytest.approx(132, abs=1)  # calcium, divalent
    # a membrane permeable to one ion sits at that ion's Nernst potential; between them otherwise
    assert N.goldman(1, 0) == pytest.approx(e_k) and N.goldman(0, 1) == pytest.approx(e_na)
    assert e_k < N.goldman(1, 0.04) < -55 and N.goldman(1, 20) > 40  # rest, and the peak of the spike


def test_rc_charging():
    t = np.array([0.0, 10.0, 1000.0])
    v = N.rc_step(t, current=1.0, resistance=10.0, capacitance=1.0)  # tau = 10
    assert v[0] == 0 and v[1] == pytest.approx(10 * (1 - math.exp(-1))) and v[2] == pytest.approx(10)


def test_rest_and_gates():
    hh = N.HH()
    assert hh.rest == pytest.approx(-65, abs=0.3)
    s = N.steady(hh.rest)
    assert s["m"] == pytest.approx(0.053, abs=0.003) and s["h"] == pytest.approx(0.596, abs=0.005)
    assert s["n"] == pytest.approx(0.318, abs=0.003)
    r = hh.simulate(0.0, 30)
    assert np.ptp(r["v"]) < 0.05  # it stays at rest
    assert N.steady(-40.0)["m"] == pytest.approx(0.5, abs=0.02)  # the removable singularity is handled
    assert N.steady(20.0, temp_c=16.3)["tau_n"] == pytest.approx(N.steady(20.0)["tau_n"] / 3)


def test_all_or_none():
    hh = N.HH()
    th = hh.threshold(0.5)
    below, above, far = hh.pulse(0.9 * th), hh.pulse(1.1 * th), hh.pulse(3 * th)
    assert below["v"].max() < -50
    assert 30 < above["v"].max() < 50 and 95 < np.ptp(above["v"]) < 120  # a spike of about 100 mV
    assert abs(far["v"].max() - above["v"].max()) < 8  # three times the stimulus, nearly the same spike
    assert above["v"].min() < hh.rest - 5  # the undershoot, toward E_K


def test_clamp_is_what_they_measured():
    hh = N.HH()
    c = hh.clamp(hh.rest + 60, 12)
    assert np.all(np.diff(c["g_k"]) >= -1e-12)  # potassium rises and stays
    assert c["g_k"][-1] == pytest.approx(hh.g_k * N.steady(hh.rest + 60)["n"] ** 4, rel=0.01)
    peak = c["g_na"].argmax()
    assert 0.2 < c["t"][peak] < 1.5 and c["g_na"][-1] < 0.1 * c["g_na"][peak]  # sodium rises and inactivates
    assert c["g_k"][:20].max() < 0.05 * c["g_k"][-1]  # the delay of n^4
    # the simulated patch, held by a huge injected current, agrees with the closed form
    held = hh.simulate(lambda t: 0.0, 0.5, v0=hh.rest)
    assert held["g_k"][-1] == pytest.approx(hh.clamp(hh.rest, 0.5)["g_k"][-1], rel=1e-3)


def test_repetitive_firing_and_refractory_period():
    hh = N.HH()
    assert hh.firing_rate(2.0) == 0
    assert 55 < hh.firing_rate(10.0) < 80 and hh.firing_rate(20.0) > hh.firing_rate(10.0)
    th = hh.threshold(0.5)
    second = hh.refractory([2.0, 6.0, 9.0, 25.0])
    assert math.isinf(second[0])  # absolute
    assert second[1] > second[2] > th  # relative: possible, at a higher price
    assert second[3] == pytest.approx(th, rel=0.25)


def test_conduction_velocity_of_1952():
    p = N.propagate()
    assert p["velocity"] == pytest.approx(18.8, abs=1.5)  # Hodgkin and Huxley's computed 18.8 m/s
    assert np.all(np.diff(p["arrival"][20:-20]) > 0)  # it travels left to right
    thin = N.propagate(radius_cm=0.0238 / 4)
    assert thin["velocity"] == pytest.approx(p["velocity"] / 2, rel=0.08)  # speed goes as the square root of radius
    assert N.length_constant(0.0238, 1 / 0.3e-3, 35.4) == pytest.approx(1.06, abs=0.02)  # about a centimetre


def test_fitzhugh_nagumo():
    f = N.FHN()
    v, w = f.fixed_point(0.0)
    assert v == pytest.approx(-1.1994, abs=1e-3) and w == pytest.approx(-0.6243, abs=1e-3)
    nv, nw = f.nullclines(v, 0.0)
    assert nv == pytest.approx(w) and nw == pytest.approx(w)
    assert f.stable(0.0) and not f.stable(0.5) and f.stable(2.0)  # rest, firing, depolarization block
    quiet, firing = f.simulate(0.0, 200), f.simulate(0.5, 400)
    assert np.ptp(quiet["v"]) < 1e-6 and np.ptp(firing["v"][4000:]) > 3
    # a kick across the middle branch gives a full excursion; a smaller one decays
    assert f.simulate(0.0, 100, v0=(-0.5, w))["v"].max() > 1.5 > 0 > f.simulate(0.0, 100, v0=(-0.9, w))["v"].max()


def test_integrate_and_fire_closed_form():
    lif = N.LIF()
    assert lif.rheobase == pytest.approx(1.5) and lif.rate(1.4) == 0
    for current in (1.6, 2.0, 4.0):
        s = lif.simulate(current, 2000)["spikes"]
        assert 1000 / np.diff(s).mean() == pytest.approx(float(lif.rate(current)), rel=0.01)
    assert lif.rate(1e6) == pytest.approx(1000 / lif.t_ref, rel=0.01)  # the refractory ceiling
    assert lif.coincidence(0.5) and not lif.coincidence(15.0)  # together they fire it, apart they do not


def test_spike_trains():
    rng = np.random.default_rng(3)
    c = N.counts(40.0, 1.0, 400, rng)
    assert c.mean() == pytest.approx(40, rel=0.05) and N.fano(c) == pytest.approx(1.0, abs=0.2)
    regular = N.counts(40.0, 1.0, 400, rng, refractory=0.015)
    assert N.fano(regular) < 0.5 and regular.mean() < c.mean()
    ramp = N.poisson_train(lambda t: 100 * t, 1.0, rng)
    assert (ramp > 0.5).sum() > 2 * (ramp <= 0.5).sum()
    a = N.adrian([0.05, 0.2, 0.4, 0.8, 1e9])
    assert a[0] == 0 and a[2] - a[1] == pytest.approx(a[3] - a[2]) and a[-1] == 150


def test_what_one_neuron_can_compute():
    x = np.array(list(itertools.product((0, 1), repeat=4)))
    # "inputs 0 and 1 together, or inputs 2 and 3 together": two branches, each a coincidence detector
    y = N.dendritic_neuron(x, [(0, 1), (2, 3)], branch_threshold=2)
    assert y.sum() == 7 and y[int("1100", 2)] and y[int("0011", 2)] and not y[int("1010", 2)]
    assert not N.separable(x, y)  # no point neuron does this
    assert N.separable(x, (x.sum(axis=1) >= 2).astype(int))  # "any two" is one linear boundary
    assert np.array_equal(N.point_neuron(x, [1, 1, 1, 1], 2), (x.sum(axis=1) >= 2).astype(int))
    xor = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    assert not N.separable(xor, [0, 1, 1, 0])
