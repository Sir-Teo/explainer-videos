"""Part 28 of *Music, Built*: what the film says is what was computed, and every sound keeps the series' rules.

    python -m pytest -q tests/music/test_music28.py
"""

import pytest

from tests.music.partcheck import check_clips, check_ear_thread, check_scenes_and_clips, check_windows
from videos.music.music28 import compute
from videos.music.music28.manifest import SCENES
from videos.music.variations import LEDGER

load = compute.load


def test_scales():
    w = load("wholetone")
    assert w["periods"] == {"major": 12, "whole": 2}
    assert [n[0] for n in w["whole"]] == [72, 72, 80, 80, 82, 82, 80]
    c = load("census")
    assert c["classes"] == 352 and c["n_symmetric"] == 15 and c["all_union"]
    assert sorted(s["mode"] for s in c["symmetric"] if s["mode"]) == list(range(1, 8))
    assert all(len(s["pcs"]) <= 6 for s in c["symmetric"] if not s["mode"])
    s = load("slendro")
    assert s["diff"] == [0, 40, 80, 20, 60]
    assert load("triads")["inside"]


def test_octatonic_chance_and_polychord():
    o = load("octatonic")
    assert o["petrushka_fits"]
    ch = o["chance"]
    assert ch["octatonic"][1] == pytest.approx(0.418, abs=0.001) and ch["diatonic"][1] == pytest.approx(0.485, abs=0.001)
    assert ch["octatonic"][4] == pytest.approx(0.030, abs=0.001) and ch["diatonic"][4] == pytest.approx(0.015, abs=0.001)
    f = load("polychord")["fit"]
    assert f["melody"]["key"] == [0, "major"] and f["chords"]["key"] == [6, "major"]
    assert f["both"]["r"] < min(f["melody"]["r"], f["chords"]["r"])


def test_rhythm_and_proportion():
    a = load("accents")
    assert a["answer"] == "A" and a["off"]["regular"] == 0.0 and a["off"]["displaced"] == pytest.approx(0.875)
    b = load("bartok")
    assert b["counts"]["7"] == 3 and b["counts"]["12"] == 12
    g = b["golden"]
    assert g["p1"] == pytest.approx(4 / 88) and g["p10_2"] > 0.6
    m = load("messiaen")
    assert m["rhythm"] == m["rhythm"][::-1] and m["palindromes"]["16"] == 193 and m["all"]["16"] == 20569
    assert load("blocks")["lcm"] == 60
    assert load("planing")["answer"] == "A"


def test_variation_28():
    t = load("tune")
    assert t["notes"]["planed_chords"] == 14 and t["notes"]["ostinato"] == 32
    v = load("variation")
    row = [r for r in LEDGER if r["part"] == 28][0]
    assert v["part"] == 28 and row["measure"] == v["measure"] and row["seconds"] == pytest.approx(v["seconds"], abs=0.05)


def test_the_part_keeps_the_series_rules():
    check_clips(compute)
    check_scenes_and_clips(compute, SCENES)
    check_windows(compute, SCENES)
    check_ear_thread(compute, SCENES)
