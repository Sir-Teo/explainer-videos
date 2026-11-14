"""Part 31 of *Music, Built*: what the film says is what was computed, and every sound keeps the series' rules.

    python -m pytest -q tests/music/test_music31.py
"""

import pytest

from tests.music.partcheck import check_clips, check_ear_thread, check_scenes_and_clips, check_windows
from videos.music.music31 import compute
from videos.music.music31.manifest import SCENES
from videos.music.variations import LEDGER

load = compute.load


def test_moves_and_quizzes():
    p = load("plr")
    assert p["order"] == ["L", "R", "P"]
    assert load("keys")["answer"] == "A" and load("keys")["A_in_C"]
    po = load("poles")
    assert po["answer"] == "B" and po["common"] == [2, 0] and po["vl"] == [1, 3]
    m = load("minor")["moves"]
    assert [x["to"] for x in m] == ["A", "F", "C"]
    c = load("compound")["pairs"]
    assert c["LP"]["to"] == "E" and c["PL"]["to"] == "Ab" and c["RP"]["to"] == "A"


def test_groups_and_space():
    g = load("groups")
    assert g["plr"] == g["ti"] == 24 and g["commute"]
    assert load("commute")["same"]
    assert load("relations")["orders"] == {"P": 2, "L": 2, "R": 2, "PL": 3, "PR": 4, "LR": 12}
    s = load("spheres")
    assert s["hist"] == {"0": 1, "1": 3, "2": 6, "3": 8, "4": 5, "5": 1} and s["by"]["5"] == ["Bbm"]
    assert load("hamilton")["count"] == 62 and len(load("chain")["full"]) == 24
    v = load("vl")
    assert 0.6 < v["r"] < 0.85 and v["max_vl"] == 6 and sorted(v["far_vl"]) == ["Bb", "D", "F#"]
    cm = load("comma")
    assert cm["comma_cents"] == pytest.approx(21.51, abs=0.01)
    f = load("film3")["moves"]
    assert f[2]["to"] == "F#" and f[2]["common"] == 0 and f[2]["vl"] == 6
    sv = load("sevenths")
    assert sv["n"] == 10 and sv["two_semitone"] == 9


def test_variation_31():
    t = load("tune")
    assert t["walk"] == ["C", "C", "Am", "C", "F", "C", "G", "C"]
    v = load("variation")
    row = [r for r in LEDGER if r["part"] == 31][0]
    assert v["part"] == 31 and row["measure"] == v["measure"] and row["seconds"] == pytest.approx(v["seconds"], abs=0.05)


def test_the_part_keeps_the_series_rules():
    check_clips(compute)
    check_scenes_and_clips(compute, SCENES)
    check_windows(compute, SCENES)
    check_ear_thread(compute, SCENES)
