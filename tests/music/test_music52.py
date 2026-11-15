"""Part 52 of *Music, Built*: what the film says is what was computed, and every sound keeps the series' rules.

    python -m pytest -q tests/music/test_music52.py
"""

import numpy as np
import pytest

from tests.music.partcheck import check_clips, check_ear_thread, check_scenes_and_clips, check_windows
from videos.music.music52 import compute
from videos.music.music52.manifest import SCENES
from videos.music.variations import LEDGER

load = compute.load


def test_fm_claims():
    b = load("bessel")
    assert b["max_err"] < 1e-4
    dx = load("dx")["feedback"]
    saw = 20 * np.log10(1 / np.arange(1, 9))
    assert dx["0.0"][1] < -100 and np.max(np.abs(np.array(dx["1.5"][1:4]) - saw[1:4])) < 3.0
    assert load("hook")["answer"] == "second"


def test_grains_and_spectral():
    g = load("gabor")["rows"]
    assert g[0]["bw"] > 3 * g[1]["bw"] > 9 * g[2]["bw"]
    s = load("spectral")
    assert s["resid_early"] > s["resid_late"] + 30 and s["cents"][-1] > 100 and 2e-4 < s["B"] < 6e-4


def test_physical_models():
    k = load("ks")
    assert max(abs(x) for x in k["untuned"]) > 20 and max(abs(x) for x in k["tuned"]) < 1.0
    assert load("waveguide")["max_err"] < 1e-12
    c = load("clarinet")
    r = np.array(c["rms"])
    assert r[0] < 0.01 and r.max() > 0.3 and r[-1] < 0.05 and c["harmonics"][1] < -40
    m = load("modal")
    cents = [x for _, x in m["cents"]]
    assert cents[-1] < -10 and abs(cents[0]) < 2 and m["answer"] == "second"


def test_variation_52():
    v = load("variation")
    row = [r for r in LEDGER if r["part"] == 52][0]
    assert v["part"] == 52 and row["measure"] == v["measure"] and row["seconds"] == pytest.approx(v["seconds"], abs=0.05)


def test_the_part_keeps_the_series_rules():
    check_clips(compute)
    check_scenes_and_clips(compute, SCENES)
    check_windows(compute, SCENES)
    check_ear_thread(compute, SCENES)
