"""Monochord's scales (Part 12): stacks of fifths, modes, evenness, interval vectors, necklaces, parent scales.

    python -m pytest -q tests/music/test_scales.py
"""

from fractions import Fraction
from itertools import combinations

import numpy as np
import pytest

from explainer.music.monochord import scales as S


def test_stacks_of_fifths_and_their_gaps():
    assert [len(S.gap_sizes(S.stack(n))) for n in range(2, 14)] == [2, 2, 3, 2, 3, 2, 3, 3, 3, 3, 2, 3]      # two sizes at 2, 3, 5, 7, 12
    assert S.moments(60) == [2, 3, 5, 7, 12, 17, 29, 41, 53]
    five, seven, twelve = S.gap_sizes(S.stack(5)), S.gap_sizes(S.stack(7)), S.gap_sizes(S.stack(12))
    assert five == pytest.approx([294.13, 203.91], abs=0.01)                    # a minor third and a tone
    assert seven == pytest.approx([203.91, 90.22], abs=0.01)                    # a tone and a Pythagorean semitone
    assert twelve == pytest.approx([113.69, 90.22], abs=0.01)                   # two semitones, a comma apart
    assert twelve[0] - twelve[1] == pytest.approx(23.46, abs=0.01)
    for n in range(2, 60):                                                      # the three-gap theorem
        assert len(S.gap_sizes(S.stack(n))) <= 3
    g = np.round(S.gaps(S.stack(7, start=1))).astype(int)                       # from one fifth below: the white keys from C
    assert list(g) == [204, 204, 90, 204, 204, 204, 90]


def test_modes_and_brightness():
    assert S.MODES["Ionian"] == (2, 2, 1, 2, 2, 2, 1) and S.MODES["Aeolian"] == S.NAMED["natural minor"]
    order = [name for name, _ in S.by_brightness()]
    assert order == ["Lydian", "Ionian", "Mixolydian", "Dorian", "Aeolian", "Phrygian", "Locrian"]
    assert [S.fifths_position(nm) for nm in order] == list(range(7))            # brightness is the tonic's place in the chain of fifths
    notes = [S.pcs(s) for _, s in S.by_brightness()]
    for a, b in zip(notes, notes[1:]):                                          # each is the last with one note a semitone lower
        diff = [(x, y) for x, y in zip(a, b) if x != y]
        assert len(diff) == 1 and diff[0][0] - diff[0][1] == 1
    assert [S.brightness(s) for _, s in S.by_brightness()] == [39, 38, 37, 36, 35, 34, 33]


def test_the_diatonic_is_even_two_sized_and_deep():
    white = S.pcs(S.MAJOR)
    assert S.steps_necklace(S.steps_of(S.maximally_even(7))) == S.steps_necklace(S.MAJOR)
    assert S.steps_necklace(S.steps_of(S.maximally_even(5))) == S.steps_necklace(S.NAMED["pentatonic"])
    assert S.steps_of(S.maximally_even(6)) == S.NAMED["whole-tone"] and S.steps_of(S.maximally_even(8)) in (S.NAMED["octatonic"], S.rotate(S.NAMED["octatonic"], 1))
    assert S.is_maximally_even(white) and not S.is_maximally_even(S.pcs(S.NAMED["harmonic minor"]))
    sevens = [c for c in combinations(range(12), 7)]
    best = max(S.evenness(c) for c in sevens)
    assert S.evenness(white) == pytest.approx(best) and S.evenness(S.pcs(S.NAMED["melodic minor"])) < best
    assert S.interval_vector(white) == (2, 5, 4, 3, 6, 1) and S.is_deep(white)
    assert S.interval_vector(S.pcs(S.NAMED["whole-tone"])) == (0, 6, 0, 6, 0, 3) and not S.is_deep(S.pcs(S.NAMED["melodic minor"]))
    assert [S.common_tones(white, t) for t in (7, 5, 2, 1, 6)] == [6, 6, 5, 2, 2]     # a fifth away, one note changes
    assert S.has_myhill(S.MAJOR) and S.has_myhill(S.NAMED["pentatonic"]) and not S.has_myhill(S.NAMED["harmonic minor"])
    assert S.myhill(S.MAJOR)[2] == [1, 2] and S.myhill(S.MAJOR)[4] == [5, 6] and S.myhill(S.MAJOR)[5] == [6, 7]
    assert [S.transpositions(S.pcs(S.NAMED[k])) for k in ("major", "whole-tone", "octatonic", "chromatic")] == [12, 2, 3, 1]


def test_every_shape_of_scale():
    assert S.burnside(12) == 352 and len(S.necklaces(12)) == 352
    assert S.burnside(12) == Fraction(2 ** 12 + 2 ** 6 + 2 * 2 ** 4 + 2 * 2 ** 3 + 2 * 2 ** 2 + 4 * 2, 12)
    c = S.classify(12)
    assert [c[k] for k in range(13)] == [1, 1, 6, 19, 43, 66, 80, 66, 43, 19, 6, 1, 1]
    sevens = [s for s in S.necklaces(12) if len(s) == 7]
    plain = [s for s in sevens if set(s) <= {1, 2}]                             # only whole and half steps
    assert len(plain) == 3 and S.steps_necklace(S.MAJOR) in plain and S.steps_necklace(S.NAMED["melodic minor"]) in plain
    apart = [s for s in plain if not any(a == 1 and b == 1 for a, b in zip(s, s[1:] + s[:1]))]
    best = max(apart, key=lambda s: S.evenness(S.pcs(s)))
    assert best == S.steps_necklace(S.MAJOR)
    fifths = {s: S.interval_vector(S.pcs(s))[4] for s in sevens}
    assert max(fifths.values()) == 6 and [s for s, v in fifths.items() if v == 6] == [S.steps_necklace(S.MAJOR)]      # only the diatonic has six fifths
    for n in (5, 6, 7, 8):
        assert S.burnside(n) == len(S.necklaces(n))


def test_tetrachords_and_melakartas():
    t = S.tetrachords()
    assert len(t) == 6 and (2, 2, 1) in t and (1, 3, 1) in t and all(sum(x) == 5 for x in t)
    m = S.melakartas()
    assert len(m) == 72 and len(set(m)) == 72
    assert S.pcs(S.MAJOR) in m and S.pcs(S.NAMED["harmonic minor"]) in m and (0, 1, 4, 5, 7, 8, 11) in m      # Mayamalavagowla
    assert S.pcs(S.NAMED["double harmonic"]) == (0, 1, 4, 5, 7, 8, 11)
    assert sum(1 for x in m if S.steps_necklace(S.steps_of(x)) == S.steps_necklace(S.MAJOR)) == 6             # six of the seven modes have a fifth above the tonic
