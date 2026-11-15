"""Part 51 of *Music, Built*: what the film says is what was computed, and every sound keeps the series' rules.

    python -m pytest -q tests/music/test_music51.py
"""

import pytest

from tests.music.partcheck import check_clips, check_ear_thread, check_scenes_and_clips, check_windows
from videos.music.music51 import compute
from videos.music.music51.manifest import SCENES
from videos.music.variations import LEDGER

load = compute.load


def test_hook_fit_is_close_and_misses_the_bump():
    d = load("fit")
    assert d["fit"]["mix"] == 0.0 and d["fit"]["res"] > 0 and 1.5 < d["fit"]["distance_db"] < 5
    t, p = d["spec"]["target"], d["spec"]["fit"]
    assert max(t[j] - p[j] for j in (5, 7, 9)) > 5
    assert d["organ"]["distance_db"] > 15 and d["recovered"]["distance_db"] < 1.5
    assert load("hook")["answer"] == "second"


def test_alias_claims():
    cv = load("alias")["curves"]
    gain = [n - p for n, p in zip(cv["naive"], cv["polyblep"])]
    assert 13.5 < min(gain) and max(gain) < 17
    assert all(q < p for p, q in zip(cv["polyblep"], cv["polyblep2"]))


def test_ladder_claims():
    d = load("ladder")
    assert d["peak"]["3.8"]["db"] > 12 and d["dc"]["3"] == pytest.approx(-12.04, abs=0.01)
    c = d["conv"]
    assert c["trapezoid"][0] < c["forward"][3] and c["corrected"][0] < c["forward"][0]
    for fc, f in d["osc"].items():
        assert abs(1200 * __import__("math").log2(f / float(fc))) < 25
    dr = load("drive")
    assert dr["h_lin"][3] > 0 > dr["h_nl"][3] + 10


def test_drums_and_tables():
    d = load("drums")
    assert d["tau"] == pytest.approx(d["tau_theory"], rel=0.02) and d["chirp"][0] > d["chirp"][3] > 51
    t = load("toms")
    assert t["low"]["tau"] > t["mid"]["tau"] > t["high"]["tau"] and t["low"]["start_hz"] < t["low"]["end_hz"]
    tb = load("table")
    assert tb["alias"]["limited"] < tb["alias"]["full"] - 30


def test_variation_51():
    v = load("variation")
    t = load("tune51")
    row = [r for r in LEDGER if r["part"] == 51][0]
    assert v["part"] == 51 and row["measure"] == v["measure"] and row["seconds"] == pytest.approx(v["seconds"], abs=0.05)
    assert t["notes"] == sum(t["counts"].values()) and t["alias_pb"] < t["alias_naive"] - 10


def test_the_part_keeps_the_series_rules():
    check_clips(compute)
    check_scenes_and_clips(compute, SCENES)
    check_windows(compute, SCENES)
    check_ear_thread(compute, SCENES)
