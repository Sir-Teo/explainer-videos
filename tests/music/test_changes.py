"""Monochord's changes (Part 39): the bebop-scale claim proved by exhaustion, chord scales, third cycles,
reharmonisation and the improviser against its baselines.

    python -m pytest -q tests/music/test_changes.py
"""

import numpy as np

from explainer.music.monochord import blues as BL
from explainer.music.monochord import changes as CH


def test_bebop_scale_claim_every_dominant_and_sixth():
    for r in BL.PCN:
        for q in ("7", "6"):
            c = CH.bebop_claim(r + q)
            assert c["bebop_all"] and len(c["bebop_scale"]) == 8
            assert c["plain_mean"] < 0.7
    # why: in descending order from the root, chord tones sit at every other position
    sc = CH.bebop_scale("C7")
    order = sorted(sc, key=lambda p: (-p) % 12)
    assert [p in (0, 4, 7, 10) for p in order] == [True, False] * 4


def test_chord_scales_and_avoid_notes():
    assert CH.chord_scale("Cmaj7")["avoid"] == [5] and CH.chord_scale("C7")["avoid"] == [5]
    assert CH.chord_scale("Cm7")["avoid"] == [] and CH.chord_scale("Cm7b5")["avoid"] == [1]
    assert CH.chord_scale("Cdim7")["avoid"] == [] and len(CH.chord_scale("Cdim7")["scale"]) == 8


def test_third_cycles():
    assert len(CH.symbols(CH.GIANT_STEPS)) == 26 and len(CH.GIANT_STEPS) == 16
    k = CH.key_centres([[s if any(s.endswith(q) for q in ("7", "m")) else s + "maj7" for s in bar] for bar in CH.GIANT_STEPS])
    assert k["distinct"] == [3, 7, 11] and k["steps"] == [4, 8]
    assert CH.coltrane("C") == ["Dm7", "Eb7", "Abmaj7", "B7", "Emaj7", "G7", "Cmaj7"]
    major = lambda r: {(r + i) % 12 for i in (0, 2, 4, 5, 7, 9, 11)}
    assert all(len(major(r) & major(r + 4)) == 3 and len(major(r) & major(r + 7)) == 6 for r in range(12))
    assert len(CH.SO_WHAT) == 32


def test_reharmonise_keeps_the_melody_inside():
    mel = [72, 76, 79, 77, 76, 74, 72]
    for scheme in ("diatonic", "secondary"):
        ch = CH.reharmonise(mel, scheme)
        for m, s in zip(mel, ch):
            c = BL.chord(s)
            assert m % 12 in c["pcs"] or m % 12 in [(c["root"] + 2) % 12, (c["root"] + 9) % 12]
    tri = CH.reharmonise(mel, "tritone")
    sec = CH.reharmonise(mel, "secondary")
    for a, b in zip(sec, tri):
        if a != b:
            assert b == BL.tritone_sub(a)


def test_improviser_beats_its_baselines():
    ch = BL.twelve_bar("C", "jazz")
    imp = [CH.judge(CH.improvise(ch, seed=s), ch) for s in range(20)]
    rnd = [CH.judge(CH.random_line(ch, seed=s), ch) for s in range(20)]
    mean = lambda js, k: float(np.mean([j[k] for j in js]))
    assert mean(imp, "on_beat_chord_tones") > mean(rnd, "on_beat_chord_tones") + 0.2
    assert mean(imp, "guide_at_changes") > mean(rnd, "guide_at_changes") + 0.4
    line = CH.improvise(ch, seed=1)
    assert all(58 <= m <= 84 for m, _ in line) and all(0 <= e < 96 for _, e in line)
    assert len({e for _, e in line}) == len(line)                          # one note at a time
