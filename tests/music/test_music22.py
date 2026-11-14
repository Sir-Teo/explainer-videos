"""Part 22 of *Music, Built*: what the film says is what was computed, and every sound keeps the series' rules.

    python -m pytest -q tests/music/test_music22.py
"""

import pytest

from tests.music.partcheck import check_clips, check_ear_thread, check_scenes_and_clips, check_windows
from videos.music.music22 import compute
from videos.music.music22.manifest import SCENES
from videos.music.variations import LEDGER

load = compute.load


def letters(ns):
    return [{0: "C", 2: "D", 4: "E", 5: "F", 7: "G", 9: "A", 11: "B"}[n[0] % 12] for n in ns]


def test_reduction_and_skeletons():
    lv = load("hook")["levels"]
    assert "".join(letters(lv[1][:8])) == "CGAGFEDC" and letters(lv[3]) == list("CCGGCC") and letters(lv[4]) == list("CGC")
    s = load("skeleton")
    assert letters(s["B"]) == list("CGEC") and letters(s["A"]) == list("CAFC")


def test_urlinie_grouping_parses():
    u = load("urlinie")
    assert u["n"] == 51 and u["real"]["5-4-3-2-1"] == 6 and u["real"]["3-2-1"] == 16 and u["tune"] == "5-4-3-2-1"
    assert u["shuffled"]["3-2-1"] + u["shuffled"].get("5-4-3-2-1", 0) == pytest.approx(3.42, abs=0.01)
    g = load("grouping")
    assert g["top"] == [8.0, 16.0, 24.0, 32.0, 40.0]
    p = load("parses")
    assert p["examples"]["I vi ii V I"]["parses"] == 5 and p["examples"]["I IV I V I"]["parses"] == 0
    assert p["growth"] == {"4": 2, "7": 14, "10": 132, "13": 1430}


def test_learned():
    d = load("learned")
    b = d["bits"]
    assert d["train_phrases"] == 934 and d["test_phrases"] == 231 and d["vocab"] == 42
    assert round(b["bigram"], 2) == 3.33 and round(b["functional"], 2) == 3.90 and round(b["latent"]["12"]["test"], 2) == 3.46
    assert b["bigram"] < b["latent"]["12"]["test"] < b["functional"] < b["unigram"]
    assert d["emit"]["SR"][0][1] == "I" and d["emit"]["TR"][0][1] == "I"


def test_variation_22():
    t = load("tune")
    assert len(t["skeleton"]) == 12 and len(t["regrown"]) == 37 and t["chord_tones_on_strong_beats"] == 15 and t["strong_beats"] == 24
    v = load("variation")
    row = [r for r in LEDGER if r["part"] == 22][0]
    assert v["part"] == 22 and row["measure"] == v["measure"] and row["seconds"] == pytest.approx(v["seconds"], abs=0.05)


def test_the_part_keeps_the_series_rules():
    check_clips(compute)
    check_scenes_and_clips(compute, SCENES)
    check_windows(compute, SCENES)
    check_ear_thread(compute, SCENES)
