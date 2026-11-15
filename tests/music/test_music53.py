"""Part 53 of *Music, Built*: what the film says is what was computed, and every sound keeps the series' rules.

    python -m pytest -q tests/music/test_music53.py
"""

import pytest

from tests.music.partcheck import check_clips, check_ear_thread, check_scenes_and_clips, check_windows
from videos.music.music53 import compute
from videos.music.music53.manifest import SCENES
from videos.music.variations import LEDGER

load = compute.load


def test_bytes_and_files():
    h = load("hook")
    assert h["answer"] == "first" and 6 < h["spread_ms"] < 8
    b = load("bytes")
    assert b["running_bytes"] < b["plain_bytes"] and b["spread"]["plain"][-1] == pytest.approx(15.36)
    s = load("smf")
    assert s["roundtrip"] and s["wav_bytes"] / s["bytes"] > 1000


def test_engine_claims():
    c = load("callback")
    assert all(c["identical"]) and c["load"][0] > c["load"][-1] and c["missed"] > 0
    t = load("timing")
    assert 15 < t["max_ms"] <= t["block_ms"] + 1e-6
    p = load("pdc")
    assert p["notch_hz"] == pytest.approx(100.0)
    z = load("zipper")
    assert 25 < z["step_cents"] < 40


def test_variation_53():
    v = load("variation")
    t = load("tune53")
    row = [r for r in LEDGER if r["part"] == 53][0]
    assert v["part"] == 53 and row["measure"] == v["measure"] and row["seconds"] == pytest.approx(v["seconds"], abs=0.05)
    assert t["identical"] and t["ratios"] == [3.0, 4.0, 5.0, 6.0]


def test_the_part_keeps_the_series_rules():
    check_clips(compute)
    check_scenes_and_clips(compute, SCENES)
    check_windows(compute, SCENES)
    check_ear_thread(compute, SCENES)
