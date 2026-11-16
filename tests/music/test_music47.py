"""Part 47 of *Music, Built*: what the film says is what was computed, and every sound keeps the series' rules.

    python -m pytest -q tests/music/test_music47.py
"""

import numpy as np
import pytest

from tests.music.partcheck import check_clips, check_ear_thread, check_scenes_and_clips, check_windows
from videos.music.music47 import compute
from videos.music.music47.manifest import SCENES
from videos.music.variations import LEDGER

load = compute.load


def test_flute_and_universals():
    h = load("hook")
    assert 700 < h["hz"][0] < 800 and all(b > a for a, b in zip(h["hz"], h["hz"][1:]))
    assert max(h["steps"]) - min(h["steps"]) > 100                       # even holes, uneven steps
    u = load("universals")["share"]
    assert u["small intervals"] == 1.0 and u["on a beat"] == 1.0 and u["descending or arched"] < 0.8


def test_priors_are_revealed():
    r = load("rhythm")
    for k, top in (("A", "1-1-2"), ("B", "2-2-3")):
        m = r[k]["mass"]
        assert m[0] < 0.35 and m[-1] > 0.6
        end = r[k]["end_share"]
        assert max((v, p) for p, v in end.items() if p != "none")[1] == top
    assert r["example"]["near"] == [2, 1, 2]
    # Four two-second cycles, 0.4 seconds of decay, and a 1.2-second gap.
    assert r["starts"]["start"] == 0.0
    assert r["starts"]["end"] == pytest.approx(9.6)


def test_transmission_builds_structure():
    c = load("chains")
    s = c["stats"]
    assert s["levels"][-1][1] < 0.6 * s["levels"][0][1] and s["step"][-1][1] < 0.6 * s["step"][0][1]
    assert s["simple"][-1][1] > 0.9 > s["simple"][0][1]
    assert c["error"][-1] < 0.5 * c["error"][0]
    sm = load("sampling")
    assert sm["sample"]["mean"][-1] > sm["best"]["mean"][-1]


def test_families_and_language():
    f = load("family")
    assert np.mean(f["trials"]) > np.mean(f["random"]) + 2
    r = load("relatives")
    assert r["nearest"]["the Tune"] in ("Alphabet Song", "Baa, Baa, Black Sheep")
    n = load("npvi")
    assert n["folk"]["French"]["mean"] < n["folk"]["English"]["mean"] and n["test"]["p"] > 0.05
    assert n["by_kind"]["song"] > n["by_kind"]["keyboard"]


def test_beat_and_bias():
    b = load("beat")["stats"]
    assert b["on"]["p"] < 1e-6 and b["off"]["p"] > 0.1
    m = load("mozart")["0.0"]
    assert m["mean_published"] > 0.1 > abs(m["mean_all"])


def test_variation_47():
    v = load("variation")
    row = [r for r in LEDGER if r["part"] == 47][0]
    assert v["part"] == 47 and row["measure"] == v["measure"] and row["seconds"] == pytest.approx(v["seconds"], abs=0.05)


def test_the_part_keeps_the_series_rules():
    check_clips(compute)
    check_scenes_and_clips(compute, SCENES)
    check_windows(compute, SCENES)
    check_ear_thread(compute, SCENES)
