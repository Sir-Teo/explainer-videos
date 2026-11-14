"""Monochord's syntax of harmony: root motion, functions, predictability, the rule of the octave, schemata, grounds."""

import numpy as np
import pytest

from explainer.music.monochord import chorales as BC
from explainer.music.monochord import fourpart as F
from explainer.music.monochord import progression as P


@pytest.fixture(scope="module")
def book():
    return BC.load()


def test_motion_and_functions(book):
    m = P.root_motions(book, "major")
    assert m.most_common(1)[0][0] == "fifth down" and m["fifth down"] > 2 * m["fifth up"]
    f = P.function_transitions(book, "major")
    assert f["DT"] == max(f.values()) and f["DS"] == min(f.values())
    assert P.function((7, "major"), "major") == "D" and P.function((2, "minor"), "major") == "S" and P.function((9, "minor"), "major") == "T"


def test_predictability(book):
    train, test = BC.split(book, offset=2)
    p = P.predictability(train, test, "major")
    assert p["uniform"] > p["n1"] > p["n2"] and p["n2"] < p["n2_shuffled"] - 1.0
    assert p["n1"] == pytest.approx(p["n1_shuffled"])                         # a model of frequencies cannot see order
    m = P.NGram([["I", "V", "I"]], 2, ["I", "V"], alpha=0.0001)
    assert m.prob(["V"], "I") > 0.99 and m.bits([["I", "V", "I"]]) < 1.1


def test_rule_of_the_octave():
    assert P.rule_chord(2, "up") == (2, 11, 7, 5)                              # V4/3 over D
    assert P.rule_chord(6, "down") == (9, 6, 2, 0)                             # the raised sixth: D7 over A
    assert set(P.rule_chord(4, "down")) == {5, 11, 7, 2} and P.rule_chord(4, "down")[0] == 5   # V4/2 over F
    for direction in ("up", "down"):
        r = P.realize_rule(direction)
        assert len(r) == 8 and all(F.spacing_ok(ch) or ch[2] - ch[3] <= 24 for ch in r)
        assert not any(F.parallels(a, b) for a, b in zip(r, r[1:]))
        for ch, d in zip(r, range(1, 9) if direction == "up" else range(8, 0, -1)):
            assert {p % 12 for p in ch} == set(P.rule_chord(d, direction))


def test_schemata_and_grounds(book):
    ev = [(5, 9), (4, 7), (2, 5), (0, 4)]
    assert P.find_schemata([(0, 0)] + ev) == [("Prinner", 1)]
    c = P.schema_census(book)
    assert sum(c["real"].values()) > sum(c["shuffled"].values())
    for name in P.GROUNDS:
        v = P.ground_voicings(name)
        assert len(v) == len(P.GROUNDS[name]["chords"]) and all(ch[3] < ch[2] < ch[1] < ch[0] for ch in v)
