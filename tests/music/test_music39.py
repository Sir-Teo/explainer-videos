"""Part 39 of *Music, Built*: what the film says is what was computed, and every sound keeps the series' rules.

    python -m pytest -q tests/music/test_music39.py
"""

import pytest

from tests.music.partcheck import check_clips, check_ear_thread, check_scenes_and_clips, check_windows
from videos.music.music39 import compute
from videos.music.music39.manifest import SCENES
from videos.music.variations import LEDGER

load = compute.load


def test_hook_and_thirds():
    h = load("hook")
    assert h["chords"] == 26 and h["answer"] == 3 and h["keys"]["distinct"] == [3, 7, 11]
    t = load("thirds")
    assert t["keys"]["distinct"] == [0, 4, 8]
    assert load("fast")["bpm"] == 286


def test_bebop_and_scales():
    b = load("bebop")
    assert sum(b["bebop"]["hits"]) == len(b["bebop"]["hits"]) == 8 and sum(b["plain"]["hits"]) == 5
    assert b["claim"]["bebop_all"] and b["major"]["bebop_all"]
    a = load("avoid")
    assert a["scale"]["avoid"] == [5] and a["tops"] == [77, 76]


def test_improviser_as_said():
    i = load("improv")
    assert i["answer"] == "B" and i["order"]["B"] == "improviser"
    assert i["judge_imp"]["on_beat_chord_tones"] > i["judge_rnd"]["on_beat_chord_tones"]
    st = i["stats"]
    assert st["improviser"]["on_beat_chord_tones"] > st["scale"]["on_beat_chord_tones"] > st["chromatic"]["on_beat_chord_tones"]
    assert st["improviser"]["guide_at_changes"] > 0.8 and st["scale"]["in_scale"] == 1.0


def test_variation_39():
    t = load("tune")
    assert t["keys"]["distinct"] == [0, 4, 8] and t["judge_solo"]["on_beat_chord_tones"] > 0.75
    v = load("variation")
    row = [r for r in LEDGER if r["part"] == 39][0]
    assert v["part"] == 39 and row["measure"] == v["measure"] and row["seconds"] == pytest.approx(v["seconds"], abs=0.05)


def test_the_part_keeps_the_series_rules():
    check_clips(compute)
    check_scenes_and_clips(compute, SCENES)
    check_windows(compute, SCENES)
    check_ear_thread(compute, SCENES)
