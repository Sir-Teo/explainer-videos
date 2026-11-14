"""Monochord's bronze and silk (Part 36)."""

from fractions import Fraction

import numpy as np

from explainer.music.monochord import bronze as B


def test_bell_two_tones():
    a = B.two_tone_bell(400.0, "a", seconds=1.0)
    b = B.two_tone_bell(400.0, "b", seconds=1.0)
    n = len(a)
    fr = np.fft.rfftfreq(8 * n, 1 / 48000)
    pa = fr[np.argmax(np.abs(np.fft.rfft(a * np.hanning(n), 8 * n)) * (fr < 600))]
    pb = fr[np.argmax(np.abs(np.fft.rfft(b * np.hanning(n), 8 * n)) * (fr < 600))]
    assert abs(pa - 400) < 1 and abs(1200 * np.log2(pb / pa) - 300) < 3


def test_lu_and_fifths():
    lu = B.sanfen_lu(12)
    assert lu[1]["length"] == 54 and lu[2]["length"] == 72
    assert sorted(round(x["cents"]) for x in lu[:5]) == [0, 204, 408, 702, 906]
    best = sorted(B.fifths_closeness(60), key=lambda r: abs(r["gap"]))[0]
    assert best["n"] == 53 and best["octaves"] == 31 and abs(best["gap"] - 3.615) < 0.01
    assert B.modes()["yu"] == [0, 300, 500, 700, 1000]


def test_qin_and_gamelan():
    assert [h.denominator for h in B.HUI] == [8, 6, 5, 4, 3, 5, 2, 5, 3, 4, 5, 6, 8]
    assert B.qin_harmonic(100, Fraction(2, 5))["partial"] == 5
    assert [round(x, 2) for x in B.bar_partials(3)] == [1.0, 2.76, 5.4]
    cs, d = B.dissonance_curve([1, 2, 3, 4, 5, 6])
    m = B.minima(cs, d)
    assert any(abs(x - 702) < 4 for x in m) and any(abs(x - 1200) < 4 for x in m)
    cs, d = B.dissonance_curve(B.bar_partials(4))
    assert not any(abs(x - 1200) < 10 for x in B.minima(cs, d))                       # an ideal bar has no octave minimum
    col = B.colotomic("lancaran")
    assert col[15] == ["gong", "kenong"] and sum(1 for c in col if "ketuk" in c) == 8
    a, b = B.interlock(list(range(16)))
    assert all((x is None) != (y is None) for x, y in zip(a, b))
