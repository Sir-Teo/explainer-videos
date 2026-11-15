"""Part 49 of *Music, Built*: what the film says is what was computed, and every sound keeps the series' rules.

    python -m pytest -q tests/music/test_music49.py
"""

import pytest

from tests.music.partcheck import check_clips, check_ear_thread, check_scenes_and_clips, check_windows
from videos.music.music49 import compute
from videos.music.music49.manifest import SCENES
from videos.music.variations import LEDGER

load = compute.load


def test_room_and_sweep():
    r = load("room")
    assert abs(r["rt60"] / r["eyring"] - 1) < 0.1
    assert load("sweep")["error_db"] < -15
    b = load("bands")
    assert b["plate"]["125"] > b["plate"]["4000"] and 300 < b["schroeder_freq"] < 900


def test_filters_and_combs():
    assert load("biquads")["butter_match"] < 1e-12
    assert load("combs")["pitch"] == pytest.approx(220, abs=1)
    assert load("ring")["info"]["50"]["pole_radius"] > load("ring")["info"]["2"]["pole_radius"]
    assert load("phase")["mag_ratio_db_max"] < 1e-6


def test_reverberators():
    s = load("schroeder")
    assert s["rt_schroeder"] == pytest.approx(2.0, rel=0.05)
    d = s["density"]
    assert max(d["room"]) > 0.9 and max(d["schroeder"]) < 0.5


def test_variation_49():
    v = load("variation")
    row = [r for r in LEDGER if r["part"] == 49][0]
    assert v["part"] == 49 and row["measure"] == v["measure"] and row["seconds"] == pytest.approx(v["seconds"], abs=0.05)


def test_the_part_keeps_the_series_rules():
    check_clips(compute)
    check_scenes_and_clips(compute, SCENES)
    check_windows(compute, SCENES)
    check_ear_thread(compute, SCENES)
