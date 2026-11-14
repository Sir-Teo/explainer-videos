"""Part 36 of *Music, Built*: what the film says is what was computed, and every sound keeps the series' rules.

    python -m pytest -q tests/music/test_music36.py
"""

import pytest

from tests.music.partcheck import check_clips, check_ear_thread, check_scenes_and_clips, check_windows
from videos.music.music36 import compute
from videos.music.music36.manifest import SCENES
from videos.music.variations import LEDGER

load = compute.load


def test_bells_and_pitch():
    assert load("hook")["answer"] == "different"
    lu = load("lu")
    assert abs(lu["comma"] - 23.46) < 0.01 and len(lu["twelve"]) == 12
    j = load("jingfang")
    assert j["best"][0]["n"] == 53 and 3 < j["beat12"] < 4 and 0.5 < j["beat53"] < 0.6
    assert sorted(load("twelve")["steps"]) [0] > 89


def test_gamelan():
    s = load("spectra")
    assert 1200.0 in [round(x) for x in s["min_harmonic"]] and all(abs(x - 1200) > 10 for x in s["min_bar"])
    o = load("ombak")
    assert o["answer"] == "B" and o["cents_off"][0] > o["cents_off"][1] > o["cents_off"][2]
    k = load("kotekan")
    assert k["answer"] == "two" and all((a is None) != (b is None) for a, b in zip(k["polos"], k["sangsih"]))
    c = load("cycle")
    assert c["colotomic"][15] == ["gong", "kenong"]


def test_variation_36():
    t = load("tune")
    assert t["worst"] < 10 and len(t["balungan"]) == 16
    v = load("variation")
    row = [r for r in LEDGER if r["part"] == 36][0]
    assert v["part"] == 36 and row["measure"] == v["measure"] and row["seconds"] == pytest.approx(v["seconds"], abs=0.05)


def test_the_part_keeps_the_series_rules():
    check_clips(compute)
    check_scenes_and_clips(compute, SCENES)
    check_windows(compute, SCENES)
    check_ear_thread(compute, SCENES)
