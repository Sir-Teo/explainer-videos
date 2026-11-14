"""Part 25 of *Music, Built*: what the film says is what was computed, and every sound keeps the series' rules.

    python -m pytest -q tests/music/test_music25.py
"""

import pytest

from tests.music.partcheck import check_clips, check_ear_thread, check_scenes_and_clips, check_windows
from videos.music.music25 import compute
from videos.music.music25.manifest import SCENES
from videos.music.variations import LEDGER

load = compute.load


def test_galilei_and_corelli():
    h = load("hook")
    assert h["pairs"]["A"]["cents"] == pytest.approx(600.0) and h["pairs"]["B"]["cents"] == pytest.approx(1200.0)
    assert h["mersenne"][2]["hz"] == pytest.approx(2 * h["mersenne"][0]["hz"]) and h["mersenne"][3]["hz"] == pytest.approx(3 * h["mersenne"][0]["hz"])
    c = load("corelli")
    assert c["notes"] == 101 and c["figure_counts"][""] == 61 and c["figure_counts"]["6"] == 17 and c["figure_counts"]["7"] == 15
    assert c["agreement"]["pitch_classes"] == pytest.approx(0.804, abs=0.002) and c["agreement"]["top"] == pytest.approx(0.277, abs=0.002)
    assert c["parallels"] == 0


def test_keys_modes_ritornello():
    k = load("keys")
    assert k["werck_C"]["third_error"] == pytest.approx(3.91, abs=0.01) and k["werck_Fs"]["third_error"] == pytest.approx(21.51, abs=0.01)
    mt = {r["key"]: r["third_error"] for r in k["table"]["quarter-comma meantone"]}
    assert sum(1 for v in mt.values() if abs(v) < 0.01) == 8 and sum(1 for v in mt.values() if v > 40) == 4
    w = load("wolf")
    assert w["good"] == pytest.approx(696.58, abs=0.01) and w["wolf"] == pytest.approx(737.64, abs=0.01)
    m = load("modes")
    assert m["palestrina"]["ion"] + m["palestrina"]["aeo"] == 441 and m["bach"]["major"] == 185 and m["bach"]["minor"] == 178
    r = load("ritornello")
    assert [f["transpose"] for f in r["found"]] == [0, 7, 0]                # the minor-mode head is missed


def test_variation_25():
    t = load("tune")
    assert t["ornaments"] == 26
    v = load("variation")
    row = [r for r in LEDGER if r["part"] == 25][0]
    assert v["part"] == 25 and row["measure"] == v["measure"] and row["seconds"] == pytest.approx(v["seconds"], abs=0.05)


def test_the_part_keeps_the_series_rules():
    check_clips(compute)
    check_scenes_and_clips(compute, SCENES)
    check_windows(compute, SCENES)
    check_ear_thread(compute, SCENES)
