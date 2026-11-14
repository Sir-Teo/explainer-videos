"""Monochord's Baroque toolkit (Part 25)."""

import math

from explainer.music.monochord import baroque as B
from explainer.music.monochord import tuning as TU


def test_galilei():
    assert B.weights_for(2.0) == 4.0
    assert math.isclose(B.string_hz(4.0) / B.string_hz(1.0), 2.0)


def test_figures():
    assert B.figure_of(48, [64, 67]) == "" and B.figure_of(48, [63, 69]) == "6" and B.figure_of(48, [65, 69]) == "6/4"
    assert B.figure_of(48, [64, 67, 70]) == "7" and B.figure_of(48, [63, 67, 69]) == "6/5" and B.figure_of(48, [62, 65, 69]) == "4/2"


def test_ritornello_and_ornaments():
    head = [(60, 0, 1), (64, 1, 1), (67, 2, 1), (64, 3, 1), (72, 4, 1), (71, 5, 1), (69, 6, 1)]
    line = head + [(62, 7 + k, 1) for k in range(6)] + [(p + 7, o + 13, d) for p, o, d in head]
    f = B.ritornello_returns(line, head=6)
    assert [x["transpose"] for x in f] == [0, 7]
    tr = B.trill(72, 0, 1, n=6, turn=False)
    assert tr[0][0] == 74 and tr[-1][0] == 72 and abs(sum(d for _, _, d in tr) - 1) < 1e-9
    ineg = B.inegale([(60, 0, 0.5), (62, 0.5, 0.5)], ratio=2.0, unit=0.5)
    assert abs(ineg[0][2] - 2 / 3) < 1e-9 and abs(ineg[1][1] - 2 / 3) < 1e-9


def test_key_colours():
    eq = B.key_colours(TU.equal(12))
    assert all(abs(r["third_error"] - 13.69) < 0.01 for r in eq)
    w = {r["key"]: r for r in B.key_colours(TU.werckmeister3())}
    assert w["C"]["third_error"] < w["E"]["third_error"] < w["F#"]["third_error"]


def test_corpus():
    d = B.load()
    assert set(d) == {"corelli", "handel"} and len(d["corelli"]) == 3
