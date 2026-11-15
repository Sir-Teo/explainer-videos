"""Monochord's transducers (Part 54): patterns, proximity, noise, lines, boxes against closed forms, crossovers, the
canceller and arrays.

    python -m pytest -q tests/music/test_transducer.py
"""

import math

import numpy as np
import pytest

from explainer.music.monochord import transducer as T

SR = 48000


def test_directivity():
    assert T.directivity(1.0)["DI"] == pytest.approx(0.0)
    assert T.directivity(0.5)["DI"] == pytest.approx(10 * math.log10(3), abs=1e-9)
    assert T.directivity(0.0)["DI"] == pytest.approx(10 * math.log10(3), abs=1e-9)
    As = np.linspace(0, 1, 1001)
    best = As[np.argmax([T.directivity(a)["DF"] for a in As])]
    assert best == pytest.approx(0.25, abs=1e-3) and T.directivity(0.25)["DF"] == pytest.approx(4.0)
    assert T.directivity(0.25)["null_deg"] == pytest.approx(109.47, abs=0.01)


def test_proximity():
    f = np.array([100.0])
    r = 0.05
    k = 2 * np.pi * 100 / T.C
    assert abs(T.proximity(f, r, 0.0)[0]) == pytest.approx(math.sqrt(1 + 1 / (k * r) ** 2))
    assert abs(T.proximity(np.array([1e5]), 1.0, 0.0)[0]) == pytest.approx(1.0, abs=1e-4)
    assert abs(T.proximity(f, r, 1.0)[0]) == pytest.approx(1.0)


def test_thermal_noise():
    assert T.thermal_noise(200.0) * 1e6 == pytest.approx(0.2545, abs=1e-3)


def test_balanced_line_rejects_common_mode():
    t = np.arange(SR) / SR
    s = np.sin(2 * np.pi * 440 * t)
    h = np.sin(2 * np.pi * 50 * t)
    assert np.allclose(T.balanced(s, h, 0.0), s)
    left = T.balanced(s, h, 0.01) - s
    assert np.max(np.abs(left)) == pytest.approx(0.01, rel=1e-6)


def test_sealed_box_matches_small():
    d = T.Driver()
    f = np.geomspace(10, 4000, 6000)
    for Vb in (0.02, 0.05, 0.2):
        r = T.response(d, f, {"kind": "sealed", "Vb": Vb})
        assert T.f_minus(f, r["spl"]) == pytest.approx(T.sealed_alignment(d, Vb)["f3"], rel=0.005)


def test_vented_b4_matches_thiele():
    d = T.Driver(Qes=0.383, Qms=1e6)
    b = T.vented_b4(d)
    f = np.geomspace(10, 4000, 6000)
    r = T.response(d, f, {"kind": "vented", "Vb": b["Vb"], "fb": b["fb"], "Ql": 1e6})
    assert T.f_minus(f, r["spl"]) == pytest.approx(b["f3"], rel=0.005)
    assert np.max(r["spl"][f > 50] - r["spl"][-1]) < 0.05


def test_impedance_peak_at_resonance():
    d = T.Driver()
    f = np.geomspace(10, 1000, 4000)
    Z = np.abs(T.response(d, f)["Z"])
    assert f[np.argmax(Z)] == pytest.approx(d.fs, rel=0.01)
    assert Z.max() == pytest.approx(d.Re * (1 + d.Qms / d.Qes), rel=0.01)


def test_crossovers():
    f = np.geomspace(100, 40000, 500)
    assert np.allclose(np.abs(T.crossover(f, "lr4")[2]), 1.0)
    assert abs(T.crossover(np.array([2000.0]), "bw2")[2][0]) < 1e-9
    assert 20 * np.log10(abs(T.crossover(np.array([2000.0]), "bw2_inv")[2][0])) == pytest.approx(3.01, abs=0.01)


def test_horn_cutoff():
    R, fc = T.horn_throat(np.array([50.0, 1e5]), 0.005, 4.0)
    assert R[0] == 0.0 and R[1] == pytest.approx(T.RHO * T.C / 0.005, rel=1e-3) and fc == pytest.approx(4 * T.C / (4 * np.pi))


def test_headphone_as_microphone_is_dull():
    hp = T.Driver(fs=110.0, Qes=1.2, Qms=2.5, Vas=0.00015, Sd=0.0011, Re=32.0)
    H = np.abs(T.headphone_as_mic(np.array([2000.0, 4000.0]), hp))
    assert 20 * np.log10(H[0] / H[1]) == pytest.approx(6.0, abs=0.5)


def test_fxlms_cancels_a_tone():
    t = np.arange(3 * SR) / SR
    x = np.sin(2 * np.pi * 100 * t)
    prim = np.zeros(50)
    prim[30] = 1.0
    d = np.convolve(x, prim)[: len(x)]
    sec = np.zeros(20)
    sec[5] = 0.8
    r = T.fxlms(d, x, sec, taps=32, mu=0.01)
    tail = slice(-SR, None)
    assert 10 * np.log10(np.mean(r["e"][tail] ** 2) / np.mean(d[tail] ** 2)) < -30


def test_array_gain():
    pos = np.arange(8) * 0.05
    assert T.array_gain(np.array([1000.0]), pos, 20.0, 20.0)[0] == pytest.approx(1.0)
    assert T.array_gain(np.array([4000.0]), pos, 0.0, 40.0)[0] < 0.2
