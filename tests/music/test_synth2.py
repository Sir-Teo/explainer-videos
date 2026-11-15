"""Monochord's second synthesizer (Part 52): FM against Bessel, grains, spectral models and physical models.

    python -m pytest -q tests/music/test_synth2.py
"""

import numpy as np
import pytest
from scipy.special import jv

from explainer.music.monochord import synth2 as F
from explainer.music.monochord.physics import string as STR

SR = 48000


def test_fm_lines_are_bessel():
    y = F.fm(1000.0, 250.0, 2.0, SR)
    pred = [(f, a) for f, a in F.sidebands(1000.0, 250.0, 2.0, 8) if 0 < f < 3200]
    meas = F.line_levels(y, [f for f, _ in pred])
    assert np.allclose(meas, [abs(a) for _, a in pred], atol=1e-4)


def test_negative_sidebands_fold_with_sign():
    lines = dict(F.sidebands(200.0, 280.0, 3.0, 4))
    assert lines[round(80.0, 6)] == pytest.approx(-jv(-1, 3.0))


def test_energy_is_independent_of_index():
    for I in (0.5, 2.0, 7.0):
        assert sum(jv(k, I) ** 2 for k in range(-40, 41)) == pytest.approx(1.0, abs=1e-10)


def test_operator_engine_equals_simple_fm():
    a = F.operators("stack2", [1.0, 1.0], [1.0, 2.0], 440.0, 4800)
    b = F.fm(440.0, 440.0, 2.0, 4800)
    assert np.max(np.abs(a - b)) < 1e-9


def test_gabor_uncertainty():
    prods = []
    for ms in (5.0, 20.0, 80.0):
        g = F.gabor_grain(1000.0, ms)
        G = np.abs(np.fft.rfft(g, 1 << 16))
        f = np.fft.rfftfreq(1 << 16, 1 / SR)
        above = f[G > 0.5 * G.max()]
        prods.append((above.max() - above.min()) * ms / 1000)
    assert max(prods) / min(prods) < 1.15 and 0.75 < np.mean(prods) < 0.95


def test_granular_freeze_keeps_pitch():
    t = np.arange(2 * SR) / SR
    src = np.sin(2 * np.pi * 300.0 * t)
    # grains spaced by a whole number of periods (75 a second: four periods of 300 Hz) add in phase
    y = F.grains(src, 1.0, 0.5, density=75, grain_ms=60, sync=True)["y"]
    assert F.measured_pitch(y, guess=300.0) == pytest.approx(300.0, rel=0.01)
    up = F.grains(src, 1.0, 0.5, density=75, grain_ms=60, pitch=1.5, sync=True)["y"]
    assert F.measured_pitch(up, guess=450.0) == pytest.approx(450.0, rel=0.01)


def test_harmonic_tracking_and_split():
    t = np.arange(SR) / SR
    f0, B = 220.0, 4e-4
    y = sum(np.exp(-t * k) / k * np.sin(2 * np.pi * k * f0 * np.sqrt(1 + B * k * k) * t) for k in range(1, 13))
    pf = F.partial_freqs(y, f0, 12)
    assert np.allclose(pf, [k * f0 * np.sqrt(1 + B * k * k) for k in range(1, 13)], rtol=2e-4)
    near, rest = F.split_partials(y, pf, f0)
    assert np.allclose(near + rest, y, atol=1e-6)
    assert 10 * np.log10(np.sum(rest ** 2) / np.sum(y ** 2)) < -20


def test_tuned_karplus_strong():
    for hz in (523.25, 1046.5, 2093.0):
        f = F.measured_pitch(F.ks_tuned(hz, 0.6), guess=hz)
        assert abs(1200 * np.log2(f / hz)) < 1.0
    assert abs(1200 * np.log2(SR / F.ks_loop_delay(2093.0, tuned=False) / 2093.0)) > 20


def test_waveguide_equals_finite_differences():
    s = STR.String.tuned(220.0)
    x = np.linspace(0, s.L, 101)
    sh = STR.pluck_shape(x, s.L, 0.2)
    run = STR.simulate(s, sh, 0.1, N=100, pickup=0.2371)
    wg = F.waveguide(sh, 0.1, run.sr, pickup=0.2371)
    assert np.max(np.abs(np.asarray(run.pickup) - wg)) < 1e-12


def test_clarinet_threshold_and_odd_harmonics():
    from explainer.music.monochord import dynamics as D
    quiet = F.clarinet(220.0, 0.4, pressure=0.4, breath=0.0, normalize=False)
    loud = F.clarinet(220.0, 0.4, pressure=0.85, breath=0.0, normalize=False)
    shut = F.clarinet(220.0, 0.4, pressure=1.25, breath=0.0, normalize=False)
    r = [np.sqrt(np.mean(y[int(0.25 * SR):] ** 2)) for y in (quiet, loud, shut)]
    assert r[1] > 50 * r[0] and r[1] > 50 * r[2]
    y = F.clarinet(220.0, 1.0)
    f = F.measured_pitch(y, guess=220.0)
    assert abs(1200 * np.log2(f / 220.0)) < 6
    h = D.harmonics(y[12000:], f, SR, 6)
    assert h[1] < -40 and h[3] < -40 and h[2] > -20


def test_modal_ideal_string_matches_dalembert():
    s = STR.String.tuned(220.0)
    x = np.linspace(0, s.L, 101)
    sh = STR.pluck_shape(x, s.L, 0.2)
    run = STR.simulate(s, sh, 0.1, N=100, pickup=0.2371)
    coef = STR.sine_coefficients(sh)
    md = F.modal_string(s.f1, 0.0, np.zeros(len(coef)), coef, 0.1, run.sr)
    a = np.asarray(run.pickup)
    assert np.max(np.abs(a - md)) / np.max(np.abs(a)) < 0.02
