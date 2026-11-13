"""Part 5 of *Music, Built*: what the film says is what was computed, and every sound keeps the series' rules.

    python -m pytest -q tests/music/test_music5.py
"""

import math

import numpy as np
import pytest

from tests.music.partcheck import check_clips, check_ear_thread, check_scenes_and_clips, check_windows
from videos.music.music5 import compute
from videos.music.music5.manifest import SCENES

load = compute.load


def test_the_cold_open_is_what_it_says():
    d = load("bent")
    assert d["wide"] == 2.1 and d["cents_wide"] == pytest.approx(84.5, abs=0.1)
    assert d["rough_true"] > 10 * d["rough_wide"]                        # in the bent tone the exact octave is the rough one


def test_number_theories_and_their_failure():
    d = load("number")
    rows = {r["name"]: r for r in d["rows"]}
    assert [rows[n]["gradus"] for n in ("octave", "fifth", "fourth", "major third", "minor third", "tritone")] == [2, 4, 5, 7, 8, 14]
    assert rows["major second"]["gradus"] == rows["minor third"]["gradus"] == rows["minor sixth"]["gradus"]   # Euler's quibble
    assert d["pure_gradus"] == 4 and d["wide_gradus"] > 100                # five cents: from 4 to a monster
    assert 2.0 < d["wide_beat"] < 2.6
    assert [rows[n]["repeat"] for n in ("octave", "fifth", "fourth", "major third", "tritone")] == [1, 2, 3, 4, 32]


def test_pulses_and_beats():
    p = load("pulses")
    assert p["end_hz"] == [300.0, 200.0]
    three, two = p["three_t"], p["two_t"]
    assert len(three[three < 1.0]) in (3, 4) and len(two[two < 1.0]) in (2, 3)     # it starts as three against two
    b = load("beats")
    assert b["gaps"] == [1.0, 4.0, 12.0] and b["worked"]["beats"] == 2.0


def test_plomp_and_levelt():
    d = load("plomp")
    assert 0.8 < d["worst_semitones"] < 1.1 and d["worst_time"] < 1.5      # roughest in the first second of the glide
    assert 0.2 < d["worst_over_band"] < 0.4                               # about a quarter of the ear's band
    assert d["pure_fifth"] < 0.01 * d["peak"] and d["pure_tritone"] < 0.03 * d["peak"]   # pure tones know no ratios
    assert d["rough"][-1] < 0.02 and float(np.max(d["rough"])) == pytest.approx(1.0, abs=1e-3)


def test_the_curve_and_its_valleys():
    d = load("curve")
    got = [(m["p"], m["q"]) for m in d["minima"]]
    assert got == [(7, 6), (6, 5), (5, 4), (4, 3), (7, 5), (3, 2), (5, 3), (7, 4), (2, 1)]
    assert max(abs(m["off_cents"]) for m in d["minima"]) < 1.0
    rough = {(m["p"], m["q"]): m["rough"] for m in d["minima"]}
    assert rough[(2, 1)] < rough[(3, 2)] < rough[(4, 3)] < rough[(5, 4)]      # the deepest valleys are the oldest consonances
    w = load("worked")
    assert [(p["lower"], p["upper"]) for p in w["fifth"]["meet"]] == [(3, 2), (6, 4)]
    assert not w["tritone"]["meet"] and w["tritone"]["total"] > 2 * w["fifth"]["total"]
    assert (w["tritone"]["pairs"][0]["lower"], w["tritone"]["pairs"][0]["upper"]) == (3, 2)


def test_the_valleys_move_with_the_timbre():
    d = load("stretched")
    assert d["worst_gap"] < 0.001                                         # each valley at its old ratio ^ log2(2.1)
    assert d["minima"][-1] == pytest.approx(2.1, abs=0.002)
    g = d["grid"]
    assert g["plain_true"] < 0.1 < g["plain_wide"] and g["bent_wide"] < 0.1 < g["bent_true"]


def test_fusion_and_triads():
    f = load("fusion")
    assert abs(f["implied_cents"]) < 2.0                                   # 4:5:6 high up implies middle C
    for r in f["rows"]:
        assert abs(r["off_cents"]) < 20, r["name"]                         # the model finds the fundamental bass
    strengths = [r["strength"] for r in f["rows"][:4]]
    assert strengths == sorted(strengths, reverse=True)
    t = load("triads")
    rows = {r["name"]: r for r in t["rows"]}
    assert t["same_roughness"] < 0.03                                      # roughness cannot tell major from minor
    assert rows["major"]["as_integers"] == [4, 5, 6] and rows["minor"]["as_integers"] == [10, 12, 15]
    assert rows["major"]["octaves_below"] == 2.0 and rows["minor"]["repeat"] == 10
    assert rows["diminished"]["rough"] > rows["augmented"]["rough"] > rows["minor"]["rough"]
    named = {v["name"] for v in t["valleys"] if v["name"]}
    assert {"major", "minor"} <= named
    c = load("culture")
    assert c["rows"]["pythagorean"]["cents"] - c["rows"]["just"]["cents"] == pytest.approx(21.5, abs=0.1) and c["times"] > 1.1


def test_variation_5_and_the_comma():
    t = load("tune")
    assert t["times"] > 3.0 and 745 < t["fifth_cents"] < 755
    kinds = [n["kind"] for n in t["notes"]]
    assert kinds.count("alone") == 14 and kinds.count("bent") == 21 and kinds.count("plain") == 7
    assert load("variation")["part"] == 5
    n = load("nextpart")
    assert n["comma"] == [531441, 524288] and n["cents"] == pytest.approx(23.46, abs=0.01)


def test_the_part_keeps_the_series_rules():
    check_clips(compute)
    check_scenes_and_clips(compute, SCENES)
    check_windows(compute, SCENES)
    check_ear_thread(compute, SCENES)
