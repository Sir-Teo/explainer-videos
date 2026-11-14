"""Monochord's chromatic toolkit (Part 19) against hand-checked theory.

    python -m pytest -q tests/music/test_chromatic.py
"""

from fractions import Fraction

import pytest

from explainer.music.monochord import chromatic as X


def test_spellings_of_the_chromatic_chords():
    assert X.applied_dominant(7) == (2, 6, 9, 0)                     # V7 of V in C: D F♯ A C
    assert X.neapolitan(0) == (1, 5, 8)                               # D♭ F A♭
    six = X.augmented_sixths(0)
    assert six == {"Italian": (8, 0, 6), "French": (8, 0, 2, 6), "German": (8, 0, 3, 6)}
    assert set(six["German"]) == set(X.triad(8, "7"))                 # the German sixth is A♭7 on the keyboard
    assert X.german_as_dominant(0)["same"]


def test_the_diminished_seventh_opens_eight_keys_and_three_share_all_24():
    d = X.dim7(11)
    assert sorted(d) == [2, 5, 8, 11]
    keys = [r["key"] for r in X.dim7_resolutions(d)]
    assert len(set(keys)) == 8 and {k[0] for k in keys} == {0, 3, 6, 9}
    every = [r["key"] for root in (11, 0, 1) for r in X.dim7_resolutions(X.dim7(root))]
    assert len(every) == 24 and set(every) == set(X.KEYS)


def test_pure_thirds_do_not_close_the_octave():
    e = X.enharmonic_drift()
    assert e["four minor thirds"] == pytest.approx(62.565, abs=0.01)
    assert e["three major thirds"] == pytest.approx(-41.059, abs=0.01) and e["diesis"] == pytest.approx(41.059, abs=0.01)
    assert X.pure_cycle(Fraction(3, 2), 12) == pytest.approx(23.46, abs=0.01)        # the Pythagorean comma (Part 6)


def test_plr_hexatonic_and_voice_leading():
    cyc = X.hexatonic((0, "major"))
    assert cyc == [(0, "major"), (0, "minor"), (8, "major"), (8, "minor"), (4, "major"), (4, "minor"), (0, "major")]
    assert all(X.voice_leading(X.triad(*a), X.triad(*b))["cost"] == 1 for a, b in zip(cyc, cyc[1:]))
    assert X.voice_leading(X.triad(0, "major"), X.triad(4, "major"))["cost"] == 2   # C to E: one held, two by a semitone
    assert X.tristan_voice_leading()["cost"] == 2


def test_the_pathfinder():
    piv = X.distances((0, "major"), chromatic=False)
    door = X.distances((0, "major"), chromatic=True)
    count = lambda d, s: sum(1 for v in d["dist"].values() if v == s)            # noqa: E731
    assert (count(piv, 1), count(piv, 2)) == (11, 12) and (count(door, 1), count(door, 2)) == (19, 4)
    assert door["dist"][(6, "major")] == 1 and door["routes"][(6, "major")][0][2] == "a diminished seventh, respelled"
    assert door["dist"][(1, "major")] == 1                              # through the German sixth
    for k, r in door["routes"].items():                                 # every route is a chain of real edges
        for a, b, how in r:
            assert X.edges(a, True)[b] == how


def test_lerdahl_distance():
    C = (0, "major")
    assert X.chord_distance((0, "major", C), (7, "major", C)) == 5      # Lerdahl's I to V
    assert X.chord_distance((0, "major", C), (9, "minor", C)) == 7
    assert X.chord_distance((0, "major", C), (2, "minor", C)) == 8
    assert X.chord_distance((0, "major", C), (0, "major", C)) == 0
    assert X.tension_curve([(0, "major", C), (7, "major", C), (0, "major", C)]) == [0, 5, 5]
