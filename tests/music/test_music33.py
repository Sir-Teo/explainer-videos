"""Part 33 of *Music, Built*: what the film says is what was computed, and every sound keeps the series' rules.

    python -m pytest -q tests/music/test_music33.py
"""

import pytest

from tests.music.partcheck import check_clips, check_ear_thread, check_scenes_and_clips, check_windows
from videos.music.music33 import compute
from videos.music.music33.manifest import SCENES
from videos.music.variations import LEDGER

load = compute.load


def test_euclid_items():
    e = load("euclid")
    assert e["result"] == "x..x.x..x.x.." and e["answer"] == "B" and e["gaps"]["B"] == [2, 1, 2, 1, 2]
    r = load("rank")
    assert r["count"] == 7 and r["rows"][0]["euclid"] and sum(x["euclid"] for x in r["rows"]) == 1
    ev = load("even")
    assert ev["bell"]["onsets"] == [0, 2, 4, 5, 7, 9, 11] and ev["pentatonic"]["onsets"] == [0, 2, 4, 7, 9]


def test_scales_oddity_canons():
    m = load("mos")
    assert m["sizes"] == [2, 3, 5, 7, 12, 17, 29, 41, 53] and len(m["steps"]["12"]) == 2
    assert load("golden")["sizes"][:6] == [2, 3, 5, 8, 13, 21]
    o = load("oddity")
    assert o["counts"]["12"]["7"] == 0 and o["counts"]["12"]["4"] == 20 and o["counts"]["12"]["5"] == 16 and o["n_pairs"]["6/12"] == 15
    c = load("canon")
    assert c["vuza"]["tiles"] and not c["vuza"]["A_periodic"] and not c["vuza"]["B_periodic"]
    assert c["vuza"]["n_tilings"] == 1296 and c["vuza"]["n_aperiodic"] == 432


def test_prosody_ringing_tunings():
    p = load("prosody")
    assert p["counts"][:7] == [1, 2, 3, 5, 8, 13, 21] and len(p["rhythms5"]) == 8 and p["distinct"] == 8
    assert load("meru")["rows"][7] == [1, 7, 15, 10, 1]
    r = load("ringing")
    assert r["distinct"] == 24 and r["back"]
    t = load("temper")
    assert t["answer"] == "B" and t["order"][1] == "just"
    assert [e["n"] for e in t["best"]] == [5, 7, 9, 10, 12, 19, 22, 31, 34, 53]
    assert t["vals"]["19"]["tempers"]["81/80"] and not t["vals"]["53"]["tempers"]["81/80"] and t["vals"]["53"]["tempers"]["schisma"]
    b = load("bp")
    assert abs(b["step_cents"] - 146.3) < 0.01


def test_variation_33():
    v = load("variation")
    row = [r for r in LEDGER if r["part"] == 33][0]
    assert v["part"] == 33 and row["measure"] == v["measure"] and row["seconds"] == pytest.approx(v["seconds"], abs=0.05)


def test_the_part_keeps_the_series_rules():
    check_clips(compute)
    check_scenes_and_clips(compute, SCENES)
    check_windows(compute, SCENES)
    check_ear_thread(compute, SCENES)
