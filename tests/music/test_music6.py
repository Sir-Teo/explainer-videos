"""Part 6 of *Music, Built*: what the film says is what was computed, and every sound keeps the series' rules.

    python -m pytest -q tests/music/test_music6.py
"""

import math

import numpy as np
import pytest

from tests.music.partcheck import check_clips, check_ear_thread, check_scenes_and_clips, check_windows
from videos.music.music6 import compute
from videos.music.music6.manifest import SCENES

load = compute.load


def test_the_pump_sinks_a_comma_a_round():
    d = load("pump")
    assert d["per_round"] == pytest.approx(-21.506, abs=0.001) and d["total"] == pytest.approx(-86.03, abs=0.01)
    rows = d["rows"]
    assert len(rows) == 17 and [r["root"] for r in rows[:5]] == ["C", "A", "D", "G", "C"]
    for a, b in zip(rows, rows[1:]):                                    # neighbouring chords share a note at exactly the same pitch
        assert any(abs(x - y) < 1e-6 for x in a["freqs"] for y in b["freqs"]), (a["root"], b["root"])
    for r in rows:                                                      # and every chord is pure: 4:5:6 or 10:12:15 in some order
        f = sorted(r["freqs"])
        ratios = sorted([f[1] / f[0], f[2] / f[1]])
        assert any(abs(ratios[0] - a) < 1e-9 and abs(ratios[1] - b) < 1e-9 for a, b in ((6 / 5, 5 / 4), (5 / 4, 4 / 3), (6 / 5, 4 / 3)))
    assert d["chain"][2]["notes"]["D"] == [10, 9] and d["chain"][4]["notes"]["C"] == [160, 81]


def test_the_commas():
    c = load("circle")
    assert c["comma"] == [531441, 524288] and c["comma_cents"] == pytest.approx(23.46, abs=0.01)
    assert c["wolf_cents"] == pytest.approx(678.5, abs=0.1) and c["steps"][12]["cents"] == pytest.approx(1223.46, abs=0.01)
    s = load("syntonic")
    assert s["comma"] == [81, 80] and s["d_a_ratio"] == [40, 27] and s["three_thirds"] == [125, 64]
    assert s["diesis_cents"] == pytest.approx(41.06, abs=0.01) and s["beat"] == pytest.approx(16.35, abs=0.01)
    notes = {n["name"]: (n["fifths"], n["thirds"]) for n in s["lattice"]}
    assert notes["C"] == (0, 0) and notes["E"] == (0, 1) and notes["D"] == (2, 0) and notes["A"] == (-1, 1)


def test_meantone_and_werckmeister():
    m = load("meantone")
    assert m["fifth_cents"] == pytest.approx(696.58, abs=0.01) and m["fifth_ratio"] == pytest.approx(5 ** 0.25)
    assert m["wolf_wide_by"] == pytest.approx(35.68, abs=0.01) and m["bad_third_wide_by"] == pytest.approx(41.06, abs=0.01)
    assert len(m["good_keys"]) == 8 and m["bad_keys"] == ["B", "F#", "C#", "G#"]
    assert m["three_errors"]["pythagorean"] > m["three_errors"]["equal"] > m["three_errors"]["meantone"] == 0.0
    w = load("well")
    assert w["wide"]["C"] < w["wide"]["E"] < w["wide"]["F#"] and w["wide"]["F#"] == pytest.approx(21.5, abs=0.1)
    assert w["narrow_fifths"] == ["C", "G", "D", "B"]
    thirds = {name: [v for _, v in w["table"][name]["thirds"]] for name in w["table"]}
    assert max(thirds["Werckmeister III"]) < 22 and min(thirds["Werckmeister III"]) > 3       # no pure third, no wolf
    assert all(v == pytest.approx(13.69, abs=0.01) for v in thirds["equal"])


def test_equal_temperament():
    e = load("equal")
    assert e["root"] == "1.059463094359295264561825"
    assert e["third_error"] == pytest.approx(13.69, abs=0.01) and e["fifth_error"] == pytest.approx(-1.96, abs=0.01)
    assert abs(e["worked"]["beats"]) == pytest.approx(0.74, abs=0.01) and abs(e["third_beat"]) == pytest.approx(10.38, abs=0.01)
    assert e["first_fret_mm"] == pytest.approx(36.48, abs=0.01) and e["frets"][12]["from_nut_mm"] == pytest.approx(325.0)
    assert e["rule"] == pytest.approx(17.817, abs=0.001)
    r = e["roots"]
    assert r["sqrt2"] ** 2 == pytest.approx(2) and r["cbrt"] ** 12 == pytest.approx(2)


def test_why_twelve_and_the_piano():
    d = load("why12")
    assert d["cf"][:6] == [0, 1, 1, 2, 2, 3] and d["convergents"][4] == [7, 12] and d["convergents"][6] == [31, 53]
    assert d["record_fifths"] == [2, 3, 5, 7, 12, 29, 41, 53]
    rows = {r["n"]: r for r in d["rows"]}
    assert abs(rows[31]["third_error"]) < 1 and abs(rows[53]["fifth_error"]) < 0.1
    p = load("piano")
    assert p["top"] > 20 and p["bottom"] < -10 and np.all(np.diff(p["curve"]) > 0)
    assert p["stretch_cents"] == pytest.approx(15.35, abs=0.01) and p["beat_exact"] > 10


def test_variation_6():
    t = load("tune")
    rows = {r["name"]: r for r in t["rows"]}
    assert len(rows) == 8 and t["best"] == "53 equal" and t["worst"].startswith("meantone, in A flat")
    assert rows["12 equal"]["error"] == pytest.approx(9.8, abs=0.1) and rows["meantone, in C"]["error"] == pytest.approx(3.8, abs=0.1)
    assert rows["53 equal"]["error"] < 1.5 and rows["Pythagorean"]["error"] == pytest.approx(15.2, abs=0.1)
    assert load("variation")["part"] == 6


def test_the_part_keeps_the_series_rules():
    check_clips(compute)
    check_scenes_and_clips(compute, SCENES)
    check_windows(compute, SCENES)
    check_ear_thread(compute, SCENES)
