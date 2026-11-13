"""Monochord's tuning layer against Barbour's tables (*Tuning and Temperament*, 1951) and exact arithmetic.

    python -m pytest -q tests/music/test_tuning.py
"""

import math
from fractions import Fraction

import pytest

from explainer.music.monochord import tuning as T


def test_the_commas():
    assert T.PYTHAGOREAN_COMMA == Fraction(531441, 524288) and T.cents(T.PYTHAGOREAN_COMMA) == pytest.approx(23.460, abs=0.001)
    assert T.cents(T.SYNTONIC_COMMA) == pytest.approx(21.506, abs=0.001)
    assert T.SCHISMA == Fraction(32805, 32768) and T.cents(T.DIESIS) == pytest.approx(41.059, abs=0.001)
    assert Fraction(3, 2) ** 4 / 4 == T.PURE_THIRD * T.SYNTONIC_COMMA                 # four fifths, two octaves down: a third and a comma
    assert Fraction(3, 2) ** 12 / 2 ** 7 == T.PYTHAGOREAN_COMMA


def test_pythagorean_and_its_wolf():
    t = T.pythagorean()
    assert t.ratios[T.NAMES.index("E")] == Fraction(81, 64) and t.ratios[T.NAMES.index("G")] == Fraction(3, 2)
    sizes = dict(t.fifths())
    assert sizes["G#"] == pytest.approx(701.955 - 23.460, abs=0.001)                  # the wolf takes the whole comma
    assert sum(s for _, s in t.fifths()) == pytest.approx(8400.0)                     # twelve fifths close seven octaves, wolf included


def test_barbours_tables():
    want = {"meantone": [0, 76.0, 193.2, 310.3, 386.3, 503.4, 579.5, 696.6, 772.6, 889.7, 1006.8, 1082.9],
            "werckmeister": [0, 90.2, 192.2, 294.1, 390.2, 498.0, 588.3, 696.1, 792.2, 888.3, 996.1, 1092.2]}
    for got, table in ((T.meantone().cents, want["meantone"]), (T.werckmeister3().cents, want["werckmeister"])):
        assert all(abs(a - b) < 0.06 for a, b in zip(got, table))
    m = T.meantone()
    assert m.interval("C", "E") == pytest.approx(T.cents(Fraction(5, 4)), abs=1e-9)   # a quarter comma: pure thirds
    assert dict(m.fifths())["G#"] == pytest.approx(737.6, abs=0.1)                    # and a wolf 36 cents wide
    assert dict(m.thirds())["B"] == pytest.approx(427.4, abs=0.1)                     # with four unusable thirds
    w = dict(T.werckmeister3().thirds())
    assert min(w.values()) == pytest.approx(390.2, abs=0.1) and max(w.values()) == pytest.approx(407.8, abs=0.1)
    assert len({round(v, 1) for v in w.values()}) == 4                                # no wolf, and keys that differ


def test_equal_temperament_and_zhu():
    assert T.root12_of_2(24) == "1.059463094359295264561825"                          # Zhu Zaiyu's twenty-five figures
    e = T.equal(12)
    assert e.hz("A", 4) == 440.0 and e.hz("C", 4) == pytest.approx(261.626, abs=0.001)
    assert all(s == pytest.approx(700.0) for _, s in e.fifths())
    beats = {(r["low"], r["high"]): r["beats"] for r in T.tuner_table(e)}
    assert beats[("F3", "A3")] == pytest.approx(6.93, abs=0.01) and beats[("A3", "E4")] == pytest.approx(-0.74, abs=0.01)


def test_why_twelve():
    cf = T.continued_fraction(math.log2(1.5), 8)
    assert cf == [0, 1, 1, 2, 2, 3, 1, 5]
    assert [c.denominator for c in T.convergents(cf)][2:7] == [2, 5, 12, 41, 53]
    err = {n: T.edo_errors(n) for n in (12, 19, 31, 53)}
    assert err[12]["fifth_error"] == pytest.approx(-1.955, abs=0.001) and err[12]["third_error"] == pytest.approx(13.686, abs=0.001)
    assert abs(err[31]["third_error"]) < 1.0 and abs(err[53]["fifth_error"]) < 0.1 and abs(err[19]["third_error"]) < 8


def test_the_comma_pump():
    chords = T.comma_pump(1)
    assert [c["root"] for c in chords] == ["C", "A", "D", "G", "C"]
    assert chords[2]["notes"]["D"] == Fraction(10, 9)                                 # not 9/8: the D that is in tune with A
    assert chords[-1]["notes"]["C"] == T.fold(Fraction(80, 81))                       # the tonic comes back a comma flat
    assert T.pump_drift(1) == pytest.approx(-21.506, abs=0.001) and T.pump_drift(5) == pytest.approx(-107.53, abs=0.01)


def test_stretched_octaves():
    assert T.stretched_octave(0.0) == 0.0
    assert T.stretched_octave(0.001) == pytest.approx(1200 * math.log2(math.sqrt(1.004 / 1.001)), abs=1e-9)
    curve = T.railsback()
    assert len(curve) == 88 and curve[48] == 0.0                                      # the A above middle C stays put
    assert curve[0] < -10 and curve[-1] > 20 and all(b > a for a, b in zip(curve, curve[1:]))
