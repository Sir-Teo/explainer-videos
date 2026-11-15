"""Part 66 of *Music, Built*: what the film says is what was computed, and every sound keeps the series' rules.

    python -m pytest -q tests/music/test_music66.py
"""

import pytest

from tests.music.partcheck import check_clips, check_ear_thread, check_scenes_and_clips, check_windows
from videos.music.music66 import compute
from videos.music.music66.manifest import SCENES
from videos.music.variations import LEDGER

load = compute.load


def test_samples_and_spectra():
    r = load("rates")
    assert r["snr_mulaw"] > r["snr_linear"] + 10
    a = load("ar")
    assert a["bits_train_curve"][-1] < a["bits_train_curve"][0]
    v = load("vocoder")
    assert v["dist_gl"] < v["dist_mel"]                                  # the bands lose more than the phase does


def test_codec_and_token_model():
    c = load("codec")["rows"]
    assert c["4"]["dist"] <= c["1"]["dist"] and c["phase only"]["dist"] < c["4"]["dist"]
    assert c["1"]["kbps"] == pytest.approx(0.5)
    t = load("tokenlm")
    assert t["steps"] <= 1500 and t["longest_copy_seconds"] < 2.0


def test_diffusion_and_ddsp():
    d = load("diffusion")
    assert d["losses"][-1] < d["losses"][0] and min(d["nearest_db"]) > 0.3        # new profiles, not copies
    s = load("ddsp")
    assert s["dist"] < s["dist_noise"] / 2 and s["losses"][-1] < s["losses"][0]
    assert load("hook")["answer"] == "first"


def test_judges_and_marks():
    f = load("fad")["distances"]
    assert f["another bowed phrase"] < f["white noise"] and f["DDSP"] < f["white noise"]
    w = load("watermark")
    r = w["rows"]["-35"]
    assert r["marked"] > 5 and r["coded"] > 3 and abs(w["clean"]) < 4 and r["other_key"] < 5 and abs(r["other_key_mean"]) < 1.5
    assert r["shifted_search"] > 5 > r["shifted"]


def test_variation_66():
    v = load("variation")
    row = [r for r in LEDGER if r["part"] == 66][0]
    assert v["part"] == 66 and row["measure"] == v["measure"] and row["seconds"] == pytest.approx(v["seconds"], abs=0.05)


def test_the_part_keeps_the_series_rules():
    check_clips(compute)
    check_scenes_and_clips(compute, SCENES)
    check_windows(compute, SCENES)
    check_ear_thread(compute, SCENES)
