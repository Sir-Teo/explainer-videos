"""Part 38 of *Music, Built*: what the film says is what was computed, and every sound keeps the series' rules.

    python -m pytest -q tests/music/test_music38.py
"""

import pytest

from tests.music.partcheck import check_clips, check_ear_thread, check_scenes_and_clips, check_windows
from explainer.music.monochord import blues as BL
from videos.music.music38 import compute
from videos.music.music38.manifest import SCENES
from videos.music.variations import LEDGER

load = compute.load


def test_hook_and_swing():
    h = load("hook")
    assert h["ratio"] == 3.0 and h["answer"] == "three times" and 120 < h["short_ms"] < 130
    s = load("swing")
    assert s["ratios"]["100"] > s["ratios"]["180"] > s["ratios"]["260"] >= 1.0
    j = load("jitter")
    assert j["sd_ms"] == 15.0 and j["max_ms"] < 50


def test_blues_and_rag():
    f = load("form")
    assert f["changes"][4] == ["F7"] and f["changes"][8] == ["G7"]
    b = load("blue")
    assert b["cents"]["minor"] == 300 and b["cents"]["major"] == 400 and 300 < b["cents"]["bent"][1] < 400
    r = load("rag")
    R_, L_ = r["sync_right"], r["sync_left"]
    assert R_["between"] > R_["onsets"] / 2 and L_["between"] < L_["onsets"] / 10 and R_["syncopated"] > L_["syncopated"]


def test_walking_guide_subs():
    w = load("walking")
    assert w["roots_ok"] and all(a == 1 for a in w["approaches"])
    g = load("guide")
    assert g["iiVI"]["total"] == 2 and g["jazz"]["max_step"] <= 3
    s = load("subs")
    assert s["answer"] == "second" and s["shared"] == [5, 11]
    assert [abs(s["bass_sub"][i + 1] - s["bass_sub"][i]) for i in range(2)] == [1, 1]
    assert [abs(s["bass_plain"][i + 1] - s["bass_plain"][i]) for i in range(2)] == [7, 5]


def test_variation_38():
    t = load("tune")
    assert t["rag_sync"]["syncopated"] > 0 and t["riff_bpm"] == 150
    v = load("variation")
    row = [r for r in LEDGER if r["part"] == 38][0]
    assert v["part"] == 38 and row["measure"] == v["measure"] and row["seconds"] == pytest.approx(v["seconds"], abs=0.05)
    assert f"{BL.swing_ratio(150):.1f}" in v["measure"]


def test_the_part_keeps_the_series_rules():
    check_clips(compute)
    check_scenes_and_clips(compute, SCENES)
    check_windows(compute, SCENES)
    check_ear_thread(compute, SCENES)


def test_guide_tones_do_not_distinguish_minor_and_half_diminished():
    minor, half = BL.chord("Cm7"), BL.chord("Cm7b5")
    assert (minor["third"], minor["seventh"]) == (half["third"], half["seventh"])
    assert set(minor["pcs"]) != set(half["pcs"])
