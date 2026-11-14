"""The engraver: notes land on the right lines, in the right order, and time maps to a place on the page.

    python -m pytest -q tests/music/test_staff.py
"""

from fractions import Fraction as F

import numpy as np
import pytest

from explainer.music.monochord import score as S
from explainer.music.staff import Staff, music_font

P = S.Pitch.parse


def test_a_music_font_is_found():
    assert music_font()


def test_notes_sit_on_their_lines():
    st = Staff(S.tune_score(), width=11.0, space=0.2)
    lines = [ln.get_center()[1] for ln in st.systems[0].lines]
    assert len(st.notes) == 42 and len(st.barlines) == 12
    y = lambda k: st.notes[k].head.get_center()[1]          # noqa: E731
    assert y(2) == pytest.approx(lines[1], abs=1e-6)        # G4 on the second line
    assert y(4) == pytest.approx((lines[1] + lines[2]) / 2, abs=1e-6)       # A4 in the space above it
    assert y(0) == pytest.approx(lines[0] - 0.2, abs=1e-6) and len(st.notes[0].ledgers) == 1         # middle C on its ledger line
    xs = [n.head.get_center()[0] for n in st.notes]
    assert all(b > a for a, b in zip(xs, xs[1:]))
    assert st.notes[6].stem is not None and st.notes[6].dur == F(1, 2) and st.notes[0].up


def test_signatures_accidentals_and_rests():
    ev = [S.Note(P("F#4"), F(1, 4)), S.Note(P("F4"), F(1, 4)), S.Note(P("F4"), F(1, 4)), S.Rest(F(1, 4)), S.Note(P("F4"), F(1, 4)), S.Note(P("Bb4"), F(3, 4))]
    st = Staff(S.Score([S.Voice(ev)], key=1, time=(4, 4)), width=9.0)
    acc = [n.accidental is not None for n in st.notes]
    assert acc == [False, True, False, True, True]          # the key has F sharp; a natural lasts the bar; the next bar needs it again
    assert len(st.rests) == 1 and len(st.events) == 6
    bass = Staff(S.Score([S.Voice([S.Note(P("G2"), F(1)), S.Note(P("A3"), F(1))], clef="bass")]), width=6.0)
    lines = [ln.get_center()[1] for ln in bass.systems[0].lines]
    assert bass.notes[0].head.get_center()[1] == pytest.approx(lines[0], abs=1e-6) and bass.notes[1].head.get_center()[1] == pytest.approx(lines[4], abs=1e-6)
    assert bass.notes[0].stem is None                        # a whole note has no stem


def test_beams_and_ties():
    ev = [S.Note(P("C5"), F(1, 8)), S.Note(P("D5"), F(1, 8)), S.Note(P("E5"), F(1, 8)), S.Note(P("G4"), F(1, 4)), S.Note(P("A4"), F(1, 8)), S.Note(P("B4"), F(1, 4), tie=True), S.Note(P("B4"), F(1, 4))]
    st = Staff(S.Score([S.Voice(ev)], time=(4, 4)), width=9.0)
    assert [n.beamed for n in st.notes] == [True, True, False, False, False, False, False]           # eighths sharing a beat are beamed
    assert len(st.notes[2].flags) == 1 and len(st.notes[4].flags) == 1 and len(st.notes[3].flags) == 0


def test_time_maps_to_the_page():
    sc = S.tune_score()
    st = Staff(sc, width=11.0, systems=2).shift(np.array([0.5, 1.0, 0.0]))
    assert len(st.systems) == 2 and st.end_time == 12
    for k in (0, 5, 20, 41):
        n = st.notes[k]
        assert st.point_at(n.time)[0] == pytest.approx(n.head.get_center()[0])                       # also after the staff has been moved
    xs = [st.x_at(F(k, 8)) for k in range(0, 48)]            # the first system: left to right
    assert all(b >= a for a, b in zip(xs, xs[1:]))
    assert st.point_at(F(13, 2))[1] < st.point_at(F(11, 2))[1]                                       # then down to the second
    assert st.note_at(F(1, 8)) == 0 and st.note_at(F(7, 4)) == 6 and st.note_at(99) == -1
    cur = st.cursor()
    fn = st.follow()
    fn(cur, sc.seconds(F(1, 2)))
    assert cur.get_center()[0] == pytest.approx(st.notes[2].head.get_center()[0])


def test_chords_on_a_staff():
    from explainer.music.staff import GrandStaff

    row = S.quick([["C4", "E4", "G4"], ["C4", "D4", "G4"], ["Db4", "F4", "Ab4"], ["A5", "B5"], ["C#4", "E4", "G4", "Bb4"]], dur=F(1, 4), time=(5, 4))
    st = Staff(row, width=9.0, carry=False)
    c, second, flats, high, dim = st.notes
    assert len(c.heads) == 3 and [h.get_center()[1] for h in c.heads] == sorted(h.get_center()[1] for h in c.heads)
    assert len({round(h.get_center()[0], 6) for h in c.heads}) == 1                   # thirds stack in one column
    assert c.up and c.stem.get_end()[1] > c.heads[-1].get_center()[1]                 # one stem, past the top head
    # a second: the upper note goes to the right of an upward stem; the lower to the left of a downward one
    assert second.heads[1].get_center()[0] > second.heads[0].get_center()[0] + 0.5 * st.space
    assert second.heads[2].get_center()[0] == pytest.approx(second.heads[0].get_center()[0])
    assert not high.up and high.heads[0].get_center()[0] < high.heads[1].get_center()[0] - 0.5 * st.space
    assert high.head is high.heads[1]                                                 # the stem starts at the head that was not moved
    # two flats a fifth apart take two columns; a sharp and a flat a seventh apart share one
    xs = sorted(round(a.get_center()[0], 4) for a in flats.accidentals)
    assert len(flats.accidentals) == 2 and xs[1] - xs[0] > 0.5 * st.space
    xd = [round(a.get_center()[0], 4) for a in dim.accidentals]
    assert len(dim.accidentals) == 2 and abs(xd[0] - xd[1]) < 0.3 * st.space
    c.heads[1].set_color("#FF0000")                                                   # one note of a chord can be coloured
    assert c.heads[1].get_fill_color() != c.heads[0].get_fill_color()
    # a chord sounds every one of its notes, and a tie joins the ones that stay
    sc = S.Score([S.Voice([S.Chord((P("C4"), P("E4"), P("G4")), F(1, 2), tie=True), S.Chord((P("C4"), P("F4"), P("A4")), F(1, 2))])])
    played = sc.performed()
    assert sorted((n["pitch"].name, round(n["dur"] / sc.seconds(F(1, 2)))) for n in played) == [("A4", 1), ("C4", 2), ("E4", 1), ("F4", 1), ("G4", 1)]
    assert len(sc.measures()[0]) == 2 and sc.measures()[0][0].pitches[2].name == "G4"
    # a grand staff: the same moment at the same place across the page
    up = [S.Note(P(n), F(1, 4)) for n in ("C5", "C5", "G5", "G5", "A5", "A5")] + [S.Note(P("G5"), F(1, 2))]
    lo = [S.Chord(tuple(P(x) for x in ch), F(1, 2)) for ch in (("C3", "E3", "G3"), ("C3", "E3", "G3"), ("C3", "F3", "A3"), ("C3", "E3", "G3"))]
    gs = GrandStaff(S.Score([S.Voice(up), S.Voice(lo, clef="bass")], time=(4, 4)), width=9.0, space=0.15)
    for k, j in ((0, 0), (2, 1), (4, 2), (6, 3)):
        assert gs.upper.notes[k].x == pytest.approx(gs.lower.notes[j].x, abs=1e-6)
    assert gs.upper.get_center()[1] > gs.lower.get_center()[1] and len(gs.joins) == 3
