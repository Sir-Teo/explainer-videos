"""Monochord's chords against what every harmony book prints, and one published number of Parncutt's model."""

import numpy as np
import pytest

from explainer.music.monochord import chords as C
from explainer.music.monochord.score import Pitch

P = Pitch.parse


def test_interval_names_and_inversions():
    cases = {("C4", "E4"): "major third", ("C4", "Eb4"): "minor third", ("C4", "G4"): "perfect fifth", ("C4", "F#4"): "augmented fourth",
             ("C4", "Gb4"): "diminished fifth", ("B3", "F4"): "diminished fifth", ("F4", "B4"): "augmented fourth", ("C4", "C5"): "perfect octave",
             ("C4", "C#4"): "augmented unison", ("C4", "Db4"): "minor second", ("E4", "C5"): "minor sixth", ("C4", "B4"): "major seventh",
             ("C#4", "Bb4"): "diminished seventh", ("C4", "D5"): "major ninth", ("Ab3", "F#4"): "augmented sixth"}
    for (a, b), name in cases.items():
        assert C.interval(P(a), P(b)).name == name
    for short in ("P1", "m2", "M2", "m3", "M3", "P4", "A4", "d5", "P5", "m6", "M6", "m7", "M7", "P8", "d7", "A2"):
        iv = C.named(short)
        assert iv.short == short
        inv = iv.invert()
        assert iv.number + inv.number == 9 and iv.semitones + inv.semitones == 12
        swap = {"P": "P", "M": "m", "m": "M", "A": "d", "d": "A"}
        assert inv.short[0] == swap[short[0]]
        assert C.interval(P("C4"), C.above(P("C4"), short)).short == short
    with pytest.raises(ValueError):
        C.named("M5")


def test_quality_is_distance_on_the_line_of_fifths():
    notes = [Pitch(s, a, 4) for s in "CDEFGAB" for a in (-1, 0, 1)]
    for a in notes:
        for b in notes:
            if b.diatonic > a.diatonic:
                iv = C.interval(a, b)
                assert iv.line == C.fifths(b) - C.fifths(a)
                assert iv.quality == C.quality_of(C.fifths(b) - C.fifths(a))
    assert sorted({C.interval_class(0, k) for k in range(12)}) == [0, 1, 2, 3, 4, 5, 6]
    assert C.spell_pc(6, key=2).name == "F#4" and C.spell_pc(6, key=-5).name == "Gb4" and C.spell_pc(10, key=0).name == "Bb4"


def test_chords_of_the_major_scale():
    tri = C.scale_chords("C4", 3)
    assert [c["kind"] for c in tri] == ["major", "minor", "minor", "major", "major", "minor", "diminished"]
    assert [c["roman"] for c in tri] == ["I", "ii", "iii", "IV", "V", "vi", "vii°"]
    sev = C.scale_chords("C4", 4)
    assert [c["kind"] for c in sev] == ["maj7", "m7", "m7", "maj7", "7", "m7", "m7b5"]
    assert [c["roman"] for c in sev] == ["Imaj7", "ii7", "iii7", "IVmaj7", "V7", "vi7", "viiø7"]
    # I, IV and V hold all seven notes between them
    assert {n[:-1] for d in (0, 3, 4) for n in tri[d]["names"]} == set("CDEFGAB")
    # in another key the spelling follows the key
    assert C.scale_chords("Eb4", 3)[4]["names"] == ["Bb4", "D5", "F5"]
    # seven thirds stacked are the whole scale
    assert sorted(p.step for p in C.spell("C4", "maj13")) == sorted("CDEFGAB")


def test_spelling_inversion_and_figures():
    assert [p.name for p in C.spell("F#4", "m7b5")] == ["F#4", "A4", "C5", "E5"]
    assert [p.name for p in C.spell("Db4", "major")] == ["Db4", "F4", "Ab4"]
    assert [p.name for p in C.spell("C#4", "dim7")] == ["C#4", "E4", "G4", "Bb4"]
    c = C.spell("C4", "major")
    assert [C.figure_name(C.invert(c, k)) for k in range(3)] == ["5/3", "6", "6/4"]
    g7 = C.spell("G3", "7")
    assert [C.figure_name(C.invert(g7, k)) for k in range(4)] == ["7", "6/5", "4/3", "4/2"]
    for k in range(3):
        v = C.invert(c, k)
        ids = C.identify(v)
        assert ids[0]["root"] == 0 and ids[0]["kind"] == "major" and ids[0]["inversion"] == k
        assert [p.step for p in C.stack_of_thirds(v)] == ["C", "E", "G"]
    assert C.stack_of_thirds([P("C4"), P("D4"), P("G4")]) is None
    # one set of notes, two names
    both = C.identify([P("C4"), P("E4"), P("G4"), P("A4")])
    assert {(c["root"], c["kind"]) for c in both} == {(9, "m7"), (0, "6")}
    assert both[0]["kind"] == "m7" and both[0]["inversion"] == 1


def test_symbols_both_ways():
    for text, names in {"C": ["C4", "E4", "G4"], "Am7": ["A4", "C5", "E5", "G5"], "F#m7b5/A": ["F#4", "A4", "C5", "E5"], "Bbmaj7": ["Bb4", "D5", "F5", "A5"],
                        "Ebdim7": ["Eb4", "Gb4", "Bbb4", "Dbb5"], "G7/B": ["G4", "B4", "D5", "F5"], "Dsus4": ["D4", "G4", "A4"], "E5": ["E4", "B4"],
                        "C+": ["C4", "E4", "G#4"], "Dm(maj7)": ["D4", "F4", "A4", "C#5"]}.items():
        got = C.parse_symbol(text)
        assert [p.name for p in got["pitches"]] == names
        again = C.parse_symbol(got["symbol"])
        assert again["kind"] == got["kind"] and again["root"] == got["root"] and again["bass"] == got["bass"]
    assert C.symbol("C", "major", "E") == "C/E" and C.symbol("F#", "m7b5") == "F♯m7♭5"
    with pytest.raises(ValueError):
        C.parse_symbol("Cfoo")


def test_parncutt_roots():
    major = C.root([0, 4, 7])
    assert major["root"] == 0 and major["salience"] == 18
    assert abs(major["ambiguity"] - 1.870829) < 1e-5            # the value the reference implementation prints (parn88, updated weights)
    minor = C.root([0, 3, 7])
    assert minor["root"] == 0 and minor["ambiguity"] > major["ambiguity"]
    dim = C.root([11, 2, 5])                                    # B D F: G, a note that is not there, is as good a root as any that is
    assert sorted(dim["tied"]) == [2, 5, 7, 11] and dim["ambiguity"] > minor["ambiguity"]
    aug = C.root([0, 4, 8])
    assert sorted(aug["tied"]) == [0, 4, 8]
    assert C.root([7, 11, 2, 5])["root"] == 7                   # G7
    sixth = C.root([0, 4, 7, 9])
    assert sixth["root"] == 0 and sixth["second"] == 9
    # doubling the root makes it surer; doubling the third less
    assert C.root([0, 4, 7], [2, 1, 1])["ambiguity"] < major["ambiguity"] < C.root([0, 4, 7], [1, 2, 1])["ambiguity"]


def test_voicings_and_the_low_limit():
    close, low = C.spacing_roughness([60, 64, 67]), C.spacing_roughness([36, 40, 43])
    spread = C.spacing_roughness([36, 43, 52])
    assert low > 2 * close and spread < low
    limits = {s: C.low_limit(s) for s in (3, 4, 7, 12)}
    assert limits[3] >= limits[4] > limits[7] > limits[12]        # the narrower the interval, the higher it must stay
    assert limits[4] == 60                                        # the reference itself
    vs = C.voicings([0, 4, 7], 48, 72, voices=4, bass=0)
    assert all(v[0] % 12 == 0 and {m % 12 for m in v} == {0, 4, 7} and list(v) == sorted(set(v)) for v in vs) and len(vs) > 10
    near = C.nearest_voicing((60, 64, 67), [5, 9, 0])
    assert near == (60, 65, 69) and C.motion((60, 64, 67), near) == 3
    assert C.voice_leading([0, 4, 7], [0, 5, 9])["cost"] == 3 and C.voice_leading([0, 4, 7], [7, 11, 2])["cost"] == 3


def test_tonnetz_moves():
    c = (0, "major")
    assert C.P(c) == (0, "minor") and C.R(c) == (9, "minor") and C.L(c) == (4, "minor")
    triads = [(r, k) for r in range(12) for k in ("major", "minor")]
    for t in triads:
        for name, f in C.MOVES.items():
            u = f(t)
            assert f(u) == t                                               # each move undoes itself
            assert len(set(C.triad_pcs(t)) & set(C.triad_pcs(u))) == 2     # and keeps two notes
            assert C.voice_leading(C.triad_pcs(t), C.triad_pcs(u))["cost"] == (2 if name == "R" else 1)
        a, b = zip(*[C.tonnetz(p) for p in C.triad_pcs(t)])
        assert all(C.at(x, y) == p for x, y, p in zip(a, b, C.triad_pcs(t)))
    assert len(C.cycle(c, "PL")) == 6 and len(C.cycle(c, "PR")) == 8
    lr = C.cycle(c, "LR")
    assert len(lr) == 24 and set(lr) == set(triads)
    assert [C.triad_name(t) for t in C.cycle(c, "PL")] == ["C", "Cm", "A♭", "A♭m", "E", "Em"]
    assert C.tonnetz_distance(c, (6, "major")) == max(C.tonnetz_distance(c, t) for t in triads if t[1] == "major")
    # every pair of notes a triangle shares is an edge of the lattice: a fifth, a major third or a minor third
    assert {C.interval_class(0, C.at(1, 0)), C.interval_class(0, C.at(0, 1)), C.interval_class(C.at(0, 1), C.at(1, 0))} == {5, 4, 3}


def test_the_listener_names_plain_chords():
    sr = 16000
    t = np.arange(int(0.8 * sr)) / sr
    for root in range(12):
        for kind in ("major", "minor"):
            y = sum(np.sin(2 * np.pi * C.hz(60 + root + h) * t) for h in C.offsets(kind))
            got = C.recognise(C.chroma(y, sr))
            assert (got["root"], got["kind"]) == (root, kind)
