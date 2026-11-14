"""Part 30 of *Music, Built*: what the film says is what was computed, and every sound keeps the series' rules.

    python -m pytest -q tests/music/test_music30.py
"""

import pytest

from tests.music.partcheck import check_clips, check_ear_thread, check_scenes_and_clips, check_windows
from videos.music.music30 import compute
from videos.music.music30.manifest import SCENES
from videos.music.variations import LEDGER

load = compute.load


def test_tape_and_studio():
    t = load("tape")
    assert t["order"][["A", "B", "C", "D"].index(t["answer"])] == "bell"
    assert t["attack"]["reversed"] > 2.5 > t["attack"]["bell"]
    s = load("speeds")["durations"]
    assert s["double"] == pytest.approx(s["normal"] / 2, rel=0.01) and s["half"] == pytest.approx(2 * s["normal"], rel=0.01)
    st = load("studie")
    assert st["n_freqs"] == 81 and st["step_cents"] == pytest.approx(111.45, abs=0.01)


def test_clouds_masses_phasing():
    c = load("clouds")
    assert c["answer"] == "A"
    tot = sum(c["hist"])
    assert tot >= 595 and sum(abs(h - e) for h, e in zip(c["hist"], c["expect"])) / tot < 0.15
    m = load("mass")
    assert all(7.5 < b < 9.5 for b in m["beats"])
    ph = load("phasing")
    u = [p["unisons"] for p in ph["patterns"]]
    assert u[0] == 12 and u[3] == u[6] == u[9] == 6 and u[1] == u[11] == 0
    assert load("sieves")["diatonic"] == [0, 2, 4, 5, 7, 9, 11]
    assert load("additive")["lengths"] == [1, 2, 3, 4, 5]


def test_spectral():
    s = load("spectral")
    assert s["answer"] == "B" and 100 < s["f0"] < 125 and len(s["notes"]) == 16
    assert {n["inst"] for n in s["notes"]} == {"piano", "bowed", "voice"}


def test_variation_30():
    t = load("tune")
    assert t["cents"]["13"] == pytest.approx(-59.5, abs=0.1) and t["cents"]["11"] == pytest.approx(51.3, abs=0.1)
    v = load("variation")
    row = [r for r in LEDGER if r["part"] == 30][0]
    assert v["part"] == 30 and row["measure"] == v["measure"] and row["seconds"] == pytest.approx(v["seconds"], abs=0.05)


def test_the_part_keeps_the_series_rules():
    check_clips(compute)
    check_scenes_and_clips(compute, SCENES)
    check_windows(compute, SCENES)
    check_ear_thread(compute, SCENES)
