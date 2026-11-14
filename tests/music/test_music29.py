"""Part 29 of *Music, Built*: what the film says is what was computed, and every sound keeps the series' rules.

    python -m pytest -q tests/music/test_music29.py
"""

import pytest

from tests.music.partcheck import check_clips, check_ear_thread, check_scenes_and_clips, check_windows
from videos.music.music29 import compute
from videos.music.music29.manifest import SCENES
from videos.music.variations import LEDGER

load = compute.load


def test_free_atonality():
    o = load("op19")
    pt = o["pc_time"]
    assert sorted(range(12), key=lambda k: -pt[k])[:2] == [11, 7]                 # B and G, the pulsing third
    assert all(x > 0 for x in pt)                                                 # all twelve used
    assert o["chromaticism"] == pytest.approx(0.247, abs=0.002)
    assert load("hook")["bars"] == 9


def test_sets_and_classes():
    s = load("sets")
    assert s["prime_A"] == s["prime_B"] == [0, 1, 4, 6] and s["answer"] == "inversion"
    assert s["examples"]["Tristan chord"]["prime"] == s["examples"]["half-diminished"]["prime"] == [0, 2, 5, 8]
    c = load("classes")
    assert c["brute"] == c["burnside"] == 224
    assert all(c["by_size"][k] == v for k, v in c["forte_sizes"].items())
    z = load("zhex")
    assert len(z["pairs"]) == 23 and z["by_size"]["6"] == 15 and z["hexachord"]["holds"] and z["hexachord"]["checked"] == 924
    h = load("hexpair")
    assert h["iv"] == h["iv_c"] and not h["same_class"]
    assert len(load("trichords")["classes"]) == 12


def test_rows_and_webern():
    r = load("row")
    assert r["distinct"] == 48 and r["answer"] == "B"
    w = r["webern"]
    assert w["inverted"] == w["intervals"] == 45 and w["same_durations"] == w["notes"] == 46 and w["lag_beats"] == 4.0
    a = load("allint")
    assert a["count"] == 3856 and a["tritone_ends"] == 3856 and a["berg_ok"] and a["symmetric"] == 176
    cb = load("combin")
    assert len(cb["hexachords"]) == 6 and all(len(x) == 12 for x in cb["aggregates"])
    op = load("op25")
    assert op["is_row"] and op["ends"] == 6 and op["tetrachords"][1] == [0, 1, 4, 6]
    h = load("hear")
    assert h["answer"] == "B" and h["share_random"] == pytest.approx(1 / 924, abs=0.0006)


def test_variation_29():
    t = load("tune")
    assert sorted(t["row"]) == list(range(12)) and t["row"][:3] == [0, 7, 9]
    v = load("variation")
    row = [r for r in LEDGER if r["part"] == 29][0]
    assert v["part"] == 29 and row["measure"] == v["measure"] and row["seconds"] == pytest.approx(v["seconds"], abs=0.05)


def test_the_part_keeps_the_series_rules():
    check_clips(compute)
    check_scenes_and_clips(compute, SCENES)
    check_windows(compute, SCENES)
    check_ear_thread(compute, SCENES)
