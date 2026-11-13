"""Part 4 of *Music, Built*: what the film says is what was computed, and every sound keeps the series' rules.

    python -m pytest -q tests/music/test_music4.py
"""

import math

import numpy as np
import pytest

from tests.music.partcheck import check_clips, check_ear_thread, check_scenes_and_clips, check_windows
from videos.music.music4 import compute
from videos.music.music4.manifest import SCENES

load = compute.load


def test_the_third_tone_is_made_by_the_ear_not_the_recording():
    d = load("two")
    assert d["third"] == 800.0 and d["in_the_clip_db"] < -120            # two lines, and nothing else
    assert -30 < d["ear_third_db"] < -10 and d["ear_floor_db"] < -80     # an oscillator at the edge adds a line there


def test_outer_and_middle_ear():
    d = load("outer")
    m = d["middle"]
    assert m["pressure_gain"] == pytest.approx(22.3, abs=0.1) and m["gain_db"] == pytest.approx(27.0, abs=0.1)
    assert m["without"] == pytest.approx(0.011, abs=0.001) and 0.2 < m["with"] < 0.35
    assert 3300 < d["canal_hz"] < 3700 and 3000 < d["best_hz"] < 4000    # the ear is best where its canal rings


def test_the_travelling_wave_sorts_by_ratio():
    w = load("wave")
    peaks = [r["peak_mm"] for r in w["rows"]]
    steps = -np.diff(peaks)
    assert np.all(steps > 0) and np.ptp(steps) < 0.05                    # every octave: the same distance
    assert w["mm_per_octave"] == pytest.approx(4.58, abs=0.02)
    assert all(0.5 < r["resonant_mm"] - r["peak_mm"] < 1.6 for r in w["rows"])   # the peak sits just basal of the resonance
    assert w["q_active"] > 1.8 * w["q_passive"] and w["gain_db"] > 10
    # against Greenwood's measured map: within 40 percent in frequency from 500 Hz to 8 kHz
    mid = [r for r in w["rows"] if 500 <= r["hz"] <= 8000]
    assert all(abs(math.log2(r["greenwood_hz"] / r["hz"])) < 0.55 for r in mid)


def test_critical_bands():
    b = load("bands")
    for r in b["widths"]:
        assert r["measured"] == pytest.approx(r["erb"], rel=0.01)          # the gammatone has the published width
    assert [round(r["semitones"], 1) for r in b["widths"]] == [3.6, 2.3, 2.0]
    assert b["erb_1k"] == pytest.approx(132.6, abs=0.1) and 100 < b["fletcher_knee"] < 200
    assert b["fletcher_db"][0] < -8 and abs(b["fletcher_db"][-1]) < 1e-9   # the threshold rises, then stops
    assert b["resolved"] == {"65.4": 5, "130.8": 7, "261.6": 8, "523.3": 8}
    assert 39 < b["bands_to_16k"] < 40


def test_loudness_and_masking():
    d = load("loud")
    rows = {int(r["hz"]): r for r in d["rows"]}
    assert rows[100]["threshold"] > rows[1000]["threshold"] + 15 > rows[3500]["threshold"] + 15
    assert rows[100]["a_db"] == pytest.approx(-19.1, abs=0.2) and abs(rows[1000]["a_db"]) < 0.01
    assert d["equal_pressure_spread_db"] < 0.01                          # the three tones really have one pressure
    assert d["ten_players_sones"] == pytest.approx(2.0) and d["sixteen_times"] == pytest.approx(2.3, abs=0.01)
    m = load("mask")
    assert m["near_threshold"] > m["probe_db"] + 10 and m["far_threshold"] < m["probe_db"] - 20
    assert not m["near_heard"] and m["far_heard"]


def test_the_clock_stops():
    k = load("locking")
    sync = [r["synchrony"] for r in k["rows"]]
    sal = [r["salience"] for r in k["rows"]]
    assert sync == sorted(sync, reverse=True) and sal == sorted(sal, reverse=True)
    assert sync[0] > 0.7 and sync[4] < 0.12 and sal[0] > 0.9 and sal[4] < 0.15
    assert k["erb_1k"] / k["jnd_hz"] > 50
    assert np.ptp(k["hist_4000"]) < 0.4 and np.ptp(k["hist_250"]) > 0.95


def test_the_pitch_that_is_not_there():
    p = load("pitch")
    rows = {r["name"]: r for r in p["rows"]}
    assert all(abs(r["cents"]) < 2 for r in p["rows"])                   # pure, full and missing: one pitch
    assert rows["upper"]["level_at_f0_db"] < -100                        # with nothing at the fundamental
    assert abs(1200 * math.log2(p["with_noise_pitch"] / p["f0"])) < 2    # and noise there does not move it
    assert p["plain_pitch"] == pytest.approx(200.0, abs=0.2)
    assert p["shifted_pitch"] == pytest.approx(p["shifted_formula"], abs=1.0) and 40 < p["shift_cents"] < 50


def test_shepard_dose_and_the_edge():
    assert load("shepard")["same_as_start"] == 0.0
    d = load("dose")
    assert [r["hours"] for r in d["rows"][:5]] == [8.0, 4.0, 2.0, 1.0, 0.25] and d["plug_factor"] == pytest.approx(101.6, abs=0.1)
    a = load("active")
    assert a["slope"] == pytest.approx(1 / 3, abs=1e-6) and a["range_out"] == pytest.approx(33.3, abs=0.1)


def test_variation_4():
    t = load("tune")
    assert t["worst_cents"] < 1.0 and t["loudest_at_f0_db"] < -100
    kinds = [n["kind"] for n in t["notes"]]
    assert kinds.count("missing") == 28 and kinds.count("shepard") == 14
    assert load("variation")["part"] == 4


def test_the_part_keeps_the_series_rules():
    check_clips(compute)
    check_scenes_and_clips(compute, SCENES)
    check_windows(compute, SCENES)
    check_ear_thread(compute, SCENES)
