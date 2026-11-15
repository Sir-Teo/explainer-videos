"""Monochord's synthesizer (Part 51): oscillators, the ladder against its circuit, drums, fitting.

    python -m pytest -q tests/music/test_synth.py
"""

import numpy as np
import pytest

from explainer.music.monochord import dynamics as D
from explainer.music.monochord import synth as S

SR = 48000


def test_sawtooths_share_harmonics_and_differ_in_aliasing():
    f = 440.0
    for fn in (S.saw_polyblep, S.saw_blit, S.saw_additive):
        h = D.harmonics(fn(f, SR), f, SR, 5)
        assert np.allclose(h, 20 * np.log10(1 / np.arange(1, 6)), atol=0.3)
    al = [D.alias_energy(fn(f, SR), f, SR) for fn in (S.saw_naive, S.saw_polyblep, S.saw_blit, S.saw_additive)]
    assert al[0] > al[1] + 12 > al[2] + 12 and al[3] < -100


def test_naive_aliasing_grows_three_db_an_octave():
    a = [D.alias_energy(S.saw_naive(f, SR), f, SR) for f in (220.0, 440.0, 880.0)]
    assert np.allclose(np.diff(a), 3.0, atol=0.6)


def test_pulse_width_zeros():
    y = S.pulse(400.0, 0.25, SR)
    h = D.harmonics(y, 400.0, SR, 8)
    assert h[3] < -40 and h[7] < -40 and h[1] > -10
    assert abs(np.mean(y)) < 1e-3


def test_hard_sync_keeps_the_master_period():
    y = S.sync_saw(100.0, 370.0, 4800, 48000)
    assert np.allclose(y[:480], y[480:960], atol=1e-6)


def test_drawbars_are_tempered():
    r = S.drawbar_ratios(True)
    cents = 1200 * np.log2(np.array(r) / np.array(S.DRAWBAR_RATIOS))
    assert cents[4] == pytest.approx(-1.955, abs=0.01) and cents[6] == pytest.approx(13.686, abs=0.01)


def test_linear_ladder_response():
    assert S.ladder_response(1000.0, 0.0, [1000.0])[0] == pytest.approx(-12.04, abs=0.01)
    assert S.ladder_response(1000.0, 3.0, [1e-3])[0] == pytest.approx(-20 * np.log10(4), abs=1e-3)
    imp = np.zeros(8192)
    imp[0] = 1e-3
    y = S.ladder(imp, 1000.0, 0.0, oversample=4)
    Y = np.abs(np.fft.rfft(y))
    f = np.fft.rfftfreq(len(y), 1 / SR)
    i = np.argmin(abs(f - 1000.0))
    assert 20 * np.log10(Y[i] / Y[1]) == pytest.approx(-12.04, abs=0.6)


def test_ladder_models_converge_to_the_circuit():
    x = S.saw_polyblep(220.0, 2400)
    ref = S.ladder_ode(x, 1500.0, 3.0)

    def err(y):
        return 10 * np.log10(np.sum((y - ref) ** 2) / np.sum(ref ** 2))
    fw = [err(S.ladder(x, 1500.0, 3.0, oversample=r, half=False)) for r in (2, 4)]
    tz = [err(S.ladder_trap(x, 1500.0, 3.0, oversample=r)) for r in (1, 2)]
    assert fw[0] - fw[1] == pytest.approx(6.0, abs=1.5)
    assert tz[0] - tz[1] == pytest.approx(12.0, abs=1.5) and tz[0] < fw[1] - 10


def test_self_oscillation_near_cutoff():
    imp = np.zeros(SR)
    imp[0] = 0.01
    y = S.ladder(imp, 440.0, 4.3)[SR // 2:]
    zc = np.where((y[:-1] < 0) & (y[1:] >= 0))[0]
    f = (len(zc) - 1) / ((zc[-1] - zc[0]) / SR)
    assert abs(1200 * np.log2(f / 440.0)) < 25 and 0.01 < np.max(np.abs(y)) < 1.0
    quiet = S.ladder(imp, 440.0, 3.0)[SR // 2:]
    assert np.max(np.abs(quiet)) < 1e-6


def test_resonator_decay_matches_q():
    y = S.resonator(S.trigger(SR), 100.0, 50.0)
    tau = 2 * 50.0 / (2 * np.pi * 100.0)
    env = np.abs(y).reshape(-1, 480).max(axis=1)
    t = (np.arange(len(env)) + 0.5) * 0.01
    s = (t > 0.05) & (t < 0.6)
    assert -1 / np.polyfit(t[s], np.log(env[s]), 1)[0] == pytest.approx(tau, rel=0.03)


def test_fit_recovers_a_known_patch():
    f = 261.63
    r = S.fit_patch(S.patch(f, 8192, 1400.0, 2.0, 0.5), f)
    assert r["res"] == 2.0 and r["mix"] == 0.5 and r["cutoff"] == pytest.approx(1400.0, rel=0.05) and r["distance_db"] < 1.5


def test_wavetable_endpoints():
    tabs = S.make_tables()
    y0 = S.wavetable(130.81, tabs, 0.0, SR)
    assert D.harmonics(y0, 130.81, SR, 3)[1] < -100
    lim = S.make_tables(harmonics=19)
    f6 = 1046.5
    assert D.alias_energy(S.wavetable(f6, lim, 1.0, SR), f6, SR) < D.alias_energy(S.wavetable(f6, tabs, 1.0, SR), f6, SR) - 25
