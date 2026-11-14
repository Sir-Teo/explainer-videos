"""Part 21 of *Music, Built*: what the film says is what was computed, and every sound keeps the series' rules.

    python -m pytest -q tests/music/test_music21.py
"""

import numpy as np
import pytest

from tests.music.partcheck import check_clips, check_ear_thread, check_scenes_and_clips, check_windows
from videos.music.music21 import compute
from videos.music.music21.manifest import SCENES
from videos.music.variations import LEDGER

load = compute.load


def test_tune_and_novelty():
    t = load("tune")
    assert t["labels"] == ["A", "B", "C", "C", "A", "B"] and t["truth"] == [8, 16, 24, 32, 40]
    assert t["score"]["hits"] == 5 and len(t["found"]) == 10
    for key in ("ssm_melody", "ssm_notes", "ssm_audio"):
        S = np.array(t[key])
        assert np.allclose(S, S.T, atol=2e-3) and np.allclose(np.diag(S), 1.0, atol=2e-3)


def test_sonata_and_segmenter():
    s = load("sonata")
    assert s["total"] == 128 and s["golden"]["rest"] == pytest.approx(0.625)
    assert s["score"]["hits"] == 9 and len(s["truth"]) == 11 and len(s["found"]) == 11
    keys = [k["key"] for k in s["keys"]]
    assert keys[0] == "C major" and "G major" in keys[8:20] and "A minor" in keys and "D minor" in keys and keys[-1] == "C major"
    g = load("segment")
    best = {k: max(x["f"] for x in v["by_width"].values()) for k, v in g["pieces"].items()}
    assert best["sonata"] == pytest.approx(9 / 11) and min(best, key=best.get) == "variations"
    assert g["best_width"] == "8" and round(100 * g["summary"]["8"]["f"]) == 44


def test_repetition_golden_and_forms():
    r = load("repetition")
    assert round(100 * r["mean"]) == 32 and round(100 * r["mean_shuffled"]) == 1 and round(100 * r["tune"]["share"]) == 64
    go = load("golden")
    assert go["hits"] == 2 and go["in_first_half"] == 37 and go["base_rate"] == pytest.approx(0.16)
    f = load("forms")
    assert set(f) - {"clips"} == set(compute.PLANS) and set(f["clips"]) == set(compute.HEARD)


def test_variation_21():
    v = load("variation")
    row = [r for r in LEDGER if r["part"] == 21][0]
    assert v["part"] == 21 and row["measure"] == v["measure"] and row["seconds"] == pytest.approx(v["seconds"], abs=0.05)


def test_the_part_keeps_the_series_rules():
    check_clips(compute)
    check_scenes_and_clips(compute, SCENES)
    check_windows(compute, SCENES)
    check_ear_thread(compute, SCENES)
