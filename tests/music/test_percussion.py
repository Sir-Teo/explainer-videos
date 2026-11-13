"""Monochord's drums, bars and bells against textbook values.

    python -m pytest -q tests/music/test_percussion.py
"""

import math

import numpy as np
import pytest

from explainer.music.monochord.instruments import percussion as P


def test_a_round_skin_follows_bessel():
    modes = P.drum_modes(6)
    assert [(r["m"], r["n"]) for r in modes] == [(0, 1), (1, 1), (2, 1), (0, 2), (3, 1), (1, 2)]
    assert [round(r["ratio"], 3) for r in modes] == [1.0, 1.593, 2.136, 2.295, 2.653, 2.917]
    centre = P.strike_amounts(modes, 0.0)
    assert centre[0] > 0.99 and centre[1] < 1e-9 and centre[2] < 1e-9 and centre[3] > 0.99      # a blow at the centre: only m = 0
    u = P.drum_shape(1, 1, 81)
    assert np.isnan(u[0, 0]) and abs(u[40, 40]) < 1e-9                    # one nodal diameter passes through the middle


def test_two_drums_one_spectrum():
    assert P.polygon_area(P.GWW_1) == P.polygon_area(P.GWW_2) == 3.5
    assert P.polygon_perimeter(P.GWW_1) == pytest.approx(P.polygon_perimeter(P.GWW_2))
    a, b = P.membrane_eigs(P.GWW_1, 8, 16), P.membrane_eigs(P.GWW_2, 8, 16)
    assert np.allclose(a, b, rtol=1e-9)                                   # different shapes, the same notes
    fine = P.membrane_eigs(P.GWW_1, 3, 32) / 4.0                          # Driscoll's drums are twice the size
    assert fine == pytest.approx([2.53794, 3.65551, 5.17556], rel=3e-3)   # Driscoll (1997)
    square = P.membrane_eigs([(0, 0), (1, 0), (1, 1), (0, 1)], 3, 24)
    assert square == pytest.approx([2 * np.pi ** 2, 5 * np.pi ** 2, 5 * np.pi ** 2], rel=5e-3)
    lam = 300.0                                                           # Weyl: the count goes as the area
    assert abs(P.weyl(3.5, P.polygon_perimeter(P.GWW_1), lam) - np.sum(P.membrane_eigs(P.GWW_1, 70, 16) < lam)) < 4


def test_a_loaded_skin_is_nearly_harmonic():
    assert P.loaded_membrane(0.4, 1.0, 0, 3) == pytest.approx([2.4048, 5.5201, 8.6537], abs=2e-3)       # no load: Bessel again
    rows = P.tabla_modes(0.4, 9.76)                                       # Ramakrishna and Sondhi's patch
    ratios = [r["ratio"] for r in rows]
    assert P.harmonic_misfit(ratios) < 70                                 # every whole number up to 5 has a mode within 70 cents
    assert P.harmonic_misfit([r["ratio"] for r in P.drum_modes(9)]) > 250  # a bare skin misses by a minor third
    assert [(r["m"], r["n"]) for r in rows[:5]] == [(0, 1), (1, 1), (2, 1), (0, 2), (3, 1)]
    assert abs(ratios[2] - 3) < 0.1 and abs(ratios[3] - 3) < 0.1          # two modes share the third harmonic, as Raman found


def test_air_slows_the_low_modes_of_a_kettledrum():
    rows = P.air_loaded()
    plain, loaded = [r["plain_ratio"] for r in rows], [r["loaded_ratio"] for r in rows]
    assert plain[1] == pytest.approx(1.34, abs=0.005) and all(b > a for a, b in zip(plain[1:], loaded[1:]))
    assert all(a < b <= c + 0.3 for a, b, c in zip(plain[1:], loaded[1:], P.TIMPANI_MEASURED[1:]))      # towards 1.5, 2, 2.5


def test_bars():
    assert P.bar_modes(np.ones(240), count=4) == pytest.approx(P.UNIFORM_BAR, rel=1e-3)
    m = P.tune_bar(4.0)
    assert m["ratios"][1] == pytest.approx(4.0, abs=1e-3) and m["ratios"][2] == pytest.approx(10.0, abs=0.15)      # a marimba: 1 : 4 : 10
    assert m["lowered"] < 0.5                                             # and the cut lowers the bar by more than an octave
    x = P.tune_bar(3.0)
    assert x["ratios"][1] == pytest.approx(3.0, abs=1e-3) and x["depth"] < m["depth"]              # a xylophone: 1 : 3, a shallower cut
    long, short = P.bar_modes(np.ones(120), length=1.0, count=1)[0], P.bar_modes(np.ones(120), length=0.5, count=1)[0]
    assert long == pytest.approx(1.0, rel=1e-3)                           # the unit is the uniform bar itself; length enters as 1/L^2


def test_bells_plates_and_gongs():
    p = P.bell_partials(262.0)
    r = {q["name"]: q["ratio"] for q in p}
    assert r["hum"] == 0.5 and r["tierce"] == 1.2 and r["nominal"] == 2.0 and r["twelfth"] == 3.0
    assert {q["name"]: q["ratio"] for q in P.bell_partials(262.0, 1.25)}["tierce"] == 1.25
    assert abs(P.bell(262.0, 1.0)).max() == pytest.approx(1.0)
    c = P.chladni(1, 3, -1, 101)
    assert abs(c[50, 50]) < 1e-9 and np.allclose(c, -c.T)                 # antisymmetric: the diagonals are nodal lines
    assert P.chladni_pitch(1, 3) == 10.0
    t = np.array([0.0, 5.0])
    assert P.gong_pitch(200.0, 0.1, t)[0] == pytest.approx(220.0) and P.gong_pitch(200.0, 0.1, t)[1] == pytest.approx(200.0, abs=0.01)
    assert P.gong_pitch(200.0, -0.1, t)[0] == pytest.approx(180.0)
    for y in (P.marimba(262.0), P.steelpan(262.0), P.drum(110.0), P.drum(110.0, tuned="timpani"), P.gong(200.0)):
        assert np.isfinite(y).all() and abs(y).max() == pytest.approx(1.0)
    assert P.mallet([100.0], 1.0)[0] > P.mallet([900.0], 1.0)[0]         # a longer contact leaves out the high partials
