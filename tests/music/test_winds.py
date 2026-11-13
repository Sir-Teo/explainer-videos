"""Monochord's wind instruments against textbook values.

    python -m pytest -q tests/music/test_winds.py
"""

import math

import numpy as np
import pytest

from explainer.music.monochord.instruments import winds as W


def cents(a, b):
    return 1200 * math.log2(a / b)


def test_pipes_resonate_where_the_textbook_says():
    length, a = 0.60, 0.0075
    stopped = [f for f, _ in W.cylinder(length, a).peaks(2500)]
    f1 = W.C / (4 * (length + 0.6133 * a))
    for n, f in zip((1, 3, 5, 7), stopped):                              # closed at the reed: odd multiples of c/4L
        assert abs(cents(f, n * f1)) < 40
    assert stopped[0] < f1                                               # wall losses slow the wave a little
    a = 0.0095
    flute = [f for f, _ in W.cylinder(length, a).peaks(2500, admittance=True)]
    f1 = W.C / (2 * (length + 2 * 0.6133 * a))
    for n, f in zip((1, 2, 3, 4), flute):                                # open at both ends: every multiple of c/2L
        assert abs(cents(f, n * f1)) < 15


def test_a_cone_has_every_harmonic():
    f = [p[0] for p in W.cone(0.60, 0.0015, 0.02).peaks(2500)]
    x1 = 0.0015 * 0.60 / (0.02 - 0.0015)
    f1 = W.C / (2 * (0.60 + x1 + 0.6133 * 0.02))                         # as if open at both ends, measured from the apex
    assert abs(cents(f[0], f1)) < 30
    assert all(abs(cents(fk, (k + 1) * f[0])) < 40 for k, fk in enumerate(f[:5]))


def test_a_trumpet_is_a_stopped_pipe_bent_into_a_harmonic_series():
    plain = [p[0] for p in W.cylinder(1.37, 0.0058).peaks(1600)]
    assert abs(plain[1] / plain[0] - 3) < 0.1 and abs(plain[2] / plain[0] - 5) < 0.15      # odd multiples
    peaks = W.trumpet().peaks(1600)
    f0, off = W.harmonicity(peaks, lowest=2, count=6)
    assert 112 < f0 < 122                                                # a B flat trumpet: 116.5 Hz
    assert max(abs(c) for c in off) < 40                                 # peaks 2 to 7 are near 2 f0 ... 7 f0
    assert peaks[0][0] < 0.75 * f0                                       # and the first is far too low: the pedal note has no peak


def test_the_reed_valve():
    dp = np.linspace(0, 1.2, 1201)
    u = W.reed_flow(dp)
    assert dp[int(np.argmax(u))] == pytest.approx(1 / 3, abs=0.002) and u[-1] == 0.0
    bore = W.clarinet()
    f1 = bore.peaks(600)[0][0]
    quiet = W.playing(W.reed_tone(bore, 0.30, 0.8)["p"])
    assert quiet["amp"] < 1e-3                                           # below a third of the closing pressure: silence
    note = W.playing(W.reed_tone(bore, 0.45, 0.8)["p"])
    assert note["amp"] > 0.2 and abs(cents(note["hz"], f1)) < 30
    h = note["harmonics_db"]
    assert h[1] < -35 and h[3] < -35 and -14 < h[2] < -8                 # a square wave: odd harmonics, the third near -9.5 dB
    soft, loud = W.playing(W.reed_tone(bore, 0.37, 1.0)["p"]), W.playing(W.reed_tone(bore, 0.6, 1.0)["p"])
    assert soft["harmonics_db"][4] < loud["harmonics_db"][4] - 5         # blown harder, it is brighter as well as louder


def test_a_register_hole_gives_the_twelfth():
    low = W.playing(W.reed_tone(W.clarinet(), 0.45, 0.8)["p"])["hz"]
    high = W.playing(W.reed_tone(W.clarinet(register_hole=True), 0.45, 0.8)["p"])["hz"]
    assert abs(cents(high, 3 * low)) < 80                                # three times the frequency: an octave and a fifth


def test_a_reed_on_a_cone_has_every_harmonic():
    sax = W.saxophone(0.60)
    f = [p[0] for p in sax.peaks(1500)]
    assert abs(f[1] / f[0] - 2) < 0.05 and abs(f[2] / f[0] - 3) < 0.1     # the mouthpiece stands in for the missing tip
    note = W.playing(W.reed_tone(sax, 0.45, 0.7, zeta=0.9)["p"], tail=0.2)
    assert abs(cents(note["hz"], f[0])) < 40 and note["harmonics_db"][1] > -8      # the second harmonic is strong: not a clarinet


def test_lips_choose_a_resonance():
    tr = W.trumpet()
    peaks = [p[0] for p in tr.peaks(1200)]
    for f_lip, k in ((190.0, 1), (280.0, 2), (360.0, 3), (450.0, 4)):
        r = W.playing(W.lip_tone(tr, f_lip, 0.7)["p"], tail=0.2)
        assert r["amp"] > 0.3 and r["hz"] > f_lip                        # an outward valve sounds above its own frequency
        assert abs(cents(r["hz"], peaks[k])) < 60                        # and close to a resonance of the tube


def test_a_flute_overblows_the_octave():
    low = W.playing(W.jet_tone(262.0, 1.0, pressure=1.0))
    high = W.playing(W.jet_tone(262.0, 1.0, pressure=3.0))
    assert abs(cents(low["hz"], 262.0)) < 10 and abs(cents(high["hz"], 524.0)) < 15
    assert low["harmonics_db"][1] < -10                                  # a mild tone: mostly its fundamental


def test_the_voice():
    for v in ("a", "i", "u"):
        y = W.voice(110.0, W.VOWELS[v], 1.0)
        f = np.fft.rfftfreq(len(y), 1 / W.SR)
        sp = np.abs(np.fft.rfft(y * np.hanning(len(y))))
        for target in W.VOWELS[v]:                                       # the strongest harmonic near each formant is within one harmonic of it
            band = (f > target - 250) & (f < target + 250)
            assert abs(f[band][int(np.argmax(sp[band]))] - target) <= 110
    neutral = W.tract_formants(W.two_tube("neutral"))
    assert neutral[1] / neutral[0] == pytest.approx(3, abs=0.05) and neutral[2] / neutral[0] == pytest.approx(5, abs=0.1)
    assert 450 < neutral[0] < 500                                        # 17.5 cm: c/4L is 490 Hz, less the end correction
    a, i = W.tract_formants(W.two_tube("a")), W.tract_formants(W.two_tube("i"))
    assert all(abs(cents(x, y)) < 100 for x, y in zip(a, W.VOWELS["a"])) and all(abs(cents(x, y)) < 100 for x, y in zip(i, W.VOWELS["i"]))
    f1, f2, f3 = W.overtone_formants(10, 160.0)
    assert f2 < 1600 < f3 and f3 - f2 < 60 and f1 < 450
