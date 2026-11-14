"""What notations keep (Part 10): contours, tablature, figured bass, mensural lengths, performance rules, and a toy
page reader.

    python -m pytest -q tests/music/test_notations.py
"""

from fractions import Fraction as F
from itertools import product

import numpy as np
import pytest

from explainer.music.monochord import score as S
from explainer.music.monochord.score import codes, figured, mensural, perform, raster, tab

P = S.Pitch.parse
TUNE = S.tune_score()
KEYS = [n.pitch.midi for n in TUNE.voices[0].notes]


def test_contour_counts_match_brute_force():
    con = codes.contour(KEYS[:7])
    assert con == [0, 1, 0, 1, 0, -1]
    brute = sum(codes.contour(m) == con for m in product(range(6), repeat=7))
    assert codes.count_contour(con, 6) == brute == 85
    for seed in range(20):
        m = codes.with_contour(con, 6, seed)
        assert codes.contour(m) == con and min(m) >= 0 and max(m) < 6
    assert codes.count_contour(codes.contour(KEYS), 8) > 10 ** 8          # the whole Tune: hundreds of millions fit


def test_bits_and_sizes():
    d = codes.description_bits(TUNE)
    assert d["notes"] == 42 and d["pitches"] == 6 and d["durations"] == 2 and d["plain_bits"] == 42 * 4
    assert 2.5 < d["entropy_bits_per_note"] < 4.0
    s = codes.sizes(TUNE)
    assert s["jianpu"] < s["ABC"] < s["MIDI"] < s["MEI"] < s["MusicXML"] and s["MusicXML, zipped"] < s["MusicXML"] / 5
    assert codes.entropy("aaaa") == 0.0 and codes.entropy("abab") == 1.0


def test_gongche_and_durations():
    assert "".join(codes.gongche(TUNE)[:14]) == "上上六六五五六凡凡工工尺尺上"
    assert [codes.dotted(k) for k in range(4)] == [1, F(3, 2), F(7, 4), F(15, 8)]
    assert codes.binary_values(F(5, 8)) == [(F(1, 2), 0), (F(1, 8), 0)]
    assert codes.binary_values(F(7, 8)) == [(F(1, 2), 2)]
    for k in range(1, 64):                                           # every sixty-fourth: the values add up, and there are few of them
        v = codes.binary_values(F(k, 64))
        assert sum(a * codes.dotted(d) for a, d in v) == F(k, 64) and len(v) <= bin(k).count("1")
    with pytest.raises(ValueError):
        codes.binary_values(F(1, 3))


def test_tablature():
    assert tab.positions(60) == [(2, 10), (3, 5), (4, 1)]            # middle C: three places on a guitar
    f = tab.fingering(KEYS)
    assert tab.sounded(f["positions"]) == KEYS                        # it plays the Tune
    assert max(fr for _, fr in f["positions"]) <= 5                   # without leaving the first position
    assert tab.count_fingerings(KEYS[:7]) == 3 ** 5 * 2 ** 2 and tab.count_fingerings(KEYS) > 10 ** 19
    worst = [tab.positions(m)[0] for m in KEYS]                      # always the lowest string that has the note
    cost = sum(tab._cost(a, b) for a, b in zip(worst, worst[1:]))
    assert f["cost"] < cost


def test_figured_bass():
    assert [p.name for p in figured.chord(P("C3"))] == ["E3", "G3"]
    assert [p.name for p in figured.chord(P("E3"), "6")] == ["G3", "C4"]
    assert [p.name for p in figured.chord(P("G2"), "7")] == ["B2", "D3", "F3"]
    assert [p.name for p in figured.chord(P("A2"), "6", key=2)] == ["C#3", "F#3"]          # the key signature supplies the sharps
    r = figured.realizations(P("C3"))
    assert all({m % 12 for m in c} >= {4, 7} and {m % 12 for m in c} <= {0, 4, 7} for c in r) and len(r) > 5
    bass = [P(x) for x in ("C3", "E3", "F3", "E3", "D3", "C3", "G2", "C3")]
    figs = ["", "6", "", "6", "6", "", "7", ""]
    a, b = figured.realize(bass, figs), figured.realize(bass, figs, top=79)
    assert a["chords"] != b["chords"] and a["parallels"] == 0 and b["parallels"] == 0 and a["count"] > 10 ** 6
    for chords in (a["chords"], b["chords"]):
        for bs, fg, c in zip(bass, figs, chords):
            want = {p.midi % 12 for p in figured.chord(bs, fg)}
            assert want <= {m % 12 for m in c} <= want | {bs.midi % 12}


def test_mensural_lengths():
    assert mensural.read("SSSSSSB", perfect=False) == [1, 1, 1, 1, 1, 1, 2]              # the Tune's first phrase in duple time
    assert mensural.read("SSSSSSB") == [1, 1, 1, 1, 1, 1, 3]                             # and the same marks in triple time
    assert mensural.read("BSB") == [2, 1, 3]                                             # imperfection
    assert mensural.read("BSSB") == [3, 1, 2, 3]                                         # alteration: the same sign, twice as long
    assert mensural.read("BSSSB") == [3, 1, 1, 1, 3]
    assert mensural.read("B.SB") == [3, 1, 2]                                            # a dot protects the breve
    for s in ("BSB", "BSSB", "BSSSB", "BSSSSB", "BSSSSSB", "SSSB", "BBSSB"):
        assert mensural.perfections(mensural.read(s))


def test_performance_rules():
    dead, live = perform.deadpan(TUNE), perform.expressive(TUNE)
    assert len(dead) == len(live) == 42
    assert all(n["t"] == n["page_t"] and n["db"] == 0 for n in dead)
    d = perform.deviations(live)
    assert perform.deviations(dead)["largest_ms"] < 1e-6
    assert 20 < d["largest_ms"] < 120 and 3 < d["db_range"] < 12
    assert live[-1]["dur"] > 1.3 * live[-1]["page_dur"]                                  # the last note is held
    assert all(b["t"] > a["t"] for a, b in zip(live, live[1:]))
    assert perform.ritard_tempo(0.0) == 1.0 and perform.ritard_tempo(1.0, final=0.5) == pytest.approx(0.5)


def test_page_reader():
    notes = [(n.pitch.staff_position(), n.dur < S.H) for n in TUNE.voices[0].notes]
    img = raster.page(notes)
    assert len(raster.staff_lines(img)) == 15
    assert raster.read_page(img) == notes                                                # a clean page: every note
    every = [(p, f) for p in range(-2, 11) for f in (True, False)]
    assert raster.read_page(raster.page(every, per_line=13)) == every
    tilted = raster.distort(img, skew=1.0)
    assert raster.read_page(tilted) == []                                                # one degree: no staff is found at all
    level, angle = raster.deskew(tilted)
    assert angle == pytest.approx(-1.0, abs=0.11) and raster.accuracy(raster.read_page(level), notes) > 0.95
    assert raster.accuracy(raster.read_page(raster.distort(img, specks=0.1, seed=1)), notes) < 0.6
    assert raster.accuracy("abc", "abc") == 1.0 and raster.accuracy("abd", "abc") == pytest.approx(2 / 3)
