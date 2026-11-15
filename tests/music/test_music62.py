"""Part 62 of *Music, Built*: what the film says is what was computed, and every sound keeps the series' rules.

    python -m pytest -q tests/music/test_music62.py
"""

import pytest

from tests.music.partcheck import check_clips, check_ear_thread, check_scenes_and_clips, check_windows
from videos.music.music62 import compute
from videos.music.music62.manifest import SCENES
from videos.music.variations import LEDGER

load = compute.load


def test_tempo_beats_downbeats():
    t = load("tempo")
    assert t["bpm"] == pytest.approx(100, abs=1) and t["slow_found"] == pytest.approx(100, abs=2) and t["slow_flat"] == pytest.approx(50, abs=1)
    b = load("beats")
    assert b["session"]["f"] > 0.9
    assert max(r["f"] for r in b["rubato"]["rows"]) < b["session"]["f"]
    h = load("halfdouble")
    assert h["scores"]["levels"]["double"] > 0.85
    d = load("downbeat")
    s = d["strength"]
    assert min(s[0], s[2]) > max(s[1], s[3])


def test_chords_align_structure():
    c = load("chords")["acc"]
    assert c["bach"] > c["hmm"] >= c["frame"] - 0.02
    a = load("align")
    assert a["err_ms"] < 40 and a["online_ms"] < 60
    cv = load("cover")["scores"]
    assert cv["cover"]["shift"] == 5 and cv["cover"]["cost"] < cv["other"]["cost"]
    s = load("structure")
    assert s["phrase_labels"] == ["a", "b", "c", "c", "a", "b"]


def test_variation_62():
    v = load("variation")
    row = [r for r in LEDGER if r["part"] == 62][0]
    assert v["part"] == 62 and row["measure"] == v["measure"] and row["seconds"] == pytest.approx(v["seconds"], abs=0.05)
    assert load("follow")["median_ms"] < 200


def test_the_part_keeps_the_series_rules():
    check_clips(compute)
    check_scenes_and_clips(compute, SCENES)
    check_windows(compute, SCENES)
    check_ear_thread(compute, SCENES)
