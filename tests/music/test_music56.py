"""Part 56 of *Music, Built*: what the film says is what was computed, and every sound keeps the series' rules.

    python -m pytest -q tests/music/test_music56.py
"""

import pytest

from tests.music.partcheck import check_clips, check_ear_thread, check_scenes_and_clips, check_windows
from videos.music.music56 import compute
from videos.music.music56.manifest import SCENES
from videos.music.variations import LEDGER

load = compute.load


def test_hook_and_variation_claims():
    h = load("hook")
    assert h["answer"] == "second" and h["order"][1] == "dub"
    me = h["measures"]
    assert me["wall"]["crest_db"] < me["dry"]["crest_db"] - 4 and me["dub"]["correlation"] > me["wall"]["correlation"]
    t = load("tune56")["measures"]
    assert t["wall"]["crest_db"] < 12 < t["dry"]["crest_db"]


def test_recording_claims():
    a = load("arrays")
    assert a["pairs"]["Blumlein"]["sra"] < a["pairs"]["AB"]["sra"] < a["pairs"]["ORTF"]["sra"] < a["pairs"]["XY"]["sra"]
    assert a["stage_pos"]["AB"]["piano"] == 1.0 and a["stage_pos"]["XY"]["piano"] < 0.5
    p = load("phase")
    assert p["tau_ms"] == pytest.approx(5.83, abs=0.01) and p["notch_hz"] == pytest.approx(85.75, abs=0.1) and p["low_loss_db"] > 4
    g = load("gain")["rows"]
    assert g["right"]["headroom_db"] > 10 and g["hot"]["clips"] and not g["low"]["clips"] and g["low"]["snr_db"] < g["right"]["snr_db"] - 15
    assert load("edit")["jump"] > 0.3


def test_mixing_claims():
    pn = load("pan")["laws"]
    assert pn["-3.0"]["centre_stereo_db"] == pytest.approx(0.0, abs=0.01) and pn["-6.0"]["centre_mono_db"] == pytest.approx(0.0, abs=0.01)
    assert pn["-3.0"]["centre_mono_db"] == pytest.approx(3.01, abs=0.01)
    m = load("masking")["overall"]
    for k in ("vox", "piano", "guitar", "bass"):
        assert m["carved"][k] < m["rough"][k]
    d = load("dynamics")
    assert d["vox"]["spread_after"] < d["vox"]["spread_before"] - 5 and d["drums"]["spread_parallel"] < d["drums"]["spread_dry"] - 3
    dp = load("depth")
    assert dp["dr_db"]["near"] > dp["dr_db"]["middle"] > dp["dr_db"]["far"] and dp["width"]["correlation"] < 0.2
    assert 0.2 < load("monitor")["bass_above_844"] < 0.4
    am = load("automix")
    assert am["answer"] == "second" and am["machine"]["hat"][0] > 5 and am["masked"]["machine"]["bass"] > am["masked"]["hand"]["bass"]


def test_variation_56():
    v = load("variation")
    row = [r for r in LEDGER if r["part"] == 56][0]
    assert v["part"] == 56 and row["measure"] == v["measure"] and row["seconds"] == pytest.approx(v["seconds"], abs=0.05)


def test_the_part_keeps_the_series_rules():
    check_clips(compute)
    check_scenes_and_clips(compute, SCENES)
    check_windows(compute, SCENES)
    check_ear_thread(compute, SCENES)
