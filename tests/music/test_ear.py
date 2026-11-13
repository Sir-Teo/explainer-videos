"""Monochord's ear (Part 4): each model against something that does not share its code.

    python -m pytest -q tests/music/test_ear.py
"""

import math

import numpy as np
import pytest

from explainer.music.monochord import ear
from explainer.music.monochord.dsp import fourier as F

SR = 48_000


def test_outer_and_middle_ear():
    assert 3000 < ear.canal_resonance() < 3700
    m = ear.middle_ear()
    assert m["pressure_gain"] == pytest.approx(22.3, abs=0.2) and m["gain_db"] == pytest.approx(27.0, abs=0.2)
    assert m["without"] < 0.02 < 0.2 < m["with"] < 0.4


def test_the_travelling_wave_sorts_frequencies_by_place():
    places = [ear.cochlea(f)["peak_x"] for f in (8000, 2000, 500, 200)]
    assert places == sorted(places)                                   # high notes at the base, low notes at the apex
    for f in (4000, 1000, 250):
        c = ear.cochlea(f)
        assert c["peak_x"] < c["resonant_x"]                          # the wave peaks before the place tuned to it
        assert abs(ear.cochlea(f, n=4000)["peak_x"] - c["peak_x"]) < 2e-4      # and the grid does not matter
        # past its peak the wave dies: almost nothing reaches the apex
        assert c["envelope"][-50:].max() < 1e-3 * c["peak"]
    # the phase of the wave only ever lags as it travels
    ph = np.unwrap(np.angle(ear.cochlea(1000)["displacement"]))
    k = int(np.argmax(ear.cochlea(1000)["envelope"]))
    assert np.all(np.diff(ph[20:k]) < 1e-6)
    # less friction, sharper tuning: the living ear against Bekesy's
    assert ear.sharpness(2000, 0.02) > 1.8 * ear.sharpness(2000, 0.08)


@pytest.mark.parametrize("hz", [200.0, 1000.0, 4000.0])
def test_a_gammatone_is_one_erb_wide(hz):
    g = ear.gammatone(hz, SR)
    n = 1 << 18
    h2 = np.abs(np.fft.rfft(g, n)) ** 2
    f = np.fft.rfftfreq(n, 1 / SR)
    width = h2.sum() * (f[1] - f[0]) / h2.max()
    assert width == pytest.approx(float(ear.erb(hz)), rel=0.03)
    assert float(ear.filter_response_db(hz, hz)[0]) == pytest.approx(0.0, abs=0.05)


def test_scales_of_the_ear():
    assert float(ear.erb(1000.0)) == pytest.approx(132.6, abs=0.2)
    assert float(ear.erb_number(1000.0)) == pytest.approx(15.6, abs=0.1)
    assert float(ear.bark(1000.0)) == pytest.approx(8.5, abs=0.1)
    c = ear.erb_space(100.0, 8000.0, 30)
    assert np.allclose(np.diff(ear.erb_number(c)), np.diff(ear.erb_number(c))[0])
    assert float(ear.greenwood(0.0)) == pytest.approx(20677, rel=0.01) and float(ear.greenwood(ear.COCHLEA_LENGTH)) == pytest.approx(19.8, abs=0.5)


def test_loudness_curves():
    # IEC 61672, table of A-weights
    for hz, want in ((1000, 0.0), (100, -19.1), (50, -30.2), (10000, -2.5), (4000, 1.0)):
        assert float(ear.a_weight_db(hz)) == pytest.approx(want, abs=0.15)
    t = ear.threshold_db(np.array([100.0, 1000.0, 3500.0, 10000.0]))
    assert t[2] < t[1] < t[0] and t[2] < 0 and t[3] > 10            # most sensitive where the ear canal resonates
    assert float(ear.sones(50)) == 2.0 and float(ear.sones(40)) == 1.0


def test_masking_is_strongest_near_the_masker():
    f = np.array([400.0, 800.0, 1000.0, 1200.0, 2000.0, 4000.0])
    m = ear.masked_threshold(1000.0, 70.0, f)
    assert int(np.argmax(m)) == 2 and m[2] == pytest.approx(66.0, abs=0.5)
    assert m[0] < 40 and m[-1] < 20


def harmonic(f0, numbers, seconds=0.25):
    t = np.arange(int(seconds * SR)) / SR
    return sum(np.sin(2 * np.pi * f0 * k * t) for k in numbers)


def test_the_pitch_model_hears_what_listeners_hear():
    f0 = 130.81
    assert ear.pitch(harmonic(f0, [1]), SR)[0] == pytest.approx(f0, rel=0.01)
    assert ear.pitch(harmonic(f0, range(1, 9)), SR)[0] == pytest.approx(f0, rel=0.01)
    assert ear.pitch(harmonic(f0, range(4, 9)), SR)[0] == pytest.approx(f0, rel=0.01)      # nothing at f0 in the air
    # Schouten's shifted residue: partials 4 to 8 of 200 Hz, all moved up by 30 Hz, sound a little above 200
    t = np.arange(int(0.25 * SR)) / SR
    y = sum(np.sin(2 * np.pi * (200.0 * k + 30.0) * t) for k in range(4, 9))
    p = ear.pitch(y, SR, lo=120, hi=400)[0]
    assert 202.0 < p < 208.0
    # fine timing is lost high up: a tone at 8 kHz gives the model little to go on
    lo, hi = ear.pitch(harmonic(500.0, [1]), SR)[1], ear.pitch(harmonic(8000.0, [1]), SR, lo=50, hi=1000)[1]
    assert lo > 0.5 and hi < 0.1 * lo


def test_shepard_tones_go_round():
    a, b = ear.shepard(0.0), ear.shepard(12.0)
    assert np.abs(a - b).max() < 1e-9                                   # twelve steps up is the same sound
    assert np.abs(ear.shepard(0.0) - ear.shepard(1.0)).max() > 0.1
    # and each one has energy only at octaves of its own pitch class
    y = ear.shepard(3.0, seconds=1.0)
    spec = np.abs(np.fft.rfft(y * F.window("hann", len(y))))
    f = np.fft.rfftfreq(len(y), 1 / SR)
    peaks = f[(spec > 0.05 * spec.max()) & (spec >= np.roll(spec, 1)) & (spec >= np.roll(spec, -1))]
    ratios = np.log2(peaks / (27.5 * 2 ** (3 / 12)))
    assert np.allclose(ratios, np.round(ratios), atol=0.02)


def test_the_noise_dose_and_the_active_oscillator():
    assert ear.safe_hours(85) == 8 and ear.safe_hours(100) == pytest.approx(0.25) and ear.safe_hours(94) == pytest.approx(1.0)
    r = ear.hopf_response(np.array([1e-6, 1e-3, 1.0]))
    slope = np.polyfit(np.log10([1e-6, 1e-3, 1.0]), np.log10(r), 1)[0]
    assert slope == pytest.approx(1 / 3, abs=1e-6)                      # a decibel in, a third of a decibel out
    # two tones in, a third tone out: 2 f1 - f2
    sr = 96_000
    t = np.arange(int(0.2 * sr)) / sr
    f1, f2 = 1000.0, 1200.0
    y = ear.hopf_run(3.0 * (np.cos(2 * np.pi * f1 * t) + np.cos(2 * np.pi * f2 * t)), sr, 800.0, mu=-1.0, scale=4000.0)
    seg = y[len(y) // 2:]
    spec = np.abs(np.fft.rfft(seg * np.hanning(len(seg))))
    f = np.fft.rfftfreq(len(seg), 1 / sr)
    at = lambda hz: spec[np.abs(f - hz) < 15].max()
    assert at(2 * f1 - f2) > 20 * at(700.0)                             # a clear line at 800 Hz, which nobody played
