"""The string of Part 1: three independent routes to the same motion must agree.

    python -m pytest -q tests/music/test_string.py
"""

import numpy as np
import pytest

from explainer.music.monochord.dsp import f0_autocorr, partials
from explainer.music.monochord.physics import (String, dalembert, energy, modal, modal_bridge_force, pluck_modes,
                                               pluck_shape, simulate, sine_coefficients, stretch_gamma)


def test_ideal_scheme_is_dalembert_exactly():
    s = String.tuned(110.0)
    N = 240
    run = simulate(s, lambda x: pluck_shape(x, s.L, 0.2, 1e-3), 0.03, N=N, snapshot_every=7)
    assert run.courant == pytest.approx(1.0)
    exact = dalembert(lambda x: pluck_shape(x, s.L, 0.2, 1e-3), s.L, s.c, run.x, run.t_snap)
    assert np.abs(run.snaps - exact).max() < 1e-12


def test_modes_sum_to_dalembert():
    s = String.tuned(110.0)
    x = np.linspace(0, s.L, 201)
    t = np.linspace(0, 2 / s.f1, 37)
    a = pluck_modes(4000, 0.3, 1e-3)
    exact = dalembert(lambda z: pluck_shape(z, s.L, 0.3, 1e-3), s.L, s.c, x, t)
    assert np.abs(modal(s, a, x, t) - exact).max() < 2e-6  # the series converges as 1/n


def test_pluck_coefficients():
    L, beta = 0.65, 1 / 3
    x = np.linspace(0, L, 3001)
    num = sine_coefficients(pluck_shape(x, L, beta), 12)
    ana = pluck_modes(12, beta)
    assert np.allclose(num, ana, atol=2e-6)
    assert abs(ana[2]) < 1e-12 and abs(ana[5]) < 1e-12 and abs(ana[8]) < 1e-12  # plucked at a third: no 3, 6, 9
    assert ana[0] / ana[1] == pytest.approx(4 * np.sin(np.pi / 3) / np.sin(2 * np.pi / 3))  # 1/n^2 envelope


def test_fundamental_is_mersenne():
    s = String(L=0.5, T=80.0, mu=0.002)
    run = simulate(s, lambda x: pluck_shape(x, s.L, 0.37, 1e-3), 0.5, sr=48_000)
    f = f0_autocorr(run.pickup, run.sr, 50, 1000)
    assert f == pytest.approx(s.f1, rel=5e-4)  # under a cent
    assert s.f1 == pytest.approx(np.sqrt(80.0 / 0.002) / (2 * 0.5))


def test_mersenne_exponents_from_beads():
    """Fit f ~ L^a T^b mu^c on simulated strings: Newton's law on beads gives a = -1, b = 1/2, c = -1/2."""
    rng = np.random.default_rng(0)
    rows, fs = [], []
    for _ in range(18):
        L, T, mu = rng.uniform(0.3, 1.0), rng.uniform(40, 160), rng.uniform(0.001, 0.008)
        s = String(L=L, T=T, mu=mu)
        run = simulate(s, lambda x: pluck_shape(x, s.L, 0.31, 1e-3), 0.4, sr=48_000)
        fs.append(np.log(f0_autocorr(run.pickup, run.sr, 30, 1500)))
        rows.append([1.0, np.log(L), np.log(T), np.log(mu)])
    coef, *_ = np.linalg.lstsq(np.array(rows), np.array(fs), rcond=None)
    assert coef[1] == pytest.approx(-1.0, abs=0.004)
    assert coef[2] == pytest.approx(0.5, abs=0.004)
    assert coef[3] == pytest.approx(-0.5, abs=0.004)
    assert np.exp(coef[0]) == pytest.approx(0.5, rel=0.02)  # the constant is 1/2


def test_stiff_damped_string_matches_its_modes():
    s = String.tuned(98.0, kappa=1.2, sigma0=0.8, sigma1=2e-3)
    run = simulate(s, lambda x: pluck_shape(x, s.L, 0.137, 1e-3), 1.5, sr=48_000)
    got = partials(run.pickup[: int(0.5 * run.sr)], run.sr, s.f1, count=8, centers=s.mode_freq(np.arange(1, 9)))
    for p in got:
        n = p["n"]
        cents = 1200 * np.log2(p["hz"] / s.mode_freq(n))
        assert abs(cents) < 6, (n, cents)  # the grid is coarse when the string is stiff: a few cents of dispersion
    assert s.mode_freq(8) / (8 * s.f1) > 1.002  # stiffness sharpens the upper partials
    # the fundamental decays at its modal rate: compare the level early and late
    n = int(0.25 * run.sr)
    early = partials(run.pickup[:n], run.sr, s.f1, 1)[0]["db"]
    late = partials(run.pickup[4 * n:5 * n], run.sr, s.f1, 1)[0]["db"]
    rate = (early - late) / 20 * np.log(10) / 1.0  # 1/s over the one second between the windows
    assert rate == pytest.approx(float(s.mode_decay(1)), rel=0.08)


def test_bridge_force_agrees_with_modes():
    s = String.tuned(110.0, sigma0=1.0, sigma1=1e-3)
    N = 200
    run = simulate(s, lambda x: pluck_shape(x, s.L, 0.2, 1e-3), 0.02, sr=48_000)
    t = np.arange(len(run.force)) / run.sr
    a = sine_coefficients(pluck_shape(run.x, s.L, 0.2, 1e-3))
    ref = modal_bridge_force(s, a, t)
    # same spectrum: compare the levels of the first partials of the two force signals
    long = simulate(s, lambda x: pluck_shape(x, s.L, 0.2, 1e-3), 0.4, sr=48_000)
    tt = np.arange(len(long.force)) / long.sr
    ref = modal_bridge_force(s, sine_coefficients(pluck_shape(long.x, s.L, 0.2, 1e-3)), tt)
    pa, pb = partials(long.force, long.sr, s.f1, 6), partials(ref, long.sr, s.f1, 6)
    for u, v in zip(pa, pb):
        assert abs(u["db"] - v["db"]) < 1.0, (u, v)
    assert N and len(t)


def test_numpy_and_compiled_loops_agree():
    s = String.tuned(196.0, kappa=0.8, sigma0=0.5, sigma1=1e-3)
    u0 = lambda x: pluck_shape(x, s.L, 0.25, 1e-3)  # noqa: E731
    a = simulate(s, u0, 0.01, sr=48_000, fast=True)
    b = simulate(s, u0, 0.01, sr=48_000, fast=False)
    assert np.abs(a.pickup - b.pickup).max() < 1e-15


def test_ideal_scheme_conserves_energy():
    s = String.tuned(110.0)
    run = simulate(s, lambda x: pluck_shape(x, s.L, 0.2, 1e-3), 0.05, N=200, snapshot_every=1)
    e = energy(run.snaps, s, run.sr)
    assert np.abs(e / e[0] - 1).max() < 1e-12
    # and that energy is the work done in pulling the string aside: T/2 integral (du/dx)^2
    assert e[0] == pytest.approx(0.5 * s.T * 1e-6 / (0.2 * 0.8 * s.L), rel=2e-2)


def test_finger_on_a_node_leaves_only_the_modes_with_a_node_there():
    s = String.tuned(130.81, L=1.0, mu=0.00154, sigma0=0.55, sigma1=4e-4)
    u0 = lambda x: pluck_shape(x, s.L, 0.137, 1e-3)  # noqa: E731
    run = simulate(s, u0, 1.0, sr=48_000, damper=(0.5, 6.0, 0.2))
    before = partials(run.pickup[: int(0.2 * run.sr)], run.sr, s.f1, 6)
    after = partials(run.pickup[int(0.6 * run.sr):], run.sr, s.f1, 6)
    for n in (1, 3, 5):   # an antinode under the finger: gone
        assert before[n - 1]["db"] - after[n - 1]["db"] > 40, n
    for n in (2, 4, 6):   # a node under the finger: they do not feel it
        assert before[n - 1]["db"] - after[n - 1]["db"] < 6, n


def test_stretching_raises_the_pitch_as_predicted():
    """Kirchhoff-Carrier: a hard pluck sounds sharp.  The square root of the mean tension is the first estimate of
    by how much; the true shift is larger, because the tension is highest just when the string is most bent (for a
    single mode, Duffing's 3/8 against the average's 1/4: a factor of 1.5)."""
    s = String.tuned(130.81, L=1.0, mu=0.00154)
    EA = 2.0e11 * np.pi * 0.00025 ** 2
    soft = simulate(s, lambda x: pluck_shape(x, s.L, 0.18, 1e-4), 0.3, sr=48_000, EA=EA, headroom=1.3)
    hard = simulate(s, lambda x: pluck_shape(x, s.L, 0.18, 1e-2), 0.3, sr=48_000, EA=EA, headroom=1.3, N=soft.N)
    f_soft = f0_autocorr(soft.pickup, soft.sr, 60, 400)
    f_hard = f0_autocorr(hard.pickup, hard.sr, 60, 400)
    assert f_soft == pytest.approx(s.f1, rel=1e-3)
    predicted = np.sqrt(hard.tension.mean())
    shift, estimate = f_hard / f_soft - 1, predicted - 1
    assert estimate < shift < 1.5 * estimate
    assert predicted > 1.02            # about half a semitone for a centimetre on a metre of steel wire
    # the static stretch of the pluck itself, in closed form
    g = stretch_gamma(s, EA)
    assert hard.tension[0] == pytest.approx(1 + g * 1e-4 / (0.18 * 0.82 * s.L), rel=1e-3)
