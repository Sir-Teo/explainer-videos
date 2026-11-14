"""Monochord's blues and swing (Part 38): chord spelling, the swing model, the walking bass, guide tones, tritone
substitution and the syncopation count, against hand calculations and brute force.

    python -m pytest -q tests/music/test_blues.py
"""

from itertools import product

import numpy as np

from explainer.music.monochord import blues as BL


def test_chords_and_forms():
    assert BL.chord("G7")["pcs"] == [7, 11, 2, 5] and BL.chord("Db7")["root"] == 1
    assert BL.chord("Dm7")["third"] == 5 and BL.chord("Dm7")["seventh"] == 0
    assert BL.chord("F#dim7")["pcs"] == [6, 9, 0, 3]
    basic = BL.twelve_bar("C", "basic")
    assert len(basic) == 12 and basic[4] == ["F7"] and basic[8] == ["G7"]
    assert BL.twelve_bar("F", "basic")[0] == ["F7"] and BL.twelve_bar("F", "basic")[4] == ["Bb7"]
    assert sum(len(b) for b in BL.twelve_bar("C", "jazz")) == 15


def test_swing_model():
    assert BL.swing_ratio(120) == 3.0 and BL.swing_ratio(300) == 1.0 and BL.swing_ratio(400) == 1.0
    assert BL.swing_ratio(60) == 3.5
    t = BL.swing_times([0, 1, 2, 3], 120)
    assert np.allclose(t, [0.0, 0.375, 0.5, 0.875])
    t = BL.swing_times([0, 1], 120, ratio=1.0, delay_ms=30.0)
    assert np.allclose(t, [0.03, 0.25])
    assert all(85 < BL.short_note_ms(b) < 110 for b in range(160, 300, 10))


def test_walking_bass_rules():
    ch = BL.twelve_bar("C", "jazz")
    wb = BL.walking_bass(ch)
    seq = BL.beats_of(ch)
    assert len(wb) == 48
    for i in range(48):
        if i == 0 or seq[i] != seq[i - 1]:
            assert wb[i] % 12 == BL.chord(seq[i])["root"]
            assert abs(wb[i - 1] - wb[i]) == 1                       # approached by a semitone (wrapping round)
    assert all(0 < abs(wb[i + 1] - wb[i]) <= 7 for i in range(47))


def test_guide_tones_are_least_motion():
    g = BL.guide_tones(["Dm7", "G7", "Cmaj7"])
    assert (g["upper"], g["lower"]) == ([65, 65, 64], [60, 59, 59]) and g["total"] == 2
    # brute force over registers in a small range: nothing moves less
    syms = ["Dm7", "G7", "Cmaj7", "A7"]
    opts = []
    for s in syms:
        c = BL.chord(s)
        a, b = c["third"], c["seventh"]
        opts.append([(x, y) for x in range(52, 73) for y in range(52, 73) if x > y and x - y <= 11 and {x % 12, y % 12} == {a, b}])
    best = min(sum(abs(p[i + 1][0] - p[i][0]) + abs(p[i + 1][1] - p[i][1]) for i in range(3)) for p in product(*opts))
    assert BL.guide_tones(syms)["total"] == best


def test_tritone_substitution():
    assert BL.tritone_sub("G7") == "Db7" and BL.tritone("G7") == BL.tritone("Db7") == {5, 11}
    for r in range(12):
        s = BL.PCN[r] + "7"
        sharing = [BL.PCN[q] + "7" for q in range(12) if BL.tritone(BL.PCN[q] + "7") == BL.tritone(s)]
        assert sorted(sharing) == sorted([s, BL.tritone_sub(s)])


def test_syncopation_count():
    # sixteenth, eighth, sixteenth in one beat: the eighth (at 6) is held across the half-beat with nothing there
    s = BL.syncopation([(72, 0, 6), (74, 6, 12), (72, 18, 6), (72, 24, 24)])
    assert s["syncopated"] == 1 and s["sync_times"] == [6] and s["between"] == 2
    assert BL.syncopation([(60, 0, 12), (62, 12, 12)])["syncopated"] == 0
    rh, lh = BL.rag_hands([(70, 0, 6), (50, 0, 12)])
    assert rh == [(70, 0, 6)] and lh == [(50, 0, 12)]
