"""Part 8 of *Music, Built*: what the film says is what was computed, and every sound keeps the series' rules.

    python -m pytest -q tests/music/test_music8.py
"""

import math

import numpy as np
import pytest

from tests.music.partcheck import check_clips, check_ear_thread, check_scenes_and_clips, check_windows
from videos.music.music8 import compute
from videos.music.music8.manifest import SCENES

load = compute.load


def cents(a, b):
    return 1200 * math.log2(a / b)


def test_two_pipes_of_one_length():
    h = load("hook")
    assert abs(h["interval_cents"] - 1200) < 20                           # an octave apart
    inside = h["clarinet_inside_db"]
    assert inside[1] < -40 and inside[3] < -40 and inside[2] > -15        # in the mouthpiece: odd harmonics only
    assert h["clarinet_db"][1] < -12 and h["flute_db"][1] < -10
    c = load("column")
    assert all(abs(cents(f, n * c["stopped"][0])) < 40 for n, f in zip((1, 3, 5, 7), c["stopped"]))
    assert all(abs(cents(f, n * c["open"][0])) < 15 for n, f in zip((1, 2, 3, 4), c["open"]))
    assert c["stopped"][0] < c["ideal_stopped"] and c["open"][0] < c["ideal_open"]          # the end correction lowers both
    w = c["worked"]
    assert 100 * c["c"] / (2 * w["middle_c"]) == pytest.approx(65.6, abs=0.1) and 100 * w["clarinet_length"] == pytest.approx(58.4, abs=0.1)


def test_the_reed():
    r = load("reed")
    dp, u = np.asarray(r["dp"]), np.asarray(r["flow"])
    assert dp[int(np.argmax(u))] == pytest.approx(1 / 3, abs=0.01)
    assert 1 / 3 < r["threshold"] < 0.40                                  # a third, and a little more for the losses
    rows = r["rows"]
    assert all(x["amp"] < 1e-3 for x in rows if x["gamma"] < 0.33)
    speaking = [x for x in rows if x["amp"] > 0.05]
    assert all(b["amp"] > a["amp"] for a, b in zip(speaking, speaking[1:]))        # louder all the way
    assert speaking[0]["fifth_db"] < speaking[5]["fifth_db"] - 8          # and brighter at first
    h = r["harmonics_db"]
    assert h[1] < -40 and abs(h[2] - (-9.5)) < 3 and abs(h[4] - (-14)) < 5       # nearly a square wave
    assert 0.5 < r["speaks_at"] < 3.0 and r["speaks_gamma"] > r["threshold"]


def test_holes_and_registers():
    o = load("holes")
    flat = [x["cents_below_cut"] for x in o["rows"]]
    assert 0 < flat[0] < flat[1] < flat[2] and flat[0] < 50 and flat[2] > 150      # the smaller the hole, the flatter
    assert abs(o["interval_cents"] - o["twelfth_cents"]) < 80 and o["ratio"] == pytest.approx(3, abs=0.15)
    assert o["peaks_register"][0] > 1.5 * o["peaks_plain"][0] and abs(cents(o["peaks_register"][1], o["peaks_plain"][1])) < 60
    j = load("jet")
    regs = [x["register"] for x in j["rows"]]
    assert regs == sorted(regs) and regs[0] == 1 and 2 in regs and regs[-1] == 3          # fundamental, octave, twelfth
    assert abs(j["quiz"]["flute_cents"] - 1200) < 20 and j["quiz_answer"] == "B"
    track = [x for x in j["track"] if x["hz"] > 0]
    before = [x["hz"] for x in track if x["t"] < j["jump_t"]]
    assert max(before) > before[2] * 1.01 and track[-1]["hz"] == pytest.approx(2 * j["hz"], rel=0.02)   # creeps sharp, then the octave
    assert j["jump_pressure"] > j["first_octave_pressure"]                # hysteresis: it holds on longer than it would start
    assert [s["harmonic"] for s in j["stops"]] == [1, 2, 3, 4, 5]


def test_cones_and_brass():
    k = load("cone")
    assert abs(k["ratios_cyl"][1] - 3) < 0.1 and abs(k["ratios_cone"][1] - 2) < 0.03 and abs(k["ratios_cone"][2] - 3) < 0.06
    assert abs(k["ratios_bare"][2] - 3) > abs(k["ratios_cone"][2] - 3)    # the mouthpiece mends the truncated cone
    assert k["quiz_answer"] == "B" and k["quiz_db"]["B"][1] < -15 < -3 < k["quiz_db"]["A"][1]
    assert k["cone_length"] > 1.5 * k["cyl_length"]
    l = load("lips")
    assert 114 < l["f0"] < 119 and max(abs(c) for c in l["off_cents"]) < 40 and l["pedal"] < 0.75 * l["f0"]
    assert abs(l["plain_peaks"][1] / l["plain_peaks"][0] - 3) < 0.1
    assert all(abs(cents(h, t)) < 40 for h, t in zip(l["heard"], l["targets"]))             # the call lands on the resonances
    stairs = [s for s in l["stairs"] if s["amp"] > 0.3 and s["hz"] > 150]
    assert all(s["hz"] > s["lip"] for s in stairs)                        # lips sound above their own frequency
    assert any(s["amp"] > 0.3 and abs(cents(s["hz"], l["f0"])) < 60 for s in l["stairs"])   # and the pedal appears unasked
    v = l["valves"]
    assert v["sharp_cents"] == pytest.approx(30.3, abs=0.2) and v["have_13"] < v["need_13"]


def test_the_voice():
    v = load("voice")
    assert -15 < v["source_slope"] < -10                                  # about 12 dB an octave
    out = np.asarray(v["out_a"])
    assert abs((int(np.argmax(out)) + 1) * v["hz"] - 730) <= v["hz"]      # the strongest harmonic of 'ah' is at its first formant
    w = load("vowels")
    n = w["shapes"]["neutral"]["formants"]
    assert n[1] / n[0] == pytest.approx(3, abs=0.05) and w["quarter"][0] == pytest.approx(490, abs=1)
    for name in ("a", "i"):
        assert all(abs(cents(x, y)) < 100 for x, y in zip(w["shapes"][name]["formants"], w["measured"][name]))
    assert w["order"] == ["u", "a", "i"] and len(w["chart"]) == 10
    s = load("singers")
    assert 12 < s["boost_db"] < 25 and s["soprano"]["gain_db"] > 20
    assert s["prominence_db"] > 15 and s["harmonics"] == [8, 8, 12, 12, 13, 13, 12]
    assert s["off_cents"]["4"] == pytest.approx(53.3, abs=0.1) and s["off_cents"]["6"] == pytest.approx(-43.8, abs=0.1)


def test_variation_8():
    t = load("tune")
    assert t["plan"][:5] == [["flute"], ["clarinet"], ["saxophone"], ["trumpet"], ["voice"]] and len(t["plan"][5]) == 5
    assert t["worst_cents"] < 10 and all(n["voices"] == t["plan"][n["phrase"]] for n in t["notes"])
    assert load("variation")["part"] == 8


def test_the_part_keeps_the_series_rules():
    check_clips(compute)
    check_scenes_and_clips(compute, SCENES)
    check_windows(compute, SCENES)
    check_ear_thread(compute, SCENES)
