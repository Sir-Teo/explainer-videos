"""Part 7 of *Music, Built*: what the film says is what was computed, and every sound keeps the series' rules.

    python -m pytest -q tests/music/test_music7.py
"""

import math

import numpy as np
import pytest

from tests.music.partcheck import check_clips, check_ear_thread, check_scenes_and_clips, check_windows
from videos.music.music7 import compute
from videos.music.music7.manifest import SCENES

load = compute.load


def test_a_body_is_a_filter_and_a_guitar_is_a_plate_on_a_bottle():
    b = load("body")
    f, r = np.asarray(b["f"]), np.asarray(b["response"])
    assert r.max() - r.min() > 20                                        # peaks and valleys, not a flat gain
    t = load("twomass")
    assert t["lower"] < t["helmholtz"] < t["plate"] < t["upper"]         # coupling pushes the two apart
    assert t["lower"] ** 2 + t["upper"] ** 2 == pytest.approx(t["helmholtz"] ** 2 + t["plate"] ** 2, rel=1e-6)
    assert t["lower"] == pytest.approx(98, abs=1) and t["upper"] == pytest.approx(204, abs=1)
    assert t["lower"] < t["dip"] < t["upper"] and t["low_e"] < t["lower"]


def test_karplus_and_strong():
    k = load("ks")
    assert k["delay"] == 244 and k["true_hz"] == pytest.approx(48_000 / 244.5, abs=0.01)
    assert k["off_cents"] == pytest.approx(2.8, abs=0.1)
    laps = np.asarray(k["laps"])
    rough = [float(np.abs(np.diff(lap)).mean()) for lap in laps]         # each lap round the loop is smoother than the last
    assert all(b < a for a, b in zip(rough, rough[1:]))


def test_the_hammer():
    h = load("hammer")
    rows = {r["name"]: r for r in h["rows"]}
    assert rows["soft"]["contact_ms"] > rows["medium"]["contact_ms"] > rows["hard"]["contact_ms"] > 1.5
    assert rows["soft"]["contact_ms"] == pytest.approx(2.5, abs=0.1) and rows["hard"]["contact_ms"] == pytest.approx(1.9, abs=0.1)
    assert rows["soft"]["centroid"] < rows["medium"]["centroid"] < rows["hard"]["centroid"]
    assert h["speed_ratio"] == 8 and h["force_ratio"] > 10                # felt stiffens: the force grows faster than the speed
    lv = np.asarray(h["levels_medium"])
    assert h["weak_partial"] == 8 and lv[7] < lv[6] - 10                  # struck near 1/8: the 8th partial is far below the 7th
    assert 20 * math.log10(abs(math.sin(8 * math.pi * h["hammer"]["at"]))) == pytest.approx(-18, abs=0.5)
    assert h["quiz_answer"] == "A"


def test_stiffness_and_unisons():
    s = load("stiff")
    n, c = np.asarray(s["n"]), np.asarray(s["cents"])
    b = s["B"]
    assert b == pytest.approx(3.8e-4, rel=0.02)
    assert np.allclose(c, 1200 * np.log2(np.sqrt((1 + b * n ** 2) / (1 + b))), atol=0.05)
    assert c[9] == pytest.approx(32, abs=0.5) and s["seventh_cents"] == pytest.approx(15.7, abs=0.2) and s["sixteenth_cents"] == pytest.approx(80, abs=1)
    assert s["quiz_answer"] == "B"
    u = load("unison")
    rows = {r["name"]: r for r in u["rows"]}
    assert rows["unison"]["at_1s"] < rows["one"]["at_1s"] - 10            # a perfect pair dies about twice as fast
    assert rows["apart"]["at_5s"] > rows["one"]["at_5s"] + 25 > rows["unison"]["at_5s"] + 25      # a cent apart: by far the longest
    assert u["early_db_s"] < -25 and -5 < u["late_db_s"] < -1             # two stages


def test_the_bow():
    b = load("bow")
    assert b["regime"]["kind"] == "Helmholtz" and b["regime"]["slip_fraction"] == pytest.approx(b["beta"], abs=0.01)
    assert b["flyback"] == pytest.approx(b["expected_flyback"], rel=0.06)
    h, saw = np.asarray(b["harmonics_db"]), np.asarray(b["sawtooth_db"])
    assert np.abs(h[:8] - saw[:8]).max() < 0.25                           # a sawtooth: partials as 1/n
    assert h[9] < -40                                                     # and none at a node under the bow
    s = load("schelleng")
    assert -1.4 < s["slope_max"] < -0.8 and -3.0 < s["slope_min"] < -1.8  # Schelleng: -1 and -2
    assert all(0.55 < r < 1.6 for r in s["max_ratio"]) and all(1.0 < r < 7 for r in s["min_ratio"])
    assert all(r["min"] < r["max"] for r in s["rows"])
    kinds = {k: v["kind"] for k, v in s["regimes"].items()}
    assert kinds == {"light": "multiple slips", "right": "Helmholtz", "heavy": "raucous"} and s["order"] == ["heavy", "right", "light"]
    assert s["regimes"]["heavy"]["pitch_ratio"] < 0.95 and s["regimes"]["light"]["slips_per_period"] >= 2
    row = s["rows"][3]
    assert row["min"] < s["forces"]["right"] < row["max"] < s["forces"]["heavy"] and s["forces"]["light"] < row["min"]


def test_the_violin_and_variation_7():
    v = load("violin")
    assert v["modes"] == {"A0": 275.0, "B1-": 460.0, "B1+": 540.0, "hill": 2500.0}
    f, db = np.asarray(v["f"]), np.asarray(v["db"])
    at = lambda hz: float(np.interp(math.log(hz), np.log(f), db))        # noqa: E731
    assert at(275) > at(196) + 15 and at(275) > at(350) + 8               # the air resonance stands clear; the open G is below it all
    assert v["largest_swing"] == pytest.approx(7, abs=0.5) and min(v["swing_db"]) < -5 < 5 < max(v["swing_db"])
    t = load("tune")
    assert t["plan"] == [["plucked"], ["struck"], ["bowed"], ["plucked", "bowed"], ["struck", "bowed"], ["plucked", "struck", "bowed"]]
    assert all(n["voices"] == t["plan"][n["phrase"]] for n in t["notes"])
    assert load("variation")["part"] == 7


def test_the_part_keeps_the_series_rules():
    check_clips(compute)
    check_scenes_and_clips(compute, SCENES)
    check_windows(compute, SCENES)
    check_ear_thread(compute, SCENES)
