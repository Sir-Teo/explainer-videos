"""Monochord's sixteenth-century toolkit (Part 24): the corpus reader, dissonance treatment, melody, imitation,
stylometry, tuning."""

import numpy as np

from explainer.music.monochord import palestrina as PS
from explainer.music.monochord import renaissance as R
from explainer.music.monochord.trecento import Piece


def piece(voices, bar=96):
    return Piece("t", "t", "x", (4, 2), bar, voices)


def test_kern_reader():
    assert R.kern_pitch("c") == 60 and R.kern_pitch("cc") == 72 and R.kern_pitch("C") == 48 and R.kern_pitch("CC") == 36
    assert R.kern_pitch("f#") == 66 and R.kern_pitch("B-") == 58
    assert R.kern_duration("1") == 96 and R.kern_duration("2.") == 72 and R.kern_duration("0") == 192 and R.kern_duration("4") == 24
    text = "**kern\t**kern\n*M4/2\t*M4/2\n=1\t=1\n1c\t1cc\n[1d\t1b\n=2\t=2\n1d]\t1cc\n*-\t*-\n"
    p = R.parse_kern(text, "x")
    assert [n[:3] for n in p.voices[0]] == [(72, 0, 96), (71, 96, 96), (72, 192, 96)]
    assert p.voices[1] == [(60, 0, 96), (62, 96, 192)]                 # the tie merged


def test_dissonance_classes():
    # bass holds A; upper C, B, A: B is a passing dissonance (a ninth/second above A)
    p = piece([[(72, 0, 24), (71, 24, 24), (69, 48, 48)], [(57, 0, 96)]])
    assert PS.dissonances(p) == {"passing": 1}
    # a 7-6 suspension: C held over the bass moving A -> D, then B
    p = piece([[(72, 0, 72), (71, 72, 24)], [(57, 0, 48), (62, 48, 48)]])
    assert PS.dissonances(p) == {"suspension": 1}
    # the same seventh struck by leap: free
    p = piece([[(69, 0, 48), (72, 48, 24), (71, 72, 24)], [(57, 0, 48), (62, 48, 48)]])
    assert PS.dissonances(p)["free"] == 1
    # a cambiata: C B (dissonant) G A over A G G#
    p = piece([[(72, 0, 24), (71, 24, 24), (67, 48, 24), (69, 72, 24)], [(57, 0, 48), (55, 48, 48)]])
    assert PS.dissonances(p).get("cambiata", 0) == 1


def test_melody_imitation_stylometry():
    m = PS.melodic(piece([[(60, 0, 24), (67, 24, 24), (65, 48, 24), (64, 72, 24)], [(48, 0, 96)]]))
    assert m["leaps"] == 1 and m["recovered"] == 1 and m["forbidden"] == 0
    head = [(60, 0, 24), (62, 24, 24), (64, 48, 24), (65, 72, 24), (67, 96, 24)]
    p = piece([head, [(q - 7, o + 96, d) for q, o, d in head]])
    im = PS.imitation(p)
    assert im["imitative"] and im["followers"][0]["interval"] == -7 and im["followers"][0]["delay"] == 96
    X = np.array([[0, 0], [0.1, 0], [1, 1], [1.1, 1]])
    assert PS.loo_centroid(X, ["a", "a", "b", "b"])["accuracy"] == 1.0
    c = PS.triad_cents()
    assert abs(c["just"][0] - 386.3137) < 1e-3 and abs(c["31-tone"][1] - 696.774) < 1e-3


def test_corpus():
    book = R.load()
    assert sum(p.book == 0 for p in book) == 1318 and sum(p.book > 0 for p in book) == 48
    assert len({p.work for p in book if p.book == 0}) == 101
