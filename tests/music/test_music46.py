"""Part 46 of *Music, Built*: what the film says is what was computed, and every sound keeps the series' rules.

    python -m pytest -q tests/music/test_music46.py
"""

import pytest

from tests.music.partcheck import check_clips, check_ear_thread, check_scenes_and_clips, check_windows
from videos.music.music46 import compute
from videos.music.music46.manifest import SCENES
from videos.music.variations import LEDGER

load = compute.load


def test_hook_and_endings():
    h = load("hook")
    assert h["ics"]["F sharp"] > h["ics"]["A"] > h["ics"]["C"] and h["answer"] == "F sharp"
    e = load("endings")
    assert e["delayed"]["ic"][-1] < e["expected"]["ic"][-1] < e["denied"]["ic"][-1]   # delay makes the arrival likelier
    a = load("again")["ic"]
    assert a[0] > a[1] > a[2]


def test_listener_numbers():
    c = load("compare")
    v = dict(zip(c["names"], c["mean_ic"]))
    assert v["random notes of the scale"] > v["the Tune"] and v["Part 42: a rejected draft"] > v["Part 42: the kept draft"]
    p = load("probe")["ic"]
    assert p["C"] < p["D"] < p["F sharp"]
    l = load("learn")
    assert l["tp_inside"] == pytest.approx(1.0) and l["answer"] == "second"


def test_variation_46():
    v = load("variation")
    row = [r for r in LEDGER if r["part"] == 46][0]
    assert v["part"] == 46 and row["measure"] == v["measure"] and row["seconds"] == pytest.approx(v["seconds"], abs=0.05)


def test_the_part_keeps_the_series_rules():
    check_clips(compute)
    check_scenes_and_clips(compute, SCENES)
    check_windows(compute, SCENES)
    check_ear_thread(compute, SCENES)
