"""Part 58 of *Music, Built*: what the film says is what was computed, and every sound keeps the series' rules.

    python -m pytest -q tests/music/test_music58.py
"""

import pytest

from tests.music.partcheck import check_clips, check_ear_thread, check_scenes_and_clips, check_windows
from videos.music.music58 import compute
from videos.music.music58.manifest import SCENES
from videos.music.variations import LEDGER

load = compute.load


def test_hook_and_rates():
    h = load("hook")
    assert h["answer"] == "second" and h["c64"]["margin"] > 10 and h["c16"]["margin"] < -10
    r = load("rates")
    for name in ("voice", "mix"):
        m = [row["margin"] for row in r[name]]
        assert all(a > b for a, b in zip(m, m[1:]))
        assert all(abs(row["kbps"] - row["target"]) / row["target"] < 0.1 for row in r[name])


def test_lossless_and_mdct():
    l = load("lossless")["signals"]
    assert l["voice"]["exact"] and l["mix"]["exact"] and l["mix"]["ratio"] < 0.7
    assert load("mdct")["max_err_mix"] < 1e-10


def test_masking_preecho_stereo():
    m = load("masking")
    assert m["answer"] == "first" and m["noise_snr_db"] < 15
    p = load("preecho")
    assert p["pre_long"] > p["pre_short"] and p["kbps"]["short"] > 2 * p["kbps"]["long"]
    s = load("stereo")
    assert s["ms"]["snr_l"] > s["lr"]["snr_l"] + 2 and s["ms"]["snr_r"] > s["lr"]["snr_r"] + 2


def test_tests_generations_rvq():
    a = load("abx")
    assert a["threshold"]["16"] == 12 and a["answer"] == "B"
    g = load("transcode")["gens"]
    assert g[0]["snr"] > g[-1]["snr"] + 3
    rows = load("rvq")["rows"]
    assert all(a["vec_err_db"] > b["vec_err_db"] for a, b in zip(rows, rows[1:]))


def test_variation_58():
    v = load("variation")
    row = [r for r in LEDGER if r["part"] == 58][0]
    assert v["part"] == 58 and row["measure"] == v["measure"] and row["seconds"] == pytest.approx(v["seconds"], abs=0.05)


def test_the_part_keeps_the_series_rules():
    check_clips(compute)
    check_scenes_and_clips(compute, SCENES)
    check_windows(compute, SCENES)
    check_ear_thread(compute, SCENES)
