"""Part 48 of *Music, Built*: what the film says is what was computed, and every sound keeps the series' rules.

    python -m pytest -q tests/music/test_music48.py
"""

import pytest

from tests.music.partcheck import check_clips, check_ear_thread, check_scenes_and_clips, check_windows
from videos.music.music48 import compute
from videos.music.music48.manifest import SCENES
from videos.music.variations import LEDGER

load = compute.load


def test_rate_and_hook():
    r = load("rate44")
    assert r["ntsc"]["rate"] == r["pal"]["rate"] == 44100
    h = load("hook")
    assert h["residue_db"]["16 bits"] < h["residue_db"]["one bit"] < h["signal_db"] - 50


def test_sampling_and_aliasing():
    s = load("sampling")
    e = s["taps_error"]
    assert e["128"] < e["32"] < e["8"] < e["4"]
    assert load("tones")["heard"] == [3000, 3000, 1000]
    st = load("stairstep")
    assert st["droop"]["20000"] == pytest.approx(-3.17, abs=0.05)


def test_quantization_and_dither():
    q = load("quant")
    for r in q["rows"]:
        if r["bits"] >= 5:
            assert r["measured"] == pytest.approx(r["theory"], abs=0.7)
    assert load("lowsine")["nonzero_none"] == 0
    sh = load("shaping")
    assert sh["2"]["below4k_db"] < sh["1"]["below4k_db"] < sh["0"]["below4k_db"] and sh["2"]["total_db"] > sh["0"]["total_db"]


def test_one_bit_and_jitter():
    d = load("deltasigma")["rows"]
    assert d["2"][3]["snr"] > 70 and d["1"][3]["snr"] < d["2"][3]["snr"]
    for r in load("jitter")["rows"]:
        assert r["measured"] == pytest.approx(r["theory"], abs=0.5)
    s = load("sidebands")
    assert s["measured"] == pytest.approx(s["predicted"], abs=1.0)
    sp = load("speeds")["snr"]
    assert sp["64"] > sp["8"] + 30


def test_variation_48():
    v = load("variation")
    row = [r for r in LEDGER if r["part"] == 48][0]
    assert v["part"] == 48 and row["measure"] == v["measure"] and row["seconds"] == pytest.approx(v["seconds"], abs=0.05)


def test_the_part_keeps_the_series_rules():
    check_clips(compute)
    check_scenes_and_clips(compute, SCENES)
    check_windows(compute, SCENES)
    check_ear_thread(compute, SCENES)
