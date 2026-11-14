"""Part 40 of *Music, Built*: what the film says is what was computed, and every sound keeps the series' rules.

    python -m pytest -q tests/music/test_music40.py
"""

import pytest

from tests.music.partcheck import check_clips, check_ear_thread, check_scenes_and_clips, check_windows
from videos.music.music40 import compute
from videos.music.music40.manifest import SCENES
from videos.music.variations import LEDGER

load = compute.load


def test_hook_and_forms():
    h = load("hook")
    assert h["enters"]["long"] == pytest.approx(20.0) and h["enters"]["short"] == pytest.approx(5.0)
    f = load("forms")
    assert [n for n, _ in f["aaba"]] == ["A", "A", "B", "A"]


def test_loops_beats_808():
    l = load("loops")
    assert l["divorce"]["on_beat"] == 12 and l["divorce"]["outside"] == 4
    b = load("beats")
    assert b["backbeat"]["rock"] == 1.0 and b["backbeat"]["trap"] == 0.0
    e = load("eight")
    assert abs(e["pitch"] - 52.0) < 1.0 and e["pitch_attack"] > 60


def test_flow_and_drop():
    f = load("flow")
    A, B = f["stats"]["beat"], f["stats"]["threes"]
    assert A["syllables"] == B["syllables"] == 40 and A["rhyme_share"] == B["rhyme_share"]
    assert A["on_beat"] > B["on_beat"] and B["gap_counts"]["3"] > A["gap_counts"].get("3", 0)
    assert f["prosody"]["good"]["agree"] == 1.0 and f["prosody"]["bad"]["agree"] == 0.25
    d = load("drop")
    assert d["answer"] == "second" and min(d["gain_shape"]) < 0.25


def test_variation_40():
    t = load("tune")
    assert t["voice_enters"] < 6.0 and len(t["order"]) == 16
    v = load("variation")
    row = [r for r in LEDGER if r["part"] == 40][0]
    assert v["part"] == 40 and row["measure"] == v["measure"] and row["seconds"] == pytest.approx(v["seconds"], abs=0.05)


def test_the_part_keeps_the_series_rules():
    check_clips(compute)
    check_scenes_and_clips(compute, SCENES)
    check_windows(compute, SCENES)
    check_ear_thread(compute, SCENES)
