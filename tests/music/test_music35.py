"""Part 35 of *Music, Built*: what the film says is what was computed, and every sound keeps the series' rules.

    python -m pytest -q tests/music/test_music35.py
"""

import pytest

from tests.music.partcheck import check_clips, check_ear_thread, check_scenes_and_clips, check_windows
from videos.music.music35 import compute
from videos.music.music35.manifest import SCENES
from videos.music.variations import LEDGER

load = compute.load


def test_quizzes():
    h = load("hook")
    assert h["order"][["A", "B", "C"].index(h["answer"])] == 350
    t = load("turkish")
    assert t["answer"] == "B" and t["third"]["arabic"] == 350 and abs(t["third"]["turkish"] - 384.9) < 0.1
    i = load("iqa")
    assert i["order"][["A", "B", "C"].index(i["answer"])] == "samai thaqil" and i["iqaat"]["samai thaqil"]["beats"] == 10


def test_numbers():
    n = {r["name"]: r for r in load("neutral")["rows"]}
    assert abs(n["Zalzal's neutral third 27/22"]["e24"]) < 5 and abs(n["just major third 5/4"]["e53"]) < 1.5
    assert abs(n["just minor third 6/5"]["e24"]) > 15
    s = load("safi")
    assert len(s["notes"]) == 17
    m = load("maqamat")
    assert m["scales"]["Saba"][-1] < 1200
    assert load("descent")["down"][1] == 1000
    assert [round(c) for c in load("thirds3")["cents"]] == [350, 355, 362]


def test_variation_35():
    t = load("tune")
    assert t["changed"] == {"Rast": 2, "Bayati": 6, "Hijaz": 4}
    v = load("variation")
    row = [r for r in LEDGER if r["part"] == 35][0]
    assert v["part"] == 35 and row["measure"] == v["measure"] and row["seconds"] == pytest.approx(v["seconds"], abs=0.05)


def test_the_part_keeps_the_series_rules():
    check_clips(compute)
    check_scenes_and_clips(compute, SCENES)
    check_windows(compute, SCENES)
    check_ear_thread(compute, SCENES)
