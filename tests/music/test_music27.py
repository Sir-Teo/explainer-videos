"""Part 27 of *Music, Built*: what the film says is what was computed, and every sound keeps the series' rules.

    python -m pytest -q tests/music/test_music27.py
"""

import pytest

from tests.music.partcheck import check_clips, check_ear_thread, check_scenes_and_clips, check_windows
from videos.music.music27 import compute
from videos.music.music27.manifest import SCENES
from videos.music.variations import LEDGER

load = compute.load


def test_keyboards_and_the_song():
    k = load("keyboards")
    assert [x["keys"] for x in k["keyboards"]] == [54, 61, 73, 78, 85, 88]
    clara = [s for s in k["spans"] if s["composer"] == "Clara Schumann"]
    assert max(s["high"] for s in clara) == 100 and all(s["high"] > 89 for s in clara)          # above Mozart's F6
    li = load("lied")
    assert li["answer"] == "A" and 28.0 in li["minor_bars"]
    assert li["share"]["n_voice"] == 205 and li["share"]["n_piano"] == 1443
    assert 67 in [n[0] for n in li["A"]["voice"]] and 68 in [n[0] for n in li["B"]["voice"]]   # G natural, G sharp


def test_tristan_and_orchestras():
    t = load("tristan")
    assert t["fits_tristan"][0] == 5 and t["fits_plain"][0] == 8
    o = load("orchestra")
    assert [r["players"] for r in o["rows"]] == [5, 9, 18, 27, 19]


def test_the_library():
    d = load("library")
    assert sum(p["n"] for p in d["points"]) == 827
    assert d["slope_i"] == pytest.approx(0.0557, abs=0.002) and d["ci_i"][0] > 0                 # instrumental: a real rise
    assert d["ci_c"][0] < 0 < d["ci_c"][1]                                                       # all pieces: not clear of zero
    assert d["songs"] < d["instrumental"] / 2
    assert min(a["chromaticism"] for a in d["after"]) > 0.24 and max(a["clarity"] for a in d["after"]) < 0.56
    assert d["quiz"]["answer"] == "A" and d["quiz"]["A_chrom"] > 3 * d["quiz"]["B_chrom"]
    aloha = next(p for p in d["points"] if "aloha" in p["group"])
    assert aloha["clarity"] == max(p["clarity"] for p in d["points"])


def test_nations_and_variation_27():
    n = load("nations")
    assert n["rh_onbeat"] / n["rh_notes"] < n["lh_onbeat"] / n["lh_notes"]                    # the rag's right hand is off the beat
    t = load("tune")
    assert t["notes"]["nocturne"] == 20 and t["notes"]["left_hand"] == 48
    v = load("variation")
    row = [r for r in LEDGER if r["part"] == 27][0]
    assert v["part"] == 27 and row["measure"] == v["measure"] and row["seconds"] == pytest.approx(v["seconds"], abs=0.05)


def test_the_part_keeps_the_series_rules():
    check_clips(compute)
    check_scenes_and_clips(compute, SCENES)
    check_windows(compute, SCENES)
    check_ear_thread(compute, SCENES)
