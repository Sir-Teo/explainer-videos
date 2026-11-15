"""Part 63 of *Music, Built*: what the film says is what was computed, and every sound keeps the series' rules.

    python -m pytest -q tests/music/test_music63.py
"""

import pytest

from tests.music.partcheck import check_clips, check_ear_thread, check_scenes_and_clips, check_windows
from videos.music.music63 import compute
from videos.music.music63.manifest import SCENES
from videos.music.variations import LEDGER

load = compute.load


def test_fingerprints():
    h = load("hook")
    assert h["result"][0]["track"] == h["truth"] and abs(h["result"][0]["offset_s"] - h["offset_s"]) < 0.1
    r = load("robust")
    bar, white = r["rates"]["bar"], r["rates"]["white"]
    assert bar[0] > 0.9 and bar[-1] < bar[0] and white[0] > 0.9
    f = load("falsematch")
    assert max(f["noise_top_votes"]) < min(f["true_votes"]) / 10
    assert f["fresh_top"][0]["votes"] < 60


def test_classifier_and_recommenders():
    h = load("horse")
    assert h["acc_hum"] > 0.8 and h["acc_clean"] < 0.6 and h["acc_fair"] > h["acc_clean"]
    r = load("recs")["recall"]
    assert r["als"] > r["popular"] > r["random"]
    c = load("recs")["cold"]
    assert c["content"] > c["random"]
    l = load("loop")
    assert l["gini"][-1] > l["gini_explore"][-1] > l["gini_own"][-1]
    p = load("playlist")
    assert p["length_smooth"] < 0.7 * p["length_random"]


def test_variation_63():
    v = load("variation")
    row = [r for r in LEDGER if r["part"] == 63][0]
    assert v["part"] == 63 and row["measure"] == v["measure"] and row["seconds"] == pytest.approx(v["seconds"], abs=0.05)


def test_the_part_keeps_the_series_rules():
    check_clips(compute)
    check_scenes_and_clips(compute, SCENES)
    check_windows(compute, SCENES)
    check_ear_thread(compute, SCENES)
