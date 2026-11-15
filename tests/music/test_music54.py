"""Part 54 of *Music, Built*: what the film says is what was computed, and every sound keeps the series' rules.

    python -m pytest -q tests/music/test_music54.py
"""

import pytest

from tests.music.partcheck import check_clips, check_ear_thread, check_scenes_and_clips, check_windows
from videos.music.music54 import compute
from videos.music.music54.manifest import SCENES
from videos.music.variations import LEDGER

load = compute.load


def test_microphone_claims():
    assert load("hook")["answer"] == "second"
    c = load("capture")
    assert c["cardioid"]["rear_db"] < -25 and c["omni"]["rear_db"] == 0.0
    p = load("proximity")["at100"]
    assert p["1.0"] < 2 and 15 < p["0.05"] < 25
    n = load("noise")
    assert n["ein_dbu"] == pytest.approx(-129.7, abs=0.1) and 10 < n["eq_spl"] < 20
    assert load("hum")["rejection_db"] == pytest.approx(40.0, abs=0.1)


def test_loudspeaker_claims():
    d = load("driver")
    for c in d["checks"]:
        assert c["sim_f3"] == pytest.approx(c["formula_f3"], rel=0.005)
    assert d["b4"]["sim_f3"] == pytest.approx(40.0, abs=0.2) and d["b4"]["sealed_f3"] > 70
    f3 = load("speakers")["f3"]
    assert f3["phone"] > 500 > f3["bookshelf"] > f3["floor"]
    x = load("crossover")
    assert x["lr4"]["at_fc"] == pytest.approx(0.0, abs=1e-6) and x["bw2_inv"]["at_fc"] == pytest.approx(3.01, abs=0.01)


def test_canceller_and_array():
    a = load("anc")["bands"]
    assert a[0]["atten"] < -20 and a[-1]["atten"] > -3
    assert load("beam")["rejection_db"] < -3


def test_variation_54():
    v = load("variation")
    row = [r for r in LEDGER if r["part"] == 54][0]
    assert v["part"] == 54 and row["measure"] == v["measure"] and row["seconds"] == pytest.approx(v["seconds"], abs=0.05)


def test_the_part_keeps_the_series_rules():
    check_clips(compute)
    check_scenes_and_clips(compute, SCENES)
    check_windows(compute, SCENES)
    check_ear_thread(compute, SCENES)
