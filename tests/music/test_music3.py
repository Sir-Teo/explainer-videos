"""Part 3 of *Music, Built*: what the film says is what was computed, and every sound keeps the series' rules.

    python -m pytest -q tests/music/test_music3.py
"""

import math

import numpy as np
import pytest

from tests.music.partcheck import check_clips, check_ear_thread, check_scenes_and_clips, check_windows
from videos.music.music3 import compute
from videos.music.music3.manifest import SCENES

load = compute.load


def test_fouriers_recipe_and_gibbs():
    s = load("square")
    assert s["proj_worst"] < 1e-6 and abs(s["proj"][1]) < 1e-9 and s["proj"][0] == pytest.approx(4 / math.pi)
    assert [round(100 * g["overshoot"], 1) for g in s["gibbs"][1:]] == [8.9, 8.9]
    assert s["rms"] == sorted(s["rms"], reverse=True)                  # the average gap only shrinks
    assert s["sine_residual"] < 1e-9                                   # a sine through a resonator is still a sine
    assert np.abs(s["sq_out"] - s["sq_in"]).max() > 0.3                # a square is not


def test_the_machine():
    d = load("dft")
    assert d["err"] < 1e-12 and d["mults_4096"] == 2048 * 12
    assert d["timing"][-1]["slow_ms"] > 50 * d["timing"][-1]["fast_ms"]
    assert all(abs(p - 130.81 * (k + 1)) < 3 for k, p in enumerate(d["peaks"]))
    assert d["worked"]["seconds"] == pytest.approx(0.153, abs=0.002)


def test_ohm_and_phase():
    o = load("ohm")
    assert o["worst_db"] < 1.5 and o["strong"] >= 6
    p = load("phase")
    assert p["low"]["spectrum_gap_db"] < 1.0 and p["high"]["spectrum_gap_db"] < 0.2
    assert p["low"]["crest_a"] > 1.8 * p["low"]["crest_b"]             # same amounts, a very different wave


def test_spectrogram_windows_and_gabor():
    assert load("stft")["scipy_gap"] < 1e-10
    w = {r["name"]: r for r in load("windows")["rows"]}
    assert round(w["rect"]["side"]) == -13 and round(w["hann"]["side"]) == -31 and round(w["blackman"]["side"]) == -58
    ww = load("windows")
    assert ww["rect_floor_near_weak"] > ww["weak_db"] + 10             # the weak tone is under the spill without a window
    g = load("gabor")
    assert g["rows"][0]["times_floor"] == pytest.approx(1.0, abs=1e-3) and all(r["times_floor"] >= 0.999 for r in g["rows"])
    assert [b["semitones"] for b in g["bursts"]] == sorted(b["semitones"] for b in g["bursts"])
    assert g["bursts"][-1]["semitones"] > 11 and g["bursts"][0]["semitones"] < 0.3


def test_constant_q_noise_and_timbre():
    q = load("cq")
    assert q["notes_in_their_bin"] == q["notes"] and q["q"] == pytest.approx(34.1, abs=0.1)
    for r in load("noise")["rows"]:
        assert r["slope"] == pytest.approx(r["want"], abs=0.25)
    assert load("noise")["one_scatter_db"] > 3.0
    t = load("timbre")
    assert t["spectrum_gap"] < 1e-12
    rows = {r["name"]: r for r in t["rows"]}
    assert rows["forwards"]["attack_ms"] < 20 < rows["attack removed"]["attack_ms"] < rows["backwards"]["attack_ms"]
    assert t["centroid"][0] > 1.5 * t["centroid"][-1]                  # a pluck starts bright and ends dull


def test_frontier_variation_and_the_missing_fundamental():
    r = load("reassign")
    assert r["ratio"] > 2.0
    t = load("tune")
    assert t["seen"][:5] == [1, 2, 3, 5, 8] and t["seen"][5] >= 12
    assert [row["brightness"] for row in t["rows"]] == sorted(row["brightness"] for row in t["rows"])
    assert load("variation")["part"] == 3
    assert load("missing")["level_at_f0_db"] < -100


def test_the_part_keeps_the_series_rules():
    check_clips(compute, floor=-30.0)           # the 5 ms tone bursts are set by their peaks: their loudness is low
    check_scenes_and_clips(compute, SCENES)
    check_windows(compute, SCENES)
    check_ear_thread(compute, SCENES)
