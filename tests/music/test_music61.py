"""Part 61 of *Music, Built*: what the film says is what was computed, and every sound keeps the series' rules.

    python -m pytest -q tests/music/test_music61.py
"""

import pytest

from tests.music.partcheck import check_clips, check_ear_thread, check_scenes_and_clips, check_windows
from videos.music.music61 import compute
from videos.music.music61.manifest import SCENES
from videos.music.variations import LEDGER

load = compute.load


def test_pitch_and_onsets():
    p = load("pitch")
    rows = {r["snr"]: r for r in p["rows"]}
    assert rows[20]["yin"] < 0.05 and rows[-10]["yin"] > 0.5                         # clean, then lost
    assert abs(p["missing_f0"] - 220) < 2                                            # the missing fundamental is found
    assert abs(p["bias_yin"]) < abs(p["bias_acf"])
    o = load("onsets")
    assert o["piano"]["f"] > o["strings"]["f"]
    assert load("pitchheard")["voiced_share"] > 0.9


def test_polyphony_transcribers():
    c = load("chords")
    assert c["answer"] == "no" and 48 in c["triad"]["nmf"] and set(c["triad"]["net"]) == {60, 64, 67}
    n, w = load("nmf")["scores"], load("net")["scores"]
    assert w["piano"]["f"] > n["piano"]["f"]                                         # learning helps, on its instrument
    assert w["harp"]["f"] < w["piano"]["f"] - 0.2                                    # and not on a timbre never heard
    poly = load("polyphony")
    assert poly["net"][0] > poly["net"][-1] and poly["nmf"][0] > poly["nmf"][-1]
    assert all(a > b for a, b in zip(poly["net"], poly["nmf"]))
    nh = load("nmfheard")
    assert nh["n_est"] > nh["n_true"] and nh["scores"]["recall"] >= 0.8


def test_scoring_and_quantization():
    s = load("scoreheard")
    assert abs(s["a"]["f"] - s["b"]["f"]) < 0.02 and s["a"]["precision"] == 1.0
    q = load("score")
    assert q["track"]["ok"] == len(q["true_beats"]) and q["fixed"]["ok"] < len(q["true_beats"]) // 2
    assert q["key"][0] == "C major"
    t = load("tune61")["rounds"]
    assert t[1]["vs_original"] > t[-1]["vs_original"]


def test_variation_61():
    v = load("variation")
    row = [r for r in LEDGER if r["part"] == 61][0]
    assert v["part"] == 61 and row["measure"] == v["measure"] and row["seconds"] == pytest.approx(v["seconds"], abs=0.05)


def test_the_part_keeps_the_series_rules():
    check_clips(compute)
    check_scenes_and_clips(compute, SCENES)
    check_windows(compute, SCENES)
    check_ear_thread(compute, SCENES)
