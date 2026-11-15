"""Part 41 of *Music, Built*: what the film says is what was computed, and every sound keeps the series' rules.

    python -m pytest -q tests/music/test_music41.py
"""

import pytest

from tests.music.partcheck import check_clips, check_ear_thread, check_scenes_and_clips, check_windows
from videos.music.music41 import compute
from videos.music.music41.manifest import SCENES
from videos.music.variations import LEDGER

load = compute.load


def test_hook_is_on_the_harmonics():
    h = load("hook")
    assert h["answer"] == 4 and h["fusion"] > 0.99
    c = {int(k): v for k, v in h["cents_off"].items()}
    assert c[24] == pytest.approx(0.0) and abs(c[19]) < 3 and 13 < c[28] < 14.5      # tempered thirds are 14 cents sharp


def test_quizzes():
    w = load("which")
    assert w["names"][w["answer"] - 1] == "clarinet"
    b = load("bright")
    assert b["centroid"]["loud"] > 1.6 * b["centroid"]["soft"]


def test_sections_and_spacing():
    s = load("section")
    assert s["incoherent_gain_db"] < s["gain_db"] < s["coherent_gain_db"]
    z = load("sizes")["level_db"]
    assert all(b > a for a, b in zip(z, z[1:]))
    r = load("spacing")["roughness"]
    assert r["close, low"] > r["open"] > r["close, high"]


def test_matching():
    m = load("match")
    e = {int(k): v for k, v in m["results"]["4"]["error_by_size"].items()}
    assert e[1] > e[4]
    b = load("bell")
    assert b["errors"]["4"] > b["vowel_error"]                          # a bell's tierce is not a harmonic


def test_variation_41():
    v = load("variation")
    row = [r for r in LEDGER if r["part"] == 41][0]
    assert v["part"] == 41 and row["measure"] == v["measure"] and row["seconds"] == pytest.approx(v["seconds"], abs=0.05)


def test_the_part_keeps_the_series_rules():
    check_clips(compute)
    check_scenes_and_clips(compute, SCENES)
    check_windows(compute, SCENES)
    check_ear_thread(compute, SCENES)
