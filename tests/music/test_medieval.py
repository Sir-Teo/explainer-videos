"""Monochord's medieval toolkit (Part 23): modes, hexachords, organum, rhythmic modes, mensuration, isorhythm, and the
fourteenth-century corpus."""

import itertools

import numpy as np

from explainer.music.monochord import medieval as MD
from explainer.music.monochord import trecento as T


def test_modes_and_classifier():
    assert [MD.MODES[m][1] % 12 for m in range(1, 9)] == [2, 2, 4, 4, 5, 5, 7, 7]
    # the reciting tones: a fifth above the final in authentic modes (a sixth in the third, where B is avoided)
    assert [MD.MODES[m][2] - MD.MODES[m][1] for m in (1, 3, 5, 7)] == [7, 8, 7, 7]
    for m in range(1, 9):
        assert MD.classify(MD.psalm_tone(m)) == m
    lo, hi = MD.mode_range(2)
    assert (lo, hi) == (57, 69)
    assert MD.classify([62, 64, 65, 67, 69, 71, 72, 74, 72, 69, 65, 62]) == 1       # D up to the octave: Dorian
    assert MD.classify([62, 60, 57, 60, 62, 64, 65, 64, 62]) == 2                   # below the final: Hypodorian
    assert abs(MD.profile([62, 64, 62]).sum() - 1) < 1e-12


def test_gamut_and_solmization():
    g = MD.gamut()
    assert g[0] == 43 and g[-1] == 76 and len(g) == 22                            # twenty letters and two b-flats
    assert len(MD.hexachords()) == 7
    ut = [p for p, _ in MD.UT_QUEANT]
    syl, mut = MD.solmize(ut)
    assert [syl[i] for i in MD.UT_LINES[:6]] == list(MD.SYLLABLES)                # ut re mi fa sol la
    assert mut == []
    # a line that needs b-flat and b-natural must mutate
    syl, mut = MD.solmize([60, 62, 64, 65, 67, 69, 70, 69, 67, 69, 71, 72])
    assert syl[6] == "fa" and syl[10] == "mi" and len(mut) >= 2
    # the path is shortest: compare with brute force on a short line
    line = [65, 67, 69, 70, 72, 71, 69]
    opts = [MD.syllable_options(p) for p in line]
    best = min(sum(a[0] != b[0] for a, b in zip(c, c[1:])) for c in itertools.product(*opts))
    assert len(MD.solmize(line)[1]) == best


def test_organum():
    pt = MD.psalm_tone(2)                                     # recites on F: a fifth below F is B, a tritone
    fifths = MD.parallel(pt, -4)
    assert MD.tritones(pt, fifths) >= 5
    ench = MD.enchiriadis(pt, floor=57)
    assert MD.tritones(pt, ench) == 0 and ench[-1] == pt[-1]
    assert all(q >= 57 or q == p for p, q in zip(pt, ench))
    rng = np.random.default_rng(0)
    fl = MD.florid([50, 53, 52, 50], rng)
    assert all((line[0] - t) % 12 in (0, 7) and (line[-1] - t) % 12 in (0, 7) for line, t in zip(fl, [50, 53, 52, 50]))


def test_rhythmic_modes_and_ligatures():
    assert all(sum(v) % 3 == 0 for v in MD.RHYTHMIC_MODES.values())          # every ordo fills whole perfections
    for m, n in ((1, 9), (2, 9), (3, 10), (5, 9), (6, 10)):
        assert MD.mode_of(MD.ligatures_for(m, n)) == m
    assert MD.mode_of([2, 2, 2, 2]) is None
    notes = MD.realize(1, [60, 62, 64, 65])
    assert [d for _, _, d in notes] == [2, 1, 2, 1]
    rng = np.random.default_rng(1)
    lines = MD.notre_dame(53, 8, rng)
    tenor = lines[-1][0][0]
    for v in lines[:-1]:
        for p, o, d in v:
            if o % 3 == 0:
                assert (p - tenor) % 12 in (0, 7)                            # every perfection starts consonant


def test_mensuration():
    assert MD.MENSURATIONS[(True, True)][1] == 9 and MD.MENSURATIONS[(False, False)][1] == 4
    assert MD.read_perfect("BSB") == [2, 1, 3]                                # imperfection
    assert MD.read_perfect("BSSB") == [3, 1, 2, 3]                            # alteration
    assert MD.read_perfect("BSSSB") == [3, 1, 1, 1, 3]
    assert MD.read_perfect("SBB") == [1, 2, 3]
    for s in ("BSBSSBSSSSB", "BSSSSSB", "BSSSSB"):
        assert sum(MD.read_perfect(s)) % 3 == 0                               # always whole perfections


def test_isorhythm():
    color = [53, 55, 57, 55, 53, 52, 50]
    talea = [2, 1, -1, 3, 1, 1, -1]
    notes = MD.isorhythm(color, talea)
    per = MD.periods(len(color), sum(1 for d in talea if d > 0))
    assert per == {"lcm": 35, "colors": 5, "taleae": 7}
    assert len(notes) == 35
    # the talea repeats exactly: inter-onset times have the talea's period
    span = sum(abs(d) for d in talea)
    assert notes[5][1] - notes[0][1] == span
    half = MD.isorhythm(color, talea, diminution=0.5)
    assert abs(half[-1][1] * 2 - notes[-1][1]) < 1e-9
    # found again by the scan: a voice built of a repeated bar pattern
    voice = [(p, int(o * 24), int(d * 24)) for p, o, d in MD.isorhythm(color * 6, [3, 3, 2, 1, -3])]
    sc = MD.talea_scan(voice, bar=72, lo=1)
    assert sc["share"] > 0.9


def test_trecento_corpus():
    book = T.load()
    assert len(book) >= 80
    assert all(2 <= len(p.voices) <= 5 for p in book)
    vitry = [p for p in book if p.composer == "Philippe de Vitry"]
    assert len(vitry) == 4
    # the tenor of each of de Vitry's motets repeats its rhythm far above chance
    rng = np.random.default_rng(0)
    for p in vitry:
        low = p.voices[2]
        sc = MD.talea_scan(low, p.bar)
        assert sc["share"] > MD.shuffled_share(low, p.bar, rng, trials=4) + 0.1
    finals = [MD.final_sonority(p) for p in book]
    assert finals.count("open") > 0.9 * len(finals)
    c = MD.cadences(book[0])
    assert c["double"] <= c["leading_tone"] <= c["sixth_octave"]
