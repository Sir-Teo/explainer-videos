"""Monochord's Romantic toolkit (Part 27)."""

import numpy as np

from explainer.music.monochord import romantic as R


def test_measures():
    scale = [(60 + s, 24 * k, 24) for k, s in enumerate([0, 2, 4, 5, 7, 9, 11, 12] * 4)]
    m = R.measure(scale, window=16, hop=8)
    assert m["chromaticism"] == 0.0 and m["clarity"] > 0.6 and tuple(m["keys"][0]["key"]) == (0, "major")
    chrom = [(60 + k % 12, 24 * k, 24) for k in range(48)]
    mc = R.measure(chrom, window=16, hop=8)
    assert mc["chromaticism"] >= 0.25 and mc["clarity"] < 0.5 < m["clarity"]   # all twelve: 3 of 12 outside even the widest minor
    assert R.in_key(11, (9, "minor")) and R.in_key(6, (9, "minor")) and not R.in_key(1, (9, "minor"))
    assert abs(R.pc_entropy(chrom) - np.log2(12)) < 1e-9 and R.pc_entropy([(60, 0, 24)]) == 0.0


def test_xml_reader_merges_ties_and_keeps_chords():
    xml = """<score-partwise><part-list><score-part id="P1"><part-name>Piano</part-name></score-part></part-list>
    <part id="P1"><measure number="1"><attributes><divisions>1</divisions><time><beats>3</beats><beat-type>4</beat-type></time>
    <transpose><chromatic>-2</chromatic></transpose></attributes>
    <note><pitch><step>C</step><octave>4</octave></pitch><duration>2</duration><tie type="start"/></note>
    <note><chord/><pitch><step>E</step><octave>4</octave></pitch><duration>2</duration></note>
    <note><pitch><step>C</step><octave>4</octave></pitch><duration>1</duration><tie type="stop"/></note>
    </measure></part></score-partwise>"""
    r = R.parse_all(xml)
    assert r["time"] == (3, 4)
    assert r["parts"]["Piano"] == [(58, 0, 72), (62, 0, 48)]           # sounding pitch; C held three beats


def test_kern_reader_follows_split_spines():
    krn = "\n".join(["**kern", "*M3/4", "4C", "*^", "4E\t4G", "4F\t4A", "*v\t*v", "4c", "*-"])
    r = R.parse_kern_all(krn)
    notes = r["parts"]["spine 0"]
    assert r["time"] == (3, 4)
    assert [(p, o) for p, o, _ in notes] == [(48, 0), (52, 24), (55, 24), (53, 48), (57, 48), (60, 72)]


def test_transformations_and_timing():
    head = [(72, 0, 1), (72, 1, 1), (79, 2, 1), (79, 3, 1), (81, 4, 1), (81, 5, 1), (79, 6, 2)]
    assert [p for p, _, _ in R.transform(head, "minor")] == [72, 72, 79, 79, 80, 80, 79]
    assert R.transform(head, "augmented")[-1] == (79, 12, 4)
    assert [p for p, _, _ in R.transform(head, "inverted")][:3] == [72, 72, 65]
    t = R.phrase_arch(np.arange(0, 17, 1.0), 8.0, depth=0.3)
    assert abs(t[8] - 8.0) < 0.1 and abs(t[16] - 16.0) < 0.2           # phrase lengths kept to first order
    assert t[1] - t[0] > t[4] - t[3]                                     # slower at the start than in the middle
    mz = R.mazurka_beats([0, 1, 2, 3], (0.85, 1.2, 0.95))
    assert np.allclose(mz, [0, 0.85, 2.05, 3.0])
    assert R.winds({"flutes": 2, "horns": 4}) == 6


def test_library_extract():
    lib = R.load_library()
    assert len(lib) == len(R.LIBRARY) == 23
    years = [r["year"] for r in lib]
    assert min(years) == 1765 and max(years) == 1924
    linden = next(r for r in lib if "Linden" in r["path"])
    assert len(linden["parts"]["Voice"]) == 205 and len(linden["parts"]["Piano"]) == 1443
