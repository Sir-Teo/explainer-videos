"""Part 45 of *Music, Built*: what the film says is what was computed, and every sound keeps the series' rules.

    python -m pytest -q tests/music/test_music45.py
"""

import pytest

from tests.music.partcheck import check_clips, check_ear_thread, check_scenes_and_clips, check_windows
from videos.music.music45 import compute
from videos.music.music45.manifest import SCENES
from videos.music.variations import LEDGER

load = compute.load


def test_hook_and_streaming():
    h = load("hook")
    assert h["leap_right"] > h["leap_heard"]
    cases = {c["name"]: c for c in load("aba")["cases"]}
    assert not cases["3 semitones, slow"]["model_streams"] and cases["12 semitones, slow"]["model_streams"]
    assert not cases["6 semitones, slow"]["model_streams"] and cases["6 semitones, fast"]["model_streams"]
    b = load("boundary")
    assert b["rms_st"] < 0.5


def test_interleaving_and_timbre():
    i = load("inter")
    assert i["crossings"] >= 10 and i["crossings_apart"] == 0 and i["answer"] == "Frère Jacques"
    t = load("timbre")
    assert len(t["space"]["coords"]) == len(t["features"]) == 13


def test_variation_45():
    v = load("variation")
    row = [r for r in LEDGER if r["part"] == 45][0]
    assert v["part"] == 45 and row["measure"] == v["measure"] and row["seconds"] == pytest.approx(v["seconds"], abs=0.05)


def test_the_part_keeps_the_series_rules():
    check_clips(compute)
    check_scenes_and_clips(compute, SCENES)
    check_windows(compute, SCENES)
    check_ear_thread(compute, SCENES)
