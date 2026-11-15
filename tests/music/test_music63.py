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
    assert h["acc_hum"] > 0.75 and h["acc_clean"] < 0.6 and h["acc_fair"] < h["majority"] + 0.05     # honest: chance
    assert h["lowest_three_bands"]["hum"] > 2 * h["lowest_three_bands"]["fair"]
    r = load("recs")["recall"]
    assert r["als"] > r["popular"] > r["random"]
    c = load("recs")["cold"]
    assert c["content"] > c["random"]
    l = load("loop")
    assert l["gini"][-1] > l["gini_explore"][-1] > l["gini_own"][-1]
    p = load("playlist")
    assert p["length_smooth"] < 0.7 * p["length_random"]


def test_the_new_sections():
    m = load("matches")
    on = sum(1 for d in m["diff_true"] if abs(d - m["offset_s"]) < 0.1)
    assert on > 3 * max(1, len(m["wrong"]) // 4) and on > len(m["true"]) / 5
    L = load("length")["rates"]["0"]
    assert L[0] < L[-1] and L[-1] > 0.7
    sp = load("speed")
    assert sp["rates"][0] > 0.95 and sp["rates"][4] < 0.1 and sp["found_fast"] != sp["truth"]
    s = load("sampled")["sample_found"]
    assert s[0] > 0.8 and s[-1] < s[0]
    h = load("hum")
    assert h["rank_of_tune"] == 1 and h["fingerprint"][0]["votes"] < 30
    lo = load("lorenz")["top10"]
    assert lo["rec"] > lo["explore"] > lo["own"]
    sc = load("scale")["rows"]
    assert sc[-1]["tail"]["6"] < 1e-12 < sc[-1]["tail"]["3"]
    n = load("neighbours")
    assert n["dist"][2] > 2.5 * n["median_dist"] and max(n["dist"][1], n["dist"][3]) < n["median_dist"] / 3
    lp = load("lengthpair")
    assert lp["eight"]["ok"] and not lp["one"]["ok"]


def test_variation_63():
    v = load("variation")
    row = [r for r in LEDGER if r["part"] == 63][0]
    assert v["part"] == 63 and row["measure"] == v["measure"] and row["seconds"] == pytest.approx(v["seconds"], abs=0.05)


def test_the_part_keeps_the_series_rules():
    check_clips(compute)
    check_scenes_and_clips(compute, SCENES)
    check_windows(compute, SCENES)
    check_ear_thread(compute, SCENES)
