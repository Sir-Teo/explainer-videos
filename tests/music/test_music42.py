"""Part 42 of *Music, Built*: what the film says is what was computed, and every sound keeps the series' rules.

    python -m pytest -q tests/music/test_music42.py
"""

import pytest

from tests.music.partcheck import check_clips, check_ear_thread, check_scenes_and_clips, check_windows
from videos.music.music42 import compute
from videos.music.music42.manifest import SCENES
from videos.music.variations import LEDGER

load = compute.load


def test_hook_and_search():
    h, s = load("hook"), load("search")
    assert h["answer"] == "second" and h["first"]["draft"] == 1 and h["kept"]["draft"] == s["best"]["draft"]
    assert sum(s["rejected"].values()) + s["survivors"] == s["drafts"] == 2000
    assert not s["best"]["verdict"]["fails"]


def test_ode_and_funnel():
    o = load("ode")
    assert o["moves"] == o["steps"] + o["repeats"] + o["leaps"] and o["leaps"] == 0
    f = load("funnel")
    assert f["counts"][0] == 15 ** 8 and all(a >= b for a, b in zip(f["counts"], f["counts"][1:]))


def test_dice_illiac_chains():
    d = load("dice")
    assert d["count"]["naive"] == 11 ** 16 and d["count"]["distinct"] < d["count"]["naive"]
    i = load("illiac")
    assert len(i["line"]) == 12 and i["rejected"]["end"] == max(i["rejected"].values())
    c = load("chains")
    assert c["orders"]["4"]["mean_copy"] > c["orders"]["1"]["mean_copy"] and c["answer"] == "second"


def test_quiz_and_tension():
    q = load("quiz")
    assert q["answer"] == "backwards"
    t = load("tension")
    assert t["late"]["fit"] > t["early"]["fit"] > 0 and t["late"]["peak_bar"] > t["early"]["peak_bar"]


def test_variation_42():
    v = load("variation")
    row = [r for r in LEDGER if r["part"] == 42][0]
    assert v["part"] == 42 and row["measure"] == v["measure"] and row["seconds"] == pytest.approx(v["seconds"], abs=0.05)


def test_the_part_keeps_the_series_rules():
    check_clips(compute)
    check_scenes_and_clips(compute, SCENES)
    check_windows(compute, SCENES)
    check_ear_thread(compute, SCENES)
