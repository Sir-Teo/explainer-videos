"""Part 57 of *Music, Built*: what the film says is what was computed, and every sound keeps the series' rules.

    python -m pytest -q tests/music/test_music57.py
"""

import pytest

from tests.music.partcheck import check_clips, check_ear_thread, check_scenes_and_clips, check_windows
from videos.music.music57 import compute
from videos.music.music57.manifest import SCENES
from videos.music.variations import LEDGER

load = compute.load


def test_hook_and_war():
    h = load("hook")
    assert h["answer"] == "second" and h["war"]["plr"] < h["gentle"]["plr"] - 5 and h["war"]["gr_max"] > h["gentle"]["gr_max"] + 10
    rows = load("war")["rows"]
    plr = [r["plr"] for r in rows]
    assert all(a >= b - 0.01 for a, b in zip(plr, plr[1:])) and plr[0] > 14 and plr[-1] < 7
    assert all(r["tp"] <= -0.95 for r in rows)
    assert max(r["lra"] for r in rows) < 1.0


def test_meter_claims():
    m = load("meters")
    for c in m["checks"]:
        assert c["ours_I"] == pytest.approx(c["ffmpeg_I"], abs=0.1) and c["ours_TP"] == pytest.approx(c["ffmpeg_TP"], abs=0.15)
        assert c["ours_LRA"] == pytest.approx(c["ffmpeg_LRA"], abs=0.5)
    assert m["tones"]["high"] - m["tones"]["low"] > 5
    assert m["blocks"]["integrated"] > m["blocks"]["ungated"] + 1


def test_peaks_limits_and_normalization():
    t = load("truepeak")
    assert t["sine_tp"] == pytest.approx(3.01, abs=0.2) and t["clipped"]["true"] > 1.5 and t["limited"]["true"] <= -0.95
    lim = load("limiter")
    assert lim["clip_tp"] > 0 and lim["lim_tp"] <= -0.95
    n = load("norm")
    assert n["answer"] == "first" and n["gains"]["-8.0"] < -5 and n["gains"]["-20.0"] > 3
    assert load("matched")["difference_db"] == 1.0


def test_dither_and_vinyl():
    d = load("dither")
    assert d["snr_16"] == pytest.approx(98.08, abs=0.01)
    v = load("vinyl")
    assert v["at"]["20"] == pytest.approx(19.27, abs=0.05) and v["exc_50"] > 100 * v["exc_5k"] - 1


def test_variation_57():
    v = load("variation")
    row = [r for r in LEDGER if r["part"] == 57][0]
    assert v["part"] == 57 and row["measure"] == v["measure"] and row["seconds"] == pytest.approx(v["seconds"], abs=0.05)


def test_the_part_keeps_the_series_rules():
    check_clips(compute)
    check_scenes_and_clips(compute, SCENES)
    check_windows(compute, SCENES)
    check_ear_thread(compute, SCENES)
