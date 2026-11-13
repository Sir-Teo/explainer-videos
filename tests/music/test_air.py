"""Monochord's air (Part 2): each simulator against something that does not share its code.

    python -m pytest -q tests/music/test_air.py
"""

import math

import numpy as np
import pytest

from explainer.music.monochord.physics import air


def pulse(t, t0=0.4e-3, w=0.12e-3, u=0.01):
    return u * math.exp(-((t - t0) / w) ** 2)


def arrival(v, dt):
    """The time of a pulse's peak, refined between samples."""
    i = int(np.argmax(v))
    a, b, c = v[i - 1], v[i], v[i + 1]
    return (i + 0.5 * (a - c) / (a - 2 * b + c)) * dt


@pytest.mark.parametrize("law,gamma", [("adiabatic", 1.4), ("isothermal", 1.0)])
def test_the_gas_law_sets_the_speed_of_sound(law, gamma):
    """No wave speed is written into the chain: it comes out as sqrt(gamma P / rho)."""
    run = air.gas_chain(6.0, 3001, pulse, 0.017, law=law, celsius=0.0, probes=(500, 2000))
    t1, t2 = (arrival(run.velocity[k], run.dt) for k in (0, 1))
    c = 1500 * run.h / (t2 - t1)
    assert c == pytest.approx(math.sqrt(gamma * air.P_ATM / air.density(0.0)), rel=2e-3)


def test_laplace_and_newton():
    assert air.speed(0.0) == pytest.approx(331.3, abs=0.3)
    assert air.speed(0.0, "isothermal") / air.speed(0.0) == pytest.approx(1 / math.sqrt(1.4))
    assert air.speed(20.0) == pytest.approx(343.2, abs=0.3)
    assert air.spl(1.0) == pytest.approx(93.98, abs=0.01) and air.impedance(20.0) == pytest.approx(413, abs=2)


def test_a_loud_wave_steepens_as_fubini_says():
    hz, u0 = 1000.0, 8.0
    xs = air.shock_distance(u0, hz, celsius=20.0)
    h = 0.5e-3
    n = int(2.0 * xs / h)                                    # long enough that no echo returns during the run
    sig = (0.3, 0.6, 0.85)
    probes = [int(s * xs / h) for s in sig]
    run = air.gas_chain(n * h, n + 1, lambda t: u0 * math.sin(2 * math.pi * hz * t) * min(1.0, t * hz / 2), 0.012,
                        celsius=20.0, probes=probes, courant=0.25)
    for s, v in zip(sig, run.velocity):
        m = int(round(4 / hz / run.dt))                      # four periods of the steady wave
        t = np.arange(m) * run.dt
        for k in (1, 2, 3):
            got = abs(2 * np.mean(v[-m:] * np.exp(-2j * np.pi * k * hz * t))) / u0
            assert got == pytest.approx(air.fubini(k, s), abs=0.02), (s, k)


def test_spreading_in_the_plane_and_in_space():
    # in a plane the pressure of a tone falls as one over the square root of the distance
    hz = 600.0
    f = air.fdtd2d(8.0, 8.0, 0.02, 0.022, sources=[(4.0, 4.0, air.tone_burst(hz))],
                   receivers=[(4.0 + r, 4.0) for r in (0.8, 1.6, 3.2)])
    tail = slice(int(0.015 / f.dt), None)
    amp = [np.abs(f.receivers[k][tail]).max() for k in range(3)]
    slope = np.polyfit(np.log([0.8, 1.6, 3.2]), np.log(amp), 1)[0]
    assert slope == pytest.approx(-0.5, abs=0.04)
    # a tube whose area grows as the square of the distance is a point source in space: one over the distance
    run = air.tube(lambda x: 4 * math.pi * (x + 0.2) ** 2, 12.0, 0.03, air.ricker(800.0), where=0.0, left="closed",
                   right="closed", sr=96_000, snapshot_every=1)
    peak = np.abs(run.snaps).max(axis=0)
    r = run.x + 0.2
    pick = [int(np.argmin(np.abs(r - v))) for v in (1.0, 2.0, 4.0, 8.0)]
    slope = np.polyfit(np.log(r[pick]), np.log(peak[pick]), 1)[0]
    assert slope == pytest.approx(-1.0, abs=0.03)


@pytest.mark.parametrize("stopped", [False, True])
def test_pipes(stopped):
    L = 0.5
    run = air.tube(1e-3, L, 0.4, air.ricker(900.0), where=0.031, left="closed" if stopped else "open", right="open",
                   probe=0.053)
    got = air.resonances(run.pressure, run.sr, count=4, fmin=100, fmax=1500)
    want = air.pipe_modes(L, 4, stopped=stopped)
    assert np.allclose(got[:len(want[want < 1500])], want[want < 1500], rtol=4e-3)


def test_a_bottle_is_a_neck_on_a_body():
    a, ln, sb, lb = math.pi * 0.01 ** 2, 0.08, math.pi * 0.035 ** 2, 0.14
    exact = air.bottle_exact(a, ln, sb, lb)
    lumped = air.helmholtz(a, ln, sb * lb)
    run = air.tube(lambda x: sb if x < lb else a, lb + ln, 0.5, air.ricker(300.0), where=0.01, left="closed",
                   right="open", probe=0.02, n=220, sr=384_000)
    got = air.resonances(run.pressure, run.sr, count=1, fmin=40, fmax=600)[0]
    assert got == pytest.approx(exact, rel=6e-3)
    assert 1.0 < lumped / exact < 1.12          # Helmholtz's formula runs a little high: the body is not a point


def test_doppler():
    y, heard = air.passing_source(440.0, 30.0, 5.0, 8.0)
    up, down = air.doppler(440.0, 30.0)
    assert heard[100] == pytest.approx(up, rel=2e-3) and heard[-100] == pytest.approx(down, rel=2e-3)
    late = len(heard) // 2 + int(5.0 / air.speed() * 48_000)        # the sound made abreast arrives d / c later
    assert heard[late] == pytest.approx(440.0, rel=1e-3)
    assert np.abs(y).max() == pytest.approx(1.0, abs=0.01)
