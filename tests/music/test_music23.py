"""Part 23 of *Music, Built*: what the film says is what was computed, and every sound keeps the series' rules.

    python -m pytest -q tests/music/test_music23.py
"""

import pytest

from tests.music.partcheck import check_clips, check_ear_thread, check_scenes_and_clips, check_windows
from videos.music.music23 import compute
from videos.music.music23.manifest import SCENES
from videos.music.variations import LEDGER

load = compute.load


def test_chant_and_guido():
    c = load("chant")
    assert c["ut_mode"] == 2 and c["quiz"]["modes"] == [2, 1]
    assert [c["modes"][str(m)]["tenor"] for m in range(1, 9)] == [69, 65, 72, 69, 72, 69, 74, 72]
    g = load("guido")
    assert [g["ut_syllables"][i] for i in c["ut_lines"][:6]] == ["ut", "re", "mi", "fa", "sol", "la"]
    assert g["ut_mutations"] == [] and g["line_mutations"] == [7] and len(g["gamut"]) == 22


def test_organum_and_rhythm():
    o = load("organum")
    assert o["tritones"] == {"parallel": 9, "flat": 0, "enchiriadis": 0}
    assert o["enchiriadis"][-1] == o["chant"][-1] and min(o["enchiriadis"]) >= 60
    r = load("rhythm")
    assert [tuple(r["modes"][str(m)]["pattern"]) for m in range(1, 7)] == [(2, 1), (1, 2), (3, 1, 2), (1, 2, 3), (3, 3), (1, 1, 1)]
    m = load("mensuration")
    assert m["franco"] == {"BSB": [2, 1, 3], "BSSB": [3, 1, 2, 3], "BSSSB": [3, 1, 1, 1, 3], "BSSSSB": [2, 1, 1, 1, 1, 3]}
    assert {k: v["minims_per_breve"] for k, v in m["readings"].items()} == {"O with a dot": 9, "O": 6, "C with a dot": 6, "C": 4}


def test_isorhythm():
    d = load("isorhythm")
    assert d["periods"] == {"lcm": 35, "colors": 5, "taleae": 7}
    lags = {v["title"].split(".")[-1].strip()[:6]: v["lag"] for v in d["vitry"]}
    assert lags["Lugent"] == 33 and lags["Rex qu"] == 12 and lags["Virtut"] == 18
    for v in d["vitry"]:
        assert v["shares"][2] > v["chance"]
    lug = [v for v in d["vitry"] if v["lag"] == 33][0]
    assert lug["shares"][2] == pytest.approx(0.977, abs=0.002) and lug["scan"]["66"] > 0.95


def test_census():
    c = load("census")
    assert c["pieces"] == 89
    assert c["on"]["perfect"] == pytest.approx(0.586, abs=0.002) and c["off"]["dissonant"] == pytest.approx(0.226, abs=0.002)
    assert c["parallels"]["trecento"] == {"parallels": 1855, "moves": 64801} and c["parallels"]["bach"] == {"parallels": 65, "moves": 144317}
    assert c["cadences"] == {"sixth_octave": 1410, "leading_tone": 1006, "double": 459}
    assert c["finals"] == {"open": 88, "third": 1} and c["bach_finals"] == {"third": 364}
    f = c["ficta"]
    assert (f["notes"], f["outside"], f["rising"]) == (65681, 2149, 1380)
    lan = load("landini")
    assert lan["total"] == 173 and lan["by_composer"]["Francesco Landini"] == [14, 4] and lan["by_composer"]["Johannes Ciconia"] == [69, 18]


def test_variation_23():
    t = load("tune")
    assert t["meet"] == 28 and len(t["color"]) == 7
    v = load("variation")
    row = [r for r in LEDGER if r["part"] == 23][0]
    assert v["part"] == 23 and row["measure"] == v["measure"] and row["seconds"] == pytest.approx(v["seconds"], abs=0.05)


def test_the_part_keeps_the_series_rules():
    check_clips(compute)
    check_scenes_and_clips(compute, SCENES)
    check_windows(compute, SCENES)
    check_ear_thread(compute, SCENES)
