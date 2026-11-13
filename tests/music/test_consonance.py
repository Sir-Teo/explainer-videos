"""Monochord's consonance layer against what it is supposed to reproduce: Euler's table, Plomp and Levelt's curve as
Sethares fitted it, his minima for a harmonic tone, and the fundamental bass of a chord.

    python -m pytest -q tests/music/test_consonance.py
"""

from fractions import Fraction

import numpy as np
import pytest

from explainer.music.monochord import consonance as K


def test_eulers_table():
    want = {"octave": 2, "fifth": 4, "fourth": 5, "major third": 7, "major sixth": 7, "minor third": 8, "minor sixth": 8,
            "major second": 8, "minor seventh": 9, "major seventh": 10, "minor second": 11, "tritone": 14}
    for name, g in want.items():
        assert K.euler_gradus(*K.JUST[name]) == g, name
    assert K.euler_gradus(6, 4) == K.euler_gradus(3, 2)                 # lowest terms


def test_galileos_pulses_and_tenney():
    assert K.coincidence(2, 1) == Fraction(2, 3) and K.coincidence(3, 2) == Fraction(2, 5)
    order = sorted(K.JUST, key=lambda n: K.tenney(*K.JUST[n]))
    assert order[:4] == ["unison", "octave", "fifth", "fourth"] and order[-1] == "tritone"


def test_beats():
    y, env = K.beating(440.0, 444.0, 1.0)
    assert K.beat_rate(440.0, 444.0) == 4.0
    assert np.all(np.abs(y) <= env + 1e-9)                              # the envelope really bounds the wave
    zeros = np.sum((env[1:-1] < env[:-2]) & (env[1:-1] <= env[2:]))
    assert zeros == 4                                                   # four silences in a second


def test_the_plomp_levelt_curve():
    x = np.linspace(0, 8, 8001)
    c = K.pl_curve(x)
    assert c[0] == 0 and x[int(np.argmax(c))] == pytest.approx(1.0, abs=0.01) and c.max() == pytest.approx(1.0, abs=1e-6)
    assert c[-1] < 0.02
    for f in (250.0, 1000.0, 4000.0):
        d = np.linspace(0, 400, 40001)
        r = K.pair_roughness(f, f + d)
        assert d[int(np.argmax(r))] == pytest.approx(K.worst_separation(f), rel=0.01)
    # the roughest separation is about a quarter of the ear's band (Part 4's ERB), within a factor of 1.5
    from explainer.music.monochord import ear
    assert 0.2 < K.worst_separation(1000.0) / float(ear.erb(1000.0)) < 0.4


def test_sethares_minima_for_a_harmonic_tone():
    r = np.linspace(1.0, 2.3, 2601)
    found = K.minima(r, K.dissonance_curve(r), depth=0.01)
    want = [7 / 6, 6 / 5, 5 / 4, 4 / 3, 7 / 5, 3 / 2, 5 / 3, 7 / 4, 2.0]
    assert len(found) == len(want)
    assert all(abs(a - b) < 0.004 for a, b in zip(found, want))         # the just ratios, from a curve that knows no ratios


def test_the_minima_move_with_the_timbre():
    r = np.linspace(1.0, 2.3, 2601)
    found = K.minima(r, K.dissonance_curve(r, stretch=2.1), depth=0.01)
    assert found[-1] == pytest.approx(2.1, abs=0.003)
    assert K.dyad_roughness(2.0, stretch=2.1) > 8 * K.dyad_roughness(2.1, stretch=2.1)   # the true octave is now rough
    assert K.dyad_roughness(2.1) > 8 * K.dyad_roughness(2.0)                             # and for a harmonic tone the reverse
    f, _ = K.harmonic_partials(100.0, 4, stretch=2.1)
    assert f[1] == pytest.approx(210.0) and f[3] == pytest.approx(441.0)


def test_triads():
    major, minor = (1, 5 / 4, 3 / 2), (1, 6 / 5, 3 / 2)
    assert K.chord_roughness(major) == pytest.approx(K.chord_roughness(minor), rel=0.03)   # the same three intervals
    assert K.fundamental_bass([(1, 1), (5, 4), (3, 2)]) == Fraction(1, 4)
    assert K.fundamental_bass([(1, 1), (6, 5), (3, 2)]) == Fraction(1, 10)
    assert K.fundamental_bass([(1, 1), (3, 2)]) == Fraction(1, 2)


def test_the_ear_model_finds_the_fundamental_bass():
    f0 = 261.63
    for chord, div in (((1, 3 / 2), 2), ((1, 4 / 3), 3), ((1, 5 / 4), 4), ((1, 5 / 4, 3 / 2), 4)):
        hz, strength = K.harmonicity(chord, f0)
        assert hz == pytest.approx(f0 / div, rel=0.01) and strength > 0.4
    assert K.harmonicity((1, 2.0), f0)[1] > K.harmonicity((1, 3 / 2), f0)[1] > K.harmonicity((1, 5 / 4), f0)[1]
