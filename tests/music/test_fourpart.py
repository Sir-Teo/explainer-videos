"""Monochord's chorales and four-part writing: the table, the rules, the labels, the harmonizer, the choir."""

import numpy as np
import pytest

from explainer.music.monochord import chorales as BC
from explainer.music.monochord import fourpart as F
from explainer.music.monochord.instruments import choir


@pytest.fixture(scope="module")
def book():
    return BC.load()


def test_the_table(book):
    assert len(book) == 364
    assert sum(c.mode == "major" for c in book) == 185 and sum(c.mode == "minor" for c in book) == 178
    c = next(x for x in book if x.name == "bwv66.6")
    assert (c.fifths, c.mode, c.tonic) == (3, "minor", 6)                                   # F sharp minor
    assert [p for p, _, _, _ in c.voices[0][:5]] == [73, 71, 69, 71, 73] and c.phrases()[0] == 144
    for x in book[:40]:
        for v in x.voices:
            assert all(o + d <= v[k + 1][1] for k, (p, o, d, f) in enumerate(v[:-1]))        # one note at a time in each voice
    g = BC.tunes(book)
    assert len(g) == 230
    passion = next(v for v in g.values() if any(c.name == "bwv244.62" for c in v))
    assert len(passion) == 11                                                                # the Passion Chorale, set eleven times
    train, test = BC.split(book, offset=2)
    assert not {BC.melody_key(c) for c in train} & {BC.melody_key(c) for c in test}


def test_rules():
    assert F.parallels((67, 64, 60, 48), (69, 65, 62, 50)) == [((0, 2), "fifths"), ((0, 3), "fifths"), ((2, 3), "octaves")]
    assert F.parallels((67, 64, 60, 48), (65, 62, 57, 50)) == []
    assert F.parallels((67, 60, 55, 48), (62, 62, 57, 50), contrary=True)                   # octaves in contrary motion
    assert F.hidden((64, 60, 55, 48), (72, 64, 55, 53)) and not F.hidden((64, 60, 55, 48), (65, 60, 57, 53))
    assert F.spacing_ok((72, 64, 55, 48)) and not F.spacing_ok((79, 60, 55, 48))
    assert F.label((67, 64, 60, 48), 0) == (0, "major", 0) and F.label((65, 62, 59, 55), 0) == (7, "7", 0)
    assert F.label((72, 67, 64, 52), 0) == (0, "major", 1) and F.roman((7, "7", 2), "major") == "V4/3"
    assert F.doubled((72, 67, 64, 48), (0, "major", 0)) == "root"


def test_bach_counted(book):
    r = F.rule_census(book)
    assert r["parallel"] == {"fifths": 52, "octaves": 23} and r["moves"] == 29326
    assert r["moves"] / sum(r["parallel"].values()) > 300                                   # about one in four hundred chord changes


def test_the_harmonizer(book):
    train, test = BC.split(book, offset=2)
    m = F.ChordModel(train, "major")
    assert m.states[:2] == [(0, "major"), (7, "major")]
    c = next(x for x in test if x.mode == "major")
    B = F.bach_on_beats(c)
    full = F.harmonize(B["soprano"], c.tonic, m, fermatas=B["fermatas"])
    plain = F.harmonize(B["soprano"], c.tonic, m, fermatas=B["fermatas"], plain=True)
    assert [ch[0] for ch in full["chords"]] == B["soprano"]                                  # the tune is kept
    for ch in full["chords"]:
        assert F.in_range(ch) and F.spacing_ok(ch)
        assert {p % 12 for p in ch} <= {(c.tonic + x) % 12 for x in range(12)}
    assert sum(len(F.parallels(a, b)) for a, b in zip(full["chords"], full["chords"][1:])) == 0
    assert full["states"][-1][0] == 0 and full["chords"][-1][3] % 12 == c.tonic               # it ends at home, root in the bass
    ev = F.evaluate(full, B)
    assert 0.2 < ev["same_chord"] <= 1.0 and plain["cost"] <= full["cost"] + 1e9


def test_the_choir():
    y = choir.chorale([[(67, 0, 1), (69, 1, 1)], [(64, 0, 1), (65, 1, 1)], [(60, 0, 1), (60, 1, 1)], [(48, 0, 1), (53, 1, 1)]], beat=0.5)
    assert np.isfinite(y).all() and abs(np.abs(y).max() - 1) < 1e-9
    one = choir.sing([(69, 0.0, 1.0)], "alto")
    spec = np.abs(np.fft.rfft(one[4800:40000]))
    f = np.fft.rfftfreq(len(one[4800:40000]), 1 / 48000)
    peak = f[np.argmax(spec * (f < 1000))]
    assert spec[(f > 430) & (f < 450)].max() > 0.05 * spec.max()                                # A4's fundamental is there
    assert peak > 400
