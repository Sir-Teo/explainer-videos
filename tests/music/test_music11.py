"""Part 11 of *Music, Built*: what the film says is what was computed, and every sound keeps the series' rules.

    python -m pytest -q tests/music/test_music11.py
"""

import numpy as np
import pytest

from tests.music.partcheck import check_clips, check_ear_thread, check_scenes_and_clips, check_windows
from videos.music.music11 import compute
from videos.music.music11.manifest import SCENES

load = compute.load


def test_identical_clicks_and_the_window_of_the_beat():
    h = load("hook")
    assert h["count"] == 16 and h["spread_db"] == pytest.approx(0.0, abs=1e-6)          # the tick and the tock are not in the sound
    t = load("tempo")
    rate = 1.0 / np.diff(np.asarray(t["times"]))
    assert rate[0] < 0.5 and rate[-1] > 45 and (np.diff(rate) > 0).all()
    z = t["zones"]
    assert 0 < z["pulse"] < z["fast"] < z["tone"] < z["end"]
    assert t["bpm_b"] / t["bpm_a"] == pytest.approx(1.05) and t["quiz_answer"] == "B"


def test_metre_and_the_pulse_finder():
    m = load("meter")
    assert m["four"] == [5, 1, 2, 1, 3, 1, 2, 1, 4, 1, 2, 1, 3, 1, 2, 1] and m["three_four"] == [3, 1, 2, 1, 2, 1] and m["six_eight"] == [3, 1, 1, 2, 1, 1]
    assert m["period"] == pytest.approx(m["true_beat"], rel=0.01) and m["bpm"] == pytest.approx(109, abs=1.5) and abs(m["phase"]) < 0.011
    taps, notes = np.asarray(m["taps"]), np.asarray(m["notes"])
    assert all(np.abs(taps - n).min() < 0.03 for n in notes)                             # every note of the Tune falls on a tap
    d = load("divide")["ms"]
    assert round(d["quarter"]) == 550 and round(d["eighth"]) == 275 and round(d["triplet"]) == 183 and round(d["sixteenth"]) == 138
    assert load("divide")["pause"]["triplet_ms"] == pytest.approx(166.7, abs=0.1)


def test_syncopation():
    s = load("sync")
    assert [p["index"] for p in s["patterns"]] == [0, 4, 6, 7]
    assert s["patterns"][1]["pattern"] == "x..x..x...x.x..." and s["weights"][3] == 1 and s["weights"][4] == 3 and s["weights"][6] == 2 and s["weights"][8] == 4
    assert s["quiz_index"] == {"A": 2, "B": 5} and s["quiz_answer"] == "B"
    assert load("accent")["answers"]["A"].startswith("the loud") and load("accent")["answers"]["B"].startswith("the long")
    ft, fb = np.asarray(s["flip_times"]), np.asarray(s["flip_beats"])
    assert np.allclose(np.diff(ft), 0.5) and all(np.abs(ft - b).min() == pytest.approx(0.25) for b in fb)      # the drum falls exactly between the strokes


def test_threes_and_twos():
    h = load("hemiola")
    assert h["p32"]["gaps"] == [2, 1, 1, 2] and h["p32"]["grid"] == 6 and h["p43"]["gaps"] == [3, 1, 2, 2, 1, 3] and h["p43"]["grid"] == 12
    assert h["canon_meets"][0] == 5 and h["canon_meets"][2] == 1 and h["canon_meets"][8] == 0 and h["canon_shifts"] == [0, 2, 8]
    a = load("additive")
    assert a["sevens"] == [[2, 2, 3], [2, 3, 2], [3, 2, 2]]
    assert [a["counts"][str(n)] for n in (5, 7, 8, 9, 11, 12)] == [2, 3, 4, 5, 9, 12]
    assert [2, 2, 2, 3] in a["nines"] and len(a["nines"]) == 5


def test_swing_is_a_short_note():
    w = load("swing")
    assert [round(x) for x in w["long_ms"]] == [250, 333, 375] and [round(x) for x in w["short_ms"]] == [250, 167, 125]
    assert w["triplet_bpm"] == pytest.approx(200) and w["straight_bpm"] == pytest.approx(300)
    bpm, ratio = np.asarray(w["bpm"]), np.asarray(w["ratio"])
    assert ratio.max() == 3.5 and ratio.min() == 1.0 and (np.diff(ratio) <= 1e-12).all()
    assert float(np.interp(200.0, bpm, ratio)) == pytest.approx(2.0, abs=0.02)


def test_a_rhythm_becomes_a_fifth():
    c = load("continuum")
    assert c["f2"] == pytest.approx(200.0, abs=0.5) and c["f3"] == pytest.approx(300.0, abs=0.5) and c["cents"] == pytest.approx(702, abs=3)
    two, three = np.asarray(c["two"]), np.asarray(c["three"])
    k = int(np.searchsorted(two, 12.0))
    assert len(three) / len(two) == pytest.approx(1.5, rel=0.01)                         # three strokes for every two, the whole way
    assert 0 < c["t20"] < c["ramp"] and np.diff(two)[k] < np.diff(two)[0]
    ha, hb = c["timbre_harmonics"]["A"], c["timbre_harmonics"]["B"]
    assert np.allclose(ha, 1.0) and min(hb) < 0.2 and max(hb) == pytest.approx(1.0) and c["timbre_hz"] == 110.0      # one pitch, two spectra


def test_the_telephone_game():
    f = load("frontier")
    assert f["near"][5] < 0.6 * f["near"][0] and f["share_a"] > 0.85 and f["share_b"] > 0.85 and f["cross"] < 0.5
    assert f["chain_end"] == [2, 1, 1]
    end = np.asarray(f["chain_end_ms"])
    assert np.allclose(end / end.sum(), [0.5, 0.25, 0.25], atol=0.03) and not np.allclose(np.asarray(f["chain_start_ms"]) / end.sum(), [0.5, 0.25, 0.25], atol=0.06)


def test_variation_11():
    t = load("tune")
    assert t["signatures"] == ["4/4", "3/4", "5/4", "7/8", "4/4, swung", "6/8 and 3/4"] and t["bar_pulses"] == [4, 3, 5, 7, 8, 6]
    c = compute.CLIPS.load("tune.variation11")
    assert len(c.notes) == 42 and [n["phrase"] for n in c.notes] == [k // 7 for k in range(42)]
    assert all(b["t"] > a["t"] for a, b in zip(c.notes, c.notes[1:]))
    hz = [round(n["hz"], 1) for n in c.notes]
    from explainer.music.monochord import tune as T
    assert hz == [round(compute.C4 * float(e["ratio"]), 1) for e in T.events(0.55)]      # not one pitch was changed
    v = load("variation")
    assert v["part"] == 11 and "4, 3, 5 and 7" in v["measure"]


def test_the_part_keeps_the_series_rules():
    check_clips(compute)
    check_scenes_and_clips(compute, SCENES)
    check_windows(compute, SCENES)
    check_ear_thread(compute, SCENES)
