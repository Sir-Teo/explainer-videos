"""Monochord's score: the model, and what each notation keeps.

    python -m pytest -q tests/music/test_score.py
"""

import xml.etree.ElementTree as ET
from fractions import Fraction

import pytest

from explainer.music.monochord import score as S
from explainer.music.monochord import tune
from explainer.music.monochord.score import read as R
from explainer.music.monochord.score import write as W


def test_pitches_are_spelled():
    cs, db = S.Pitch.parse("C#4"), S.Pitch.parse("Db4")
    assert cs.midi == db.midi == 61 and cs != db and cs.diatonic + 1 == db.diatonic
    assert S.Pitch.parse("C4").midi == 60 and S.Pitch.parse("A4").hz() == pytest.approx(440.0)
    assert S.Pitch.parse("E4").staff_position() == 0 and S.Pitch.parse("F5").staff_position() == 8      # the treble staff's lines
    assert S.Pitch.parse("C4").staff_position() == -2 and S.Pitch.parse("G2").staff_position("bass") == 0
    assert S.Pitch.parse("C4").up(2, 4).name == "E4" and S.Pitch.parse("E4").up(2, 3).name == "G4"      # a major, then a minor third
    assert S.Pitch.parse("F#4").up(2, 4).name == "A#4" and S.Pitch.parse("Gb4").up(2, 4).name == "Bb4"
    assert S.Pitch.from_midi(61).name == "C#4" and S.Pitch.from_midi(61, flats=True).name == "Db4"


def test_durations_are_exact():
    assert S.value(Fraction(1, 4)) == ("quarter", 0) and S.value(Fraction(3, 8)) == ("quarter", 1) and S.value(Fraction(7, 16)) == ("quarter", 2)
    with pytest.raises(ValueError):
        S.value(Fraction(5, 16))
    sc = S.Score([S.Voice([S.Note(S.Pitch.parse("C4"), Fraction(3, 4)), S.Note(S.Pitch.parse("D4"), Fraction(1, 2)), S.Rest(Fraction(3, 4))])], time=(4, 4))
    bars = sc.measures()
    assert [[e.dur for e in b] for b in bars] == [[Fraction(3, 4), Fraction(1, 4)], [Fraction(1, 4), Fraction(3, 4)]]
    assert bars[0][1].tie and not bars[1][0].tie                          # a note across the barline is split and tied
    played = sc.performed()
    assert len(played) == 2 and played[1]["dur"] == pytest.approx(sc.seconds(Fraction(1, 2)))          # and played as one


def test_the_tune_as_a_score():
    t = S.tune_score()
    assert len(t.voices[0].events) == len(tune.TUNE) == 42 and t.length == 12 and len(t.measures()) == 12
    assert [e.pitch.name for e in t.voices[0].events[:7]] == ["C4", "C4", "G4", "G4", "A4", "A4", "G4"]
    assert t.voices[0].events[6].dur == Fraction(1, 2)
    e = S.tune_score("Eb4")
    assert e.key == -3 and [n.pitch.name for n in e.voices[0].events[:7]] == ["Eb4", "Eb4", "Bb4", "Bb4", "C5", "C5", "Bb4"]
    assert S.tune_score("A3").key == 3 and S.tune_score("A3").voices[0].events[4].pitch.name == "F#4"
    p = t.performed()
    assert p[0]["hz"] == pytest.approx(261.63, abs=0.01) and p[2]["t"] == pytest.approx(2 * 60 / 109)


def test_musicxml_and_mei_keep_everything():
    for tonic in ("C4", "Eb4", "F#4"):
        t = S.tune_score(tonic, words=True)
        back = R.musicxml(W.musicxml(t))
        assert back.voices[0].events == t.voices[0].events and (back.key, back.time, back.tempo, back.title) == (t.key, t.time, t.tempo, t.title)
    root = ET.fromstring(W.mei(S.tune_score("Eb4")))
    ns = {"m": "http://www.music-encoding.org/ns/mei"}
    notes = root.findall(".//m:note", ns)
    assert len(notes) == 42 and notes[0].get("pname") == "e" and notes[0].get("accid") == "f" and notes[6].get("dur") == "2"
    assert root.find(".//m:scoreDef", ns).get("keysig") == "3f" and len(root.findall(".//m:measure", ns)) == 12


def test_midi_keeps_the_keys_and_forgets_the_spelling():
    t = S.tune_score("Eb4")
    data = W.midi(t)
    assert data[:4] == b"MThd" and len(data) < 500                        # forty-two notes in a few hundred bytes
    back = R.midi(data)
    assert [e.pitch.midi for e in back.voices[0].notes] == [e.pitch.midi for e in t.voices[0].notes]
    assert [e.dur for e in back.voices[0].notes] == [e.dur for e in t.voices[0].notes]
    assert back.tempo == pytest.approx(t.tempo, rel=1e-4) and back.time == t.time and back.key == t.key
    assert back.voices[0].notes[0].pitch.name == "D#4" != t.voices[0].notes[0].pitch.name               # E flat came back as D sharp
    assert R.midi(data, flats=True).voices[0].notes[0].pitch.name == "Eb4"
    short = R.midi(W.midi(t, gate=0.8))                                   # played a little detached: the note values are gone too
    assert short.voices[0].notes[0].dur == Fraction(1, 5) and short.voices[0].events[1].is_rest
    tied = S.Score([S.Voice([S.Note(S.Pitch.parse("C4"), Fraction(1, 2), tie=True), S.Note(S.Pitch.parse("C4"), Fraction(1, 4))])])
    assert [e.dur for e in R.midi(W.midi(tied)).voices[0].notes] == [Fraction(3, 4)]                    # a tie is one long key press


def test_text_notations():
    t = S.tune_score()
    assert W.jianpu(t).startswith("1=C  4/4  1 1 5 5 | 6 6 5 - | 4 4 3 3 | 2 2 1 - |")
    assert W.jianpu(S.tune_score("Eb4")).split("  ")[2] == W.jianpu(t).split("  ")[2]                   # the same digits in every key
    assert W.jianpu(S.tune_score("Eb4")).startswith("1=Eb")
    assert "C C G G | A A G2 |" in W.abc(t) and "K:C" in W.abc(t) and "K:Eb" in W.abc(S.tune_score("Eb4"))
    assert "E E B B | c c B2" in W.abc(S.tune_score("Eb4"))               # the key signature carries the flats
    assert W.lilypond(t).startswith("{ \\time 4/4 c'4 c'4 g'4 g'4 | a'4 a'4 g'2")
    assert "ees'4 ees'4 bes'4" in W.lilypond(S.tune_score("Eb4"))
    assert W.solfege(t).split()[:7] == ["do", "do", "sol", "sol", "la", "la", "sol"] == W.solfege(S.tune_score("A3")).split()[:7]
