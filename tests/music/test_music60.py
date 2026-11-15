"""Part 60 of *Music, Built*: what the film says is what was computed, and every sound keeps the series' rules.

    python -m pytest -q tests/music/test_music60.py
"""

import pytest

from tests.music.partcheck import check_clips, check_ear_thread, check_scenes_and_clips, check_windows
from videos.music.music60 import compute
from videos.music.music60.manifest import SCENES
from videos.music.variations import LEDGER

load = compute.load


def test_hook_and_melodies():
    h = load("hook")
    assert h["a"][:8] == h["b"][:8] and h["a"][8:] != h["b"][8:]
    m = load("melodies")
    eff = [m["effective"][str(k)] for k in m["ks"]]
    assert all(a < b for a, b in zip(eff, eff[1:]))
    assert m["effective"]["8"] < 1e-4 * m["uniform"]["8"]
    assert 0.01 < m["pair_share8"] < 0.2


def test_money():
    w = load("waterfall")
    assert 0.003 < w["rate"] < 0.006
    lab, ind = w["million_label"], w["million_indie"]
    assert ind["the artist (credited, against the advance)"] > 4 * lab["the artist (credited, against the advance)"]
    d = load("deals")
    assert d["need"] > 3 * d["label_breakeven"]
    p = load("pool")
    assert p["change"]["niche"] > 0 > p["change"]["chart"] and p["pro_rata"]["fraud"] > 5 * p["bot_fees"]


def test_market_live_similar_ai():
    mk = load("market")
    assert mk["gini_social"] > mk["gini_independent"] and mk["U_social"] > mk["U_independent"]
    t = load("live")["tickets"]
    assert t["dynamic"]["artist"] > t["clearing_price"]["artist"] > t["face_value"]["artist"]
    s = load("similar")["match"]
    assert s["transposed_notes"] == 0 and s["transposed_intervals"] == s["n"] - 1 and s["contour_dirs"] == s["n"] - 1
    a = load("ai")
    assert a["answer"] == "first" and a["surprise_new"] < a["surprise_old"]
    assert load("sample")["answer"] == "first"


def test_variation_60():
    v = load("variation")
    row = [r for r in LEDGER if r["part"] == 60][0]
    assert v["part"] == 60 and row["measure"] == v["measure"] and row["seconds"] == pytest.approx(v["seconds"], abs=0.05)
    t = load("tune60")["rows"]
    assert t["cover"]["to_us"] == 0 < t["remix"]["to_us"] < t["original"]["to_us"]


def test_the_part_keeps_the_series_rules():
    check_clips(compute)
    check_scenes_and_clips(compute, SCENES)
    check_windows(compute, SCENES)
    check_ear_thread(compute, SCENES)
