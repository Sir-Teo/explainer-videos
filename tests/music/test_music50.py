"""Part 50 of *Music, Built*: what the film says is what was computed, and every sound keeps the series' rules.

    python -m pytest -q tests/music/test_music50.py
"""

import pytest

from tests.music.partcheck import check_clips, check_ear_thread, check_scenes_and_clips, check_windows
from videos.music.music50 import compute
from videos.music.music50.manifest import SCENES
from videos.music.variations import LEDGER

load = compute.load


def test_hook_corrects():
    h = load("hook")
    assert h["before_cents"] > 15 and h["after_cents"] < 3


def test_shapers_and_intermodulation():
    s = load("shapers")
    assert s["cheb"][2] == pytest.approx(-6.02, abs=0.05)
    i = load("imd")
    assert i["fifth"]["gcd"] == 110 and i["third"]["gcd"] == 55
    a = load("alias")["measure"]
    assert a["x8"] < a["adaa"] < a["plain"]


def test_dynamics():
    c = load("curves")
    assert c["attack_ms"] < 30 and c["release_ms"] > 100
    cp = load("comp")
    assert cp["spread"]["compressed"] < cp["spread"]["plain"]


def test_time_and_pitch():
    p = load("pitch")["durations"]
    assert p["psola"] == pytest.approx(p["original"]) and p["resampled"] < p["original"]


def test_variation_50():
    v = load("variation")
    row = [r for r in LEDGER if r["part"] == 50][0]
    assert v["part"] == 50 and row["measure"] == v["measure"] and row["seconds"] == pytest.approx(v["seconds"], abs=0.05)


def test_the_part_keeps_the_series_rules():
    check_clips(compute)
    check_scenes_and_clips(compute, SCENES)
    check_windows(compute, SCENES)
    check_ear_thread(compute, SCENES)
