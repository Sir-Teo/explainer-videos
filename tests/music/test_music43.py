"""Part 43 of *Music, Built*: what the film says is what was computed, and every sound keeps the series' rules.

    python -m pytest -q tests/music/test_music43.py
"""

import pytest

from tests.music.partcheck import check_clips, check_ear_thread, check_scenes_and_clips, check_windows
from videos.music.music43 import compute
from videos.music.music43.manifest import SCENES
from videos.music.variations import LEDGER

load = compute.load


def test_hook_and_identity():
    h = load("hook")
    assert h["r"]["one-three"] > 0.999 > h["r"]["one-two"]
    i = load("identity")
    assert i["ranking"][0][0] == "pianist D" and i["ranking"][0][1] > i["take_ranking"][0][1] > i["between_max"]


def test_duo_and_quartet():
    d = load("duo")["cases"]
    assert abs(d["nobody listens"]["final_ms"]) > 150 and abs(d["both listen"]["final_ms"]) < 80
    assert abs(d["one over-corrects"]["final_ms"]) > 150
    c = load("duo_curve")
    assert 0.6 < c["best_alpha"] < 1.1
    q = load("quartet")
    assert abs(q["democratic"]["spread_ms"] - q["autocratic"]["spread_ms"]) < 5


def test_vibrato_and_ritard():
    v = load("vibrato")
    assert v["answer"] == "the same" and abs(v["mean_hz"] - 440.0) < 0.5
    r = load("ritard")
    assert r["curves"]["2"][-1] == pytest.approx(0.5)


def test_variation_43():
    v = load("variation")
    row = [r for r in LEDGER if r["part"] == 43][0]
    assert v["part"] == 43 and row["measure"] == v["measure"] and row["seconds"] == pytest.approx(v["seconds"], abs=0.05)


def test_the_part_keeps_the_series_rules():
    check_clips(compute)
    check_scenes_and_clips(compute, SCENES)
    check_windows(compute, SCENES)
    check_ear_thread(compute, SCENES)
