"""Monochord's nonlinear and time-varying effects (Part 50): shapers, dynamics, time and pitch.

    python -m pytest -q tests/music/test_dynamics.py
"""

import numpy as np
import pytest

from explainer.music.monochord import dynamics as D

SR = 48000


def test_chebyshev_identity_and_exact_harmonics():
    th = np.linspace(0, np.pi, 50)
    for n in range(6):
        assert np.allclose(D.chebyshev(n, np.cos(th)), np.cos(n * th))
    x = np.cos(2 * np.pi * 1000 * np.arange(SR) / SR)
    h = D.harmonics(D.cheb_shaper([1.0, 0.0, 0.5], x), 1000, SR, 3)
    assert h[2] == pytest.approx(-6.02, abs=0.05) and h[1] < -150


def test_odd_shapers_make_odd_harmonics():
    x = np.cos(2 * np.pi * 500 * np.arange(SR) / SR)
    for k in ("hard", "tanh", "cubic"):
        h = D.harmonics(D.shape(x, k, 3.0), 500, SR, 6)
        assert h[1] < -100 and h[3] < -100 and h[2] > -30


def test_oversampling_beats_plain_on_aliasing():
    from scipy.signal import resample_poly
    t = np.arange(SR) / SR
    x = 0.9 * np.sin(2 * np.pi * 3733 * t)
    plain = D.alias_energy(np.tanh(4 * x), 3733, SR)
    os8 = D.alias_energy(resample_poly(np.tanh(4 * resample_poly(x, 8, 1)), 1, 8), 3733, SR)
    assert os8 < plain - 10 and D.alias_energy(D.adaa_tanh(x, 4), 3733, SR) < plain


def test_static_curve():
    y = D.static_curve(np.array([-40.0, -20.0, 0.0]), -20, 4, 0)
    assert y.tolist() == pytest.approx([-40.0, -20.0, -15.0])


def test_compressor_reaches_its_static_gain():
    t = np.arange(SR) / SR
    x = 0.8 * np.sin(2 * np.pi * 440 * t)
    r = D.compressor(x, SR, -20, 4, 0, 5, 100)
    lvl = 20 * np.log10(0.8)
    assert r["gr_db"][-1] == pytest.approx(lvl - D.static_curve(np.array([lvl]), -20, 4, 0)[0], abs=0.3)


def test_yin_finds_a_tone():
    t = np.arange(SR // 2) / SR
    x = np.sin(2 * np.pi * 220 * t) + 0.5 * np.sin(2 * np.pi * 440 * t)
    _, f0, _ = D.yin(x, SR)
    assert np.median(f0[f0 > 0]) == pytest.approx(220, rel=0.005)


def test_psola_shifts_pitch_and_keeps_length():
    t = np.arange(SR) / SR
    x = sum(np.sin(2 * np.pi * 200 * k * t) / k for k in range(1, 8))
    tt, f0, _ = D.yin(x, SR)
    y = D.psola(x, SR, tt, f0, np.full(len(tt), 1.5))
    _, f2, _ = D.yin(y, SR)
    assert len(y) == len(x) and np.median(f2[f2 > 0]) == pytest.approx(300, rel=0.02)


def test_phase_vocoder_stretches_and_keeps_pitch():
    t = np.arange(SR) / SR
    x = np.sin(2 * np.pi * 330 * t)
    y = D.pv_stretch(x, 2.0)
    assert len(y) / len(x) == pytest.approx(2.0, rel=0.05)
    _, f, _ = D.yin(y[SR // 2: SR], SR)
    assert np.median(f[f > 0]) == pytest.approx(330, rel=0.01)


def test_correct_snaps_to_the_scale():
    f = np.array([270.0, 300.0, 380.0])
    out = D.correct(f, np.arange(3) * 0.01)
    assert out == pytest.approx([261.6256, 293.6648, 391.9954], rel=1e-4)
