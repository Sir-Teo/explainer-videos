"""Part 34 of *Music, Built*: what the film says is what was computed, and every sound keeps the series' rules.

    python -m pytest -q tests/music/test_music34.py
"""

import pytest

from tests.music.partcheck import check_clips, check_ear_thread, check_scenes_and_clips, check_windows
from videos.music.music34 import compute
from videos.music.music34.manifest import SCENES
from videos.music.variations import LEDGER

load = compute.load


def test_drone_and_swaras():
    t = load("tanpura")
    assert t["at"]["jawari"]["0.1"] > 2 * t["at"]["plain"]["0.1"] and t["at"]["jawari"]["0.3"] > 2 * t["at"]["plain"]["0.3"]
    assert load("shruti")["n"] == 22
    g = load("ga")
    assert g["answer"] == "A" and 9 < g["beat_hz"] < 12
    assert abs(load("comma")["diff"] - 21.51) < 0.01


def test_ragas_and_scales():
    r = load("raga")
    assert r["answer"] == "B" and r["order"][1] == "Yaman" and 6 in r["ragas"]["Yaman"]["aroha"] and 5 not in r["ragas"]["Yaman"]["aroha"]
    assert set(load("bhupali")["aroha"]) == {0, 2, 4, 7, 9, 12}
    th = load("thaat")
    assert th["n_space"] == 32 and th["n_mela"] == 72 and th["thaat_melas"]["Bilawal"] == 29 and th["thaat_melas"]["Kalyan"] == 65


def test_tala_and_tihai():
    tl = load("tala")["talas"]
    assert [tl[k]["beats"] for k in ("Teentaal", "Jhaptaal", "Rupak")] == [16, 10, 7]
    assert sum(tl["Jhaptaal"]["vibhags"]) == 10
    h = load("hook")
    assert h["tihai"]["end"] == 16 and h["starts"] == [4, 9, 14]
    q = load("tihai")
    assert q["answer"] == "B" and q["plans"]["A"]["g"] == 0 and q["plans"]["B"]["g"] == 2 and q["plans"]["A"]["valid"] and q["plans"]["B"]["valid"]
    assert {(x["p"], x["g"]) for x in q["solutions"]["9"] if x["cycles"] == 1} == {(1, 3), (3, 0)}
    assert load("chakkardar")["count"] == 15


def test_variation_34():
    t = load("tune")
    assert t["n_beats"] == 16
    v = load("variation")
    row = [r for r in LEDGER if r["part"] == 34][0]
    assert v["part"] == 34 and row["measure"] == v["measure"] and row["seconds"] == pytest.approx(v["seconds"], abs=0.05)


def test_the_part_keeps_the_series_rules():
    check_clips(compute)
    check_scenes_and_clips(compute, SCENES)
    check_windows(compute, SCENES)
    check_ear_thread(compute, SCENES)
