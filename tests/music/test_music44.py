"""Part 44 of *Music, Built*: what the film says is what was computed, and every sound keeps the series' rules.

    python -m pytest -q tests/music/test_music44.py
"""

import pytest

from tests.music.partcheck import check_clips, check_ear_thread, check_scenes_and_clips, check_windows
from videos.music.music44 import compute
from videos.music.music44.manifest import SCENES
from videos.music.variations import LEDGER

load = compute.load


def test_scene_and_hook():
    s = load("scene")
    assert s["best"]["worst_frames"] <= 1.0 and s["best"]["beats"] == [4.0, 11.0, 16.0]
    assert max(s["click_err_frames"]) > 1.0                             # the rounded click drifts past a frame
    assert load("hook")["answer"] == "first" and load("sync")["answer"] == "third"


def test_game_and_quantise():
    q = load("quantise")["quantise"]
    for k in ("beat", "bar", "phrase"):
        assert q[k]["mean"] == pytest.approx(q[k]["expected"], abs=0.1)
    g = load("game")
    assert g["states"][0] == "explore" and set(g["states"]) <= {"explore", "danger", "combat", "victory"}


def test_mix_and_chip():
    m = load("mix")
    assert m["ratio_after_db"] > m["ratio_before_db"] + 3
    a = load("arp")
    assert a["answer"] == "second" and a["rate"] == 60.0


def test_variation_44():
    v = load("variation")
    row = [r for r in LEDGER if r["part"] == 44][0]
    assert v["part"] == 44 and row["measure"] == v["measure"] and row["seconds"] == pytest.approx(v["seconds"], abs=0.05)
    t = load("tune")
    assert 0.5 + 14 * t["beat"] == pytest.approx(t["hit"])


def test_the_part_keeps_the_series_rules():
    check_clips(compute)
    check_scenes_and_clips(compute, SCENES)
    check_windows(compute, SCENES)
    check_ear_thread(compute, SCENES)
