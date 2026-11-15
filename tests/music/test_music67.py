"""Part 67 of *Music, Built*: what the film says is what was computed, and every sound keeps the series' rules.

    python -m pytest -q tests/music/test_music67.py
"""

import numpy as np
import pytest

from tests.music.partcheck import check_clips, check_ear_thread, check_scenes_and_clips, check_windows
from videos.music.music67 import compute
from videos.music.music67.manifest import SCENES
from videos.music.variations import LEDGER

load = compute.load


def test_sources_and_canon():
    s = load("stemma")
    assert min(s["witness_errors"]) >= 2 and s["majority_errors"] <= min(s["witness_errors"]) and s["branch_errors"] < min(s["witness_errors"])
    assert s["rf"]["recovered"] >= s["rf"]["true_splits"] - 2
    c = load("canon")["rows"]
    assert c["chorales"]["steps"]["lo"] > c["tunes"]["steps"]["hi"]           # the intervals do not overlap


def test_literature_and_power():
    m = load("meta")
    assert m["first"]["est"] > 8 * m["true"] and m["fe_published"] > 2 * m["true"] and abs(m["fe_all"] - m["true"]) < 0.05
    p = load("power")
    assert p["needed"]["0.6"] == 158 and p["twenty"]["0.6"]["power"] < 0.15
    ph = load("phack")["rates"]
    assert ph["none"] < 0.07 and ph["ABCD"] > 0.5


def test_data_audit_and_repro():
    l = load("leakage")
    assert np.mean(l["leaky"]) < np.mean(l["honest"]) - 0.3
    a = load("audit")
    assert a["p65_best_order"]["share"] == pytest.approx(0.7) and a["p66_false_alarms"]["above5"] == 0
    assert load("repro")["equal"]
    t = load("tappers")
    assert t["a_vs_b"] < max(t["a_vs_played"], t["b_vs_played"])


def test_variation_67():
    v = load("variation")
    row = [r for r in LEDGER if r["part"] == 67][0]
    assert v["part"] == 67 and row["measure"] == v["measure"] and row["seconds"] == pytest.approx(v["seconds"], abs=0.05)


def test_the_part_keeps_the_series_rules():
    check_clips(compute)
    check_scenes_and_clips(compute, SCENES)
    check_windows(compute, SCENES)
    check_ear_thread(compute, SCENES)
